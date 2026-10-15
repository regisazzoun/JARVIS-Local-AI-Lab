from pathlib import Path
import subprocess,json,hashlib,re,datetime
p=Path(__file__).parent;src=p.parent/'mission05B-P-preuves';checks={};data={}
def run(name,cmd):
 r=subprocess.run(cmd,capture_output=True,text=True);(p/(name+'.txt')).write_text(r.stdout);(p/(name+'.stderr')).write_text(r.stderr);data[name]={'argv':cmd,'returncode':r.returncode};return r
info=json.loads((p/'installation-resultat.json').read_text());checks['apt_return_zero']=info.get('returncode')==0
r=run('dpkg-audit-final',['sudo','-n','dpkg','--audit']);checks['dpkg_coherent']=r.returncode==0 and not r.stdout.strip()
r=run('paquets-finaux',['dpkg-query','-W','-f=${binary:Package}\t${db:Status-Status}\t${Version}\n']);after={a:(b,c) for a,b,c in (l.split('\t') for l in r.stdout.splitlines())}
b=Path(json.loads((p/'sauvegarde-validation.json').read_text())['path']);before={a:(b,c) for a,b,c in (l.split('\t') for l in (b/'paquets.tsv').read_text().splitlines())}
changes={k:{'before':v,'after':after.get(k)} for k,v in before.items() if v[0]=='installed' and after.get(k)!=v}
added={k:v for k,v in after.items() if v[0]=='installed' and before.get(k,('',))[0]!='installed'}
expected=json.loads((src/'transaction-exacte.json').read_text());checks['existing_packages_unchanged']=not changes
checks['exact_29_new_packages']=len(added)==29 and {k.split(':')[0]:v[1] for k,v in added.items()}=={d['Package']:d['Version'] for d in expected}
(p/'paquets-difference.json').write_text(json.dumps({'added':added,'existing_changed':changes},indent=2))
r=run('dkms-final',['sudo','-n','/usr/sbin/dkms','status']);kernels=['6.12.111+deb13-amd64','6.18.54-1-t2-trixie'];checks['dkms_both_kernels']=r.returncode==0 and all(f'nvidia/595.91.07, {k}, x86_64: installed' in r.stdout for k in kernels)
mods={}
for k in kernels:
 mods[k]={}
 for m in ['nvidia','nvidia_modeset','nvidia_drm','nvidia_uvm','nvidia_peermem']:
  rr=run('modinfo-'+k+'-'+m,['/usr/sbin/modinfo','-k',k,m]);fields={}
  for l in rr.stdout.splitlines():
   if ':' in l:
    a,c=l.split(':',1);fields.setdefault(a.strip(),[]).append(c.strip())
  mods[k][m]=fields
  checks['module_'+k+'_'+m]=rr.returncode==0 and fields.get('version')==['595.91.07'] and fields.get('vermagic',[''])[0].startswith(k+' ') and Path(fields.get('filename',['/not-present'])[0]).is_file()
 checks['open_license_'+k]=mods[k]['nvidia'].get('license')==['Dual MIT/GPL']
(p/'modules-verification.json').write_text(json.dumps(mods,indent=2))
r=run('logs-dkms-inventaire',['sudo','-n','find','/var/lib/dkms/nvidia/595.91.07','-type','f','-name','make.log']);logs=[]
for i,f in enumerate(r.stdout.splitlines()):
 rr=run('dkms-make-'+str(i),['sudo','-n','cat',f]);errors=[l for l in rr.stdout.splitlines() if re.search(r'(?i)fatal error:|\berror:|\bError [0-9]+|error!',l)];warnings=[l for l in rr.stdout.splitlines() if 'warning:' in l.lower()];logs.append({'path':f,'saved_as':'dkms-make-'+str(i)+'.txt','error_lines':errors,'warning_lines':warnings})
checks['dkms_logs_no_errors']=len(logs)>=2 and all(not l['error_lines'] for l in logs);(p/'dkms-logs-analyse.json').write_text(json.dumps(logs,indent=2))
r=run('firmware-verify',['sudo','-n','dpkg','--verify','firmware-nvidia-gsp']);checks['firmware_package_integrity']=r.returncode==0 and not r.stdout.strip()
firm={}
for n in ['gsp_tu10x.bin','gsp_ga10x.bin']:
 f=Path('/lib/firmware/nvidia/595.91.07')/n;firm[n]={'exists':f.is_file(),'size':f.stat().st_size if f.exists() else None,'sha256':hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else None}
checks['gsp_firmware_present']=all(v['exists'] and v['size']>0 for v in firm.values());(p/'firmware-verification.json').write_text(json.dumps(firm,indent=2))
r=run('initramfs-apres-liste',['/usr/bin/lsinitramfs','/boot/initrd.img-6.18.54-1-t2-trixie']);checks['initramfs_readable']=r.returncode==0
old=set((p/'initramfs-avant-liste.txt').read_text().splitlines());new=set(r.stdout.splitlines());critical=[l for l in old if any(s in l for s in ['/i915.ko','/nvme.ko','/dm-mod.ko','/ext4.ko','t2bce','hid-apple','/lvm.rules']) or l in ['init','scripts/local','usr/sbin/lvm','usr/sbin/dmsetup','etc/lvm/lvm.conf'] or re.search(r'/[0-9]+-lvm\.rules$',l)]
missing=sorted(set(critical)-new);checks['boot_components_preserved']=not missing and all(any(s in l for l in new) for s in ['/i915.ko','/nvme.ko','/dm-mod.ko','/ext4.ko','usr/sbin/lvm','usr/sbin/dmsetup'])
(p/'initramfs-comparaison.json').write_text(json.dumps({'old_entry_count':len(old),'new_entry_count':len(new),'critical_entries':critical,'missing_critical':missing,'removed':sorted(old-new),'added':sorted(new-old),'t2bce_before':[l for l in old if 't2bce' in l],'t2bce_after':[l for l in new if 't2bce' in l],'nvidia_after':[l for l in new if 'nvidia' in l.lower()]},indent=2))
r=run('boot-hashes-final',['sudo','-n','sha256sum','/boot/grub/grub.cfg','/boot/vmlinuz-6.18.54-1-t2-trixie','/boot/initrd.img-6.18.54-1-t2-trixie']);oldhash={l.split(None,1)[1].strip():l.split()[0] for l in (b/'boot-sha256.txt').read_text().splitlines()};hashes={l.split(None,1)[1].strip():l.split()[0] for l in r.stdout.splitlines()};checks['grub_kernel_hashes_unchanged']=all(hashes.get(f)==oldhash.get(f) for f in ['/boot/grub/grub.cfg','/boot/vmlinuz-6.18.54-1-t2-trixie']);checks['initramfs_regenerated']=hashes.get('/boot/initrd.img-6.18.54-1-t2-trixie')!=oldhash.get('/boot/initrd.img-6.18.54-1-t2-trixie')
r=run('pci-final',['lspci','-Dnnk']);checks['core_still_absent']='[10de:' not in r.stdout and r.returncode==0;checks['intel_i915_bound']='0000:00:02.0' in r.stdout and 'Kernel driver in use: i915' in r.stdout
r=run('lsmod-final',['lsmod']);checks['no_nvidia_loaded']=not any(l.startswith(('nvidia','nouveau')) for l in r.stdout.splitlines());checks['i915_loaded']=any(l.startswith('i915 ') for l in r.stdout.splitlines())
r=run('services-final',['systemctl','is-active','sddm','ssh','ssh.socket']);checks['services_active']=r.returncode==0 and r.stdout.splitlines()==['active']*3
r=run('session-finale',['loginctl','show-session','5','-p','Type','-p','Desktop','-p','Active','-p','State']);checks['gnome_wayland_active']=all(s in r.stdout for s in ['Desktop=GNOME','Type=wayland','Active=yes','State=active'])
r=run('gnome-process-final',['pgrep','-x','gnome-shell']);checks['gnome_same_pid']=r.returncode==0 and r.stdout==(p/'gnome-initial.txt').read_text()
r=run('boot-id-final',['cat','/proc/sys/kernel/random/boot_id']);checks['same_boot_id']=r.stdout==(p/'boot-id-initial.txt').read_text()
r=run('cmdline-final',['cat','/proc/cmdline']);checks['same_cmdline']=r.stdout==(p/'cmdline-initial.txt').read_text()
r=run('persistance-avant-fin',['systemctl','show','nvidia-persistenced','-p','ActiveState','-p','UnitFileState','-p','LoadState','-p','MainPID']);checks['persistance_not_running']='ActiveState=inactive' in r.stdout and 'MainPID=0' in r.stdout
run('services-pids',['systemctl','show','sddm','ssh','ssh.socket','-p','MainPID','-p','ActiveState','-p','ExecMainStartTimestampMonotonic'])
run('ldconfig-cache',['/usr/sbin/ldconfig','-p']);run('espace-final',['df','-h','/','/boot'])
result={'time':datetime.datetime.now().astimezone().isoformat(),'checks':checks,'commands':data,'all_passed':all(checks.values()),'failed':[k for k,v in checks.items() if not v]};(p/'validation-complete.json').write_text(json.dumps(result,indent=2));print(json.dumps({'all_passed':result['all_passed'],'failed':result['failed'],'checks_count':len(checks),'dkms_log_warnings':[len(l['warning_lines']) for l in logs]},indent=2))

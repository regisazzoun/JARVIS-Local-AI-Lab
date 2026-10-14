from pathlib import Path
import subprocess,json,datetime,hashlib,shutil
out=Path(__file__).resolve().parent
metadata={'debut':datetime.datetime.now().astimezone().isoformat(),'commandes':{}}
def command(name,args):
 r=subprocess.run(args,capture_output=True)
 (out/(name+'.txt')).write_bytes(r.stdout);(out/(name+'.stderr')).write_bytes(r.stderr)
 metadata['commandes'][name]={'argv':args,'code':r.returncode}
 return r.stdout
commands={
'identite':['uname','-a'],'journal-noyau':['sudo','-n','journalctl','-b','-k','--no-pager','-o','short-monotonic'],
'journal-systeme':['sudo','-n','journalctl','-b','--no-pager','-o','short-iso-precise'],
'dmesg':['sudo','-n','dmesg','--time-format=raw'],'journal-precedent-noyau':['sudo','-n','journalctl','-b','-1','-k','--no-pager','-o','short-monotonic'],
'journal-sddm':['sudo','-n','journalctl','-b','-u','sddm','--no-pager'],'boots':['sudo','-n','journalctl','--list-boots','--no-pager'],
'pci':['lspci','-Dnnk'],'pci-arbre':['lspci','-Dtv'],'seat':['loginctl','show-seat','seat0','-a'],
'processus':['ps','-eo','pid,user,comm,args'],'services':['systemctl','show','graphical.target','display-manager.service','ssh.service','ssh.socket','-p','Id','-p','ActiveState','-p','SubState','-p','MainPID','-p','ActiveEnterTimestamp'],
'sessions':['loginctl','list-sessions'],'modules':['lsmod'],'reseau':['ip','-br','address'],
'routes':['ip','route'],'connexions':['ss','-tn'],'stockage':['lsblk','-o','NAME,TYPE,FSTYPE,SIZE,MOUNTPOINTS'],'montages':['findmnt','/'],
'bolt':['boltctl','list'],'udev-framebuffer':['sudo','-n','udevadm','info','-q','all','-p','/sys/class/graphics/fb0']}
for name,args in commands.items():command(name,args)
files={'boot-id':'/proc/sys/kernel/random/boot_id','cmdline':'/proc/cmdline','iomem':'/proc/iomem','ioports':'/proc/ioports','fb':'/proc/fb','resource-alignment':'/sys/bus/pci/resource_alignment','nvme-state':'/sys/class/nvme/nvme0/state','ethernet-carrier':'/sys/class/net/enp4s0/carrier','ethernet-speed':'/sys/class/net/enp4s0/speed','sddm-state':'/var/lib/sddm/state.conf','produit':'/sys/class/dmi/id/product_name','bios-version':'/sys/class/dmi/id/bios_version','bios-date':'/sys/class/dmi/id/bios_date'}
for name,path in files.items():command(name,['sudo','-n','cat',path])
pci={}
for d in sorted(Path('/sys/bus/pci/devices').iterdir()):
 v={'path':str(d.resolve()),'driver':str((d/'driver').resolve()) if (d/'driver').exists() else None}
 for f in ['vendor','device','class','resource','boot_vga','enable','power/runtime_status','aer_dev_correctable','aer_dev_nonfatal','aer_dev_fatal']:
  try:v[f]=(d/f).read_text()
  except OSError:v[f]=None
 if v['class'].startswith('0x0604') or d.name in ['0000:00:00.0','0000:81:00.0']:
  r=subprocess.run(['sudo','-n','dd','if='+str(d/'config'),'bs=64','count=1','status=none'],capture_output=True)
  (out/('config-'+d.name+'.bin')).write_bytes(r.stdout)
  metadata['commandes']['config-'+d.name]={'code':r.returncode,'taille':len(r.stdout),'stderr':r.stderr.decode()}
 pci[d.name]=v
(out/'pci-sysfs.json').write_text(json.dumps(pci,indent=2))
for t in sorted(Path('/sys/firmware/acpi/tables').iterdir()):
 if t.is_file():
  r=subprocess.run(['sudo','-n','cat',str(t)],capture_output=True);(out/('acpi-'+t.name+'.bin')).write_bytes(r.stdout)
  metadata['commandes']['acpi-'+t.name]={'code':r.returncode,'taille':len(r.stdout),'stderr':r.stderr.decode()}
acpi={}
for d in sorted(Path('/sys/bus/acpi/devices').iterdir()):
 v={}
 for f in ['path','hid','status','modalias']:
  try:v[f]=(d/f).read_text()
  except OSError:pass
 acpi[d.name]=v
(out/'acpi-sysfs.json').write_text(json.dumps(acpi,indent=2))
command('etat-graphique',['sudo','-n','sh','-c','ls -la /sys/class/drm /dev/dri /sys/bus/pci/devices/0000:00:02.0; cat /sys/class/graphics/fb0/name /sys/class/graphics/fb0/modes /sys/class/graphics/fb0/virtual_size; cat /sys/class/vtconsole/vtcon*/name /sys/class/vtconsole/vtcon*/bind'])
comparison={}
for mission in ['04O','04P','04Q']:
 base=out.parent/('mission'+mission+'-preuves')
 if mission!='04Q':base=base/'initial'
 old=json.loads((base/'pci-sysfs.json').read_text())
 comparison[mission]={'absents':sorted(set(old)-set(pci)),'nouveaux':sorted(set(pci)-set(old)),'ressources_modifiees':{k:{'avant':old[k]['resource'],'actuel':pci[k]['resource']} for k in sorted(set(old)&set(pci)) if old[k]['resource']!=pci[k]['resource']},'pilotes_modifies':{k:{'avant':old[k]['driver'],'actuel':pci[k]['driver']} for k in sorted(set(old)&set(pci)) if old[k]['driver']!=pci[k]['driver']},'cmdline_identique':(base/('cmdline.txt' if mission=='04Q' else 'proc_cmdline.txt')).read_bytes()==(out/'cmdline.txt').read_bytes()}
 if mission!='04Q':
  comparison[mission]['acpi']={}
  for f in out.glob('acpi-*.bin'):
   oldfile=base/f.name
   comparison[mission]['acpi'][f.name]={'identique':oldfile.exists() and oldfile.read_bytes()==f.read_bytes(),'sha256_actuel':hashlib.sha256(f.read_bytes()).hexdigest(),'sha256_reference':hashlib.sha256(oldfile.read_bytes()).hexdigest() if oldfile.exists() else None}
(out/'comparaison.json').write_text(json.dumps(comparison,indent=2))
metadata['fin']=datetime.datetime.now().astimezone().isoformat()
(out/'collecte.json').write_text(json.dumps(metadata,indent=2))
print('Collecte achevée',metadata['fin'])
print(json.dumps({m:{k:v for k,v in x.items() if k!='acpi'} for m,x in comparison.items()},indent=2))
print('ACPI différentes:',{m:[k for k,v in x.get('acpi',{}).items() if not v['identique']] for m,x in comparison.items()})
print('Noeuds ACPI graphics:',{k:v for k,v in acpi.items() if any(s in v.get('path','') for s in ['IGPU','GFX','PCI0']) and (k.startswith('device:') or 'IGPU' in v.get('path','') or k.startswith('PNP0A'))})

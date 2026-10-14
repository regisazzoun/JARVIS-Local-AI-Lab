#!/usr/bin/env python3
# Lecture seule du système. Écrit uniquement une nouvelle archive dans le dossier indiqué.
from pathlib import Path
import subprocess,sys,json,datetime
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
def run(name,args):
 r=subprocess.run(args,capture_output=True,text=True)
 (out/name).write_text(r.stdout+'\nSTDERR:\n'+r.stderr+'\nEXIT: '+str(r.returncode)+'\n')
for name,args in [('noyau.log',['journalctl','-b','-k','-o','short-iso-precise','--no-pager']),('systeme.log',['journalctl','-b','-o','short-iso-precise','--no-pager']),('pci.txt',['lspci','-Dnnvvk']),('arbre.txt',['lspci','-Dtv']),('modules.txt',['lsmod']),('reseau.txt',['ip','-br','address']),('routes.txt',['ip','route']),('ssh.txt',['systemctl','status','ssh','ssh.socket','--no-pager']),('ecoutes.txt',['ss','-ltnp']),('iomem.txt',['cat','/proc/iomem']),('bolt.txt',['boltctl','list']),('bolt-domaines.txt',['boltctl','domains']),('connexions.txt',['ss','-tnp']),('journal-bolt.txt',['journalctl','-b','-u','bolt','--no-pager','-o','short-iso-precise'])]:run(name,args)
(out/'boot.txt').write_text(datetime.datetime.now().astimezone().isoformat()+'\n'+Path('/proc/cmdline').read_text()+Path('/proc/sys/kernel/random/boot_id').read_text())
data={}
for d in Path('/sys/bus/pci/devices').iterdir():
 if (d/'class').read_text().strip().startswith('0x0604') or ((d/'vendor').read_text().strip()=='0x10de' and (d/'device').read_text().strip()=='0x1eb0') or d.name=='0000:00:02.0':
  data[d.name]={'path':str(d.resolve()),'driver':str((d/'driver').resolve()) if (d/'driver').exists() else None}
  for f in ['resource','vendor','device','class','boot_vga','current_link_speed','current_link_width']:
   try:data[d.name][f]=(d/f).read_text()
   except OSError:pass
(out/'ressources.json').write_text(json.dumps(data,indent=2))
print('Archive:',out)

# Identification dynamique et chaîne, sans écriture PCIe.
gpus=[]
for d in Path('/sys/bus/pci/devices').iterdir():
 if (d/'vendor').read_text().strip()=='0x10de' and (d/'device').read_text().strip()=='0x1eb0':
  gpus.append({'bdf':d.name,'path':str(d.resolve())})
(out/'gpu-identification.json').write_text(json.dumps(gpus,indent=2))
for g in gpus:
 run('gpu-'+g['bdf'].replace(':','_')+'.txt',['lspci','-Dnnvvk','-s',g['bdf']])
state={}
for base,attrs in [('/sys/bus/thunderbolt/devices',['authorized','unique_id','device_name','security']),('/sys/class/drm',['status','enabled','modes']),('/sys/class/net',['operstate','carrier','speed'])]:
 for d in Path(base).iterdir():
  e={'path':str(d.resolve())}
  for f in attrs:
   try:e[f]=(d/f).read_text()
   except OSError:pass
  state[str(d)]=e
(out/'peripheriques.json').write_text(json.dumps(state,indent=2))
import hashlib
(out/'SHA256SUMS.json').write_text(json.dumps({f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.iterdir() if f.is_file()},indent=2))

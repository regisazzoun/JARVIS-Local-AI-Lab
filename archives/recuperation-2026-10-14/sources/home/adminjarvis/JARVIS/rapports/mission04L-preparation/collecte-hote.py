#!/usr/bin/env python3
"""Collecte préalable 04L. Lecture système uniquement ; écrit des preuves locales."""
import os, sys, subprocess, json, hashlib, datetime, shutil
from pathlib import Path
if os.geteuid() != 0:
    sys.exit('Exécuter depuis le terminal hôte avec sudo python3 ; aucune collecte privilégiée effectuée.')
base=Path('/home/adminjarvis/JARVIS/rapports/mission04L-preparation')
boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
out=base/('hote-'+boot+'-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
out.mkdir(parents=True, exist_ok=False)
records={}
def run(name, args):
    try:
        p=subprocess.run(args, capture_output=True, text=True, timeout=60)
        r={'command':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    except Exception as e: r={'command':args,'error':str(e)}
    (out/(name+'.json')).write_text(json.dumps(r,indent=2,ensure_ascii=False))
    records[name]={k:v for k,v in r.items() if k!='stdout'}
for name,args in {
 'identite':['id'], 'noyau':['uname','-a'], 'pci':['lspci','-Dnnvvk'],
 'arbre':['lspci','-Dtv'], 'journal-noyau':['journalctl','-b','-k','--no-pager','-o','short-iso-precise'],
 'journal-systeme':['journalctl','-b','--no-pager','-o','short-iso-precise'],
 'journal-bolt':['journalctl','-b','-u','bolt','--no-pager','-o','short-iso-precise'],
 'services':['systemctl','status','ssh.service','ssh.socket','display-manager.service','--no-pager'],
 'sessions':['loginctl','list-sessions'], 'reseau':['ip','-details','address'], 'routes':['ip','route'],
 'ecoutes':['ss','-lntp'], 'connexions':['ss','-ntp'], 'stockage':['lsblk','-o','NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,MODEL'],
 'montages':['findmnt'], 'bolt':['boltctl','list'], 'bolt-domaines':['boltctl','domains'],
 'processus':['ps','-eo','pid,user,comm,args'], 'dmi':['dmidecode','-t','system']
}.items(): run(name,args)
reads={}
def readfile(path, dest=None, binary=False):
    path=Path(path)
    try:
        data=path.read_bytes()
        reads[str(path)]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        if dest: (out/dest).write_bytes(data)
        elif not binary: reads[str(path)]['text']=data.decode(errors='replace')
    except Exception as e: reads[str(path)]={'error':str(e)}
for path in ['/proc/cmdline','/proc/iomem','/proc/modules','/proc/self/status','/sys/bus/pci/resource_alignment','/sys/class/dmi/id/product_name']:
    readfile(path,path.replace('/','_').lstrip('_')+'.txt')
pci={}
for dev in sorted(Path('/sys/bus/pci/devices').glob('*')):
    r={'path':str(dev.resolve()),'driver':str((dev/'driver').resolve()) if (dev/'driver').exists() else None}
    for n in ['vendor','device','class','resource','boot_vga']:
        try:r[n]=(dev/n).read_text()
        except Exception as e:r[n]={'error':str(e)}
    if r.get('class','').__class__ is str and r['class'].strip().startswith('0x0604'):
        try:
            with (dev/'config').open('rb') as f:data=f.read(64)
            (out/('config-'+dev.name+'.bin')).write_bytes(data)
            r['config64']={'bytes':len(data),'hex':data.hex()}
            if len(data)>=48:
                lo=int.from_bytes(data[36:38],'little');hi=int.from_bytes(data[38:40],'little')
                r['pref_type_base']=lo&15;r['pref_type_limit']=hi&15
                start=(lo&0xfff0)<<16;end=((hi&0xfff0)<<16)|0xfffff
                if (lo&15)==1:start|=int.from_bytes(data[40:44],'little')<<32;end|=int.from_bytes(data[44:48],'little')<<32
                r['pref_range']={'start':hex(start),'end':hex(end),'enabled_range':start<=end,'bytes':end-start+1 if start<=end else 0}
        except Exception as e:r['config64']={'error':str(e)}
    pci[dev.name]=r
(out/'pci-sysfs.json').write_text(json.dumps(pci,indent=2))
for directory in ['/sys/class/drm','/sys/class/net','/sys/class/nvme','/sys/bus/thunderbolt/devices']:
    for dev in Path(directory).glob('*'):
        for n in ['status','enabled','modes','operstate','carrier','speed','state','model','device_name','authorized','security','unique_id','boot_acl']:
            if (dev/n).exists():readfile(dev/n)
for table in Path('/sys/firmware/acpi/tables').glob('*'):
    if table.is_file():readfile(table,'acpi-'+table.name+'.bin',True)
kernel=os.uname().release
for path in ['/boot/System.map-'+kernel,'/boot/config-'+kernel]:readfile(path,Path(path).name)
readfile('/boot/vmlinuz-'+kernel,binary=True)
# Lecture d'un état de santé, uniquement si smartctl est déjà installé.
if shutil.which('smartctl'):run('nvme-sante',['smartctl','-a','/dev/nvme0'])
(out/'lectures.json').write_text(json.dumps(reads,indent=2,ensure_ascii=False))
end=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
(out/'collecte.json').write_text(json.dumps({'boot_id':boot,'boot_id_fin':end,'date':datetime.datetime.now().astimezone().isoformat(),'commands':records,'writes':'preuves uniquement'},indent=2))
(out/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(out.iterdir()) if p.is_file()))
# Rendre les preuves accessibles au propriétaire du workspace sans modifier de fichiers système.
uid=base.stat().st_uid;gid=base.stat().st_gid
for p in [out,*out.iterdir()]:os.chown(p,uid,gid)
print('Preuves :',out)
print('Boot identique :',boot==end)
print('Collecte terminée ; aucune configuration modifiée. Les résultats doivent être examinés avant tout test.')

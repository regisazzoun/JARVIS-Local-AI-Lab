from pathlib import Path
import os,stat,hashlib,json,subprocess,datetime
w=Path(__file__).resolve().parent
assert os.geteuid()==0
before=json.loads((w/'empreintes-avant.json').read_text())
for name,r in before.items():
 p=Path(name);assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],name
 assert stat.S_IMODE(p.stat().st_mode)==r['mode'] and p.stat().st_uid==r['uid'] and p.stat().st_gid==r['gid'],name
assert Path('/proc/sys/kernel/random/boot_id').read_text()==(w/'boot-id-avant.txt').read_text()
name='46_jarvis_t2_egpu_reallocation_ciblee';source=(w/name).read_bytes();cfg=(w/'grub.cfg-genere').read_bytes();validation=json.loads((w/'validation-candidat.json').read_text())
assert hashlib.sha256(cfg).hexdigest()==validation['sha256_candidat']
block=b'\n### BEGIN /etc/grub.d/'+name.encode()+b' ###\n'+(w/'entree-candidate.cfg').read_bytes()+b'### END /etc/grub.d/'+name.encode()+b' ###\n'
assert cfg.count(block)==1 and cfg.replace(block,b'')==(w/'grub.cfg-avant').read_bytes()
assert b'\n'.join(source.splitlines()[2:])+b'\n'==(w/'entree-candidate.cfg').read_bytes()
subprocess.run(['grub-script-check',str(w/'grub.cfg-genere')],check=True)
dest=Path('/etc/grub.d')/name;cfgdest=Path('/boot/grub/grub.cfg');assert not dest.exists()
old=cfgdest.stat();a=dest.with_name('.'+name+'.mission04L');b=cfgdest.with_name('.grub.cfg.mission04L')
def stage(path,data,mode,uid,gid):
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,mode)
 with os.fdopen(fd,'wb') as f:
  f.write(data);f.flush();os.fchown(f.fileno(),uid,gid);os.fchmod(f.fileno(),mode);os.fsync(f.fileno())
try:
 stage(a,source,0o755,0,0);stage(b,cfg,stat.S_IMODE(old.st_mode),old.st_uid,old.st_gid)
 os.replace(a,dest)
 try:os.replace(b,cfgdest)
 except BaseException:
  dest.unlink();raise
finally:
 for p in [a,b]:
  if p.exists():p.unlink()
for directory in ['/etc/grub.d','/boot/grub']:
 fd=os.open(directory,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
assert dest.read_bytes()==source and cfgdest.read_bytes()==cfg
subprocess.run(['grub-script-check',str(cfgdest)],check=True)
unchanged=[]
for name,r in before.items():
 if name=='/boot/grub/grub.cfg':continue
 assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==r['sha256'],name
 unchanged.append(name)
result={'date':datetime.datetime.now().astimezone().isoformat(),'changes':[str(dest),str(cfgdest)],'sha256_grub':hashlib.sha256(cfg).hexdigest(),'sha256_source':hashlib.sha256(source).hexdigest(),'source_mode':oct(stat.S_IMODE(dest.stat().st_mode)),'grub_mode':oct(stat.S_IMODE(cfgdest.stat().st_mode)),'unchanged':unchanged,'boot_id_fin':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'cmdline_fin':Path('/proc/cmdline').read_text().strip()}
(w/'installation-resultat.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='unchanged'},indent=2));print('Autres fichiers vérifiés inchangés :',len(unchanged))

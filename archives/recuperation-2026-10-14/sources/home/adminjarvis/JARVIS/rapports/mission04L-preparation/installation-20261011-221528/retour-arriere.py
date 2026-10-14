"""Retire uniquement l'installation 04L, après autorisation. Ne redémarre pas."""
from pathlib import Path
import os,stat,json,hashlib,subprocess
w=Path(__file__).resolve().parent
assert os.geteuid()==0,'Exécution privilégiée requise'
result=json.loads((w/'installation-resultat.json').read_text());before=json.loads((w/'empreintes-avant.json').read_text());source=Path('/etc/grub.d/46_jarvis_t2_egpu_reallocation_ciblee');cfg=Path('/boot/grub/grub.cfg')
assert hashlib.sha256(cfg.read_bytes()).hexdigest()==result['sha256_grub'],'GRUB a évolué : réexaminer le retour arrière'
assert hashlib.sha256(source.read_bytes()).hexdigest()==result['sha256_source'],'Source a évolué : réexaminer le retour arrière'
for name,r in before.items():
 if name==str(cfg):continue
 assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==r['sha256'],'Fichier protégé a évolué : '+name
old=(w/'grub.cfg-avant').read_bytes();assert hashlib.sha256(old).hexdigest()==before[str(cfg)]['sha256']
subprocess.run(['grub-script-check',str(w/'grub.cfg-avant')],check=True)
meta=cfg.stat();tmp=cfg.with_name('.grub.cfg.retour04L');assert not tmp.exists();fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,stat.S_IMODE(meta.st_mode))
with os.fdopen(fd,'wb') as f:
 f.write(old);f.flush();os.fchown(f.fileno(),meta.st_uid,meta.st_gid);os.fchmod(f.fileno(),stat.S_IMODE(meta.st_mode));os.fsync(f.fileno())
try:
 os.replace(tmp,cfg);source.unlink()
finally:
 if tmp.exists():tmp.unlink()
for directory in ['/boot/grub','/etc/grub.d']:
 fd=os.open(directory,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
print('GRUB antérieur restauré et source 46 retirée. Aucun redémarrage exécuté.')

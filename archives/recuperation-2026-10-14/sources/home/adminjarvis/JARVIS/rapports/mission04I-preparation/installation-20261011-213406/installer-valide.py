import os,stat,json,hashlib,subprocess
from pathlib import Path
p=Path("/home/adminjarvis/JARVIS/rapports/mission04I-preparation")
w=Path((p/"dernier-dossier-installation.txt").read_text().strip())
before=json.loads((w/"empreintes-avant.json").read_text())
for f,h in before.items():
 assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h,f
source=(p/"45_jarvis_t2_egpu_reserve_512m").read_bytes()
expected=(p/"entree-grub-prevue.cfg").read_bytes()
assert b"\n".join(source.splitlines()[2:])+b"\n"==expected
assert b"pci=realloc=on pci=hpmmioprefsize=512M" in source
cfg=(w/"grub.cfg-genere").read_bytes()
assert cfg==(p/"grub.cfg-candidat").read_bytes()
assert hashlib.sha256(cfg).hexdigest()=="81be6b6101d1916fb9c62de50444959ee19b8a3dbbf714c8eb9c368f2919054d"
subprocess.run(["grub-script-check",str(w/"grub.cfg-genere")],check=True)
dest=Path("/etc/grub.d/45_jarvis_t2_egpu_reserve_512m")
assert not dest.exists()
old=Path("/boot/grub/grub.cfg").stat()
source_tmp=dest.with_name(".45_jarvis_t2_egpu_reserve_512m.installation")
cfg_dest=Path("/boot/grub/grub.cfg")
cfg_tmp=cfg_dest.with_name(".grub.cfg.mission04I")
def stage(path,content,mode,uid,gid):
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,mode)
 with os.fdopen(fd,"wb") as f:
  f.write(content);f.flush();os.fchown(f.fileno(),uid,gid);os.fchmod(f.fileno(),mode);os.fsync(f.fileno())
stage(source_tmp,source,0o755,0,0)
try:
 stage(cfg_tmp,cfg,stat.S_IMODE(old.st_mode),old.st_uid,old.st_gid)
 os.replace(source_tmp,dest)
 try:os.replace(cfg_tmp,cfg_dest)
 except BaseException:
  dest.unlink();raise
finally:
 for t in (source_tmp,cfg_tmp):
  if t.exists():t.unlink()
for d in ("/etc/grub.d","/boot/grub"):
 fd=os.open(d,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
assert dest.read_bytes()==source and cfg_dest.read_bytes()==cfg
print("Source 45 et GRUB actif installés ; source root:root 0755 ; mode GRUB conservé.")

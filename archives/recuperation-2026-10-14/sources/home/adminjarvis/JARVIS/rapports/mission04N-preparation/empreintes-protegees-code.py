import pathlib,hashlib,json
ps=[pathlib.Path('/etc/default/grub'),pathlib.Path('/boot/grub/grub.cfg'),pathlib.Path('/boot/grub/grubenv')]
ps+=list(pathlib.Path('/etc/grub.d').glob('*'))+list(pathlib.Path('/etc/default/grub.d').glob('*'))
ps+=[p for p in pathlib.Path('/boot').glob('*') if p.name.startswith(('vmlinuz-','initrd.img-','config-','System.map-'))]
print(json.dumps({str(p):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':oct(p.stat().st_mode & 0o7777),'uid':p.stat().st_uid,'gid':p.stat().st_gid} for p in ps if p.is_file()},indent=2))
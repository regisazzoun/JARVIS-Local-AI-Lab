#!/usr/bin/env python3
"""Overlay authenticated Debian netboot with pinned SSH supervision; never create RAID."""
import sys,copy,gzip,hashlib,json,lzma,os,pathlib,re,shutil,subprocess,urllib.request,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
os.umask(0o077)
b=ROOT/'private/reinstall-02'; b.mkdir(mode=0o700,exist_ok=True)
stage=b/'stage';stage.mkdir(exist_ok=True);assets=ROOT/'private/debian-verified'
subprocess.run(['gpgv','--keyring','/usr/share/keyrings/debian-archive-keyring.gpg',str(assets/'Release.gpg'),str(assets/'Release')],check=True,capture_output=True)
release=(assets/'Release').read_text().split('SHA256:\n')[1].split('\nSHA512:')[0]
checks={l.split()[2]:l.split()[0] for l in release.splitlines() if len(l.split())==3}
index=(assets/'installer-Packages.xz').read_bytes()
assert hashlib.sha256(index).hexdigest()==checks['main/debian-installer/binary-amd64/Packages.xz']
sums=(assets/'SHA256SUMS').read_bytes();assert hashlib.sha256(sums).hexdigest()==checks['main/installer-amd64/current/images/SHA256SUMS']
entries={l.split(maxsplit=1)[1].lstrip('*./'):l.split()[0] for l in sums.decode().splitlines()}
for n in ['linux','initrd.gz']:assert hashlib.sha256((assets/n).read_bytes()).hexdigest()==entries['netboot/debian-installer/amd64/'+n]
pkgs={}
for para in lzma.decompress(index).decode().split('\n\n'):
 d=dict(l.split(': ',1) for l in para.splitlines() if ': ' in l and not l.startswith(' '))
 if 'Package' in d:pkgs[d['Package']]=d
selected=set()
def add(n):
 if n in selected:return
 d=pkgs[n];selected.add(n)
 for dep in d.get('Depends','').split(','):
  dep=re.split(r'[ (|]',dep.strip())[0]
  if dep in pkgs and ('lib' in dep or dep.endswith('-udeb')) and dep not in ['debootstrap-udeb']:add(dep)
add('bootstrap-base');add('gpgv-udeb');add('debootstrap-udeb');add('openssh-server-udeb');add('mdadm-udeb');add('e2fsprogs-udeb');add('kbd-udeb') if 'kbd-udeb' in pkgs else None
for n in ['md','ext4','crypto','scsi','fat']:selected.add(n+'-modules-6.12.107+deb13-amd64-di')
cache=b/'udebs';cache.mkdir(exist_ok=True)
for n in sorted(selected):
 d=pkgs[n];raw=urllib.request.urlopen('https://deb.debian.org/debian/'+d['Filename'],timeout=60).read();assert hashlib.sha256(raw).hexdigest()==d['SHA256']
 p=cache/(n+'.udeb');p.write_bytes(raw);subprocess.run(['dpkg-deb','-x',str(p),str(stage)],check=True)
# Normalize legacy udeb directories to Debian netboot usr-merge layout.
for legacy in ['bin','sbin','lib']:
 olddir=stage/legacy;newdir=stage/'usr'/legacy
 if olddir.is_dir() and not olddir.is_symlink():
  shutil.copytree(olddir,newdir,dirs_exist_ok=True);shutil.rmtree(olddir);olddir.symlink_to('usr/'+legacy)
# Compute module indexes against the merged base on the controller, not in TCG/installer.
with tempfile.TemporaryDirectory() as tmp:
 merged=pathlib.Path(tmp)
 subprocess.run(['cpio','-idm','--quiet','usr/lib/modules/*'],input=gzip.decompress((assets/'initrd.gz').read_bytes()),cwd=merged,check=True)
 shutil.copytree(stage/'usr/lib/modules',merged/'usr/lib/modules',dirs_exist_ok=True)
 (merged/'lib').symlink_to('usr/lib')
 subprocess.run(['/usr/sbin/depmod','-b',str(merged),'6.12.107+deb13-amd64'],check=True,capture_output=True)
 for item in (merged/'usr/lib/modules/6.12.107+deb13-amd64').glob('modules.*'):
  shutil.copy(item,stage/'usr/lib/modules/6.12.107+deb13-amd64'/item.name)
(stage/'usr/share/keyrings').mkdir(parents=True,exist_ok=True)
shutil.copy('/usr/share/keyrings/debian-archive-keyring.gpg',stage/'usr/share/keyrings/debian-archive-keyring.gpg')
# Current signed udebs supply ssh/mdadm/ext4 and all dynamic libraries in RAM.
if not (b/'identity').exists():subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(b/'identity')],check=True)
if not (b/'host_key').exists():subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(b/'host_key')],check=True)
(stage/'jarvis').mkdir(exist_ok=True);shutil.copy(b/'host_key',stage/'jarvis/host_key');shutil.copy(b/'host_key.pub',stage/'jarvis/host_key.pub')
shutil.copy(b/'identity.pub',stage/'jarvis/authorized_keys')
if not (b/'target_host_key').exists():subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(b/'target_host_key')],check=True)
for n in ['target_host_key','target_host_key.pub']:shutil.copy(b/n,stage/'jarvis'/n)
shutil.copy(pathlib.Path(__file__).with_name('install-preserve.sh'),stage/'jarvis/install-preserve.sh')
for name in ['progress-viewer.sh','progress-console.service']:shutil.copy(pathlib.Path(__file__).with_name(name),stage/'jarvis'/name)
manifest=json.loads((ROOT/'private/bootstrap-discovery-04/manifest.install-target.json').read_text())
sys.path.insert(0,str(ROOT/'physical'))
from validate import validate
live=json.loads((ROOT/'private/bootstrap-discovery-04/inventory.observed.json').read_text())
# Offline manifest consistency only; the physical shell guard independently requires /sys/firmware/efi.
live['uefi']=True
for d in live['disks']:d.setdefault('type','disk');d.setdefault('ro',False)
validate(manifest,live)
rows=['uuid\t'+manifest['uuid'],'product\t'+manifest['product']]
for d in manifest['disks']:rows.append('\t'.join(['disk',pathlib.Path(d['path']).name,d['serial'],d['model'],str(d['size']//512)]))
for d in manifest.get('excluded_empty_media',[]):rows.append('\t'.join(['empty-media',pathlib.Path(d['path']).name,d['model'],'0']))
tsv='\n'.join(rows)+'\n';(stage/'approved.tsv').write_text(tsv);(stage/'approved-erase.sha256').write_text(hashlib.sha256(tsv.encode()).hexdigest()+'\n')
shutil.copy(ROOT/'debian/guard-physical.sh',stage/'guard-physical.sh')
# The Debian installer BusyBox omits tee/gzip: supply only those applets from
# Debian's authenticated busybox-static package, without replacing installer tools.
tools=b/'resume-tools';tools.mkdir(exist_ok=True)
subprocess.run(['apt-get','download','busybox-static'],cwd=tools,check=True,capture_output=True)
packages=list(tools.glob('busybox-static*.deb'));assert len(packages)==1,'Ambiguous static BusyBox package'
subprocess.run(['dpkg-deb','-x',str(packages[0]),str(tools/'root')],check=True)
shutil.copy(tools/'root/usr/bin/busybox',stage/'jarvis/busybox-full')
for applet in ['tee','gzip']:
 link=stage/'usr/bin'/applet
 if link.exists() or link.is_symlink():link.unlink()
 link.symlink_to('/jarvis/busybox-full')
shutil.copy(pathlib.Path(__file__).with_name('supervised-start.sh'),stage/'jarvis/start.sh')
# French console map from host kbd package, converted with compile-time console tools.
keymap=b/'fr.bmap'
with keymap.open('wb') as f:subprocess.run(['/usr/bin/loadkeys','--bkeymap',str(b/'console/usr/share/keymaps/i386/azerty/fr.kmap.gz')],stdout=f,check=True)
shutil.copy(keymap,stage/'jarvis/fr.bmap')
shutil.copytree(b/'console/usr/share/keymaps',stage/'usr/share/keymaps',dirs_exist_ok=True)
for km in (stage/'usr/share/keymaps').rglob('*.gz'):
 km.with_suffix('').write_bytes(gzip.decompress(km.read_bytes()));km.unlink()
shutil.copy('/usr/bin/dumpkeys',stage/'usr/bin/dumpkeys')
password=(ROOT/'private/reprise-user-password.txt').read_text().rstrip('\n')
r=subprocess.run(['openssl','passwd','-6','-stdin'],input=password+'\n',capture_output=True,text=True,check=True)
(stage/'jarvis/root.hash').write_text(r.stdout)
(stage/'preseed.cfg').write_text('d-i debian-installer/locale string fr_FR.UTF-8\nd-i keyboard-configuration/xkb-keymap select fr\nd-i console-keymaps-at/keymap select fr\nd-i preseed/early_command string /bin/sh /jarvis/start.sh\n')
# Dependencies for scsi NVMe are handled by normal modprobe using merged modules.dep.
http=b/'http';http.mkdir(exist_ok=True)
subprocess.run(['cp',str(assets/'linux'),str(http/'linux')],check=True)
names='\n'.join(sorted(str(p.relative_to(stage)) for p in stage.rglob('*')))+'\n'
a=subprocess.run(['cpio','-o','-H','newc','--reproducible','--owner=0:0'],cwd=stage,input=names.encode(),capture_output=True,check=True).stdout
temporary=http/'initrd.gz.new';temporary.write_bytes((assets/'initrd.gz').read_bytes()+gzip.compress(a,mtime=0));temporary.replace(http/'initrd.gz')
(http/'discovery.ipxe').write_text('#!ipxe\ndhcp\nset base http://192.168.1.99:8088\nkernel ${base}/linux initrd=initrd.gz auto=true priority=critical file=/preseed.cfg locale=fr_FR.UTF-8 keymap=fr keyboard-configuration/xkb-keymap=fr nomodeset fb=false console=tty0\ninitrd ${base}/initrd.gz\nboot\n')
old=ROOT/'private/installation-01'
shutil.copytree(old/'tftp',b/'tftp',dirs_exist_ok=True)
(b/'proxy.conf').write_text((old/'proxy.conf').read_text().replace(str(old),str(b)))
(b/'restrict.nft').write_text((old/'restrict.nft').read_text())
(b/'build.json').write_text(json.dumps({'authenticated_udebs':sorted(selected),'initrd_sha256':hashlib.sha256((http/'initrd.gz').read_bytes()).hexdigest(),'manifest_sha256':hashlib.sha256((ROOT/'private/bootstrap-discovery-04/manifest.install-target.json').read_bytes()).hexdigest()},indent=2)+'\n')
print('Built',b,'with pinned installer host key and no automatic disk writes')

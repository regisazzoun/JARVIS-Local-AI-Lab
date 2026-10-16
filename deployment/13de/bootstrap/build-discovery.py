#!/usr/bin/env python3
"""Authenticated Debian assets + embedded automatic discovery. Never enables installation."""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import argparse,gzip,hashlib,json,pathlib,secrets,subprocess,os
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('assets',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);a=p.parse_args()
os.umask(0o077); a.output.mkdir(mode=0o700) # New output only, do not reuse session capabilities.
assets=a.assets.resolve(); out=a.output.resolve()
subprocess.run(['gpgv','--keyring','/usr/share/keyrings/debian-archive-keyring.gpg',str(assets/'Release.gpg'),str(assets/'Release')],check=True)
checks=(assets/'SHA256SUMS').read_bytes();release=(assets/'Release').read_text().split('SHA256:\n',1)[1].split('\nSHA512:',1)[0]
assert any(l.split()[-1:]==['main/installer-amd64/current/images/SHA256SUMS'] and l.split()[0]==hashlib.sha256(checks).hexdigest() for l in release.splitlines())
entries={l.split(maxsplit=1)[1].lstrip('*./'):l.split()[0] for l in checks.decode().splitlines()}
for n in ('linux','initrd.gz'):assert hashlib.sha256((assets/n).read_bytes()).hexdigest()==entries['netboot/debian-installer/amd64/'+n]
key=secrets.token_hex(24)
script=(ROOT/'discovery/collect.sh').read_text()
for k,v in dict(BASE='http://192.168.1.99:8090',KEY=key,HOST='192.168.1.99',PORT='8090').items():script=script.replace('@'+k+'@',v)
stage=out/'stage';stage.mkdir()
(stage/'jarvis-collect.sh').write_text(script)
(stage/'jarvis-discovery.sh').write_bytes((ROOT/'bootstrap/discovery-start.sh').read_bytes())
(stage/'preseed.cfg').write_text('''d-i debian-installer/locale string fr_FR.UTF-8
d-i keyboard-configuration/xkb-keymap select fr
d-i netcfg/choose_interface select auto
d-i netcfg/get_hostname string jarvis-discovery
d-i netcfg/get_domain string local
d-i netcfg/disable_autoconfig boolean false
d-i preseed/early_command string /bin/sh /jarvis-discovery.sh
''')
from nvme_drivers import add
add(assets,stage)
names='\n'.join(sorted(str(p.relative_to(stage)) for p in stage.rglob('*')))+'\n'
archive=subprocess.run(['cpio','-o','-H','newc','--reproducible'],cwd=stage,input=names.encode(),capture_output=True,check=True).stdout
(out/'initrd.gz').write_bytes((assets/'initrd.gz').read_bytes()+gzip.compress(archive,mtime=0))
(out/'linux').write_bytes((assets/'linux').read_bytes())
(out/'discovery.ipxe').write_text('''#!ipxe
dhcp || goto failed
set base http://192.168.1.99:8088
kernel ${base}/linux initrd=initrd.gz auto=true priority=critical file=/preseed.cfg interface=auto nomodeset fb=false console=tty0
initrd ${base}/initrd.gz
boot || goto failed
:failed
echo STOP - discovery boot failed
shell
''')
settings=dict(bind='192.168.1.99',port=8090,source='192.168.1.0/24',key=key,script=str(stage/'jarvis-collect.sh'),output=str(out/'hardware-report.txt'),manifest_output=str(out/'manifest.unapproved.json'))
(out/'receiver.json').write_text(json.dumps(settings,indent=2)+'\n')
# Serve only these files, never out itself (which includes receiver capability/settings).
http=out/'http';http.mkdir()
for name in ('linux','initrd.gz','discovery.ipxe'):os.link(out/name,http/name)
print('DISCOVERY-ONLY assets prepared:',out)

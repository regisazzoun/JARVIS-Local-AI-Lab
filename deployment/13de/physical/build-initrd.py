#!/usr/bin/env python3
"""Build a fail-closed candidate initrd; does not add destructive authorization."""
import argparse, copy, gzip, hashlib, json, pathlib, subprocess, tempfile
from validate import validate
p=argparse.ArgumentParser()
p.add_argument('manifest');p.add_argument('public_key');p.add_argument('verified_assets');p.add_argument('output')
a=p.parse_args()
manifest=json.loads(pathlib.Path(a.manifest).read_text())
live=copy.deepcopy(manifest);live['uefi']=True
for disk in live['disks']:disk.update(type='disk',ro=False)
validate(manifest,live)
# Reject manifest field delimiters, shell fragments remain data and are never sourced.
for disk in manifest['disks']:
 for field in ('path','serial','model'):
  assert not any(c in disk[field] for c in '\r\n\t'), field
 assert disk['size'] % 512 == 0
key=pathlib.Path(a.public_key).resolve()
subprocess.run(['ssh-keygen','-lf',str(key)],check=True,capture_output=True)
assert len(key.read_text().splitlines())==1
assert key.read_text().startswith(('ssh-ed25519 ', 'ssh-rsa ', 'ecdsa-sha2-nistp256 '))
assets=pathlib.Path(a.verified_assets)
checks={line.split(maxsplit=1)[1].lstrip('*./'):line.split()[0] for line in (assets/'SHA256SUMS').read_text().splitlines()}
# Revalidate signature/Release binding, not just payload hashes supplied by caller.
subprocess.run(['gpgv','--keyring','/usr/share/keyrings/debian-archive-keyring.gpg',str(assets/'Release.gpg'),str(assets/'Release')],check=True)
release=(assets/'Release').read_text().split('SHA256:\n',1)[1].split('\nSHA512:',1)[0]
assert any(line.split()[-1:] == ['main/installer-amd64/current/images/SHA256SUMS'] and line.split()[0] == hashlib.sha256((assets/'SHA256SUMS').read_bytes()).hexdigest() for line in release.splitlines())
for name in ('linux','initrd.gz'):
 assert hashlib.sha256((assets/name).read_bytes()).hexdigest()==checks['netboot/debian-installer/amd64/'+name]
base=pathlib.Path(__file__).resolve().parents[1]/'debian'
with tempfile.TemporaryDirectory() as tmp:
 stage=pathlib.Path(tmp)
 for src,dst in [('guard-physical.sh','guard-physical.sh'),('install-ssh.sh','install-ssh.sh'),('preseed-dell.candidate.cfg','preseed.cfg')]:
  (stage/dst).write_bytes((base/src).read_bytes())
 (stage/'authorized_key').write_bytes(key.read_bytes())
 rows=['uuid\t'+manifest['uuid'],'product\t'+manifest['product']]
 for d in manifest['disks']:
  rows.append('\t'.join(['disk',pathlib.Path(d['path']).name,d['serial'],d['model'],str(d['size']//512)]))
 (stage/'approved.tsv').write_text('\n'.join(rows)+'\n')
 names='\n'.join(sorted(f.name for f in stage.iterdir()))+'\n'
 archive=subprocess.run(['cpio','-o','-H','newc','--reproducible'],cwd=stage,input=names.encode(),capture_output=True,check=True).stdout
 with pathlib.Path(a.output).open('xb') as out:
  out.write((assets/'initrd.gz').read_bytes());out.write(gzip.compress(archive,mtime=0))
print('Candidate built; erase approval absent: installer stops before partitioning.')

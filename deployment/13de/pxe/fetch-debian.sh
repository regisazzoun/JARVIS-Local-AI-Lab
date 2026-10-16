#!/bin/sh
# Download into a NEW private directory; verify signed Debian archive Release
# and its SHA256SUMS reference before trusting installer payloads.
set -eu
umask 077
out=${1:?new output directory required}
mkdir "$out"
cd "$out"
base=https://deb.debian.org/debian/dists/trixie
curl -fSsLO "$base/Release"
curl -fSsLO "$base/Release.gpg"
gpgv --keyring /usr/share/keyrings/debian-archive-keyring.gpg Release.gpg Release
curl -fSsLo SHA256SUMS "$base/main/installer-amd64/current/images/SHA256SUMS"
python3 - <<'PY'
import hashlib,pathlib
lines=pathlib.Path('Release').read_text().split('SHA256:\n',1)[1].split('\nSHA512:',1)[0].splitlines()
expected=[l.split()[0] for l in lines if l.split()[-1:] == ['main/installer-amd64/current/images/SHA256SUMS']]
assert len(expected)==1, 'installer checksum not authenticated in Release'
assert hashlib.sha256(pathlib.Path('SHA256SUMS').read_bytes()).hexdigest()==expected[0]
PY
for name in linux initrd.gz; do
 curl -fSsLo "$name" "$base/main/installer-amd64/current/images/netboot/debian-installer/amd64/$name"
done
python3 - <<'PY'
import hashlib,pathlib
entries={line.split(maxsplit=1)[1].lstrip('*./'):line.split()[0] for line in pathlib.Path('SHA256SUMS').read_text().splitlines()}
for name in ('linux','initrd.gz'):
 assert hashlib.sha256(pathlib.Path(name).read_bytes()).hexdigest()==entries['netboot/debian-installer/amd64/'+name],name
print('Verified Debian installer payloads')
PY

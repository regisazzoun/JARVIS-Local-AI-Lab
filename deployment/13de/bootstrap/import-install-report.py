#!/usr/bin/env python3
"""Bind firstboot identity and public host key to approved deployment; no remote actions."""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import argparse,base64,hashlib,json,os,pathlib,re,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'physical'))
from report_manifest import parse
p=argparse.ArgumentParser();p.add_argument('report',type=pathlib.Path);p.add_argument('manifest',type=pathlib.Path);p.add_argument('identity',type=pathlib.Path);p.add_argument('password',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);a=p.parse_args()
os.umask(0o077)
text=a.report.read_text(); metadata=json.loads(pathlib.Path(str(a.report)+'.metadata.json').read_text())
assert metadata['sha256']==hashlib.sha256(a.report.read_bytes()).hexdigest()
actual=parse(text);expected=json.loads(a.manifest.read_text())
for field in ('vendor','product','uuid'):assert actual[field]==expected[field],field
identity=lambda d:tuple(d[k] for k in ('path','serial','model','size'))
assert sorted(map(identity,actual['disks']))==sorted(map(identity,expected['disks'])),'disks'
assert text.count('JARVIS_HOSTKEY_BEGIN\n')==1
key=text.split('JARVIS_HOSTKEY_BEGIN\n')[1].split('JARVIS_HOSTKEY_END')[0].strip()
assert re.fullmatch(r'ssh-ed25519 [A-Za-z0-9+/=]+(?: [^\n]+)?',key),'host key'
import subprocess
pub=subprocess.check_output(['ssh-keygen','-y','-f',str(a.identity)],text=True).strip()
s=dict(host=metadata['source_ip'],approved_addresses=[metadata['source_ip']],manifest=str(a.manifest.resolve()),identity_file=str(a.identity.resolve()),password_file=str(a.password.resolve()),host_public_key=key,authorized_public_key_sha256=hashlib.sha256(base64.b64decode(pub.split()[1])).hexdigest(),host_key_origin='reviewed-authenticated-installation-report',administration_authorized=False)
with a.output.open('x') as f:json.dump(s,f,indent=2);f.write('\n')
print('Identity/host-key report imported; administrative authorization remains FALSE.')

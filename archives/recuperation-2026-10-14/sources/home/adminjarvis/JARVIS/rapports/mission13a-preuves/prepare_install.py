from pathlib import Path
import json,hashlib,shutil,importlib.metadata as md
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name,parse_wheel_filename
src=Path('/tmp/jarvis-m12-EC3FOY');proof=Path('/home/adminjarvis/JARVIS/rapports/mission13a-preuves');ref=proof.parent/'mission12-preuves';root=Path('/opt/jarvis/voice')
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
# Determine base dependencies from the actually tested distributions, without extras.
selected=set();pending=['faster-whisper','piper-tts']
while pending:
 name=canonicalize_name(pending.pop())
 if name in selected:continue
 selected.add(name)
 for dep in md.distribution(name).requires or []:
  r=Requirement(dep)
  if r.marker is None or r.marker.evaluate({'extra':''}):pending.append(r.name)
lock={canonicalize_name(line.split('==')[0]):line for line in (ref/'requirements-tested-cp313-linux.txt').read_text().splitlines()}
assert selected<=lock.keys()
wheel_manifest={f['file']:f for f in json.loads((ref/'wheel-manifest.json').read_text())}
wheels=[]
for f in (src/'wheels').glob('*.whl'):
 name,version,_,_=parse_wheel_filename(f.name)
 if (name in selected and str(version)==md.version(name)) or name=='pip':
  expected=wheel_manifest[f.name]['sha256'];assert sha(f)==expected
  wheels.append((f,expected))
models=[]
for entry in json.loads((ref/'download-manifest.json').read_text())['files']:
 name=entry['name']
 if name.startswith('whisper-small-') or name.startswith('tom-'):
  f=src/'models'/name;assert sha(f)==entry['sha256'];models.append((f,entry))
assert len(models)==7
before=json.loads((proof/'before.json').read_text());old=json.loads((ref/'before.json').read_text())
for p,h in old['files'].items():
 if p in before['configs']:assert before['configs'][p]==h, 'Contradiction avec Mission 12: '+p
assert before['services']['stdout']=='active\nactive\n'
assert not root.exists(), 'Installation existante, ne pas écraser'
# Root directory created separately with sudo only; all package operations run as UID1000.
(proof/'selected-dependencies.json').write_text(json.dumps(sorted(selected),indent=2))
(proof/'verified-inputs.json').write_text(json.dumps({'wheels':[{'file':f.name,'sha256':h} for f,h in wheels],'models':[e for f,e in models]},indent=2))
(proof/'requirements-voice-cp313-linux.txt').write_text('\n'.join(lock[n] for n in sorted(selected))+'\n')
print('Verified',len(wheels),'wheels and',len(models),'model files; no contradiction with Mission12')

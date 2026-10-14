"""Generate a fictional WAV fixture with the installed CPU Piper; never overwrite a file."""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from jarvis.core import Core
from jarvis.memory import Memory
config=json.loads((ROOT/'config/13e.json').read_text());target=ROOT/'runtime/qa13f-input.wav'
if target.exists():raise SystemExit('Fixture already exists and was preserved')
voice=Core(config,Memory(ROOT/'runtime/memory.sqlite')).voice('tts','Bonjour Jarvis. Pour ce test fictif, dis simplement bonjour en français.')
with target.open('xb') as f:f.write(voice)
print('Fictional Piper WAV fixture generated:',target.name,len(voice),'bytes')

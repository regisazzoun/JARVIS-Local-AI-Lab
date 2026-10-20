import argparse
from pathlib import Path
import hashlib,json,wave
from piper import PiperVoice
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
root=args.output;root.mkdir(parents=True,exist_ok=True)
voice=PiperVoice.load('/opt/jarvis/voice/models/tts/fr_FR-tom-medium.onnx')
texts={
 'initial':'Bonjour JARVIS. Préparons une visite fictive du musée des sciences samedi à quatorze heures, pour deux adultes, avec un budget de quarante euros. Décris un programme détaillé en six étapes, pendant au moins quinze secondes.',
 'interrupt':'Stop. Change le programme : dimanche à dix heures, budget vingt euros. Confirme uniquement les nouveaux horaires et le budget.',
 'continuity':'Quel est maintenant le jour de la visite, son horaire et le budget ?'}
manifest={}
for name,text in texts.items():
 path=root/(name+'.wav')
 with wave.open(str(path),'wb') as w:voice.synthesize_wav(text,w)
 with wave.open(str(path),'rb') as w:meta={'sample_rate':w.getframerate(),'channels':w.getnchannels(),'duration_s':w.getnframes()/w.getframerate()}
 manifest[name]={'text':text,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),**meta}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(manifest,ensure_ascii=False))

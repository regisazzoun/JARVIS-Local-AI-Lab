"""Codex exact correction tool, executed by JARVIS; originals preserved."""
import hashlib,json,time
from pathlib import Path
root=Path(__file__).parent;app=root.parent/'livekit-agent';history=root/'historique';history.mkdir(exist_ok=True)
patches={
 'tts_adapter.py':[
  ('sample_rate: int = 16000','sample_rate: int = 44100'),
  ("wav_buffer.seek(44)\n        pcm_data = wav_buffer.read()", "with wave.open(io.BytesIO(wav_buffer.getvalue()), 'rb') as stream:\n            if stream.getframerate() != 44100:\n                raise RuntimeError('Unexpected Piper rate; explicit resampling required')\n            pcm_data = stream.readframes(stream.getnframes())")],
 'factories.py':[("timeout=120.0  #", "reasoning_effort=\"none\",\n        timeout=120.0  #")],
 'agent.py':[("turn_handling={\"interruption\": {\"enabled\": True, \"mode\": \"vad\"}}", "turn_handling={\"interruption\": {\"enabled\": True, \"mode\": \"vad\", \"min_duration\": 0.3, \"resume_false_interruption\": False}}")]
}
receipt={'actor':'Codex correction tool executed by JARVIS','utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'files':[]}
for name,changes in patches.items():
 path=app/name;before=path.read_text();after=before
 for old,new in changes:
  if old in after:
   assert after.count(old)==1,(name,old);after=after.replace(old,new)
  else:assert new in after,('Unexpected source; stop this correction',name,old)
 sha=hashlib.sha256(before.encode()).hexdigest();(history/(name+'.'+sha[:12]+'.txt')).write_text(before)
 compile(after,str(path),'exec');path.write_text(after)
 receipt['files'].append({'file':name,'before':sha,'after':hashlib.sha256(after.encode()).hexdigest(),'changed':before!=after})
(root/'reports/component-correction.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))

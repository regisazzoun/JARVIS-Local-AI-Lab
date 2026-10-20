"""Codex causal correction tool; explicit supported SDK option, no SDK patch."""
import hashlib,json,time
from pathlib import Path
root=Path(__file__).parent;path=root.parent/'livekit-agent/agent.py';before=path.read_text()
old='session = AgentSession(\n        stt=stt_provider,'
new='session = AgentSession(\n        # Explicit prototype policy: browser AEC remains enabled; first-turn barge-in is tested.\n        aec_warmup_duration=0.0,\n        turn_handling={\"interruption\": {\"enabled\": True, \"mode\": \"vad\", \"min_duration\": 0.3, \"min_words\": 0, \"resume_false_interruption\": False}, \"preemptive_generation\": {\"enabled\": False}},\n        stt=stt_provider,'
if old in before:after=before.replace(old,new,1)
else:assert new in before;after=before
after=after.replace('        preemptive_generation={"enabled": False},\n','')
sha=hashlib.sha256(before.encode()).hexdigest();(root/'historique'/('agent-before-aec-'+sha[:12]+'.py.txt')).write_text(before)
compile(after,str(path),'exec');path.write_text(after)
receipt={'actor':'Codex exact correction tool executed by JARVIS','utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'before_sha256':sha,'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'sdk_default_aec_warmup_s':3.0,'configured_aec_warmup_s':0.0,'session_min_interruption_duration_s':0.3,'session_resume_false_interruption':False,'preemptive_generation':False,'scope':'Prototype first-turn barge-in; browser echo cancellation unchanged','limit':'Physical microphone echo robustness untested'}
(root/'reports/aec-correction.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))

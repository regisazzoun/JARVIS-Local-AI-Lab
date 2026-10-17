"""Synthetic speech -> actual STT -> same chat path as browser -> host tools."""
import json,pathlib,time,urllib.request,urllib.error
from reception import login,client,ROOT,OUT,call
login();start=time.monotonic()
text='Crée un fichier de test vocal sur le système hôte Debian dans un répertoire de travail autorisé, puis relis ce fichier et vérifie le résultat. Utilise les outils hôtes et conserve un rapport.'
def raw_call(path,data):
    req=urllib.request.Request('http://localhost:8765'+path,data=data,headers={'Content-Type':'application/octet-stream','X-Jarvis-Request':'1'})
    for attempt in range(300):
        try:
            with client.open(req,timeout=1200) as r:return r.read()
        except urllib.error.HTTPError as e:
            if e.code!=409:raise
            time.sleep(2)
    raise RuntimeError('Passerelle occupée ; aucun essai vocal lancé')
wav=raw_call('/api/tts',json.dumps({'text':text}).encode());(OUT/'voice-synthetic.wav').write_bytes(wav)
stt=json.loads(raw_call('/api/stt',wav));transcript=stt.get('text',stt.get('transcription'))
if not transcript:raise RuntimeError('Transcription absente : '+str(list(stt)))
r=call('/api/chat',{'text':transcript,'model':'qwen3.5:27b-q4_K_M','project':'mission11-voice','agent_mode':True,'retain':True})
(OUT/'voice.json').write_text(json.dumps({'kind':'Piper synthetic WAV, Whisper STT, actual Qwen and broker; not physical microphone','input':text,'stt':stt,'elapsed_s':time.monotonic()-start,'response':r},ensure_ascii=False,indent=2))
print(json.dumps({'elapsed_s':round(time.monotonic()-start,2),'transcript':transcript,'tools':[{'tool':x['tool'],'ok':x['ok']} for x in r['tools']],'answer':r['answer']},ensure_ascii=False))

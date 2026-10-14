"""Actual deployed-service reception. Only fictional fixtures are removed afterward."""
import urllib.request,http.cookiejar,json,time,subprocess,io,wave,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));OUT=Path('/home/adminjarvis/JARVIS/rapports/mission13e-preuves');BASE='http://localhost:8765';project='__13e_reception_fictive__';password=(ROOT/'runtime/credentials.txt').read_text().splitlines()[1].split(': ',1)[1];client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));report={};conversation=None;mid=None

def call(path,data=None,raw=False):
 headers={};body=None
 if data is not None:body=data if raw else json.dumps(data).encode();headers={'Content-Type':'application/octet-stream' if raw else 'application/json','X-Jarvis-Request':'1'}
 with client.open(urllib.request.Request(BASE+path,data=body,headers=headers),timeout=240) as r:
  data=r.read();return data if r.headers.get('Content-Type','').startswith('audio/') else json.loads(data)
def login():return call('/api/login',{'username':'adminjarvis','password':password})
try:
 try:urllib.request.urlopen(BASE+'/api/memories');raise AssertionError('unauthenticated accepted')
 except urllib.error.HTTPError as e:assert e.code==401;report['auth_unauthorized_status']=e.code
 login();assert call('/api/session')['authenticated']
 mid=call('/api/memory/propose',{'content':'Le projet fictif Reprise13E possède le code TEST-386.','project':project})['id'];call('/api/memory/approve',{'id':mid,'explicit':True})
 r=call('/api/chat',{'text':'Quel est le code du projet fictif Reprise13E ? Réponds en une phrase.','model':'qwen3.5:27b-q4_K_M','project':project});conversation=r['conversation'];assert mid in r['memories_used'] and 'TEST-386' in r['answer'];report['first_answer']=r['answer']
 pid_before=subprocess.check_output(['systemctl','show','jarvis-conversation.service','--property=MainPID','--value'],text=True).strip()
 subprocess.run(['sudo','-n','systemctl','restart','jarvis-conversation.service'],check=True)
 for i in range(30):
  try:
   assert not call('/api/session')['authenticated'];break
  except Exception:time.sleep(.2)
 else:raise AssertionError('restart readiness failed')
 login();history=call('/api/history?id='+conversation);assert len(history)==2
 r=call('/api/chat',{'text':'Rappelle le code du projet fictif Reprise13E en une phrase.','model':'qwen3.5:27b-q4_K_M','project':project,'conversation':conversation});assert mid in r['memories_used'] and 'TEST-386' in r['answer'];report['after_restart']=r['answer'];report['persisted_messages']=len(call('/api/history?id='+conversation));report['pid_before']=pid_before;report['pid_after']=subprocess.check_output(['systemctl','show','jarvis-conversation.service','--property=MainPID','--value'],text=True).strip();assert report['pid_before']!=report['pid_after']
 r=call('/api/chat',{'text':'Utilise jarvis_services et vérifie la disponibilité réelle d’Open WebUI par HTTP. Explique les résultats en français, sans interpréter active/exited comme une panne.','model':'qwen3.5:27b-q4_K_M','retain':False});assert any(t['tool']=='jarvis_services' and t['ok'] and t['result'].get('open_webui_http',{}).get('status')==200 for t in r['tools']);report['diagnostic']=r
 started=time.monotonic();stt=call('/api/stt',(ROOT/'runtime/test-input.wav').read_bytes(),True);t1=time.monotonic();r=call('/api/chat',{'text':stt['text'],'model':'qwen3.5:27b-q4_K_M','retain':False});t2=time.monotonic();audio=call('/api/tts',{'text':r['answer']});t3=time.monotonic()
 with wave.open(io.BytesIO(audio)) as w:assert w.getnframes()>0;duration=w.getnframes()/w.getframerate()
 report['deployed_voice']={'transcript':stt['text'],'answer':r['answer'],'stt_s':t1-started,'ollama_s':t2-t1,'tts_s':t3-t2,'total_s':t3-started,'audio_s':duration}
 report['passed']=True
finally:
 # Delete only exact fictional IDs created in this script; never touch other records.
 from jarvis.memory import Memory
 m=Memory(ROOT/'runtime/memory.sqlite')
 if mid:m.delete(mid)
 if conversation:
  with m.connect() as c:
   c.execute('DELETE FROM messages_fts WHERE id IN (SELECT id FROM messages WHERE conversation=?)',(conversation,))
   c.execute('DELETE FROM conversations WHERE id=? AND project=?',(conversation,project))
 report['canonical_counts_after_fixture_cleanup']={k:len(v) for k,v in m.export().items()};(OUT/'deployed-reception.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))

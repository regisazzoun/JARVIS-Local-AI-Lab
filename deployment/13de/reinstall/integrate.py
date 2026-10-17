#!/usr/bin/env python3
"""Retain Mac voice/SQLite/tools and route real authenticated requests to Dell Ollama."""
import argparse,pathlib,json,subprocess,urllib.request,http.cookiejar,time,uuid,sqlite3,io,wave,hashlib,hmac
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);p.add_argument('ip');a=p.parse_args();b=a.session;osroot=pathlib.Path('/opt/jarvis/conversation');config=osroot/'config/13e.json';compose=pathlib.Path('/home/adminjarvis/JARVIS/open-webui/compose.yaml')
oldconfig=config.read_bytes();oldcompose=compose.read_bytes();(b/'gateway-before.json').write_bytes(oldconfig);(b/'compose-before.yaml').write_bytes(oldcompose)
# Use SQLite's online backup, never copy a live WAL database as an ordinary file.
with sqlite3.connect(osroot/'runtime/memory.sqlite') as src,sqlite3.connect(b/'canonical-memory-before.sqlite') as dst:src.backup(dst)
results={};fixture=None
jar=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def gateway(path,data=None,raw=False):
 body=None if data is None else data if raw else json.dumps(data).encode()
 req=urllib.request.Request('http://localhost:8765'+path,data=body,headers={'X-Jarvis-Request':'1','Content-Type':'application/octet-stream' if raw else 'application/json'})
 with jar.open(req,timeout=600) as r:
  data=r.read();return data if r.headers.get('Content-Type','').startswith('audio/') else json.loads(data)
def restart():
 subprocess.run(['sudo','-n','systemctl','restart','jarvis-conversation.service'],check=True)
 subprocess.run(['sudo','-n','systemctl','restart','jarvis-open-webui.service'],check=True)
 deadline=time.monotonic()+120
 while time.monotonic()<deadline:
  try:
   if gateway('/api/health')['application']=='ok':return
  except Exception:pass
  time.sleep(2)
 raise RuntimeError('Gateway did not return after configuration')
def put(path,data):
 temp=b/'config-upload.tmp';temp.write_bytes(data);subprocess.run(['sudo','-n','cp',str(temp),str(path)],check=True);temp.unlink()
try:
 cfg=json.loads(oldconfig);cfg['ollama_url']='http://'+a.ip+':11434'
 put(config,(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n').encode())
 text=oldcompose.decode();assert text.count('OLLAMA_BASE_URL: http://127.0.0.1:11434')==1
 put(compose,text.replace('OLLAMA_BASE_URL: http://127.0.0.1:11434','OLLAMA_BASE_URL: http://'+a.ip+':11434').encode())
 restart()
 creds=(osroot/'runtime/credentials.txt').read_text().splitlines()
 active=json.loads((osroot/'runtime/auth.json').read_text())
 candidates=[creds[1].split(': ',1)[1],(b.parent/'reprise-user-password.txt').read_text().rstrip('\n')]
 password=next((value for value in candidates if hmac.compare_digest(hashlib.pbkdf2_hmac('sha256',value.encode(),bytes.fromhex(active['salt']),300000).hex(),active['hash'])),None)
 assert password is not None,'No locally available credential matches the active gateway; never reset existing account implicitly'
 gateway('/api/login',{'username':active['username'],'password':password})
 assert gateway('/api/session')['authenticated'];results['gateway_authenticated']=True
 project='__mission14_'+uuid.uuid4().hex[:10];code='TEST-J14-'+uuid.uuid4().hex[:8]
 fixture=gateway('/api/memory/propose',{'content':'Le code de validation fictif du projet '+project+' est '+code+'.','project':project})['id']
 gateway('/api/memory/approve',{'id':fixture,'explicit':True})
 result=gateway('/api/chat',{'text':'Quel est le code de validation fictif du projet '+project+' ? Réponds avec ce code.','model':'qwen3.5:27b-q4_K_M','project':project,'retain':False})
 assert code in result['answer'] and fixture in result['memories_used'],'Canonical memory recall not validated'
 results['canonical_memory_recall']={'passed':True,'model':'qwen3.5:27b-q4_K_M','canonical_db_unchanged_path':True}
 diagnostic=gateway('/api/chat',{'text':'Utilise obligatoirement l’outil jarvis_services pour vérifier les services JARVIS du Mac mini. Rapporte uniquement les résultats réellement observés.','model':'qwen3.5:27b-q4_K_M','retain':False})
 assert any(t.get('tool')=='jarvis_services' and t.get('ok') for t in diagnostic.get('tools',[])),'Real tool calling not validated'
 results['tool_calling']={'passed':True,'tool':'jarvis_services','scope':'existing Mac tools; no new autonomous Dell mutation policy'}
 wav=(osroot/'runtime/qa13f-input.wav').read_bytes();stt=gateway('/api/stt',wav,True);assert stt['text'].strip()
 response=gateway('/api/chat',{'text':stt['text'],'model':'qwen3.5:27b-q4_K_M','retain':False});assert response['answer'].strip()
 audio=gateway('/api/tts',{'text':response.get('spoken_answer') or response['answer'][:250]})
 with wave.open(io.BytesIO(audio)) as w:assert w.getnframes()>0
 results['voice']={'passed':True,'source':'existing synthetic WAV; no physical microphone test','stt':'Whisper Small on Mac','tts':'Piper Tom on Mac','inference':'Qwen on Dell','audio_bytes':len(audio)}
 lines=pathlib.Path('/home/adminjarvis/JARVIS/open-webui/identifiants-admin.txt').read_text().splitlines()
 def web(path,data=None,token=None):
  headers={'Content-Type':'application/json'}
  if token:headers['Authorization']='Bearer '+token
  req=urllib.request.Request('http://192.168.1.99:3000'+path,data=None if data is None else json.dumps(data).encode(),headers=headers)
  with urllib.request.urlopen(req,timeout=600) as r:return json.load(r)
 token=web('/api/v1/auths/signin',{'email':lines[0].split(': ',1)[1],'password':lines[1].split(': ',1)[1]})['token']
 response=web('/api/chat/completions',{'model':'llama3.1:8b','messages':[{'role':'user','content':'Calcule 17 fois 23, réponds avec le résultat.'}],'stream':False,'options':{'num_ctx':4096,'num_predict':64}},token)
 assert '391' in response['choices'][0]['message']['content']
 results['open_webui_authenticated_inference']={'passed':True,'model':'llama3.1:8b','backend':'Dell'}
 gateway('/api/memory/delete',{'id':fixture,'explicit':True});fixture=None
 with sqlite3.connect(osroot/'runtime/memory.sqlite') as c:assert c.execute('PRAGMA quick_check').fetchone()[0]=='ok'
 (b/'integration-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print('JARVIS_INTEGRATION_VALIDATED: authenticated gateway, memory, tools, voice and Open WebUI')
except BaseException:
 if fixture:
  try:gateway('/api/memory/delete',{'id':fixture,'explicit':True})
  except Exception:pass
 put(config,oldconfig);put(compose,oldcompose);restart()
 (b/'integration-rollback.txt').write_text('Previous inference backend settings restored after failed integration validation. Canonical memory database retained.\n')
 raise

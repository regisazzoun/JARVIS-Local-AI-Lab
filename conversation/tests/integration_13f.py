import os
"""Real deployed API, real models, canonical SQLite; no private transcript export."""
import urllib.request,http.cookiejar,json,time,sys,subprocess,io,wave,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));from jarvis.memory import Memory
OUT=Path(os.environ.get('JARVIS_TEST_OUTPUT',str(ROOT/'runtime/qa13f')));m=Memory(ROOT/'runtime/memory.sqlite');client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));report={'kind':'real deployed authenticated HTTP, SQLite commits and actual Ollama/Whisper/Piper','checks':[]};fixtures=[]
OUT.mkdir(mode=0o700,parents=True,exist_ok=True)
username=(ROOT/'runtime/credentials.txt').read_text().splitlines()[0].split(': ',1)[1];password=(ROOT/'runtime/credentials.txt').read_text().splitlines()[1].split(': ',1)[1]
def call(path,data=None,raw=False):
 body=None if data is None else data if raw else json.dumps(data).encode();headers={} if data is None else {'Content-Type':'application/octet-stream' if raw else 'application/json','X-Jarvis-Request':'1'}
 with client.open(urllib.request.Request('http://localhost:8765'+path,data=body,headers=headers),timeout=600) as r:
  body=r.read();return body if r.headers.get('Content-Type','').startswith('audio/') else json.loads(body)
def login():call('/api/login',{'username':username,'password':password})
def chat(text,model='qwen3.5:27b-q4_K_M',retain=False):
 r=call('/api/chat',{'text':text,'model':model,'retain':retain,'project':'__13f_validation__'});
 if retain:fixtures.append(r['conversation'])
 return r
def check(name,fn):
 try:detail=fn();report['checks'].append({'name':name,'passed':True,'details':detail});print(name,'OK',flush=True)
 except Exception as e:report['checks'].append({'name':name,'passed':False,'error':str(e)});print(name,'FAILED',str(e),flush=True)
 (OUT/'integration-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
login()
def automatic():
 r=chat('Je préfère des réponses vocales courtes.',retain=True);assert r['preference_events'];assert m.preferences()['voice_length']=='short';events=r['preference_events'];assert events[0]['status']=='approved'
 global mid;mid=events[0]['id'];r=chat('Je préfère des réponses vocales courtes.');assert r['preference_events'][0]['id']==mid
 with m.connect() as c:assert c.execute('SELECT COUNT(*) FROM preferences WHERE key=?',('voice_length',)).fetchone()[0]==1
 return {'actual_sqlite_commit':True,'duplicate_same_id':True,'events':events}
check('automatic durable preference and deduplication',automatic)
def shared():
 results=[]
 for model in call('/api/config')['models']:
  r=chat('Quelle longueur ai-je choisie pour les réponses vocales ? Réponds en une phrase sans modifier de souvenir.',model);assert mid in r['memories_used'];assert any(x in r['answer'].lower() for x in ['court','bref','brèv','short','concis']),r['answer'];results.append({'model':model,'answer':r['answer'],'same_memory_id_injected':True,'timings':r['timings']})
 return results
check('shared memory recall by three actual models',shared)
def replace_delete():
 r=chat('Désormais je préfère des réponses vocales détaillées.');assert m.preferences()['voice_length']=='detailed';assert r['preference_events'][0]['id']==mid
 r=chat('Oublie ma préférence de longueur vocale.');assert 'voice_length' not in m.preferences();assert r['preference_events'][0]['deleted'];assert not any(x['id']==mid for x in m.search('vocales'))
 r=chat('Je préfère des réponses vocales courtes.');assert m.preferences()['voice_length']=='short'
 return {'replacement_same_id':True,'delete_committed_and_fts_removed':True,'desired_short_preference_restored':True}
check('spoken replacement and deletion without validation click',replace_delete)
def language():
 chat('Désormais réponds en anglais.');r=chat('What language should you use now? Answer in one sentence.');assert m.preferences()['language']=='en';assert 'english' in r['answer'].lower(),r['answer'];english=r['answer'];chat('Désormais réponds en français.');assert m.preferences()['language']=='fr';return {'english_followup':english,'french_restored':True}
check('persistent language preference applied in later conversation',language)
def concise():
 r=chat('Fournis un rapport technique écrit détaillé sur le rôle de systemd, avec une liste, un petit tableau, un exemple de commande et un chemin de configuration.');assert len(r['answer'])>len(r['spoken_answer']);assert len(r['spoken_answer'])<360
 for word in ['```','/etc/','|','systemctl status']:assert word not in r['spoken_answer']
 return {'written_chars':len(r['answer']),'spoken_chars':len(r['spoken_answer']),'written':r['answer'],'spoken':r['spoken_answer'],'timings':r['timings']}
check('detailed written response and short cleaned speech',concise)
def real_diagnostics():
 r=chat('Effectue un diagnostic réel de la passerelle JARVIS, du GPU et des ressources mémoire. Vérifie aussi la santé HTTP réelle de WebUI. Utilise les outils et interprète sans inventer de mesure.');names={x['tool'] for x in r['tools']};assert 'jarvis_services' in names;assert 'hardware_inventory' in names or 'system_status' in names;services=next(x for x in r['tools'] if x['tool']=='jarvis_services');assert services['result']['open_webui_http']['status']==200
 return {'answer':r['answer'],'tools':r['tools'],'timings':r['timings']}
check('real model-selected host diagnosis and WebUI health',real_diagnostics)
def voice():
 started=time.monotonic();stt=call('/api/stt',(ROOT/'runtime/qa13f-input.wav').read_bytes(),True);t1=time.monotonic();r=chat(stt['text']);t2=time.monotonic();wav=call('/api/tts',{'text':r['spoken_answer']});t3=time.monotonic()
 with wave.open(io.BytesIO(wav)) as w:assert w.getnframes()>0;duration=w.getnframes()/w.getframerate()
 return {'transcript':stt['text'],'written':r['answer'],'spoken':r['spoken_answer'],'stt_s':t1-started,'llm_including_summary_s':t2-t1,'tts_s':t3-t2,'total_s':t3-started,'audio_s':duration}
check('real French STT -> actual Qwen -> concise Piper',voice)
def backup_restart():
 tag=uuid.uuid4().hex;target=ROOT/('runtime/backups/mission13f-validation-'+tag+'.sqlite');target.parent.mkdir(exist_ok=True)
 if target.exists():raise AssertionError('Use a fresh backup target')
 m.backup(target);restored=Memory.restore(target,ROOT/('runtime/backups/mission13f-restored-'+tag+'.sqlite'));assert restored.preferences()==m.preferences()
 before=m.preferences();count=len(m.history(fixtures[0]));pid_before=subprocess.check_output(['systemctl','show','jarvis-conversation','-p','MainPID','--value'],text=True).strip();subprocess.run(['sudo','-n','systemctl','restart','jarvis-conversation'],check=True)
 for i in range(50):
  try:
   if call('/api/health')['application']=='ok':break
  except Exception:time.sleep(.2)
 else:raise AssertionError('Service did not recover')
 assert not call('/api/session')['authenticated'];login();assert call('/api/preferences')==before;assert len(call('/api/history?id='+fixtures[0]))==count
 pid_after=subprocess.check_output(['systemctl','show','jarvis-conversation','-p','MainPID','--value'],text=True).strip();assert pid_before!=pid_after
 r=chat('Quelle longueur ai-je choisie pour les réponses vocales ?');assert any(x in r['answer'].lower() for x in ['court','bref','concis','short'])
 return {'online_backup_and_new_target_restore':True,'preferences_preserved':True,'history_count_preserved':count,'relogin_and_real_followup':True,'pid_changed':True}
check('backup restore persistence and reconnection after actual service restart',backup_restart)
# Remove only test conversations, never pre-existing history or user memories.
with m.connect() as c:
 for cid in fixtures:
  c.execute('DELETE FROM messages_fts WHERE id IN (SELECT id FROM messages WHERE conversation=?)',(cid,));c.execute('DELETE FROM conversations WHERE id=? AND project=?',(cid,'__13f_validation__'))
if any(not x['passed'] for x in report['checks']):raise SystemExit(1)

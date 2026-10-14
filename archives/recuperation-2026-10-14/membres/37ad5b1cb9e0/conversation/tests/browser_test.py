"""Real headless Chromium, fake microphone backed by a real WAV. Not physical client validation."""
import os,json,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];out=Path('/home/adminjarvis/JARVIS/rapports/mission13e-preuves');BASE=os.environ.get('JARVIS_TEST_URL','http://localhost:8767');password=(ROOT/'runtime/credentials.txt').read_text().splitlines()[1].split(': ',1)[1];report={'type':'real Chromium; file-backed fake microphone; real HTTP STT/Ollama/TTS; desktop/mobile layout emulation','tests':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream','--use-file-for-fake-audio-capture='+str(ROOT/'runtime/test-input.wav'),'--autoplay-policy=no-user-gesture-required'])
 context=browser.new_context(permissions=['microphone'],viewport={'width':1280,'height':900});page=context.new_page();errors=[];fixture_conversations=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def wait(expression,timeout=30000):
  deadline=time.monotonic()+timeout/1000
  while time.monotonic()<deadline:
   if page.evaluate('() => ('+expression+')'):return
   page.wait_for_timeout(100)
  raise TimeoutError('Condition non atteinte: '+expression)
 def check(name,fn):
  try:detail=fn();report['tests'].append({'name':name,'passed':True,'details':detail});print(name,'OK',flush=True)
  except Exception as e:report['tests'].append({'name':name,'passed':False,'error':str(e)});print(name,'FAILED',str(e),flush=True)
  finally:(out/'browser-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 def login():
  page.goto(BASE);assert page.locator('#loginpanel').is_visible();page.locator('#password').fill(password);page.locator('#loginform button').click();page.locator('#workspace').wait_for(state='visible');assert page.locator('#model option').count()==3;page.locator('#project').fill('__13e_browser_fiction__')
  return {'origin_secure':page.evaluate('isSecureContext'),'model_count':3}
 check('authenticated UI load',login)
 def recording():
  page.locator('#autosend').uncheck();page.locator('#speak').uncheck();page.locator('#togglemic').click();wait("document.getElementById('state').textContent==='Enregistrement'");page.wait_for_timeout(6500);page.locator('#togglemic').click();wait("document.getElementById('text').value.length>0",timeout=45000)
  text=page.locator('#text').input_value();assert 'bonjour' in text.lower(),text;assert page.evaluate('stream.getTracks().every(t=>t.readyState==="ended")')
  return {'transcription':text,'tracks_stopped':True}
 check('browser microphone file -> MediaRecorder WebM -> real Whisper',recording)
 def written():
  page.locator('#text').fill('Réponds seulement : Bonjour, je suis JARVIS.');page.locator('#send').click();wait("document.querySelectorAll('#history article.assistant').length>0",timeout=180000);assert 'JARVIS' in page.locator('#history article.assistant').last.inner_text().upper();wait('!busy',timeout=180000)
  fixture_conversations.append(page.evaluate('conversation'));return {'answer':page.locator('#history article.assistant').last.inner_text()}
 check('browser conversation with real Qwen',written)
 def playback():
  page.locator('#replay').click();wait("audio && !audio.paused && audio.currentTime>0",timeout=40000);current=page.evaluate('audio.currentTime');page.locator('#stop').click();assert page.evaluate('audio===null && objectURL===null');return {'played_seconds':current,'interrupted':True}
 check('real browser audio playback and interruption',playback)
 def long_audio():
  text='Cette phrase française est un test de lecture vocale longue. '*18
  page.evaluate('(s)=>{window.longTest=talk(s).then(()=>true);}',text);wait("audio && !audio.paused && audio.currentTime>0",timeout=40000);page.locator('#stop').click();wait('audio===null && objectURL===null');return {'chars':len(text),'segmented_and_interrupted':True}
 check('long TTS response segmented and interrupted',long_audio)
 def automatic_voice():
  page.locator('#new').click();page.locator('#autosend').check();page.locator('#speak').check();page.locator('#togglemic').click();wait("document.getElementById('state').textContent==='Enregistrement'");page.wait_for_timeout(6500);page.locator('#togglemic').click();wait("audio && !audio.paused && audio.currentTime>0",timeout=120000);fixture_conversations.append(page.evaluate('conversation'));answer=page.locator('#history article.assistant').last.inner_text();page.locator('#stop').click();wait('!busy',timeout=10000);return {'answer':answer,'complete_automatic_voice_chain':True}
 check('automatic recording -> STT -> real Qwen -> Piper -> browser playback',automatic_voice)
 def mobile():
  page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=str(out/'mobile-layout.png'),full_page=True);return {'width':390,'horizontal_overflow':False,'device':'Chromium viewport emulation; not Safari/iPhone hardware'}
 check('mobile layout',mobile)
 def logout():
  page.locator('#logout').click();page.locator('#loginpanel').wait_for(state='visible');r=page.request.get(BASE+'/api/memories');assert r.status==401;assert not errors,errors;return {'unauthenticated_api_status':r.status,'javascript_errors':errors}
 check('logout rejects private API',logout)
 browser.close()
 if BASE.endswith(':8765'):
  import sys;sys.path.insert(0,str(ROOT))
  from jarvis.memory import Memory
  m=Memory(ROOT/'runtime/memory.sqlite')
  with m.connect() as c:
   for cid in fixture_conversations:
    row=c.execute('SELECT project FROM conversations WHERE id=?',(cid,)).fetchone()
    if row and row['project']=='__13e_browser_fiction__':
     c.execute('DELETE FROM messages_fts WHERE id IN (SELECT id FROM messages WHERE conversation=?)',(cid,));c.execute('DELETE FROM conversations WHERE id=?',(cid,))
if any(not r['passed'] for r in report['tests']):raise SystemExit(1)

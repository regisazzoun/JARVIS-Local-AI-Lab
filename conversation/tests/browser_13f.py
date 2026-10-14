import os
"""Chromium integration with artificial WAV microphone. No physical speech claim."""
import json,time,os,wave,struct
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=Path(os.environ.get('JARVIS_TEST_OUTPUT',str(ROOT/'runtime/qa13f')));report={'kind':'Real Chromium/WebAudio with WAV-backed artificial microphone. Physical echo/noise and Safari not validated.','checks':[]};username=(ROOT/'runtime/credentials.txt').read_text().splitlines()[0].split(': ',1)[1];password=(ROOT/'runtime/credentials.txt').read_text().splitlines()[1].split(': ',1)[1]
OUT.mkdir(mode=0o700,parents=True,exist_ok=True)
# Add trailing silence to make end-of-speech automatic and reproducible.
source=ROOT/'runtime/qa13f-input.wav';target=ROOT/'runtime/vad-input13f.wav'
with wave.open(str(source)) as r:
 params=r.getparams();data=r.readframes(r.getnframes())
with wave.open(str(target),'wb') as w:w.setparams(params);w.writeframes(data+b'\0'*(params.framerate*params.nchannels*params.sampwidth*3))
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream','--use-file-for-fake-audio-capture='+str(target),'--autoplay-policy=no-user-gesture-required'])
 page=browser.new_page(permissions=['microphone'],viewport={'width':1280,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def wait(expr,seconds=90):
  deadline=time.monotonic()+seconds
  while time.monotonic()<deadline:
   if page.evaluate('() => ('+expr+')'):return
   page.wait_for_timeout(100)
  raise AssertionError('Timeout '+expr)
 def check(name,fn):
  try:detail=fn();report['checks'].append({'name':name,'passed':True,'details':detail});print(name,'OK',flush=True)
  except Exception as e:report['checks'].append({'name':name,'passed':False,'error':str(e)});print(name,'FAILED',str(e),flush=True)
  (OUT/'browser-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 def login():
  page.goto('http://localhost:8765');page.locator('#username').fill(username);page.locator('#password').fill(password);page.locator('#loginform button').click();page.locator('#workspace').wait_for(state='visible');page.locator('#autosend').uncheck();page.locator('#speak').uncheck();return {'models':page.locator('#model option').count()}
 check('authenticated UI and JS load',login)
 def vad():
  page.locator('#vad').click();wait('vadActive',15);wait("document.getElementById('text').value.length>0",60);text=page.locator('#text').input_value();assert 'bonjour' in text.lower(),text
  assert page.evaluate('vadActive');assert page.evaluate('vadSamples===0');page.locator('#vad').click();wait('!vadActive');assert page.evaluate('vadStream===null && vadContext===null');return {'transcript':text,'automatic_onset_and_silence_end':True,'auto_listening_kept_after_transcript':True,'released_microphone':True}
 check('WAV microphone -> AudioWorklet VAD -> silence stop -> real Whisper',vad)
 def playback():
  page.evaluate("()=>{talk('Le service est disponible.').catch(error);}");wait('audio && !audio.paused && audio.currentTime>0',40);page.locator('#stop').click();wait('audio===null');assert page.evaluate('objectURL===null');return {'real_piper_playback_interrupted':True}
 check('Piper real playback and stop',playback)
 def consecutive():
  page.locator('#new').click();page.locator('#retain').uncheck();page.locator('#autosend').check();page.locator('#speak').check();page.locator('#vad').click();wait('vadActive',15)
  wait("document.querySelectorAll('#history article.assistant').length>=2",120)
  wait('audio && !audio.paused && audio.currentTime>0',40);answer_count=page.locator('#history article.assistant').count();assert page.evaluate('vadActive');page.locator('#vad').click();page.locator('#stop').click();wait('!busy',40)
  return {'real_STT_Ollama_Piper_exchanges':answer_count,'single_initial_listen_click':True,'artificial_microphone_only':True}
 check('two consecutive automatic voice exchanges with actual Qwen',consecutive)
 def barge():
  page.locator('#autosend').uncheck();page.locator('#barge').check();page.locator('#vad').click();wait('vadActive',15)
  page.evaluate("()=>{lastAnswer='Voici une lecture de test suffisamment longue pour vérifier son interruption automatique par la voix. '.repeat(4);}")
  page.locator('#replay').click();wait('audio && !audio.paused',40);epoch=page.evaluate('voiceEpoch');wait('voiceEpoch>'+str(epoch)+' && audio===null',30)
  assert page.evaluate('vadActive');page.locator('#vad').click();wait('!busy && !vadSending',50);page.locator('#barge').uncheck()
  return {'real_audio_playback_interrupted_by_WAV_microphone':True,'physical_echo_not_tested':True}
 check('voice barge-in with artificial microphone and listening resume',barge)

 def silence():
  # Algorithm-level deterministic stream: does not substitute for acoustic tests.
  page.evaluate("()=>{vadActive=true;vadContext={sampleRate:48000};vadCooldown=0;for(let i=0;i<400;i++)vadFrame(new Float32Array(128));}")
  assert page.evaluate('vadStart===0 && vadFrames.length===0');page.evaluate('()=>{vadActive=false;vadContext=null;resetVad();}');return {'type':'simulated zero samples; no false onset'}
 check('silence rejection algorithm simulation',silence)
 def mobile():
  page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=str(OUT/'mobile-layout.png'),full_page=True);return {'viewport_emulation_only':True,'no_overflow':True}
 check('mobile layout',mobile)
 def logout():
  page.locator('#logout').click();page.locator('#loginpanel').wait_for(state='visible');assert page.request.get('http://localhost:8765/api/tools').status==401;assert not errors,errors;return {'private_tools_rejected':True,'page_errors':errors}
 check('logout privacy and JS errors',logout)
 browser.close()
if any(not x['passed'] for x in report['checks']):raise SystemExit(1)

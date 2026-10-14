from pathlib import Path
import subprocess,time,json,threading,datetime
P=Path('/home/adminjarvis/JARVIS/rapports/mission13a-preuves');R=Path('/opt/jarvis/voice');samples=[];stop=threading.Event()
def monitor():
 while not stop.is_set():
  p=subprocess.run(['nvidia-smi','--query-compute-apps=pid,process_name,used_memory','--format=csv,noheader'],text=True,capture_output=True)
  samples.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'processes':p.stdout,'stderr':p.stderr});stop.wait(.2)
t=threading.Thread(target=monitor);t.start();runs=[]
try:
 for name,engine,wav in [('A-stt','stt','A-tom.wav'),('D-tts','tts','D-tom.wav'),('D-stt','stt','D-tom.wav')]:
  command=[str(R/'scripts/run-offline'),engine,str(P/name),'--wav',str(P/wav)]
  p=subprocess.run(command,text=True,capture_output=True);(P/(name+'.launcher.log')).write_text(p.stdout+p.stderr);runs.append({'test':name,'exit_code':p.returncode})
  if p.returncode:raise RuntimeError(name+' failed')
  # Each subprocess fully terminates before the next fresh engine loads.
finally:
 stop.set();t.join();(P/'gpu-during-tests.json').write_text(json.dumps(samples,indent=2));(P/'acceptance-runs.json').write_text(json.dumps(runs,indent=2))
print(json.dumps(runs,indent=2))
for name in ['A-stt','D-stt']:
 r=json.loads((P/(name+'.result.json')).read_text());print(name,repr(r['transcript']),r['transcription_s'],r['word_differences'])

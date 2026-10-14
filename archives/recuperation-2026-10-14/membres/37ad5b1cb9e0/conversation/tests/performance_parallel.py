"""Real GPU generation alongside CPU voice; no stored conversation or memory."""
import sys,json,time,urllib.request,tempfile,threading,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from jarvis.core import Core
from jarvis.memory import Memory
report={'type':'real existing Ollama API + CPU voice workers, bounded one generation'}
with tempfile.TemporaryDirectory() as t:
 cfg=json.loads((ROOT/'config/13e.json').read_text());core=Core(cfg,Memory(t+'/test.sqlite'));samples=[];done=threading.Event()
 def sample():
  while not done.is_set():
   gpu=subprocess.run(['nvidia-smi','--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=5)
   samples.append({'time':time.time(),'gpu':gpu.stdout.strip(),'memory':subprocess.check_output(['free','-m'],text=True)})
   done.wait(.5)
 monitor=threading.Thread(target=sample);monitor.start();start=time.monotonic()
 def llm():
  payload={'model':cfg['default_model'],'messages':[{'role':'user','content':'Explique en français en environ cent mots le fonctionnement de la synthèse vocale locale.'}],'stream':False,'think':False,'options':{'num_predict':180,'num_ctx':8192}}
  with urllib.request.urlopen(urllib.request.Request(cfg['ollama_url']+'/api/chat',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'}),timeout=120) as r:result=json.load(r)
  report['generation_s']=time.monotonic()-start;report['answer']=result['message']['content'];report['ollama_durations']={k:result.get(k) for k in ['load_duration','eval_duration','eval_count']}
 worker=threading.Thread(target=llm);worker.start();voice_start=time.monotonic();report['transcription']=core.voice('stt',(ROOT/'runtime/test-input.wav').read_bytes())['text'];report['stt_s']=time.monotonic()-voice_start;tts_start=time.monotonic();core.voice('tts','Test fictif de synthèse vocale sur CPU pendant la génération du modèle.');report['tts_s']=time.monotonic()-tts_start;worker.join();done.set();monitor.join();report['samples']=samples;report['total_s']=time.monotonic()-start
Path('/home/adminjarvis/JARVIS/rapports/mission13e-preuves/parallel-performance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print({k:v for k,v in report.items() if k!='samples'})

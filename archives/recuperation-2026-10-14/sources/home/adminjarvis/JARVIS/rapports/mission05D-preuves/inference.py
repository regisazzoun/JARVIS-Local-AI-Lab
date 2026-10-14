import urllib.request,json,time,subprocess,pathlib,threading
p=pathlib.Path(__file__).parent;stop=threading.Event();samples=[]
def monitor():
 while not stop.is_set():
  d={'time':time.time()}
  for name,args in [('gpu',['--query-gpu=memory.used,utilization.gpu,temperature.gpu','--format=csv,noheader,nounits']),('processes',['--query-compute-apps=pid,process_name,used_memory','--format=csv,noheader,nounits'])]:
   r=subprocess.run(['nvidia-smi']+args,capture_output=True,text=True,timeout=10);d[name]=r.stdout.strip()
  samples.append(d);stop.wait(.5)
def api(path,data=None):
 req=urllib.request.Request('http://127.0.0.1:11434/api/'+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=300) as r:return json.load(r)
t=threading.Thread(target=monitor);t.start()
try:
 start=time.perf_counter();r=api('generate',{'model':'llama3.1:8b','prompt':'Réponds en français en trois phrases. Présente-toi comme le premier modèle local de JARVIS et explique simplement à quoi sert un GPU pour une intelligence artificielle.','stream':False,'keep_alive':'10m','options':{'num_ctx':4096,'num_predict':160,'temperature':0}});r['wall_seconds']=time.perf_counter()-start
 (p/'inference-resultat.json').write_text(json.dumps(r,indent=2,ensure_ascii=False));(p/'ollama-ps.json').write_text(json.dumps(api('ps'),indent=2));(p/'model-show.json').write_text(json.dumps(api('show',{'model':'llama3.1:8b'}),indent=2));print(r['response']);print('tokens/s',r['eval_count']/(r['eval_duration']/1e9));print('load s',r['load_duration']/1e9)
finally:
 stop.set();t.join();(p/'gpu-inference.json').write_text(json.dumps(samples,indent=2))

import urllib.request,urllib.error,json,pathlib,time,subprocess,threading,uuid
p=pathlib.Path(__file__).parent;base='http://192.168.1.99:3000';lines=pathlib.Path('/home/adminjarvis/JARVIS/open-webui/identifiants-admin.txt').read_text().splitlines();creds={'email':lines[0].split(': ',1)[1],'password':lines[1].split(': ',1)[1]};token=None

def api(path,data=None,auth=True):
 h={'Content-Type':'application/json'}
 if auth and token:h['Authorization']='Bearer '+token
 req=urllib.request.Request(base+path,data=None if data is None else json.dumps(data).encode(),headers=h)
 with urllib.request.urlopen(req,timeout=300) as r:return json.load(r)
a=api('/api/v1/auths/signin',creds,False);token=a['token'];assert a['role']=='admin'
models=api('/api/models');(p/'models.json').write_text(json.dumps(models,indent=2));assert any(m['id']=='llama3.1:8b' for m in models['data'])
try:api('/api/models',auth=False);raise RuntimeError('Unauthenticated model access allowed')
except urllib.error.HTTPError as e:assert e.code in (401,403)
stop=threading.Event();samples=[]
def monitor():
 while not stop.is_set():
  row={'time':time.time()}
  for n,args in [('gpu',['--query-gpu=memory.used,utilization.gpu,temperature.gpu','--format=csv,noheader,nounits']),('processes',['--query-compute-apps=pid,process_name,used_memory','--format=csv,noheader,nounits'])]:
   r=subprocess.run(['nvidia-smi']+args,capture_output=True,text=True,timeout=10);row[n]=r.stdout.strip()
  samples.append(row);stop.wait(.5)
t=threading.Thread(target=monitor);t.start();results=[]
try:
 for i,prompt in enumerate(['Réponds en une phrase : que signifie JARVIS ?','Calcule 17 × 23 et explique brièvement une méthode de vérification.','Écris une fonction Python qui calcule les nombres premiers inférieurs à n avec le crible d’Ératosthène, puis explique sa complexité.']):
  start=time.perf_counter();r=api('/api/chat/completions',{'model':'llama3.1:8b','messages':[{'role':'user','content':prompt}],'stream':False,'options':{'num_ctx':4096,'num_predict':256,'temperature':0}});elapsed=time.perf_counter()-start
  content=r['choices'][0]['message']['content'];row={'test':i+1,'prompt':prompt,'wall_seconds':elapsed,'response':r};results.append(row);(p/'inferences.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print('Test',i+1,'seconds',round(elapsed,2),'usage',r.get('usage'),content[:220],flush=True)
  u=str(uuid.uuid4());v=str(uuid.uuid4());chat={'title':'Mission 06 — Test '+str(i+1),'models':['llama3.1:8b'],'messages':[{'id':u,'role':'user','content':prompt},{'id':v,'role':'assistant','content':content,'model':'llama3.1:8b'}],'history':{'messages':{u:{'id':u,'parentId':None,'childrenIds':[v],'role':'user','content':prompt},v:{'id':v,'parentId':u,'childrenIds':[],'role':'assistant','content':content,'model':'llama3.1:8b','done':True}},'currentId':v},'timestamp':int(time.time()*1000)}
  stored=api('/api/v1/chats/new',{'chat':chat});row['saved_chat_id']=stored['id'];(p/'inferences.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
finally:stop.set();t.join();(p/'gpu-tests.json').write_text(json.dumps(samples,indent=2))

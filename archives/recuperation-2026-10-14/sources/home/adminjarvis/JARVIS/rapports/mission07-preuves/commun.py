import pathlib,json,urllib.request,time,subprocess
P=pathlib.Path(__file__).parent
WEB='http://192.168.1.99:3000';TOKEN=None

def req(url,data=None,token=None):
 h={'Content-Type':'application/json'}
 if token:h['Authorization']='Bearer '+token
 q=urllib.request.Request(url,data=None if data is None else json.dumps(data,ensure_ascii=False).encode(),headers=h)
 with urllib.request.urlopen(q,timeout=300) as r:return json.load(r)
def login():
 global TOKEN
 lines=pathlib.Path('/home/adminjarvis/JARVIS/open-webui/identifiants-admin.txt').read_text().splitlines()
 TOKEN=req(WEB+'/api/v1/auths/signin',{'email':lines[0].split(': ',1)[1],'password':lines[1].split(': ',1)[1]})['token']
def gpu():
 s=subprocess.check_output(['nvidia-smi','--query-gpu=memory.used,utilization.gpu,temperature.gpu','--format=csv,noheader,nounits'],text=True).strip();return [float(x.strip()) for x in s.split(',')]
def run(messages,options=None,route='direct',files=None):
 body={'model':'llama3.1:8b','messages':messages,'stream':False,'keep_alive':'30m'}
 if options is not None:body['options']=options
 if files:body['files']=files
 start=time.perf_counter();r=req(('http://127.0.0.1:11434/api/chat' if route=='direct' else WEB+'/api/chat/completions'),body,None if route=='direct' else TOKEN);elapsed=time.perf_counter()-start
 if route=='direct':text=r['message']['content'];metrics={k:r.get(k) for k in ['prompt_eval_count','prompt_eval_duration','eval_count','eval_duration','load_duration','total_duration','done_reason']}
 else:text=r['choices'][0]['message']['content'];metrics=r.get('usage',{})
 return {'request':body,'response':r,'text':text,'wall_seconds':elapsed,'gpu_after':gpu(),'metrics':metrics,'ollama_ps':req('http://127.0.0.1:11434/api/ps')}

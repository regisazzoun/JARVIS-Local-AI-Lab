"""Fixed D02 audio cases through existing authenticated canonical STT, no model input.
Secrets remain in existing operator authentication; only observations are returned.
"""
import os,json,time,hashlib,importlib.util,urllib.request,urllib.error,re
from pathlib import Path
cfg=json.loads(Path('/etc/jarvis/jl03-stt-probe.json').read_text());started=time.time()
private=Path('/home/adminjarvis/JARVIS/jl03-cor-p1-private/stt-auth');private.mkdir(mode=0o700,exist_ok=True);os.environ['MISSION11_EVIDENCE']=str(private)
spec=importlib.util.spec_from_file_location('reception','/home/adminjarvis/JARVIS/mission11/agentic/mission11/reception.py');auth=importlib.util.module_from_spec(spec);spec.loader.exec_module(auth)
def once(path,data=None):
 req=urllib.request.Request('http://localhost:8765'+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json','X-Jarvis-Request':'1'})
 with auth.client.open(req,timeout=30) as response:return json.load(response)
auth.call=once;auth.login()
def words(text):return re.findall(r"[^\W_]+",text.lower(),flags=re.UNICODE)
def distance(a,b):
 row=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  current=[i]
  for j,y in enumerate(b,1):current.append(min(current[-1]+1,row[j]+1,row[j-1]+(x!=y)))
  row=current
 return row[-1]
cases=[];busy=False
for case in cfg['cases']:
 raw=Path(case['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==case['sha256'],'Fixed fixture changed; do not infer a result'
 begin=time.time();req=urllib.request.Request('http://localhost:8765/api/stt',data=raw,headers={'Content-Type':case['content_type'],'X-Jarvis-Request':'1'})
 try:
  with auth.client.open(req,timeout=135) as response:code=response.status;observed=json.load(response)
 except urllib.error.HTTPError as e:
  code=e.code
  try:observed=json.loads(e.read())
  except ValueError:observed={'error':'NonJSON response'}
 result={'case':case['name'],'http_status':code,'elapsed_s':time.time()-begin,'observed':observed,'sha256':case['sha256']}
 if code==409:result['verdict']='INSUFFICIENT';busy=True
 elif case['expected']=='speech':
  expected=words(case['text']);actual=words(observed.get('text',''));wer=distance(expected,actual)/max(1,len(expected));result.update(expected_text=case['text'],word_error_rate=wer,verdict='PASS' if code==200 and actual and wer<=0.25 else 'FAIL')
 else:result['verdict']='PASS' if code==400 and not observed.get('text') else 'FAIL'
 cases.append(result)
 if busy:break
result={'observed_at':time.time(),'started':started,'endpoint':'Existing authenticated canonical /api/stt','implementation_actor':'Codex fixed test infrastructure','execution_actor':'See broker caller and canonical native invocation; operator preflight is not JARVIS execution','cases':cases,'status':'INSUFFICIENT' if busy else 'PASS' if len(cases)==len(cfg['cases']) and all(c['verdict']=='PASS' for c in cases) else 'FAIL','scope':'Baseline on controlled existing TTS01 WAV/silence/invalid input; not acceptance of browser capture or owner microphone'}
folder=Path('/var/lib/jarvis/projects/jl03-cor-p1/D02/logs');folder.mkdir(exist_ok=True);artifact=folder/('live-stt-'+str(time.time_ns())+'.json');artifact.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({**result,'artifact':str(artifact)},ensure_ascii=False));raise SystemExit(0 if result['status']=='PASS' else 2)

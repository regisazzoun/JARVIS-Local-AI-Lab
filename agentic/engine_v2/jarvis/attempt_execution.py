"""Observed execution over the existing broker and persistent AttemptLedger."""
import concurrent.futures,hashlib,json,os,shlex,socket,threading,time,uuid
from pathlib import Path
from .attempt_ledger import AttemptLedger, digest
from . import host_client

HOSTS={'Dell1':'dell-observe','Dell2':'dell2'}
WRAPPER=r'''
import json,subprocess,pathlib,time,os,signal,hashlib
config=json.loads(CONFIG)
root=pathlib.Path('.p2-reception');root.mkdir(exist_ok=True)
base=root/config['attempt']
def hashes():
 return {name:hashlib.sha256(pathlib.Path(name).read_bytes()).hexdigest() if pathlib.Path(name).exists() else None for name in config['correction_files']}
before=hashes()
p=subprocess.Popen(['bash','-c',config['command']],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
start={'attempt':config['attempt'],'problem':config['problem'],'command_sha256':config['command_sha256'],'pid':p.pid,'started_at':time.time(),'child_started':True}
base.with_suffix('.started.json').write_text(json.dumps(start))
with (root/'executions.jsonl').open('a') as log:log.write(json.dumps(start)+'\n')
try:out,err=p.communicate(timeout=25)
except subprocess.TimeoutExpired:
 os.killpg(p.pid,signal.SIGKILL);out,err=p.communicate();err+='\ncontrolled child deadline reached'
receipt={'start':start,'execution':{'returncode':p.returncode,'stdout':out,'stderr':err,'finished_at':time.time()},'correction_before':before,'correction_after':hashes()}
raw=json.dumps(receipt).encode();base.with_suffix('.result.json').write_bytes(raw)
print(json.dumps({'attempt':config['attempt'],'receipt_sha256':hashlib.sha256(raw).hexdigest(),'receipt':receipt}))
'''
class FaultChannel:
 """Real one-request Unix transport: close listener, or drop an actual reply."""
 def __init__(self,store,mission,attempt,mode):
  self.store=store;self.m=mission;self.attempt=attempt;self.mode=mode
  parent=store.root/'runtime/p2-channels';parent.mkdir(exist_ok=True,mode=0o700)
  self.path=parent/(attempt[:12]+'.sock');self.server=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);self.server.bind(str(self.path));self.server.listen(1);self.thread=None
  self.thread=threading.Thread(target=self.forward,daemon=True);self.thread.start()
 def forward(self):
  try:
   downstream,_=self.server.accept()
   with downstream, socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as upstream:
    data=b''
    while not data.endswith(b'\n'):
     block=downstream.recv(65536)
     if not block:raise RuntimeError('No complete request')
     data+=block
    upstream.connect(host_client.SOCKET);upstream.sendall(data);response=b''
    while not response.endswith(b'\n'):
     block=upstream.recv(65536)
     if not block:break
     response+=block
    parsed=json.loads(response)
    if self.mode=='worker_unavailable':
     downstream.sendall(response)
     self.store.event(self.m,'p2_worker_channel_health',actor='Codex-fixture',result={'attempt':self.attempt,'broker_evidence_id':parsed.get('evidence_id'),'actual_healthy_reply_forwarded':True})
    else:
     payload=json.loads(parsed.get('result',{}).get('stdout','{}'))
     self.store.event(self.m,'p2_fault_injection',actor='Codex-fixture',result={'attempt':self.attempt,'fault':'response_dropped_after_real_upstream_reply','broker_evidence_id':parsed.get('evidence_id'),'response_sha256':hashlib.sha256(response).hexdigest(),'receipt_sha256':payload.get('receipt_sha256'),'response_bytes':len(response),'not_a_simulated_broker_result':True})
    self.server.close()
  except Exception as error:
   self.store.event(self.m,'p2_fixture_error',actor='Codex-fixture',result={'attempt':self.attempt,'error':str(error)})
 def close(self):
  if self.thread:self.thread.join(timeout=5)
  self.server.close();self.path.unlink(missing_ok=True)

class AttemptExecutor:
 def __init__(self,store,mission,project='mission26-phase2'):
  self.store=store;self.m=mission;self.project=project;self.ledger=AttemptLedger(store,mission)
 def call(self,host,command,endpoint=None,project=None):
  args={'host':HOSTS[host],'action':'project_exec','project':project or self.project,'command':command}
  token=self.store.begin_call(self.m,None,'host_remote',args);start=time.monotonic()
  try:
   raw=host_client.request('host_remote',args,workload_class='mission',_endpoint=endpoint)
   result={'ok':True,'result':{**raw['result'],'evidence_id':raw.get('evidence_id')},'tool':'host_remote'}
  except Exception as error:
   raw=getattr(error,'response',{});result={'ok':False,'error':str(error),'result':raw.get('result',{}),'diagnostic':raw.get('diagnostic',{}),'error_code':raw.get('error_code',type(error).__name__)}
  self.store.finish_call(token,result,time.monotonic()-start)
  proof=self.store.event(self.m,'p2_transport_observed',actor='JARVIS-engine',result={'invocation':token,'executor':host,'response':result,'endpoint_kind':'controlled_reception_channel' if endpoint else 'production_broker'})
  return result,proof,token
 def read(self,row,kind):
  command='python3 -c '+shlex.quote("import pathlib,json; p=pathlib.Path("+repr('.p2-reception/'+row['id']+'.'+kind+'.json')+"); print(p.read_text() if p.exists() else '{}')")
  r,proof,token=self.call(row['executor'],command)
  if not r['ok'] or r['result'].get('returncode')!=0:return {},proof
  try:return json.loads(r['result']['stdout']),proof
  except (ValueError,KeyError):return {},proof
 def started(self,row,start,transport_proof):
  if not start.get('child_started') or start.get('attempt')!=row['id'] or start.get('command_sha256')!=digest(row['request']['command']):raise ValueError('Start marker does not match actual attempt')
  evidence=self.store.event(self.m,'p2_started_observed',actor='JARVIS-engine',result={'attempt':row['id'],'marker':start,'transport_evidence':transport_proof})
  current=self.ledger.get(row['id'])
  if current['state']=='DISPATCHED' or (current['state']=='VALIDATION_INCONCLUSIVE' and current['unknown_outcome']):self.ledger.transition(row['id'],'RUNNING',evidence=evidence,result={'started':start})
  return evidence
 def complete(self,row,receipt,transport_proof):
  self.started(row,receipt['start'],transport_proof);execution=receipt['execution'];code=execution['returncode']
  result={'returncode':code,'started':receipt['start'],'execution':execution,'verified':False,'transport_evidence':transport_proof}
  if code!=0:state='EXECUTED_TEST_FAILED' if row['phase'] in ('test','correction_test') else 'EXECUTION_FAILED'
  else:
   verifier=row['request'].get('verification')
   if not verifier:state='VALIDATION_INCONCLUSIVE';result['verification']={'verdict':'INSUFFICIENT','reason':'No verifier provided'}
   else:
    prior=[e for e in self.store.events(self.m,limit=100000) if e['result'].get('attempt')==row['id']]
    observed={e['result'].get('observation',{}).get('verification_evidence') for e in prior if e['kind']=='p2_result_observed'}-{None}
    sequence=max([len(observed)]+[e['result']['sequence'] for e in prior if e['kind']=='p2_verification_dispatched'])
    if sequence>=3:raise ValueError('Three verification attempts already dispatched; targeted escalation required, no fourth')
    self.store.event(self.m,'p2_verification_dispatched',actor='JARVIS-engine',result={'attempt':row['id'],'sequence':sequence+1,'command':verifier,'original_execution_not_repeated':True})
    validation,vproof,token=self.call(row['executor'],verifier);result['verification_evidence']=vproof
    result['verification_execution']={k:validation.get('result',{}).get(k) for k in ('returncode','stdout','stderr')}
    result['verification_transport_ok']=validation['ok']
    try:verdict=json.loads(validation['result']['stdout']) if validation['ok'] and validation['result'].get('returncode')==0 else {}
    except (ValueError,KeyError):verdict={}
    result['verification']=verdict
    contract=row['request'].get('verification_contract')
    if contract and validation['ok'] and validation['result'].get('returncode')==0:
     from .verification import evaluate
     semantic=evaluate(validation['result']['stdout'],contract);result['verification_semantic']=semantic
     if semantic['status']=='PASS':state='SUCCESS';result['verified']=True
     else:state='EXECUTED_TEST_FAILED'
    elif verdict.get('verdict')=='PASS':state='SUCCESS';result['verified']=True
    elif verdict.get('verdict')=='FAIL':state='EXECUTED_TEST_FAILED'
    else:state='VALIDATION_INCONCLUSIVE'
  evidence=self.store.event(self.m,'p2_result_observed',actor='JARVIS-engine',result={'attempt':row['id'],'receipt':receipt,'observation':result,'state':state})
  self.ledger.transition(row['id'],state,evidence=evidence,result=result,unknown=False)
  if state in ('EXECUTION_FAILED','EXECUTED_TEST_FAILED') and row['phase']=='correction_test':
   changed=bool(receipt['correction_before']) and receipt['correction_before']!=receipt['correction_after']
   self.ledger.failure(row['id'],correction_changed=changed)
  return self.result(row['id'])
 def result(self,attempt):
  row=self.ledger.get(attempt)
  with self.store.db() as c:p=dict(c.execute('SELECT * FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(self.m,row['problem'])).fetchone())
  return {'attempt':attempt,'state':row['state'],'unknown_outcome':bool(row['unknown_outcome']),'problem':row['problem'],'failed_cycles':p['failed_cycles'],'infra_incidents':p['infra_incidents'],'problem_state':p['state'],'result':row['result'],'executor':row['executor']}
 def run(self,scope,descriptor,key,executor,phase,command,verification='',fault=None,correction_files=(),verification_contract=None):
  problem=self.ledger.problem(scope,descriptor);request={'command':command,'verification':verification,'correction_files':list(correction_files),'fault':fault,'verification_contract':verification_contract}
  begin=self.ledger.begin(problem,key,executor,phase,request)
  if 'attempt' not in begin or begin.get('cached') or begin.get('requires_observation'):return begin
  row=self.ledger.get(begin['attempt']);self.ledger.transition(row['id'],'DISPATCHED')
  cfg={'attempt':row['id'],'problem':problem,'command':command,'command_sha256':digest(command),'correction_files':list(correction_files)}
  wrapper='python3 -c '+shlex.quote(WRAPPER.replace('CONFIG',repr(json.dumps(cfg))))
  channel=FaultChannel(self.store,self.m,row['id'],fault) if fault in ('worker_unavailable','drop_reply') else None
  try:
   if fault=='worker_unavailable':
    healthy,health_proof,_=self.call(executor,'python3 -c '+shlex.quote('print("reception-worker-healthy")'),str(channel.path))
    if not healthy['ok']:raise ValueError('Cannot assert worker became unavailable: initial health check failed')
    channel.thread.join(timeout=5)
    self.store.event(self.m,'p2_worker_channel_stopped',actor='Codex-fixture',result={'attempt':row['id'],'healthy_evidence':health_proof,'actual_listener_closed':True,'production_broker_and_Dell_not_stopped':True})
   with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
    future=pool.submit(self.call,executor,wrapper,str(channel.path) if channel else None,'p2-deliberately-ungranted' if fault=='policy_denied' else None)
    witnessed=False
    while not future.done():
     if not witnessed and fault!='worker_unavailable' and fault!='policy_denied':
      marker,proof=self.read(row,'started')
      if marker:self.started(row,marker,proof);witnessed=True
     if not future.done():time.sleep(0.15)
    response,proof,token=future.result()
   if not response['ok']:
    known_not_executed=fault in ('policy_denied','worker_unavailable')
    evidence=self.store.event(self.m,'p2_dispatch_failure_observed',actor='JARVIS-engine',result={'attempt':row['id'],'transport_evidence':proof,'known_not_executed':known_not_executed,'fault_fixture':fault,'response':response})
    self.ledger.transition(row['id'],'NOT_EXECUTED' if known_not_executed else 'VALIDATION_INCONCLUSIVE',evidence=evidence,result={'reason':fault or 'transport_error','transport_evidence':proof,'response':response},unknown=not known_not_executed)
    self.ledger.failure(row['id'],infrastructure=True)
    return self.result(row['id'])
   payload=json.loads(response['result']['stdout']);receipt=payload['receipt']
   if payload['attempt']!=row['id'] or hashlib.sha256(json.dumps(receipt).encode()).hexdigest()!=payload['receipt_sha256']:raise ValueError('Receipt mismatch')
   return self.complete(row,receipt,proof)
  finally:
   if channel:channel.close()
 def observe(self,attempt,verification=None,verification_contract=None):
  row=self.ledger.get(attempt)
  if not row['unknown_outcome'] and row['state']!='VALIDATION_INCONCLUSIVE':return {'cached':True,**self.result(attempt)}
  if verification is not None:
   self.store.event(self.m,'p2_verification_revised',actor='JARVIS-engine',result={'attempt':attempt,'previous':row['request'].get('verification'),'new':verification,'original_execution_not_repeated':True})
  revisions=[e for e in self.store.events(self.m,limit=100000) if e['kind']=='p2_verification_revised' and e['result'].get('attempt')==attempt]
  if revisions:row['request']={**row['request'],'verification':revisions[-1]['result']['new']}
  contracts=[e for e in self.store.events(self.m,limit=100000) if e['kind']=='p2_verification_contract_bound' and e['result'].get('attempt')==attempt]
  existing=row['request'].get('verification_contract') or (contracts[-1]['result']['contract'] if contracts else None)
  if verification_contract is not None:
   if existing and existing!=verification_contract:raise ValueError('Owner verification contract immutable')
   if not existing:self.store.event(self.m,'p2_verification_contract_bound',actor='JARVIS-engine',result={'attempt':attempt,'contract':verification_contract,'original_execution_not_repeated':True})
   existing=verification_contract
  if existing:row['request']={**row['request'],'verification_contract':existing}
  receipt,proof=self.read(row,'result')
  if not receipt:return {'requires_observation':True,**self.result(attempt)}
  if row['request'].get('fault')=='drop_reply':
   injections=[e for e in self.store.events(self.m,limit=100000) if e['kind']=='p2_fault_injection' and e['result'].get('attempt')==attempt]
   expected=injections[-1]['result'].get('receipt_sha256') if injections else None
   if not expected or hashlib.sha256(json.dumps(receipt).encode()).hexdigest()!=expected:raise ValueError('Independent receipt differs from SHA of the real dropped broker reply')
  return self.complete(row,receipt,proof)

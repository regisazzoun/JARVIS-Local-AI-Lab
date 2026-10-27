"""Opt-in model-directed execution. No application diagnosis, patch or test selection.
All state lives in MissionStore; the existing broker remains the permission boundary.
"""
import hashlib
import json
import re
import shlex
import time
import uuid
from pathlib import Path

PROJECT = 'mission26-phase1'
ROOT = '/opt/jarvis-lab/mission26-phase1'
LOCAL = Path('/var/lib/jarvis/projects/mission26-phase1')
HOSTS = {'Dell1': 'dell-observe', 'Dell2': 'dell2'}
TOOLS = ['authority_plan', 'authority_revise_plan', 'authority_work', 'authority_sync', 'authority_finish', 'mission_note', 'mission_evidence', 'authority_resources', 'authority_edit', 'authority_analyze', 'authority_read_execution','context_checkpoint','context_resume','context_recall']

# This observer is infrastructure, not an application test. Commands are model supplied.
RUNNER = r'''
import subprocess,os,json,hashlib,pathlib,resource

def manifest():
 out={}
 for p in sorted(pathlib.Path('.').rglob('*')):
  if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts and '.receipts' not in p.parts and p.suffix in ('.py','.md','.json','.txt','.mjs','.js'):
   out[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
 return out

def limited():
 os.nice(10)
 cpus=sorted(os.sched_getaffinity(0));os.sched_setaffinity(0,cpus[-2:])
 resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
 resource.setrlimit(resource.RLIMIT_CPU,(35,35))
 resource.setrlimit(resource.RLIMIT_FSIZE,(8*1024**2,8*1024**2))
 resource.setrlimit(resource.RLIMIT_NOFILE,(128,128))

before=manifest()
try:
 p=subprocess.run(['timeout','--kill-after=2','45','bash','-c',COMMAND],capture_output=True,text=True,preexec_fn=limited)
 observed={'returncode':p.returncode,'stdout':p.stdout[:20000],'stderr':p.stderr[:8000], 'output_truncated':len(p.stdout)>20000 or len(p.stderr)>8000}
except Exception as e:observed={'returncode':125,'stderr':str(e),'stdout':''}
after=manifest()
print(json.dumps({'before':before,'after':after,'execution':observed,'limits':{'nice':10,'cpu_cores':2,'memory_gib':4,'wall_seconds':45,'gpu':False}}))
'''

def runner_program(command,roots=None):
 body=RUNNER.replace('COMMAND',repr(command))
 if roots:
  if not isinstance(roots,list) or any(not isinstance(r,str) or Path(r).is_absolute() or '..' in Path(r).parts for r in roots):raise ValueError('Safe owner manifest roots required')
  body=body.replace("pathlib.Path('.').rglob('*')", "{p for root in "+repr(roots)+" for p in pathlib.Path(root).rglob('*')}")
 return body

def receipt_program(command,remote_path,roots=None):
 body=runner_program(command,roots)
 body=body.replace("'__pycache__' not in p.parts", "'__pycache__' not in p.parts and '.receipts' not in p.parts")
 body=body.replace("p.stdout[:20000]", "p.stdout").replace("p.stderr[:8000]", "p.stderr")
 body=body.replace("len(p.stdout)>20000 or len(p.stderr)>8000", "False")
 marker="print(json.dumps({'before':before,'after':after,'execution':observed,'limits':{'nice':10,'cpu_cores':2,'memory_gib':4,'wall_seconds':45,'gpu':False}}))"
 replacement="""receipt={'before':before,'after':after,'execution':observed,'limits':{'nice':10,'cpu_cores':2,'memory_gib':4,'wall_seconds':45,'gpu':False}}
raw=json.dumps(receipt).encode()
target=pathlib.Path(RECEIPT_PATH);target.parent.mkdir(exist_ok=True);target.write_bytes(raw)
print(json.dumps({'receipt_path':str(target),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'process_returncode':observed['returncode']}))""".replace('RECEIPT_PATH',repr(remote_path))
 assert marker in body
 body=body.replace(marker,replacement)
 return body

def edit_program(edits):
 """Literal model-authored edits; file content is data, never evaluated as code."""
 return """import json, pathlib, os, tempfile, ast
edits=json.loads(PAYLOAD)
root=pathlib.Path.cwd().resolve()
pending=[]
seen=set()
for edit in edits:
 relative=pathlib.Path(edit['path'])
 if relative.is_absolute() or '..' in relative.parts or not relative.parts or relative.parts[0] in ('.receipts','runtime'):
  raise ValueError('Edit path outside authorized source workspace')
 target=root/relative
 if not target.resolve().is_relative_to(root) or target.is_symlink():
  raise ValueError('Symlink or path escape refused')
 if str(relative) in seen:raise ValueError('Duplicate edit path; combine changes for one file')
 seen.add(str(relative))
 if edit['old'] is None:
  if target.exists():raise ValueError('New-file edit target already exists: '+str(relative))
  content=edit['new']
 else:
  previous=target.read_text()
  if not edit['old'] or previous.count(edit['old'])!=1:
   raise ValueError('Edit anchor must match exactly once: '+str(relative))
  content=previous.replace(edit['old'],edit['new'],1)
 if len(content.encode())>2*1024*1024:raise ValueError('Candidate file too large')
 if target.suffix=='.py':ast.parse(content,filename=str(relative))
 pending.append((target,content))
for target,content in pending:
 target.parent.mkdir(parents=True,exist_ok=True)
 fd,name=tempfile.mkstemp(prefix='.jarvis-edit-',dir=target.parent)
 try:
  with os.fdopen(fd,'w') as stream:stream.write(content);stream.flush();os.fsync(stream.fileno())
  if target.exists():os.chmod(name,target.stat().st_mode & 0o777)
  os.replace(name,target)
 finally:
  if os.path.exists(name):os.unlink(name)
print(json.dumps({'written_files':[str(target.relative_to(root)) for target,_ in pending]}))
""".replace('PAYLOAD',repr(json.dumps(edits,ensure_ascii=False)))

def version(manifest):
 return hashlib.sha256(json.dumps(manifest,sort_keys=True).encode()).hexdigest()

def budget(state, issue, enforce=True):
 value=state.setdefault('issues',{}).setdefault(issue,{'failed_cycles':0,'delegation_failures':0})
 if enforce and value['failed_cycles']-value.get('correction_resolved_through',0)>=3:raise ValueError('BLOQUÉ: trois cycles échoués pour cette anomalie; dossier Codex requis, compteur conservé')
 if enforce and value['delegation_failures']-value.get('delegation_resolved_through',0)>=3:raise ValueError('BLOQUÉ: trois délégations échouées; dossier Codex requis')
 return value

class Authority:
 def __init__(self,reg):
  self.reg=reg;self.store=reg.mission_store;self.m=reg.context['mission_id'];self.t=reg.context.get('task_id')
  self.spec=json.loads(self.store.get(self.m)['spec'])
  workspace=self.spec.get('authority_workspace',{})
  self.project=workspace.get('project',PROJECT);self.remote_root=workspace.get('remote_root',ROOT);self.local=Path(workspace.get('local_root',str(LOCAL)))
  if not re.fullmatch(r'[a-zA-Z0-9_-]+',self.project) or not self.remote_root.startswith('/opt/jarvis-lab/') or '..' in Path(self.remote_root).parts or '..' in self.local.parts or not self.local.is_relative_to('/var/lib/jarvis/projects'):raise ValueError('Invalid declared authorized workspace')
  if not self.spec.get('distributed_authority'):raise ValueError('Distributed authority is opt-in for this mission only')
 def state(self):
  if hasattr(self.store,'db'):
   with self.store.db() as c:row=c.execute("SELECT result FROM mission_events WHERE mission=? AND kind='authority_state' ORDER BY id DESC LIMIT 1",(self.m,)).fetchone()
   return json.loads(row['result']) if row else {'issues':{},'executions':{},'syncs':[]}
  rows=[e for e in self.store.events(self.m,limit=100000) if e['kind']=='authority_state']
  return rows[-1]['result'] if rows else {'issues':{},'executions':{},'syncs':[]}
 def event(self,kind,result,arguments=None,actor='JARVIS-engine'):
  return self.store.event(self.m,kind,self.t,actor,arguments=arguments,result=result)
 def save(self,state):self.event('authority_state',state)
 def decision(self,args):
  if hasattr(self.store,'db'):
   with self.store.db() as c:row=c.execute("SELECT id,result FROM mission_events WHERE mission=? AND kind='inference_finished' ORDER BY id DESC LIMIT 1",(self.m,)).fetchone()
   events=[{'id':row['id'],'result':json.loads(row['result'])}] if row else []
  else:events=[e for e in self.store.events(self.m,limit=100000) if e['kind']=='inference_finished']
  metrics=events[-1]['result'].get('metrics',{}) if events else {}
  if metrics.get('effective_model')!='qwen3-coder-next:q4_K_M' or metrics.get('node')!='Dell1':
   raise ValueError('Decision requires actual Qwen80B inference receipt on dell-1; observed '+str({k:metrics.get(k) for k in ('node','effective_model')}))
  return self.event('authority_model_decision',{'model':metrics['effective_model'],'inference_machine':metrics['node'],'inference_event':events[-1]['id'],'instruction':args},actor='JARVIS/Qwen80B')
 def remote(self,host,command):
  args={'host':HOSTS[host],'action':'project_exec','project':self.project,'command':command}
  token=self.store.begin_call(self.m,self.t,'host_remote',args);start=time.monotonic()
  result=self.reg.execute('host_remote',args)
  self.store.finish_call(token,result,time.monotonic()-start)
  if not result.get('ok'):raise RuntimeError(json.dumps(result,ensure_ascii=False)[:2000])
  return result['result'],token
 def resources(self,a):
  result={}
  for label,host in HOSTS.items():
   args={'host':host,'action':'resources'}
   token=self.store.begin_call(self.m,self.t,'host_remote',args);start=time.monotonic();r=self.reg.execute('host_remote',args);self.store.finish_call(token,r,time.monotonic()-start)
   result[label]={'invocation':token,'ok':r.get('ok'),'stdout':r.get('result',{}).get('stdout','')[:5000]}
  state=self.state();state['resources']=result;self.save(state)
  return result
 def durable_run(self,host,command,operation,state):
  """Repair for demonstrated broker truncation: full immutable receipt as bytes."""
  receipt_id=uuid.uuid4().hex
  remote_path=self.remote_root+'/.receipts/'+receipt_id+'.json'
  operation['receipt_path']=remote_path;self.save(state)
  body=receipt_program(command,remote_path,self.spec.get('authority_manifest_roots'))
  raw,call=self.remote(host,'python3 -c '+shlex.quote(body));header=json.loads(raw['stdout'])
  local=self.local/'receipts'/self.m/(receipt_id+'.json');local.parent.mkdir(parents=True,exist_ok=True)
  args={'host':HOSTS[host],'action':'project_download','project':self.project,'path':remote_path,'local_path':str(local)}
  token=self.store.begin_call(self.m,self.t,'host_remote',args);start=time.monotonic();r=self.reg.execute('host_remote',args);self.store.finish_call(token,r,time.monotonic()-start)
  if not r.get('ok'):raise RuntimeError('Receipt persisted remotely; download failed. Do not rerun command. '+str(r)[:500])
  data=local.read_bytes()
  if hashlib.sha256(data).hexdigest()!=header['sha256']:raise ValueError('Complete receipt digest mismatch')
  observed=json.loads(data);observed['full_receipt']={'remote':remote_path,'local':str(local),'sha256':header['sha256'],'bytes':len(data),'download_invocation':token}
  for field in ('stdout','stderr'):
   text=observed['execution'].get(field,'')
   if len(text)>2000:
    observed['execution'][field]=text[:1500]+'\n[EXCERPT; complete immutable receipt at full_receipt]\n'+text[-500:]
    observed['execution'][field+'_model_excerpt']=True
  return observed,call
 def read_execution(self,a):
  reference=str(a['reference']);entry=self.state().get('executions',{}).get(reference)
  if not entry:raise ValueError('Execution reference is not recorded in this mission')
  execution=entry['execution'];complete=not execution.get('output_truncated') and not execution.get('stdout_model_excerpt')
  receipt=entry.get('full_receipt')
  if receipt:
   path=Path(receipt['local']).resolve()
   if not path.is_relative_to((self.local/'receipts'/self.m).resolve()):raise ValueError('Receipt path outside this mission')
   data=path.read_bytes()
   if hashlib.sha256(data).hexdigest()!=receipt['sha256']:raise ValueError('Receipt digest changed')
   execution=json.loads(data)['execution'];complete=not execution.get('output_truncated')
  stream=a.get('stream','stderr');lines=execution.get(stream,'').splitlines();start=a.get('start_line',1)-1
  content='\n'.join(lines[start:start+min(a.get('max_lines',40),80)])
  return {'reference':int(reference),'executor':entry['host'],'kind':entry['kind'],'observed_process_returncode':execution['returncode'],'stream':stream,'start_line':start+1,'content':content[:8000],'total_lines':len(lines),'source_complete':complete,'excerpt_truncated':len(content)>8000,'source_version':version(entry['after']),'full_receipt':receipt}
 def analyze_latest(self,a):
  issue=self.state().get('issues',{}).get(a['issue'],{})
  reference=issue.get('last_failed_test')
  if not reference:raise ValueError('No observed failed test exists for this issue')
  return self.work({'issue':a['issue'],'kind':'analyze','reference':reference,'summary':a['summary']})
 def edit(self,a):
  command='python3 -c '+shlex.quote(edit_program(a['edits']))
  return self.work({'issue':a['issue'],'kind':'correct','summary':a['summary'],'operation_id':a['operation_id'],'executor':a['executor'],'command':command})
 def work(self,a):
  issue=a['issue']
  if issue not in self.spec['authority_requirements']:raise ValueError('Unknown stable owner requirement; allowed EXACT ids: '+str(self.spec['authority_requirements']))
  state=self.state();kind=a['kind']
  if self.spec.get('authority_readonly_validation') and kind not in ('test','analyze','accept'):raise ValueError('Owner assigned test-only validation; source modifications/inspection are not this task')
  v=budget(state,issue,enforce=kind not in ('analyze','accept'))
  key=a.get('operation_id')
  if kind in ('inspect','correct','test') and not key:raise ValueError('operation_id required, unique per intended execution, reuse it for transport retry')
  previous=state.get('operations',{}).get(key) if key else None
  if previous:
   if previous['arguments']!=a:
    raise ValueError('operation_id reused for different arguments: '+json.dumps({'operation_id':key,'registered_arguments':previous['arguments'],'requested_arguments':a,'original_outcome_known':bool(previous.get('result')),'remedy':'For a DIFFERENT intended command choose a new unique operation_id. For retry of the SAME command preserve ALL original arguments. No command was executed by this refusal; never rerun an uncertain operation blindly.'},ensure_ascii=False))
   if previous.get('result'):return previous['result']
   raise ValueError('Execution outcome uncertain; inspect receipts before a new operation, never blindly repeat')
  decision=self.decision(a)
  if kind=='analyze':
   ref=str(a.get('reference',''));obs=state['executions'].get(ref)
   if not obs or obs.get('issue')!=issue or 'execution' not in obs:raise ValueError('Analyze references an actual executed operation for the same requirement, regardless of its declared phase')
   v['analyzed']=ref;v['analysis']=a['summary'];self.save(state)
   return {'decision':decision,'analyzed':ref,'execution_analyzed':True,'declared_kind':obs['kind'],'observed_returncode':obs['execution']['returncode'],'failed_cycles':v['failed_cycles']}
  if kind=='accept':
   ref=str(a.get('reference',''));obs=state['executions'].get(ref);source=state['executions'].get(str(a.get('source_reference','')))
   if not obs or obs['issue']!=issue or obs['kind']!='test' or obs['execution']['returncode']!=0 or obs['execution'].get('output_truncated'):
    raise ValueError('Accept requires the EXECUTION reference of an actual passed, untruncated test, not a decision id. Observed tests: '+str([{'reference':k,'executor':r.get('host'),'process_returncode':r['execution']['returncode']} for k,r in state['executions'].items() if r['kind']=='test' and r['issue']==issue][-3:]))
   if obs['before']!=obs['after']:raise ValueError('Test modified tracked files: rerun on a stable version')
   readonly=self.spec.get('authority_readonly_validation') is True
   if not source or source['kind']!=('test' if readonly else 'correct') or source['host']==obs['host'] or source['after']!=obs['after']:
    raise ValueError('Independent validation requires source_reference of an actual CORRECTION EXECUTION on the other Dell, at EXACT full manifest. Candidates: '+str([{'reference':k,'host':r['host'],'same_manifest':r['after']==obs['after']} for k,r in state['executions'].items() if r.get('kind')=='correct' and r.get('issue')==issue][-3:]))
   if not readonly and source['before']==source['after']:raise ValueError('Source correction has no observed file change; a declared correction is not an actual modification')
   if readonly and (source['execution']['returncode']!=0 or source['before']!=source['after']):raise ValueError('Test-only peer must have actually passed on stable source')
   current,_=self.remote(obs['host'],"python3 -c "+shlex.quote(runner_program('true',self.spec.get('authority_manifest_roots'))))
   fresh=json.loads(current['stdout'])
   if fresh['after']!=obs['after']:raise ValueError('Validator workspace changed since the passed test')
   v.pop('pending_correction',None)
   v['accepted']={'decision':decision,'test':ref,'source':str(a['source_reference']),'version':version(obs['after']),'host':obs['host'],'independent':True,'validation_scope':'test-only, no correction claimed' if readonly else 'source correction and independent test'}
   from jarvis.authority_attempts import AuthorityAttempts
   AuthorityAttempts(self).accepted(issue,a['source_reference'],v['accepted'])
   self.save(state);self.event('authority_validation',v['accepted'],actor='JARVIS/Qwen80B')
   return {'accepted':True,**v['accepted'],'meaning':'Passed process and exact cross-host source provenance; application adequacy remains independently reviewed by Codex'}
  host=a.get('executor');command=a.get('command')
  if host not in HOSTS or not command:raise ValueError('inspect/correct/test require executor Dell1 or Dell2 and command')
  if kind=='correct' and v.get('last_failed_test') and int(v['last_failed_test'])>v.get('correction_resolution_event',0) and v.get('analyzed')!=v['last_failed_test']:
   raise ValueError('Analyze the last actual failed test before another correction')
  from jarvis.authority_attempts import AuthorityAttempts
  persistent=AuthorityAttempts(self);attempt=persistent.begin(a,state)
  if attempt.get('cached'):return attempt['value']
  state.setdefault('operations',{})[key]={'arguments':a,'decision':decision,'attempt':attempt['attempt']};self.save(state)
  self.event('authority_dispatch',{'decision':decision,'executor':host,'command':command})
  try:
   if self.spec.get('authority_durable_receipts'):
    observed,call=self.durable_run(host,command,state['operations'][key],state)
   else:
    raw,call=self.remote(host,'python3 -c '+shlex.quote(runner_program(command,self.spec.get('authority_manifest_roots'))))
    observed=json.loads(raw['stdout'])
  except Exception as error:
   persistent.uncertain(attempt['attempt'],error)
   v['delegation_failures']+=1;self.save(state)
   if v['delegation_failures']-v.get('delegation_resolved_through',0)>=3:self.event('authority_escalation',{'issue':issue,'reason':'Three delegation failures','state':v},actor='JARVIS-engine')
   self.event('authority_delegation_failure',{'decision':decision,'executor':host,'error':str(error),'count':v['delegation_failures']})
   raise
  observed.update(issue=issue,host=host,kind=kind,decision=decision,broker_invocation=call)
  ref=str(self.event('authority_execution',observed));state['executions'][ref]=observed
  if kind=='inspect' and observed['before']!=observed['after']:
   persistent.finish(attempt['attempt'],observed,{'reference':int(ref),'executor':host,'execution':observed['execution']})
   self.save(state);raise ValueError('Inspection changed tracked files; classification violated, changes retained in evidence')
  if kind=='correct':v['pending_correction']=ref;v.pop('accepted',None)
  if kind=='test':
   v['last_test']=ref
   from jarvis.authority_attempts import test_infrastructure_error
   infrastructure=test_infrastructure_error(observed['execution'])
   if infrastructure:
    v['delegation_failures']+=1
    self.event('authority_test_not_reached',{'issue':issue,'execution':ref,'reason':'Observed missing dependency, missing file or command before test','delegation_failures':v['delegation_failures']})
   if observed['execution']['returncode']!=0 and not infrastructure:
    v['last_failed_test']=ref
    pending=state['executions'].get(v.get('pending_correction'),{})
    if pending and pending['before']!=pending['after'] and pending['after']==observed['after']:
     v['failed_cycles']+=1;v.pop('pending_correction',None)
     if v['failed_cycles']>=3:self.event('authority_escalation',{'issue':issue,'reason':'Three failed correction/test cycles','state':v},actor='JARVIS-engine')
   # A zero process exit alone never closes a correction cycle; accept does.
  result={'reference':int(ref),'decision':decision,'executor':host,'test_executed':kind=='test' and not test_infrastructure_error(observed['execution']),'execution':observed['execution'],'version':version(observed['after']),'files':observed['after'],'actual_changed_files':[f for f in set(observed['before'])|set(observed['after']) if observed['before'].get(f)!=observed['after'].get(f)],'reference_usage':'reference is the event ID for analyze, sync.source_reference and accept; version and file hashes are NOT event IDs','failed_cycles':v['failed_cycles'],'next':'analyze actual failure before correcting' if kind=='test' and observed['execution']['returncode'] else 'Qwen decides next action'}
  persistent.finish(attempt['attempt'],observed,result)
  state['operations'][key]['result']=result;self.save(state)
  return result
 def plan(self,a):
  history=self.store.plans(self.m)
  if history and 'expected_version' not in a:raise ValueError('Revising an existing plan requires expected_version='+str(history[-1]['version'])+' and reason. A correction/test/sync does NOT require replanning.')
  decision=self.decision(a);tasks=[]
  for step in a['steps']:
   if not re.fullmatch(r'[A-Za-z0-9_-]{1,40}',step['id']):raise ValueError('Invalid task id')
   for issue in step['issues']:
    if issue not in self.spec['authority_requirements']:raise ValueError('Unknown owner requirement id; allowed EXACT ids: '+str(self.spec['authority_requirements']))
   tasks.append({'id':step['id'],'title':step['title'],'objective':step['title'],'depends':step['depends'],'tools':TOOLS,'strict_tools':True,
    'contract':{'report_path':str(self.local/'reports'/self.m/(step['id']+'.md')),'checks':[{'tool':'authority_work','arguments':{'kind':'accept','issue':i},'ok':True} for i in step['issues']]}})
  covered={i for step in a['steps'] for i in step['issues']}
  if covered!=set(self.spec['authority_requirements']):raise ValueError('Coverage gap; model must cover '+str(self.spec['authority_requirements']))
  self.store.plan(self.m,tasks,author='JARVIS/Qwen80B@Dell1',metadata={'decision_event':decision},reason=a.get('reason','Model initial plan'),expected_version=a.get('expected_version'))
  return {'tasks':tasks,'version':len(self.store.plans(self.m)),'next':'Execute the ready task. Files, commands, tests and executors are your decisions.'}
 def sync(self,a):
  state=self.state();budget(state,a['issue']);decision=self.decision(a)
  src,dst=a['source'],a['destination']
  if src==dst:raise ValueError('Distinct source and destination required')
  files=a['files']
  if not files or any(Path(f).is_absolute() or '..' in Path(f).parts or not re.fullmatch(r'[\w./-]+',f) for f in files):raise ValueError('Safe relative explicit file list required')
  # Version precondition chosen by model; no implicit merge or silent overwrite.
  ref=state['executions'].get(str(a['source_reference']))
  if not ref or ref['host']!=src:raise ValueError('source_reference requires the numeric execution reference returned by authority_work, NOT a file/version SHA. Observed source candidates: '+str([{'reference':key,'kind':row['kind'],'host':row['host']} for key,row in state['executions'].items() if row['host']==src][-3:]))
  before,_=self.remote(src,'python3 -c '+shlex.quote(runner_program('true',self.spec.get('authority_manifest_roots'))))
  if json.loads(before['stdout'])['after']!=ref['after']:raise ValueError('Source changed; inspect and choose the current source reference')
  import zipfile
  # Archive content is selected by Qwen. Existing SHA-checked broker transports bytes.
  cmd="python3 -c "+shlex.quote("import zipfile;z=zipfile.ZipFile('_authority.zip','w');[z.write(f,f) for f in "+repr(files)+"];z.close()")
  self.remote(src,cmd)
  local=self.local/('transfer-'+self.m+'.zip')
  for host,action in [(src,'project_download'),(dst,'project_upload')]:
   args={'host':HOSTS[host],'action':action,'project':self.project,'path':self.remote_root+'/_authority.zip','local_path':str(local)}
   token=self.store.begin_call(self.m,self.t,'host_remote',args);start=time.monotonic();r=self.reg.execute('host_remote',args);self.store.finish_call(token,r,time.monotonic()-start)
   if not r.get('ok'):raise RuntimeError(str(r)[:1000])
  check,_=self.remote(dst,"python3 -c "+shlex.quote("import zipfile;z=zipfile.ZipFile('_authority.zip');assert all(not p.startswith('/') and '..' not in p.split('/') for p in z.namelist());z.extractall('.')"))
  after,_=self.remote(dst,'python3 -c '+shlex.quote(runner_program('true',self.spec.get('authority_manifest_roots'))))
  manifest=json.loads(after['stdout'])['after']
  if any(manifest.get(f)!=ref['after'].get(f) for f in files):raise ValueError('Transferred file hash mismatch')
  receipt={'decision':decision,'source':src,'destination':dst,'files':files,'source_reference':a['source_reference'],'version':version(manifest),'exact_workspace':manifest==ref['after']}
  state['syncs'].append(receipt);self.save(state);self.event('authority_synchronized',receipt)
  return receipt
 def finish(self,a):
  task=next(t for t in self.store.tasks(self.m) if t['id']==self.t)
  state=self.state()
  issues=[c['arguments']['issue'] for c in task['contract']['checks']]
  if any(not state['issues'].get(i,{}).get('accepted') for i in issues):raise ValueError('Actual independent acceptance required before task report')
  path=task['contract']['report_path']
  args={'path':path,'content':a['report']};token=self.store.begin_call(self.m,self.t,'host_write_file',args);start=time.monotonic();r=self.reg.execute('host_write_file',args);self.store.finish_call(token,r,time.monotonic()-start)
  if not r.get('ok'):raise ValueError(str(r))
  observations=self.store.observations(self.m,self.t)
  evidence=next(o['id'] for o in reversed(observations) if o['tool']=='authority_work' and o['arguments'].get('kind')=='accept' and (o['result'] or {}).get('ok'))
  return self.reg.execute('mission_task_complete',{'id':self.t,'report_path':path,'evidence_id':evidence})['result']

def register(reg):
 def add(name,description,props,required,method):
  reg.specs[name]=(description,props,required,'host_authorized',lambda a:getattr(Authority(reg),method)(a))
 text={'type':'string','maxLength':12000}
 reference={'type':'integer','minimum':1,'description':'Actual numeric execution event ID returned as reference, never a file hash or version SHA.'}
 issue={'type':'string','enum':['Q1','Q2'],'description':'EXACT stable owner criterion id; never rename or invent ids.'}
 add('authority_resources','Observe current resources of BOTH Dell executors through existing broker. You choose placement; this tool never assigns work.',{},[],'resources')
 add('authority_plan','Save YOUR plan: 1 to 5 reception work packages, not separate inspect/test/report actions. Each package covers one or more owner issues through correction AND independent validation. issues must use exact owner_requirement_ids. You MAY inspect before planning. Commands, files and host selection remain YOUR decisions.',{'steps':{'type':'array','minItems':1,'maxItems':5,'items':{'type':'object','required':['id','title','depends','issues'],'properties':{'id':text,'title':text,'depends':{'type':'array','items':text},'issues':{'type':'array','minItems':1,'items':issue}},'additionalProperties':False}},'expected_version':{'type':'integer'},'reason':text},['steps'],'plan')
 initial=reg.specs['authority_plan']
 reg.specs['authority_revise_plan']=('GLOBAL plan revision ONLY when dependencies or owner coverage genuinely change. Not for recording analysis or a new command: use authority_work/analyze. Supply ALL work packages covering ALL owner criteria and expected_version=current plan_version. Received tasks immutable.',initial[1],['steps','expected_version','reason'],initial[3],initial[4])
 add('authority_work','YOUR decision then actual Dell execution. inspect/correct/test: choose executor, command, summary. analyze: reference actual failed test + summary/hypothesis. accept: reference passed test and source_reference correction on OTHER host at EXACT manifest. Commands run in the mission-declared authorized project root. Counts persist per issue. Outputs include execution returncode distinct from tool transport success.',{'issue':issue,'kind':{'type':'string','enum':['inspect','correct','test','analyze','accept']},'summary':text,'operation_id':text,'executor':{'type':'string','enum':list(HOSTS)},'command':text,'reference':reference,'source_reference':reference},['issue','kind','summary','operation_id'],'work')
 add('authority_read_execution','Read actual stdout/stderr of an execution in THIS mission, using its numeric execution reference. Not a UUID, receipt filename, model decision or broker id. Reads complete SHA-checked receipt when available; select line window to avoid repeated full-file excerpts.',{'reference':reference,'stream':{'type':'string','enum':['stdout','stderr']},'start_line':{'type':'integer','minimum':1},'max_lines':{'type':'integer','minimum':1,'maximum':80}},['reference'],'read_execution')
 add('authority_analyze','Record YOUR technical diagnosis of the latest observed failed test for this issue. The engine attaches its exact existing execution reference automatically. No command is run. Use before the next correction; do not send a shell command or guess an event number.',{'issue':issue,'summary':text},['issue','summary'],'analyze_latest')
 add('authority_edit','Apply YOUR literal source edits on a chosen Dell, with real before/after receipts. File contents are data, not a shell script. Existing file: old must match exactly once; new replaces it. New file: old=null, new is complete file content, target must not exist. No tests are implicitly run. Same correction counters and idempotency as authority_work. Never recopy a whole existing class to replace the application.',{'issue':issue,'executor':{'type':'string','enum':list(HOSTS)},'summary':text,'operation_id':text,'edits':{'type':'array','minItems':1,'maxItems':8,'items':{'type':'object','required':['path','old','new'],'properties':{'path':{'type':'string','minLength':1},'old':{'type':['string','null']},'new':{'type':'string'}},'additionalProperties':False}}},['issue','executor','summary','operation_id','edits'],'edit')
 add('authority_sync','YOUR explicit one-way synchronization strategy. Choose files, source, destination and source_reference latest observed source execution. SHA checked; no implicit merge. Include tests so peer validates exact version.',{'issue':issue,'source':{'type':'string','enum':list(HOSTS)},'destination':{'type':'string','enum':list(HOSTS)},'files':{'type':'array','items':text},'source_reference':reference,'summary':text},['issue','source','destination','files','source_reference','summary'],'sync')
 add('authority_finish','Write your concise factual task report to its canonical path and request existing task completion gates. Cite actual event references, failures, attribution. No application modification on Mac.',{'report':text},['report'],'finish')


def interface_failure(store, mission, task, name, error):
 """Also bound format/delegation refusals which occur before a tool body runs."""
 spec=json.loads(store.get(mission)['spec']);epoch=spec.get('authority_interface_epoch','initial')
 category=name+':'+ ('schema' if str(error).startswith('Schema ') else str(error).split(':')[0][:100])
 if hasattr(store,'db'):
  with store.db() as c:prior=c.execute("SELECT id FROM mission_events WHERE mission=? AND kind='authority_interface_failure' AND json_extract(result,'$.epoch')=? AND json_extract(result,'$.category')=?",(mission,epoch,category)).fetchall()
 else:prior=[e for e in store.events(mission,limit=100000) if e['kind']=='authority_interface_failure' and e['result'].get('epoch')==epoch and e['result'].get('category')==category]
 count=len(prior)+1
 store.event(mission,'authority_interface_failure',task,'JARVIS-engine',result={'epoch':epoch,'category':category,'count':count,'error':str(error)[:1500]})
 if count>=3:
  store.event(mission,'authority_escalation',task,'JARVIS-engine',result={'reason':'Three comparable interface/delegation refusals','category':category,'count':count,'epoch':epoch})
  return True
 return False


def working_state(state):
 """Resolved incidents stay in the immutable journal, not as current work."""
 view={**state,'issues':{},'executions':{}}
 for issue,value in state.get('issues',{}).items():
  current=dict(value);resolved=value.get('correction_resolution_event',0)
  old_analysis=value.get('analyzed')
  for field in ('last_failed_test','last_test','analyzed','pending_correction'):
   reference=value.get(field)
   if resolved and str(reference).isdigit() and int(reference)<resolved:current.pop(field,None)
  if resolved and str(old_analysis).isdigit() and int(old_analysis)<resolved:current.pop('analysis',None)
  if resolved:current['resolved_history']={'resolution_event':resolved,'failed_cycles_retained':value['failed_cycles'],'new_segment_failed_cycles':value['failed_cycles']-value.get('correction_resolved_through',0),'archived_incidents':'mission_evidence; no replay of resolved failures'}
  view['issues'][issue]=current
 for reference,execution in state.get('executions',{}).items():
  resolved=state.get('issues',{}).get(execution.get('issue'),{}).get('correction_resolution_event',0)
  if not resolved or int(reference)>resolved:view['executions'][reference]=execution
 return view

def model_view(value):
 """Keep actionable execution references; audit-only ids remain in SQLite."""
 if isinstance(value,list):return [model_view(v) for v in value]
 if not isinstance(value,dict):return value
 return {k:({'manifest_sha256':version(v),'file_paths':list(v),'full_manifest':'Original durable execution receipt'} if k in ('files','before','after') and isinstance(v,dict) and all(isinstance(x,str) and re.fullmatch(r'[0-9a-f]{64}',x) for x in v.values()) else int(v) if k in ('reference','source_reference') and isinstance(v,str) and v.isdigit() else model_view(v)) for k,v in value.items() if k not in ('decision','broker_invocation','inference_event')}

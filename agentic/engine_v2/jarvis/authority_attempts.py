"""Bridge historical Authority receipts to the single canonical AttemptLedger.

No application command/test selection. Qwen still chooses both and the executor.
"""
import json
from .attempt_ledger import digest

def test_infrastructure_error(execution):
 text=str(execution.get('stderr',''))
 return execution.get('returncode') in (126,127) or any(k in text for k in ('ModuleNotFoundError:','FileNotFoundError:','command not found'))

class AuthorityAttempts:
 def __init__(self,authority):
  self.a=authority;self.s=authority.store;self.m=authority.m;self.ledger=self.s.attempt_ledger(self.m)
 def begin(self,args,state):
  kind=args['kind'];issue=args['issue']
  scope='authority:'+issue if kind=='correct' else 'authority-observation:'+issue+':'+kind+':'+digest(args['command'])
  descriptor={'issue':issue,'project':self.a.project,'kind':'correction-cycle' if kind=='correct' else kind}
  problem=self.ledger.problem(scope,descriptor)
  # Observe source version before lookup, so a cached test can never receive a
  # different version edited by another actor since its original execution.
  from .distributed_authority import runner_program
  raw,_=self.a.remote(args['executor'],'python3 -c '+__import__('shlex').quote(runner_program('true',self.a.spec.get('authority_manifest_roots'))))
  current=json.loads(raw['stdout'])['after']
  request={'command':args['command'],'kind':kind,'source_manifest':current}
  if self.a.spec.get('authority_engine_operation_ids'):
   # A completed-task receipt must never masquerade as this task's execution.
   # Same-task repeats still deduplicate; issue failure counters stay shared.
   request['task']=self.a.t
  result=self.ledger.begin(problem,args['operation_id'],args['executor'],'correction_test' if kind=='correct' else 'test' if kind=='test' else 'execute',request)
  if result.get('blocked') or result.get('requires_observation'):raise ValueError('P2 persistent authority guard; original action not dispatched: '+json.dumps(result))
  if result.get('cached'):
   value=self.ledger.get(result['attempt'])['result']['value']
   return {'cached':True,'value':{**value,'cached':True,'original_reference':value['reference']} if self.a.spec.get('authority_engine_operation_ids') else value}
  self.ledger.transition(result['attempt'],'DISPATCHED');return result
 def uncertain(self,attempt,error):
  evidence=self.s.event(self.m,'p2_dispatch_failure_observed',actor='JARVIS-engine',result={'attempt':attempt,'known_not_executed':False,'error':str(error),'legacy_path':'Authority.work'})
  self.ledger.transition(attempt,'VALIDATION_INCONCLUSIVE',evidence=evidence,result={'error':str(error)},unknown=True);self.ledger.failure(attempt,infrastructure=True)
 def finish(self,attempt,observed,value):
  row=self.ledger.get(attempt);execution=observed['execution'];code=execution['returncode'];changed=observed['before']!=observed['after'];kind=observed['kind']
  marker={'child_started':True,'basis':'actual completed child in SHA-checked historical receipt','broker_invocation':observed['broker_invocation']}
  evidence=self.s.event(self.m,'p2_started_observed',actor='JARVIS-engine',result={'attempt':attempt,'marker':marker})
  self.ledger.transition(attempt,'RUNNING',evidence=evidence)
  infrastructure=test_infrastructure_error(execution)
  passed=code==0 and not changed and kind in ('inspect','test')
  result={'value':value,'returncode':code,'execution':execution,'started':marker,'verified':passed,'source_manifest':observed['after'],'source_changed':changed,'verification_scope':'read-only inspection or passed process test on stable source; not application acceptance'}
  target='SUCCESS' if passed else 'EXECUTED_TEST_FAILED' if code and kind=='test' and not infrastructure else 'EXECUTION_FAILED' if code else 'EXECUTED_TEST_FAILED' if changed and kind=='inspect' else 'VALIDATION_INCONCLUSIVE'
  evidence=self.s.event(self.m,'p2_result_observed',actor='JARVIS-engine',result={'attempt':attempt,'observation':result,'state':target,'legacy_execution_reference':value['reference']})
  self.ledger.transition(attempt,target,evidence=evidence,result=result,unknown=False)
  if code and kind=='correct':self.ledger.failure(attempt,correction_changed=changed)
  if kind=='test' and code and infrastructure:self.ledger.failure(attempt,correction_changed=False)
  if kind=='test' and code and not infrastructure:
   snapshot=self.ledger.snapshot();problem=self.ledger.problem('authority:'+observed['issue'],{'issue':observed['issue'],'project':self.a.project,'kind':'correction-cycle'})
   for raw in snapshot['attempts']:
    if raw['problem']!=problem or raw['state']!='VALIDATION_INCONCLUSIVE' or raw['unknown_outcome']:continue
    prior=self.ledger.get(raw['id']);r=prior['result']
    if r.get('source_manifest')!=observed['after']:continue
    failed={**r,'verified':False,'failed_test_reference':value['reference'],'test_execution':execution}
    proof=self.s.event(self.m,'p2_result_observed',actor='JARVIS-engine',result={'attempt':raw['id'],'observation':failed,'state':'EXECUTED_TEST_FAILED'})
    self.ledger.transition(raw['id'],'EXECUTED_TEST_FAILED',evidence=proof,result=failed,unknown=False);self.ledger.failure(raw['id'],correction_changed=r['source_changed'])
 def accepted(self,issue,source_reference,acceptance):
  for raw in self.ledger.snapshot()['attempts']:
   if raw['state']!='VALIDATION_INCONCLUSIVE' or raw['unknown_outcome']:continue
   row=self.ledger.get(raw['id']);r=row['result']
   if r.get('value',{}).get('reference')!=int(source_reference):continue
   result={**r,'verified':True,'independent_acceptance':acceptance}
   proof=self.s.event(self.m,'p2_result_observed',actor='JARVIS-engine',result={'attempt':raw['id'],'observation':result,'state':'SUCCESS'})
   self.ledger.transition(raw['id'],'SUCCESS',evidence=proof,result=result,unknown=False)

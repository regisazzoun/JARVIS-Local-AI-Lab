"""Persistent attempt states in the canonical MissionStore SQLite; no second engine."""
import hashlib,json,time,uuid

STATES={'PENDING','DISPATCHED','RUNNING','NOT_EXECUTED','EXECUTION_FAILED','EXECUTED_TEST_FAILED','VALIDATION_INCONCLUSIVE','SUCCESS','BLOCKED','ESCALATED'}
TRANSITIONS={
 'PENDING':{'DISPATCHED','NOT_EXECUTED','BLOCKED'},
 'DISPATCHED':{'RUNNING','NOT_EXECUTED','VALIDATION_INCONCLUSIVE'},
 'RUNNING':{'EXECUTION_FAILED','EXECUTED_TEST_FAILED','VALIDATION_INCONCLUSIVE','SUCCESS'},
 'VALIDATION_INCONCLUSIVE':{'NOT_EXECUTED','RUNNING','EXECUTION_FAILED','EXECUTED_TEST_FAILED','SUCCESS','BLOCKED'},
 'NOT_EXECUTED':{'DISPATCHED','BLOCKED'},'EXECUTION_FAILED':{'BLOCKED'},'EXECUTED_TEST_FAILED':{'BLOCKED'},'BLOCKED':{'ESCALATED'}}
def encoded(value):return json.dumps(value,sort_keys=True,ensure_ascii=False)
def digest(value):return hashlib.sha256(encoded(value).encode()).hexdigest()
class AttemptLedger:
 def __init__(self,store,mission):
  self.store=store;self.m=mission;store.get(mission)
  with store.db() as c:
   c.executescript('''CREATE TABLE IF NOT EXISTS mission_problems_v2(
    mission TEXT NOT NULL,scope TEXT NOT NULL,fingerprint TEXT NOT NULL,descriptor TEXT NOT NULL,
    failed_cycles INTEGER NOT NULL DEFAULT 0,infra_incidents INTEGER NOT NULL DEFAULT 0,
    state TEXT NOT NULL DEFAULT 'OPEN',escalation_event INTEGER,
    PRIMARY KEY(mission,fingerprint),UNIQUE(mission,scope));
   CREATE TABLE IF NOT EXISTS mission_attempts_v2(
    id TEXT PRIMARY KEY,mission TEXT NOT NULL,problem TEXT NOT NULL,operation_key TEXT NOT NULL,
    signature TEXT NOT NULL,executor TEXT NOT NULL,phase TEXT NOT NULL,request TEXT NOT NULL,
    state TEXT NOT NULL,unknown_outcome INTEGER NOT NULL DEFAULT 0,result TEXT NOT NULL DEFAULT '{}',
    created REAL NOT NULL,updated REAL NOT NULL,
    UNIQUE(mission,problem,operation_key),UNIQUE(mission,problem,signature));''')
   if 'infra_resolved_through' not in {r['name'] for r in c.execute('PRAGMA table_info(mission_problems_v2)')}:
    c.execute('ALTER TABLE mission_problems_v2 ADD COLUMN infra_resolved_through INTEGER NOT NULL DEFAULT 0')
   if 'misclassified_failed_cycles' not in {r['name'] for r in c.execute('PRAGMA table_info(mission_problems_v2)')}:
    c.execute('ALTER TABLE mission_problems_v2 ADD COLUMN misclassified_failed_cycles INTEGER NOT NULL DEFAULT 0')
   if 'correction_resolved_through' not in {r['name'] for r in c.execute('PRAGMA table_info(mission_problems_v2)')}:
    c.execute('ALTER TABLE mission_problems_v2 ADD COLUMN correction_resolved_through INTEGER NOT NULL DEFAULT 0')
 def rectify_report_success(self,attempt,verification):
  """Coordinator reopening of a proved false PASS, with append-only erratum.

  Same report bytes and exact task criterion are required. The old PASS and
  original attempt result remain available; a real failed correction is counted.
  This method is not exposed as a model tool and never resets a failure budget.
  """
  if self.store.get(self.m)['state']!='interrupted':raise ValueError('Report rectification requires interrupted execution')
  with self.store.db() as c:
   prior=c.execute("SELECT id FROM mission_events WHERE mission=? AND kind='coordinator_report_success_rectified' AND json_extract(result,'$.attempt')=?",(self.m,attempt)).fetchone()
  if prior:
   row=self.get(attempt)
   if row['state']=='EXECUTED_TEST_FAILED':self.failure(attempt,correction_changed=bool(row['result'].get('change_observed')))
   return {'event':prior['id'],'cached':True}
  with self.store.db() as c:
   c.execute('BEGIN IMMEDIATE')
   row=c.execute('SELECT * FROM mission_attempts_v2 WHERE mission=? AND id=?',(self.m,attempt)).fetchone()
   prior=c.execute("SELECT id FROM mission_events WHERE mission=? AND kind='coordinator_report_success_rectified' AND json_extract(result,'$.attempt')=?",(self.m,attempt)).fetchone()
   if prior:raise ValueError('Concurrent rectification recorded; retry coordinator reconciliation without executing any operation')
   proof=c.execute("SELECT * FROM mission_events WHERE mission=? AND id=? AND kind='semantic_verification'",(self.m,verification)).fetchone()
   if not row or not proof:raise ValueError('Original attempt or fresh verification absent')
   request=json.loads(row['request']);old=json.loads(row['result']);verdict=json.loads(proof['result'])
   previous=old.get('verification',{})
   if not previous and old.get('verification_events'):
    original=c.execute("SELECT id,result FROM mission_events WHERE mission=? AND id=? AND kind='semantic_verification'",(self.m,old['verification_events'][-1])).fetchone()
    if original:previous={**json.loads(original['result']),'verification_event':original['id']}
   args=request.get('arguments',{})
   task=next((t for t in self.store.tasks(self.m) if t['id']==request.get('task')),None)
   if row['state']!='SUCCESS' or row['unknown_outcome'] or request.get('tool')!='host_write_file' or previous.get('status')!='PASS':raise ValueError('Known report write with original PASS required')
   if not task or proof['task']!=task['id'] or verdict.get('contract') not in task['contract'].get('semantic',[]) or verdict.get('contract',{}).get('kind')!='report':raise ValueError('Exact report task criterion required')
   expected=hashlib.sha256(args.get('content','').encode()).hexdigest()
   if args.get('path')!=task['contract'].get('report_path') or previous.get('sha256')!=expected or verdict.get('sha256')!=expected or verdict.get('status')!='FAIL' or not verdict.get('observations') or proof['id']<=previous.get('verification_event',0):raise ValueError('Fresh FAIL must contradict PASS on identical observed report bytes')
   verdict={**verdict,'verification_event':verification}
   result={**old,'original_success_result':old,'verification':verdict,'verified':False,'failure_counted':False,'rectification_verification':verification}
   c.execute("UPDATE mission_attempts_v2 SET state='EXECUTED_TEST_FAILED',result=?,updated=? WHERE id=?",(encoded(result),time.time(),attempt))
   c.execute("UPDATE tasks SET state='running',last_error=?,updated=? WHERE mission=? AND id=?",('Original report PASS contradicted by fresh evidence; correction required',time.time(),self.m,task['id']))
   event=self.store.event(self.m,'coordinator_report_success_rectified',task['id'],'Codex',result={'attempt':attempt,'original_verification':previous.get('verification_event'),'new_verification':verification,'sha256':expected,'old_state':'SUCCESS','new_state':'EXECUTED_TEST_FAILED','original_events_preserved':True,'counter_reset':False},connection=c)
  self.failure(attempt,correction_changed=bool(old.get('change_observed')))
  return {'event':event,'cached':False}
 def resolve_report_interface(self,problem,evidence):
  """Coordinator-only new report strategy after a verified interface repair.

  Historical failed totals/attempts remain immutable. This does not receive a
  report or permit changing application predicates. Three new failures stop.
  """
  from pathlib import Path
  if self.store.get(self.m)['state']!='interrupted':raise ValueError('Report recovery requires interrupted execution')
  allowed={'mission_reporting.py','mission_assurance.py','durable_cycle.py','mission_context_budget.py','operational_policy.py','report_claims.py'}
  with self.store.db() as c:
   c.execute('BEGIN IMMEDIATE')
   proof=c.execute('SELECT id,actor,kind,result FROM mission_events WHERE mission=? AND id=?',(self.m,evidence)).fetchone()
   if not proof or proof['actor']!='Codex' or proof['kind']!='coordinator_report_interface_verified':raise ValueError('Explicit coordinator report-interface verification required')
   data=json.loads(proof['result']);refs=data.get('evidence_events',[])
   if data.get('problem')!=problem or data.get('verified') is not True or not refs:raise ValueError('Verification must bind the exact report problem and evidence')
   if any(type(ref) is not int or ref>=evidence or not c.execute('SELECT id FROM mission_events WHERE mission=? AND id=?',(self.m,ref)).fetchone() for ref in refs):raise ValueError('Original verification evidence missing')
   before=c.execute('SELECT actor,result FROM mission_events WHERE mission=? AND id=? AND id<?',(self.m,data.get('previous_verification'),evidence)).fetchone()
   manifest=data.get('deployed_manifest') or {};old=json.loads(before['result']).get('deployed_manifest',{}) if before and before['actor']=='Codex' else {}
   if not manifest or not old or not any(name in old and old[name]!=value for name,value in manifest.items()):raise ValueError('An actual changed report interface is required, not a renamed retry')
   base=(self.store.root/'jarvis').resolve()
   for name,value in manifest.items():
    path=(base/name).resolve()
    if name not in allowed or not path.is_relative_to(base) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=value:raise ValueError('Deployed report interface hash mismatch')
   previous_resolution=c.execute("SELECT id FROM mission_events WHERE mission=? AND kind='p2_report_interface_resolution' AND json_extract(result,'$.problem')=? ORDER BY id DESC LIMIT 1",(self.m,problem)).fetchone()
   if previous_resolution and data.get('previous_verification',0)<=previous_resolution['id']:raise ValueError('The before-repair proof predates the previous recovery; a new actual repair is required')
   p=c.execute('SELECT * FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(self.m,problem)).fetchone()
   if p and p['escalation_event'] and proof['id']<=p['escalation_event']:raise ValueError('Repair proof predates the latest escalation')
   criteria=json.loads(p['descriptor']).get('criteria',[]) if p else []
   if not p or p['state'] not in ('BLOCKED','ESCALATED') or p['failed_cycles']-p['correction_resolved_through']<3 or not criteria or any(x.get('kind')!='report' for x in criteria):raise ValueError('Only an escalated report-validation problem may use this recovery')
   if c.execute("SELECT id FROM mission_attempts_v2 WHERE mission=? AND problem=? AND (unknown_outcome=1 OR state IN ('PENDING','DISPATCHED','RUNNING') OR (state='VALIDATION_INCONCLUSIVE' AND coalesce(json_extract(result,'$.verification_not_executed'),0)!=1))",(self.m,problem)).fetchone():raise ValueError('Observe pending or unknown effects before recovery')
   c.execute("UPDATE mission_problems_v2 SET correction_resolved_through=failed_cycles,state='RESOLVED' WHERE mission=? AND fingerprint=?",(self.m,problem))
   return self.store.event(self.m,'p2_report_interface_resolution',actor='JARVIS-engine',result={'problem':problem,'verification_event':evidence,'failed_cycles':p['failed_cycles'],'correction_resolved_through':p['failed_cycles'],'active_failed_cycles':0,'old_attempts_and_totals_unchanged':True,'report_received':False},connection=c)
 def reclassify_unloaded_test(self,reference,evidence):
  """Rectify proved loader failures, retaining raw totals and original events.

  This is a coordinator audit, never an agent retry/reset operation.
  """
  if self.store.get(self.m)['state']!='interrupted':raise ValueError('Classification audit requires interrupted execution')
  from .authority_attempts import test_not_loaded
  with self.store.db() as c:
   c.execute('BEGIN IMMEDIATE')
   proof=c.execute('SELECT actor,kind,result FROM mission_events WHERE mission=? AND id=?',(self.m,evidence)).fetchone()
   if not proof or proof['actor'] not in ('Codex','Codex-periodic') or proof['kind']!='coordinator_test_loading_failure_verified':raise ValueError('Explicit coordinator loader-failure verification required')
   data=json.loads(proof['result'])
   if data.get('test_reference')!=reference or data.get('verified') is not True:raise ValueError('Verification must bind the exact test execution')
   event=c.execute("SELECT result FROM mission_events WHERE mission=? AND id=? AND kind='authority_execution'",(self.m,reference)).fetchone()
   if not event:raise ValueError('Native test execution absent')
   observation=json.loads(event['result']);execution=observation.get('execution',{})
   if observation.get('kind')!='test' or observation.get('before')!=observation.get('after') or execution.get('returncode')==0 or execution.get('output_truncated') or execution.get('stdout_model_excerpt') or execution.get('stderr_model_excerpt') or not test_not_loaded(execution):raise ValueError('Complete native evidence does not prove a pure loader failure')
   prior=c.execute("SELECT id,result FROM mission_events WHERE mission=? AND kind='p2_test_classification_corrected' AND json_extract(result,'$.test_reference')=?",(self.m,reference)).fetchone()
   if prior:return {**json.loads(prior['result']),'event':prior['id'],'cached':True}
   corrections=[]
   for row in c.execute('SELECT * FROM mission_attempts_v2 WHERE mission=?',(self.m,)).fetchall():
    result=json.loads(row['result']);related=str(result.get('failed_test_reference',''))==str(reference)
    own=str(result.get('value',{}).get('reference',''))==str(reference)
    if related:
     counted=c.execute("SELECT id FROM mission_events WHERE mission=? AND kind='p2_problem_counter' AND json_extract(result,'$.attempt')=? AND json_extract(result,'$.counter')='failed_cycles'",(self.m,row['id'])).fetchone()
     if not counted or not result.get('failure_counted'):raise ValueError('Counted functional failure not established')
     problem=c.execute('SELECT * FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(self.m,row['problem'])).fetchone()
     if problem['failed_cycles']<1:raise ValueError('Qualified counter cannot become negative')
     c.execute('UPDATE mission_problems_v2 SET failed_cycles=failed_cycles-1,misclassified_failed_cycles=misclassified_failed_cycles+1,infra_incidents=infra_incidents+1 WHERE mission=? AND fingerprint=?',(self.m,row['problem']))
     corrections.append({'attempt':row['id'],'problem':row['problem'],'old_qualified_failed_cycles':problem['failed_cycles'],'new_qualified_failed_cycles':problem['failed_cycles']-1,'historical_total_preserved':problem['failed_cycles']+problem['misclassified_failed_cycles']})
     result.update(verification_not_executed=True,failure_counted=False,misclassified_failure_verification=evidence)
     c.execute("UPDATE mission_attempts_v2 SET state='VALIDATION_INCONCLUSIVE',unknown_outcome=0,result=?,updated=? WHERE id=?",(encoded(result),time.time(),row['id']))
    elif own:
     result.update(verification_not_executed=True,classification_verification=evidence)
     if isinstance(result.get('value'),dict):result['value']={**result['value'],'test_executed':False,'classification_verification':evidence}
     c.execute("UPDATE mission_attempts_v2 SET state='EXECUTION_FAILED',result=?,updated=? WHERE id=?",(encoded(result),time.time(),row['id']))
   for problem in {row['problem'] for row in corrections}:
    c.execute("UPDATE mission_problems_v2 SET state='OPEN' WHERE mission=? AND fingerprint=? AND failed_cycles-correction_resolved_through<3 AND infra_incidents-infra_resolved_through<3 AND state IN ('BLOCKED','ESCALATED')",(self.m,problem))
   result={'test_reference':reference,'verification_event':evidence,'test_execution_status':'NOT_EXECUTED','command_executed':True,'corrections':corrections,'original_events_preserved':True,'not_a_counter_reset':True}
   result['event']=self.store.event(self.m,'p2_test_classification_corrected',actor='Codex',result=result,connection=c)
   return result
 def resolve_infrastructure(self,problem,evidence):
  """Acknowledge verified infrastructure repair; never erase failures or unknown effects."""
  with self.store.db() as c:
   c.execute('BEGIN IMMEDIATE')
   proof=c.execute('SELECT actor,kind,result FROM mission_events WHERE mission=? AND id=?',(self.m,evidence)).fetchone()
   if not proof or proof['actor'] not in ('Codex','Codex-periodic') or proof['kind']!='coordinator_infrastructure_verified':raise ValueError('Infrastructure resolution needs an explicit coordinator verification event')
   data=json.loads(proof['result']);refs=data.get('evidence_events',[])
   if data.get('problem')!=problem or data.get('verified') is not True or not refs:raise ValueError('Verified repair must bind this exact problem and its evidence')
   for ref in refs:
    if type(ref) is not int or ref==evidence or not c.execute('SELECT id FROM mission_events WHERE mission=? AND id=?',(self.m,ref)).fetchone():raise ValueError('Repair evidence absent from this mission')
   p=c.execute('SELECT * FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(self.m,problem)).fetchone()
   if not p or p['failed_cycles']-p['correction_resolved_through']>=3:raise ValueError('Three functional failures remain escalated; infrastructure repair cannot reset them')
   if c.execute("SELECT id FROM mission_attempts_v2 WHERE mission=? AND problem=? AND (unknown_outcome=1 OR state IN ('PENDING','DISPATCHED','RUNNING') OR (state='VALIDATION_INCONCLUSIVE' AND coalesce(json_extract(result,'$.verification_not_executed'),0)!=1))",(self.m,problem)).fetchone():raise ValueError('Observe pending or unknown effects before infrastructure resolution')
   c.execute("UPDATE mission_problems_v2 SET infra_resolved_through=infra_incidents,state='RESOLVED' WHERE mission=? AND fingerprint=?",(self.m,problem))
   return self.store.event(self.m,'p2_infrastructure_resolution',actor='JARVIS-engine',result={'problem':problem,'verification_event':evidence,'infra_incidents':p['infra_incidents'],'infra_resolved_through':p['infra_incidents'],'failed_cycles':p['failed_cycles'],'old_attempts_and_totals_unchanged':True},connection=c)
 def problem(self,scope,descriptor):
  fingerprint=digest({'mission':self.m,'scope':scope,'descriptor':descriptor})
  with self.store.db() as c:
   c.execute('BEGIN IMMEDIATE')
   row=c.execute('SELECT * FROM mission_problems_v2 WHERE mission=? AND scope=?',(self.m,scope)).fetchone()
   if row and row['fingerprint']!=fingerprint:raise ValueError('Owner problem contract immutable; aliases cannot change its identity')
   if not row:c.execute('INSERT INTO mission_problems_v2(mission,scope,fingerprint,descriptor) VALUES(?,?,?,?)',(self.m,scope,fingerprint,encoded(descriptor)))
  return fingerprint
 def begin(self,problem,key,executor,phase,request):
  signature=digest({'executor':executor,'phase':phase,'request':request})
  with self.store.db() as c:
   c.execute('BEGIN IMMEDIATE')
   p=c.execute('SELECT * FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(self.m,problem)).fetchone()
   if not p:raise ValueError('Problem not registered')
   same=c.execute('SELECT * FROM mission_attempts_v2 WHERE mission=? AND problem=? AND operation_key=?',(self.m,problem,key)).fetchone()
   if same and same['signature']!=signature:raise ValueError('Operation key conflicts with original request; nothing executed')
   if p['state'] in ('BLOCKED','ESCALATED'):
    event=self.store.event(self.m,'p2_attempt_rejected',actor='JARVIS-engine',result={'problem':problem,'operation_key':key,'reason':'three failed cycles/incidents; no autonomous fourth','failed_cycles':p['failed_cycles'],'infra_incidents':p['infra_incidents']},connection=c)
    return {'blocked':True,'state':p['state'],'event':event,'problem':problem}
   same=same or c.execute('SELECT * FROM mission_attempts_v2 WHERE mission=? AND problem=? AND signature=?',(self.m,problem,signature)).fetchone()
   pending=c.execute("SELECT * FROM mission_attempts_v2 WHERE mission=? AND problem=? AND (unknown_outcome=1 OR state IN ('PENDING','DISPATCHED','RUNNING') OR (state='VALIDATION_INCONCLUSIVE' AND coalesce(json_extract(result,'$.verification_not_executed'),0)!=1))",(self.m,problem)).fetchone()
   if pending:return {'requires_observation':True,'attempt':pending['id'],'state':pending['state'],'problem':problem}
   if same:
    repair=c.execute("SELECT id FROM mission_events WHERE mission=? AND kind='p2_infrastructure_resolution' AND json_extract(result,'$.problem')=? AND created>? ORDER BY id DESC LIMIT 1",(self.m,problem,same['updated'])).fetchone() if same['state']=='NOT_EXECUTED' and p['state']=='RESOLVED' else None
    if repair:return {'attempt':same['id'],'state':'NOT_EXECUTED','problem':problem,'verified_retry':repair['id']}
    return {'cached':True,'attempt':same['id'],'state':same['state'],'result':json.loads(same['result']),'problem':problem}
   ident=uuid.uuid4().hex;now=time.time()
   c.execute('INSERT INTO mission_attempts_v2(id,mission,problem,operation_key,signature,executor,phase,request,state,created,updated) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(ident,self.m,problem,key,signature,executor,phase,encoded(request),'PENDING',now,now))
   self.store.event(self.m,'p2_attempt_transition',actor='JARVIS-engine',result={'attempt':ident,'problem':problem,'from':None,'state':'PENDING','executor':executor},connection=c)
   return {'attempt':ident,'problem':problem,'state':'PENDING'}
 def get(self,attempt):
  with self.store.db() as c:row=c.execute('SELECT * FROM mission_attempts_v2 WHERE mission=? AND id=?',(self.m,attempt)).fetchone()
  if not row:raise ValueError('Attempt absent from this mission')
  result=dict(row);result['request']=json.loads(result['request']);result['result']=json.loads(result['result']);return result
 def transition(self,attempt,state,evidence=None,result=None,unknown=None):
  if state not in STATES:raise ValueError('Unknown attempt state')
  with self.store.db() as c:
   c.execute('BEGIN IMMEDIATE');row=c.execute('SELECT * FROM mission_attempts_v2 WHERE mission=? AND id=?',(self.m,attempt)).fetchone()
   if not row or state not in TRANSITIONS.get(row['state'],set()):raise ValueError('Illegal attempt transition '+str(row['state'] if row else None)+' -> '+state)
   if row['state']=='NOT_EXECUTED' and state=='DISPATCHED':
    problem=c.execute('SELECT state,failed_cycles,correction_resolved_through,infra_incidents,infra_resolved_through FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(self.m,row['problem'])).fetchone()
    repair=c.execute("SELECT id FROM mission_events WHERE mission=? AND kind='p2_infrastructure_resolution' AND json_extract(result,'$.problem')=? AND created>? ORDER BY id DESC LIMIT 1",(self.m,row['problem'],row['updated'])).fetchone()
    if not repair or problem['state']!='RESOLVED' or problem['failed_cycles']-problem['correction_resolved_through']>=3 or problem['infra_incidents']-problem['infra_resolved_through']>=3:raise ValueError('Known non-execution retry requires a later verified infrastructure repair')
    result={'verified_retry':repair['id'],'previous_result':json.loads(row['result'])};unknown=False
   if state not in ('DISPATCHED','BLOCKED'):
    proof=c.execute('SELECT id,kind,result FROM mission_events WHERE mission=? AND id=?',(self.m,evidence)).fetchone()
    if not proof:raise ValueError('Observed state requires same-mission evidence event')
   if state not in ('DISPATCHED','BLOCKED'):
    observed=json.loads(proof['result'] or '{}')
    expected_kind={'RUNNING':'p2_started_observed','NOT_EXECUTED':'p2_dispatch_failure_observed','EXECUTION_FAILED':'p2_result_observed','EXECUTED_TEST_FAILED':'p2_result_observed','SUCCESS':'p2_result_observed','ESCALATED':'p2_escalation'}.get(state)
    if expected_kind and proof['kind']!=expected_kind:raise ValueError('Evidence is not an observation for this transition')
    if observed.get('attempt')!=attempt:raise ValueError('Evidence belongs to another attempt')
    if state=='RUNNING' and not observed.get('marker',{}).get('child_started'):raise ValueError('No observed child start')
    if state=='NOT_EXECUTED' and observed.get('known_not_executed') is not True:raise ValueError('Non-execution not established')
    if state=='VALIDATION_INCONCLUSIVE' and proof['kind'] not in ('p2_result_observed','p2_dispatch_failure_observed'):raise ValueError('Missing uncertainty observation')
    if state in ('SUCCESS','EXECUTION_FAILED','EXECUTED_TEST_FAILED') and observed.get('observation')!=result:raise ValueError('Result differs from original observed evidence')
   if state=='SUCCESS':
    if not result or result.get('returncode')!=0 or result.get('verified') is not True or not result.get('started'):
     raise ValueError('SUCCESS requires observed start, child0 and actual verification PASS')
   c.execute('UPDATE mission_attempts_v2 SET state=?,unknown_outcome=?,result=?,updated=? WHERE id=?',(state,row['unknown_outcome'] if unknown is None else int(unknown),encoded(result if result is not None else json.loads(row['result'])),time.time(),attempt))
   event=self.store.event(self.m,'p2_attempt_transition',actor='JARVIS-engine',result={'attempt':attempt,'problem':row['problem'],'from':row['state'],'state':state,'evidence':evidence,'unknown_outcome':unknown},connection=c)
   return event
 def failure(self,attempt,*,correction_changed=False,infrastructure=False):
  row=self.get(attempt)
  if row['result'].get('failure_counted'):return
  if infrastructure and row['state'] not in ('NOT_EXECUTED','VALIDATION_INCONCLUSIVE'):raise ValueError('No observed infrastructure failure')
  if not infrastructure and row['state'] not in ('EXECUTION_FAILED','EXECUTED_TEST_FAILED'):raise ValueError('No observed failed correction')
  escalate=None
  with self.store.db() as c:
   c.execute('BEGIN IMMEDIATE');result=json.loads(c.execute('SELECT result FROM mission_attempts_v2 WHERE id=?',(attempt,)).fetchone()['result'])
   if result.get('failure_counted'):return
   field='infra_incidents' if infrastructure or not correction_changed else 'failed_cycles'
   c.execute('UPDATE mission_problems_v2 SET '+field+'='+field+'+1 WHERE mission=? AND fingerprint=?',(self.m,row['problem']))
   result['failure_counted']=True;c.execute('UPDATE mission_attempts_v2 SET result=? WHERE id=?',(encoded(result),attempt))
   p=c.execute('SELECT * FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(self.m,row['problem'])).fetchone()
   self.store.event(self.m,'p2_problem_counter',actor='JARVIS-engine',result={'attempt':attempt,'problem':row['problem'],'counter':field,'failed_cycles':p['failed_cycles'],'active_failed_cycles':p['failed_cycles']-p['correction_resolved_through'],'infra_incidents':p['infra_incidents']},connection=c)
   if p['failed_cycles']-p['correction_resolved_through']>=3 or p['infra_incidents']-p['infra_resolved_through']>=3:
    c.execute("UPDATE mission_problems_v2 SET state='BLOCKED' WHERE mission=? AND fingerprint=?",(self.m,row['problem']))
    e=self.store.event(self.m,'p2_escalation',actor='JARVIS-engine',result={'problem':row['problem'],'attempt':attempt,'failed_cycles':p['failed_cycles'],'infra_incidents':p['infra_incidents'],'reason':'Three confirmed failures; no fourth autonomous correction','request_to':'Codex','evidence':result},connection=c)
    c.execute("UPDATE mission_problems_v2 SET state='ESCALATED',escalation_event=? WHERE mission=? AND fingerprint=?",(e,self.m,row['problem']))
    escalate=e
    self.store.event(self.m,'p2_problem_transition',actor='JARVIS-engine',result={'problem':row['problem'],'states':['BLOCKED','ESCALATED'],'evidence':e},connection=c)
  if escalate:
   self.transition(attempt,'BLOCKED',evidence=escalate)
   self.transition(attempt,'ESCALATED',evidence=escalate)
 def snapshot(self):
  with self.store.db() as c:
   problems=[dict(r) for r in c.execute('SELECT * FROM mission_problems_v2 WHERE mission=? ORDER BY scope',(self.m,))]
   attempts=[dict(r) for r in c.execute('SELECT * FROM mission_attempts_v2 WHERE mission=? ORDER BY created,id',(self.m,))]
  return {'mission':self.m,'problems':problems,'attempts':attempts}

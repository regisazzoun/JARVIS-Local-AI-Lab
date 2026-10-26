"""Persistent attempt states in the canonical MissionStore SQLite; no second engine."""
import hashlib,json,time,uuid

STATES={'PENDING','DISPATCHED','RUNNING','NOT_EXECUTED','EXECUTION_FAILED','EXECUTED_TEST_FAILED','VALIDATION_INCONCLUSIVE','SUCCESS','BLOCKED','ESCALATED'}
TRANSITIONS={
 'PENDING':{'DISPATCHED','NOT_EXECUTED','BLOCKED'},
 'DISPATCHED':{'RUNNING','NOT_EXECUTED','VALIDATION_INCONCLUSIVE'},
 'RUNNING':{'EXECUTION_FAILED','EXECUTED_TEST_FAILED','VALIDATION_INCONCLUSIVE','SUCCESS'},
 'VALIDATION_INCONCLUSIVE':{'RUNNING','EXECUTION_FAILED','EXECUTED_TEST_FAILED','SUCCESS','BLOCKED'},
 'EXECUTION_FAILED':{'BLOCKED'},'EXECUTED_TEST_FAILED':{'BLOCKED'},'BLOCKED':{'ESCALATED'}}
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
   pending=c.execute("SELECT * FROM mission_attempts_v2 WHERE mission=? AND problem=? AND (unknown_outcome=1 OR state IN ('PENDING','DISPATCHED','RUNNING','VALIDATION_INCONCLUSIVE'))",(self.m,problem)).fetchone()
   if pending:return {'requires_observation':True,'attempt':pending['id'],'state':pending['state'],'problem':problem}
   if same:return {'cached':True,'attempt':same['id'],'state':same['state'],'result':json.loads(same['result']),'problem':problem}
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
   self.store.event(self.m,'p2_problem_counter',actor='JARVIS-engine',result={'attempt':attempt,'problem':row['problem'],'counter':field,'failed_cycles':p['failed_cycles'],'infra_incidents':p['infra_incidents']},connection=c)
   if p['failed_cycles']>=3 or p['infra_incidents']>=3:
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

"""Bound historical worker exception retries in the same persistent ledger.
A pending tool call is an unknown effect, never an invitation to replay it.
"""
import json

def record_failure(store,row,error):
 mission=row['id'];cycle=row['attempts'];ledger=store.attempt_ledger(mission)
 scope='worker-recovery:'+type(error).__name__
 problem=ledger.problem(scope,{'component':'durable-worker','exception_type':type(error).__name__})
 with store.db() as c:
  c.execute('BEGIN IMMEDIATE')
  old=c.execute("SELECT result FROM mission_events WHERE mission=? AND kind='worker_recovery_recorded' AND json_extract(result,'$.cycle')=?",(mission,cycle)).fetchone()
  if old:return json.loads(old['result'])
  pending=[dict(r) for r in c.execute("SELECT id,tool,state FROM tool_calls WHERE mission=? AND state='started'",(mission,))]
  c.execute('UPDATE mission_problems_v2 SET infra_incidents=infra_incidents+1 WHERE mission=? AND fingerprint=?',(mission,problem))
  count=c.execute('SELECT infra_incidents FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(mission,problem)).fetchone()[0]
  result={'problem':problem,'cycle':cycle,'incident_count':count,'exception_type':type(error).__name__,'error':str(error),'unknown_effect_calls':pending,'stop':bool(pending) or count>=3,'test_failure_count':0,'meaning':'Worker exception, not a functional test verdict'}
  event=store.event(mission,'worker_recovery_recorded',actor='JARVIS-engine',result=result,connection=c)
  if result['stop']:
   escalation=store.event(mission,'p2_escalation',actor='JARVIS-engine',result={'problem':problem,'reason':'Unknown effect requires observation' if pending else 'Three comparable worker exceptions; no fourth automatic cycle','request_to':'Codex','worker_recovery_event':event,'infra_incidents':count},connection=c)
   c.execute("UPDATE mission_problems_v2 SET state='ESCALATED',escalation_event=? WHERE mission=? AND fingerprint=?",(escalation,mission,problem))
  return result


def blocked_problem(store,mission):
    with store.db() as c:
        row=c.execute("SELECT fingerprint,infra_incidents,escalation_event FROM mission_problems_v2 WHERE mission=? AND scope LIKE 'worker-recovery:%' AND state='ESCALATED' LIMIT 1",(mission,)).fetchone() if c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mission_problems_v2'").fetchone() else None
    return dict(row) if row else None

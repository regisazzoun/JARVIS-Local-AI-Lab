import unittest,tempfile
from jarvis.mission_store import MissionStore
from jarvis.worker_recovery import record_failure,blocked_problem
class RecoveryTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.s=MissionStore(self.temp.name);self.m=self.s.create('goal','model','conv')
 def tearDown(self):self.temp.cleanup()
 def test_third_exception_escalates_and_restart_keeps_count(self):
  for cycle in range(1,4):
   r=record_failure(self.s,{'id':self.m,'attempts':cycle},TimeoutError('same backend'))
   self.assertEqual(r['stop'],cycle==3)
  other=MissionStore(self.temp.name);r=record_failure(other,{'id':self.m,'attempts':3},TimeoutError('same backend'))
  self.assertIsNotNone(blocked_problem(other,self.m));self.assertEqual(r['incident_count'],3);self.assertEqual(len([e for e in other.events(self.m) if e['kind']=='worker_recovery_recorded']),3)
 def test_pending_tool_never_automatically_replays(self):
  token=self.s.begin_call(self.m,None,'host_remote',{'command':'possible-effect'})
  r=record_failure(self.s,{'id':self.m,'attempts':1},ConnectionError('reply unknown'))
  self.assertTrue(r['stop']);self.assertEqual(r['unknown_effect_calls'][0]['id'],token);self.assertEqual(r['test_failure_count'],0)
 def test_distinct_cycle_records_once(self):
  row={'id':self.m,'attempts':1}
  a=record_failure(self.s,row,RuntimeError('broken'));b=record_failure(self.s,row,RuntimeError('broken'))
  self.assertEqual(a['incident_count'],b['incident_count'])

 def test_verified_repair_keeps_totals_but_bounds_three_new_incidents(self):
  for cycle in range(1,4):last=record_failure(self.s,{'id':self.m,'attempts':cycle},TimeoutError('old'))
  p=last['problem'];ref=self.s.event(self.m,'repair_preflight',actor='Codex',result={'verified':True})
  proof=self.s.event(self.m,'coordinator_infrastructure_verified',actor='Codex',result={'problem':p,'verified':True,'evidence_events':[ref]})
  self.s.attempt_ledger(self.m).resolve_infrastructure(p,proof)
  for cycle in range(4,7):
   actual=record_failure(self.s,{'id':self.m,'attempts':cycle},TimeoutError('new'))
   self.assertEqual(actual['incident_count'],cycle)
   self.assertEqual(actual['active_incident_count'],cycle-3)
   self.assertEqual(actual['stop'],cycle==6)
  self.assertIsNotNone(blocked_problem(self.s,self.m))

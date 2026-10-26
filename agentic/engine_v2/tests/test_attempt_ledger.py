import tempfile, unittest, json
from pathlib import Path
from jarvis.mission_store import MissionStore
from jarvis.attempt_ledger import AttemptLedger,digest
class LedgerTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.store=MissionStore(self.root);self.m=self.store.create('test','model','conv');self.l=self.store.attempt_ledger(self.m);self.p=self.l.problem('component',{'criterion':'fixed'})
 def tearDown(self):self.temp.cleanup()
 def attempt(self,key='a',command='exit1'):
  return self.l.begin(self.p,key,'Dell1','correction_test',{'command':command})['attempt']
 def started(self,a):
  self.l.transition(a,'DISPATCHED');e=self.store.event(self.m,'p2_started_observed',result={'attempt':a,'marker':{'child_started':True}});self.l.transition(a,'RUNNING',evidence=e)
 def failed(self,a):
  result={'returncode':1,'started':{'child_started':True},'verified':False};e=self.store.event(self.m,'p2_result_observed',result={'attempt':a,'observation':result});self.l.transition(a,'EXECUTED_TEST_FAILED',evidence=e,result=result);self.l.failure(a,correction_changed=True)
 def test_counter_persists_and_renamed_fourth_operation_is_blocked(self):
  for n in range(3):
   a=self.attempt(str(n),'changed-'+str(n));self.started(a);self.failed(a)
  self.assertEqual(self.l.get(a)['state'],'ESCALATED')
  other=AttemptLedger(MissionStore(self.root),self.m);r=other.begin(self.p,'new-task-alias','Dell2','correction_test',{'command':'different-fourth'});self.assertTrue(r['blocked']);self.assertEqual(len(other.snapshot()['attempts']),3)
 def test_unknown_result_blocks_new_key_and_different_request(self):
  a=self.attempt();self.l.transition(a,'DISPATCHED');e=self.store.event(self.m,'p2_dispatch_failure_observed',result={'attempt':a,'known_not_executed':False});self.l.transition(a,'VALIDATION_INCONCLUSIVE',evidence=e,unknown=True)
  r=self.l.begin(self.p,'renamed','Dell2','test',{'command':'new command'});self.assertTrue(r['requires_observation']);self.assertEqual(r['attempt'],a)
 def test_completed_request_is_idempotent_across_alias(self):
  a=self.attempt();self.started(a);self.failed(a);r=self.l.begin(self.p,'renamed','Dell1','correction_test',{'command':'exit1'});self.assertTrue(r['cached']);self.assertEqual(len(self.l.snapshot()['attempts']),1)
 def test_problem_descriptor_cannot_be_replaced(self):
  with self.assertRaises(ValueError):self.l.problem('component',{'criterion':'renamed'})
 def test_arbitrary_evidence_does_not_create_success(self):
  a=self.attempt();self.l.transition(a,'DISPATCHED');fake=self.store.event(self.m,'plan',result={'attempt':a})
  with self.assertRaises(ValueError):self.l.transition(a,'RUNNING',evidence=fake)
 def test_running_attempt_prevents_concurrent_second_dispatch(self):
  a=self.attempt();self.started(a);r=self.l.begin(self.p,'new','Dell1','test',{'command':'something'});self.assertTrue(r['requires_observation']);self.assertEqual(r['attempt'],a)
 def test_infrastructure_failure_does_not_consume_correction_cycle(self):
  a=self.attempt();self.l.transition(a,'DISPATCHED');e=self.store.event(self.m,'p2_dispatch_failure_observed',result={'attempt':a,'known_not_executed':True});self.l.transition(a,'NOT_EXECUTED',evidence=e);self.l.failure(a,infrastructure=True)
  p=self.l.snapshot()['problems'][0];self.assertEqual(p['failed_cycles'],0);self.assertEqual(p['infra_incidents'],1)
 def test_success_requires_observed_verification(self):
  a=self.attempt();self.started(a);r={'returncode':0,'started':{'child_started':True},'verified':False};e=self.store.event(self.m,'p2_result_observed',result={'attempt':a,'observation':r})
  with self.assertRaises(ValueError):self.l.transition(a,'SUCCESS',evidence=e,result=r)
 def test_verifier_fourth_call_is_blocked_without_dispatch(self):
  from jarvis.attempt_execution import AttemptExecutor
  from unittest.mock import Mock
  a=self.l.begin(self.p,'verify','Dell1','execute',{'command':'true','verification':'verifier'})['attempt'];self.started(a)
  for n in range(1,4):self.store.event(self.m,'p2_verification_dispatched',result={'attempt':a,'sequence':n})
  runner=AttemptExecutor(self.store,self.m);runner.call=Mock()
  receipt={'start':{'attempt':a,'child_started':True,'command_sha256':digest('true')},'execution':{'returncode':0},'correction_before':{},'correction_after':{}}
  with self.assertRaisesRegex(ValueError,'no fourth'):runner.complete(self.l.get(a),receipt,1)
  runner.call.assert_not_called()

 def test_failed_verifier_does_not_mark_completed_action_running_again(self):
  from jarvis.attempt_execution import AttemptExecutor
  from unittest.mock import Mock
  a=self.l.begin(self.p,'verified-once','Dell1','execute',{'command':'true','verification':'bad-verifier'})['attempt'];self.started(a)
  r={'returncode':0,'started':{'child_started':True},'verified':False};e=self.store.event(self.m,'p2_result_observed',result={'attempt':a,'observation':r})
  self.l.transition(a,'VALIDATION_INCONCLUSIVE',evidence=e,result=r,unknown=False)
  runner=AttemptExecutor(self.store,self.m)
  runner.started(self.l.get(a),{'attempt':a,'child_started':True,'command_sha256':digest('true')},1)
  self.assertEqual(self.l.get(a)['state'],'VALIDATION_INCONCLUSIVE')
 def test_code_zero_with_wrong_semantic_value_fails(self):
  from jarvis.attempt_execution import AttemptExecutor
  from unittest.mock import Mock
  a=self.l.begin(self.p,'wrong-value','Dell2','correction_test',{'command':'write-value','verification':'read-value','verification_contract':{'kind':'json','expected':{'/value':42},'types':{'/value':'integer'}}})['attempt'];self.started(a)
  runner=AttemptExecutor(self.store,self.m);runner.call=Mock(return_value=({'ok':True,'result':{'returncode':0,'stdout':'{"value":100}','stderr':''}},1,'token'))
  receipt={'start':{'attempt':a,'child_started':True,'command_sha256':digest('write-value')},'execution':{'returncode':0},'correction_before':{'f':'old'},'correction_after':{'f':'new'}}
  result=runner.complete(self.l.get(a),receipt,1)
  self.assertEqual(result['state'],'EXECUTED_TEST_FAILED');self.assertEqual(result['failed_cycles'],1)
  self.assertEqual(result['result']['verification_semantic']['status'],'FAIL')

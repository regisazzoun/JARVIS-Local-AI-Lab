import importlib.util,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
spec=importlib.util.spec_from_file_location('authority',Path(__file__).parents[1]/'jarvis/distributed_authority.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
class Store:
 def __init__(self):self.rows=[]
 def get(self,m):return {'spec':json.dumps({'distributed_authority':True,'authority_requirements':['Q1']})}
 def events(self,*args,**kwargs):return self.rows
 def event(self,m,kind,t,actor,**kwargs):
  n=len(self.rows)+1;self.rows.append({'id':n,'kind':kind,'actor':actor,'result':kwargs['result']});return n
class GuardTests(unittest.TestCase):
 def setUp(self):
  self.s=Store();self.r=SimpleNamespace(mission_store=self.s,context={'mission_id':'real','task_id':'task'})
  self.s.rows.append({'id':1,'kind':'inference_finished','result':{'metrics':{'node':'Dell1','effective_model':'qwen3-coder-next:q4_K_M'}}})
  self.x=a.Authority(self.r)
 def test_latest_analysis_links_observed_failure_without_guessing_id(self):
  state=self.x.state();state['issues']['Q1']={'failed_cycles':1,'delegation_failures':0,'last_failed_test':'31'}
  state['executions']['31']={'issue':'Q1','kind':'test','execution':{'returncode':1}}
  self.x.save(state)
  r=self.x.analyze_latest({'issue':'Q1','summary':'My diagnosis based on the observed failure'})
  self.assertEqual(r['analyzed'],'31');self.assertEqual(self.x.state()['issues']['Q1']['analyzed'],'31')
 def test_counters_survive_new_adapter(self):
  state=self.x.state();a.budget(state,'Q1')['failed_cycles']=3;self.x.save(state)
  with self.assertRaisesRegex(ValueError,'trois cycles'):a.budget(a.Authority(self.r).state(),'Q1')
 def test_third_failure_stops_fourth_but_not_analysis(self):
  state={'issues':{'Q1':{'failed_cycles':2,'delegation_failures':0}}};self.assertEqual(a.budget(state,'Q1')['failed_cycles'],2)
  state['issues']['Q1']['failed_cycles']=3
  with self.assertRaises(ValueError):a.budget(state,'Q1')
  self.assertEqual(a.budget(state,'Q1',enforce=False)['failed_cycles'],3)
 def test_delegation_cap_is_separate(self):
  state={'issues':{'Q1':{'failed_cycles':0,'delegation_failures':3}}}
  with self.assertRaisesRegex(ValueError,'délégations'):a.budget(state,'Q1')
 def test_requested_model_name_does_not_attest_decision(self):
  self.s.rows[0]['result']['metrics']['node']='MacMini'
  with self.assertRaisesRegex(ValueError,'actual Qwen'):self.x.decision({'summary':'I am Qwen80B'})
 def test_actual_model_receipt_linked(self):
  n=self.x.decision({'summary':'inspect on Dell2'})
  self.assertEqual(self.s.rows[n-1]['result']['inference_event'],1)
 def test_failed_test_not_acceptance(self):
  state=self.x.state();state['executions']['T']={'issue':'Q1','kind':'test','execution':{'returncode':1}}
  self.x.save(state)
  with self.assertRaisesRegex(ValueError,'passed'):self.x.work({'issue':'Q1','kind':'accept','summary':'done','reference':'T'})
 def test_different_manifest_not_independent_validation(self):
  state=self.x.state();state['executions']={'T':{'issue':'Q1','host':'Dell2','kind':'test','execution':{'returncode':0},'before':{'x.py':'B'},'after':{'x.py':'B'}},'C':{'kind':'correct','host':'Dell1','after':{'x.py':'A'}}};self.x.save(state)
  with self.assertRaisesRegex(ValueError,'EXACT'):self.x.work({'issue':'Q1','kind':'accept','summary':'done','reference':'T','source_reference':'C'})
 def test_execution_idempotency_never_runs_remote_twice(self):
  args={'issue':'Q1','kind':'correct','summary':'fix','executor':'Dell1','command':'false','operation_id':'once'}
  state=self.x.state();state['operations']={'once':{'arguments':args,'result':{'reference':'ACTUAL'}}};self.x.save(state);self.x.remote=Mock()
  self.assertEqual(self.x.work(args),{'reference':'ACTUAL'});self.x.remote.assert_not_called()
 def test_uncertain_execution_cannot_blindly_retry(self):
  args={'issue':'Q1','kind':'correct','summary':'fix','executor':'Dell1','command':'false','operation_id':'once'}
  state=self.x.state();state['operations']={'once':{'arguments':args}};self.x.save(state)
  with self.assertRaisesRegex(ValueError,'uncertain'):self.x.work(args)
 def test_failed_test_is_executed_and_counted_only_after_correction(self):
  observed={'before':{'a.py':'A'},'after':{'a.py':'A'},'execution':{'returncode':1,'stdout':'FAIL real process fixture','stderr':'','output_truncated':False}}
  self.x.remote=Mock(return_value=({'stdout':json.dumps(observed)},'broker-test'))
  baseline=self.x.work({'issue':'Q1','kind':'test','summary':'baseline','executor':'Dell1','command':'false','operation_id':'baseline'})
  self.assertTrue(baseline['test_executed']);self.assertEqual(baseline['execution']['returncode'],1);self.assertEqual(baseline['failed_cycles'],0)
  self.x.work({'issue':'Q1','kind':'analyze','summary':'Interpret actual failure','reference':baseline['reference']})
  self.x.work({'issue':'Q1','kind':'correct','summary':'attempt','executor':'Dell1','command':'false','operation_id':'correct-1'})
  failed=self.x.work({'issue':'Q1','kind':'test','summary':'verification','executor':'Dell1','command':'false','operation_id':'test-1'})
  self.assertEqual(failed['failed_cycles'],1)
  with self.assertRaisesRegex(ValueError,'Analyze'):
   self.x.work({'issue':'Q1','kind':'correct','summary':'unanalysed retry','executor':'Dell2','command':'false','operation_id':'correct-2'})
 def test_actionable_view_preserves_reference_and_original_audit(self):
  original={'decision':7,'result':{'reference':'12','source_reference':'9','execution':{'returncode':1,'stderr':'Expected ValueError observed'},'broker_invocation':'private-audit-id'}}
  view=a.model_view(original)
  self.assertNotIn('decision',view);self.assertEqual(view['result']['reference'],12)
  self.assertEqual(view['result']['source_reference'],9)
  self.assertEqual(view['result']['execution']['returncode'],1)
  self.assertEqual(original['decision'],7);self.assertIn('broker_invocation',original['result'])
 def test_declared_correction_without_changed_file_cannot_be_accepted(self):
  state=self.x.state();state['executions']={'11':{'issue':'Q1','host':'Dell2','kind':'test','execution':{'returncode':0},'before':{'a.py':'A'},'after':{'a.py':'A'}},'10':{'issue':'Q1','kind':'correct','host':'Dell1','before':{'a.py':'A'},'after':{'a.py':'A'}}};self.x.save(state);self.x.remote=Mock()
  with self.assertRaisesRegex(ValueError,'no observed file change'):
   self.x.work({'issue':'Q1','kind':'accept','summary':'claimed fix','reference':11,'source_reference':10})
  self.x.remote.assert_not_called()
 def test_failed_execution_can_be_analyzed_despite_wrong_declared_phase(self):
  state=self.x.state();state['executions']['11']={'issue':'Q1','kind':'correct','execution':{'returncode':1}};self.x.save(state)
  result=self.x.work({'issue':'Q1','kind':'analyze','summary':'Actual failure observed','reference':11})
  self.assertTrue(result['execution_analyzed']);self.assertEqual(result['declared_kind'],'correct');self.assertEqual(result['observed_returncode'],1)
 def test_resolved_infrastructure_history_is_not_erased(self):
  state={'issues':{'P2':{'failed_cycles':0,'delegation_failures':3,'delegation_resolved_through':3}}}
  self.assertEqual(a.budget(state,'P2')['delegation_failures'],3)
  state['issues']['P2']['delegation_failures']=6
  with self.assertRaises(ValueError):a.budget(state,'P2')
 def test_version_sensitive_to_every_file(self):
  self.assertNotEqual(a.version({'a.py':'x'}),a.version({'a.py':'x','test.py':'y'}))
class InterfaceGuardTests(unittest.TestCase):
 def test_third_schema_failure_requests_stop_and_keeps_events(self):
  store=Store()
  for n in range(1,4):
   self.assertEqual(a.interface_failure(store,'m','t','authority_plan','Schema bad'),n==3)
  self.assertEqual(len([e for e in store.rows if e['kind']=='authority_interface_failure']),3)
  self.assertTrue(any(e['kind']=='authority_escalation' for e in store.rows))
if __name__=='__main__':unittest.main()

"""Software contracts; no simulated fixture is an agentic reception proof."""
import hashlib,json,subprocess,tempfile,unittest
from pathlib import Path
from jarvis.authority_probe import probe_command,matrix,declaration_digest
from jarvis.authority_attempts import test_not_loaded,test_infrastructure_error
from jarvis.mission_store import MissionStore

class DeclaredProbeTests(unittest.TestCase):
 def test_argv_is_exact_and_test_source_must_match(self):
  with tempfile.TemporaryDirectory() as root:
   p=Path(root)/'probe.py';p.write_text('import sys; assert sys.argv[1:] == []; print("real probe ran")\n')
   spec={'argv':['python3',str(p)],'env':{},'sources':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()}}
   result=subprocess.run(probe_command(spec),shell=True,text=True,capture_output=True)
   self.assertEqual(result.returncode,0,result.stderr);self.assertIn('real probe ran',result.stdout)
   p.write_text('raise RuntimeError("tampered code must not run")')
   result=subprocess.run(probe_command(spec),shell=True,text=True,capture_output=True)
   self.assertEqual(result.returncode,125);self.assertIn('JARVIS_PROBE_NOT_STARTED',result.stderr);self.assertNotIn('RuntimeError',result.stderr)
 def test_loader_failure_in_merged_stdout_is_not_a_functional_test(self):
  failed={'returncode':1,'stdout':"tests (unittest.loader._FailedTest.tests) ... ERROR\nModuleNotFoundError: No module named 'jarvis.tests'\nRan 1 test in 0.000s\n",'stderr':''}
  self.assertTrue(test_not_loaded(failed));self.assertTrue(test_infrastructure_error(failed))
  actual={'returncode':1,'stdout':'test_real (__main__.ActualCase.test_real) ... FAIL\nRan 1 test in 0.001s\nAssertionError: wrong result','stderr':''}
  self.assertFalse(test_not_loaded(actual));self.assertFalse(test_infrastructure_error(actual))
 def test_matrix_requires_both_probes_hosts_and_exact_declaration_version(self):
  spec={'authority_probes':{'one':{'argv':['python3','one.py'],'sources':{}},'two':{'argv':['python3','two.py'],'sources':{}}}};manifest={'app.py':'new'};state={'executions':{}}
  self.assertEqual(matrix(spec,state,manifest)['Dell1']['one']['status'],'NOT_EXECUTED')
  for i,(host,key) in enumerate((('Dell1','one'),('Dell1','two'),('Dell2','one'),('Dell2','two')),1):
   state['executions'][str(i)]={'host':host,'probe_id':key,'kind':'test','before':manifest,'after':manifest,'probe_declaration_sha256':declaration_digest(spec['authority_probes'][key]),'execution':{'returncode':0}}
  self.assertTrue(all(v['status']=='PASS' for probes in matrix(spec,state,manifest).values() for v in probes.values()))
  state['executions']['4']['after']={'app.py':'old'}
  self.assertEqual(matrix(spec,state,manifest)['Dell2']['two']['status'],'NOT_EXECUTED')

class ClassificationAuditTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.s=MissionStore(self.temp.name);self.m=self.s.create('fixture','model','conv');self.l=self.s.attempt_ledger(self.m);self.p=self.l.problem('fixture-correction',{'stable':'same issue'})
 def source_failure(self,output):
  execution={'returncode':1,'stdout':output,'stderr':'','output_truncated':False}
  ref=self.s.event(self.m,'authority_execution',result={'kind':'test','execution':execution,'before':{},'after':{}})
  a=self.l.begin(self.p,'one','Dell1','correction_test',{'command':'fixture'})['attempt'];self.l.transition(a,'DISPATCHED')
  start=self.s.event(self.m,'p2_started_observed',result={'attempt':a,'marker':{'child_started':True}});self.l.transition(a,'RUNNING',evidence=start)
  result={'returncode':0,'started':{'child_started':True},'verified':False,'source_changed':True,'failed_test_reference':ref,'test_execution':execution,'value':{'reference':111}}
  ev=self.s.event(self.m,'p2_result_observed',result={'attempt':a,'observation':result});self.l.transition(a,'EXECUTED_TEST_FAILED',evidence=ev,result=result);self.l.failure(a,correction_changed=True)
  self.s.transition(self.m,'interrupted');return a,ref
 def proof(self,ref,actor='Codex'):
  return self.s.event(self.m,'coordinator_test_loading_failure_verified',actor=actor,result={'verified':True,'test_reference':ref})
 def test_reclassification_preserves_historical_total_and_is_idempotent(self):
  a,ref=self.source_failure('unittest.loader._FailedTest.tests\nModuleNotFoundError: no module\nRan 1 test in 0.000s')
  proof=self.proof(ref);result=self.l.reclassify_unloaded_test(ref,proof)
  p=self.l.snapshot()['problems'][0];self.assertEqual((p['failed_cycles'],p['misclassified_failed_cycles']),(0,1))
  self.assertEqual(result['corrections'][0]['historical_total_preserved'],1)
  self.assertEqual(self.l.get(a)['state'],'VALIDATION_INCONCLUSIVE');self.assertFalse(self.l.get(a)['unknown_outcome'])
  self.assertFalse(self.l.get(a)['result']['failure_counted'])
  self.assertTrue(self.l.reclassify_unloaded_test(ref,proof)['cached'])
  self.assertEqual(self.l.snapshot()['problems'][0]['misclassified_failed_cycles'],1)
  self.assertNotIn('requires_observation',self.l.begin(self.p,'next','Dell1','correction_test',{'command':'new actual correction'}))
 def test_real_assertion_failure_cannot_be_excused(self):
  a,ref=self.source_failure('test_real (__main__.Actual.test_real) ... FAIL\nAssertionError: wrong\nRan 1 test in 0.001s')
  with self.assertRaisesRegex(ValueError,'pure loader'):self.l.reclassify_unloaded_test(ref,self.proof(ref))
  self.assertEqual(self.l.snapshot()['problems'][0]['failed_cycles'],1)
 def test_model_cannot_reclassify_a_counter(self):
  a,ref=self.source_failure('unittest.loader._FailedTest.tests\nModuleNotFoundError: no module\nRan 1 test in 0.000s')
  with self.assertRaisesRegex(ValueError,'coordinator'):self.l.reclassify_unloaded_test(ref,self.proof(ref,'JARVIS'))

class EvidenceBoundAcceptanceTests(unittest.TestCase):
 def fixture(self):
  from jarvis.authority_probe import declaration_digest
  spec={'authority_readonly_validation':True,'authority_probes':{'core':{'argv':['core'],'sources':{}},'var':{'argv':['var'],'sources':{}}}}
  manifest={'app':'current'};rows={'10':{'issue':'R','host':'Dell1','kind':'correct','before':{'app':'old'},'after':manifest,'execution':{'returncode':0}}}
  for ref,host,key in [(11,'Dell1','core'),(12,'Dell1','var'),(13,'Dell2','core'),(14,'Dell2','var')]:
   rows[str(ref)]={'issue':'R','host':host,'kind':'test','probe_id':key,'probe_declaration_sha256':declaration_digest(spec['authority_probes'][key]),'before':manifest,'after':manifest,'execution':{'returncode':0}}
  return spec,{'executions':rows},{'issue':'R','validator':'Dell2','summary':'Model decides acceptance from recorded observations'}
 def test_readonly_resolves_two_actual_passed_peer_tests(self):
  from jarvis.authority_probe import acceptance_request
  spec,state,args=self.fixture();r=acceptance_request(spec,state,args)
  self.assertEqual((r['reference'],r['source_reference']),(14,12));self.assertEqual(r['kind'],'accept')
 def test_editable_retains_actual_correction_provenance(self):
  from jarvis.authority_probe import acceptance_request
  spec,state,args=self.fixture();spec['authority_readonly_validation']=False
  self.assertEqual(acceptance_request(spec,state,args)['source_reference'],10)
  args['validator']='Dell1'
  with self.assertRaisesRegex(ValueError,'peer'):acceptance_request(spec,state,args)
 def test_cannot_accept_missing_failed_or_wrong_version_probes(self):
  import copy
  from jarvis.authority_probe import acceptance_request
  spec,state,args=self.fixture()
  for change in ['missing','failed','version','declaration']:
   bad=copy.deepcopy(state)
   if change=='missing':bad['executions'].pop('14')
   elif change=='failed':bad['executions']['14']['execution']['returncode']=1
   elif change=='version':bad['executions']['14']['after']={'app':'stale'}
   else:bad['executions']['14']['probe_declaration_sha256']='changed'
   with self.subTest(change=change),self.assertRaisesRegex(ValueError,'All declared probes'):acceptance_request(spec,bad,args)

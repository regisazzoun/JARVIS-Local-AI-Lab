import hashlib,tempfile,unittest
from types import SimpleNamespace
from unittest.mock import Mock
from jarvis.mission_store import MissionStore
from jarvis.legacy_attempts import guarded,settle,pending_report_validation
class Recomposition(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.s=MissionStore(self.tmp.name)
  self.m=self.s.create('fixture report','model','conv',spec={'planning_report_steps':True})
  self.criterion={'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/fixture.md'}}}
  self.s.plan(self.m,[{'id':'t','title':'fixture','contract':{'report_path':'/fixture.md','semantic':[self.criterion]}}])
  self.reg=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'t'})
  self.sha=hashlib.sha256(b'fixture').hexdigest()
  guarded(self.reg,'host_write_file',{'path':'/fixture.md','content':'fixture'},Mock(return_value={'returncode':0,'evidence_id':'fixture-write'}),True)
  verdict={'status':'FAIL','contract':self.criterion,'sha256':self.sha}
  ref=self.s.event(self.m,'semantic_verification','t',result=verdict);verdict['verification_event']=ref;settle(self.reg,verdict)
 def compose(self,*,ok=True,sha=None,task='t',prepared=True):
  ref=self.s.event(self.m,'proof_bound_report_prepared',task,result={'draft_sha256':sha or self.sha}) if prepared else 0
  call=self.s.begin_call(self.m,task,'mission_report_compose',{'references':[],'explanation':''})
  self.s.finish_call(call,{'ok':ok,'result':{'returncode':0 if ok else 1,'prepared_event':ref,'write':{'ok':ok,'result':{'returncode':0 if ok else 1}}}},0)
 def test_same_content_with_new_completed_provenance_reopens_verify_only(self):
  self.assertEqual(pending_report_validation(self.s,self.m,'t')['phase'],'correct');self.compose();before=self.s.attempt_ledger(self.m).snapshot()
  state=pending_report_validation(self.s,self.m,'t');self.assertEqual(state['phase'],'verify');self.assertTrue(state['recomposed_after_failed_verification']['prior_failure_unchanged'])
  self.assertEqual(before,self.s.attempt_ledger(self.m).snapshot());self.assertEqual(before['attempts'][0]['state'],'EXECUTED_TEST_FAILED')
  self.assertFalse(self.s.contract_status(self.m,'t')['all_satisfied'])
 def test_preparation_without_completed_composition_does_not_unlock(self):
  self.s.event(self.m,'proof_bound_report_prepared','t',result={'draft_sha256':self.sha})
  self.assertEqual(pending_report_validation(self.s,self.m,'t')['phase'],'correct')
 def test_failed_composition_does_not_unlock(self):
  self.compose(ok=False);self.assertEqual(pending_report_validation(self.s,self.m,'t')['phase'],'correct')
 def test_other_bytes_or_other_task_do_not_unlock(self):
  self.compose(sha='f'*64);self.compose(task='other');self.assertEqual(pending_report_validation(self.s,self.m,'t')['phase'],'correct')
 def test_newer_unknown_write_is_not_hidden_by_composition(self):
  self.compose()
  with self.assertRaises(ConnectionError):guarded(self.reg,'host_write_file',{'path':'/fixture.md','content':'different'},Mock(side_effect=ConnectionError('unknown')),True)
  self.assertIsNone(pending_report_validation(self.s,self.m,'t'))

import unittest,tempfile,json
from types import SimpleNamespace
from unittest.mock import Mock
from jarvis.mission_store import MissionStore
from jarvis.legacy_attempts import guarded,settle
class CanonicalGuardTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.s=MissionStore(self.temp.name);self.m=self.s.create('goal','model','conversation');self.contract={'kind':'json','source':{'tool':'host_read_file','arguments':{'path':'/fixture.json'}},'expected':{'/value':42}}
  self.s.plan(self.m,[{'id':'task','title':'task','contract':{'semantic':[self.contract]}}]);self.reg=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'task'})
 def tearDown(self):self.temp.cleanup()
 def run_action(self,command='first',code=0):
  fn=Mock(return_value={'returncode':code,'stdout':'','evidence_id':'real-backend-ref'});r=guarded(self.reg,'host_exec',{'command':command},fn,True);return r,fn
 def verdict(self,status,contract=None):
  v={'status':status,'contract':contract or self.contract};e=self.s.event(self.m,'semantic_verification','task',result=v);v['verification_event']=e;settle(self.reg,v)
 def test_rc0_is_not_semantic_success_and_new_alias_is_blocked(self):
  self.run_action();self.assertEqual(self.s.attempt_ledger(self.m).snapshot()['attempts'][0]['state'],'VALIDATION_INCONCLUSIVE')
  fn=Mock()
  with self.assertRaisesRegex(ValueError,'no action dispatched'):guarded(self.reg,'host_exec',{'command':'renamed'},fn,True)
  fn.assert_not_called()
 def test_independent_contract_pass_unlocks_and_replays_without_dispatch(self):
  self.run_action();self.verdict('PASS');fn=Mock();guarded(self.reg,'host_exec',{'command':'first'},fn,True);fn.assert_not_called();self.assertEqual(self.s.attempt_ledger(self.m).snapshot()['attempts'][0]['state'],'SUCCESS')
 def test_unrelated_explicit_contract_does_not_accept(self):
  self.run_action();self.verdict('PASS',{'kind':'json','expected':{'/other':0}});self.assertEqual(self.s.attempt_ledger(self.m).snapshot()['attempts'][0]['state'],'VALIDATION_INCONCLUSIVE')
 def test_three_observed_verification_failures_escalate(self):
  for i in range(3):self.run_action(str(i));self.verdict('FAIL')
  fn=Mock()
  with self.assertRaisesRegex(ValueError,'no fourth'):guarded(self.reg,'host_exec',{'command':'fourth'},fn,True)
  fn.assert_not_called();self.assertEqual(self.s.attempt_ledger(self.m).snapshot()['problems'][0]['state'],'ESCALATED')
 def test_transport_unknown_is_not_declared_unexecuted_or_succeeded(self):
  with self.assertRaises(ConnectionError):guarded(self.reg,'host_exec',{'command':'x'},Mock(side_effect=ConnectionError('lost')),True)
  self.verdict('PASS');row=self.s.attempt_ledger(self.m).snapshot()['attempts'][0];self.assertTrue(row['unknown_outcome']);self.assertEqual(row['state'],'VALIDATION_INCONCLUSIVE')
 def test_all_predicates_must_be_fresh_after_mutation(self):
  second={**self.contract,'expected':{'/value':43}};task=self.s.tasks(self.m)[0];task['contract']['semantic'].append(second)
  self.s.plan(self.m,[task],expected_version=1);self.verdict('PASS');self.run_action();self.verdict('PASS',second);self.assertEqual(self.s.attempt_ledger(self.m).snapshot()['attempts'][0]['state'],'VALIDATION_INCONCLUSIVE');self.verdict('PASS');self.assertEqual(self.s.attempt_ledger(self.m).snapshot()['attempts'][0]['state'],'SUCCESS')
 def test_real_registry_and_verifier_share_guarded_attempt(self):
  from jarvis.tools import Registry
  from jarvis.memory import Memory
  from pathlib import Path
  reg=Registry(Memory(Path(self.temp.name)/'memory.sqlite'),self.temp.name)
  reg.mission_store=self.s;reg.context={'mission_id':self.m,'task_id':'task'};current={'value':0};writes=[]
  reg.specs['host_read_file']=('read',{'path':{'type':'string'}},['path'],'host_authorized',lambda a:{'returncode':0,'stdout':json.dumps(current),'evidence_id':'read'})
  def write(a):current['value']=json.loads(a['content'])['value'];writes.append(a);return {'returncode':0,'evidence_id':'write'}
  reg.specs['host_write_file']=('write',{'path':{'type':'string'},'content':{'type':'string'}},['path','content'],'host_authorized',write)
  result=reg.execute('host_write_file',{'path':'/fixture.json','content':'{"value":42}'});self.assertTrue(result['ok'],result)
  self.assertFalse(reg.execute('host_write_file',{'path':'/fixture.json','content':'{"value":43}'})['ok']);self.assertEqual(len(writes),1)
  result=reg.execute('mission_verify',{'contract':'active:0'});self.assertTrue(result['ok'],result)
  snapshot=self.s.attempt_ledger(self.m).snapshot();self.assertEqual(snapshot['attempts'][0]['state'],'SUCCESS')
  self.assertTrue(json.loads(snapshot['attempts'][0]['result'])['change_observed'])
 def test_real_registry_mission_action_alternate_key_cannot_bypass(self):
  from jarvis.tools import Registry
  from jarvis.memory import Memory
  from pathlib import Path
  reg=Registry(Memory(Path(self.temp.name)/'memory.sqlite'),self.temp.name);reg.mission_store=self.s;reg.context={'mission_id':self.m,'task_id':'task'}
  calls=[]
  reg.specs['host_exec']=('write',{'command':{'type':'string'}},['command'],'host_authorized',lambda a:calls.append(a) or {'returncode':0})
  reg.specs['host_read_file']=('read',{'path':{'type':'string'}},['path'],'host_authorized',lambda a:{'returncode':0,'stdout':'{"value":0}'})
  a={'operation_key':'original','tool':'host_exec','arguments':'{"command":"first"}'}
  self.assertTrue(reg.execute('mission_action',a)['ok'])
  b={**a,'operation_key':'other','arguments':'{"command":"second"}'}
  self.assertFalse(reg.execute('mission_action',b)['ok']);self.assertEqual(len(calls),1)
 def test_remote_verification_downloads_fresh_bytes_and_checks_sha(self):
  import hashlib
  from jarvis.verification import Verifier
  body='{"value":42}';seen=[]
  def execute(name,args):
   seen.append((name,args))
   if name=='host_remote':return {'ok':True,'result':{'returncode':0,'sha256':hashlib.sha256(body.encode()).hexdigest(),'evidence_id':'download'}}
   return {'ok':True,'result':{'returncode':0,'stdout':body,'evidence_id':'read'}}
  reg=SimpleNamespace(execute=execute,context={})
  source={'tool':'host_remote','arguments':{'action':'project_download','host':'dell2','project':'p','path':'/remote.json','local_path':'/local.json'}}
  text,proof=Verifier(reg).read(source);self.assertEqual(text,body);self.assertEqual([s[0] for s in seen],['host_remote','host_read_file']);self.assertIn('fresh_local_read',proof)
 def test_changed_local_copy_cannot_pass_remote_download_verification(self):
  from jarvis.verification import Verifier
  def execute(name,args):
   return {'ok':True,'result':{'returncode':0,'sha256':'f'*64,'stdout':'{"value":42}'}}
  reg=SimpleNamespace(execute=execute,context={})
  with self.assertRaisesRegex(ValueError,'SHA differs'):Verifier(reg).read({'tool':'host_remote','arguments':{'action':'project_download','local_path':'/copy.json'}})

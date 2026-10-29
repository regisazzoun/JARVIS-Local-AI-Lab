"""Canonical SQLite/tool integration fixtures, not distributed autonomy evidence."""
import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from jarvis.core import Core,ROOT
from jarvis.memory import Memory
from jarvis.mission_store import MissionStore
from jarvis.distributed_authority import Authority
from jarvis.authority_identity import invocation_scope


class IdentityTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name);self.s=MissionStore(self.root)
  self.m=self.s.create('software fixture','model','conv',spec={'distributed_authority':True,'authority_requirements':['Q1'],'authority_engine_operation_ids':True})
  self.s.plan(self.m,[{'id':'task','title':'fixture'},{'id':'peer','title':'other task'}])
  self.config=json.loads((ROOT/'config/example.json').read_text());self.config['identity_file']=str(ROOT/'identity/JARVIS-v2.md');self.reg=self.registry()
  self.s.event(self.m,'inference_finished','task',result={'metrics':{'node':'Dell1','effective_model':'qwen3-coder-next:q4_K_M'},'software_fixture':True})
  self.executed=[];self.source='one';self.fail_transport=False
  def remote(instance,host,command):
   # Only fixture user commands increment this list, never source probes.
   if "'printf A'" in command or "'printf B'" in command:
    self.executed.append((host,'A' if "'printf A'" in command else 'B'))
    if self.fail_transport:raise OSError('fixture response lost; outcome unknown')
   manifest={'app.py':self.source}
   return {'stdout':json.dumps({'before':manifest,'after':manifest,'execution':{'returncode':0,'stdout':'fixture observed','stderr':''}})},'fixture-broker'
  self.patcher=patch.object(Authority,'remote',remote);self.patcher.start();self.addCleanup(self.patcher.stop)

 def registry(self):
  reg=Core(self.config,Memory(self.root/'memory.sqlite')).tools
  reg.mission_store=self.s;reg.context={'mission_id':self.m,'task_id':'task'}
  return reg

 def args(self,command='printf A',kind='inspect'):
  return {'issue':'Q1','kind':kind,'executor':'Dell1','command':command,'summary':'Fixture operation'}

 def call(self,args,tool='authority_work'):
  token=self.s.begin_call(self.m,self.reg.context['task_id'],tool,args)
  with invocation_scope(token):result=self.reg.execute(tool,args)
  self.s.finish_call(token,result,0)
  return token,result

 def test_different_commands_need_no_model_ids_and_keep_decision_attribution(self):
  first,a=self.call(self.args());second,b=self.call(self.args('printf B'))
  self.assertTrue(a['ok'],a);self.assertTrue(b['ok'],b)
  self.assertEqual(self.executed,[('Dell1','A'),('Dell1','B')])
  state=Authority(self.reg).state();self.assertEqual(set(state['operations']),{'call:'+first,'call:'+second})
  decisions=[e for e in self.s.events(self.m) if e['kind']=='authority_model_decision']
  self.assertTrue(all('operation_id' not in e['result']['instruction'] for e in decisions))
  identities=[e for e in self.s.events(self.m) if e['kind']=='authority_operation_identity']
  self.assertEqual(len(identities),2);self.assertTrue(all(e['actor']=='JARVIS-engine' for e in identities))

 def test_same_intent_changed_summary_and_registry_restart_deduplicates(self):
  _,first=self.call(self.args());self.reg=self.registry()
  args=self.args();args['summary']='A new description is not a new operation'
  _,second=self.call(args)
  self.assertTrue(second['ok'],second);self.assertTrue(second['result']['cached'])
  self.assertEqual(second['result']['reference'],first['result']['reference'])
  self.assertEqual(len(self.executed),1)

 def test_new_task_gets_own_execution_not_previous_task_receipt(self):
  _,first=self.call(self.args());self.reg.context['task_id']='peer'
  _,second=self.call(self.args())
  self.assertTrue(second['ok'],second);self.assertNotEqual(first['result']['reference'],second['result']['reference'])
  self.assertEqual(len(self.executed),2)

 def test_changed_source_gets_fresh_test(self):
  _,first=self.call(self.args(kind='test'));self.source='changed'
  _,second=self.call(self.args(kind='test'))
  self.assertTrue(second['ok'],second);self.assertNotEqual(first['result']['reference'],second['result']['reference'])
  self.assertEqual(len(self.executed),2)

 def test_unknown_correction_blocks_different_command_and_new_identity(self):
  self.fail_transport=True
  _,first=self.call(self.args(kind='correct'));self.assertFalse(first['ok'])
  self.fail_transport=False
  _,second=self.call(self.args('printf B',kind='correct'))
  self.assertFalse(second['ok']);self.assertIn('requires_observation',second['error'])
  self.assertEqual(self.executed,[('Dell1','A')])
  self.assertTrue(any(r['unknown_outcome'] for r in self.s.attempt_ledger(self.m).snapshot()['attempts']))

 def test_three_failures_still_stop_dispatch_despite_new_generated_keys(self):
  a=Authority(self.reg);state=a.state();state['issues']['Q1']={'failed_cycles':3,'delegation_failures':0};a.save(state)
  _,result=self.call(self.args());self.assertFalse(result['ok']);self.assertIn('trois cycles',result['error'])
  self.assertEqual(self.executed,[]);self.assertEqual(Authority(self.reg).state()['issues']['Q1']['failed_cycles'],3)

 def test_forged_or_finished_invocation_cannot_execute(self):
  args=self.args();token=self.s.begin_call(self.m,'peer','authority_work',args)
  with invocation_scope(token):r=self.reg.execute('authority_work',args)
  self.assertFalse(r['ok']);self.assertIn('mission/task',r['error'])
  self.s.finish_call(token,{'ok':False},0)
  self.reg.context['task_id']='peer'
  with invocation_scope(token):r=self.reg.execute('authority_work',args)
  self.assertFalse(r['ok']);self.assertEqual(self.executed,[])

 def test_command_cannot_be_swapped_under_same_canonical_invocation(self):
  token=self.s.begin_call(self.m,'task','authority_work',self.args())
  with invocation_scope(token):r=self.reg.execute('authority_work',self.args('printf B'))
  self.assertFalse(r['ok']);self.assertIn('differs',r['error']);self.assertEqual(self.executed,[])

 def test_no_context_fallback_or_model_supplied_key(self):
  r=self.reg.execute('authority_work',self.args());self.assertFalse(r['ok']);self.assertIn('canonical',r['error'])
  args={**self.args(),'operation_id':'model-label'};_,r=self.call(args)
  self.assertFalse(r['ok']);self.assertEqual(self.executed,[])
  schema=self.reg.active_schema('authority_edit');self.assertNotIn('operation_id',schema['properties']);self.assertNotIn('operation_id',schema['required'])

 def test_legacy_mode_keeps_collision_rejection(self):
  with self.s.db() as c:
   spec=json.loads(self.s.get(self.m)['spec']);spec['authority_engine_operation_ids']=False
   c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  args={**self.args(),'operation_id':'legacy'};_,first=self.call(args);self.assertTrue(first['ok'],first)
  args['command']='printf B';_,second=self.call(args)
  self.assertFalse(second['ok']);self.assertIn('reused for different arguments',second['error']);self.assertEqual(len(self.executed),1)

 def test_edit_adapter_binds_generated_command_to_original_edit_invocation(self):
  args={'issue':'Q1','executor':'Dell2','summary':'literal code edit','edits':[{'path':'app.py','old':'one','new':'two'}]}
  _,r=self.call(args,tool='authority_edit')
  self.assertTrue(r['ok'],r)
  identity=[e for e in self.s.events(self.m) if e['kind']=='authority_operation_identity']
  self.assertEqual(len(identity),1)

 def test_real_durable_dispatch_supplies_started_invocation_scope(self):
  from jarvis.missions import Missions
  self.config['durable_cycle_rounds']=1
  core=Core(self.config,Memory(self.root/'memory.sqlite'));engine=Missions(core,self.root,start_worker=False)
  def transport(payload):
   core=engine.execution_core
   core.metrics.append({'node':'Dell1','effective_model':'qwen3-coder-next:q4_K_M','software_fixture':True})
   return {'role':'assistant','tool_calls':[{'function':{'name':'authority_work','arguments':self.args()}}]}
  engine.execution_core.transport=transport
  engine.cycle.run(engine.store.get(self.m))
  executions=[e for e in self.s.events(self.m) if e['kind']=='authority_execution']
  self.assertEqual(len(executions),1)
  self.assertEqual(self.executed,[('Dell1','A')])

 def test_new_api_submissions_enable_engine_ids_but_keep_explicit_legacy_choice(self):
  from jarvis.missions import Missions
  core=Core(self.config,Memory(self.root/'memory.sqlite'));engine=Missions(core,self.root,start_worker=False)
  for setting in [None,False]:
   spec={'distributed_authority':True,'autonomous':False}
   if setting is not None:spec['authority_engine_operation_ids']=setting
   result=engine.submit('new fixture',self.config['models'][0],spec=spec)
   saved=json.loads(engine.store.get(result['id'])['spec'])
   self.assertIs(saved['authority_engine_operation_ids'],True if setting is None else False)

 def test_obsolete_diagnosis_drops_from_working_view_but_history_and_counts_survive(self):
  with self.s.db() as c:
   spec=json.loads(self.s.get(self.m)['spec']);spec['authority_task_scoped_evidence']=True;spec['authority_evidence_after_event']=999999
   c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  a=Authority(self.reg);state=a.state();state['issues']['Q1']={'failed_cycles':2,'delegation_failures':1,'analyzed':'old','analysis':'Obsolete hypothesis'};a.save(state)
  view=a.active_state();self.assertNotIn('analysis',view['issues']['Q1']);self.assertNotIn('analyzed',view['issues']['Q1'])
  self.assertEqual(view['issues']['Q1']['failed_cycles'],2)
  self.assertEqual(a.state()['issues']['Q1']['analysis'],'Obsolete hypothesis')

 def test_reader_active_schema_tracks_current_manifest_without_erasing_history(self):
  _,first=self.call(self.args());old=first['result']['reference']
  self.source='new version';_,second=self.call(self.args('printf B'));new=second['result']['reference']
  props=self.reg.active_schema('authority_read_execution')['properties']
  self.assertEqual(props['reference']['enum'],[new])
  self.assertIn(str(old),Authority(self.reg).state()['executions'])
  from jarvis.mission_context_budget import ContextBudget
  archived=ContextBudget(self.s,self.m,'task').recall(old,limit=4000)
  self.assertEqual(archived['reference'],old)
  self.assertEqual(archived['kind'],'authority_execution')

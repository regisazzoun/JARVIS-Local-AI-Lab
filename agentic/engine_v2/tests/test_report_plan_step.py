"""Real registry/store checks; not evidence of model autonomy."""
import json,tempfile,unittest
from pathlib import Path
from jarvis.tools import Registry
from jarvis.memory import Memory
from jarvis.mission_store import MissionStore
class ReportStepTests(unittest.TestCase):
 def completed_report_write(self):
  from types import SimpleNamespace
  from jarvis.legacy_attempts import guarded
  self.assertTrue(self.save()['ok'])
  reg=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'a'})
  guarded(reg,'host_write_file',{'path':'/project/a.md','content':'Software fixture report'},lambda a:{'returncode':0,'evidence_id':'software-fixture-write'},True)
  return reg

 def test_pending_report_projection_requires_known_completed_matching_write(self):
  from jarvis.legacy_attempts import pending_report_validation
  import hashlib
  self.completed_report_write()
  p=pending_report_validation(self.s,self.m,'a');self.assertIsNotNone(p)
  self.assertEqual(p['expected_written_content_sha256'],hashlib.sha256(b'Software fixture report').hexdigest())
  self.assertEqual(p['verification_calls'],[{'contract':'active:0'}]);self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')
  self.assertIsNone(pending_report_validation(self.s,self.m,'other-task'))
  with self.s.db() as c:c.execute('UPDATE mission_attempts_v2 SET unknown_outcome=1 WHERE id=?',(p['attempt'],))
  self.assertIsNone(pending_report_validation(self.s,self.m,'a'))

 def test_actual_cycle_focuses_validation_then_restores_tools_after_observed_failure(self):
  from jarvis.core import Core
  from jarvis.missions import Missions
  from jarvis.legacy_attempts import settle,pending_report_validation
  reg=self.completed_report_write();identity=self.root/'identity.txt';identity.write_text('Full test identity')
  core=Core({'identity_file':str(identity),'durable_cycle_rounds':1,'num_ctx':32768},Memory(self.root/'runtime/memory.sqlite'))
  missions=Missions(core,self.root,start_worker=False,start_publisher=False);captured=[]
  def transport(payload):
   captured.append(payload)
   return {'tool_calls':[{'function':{'name':'mission_note','arguments':{'content':'Software fixture, not an actual model'}}}]}
  missions.execution_core.transport=transport;missions.cycle.run(self.s.get(self.m))
  names={t['function']['name'] for t in captured[-1]['tools']}
  self.assertIn('mission_verify',names);self.assertNotIn('host_write_file',names);self.assertNotIn('mission_plan_report_step',names)
  verdict={'status':'FAIL','contract':self.s.tasks(self.m)[0]['contract']['semantic'][0]}
  self.s.event(self.m,'semantic_verification','a',result=verdict);settle(reg,verdict)
  self.assertEqual(pending_report_validation(self.s,self.m,'a')['phase'],'correct')
  missions.cycle.run(self.s.get(self.m))
  names={t['function']['name'] for t in captured[-1]['tools']};self.assertIn('host_write_file',names)
  self.assertNotIn('mission_plan_report_step',names);self.assertNotIn('host_service',names)
  attempt=self.s.attempt_ledger(self.m).snapshot()['attempts'][0]
  self.assertEqual(attempt['state'],'EXECUTED_TEST_FAILED');self.assertFalse(attempt['unknown_outcome'])

 def test_validation_instruction_survives_budget_compaction(self):
  from jarvis.mission_context_budget import ContextBudget
  self.completed_report_write()
  payload={'model':'fixture','messages':[{'role':'system','content':'Complete policy'},{'role':'user','content':'old '*30000}],'options':{'num_predict':1024},'tools':[]}
  result=ContextBudget(self.s,self.m,'a').prepare(payload,{'limit':16384})
  state=json.loads(result['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['pending_report_validation']['report_path'],'/project/a.md')
  self.assertEqual(state['pending_report_validation']['verification_calls'],[{'contract':'active:0'}])
  self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')

 def test_pass_only_exposes_completion_and_newer_unknown_write_invalidates_old_focus(self):
  from jarvis.legacy_attempts import pending_report_validation,settle
  reg=self.completed_report_write()
  verdict={'status':'PASS','contract':self.s.tasks(self.m)[0]['contract']['semantic'][0]}
  self.s.event(self.m,'semantic_verification','a',result=verdict);settle(reg,verdict)
  self.assertEqual(pending_report_validation(self.s,self.m,'a')['phase'],'complete')
  self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')
  # A newer unknown write is a distinct software fixture state, not proof that
  # the previous PASS still describes the current file.
  with self.s.db() as c:
   row=dict(c.execute('SELECT * FROM mission_attempts_v2 WHERE mission=?',(self.m,)).fetchone())
   row.update(id='newer-unknown-fixture',operation_key='unknown',signature='newer',state='VALIDATION_INCONCLUSIVE',unknown_outcome=1,created=row['created']+1)
   c.execute('INSERT INTO mission_attempts_v2 ('+','.join(row)+') VALUES ('+','.join('?' for _ in row)+')',tuple(row.values()))
  self.assertIsNone(pending_report_validation(self.s,self.m,'a'))

 def test_execution_projection_keeps_identity_owner_goal_and_stored_criterion(self):
  from jarvis.core import Core
  from jarvis.missions import Missions
  identity=self.root/'identity.txt';identity.write_text('KEEP FULL IDENTITY AND OWNER AUTHORIZATION')
  core=Core({'identity_file':str(identity),'durable_cycle_rounds':1,'num_ctx':32768},Memory(self.root/'runtime/memory.sqlite'))
  missions=Missions(core,self.root,start_worker=False,start_publisher=False)
  m=missions.store.create('FULL OWNER OBJECTIVE; NO DEPLOYMENT','fixture','conv',spec={'planning_report_steps':True})
  criterion={'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/project/a.md'}}}
  missions.store.plan(m,[{'id':'a','title':'Observe and report','objective':'Read actual unit status','depends':[],'tools':['mission_note'],'contract':{'report_path':'/project/a.md','semantic':[criterion]}}])
  captured=[]
  def transport(payload):
   captured.append(payload)
   return {'tool_calls':[{'function':{'name':'mission_note','arguments':{'content':'Software fixture only'}}}]}
  missions.execution_core.transport=transport;missions.cycle.run(missions.store.get(m))
  self.assertTrue(captured[0]['messages'][0]['content'].startswith(identity.read_text()))
  self.assertIn('FULL OWNER OBJECTIVE; NO DEPLOYMENT',captured[0]['messages'][1]['content'])
  self.assertNotIn('mission_plan',[t['function']['name'] for t in captured[0]['tools']])
  self.assertEqual(missions.store.tasks(m)[0]['contract']['semantic'],[criterion])

 def test_saved_plan_is_not_reported_as_unexecuted_when_review_exceeds_budget(self):
  from unittest.mock import patch
  from jarvis.mission_context_budget import ContextCapacityError
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'autonomous':True,'planning_report_steps':True,'assurance':True}),self.m))
  with patch('jarvis.mission_assurance.audit_plan',side_effect=ContextCapacityError('oversized review fixture')):
   result=self.save()
  self.assertTrue(result['ok'],result);value=result['result']
  self.assertEqual(value['current_plan_version'],1);self.assertFalse(value['execution_allowed'])
  self.assertEqual(value['coverage']['status'],'INSUFFICIENT');self.assertTrue(value['coverage']['review_pending'])
  self.assertEqual(len(self.s.plans(self.m)),1);self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.s=MissionStore(self.root);self.m=self.s.create('Observe and report','model','conv',spec={'autonomous':True,'planning_report_steps':True})
  self.r=Registry(Memory(self.root/'runtime/memory.sqlite'),self.root);self.r.mission_store=self.s;self.r.context={'mission_id':self.m}
  self.args={'id':'a','title':'Model chosen task','objective':'Observe real units','depends':[],'tools':['host_service','host_write_file'],'observations':['actual unit status'],'verification':'Review facts against service receipts','recovery':'Diagnose unavailable capability','artifacts':['/project/a.md'],'report_path':'/project/a.md','expected_version':0,'reason':'Initial model step','plan_objective':'Observe and report','plan_success_criteria':['Factual observation report'],'plan_artifacts':['/project/a.md'],'plan_stop_conditions':['Report verified']}
 def save(self,args=None):return self.r.execute('mission_plan_report_step',args or self.args)
 def test_flat_step_preserves_values_and_ordinary_semantic_predicate(self):
  result=self.save();self.assertTrue(result['ok'],result)
  t=self.s.tasks(self.m)[0];self.assertEqual(t['title'],self.args['title']);self.assertEqual(t['state'],'pending')
  self.assertEqual(t['contract'],{'report_path':'/project/a.md','semantic':[{'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/project/a.md'}}}]})
  self.assertFalse(self.s.contract_status(self.m,'a')['all_satisfied'])
  self.assertEqual(self.s.plans(self.m)[0]['author'],'JARVIS')
  self.assertNotIn('mission_plan',[s['function']['name'] for s in self.r.schemas()])
  self.assertIn('mission_plan_report_step',[s['function']['name'] for s in self.r.schemas()])
 def test_append_requires_current_version_and_cannot_change_received_task(self):
  self.assertTrue(self.save()['ok'])
  new={**self.args,'id':'b','depends':['a'],'expected_version':1,'report_path':'/project/b.md','artifacts':['/project/b.md']}
  self.assertTrue(self.save(new)['ok']);self.assertEqual(len(self.s.tasks(self.m)),2)
  self.assertFalse(self.save(new)['ok']);self.assertEqual(len(self.s.plans(self.m)),2)
  with self.s.db() as c:c.execute("UPDATE tasks SET state='validated' WHERE mission=? AND id='a'",(self.m,))
  self.assertFalse(self.save({**self.args,'title':'Weaken received','expected_version':2})['ok'])
  self.assertEqual(self.s.tasks(self.m)[0]['title'],self.args['title'])
 def test_opt_in_and_original_container_decode_keep_types(self):
  args={**self.args,'tools':json.dumps(self.args['tools'])};self.assertTrue(self.save(args)['ok'])
  self.assertIsInstance(self.s.plans(self.m)[0]['plan']['tasks'][0]['tools'],list)
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'autonomous':True}),self.m))
  self.assertNotIn('mission_plan_report_step',[s['function']['name'] for s in self.r.schemas()])
  self.assertFalse(self.save({**self.args,'id':'c','expected_version':1})['ok']);self.assertEqual(len(self.s.plans(self.m)),1)

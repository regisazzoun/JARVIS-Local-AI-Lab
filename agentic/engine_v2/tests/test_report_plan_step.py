"""Real registry/store checks; not evidence of model autonomy."""
import json,tempfile,unittest
from pathlib import Path
from jarvis.tools import Registry
from jarvis.memory import Memory
from jarvis.mission_store import MissionStore
class ReportStepTests(unittest.TestCase):
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

import json,tempfile,unittest
from jsonschema import Draft202012Validator
from jarvis.mission_store import MissionStore
from jarvis.mission_context_budget import ContextBudget,observation_view
from jarvis.operational_policy import observed_policy,service_schemas,observation_arguments
class OperationalPolicyTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.s=MissionStore(self.tmp.name);self.m=self.s.create('Observe services; do not modify them','fixture','conv')
 def policy(self):
  token=self.s.begin_call(self.m,None,'host_policy',{})
  self.s.finish_call(token,{'ok':True,'result':{'services':{'real.service':['is-active']},'write_roots':['/project'],'policy_identity':{'policy_sha256':'a'*64}}},0)
  return token
 def test_policy_survives_compaction_and_unrelated_reads_without_becoming_service_proof(self):
  token=self.policy()
  for i in range(5):
   t=self.s.begin_call(self.m,None,'host_read_file',{'path':'/absent'});self.s.finish_call(t,{'ok':False,'error':'absent'},0)
  before=self.s.attempt_ledger(self.m).snapshot()
  p={'model':'fixture','messages':[{'role':'system','content':'owner policy'},{'role':'user','content':'x'*50000}],'tools':[],'options':{'num_predict':1024}}
  ContextBudget(self.s,self.m).prepare(p,{'limit':16384})
  state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['observed_host_policy']['invocation_id'],token)
  self.assertEqual(state['observed_host_policy']['services'],{'real.service':['is-active']})
  self.assertEqual(state['observed_host_policy']['write_roots'],['/project'])
  self.assertNotIn('state',state['observed_host_policy']);self.assertEqual(before,self.s.attempt_ledger(self.m).snapshot())
 def test_observed_service_names_bind_schema_without_mutating_registry_or_adding_permissions(self):
  self.policy();original=[{'function':{'name':'host_service','parameters':{'type':'object','properties':{'service':{'type':'string'},'action':{'type':'string'}},'required':['service','action']}}}]
  schema=service_schemas(original,observed_policy(self.s,self.m))[0]['function']['parameters']
  self.assertTrue(Draft202012Validator(schema).is_valid({'service':'real.service','action':'is-active'}))
  self.assertFalse(Draft202012Validator(schema).is_valid({'service':'invented.service','action':'is-active'}))
  self.assertNotIn('enum',original[0]['function']['parameters']['properties']['service'])
 def test_rejected_model_proposal_is_a_reference_not_an_observed_fact(self):
  args={'metadata':{'objective':'Fictitious outage'},'tasks':[{'observations':['Invented command failed']}]}
  view=observation_arguments('mission_plan',args)
  self.assertNotIn('Fictitious outage',json.dumps(view));self.assertTrue(view['proposal_is_not_an_execution_observation']);self.assertIn('metadata',args)
 def test_compressed_failed_service_call_retains_exact_target(self):
  o={'id':'receipt','tool':'host_service','arguments':{'service':'invented.service','action':'status'},'result':{'ok':False,'error':'Action/service outside policy'}}
  self.assertEqual(observation_view(o)['parameters'],{'service':'invented.service','action':'status'})
 def test_relocation_never_changes_application_predicates_or_received_proofs(self):
  from jarvis.operational_policy import report_relocation
  with self.s.db() as db:db.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'report_workspace':'/allowed'}),self.m))
  old={'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/invalid/old.md'}}}
  new={'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/allowed/new.md'}}}
  task={'id':'a','state':'pending','contract':{'report_path':'/invalid/old.md'}}
  self.assertTrue(report_relocation(self.s,self.m,task,old,[new]))
  self.assertFalse(report_relocation(self.s,self.m,{**task,'state':'validated'},old,[new]))
  self.assertFalse(report_relocation(self.s,self.m,task,{**old,'kind':'json'},[new]))
  self.s.event(self.m,'semantic_verification','a',result={'status':'PASS','contract':old})
  self.assertFalse(report_relocation(self.s,self.m,task,old,[new]))
 def test_planning_view_preserves_exact_goal_plan_and_counters_without_rejected_proposal(self):
  from jarvis.operational_policy import planning_state
  self.policy();self.s.plan(self.m,[{'id':'a','title':'Model selected task','objective':'Observe services'}])
  rejected=self.s.begin_call(self.m,None,'mission_plan',{'metadata':{'objective':'Invented service outage'}})
  self.s.finish_call(rejected,{'ok':False,'error':'Malformed plan; no operation executed'},0)
  before=self.s.attempt_ledger(self.m).snapshot()
  state=planning_state(self.s,self.m,{'host_service':None},[])
  self.assertEqual(state['owner_goal'],self.s.get(self.m)['goal'])
  self.assertEqual(state['current_plan_proposal'],self.s.plans(self.m)[-1]['plan'])
  self.assertEqual(state['latest_tool_result']['invocation_id'],rejected)
  self.assertNotIn('Invented service outage',json.dumps(state))
  self.assertEqual(before,self.s.attempt_ledger(self.m).snapshot())
 def test_execution_can_revise_a_flat_plan_with_the_interface_named_in_its_instructions(self):
  from jarvis.durable_cycle import task_schemas
  schemas=[{'function':{'name':name}} for name in ['host_service','mission_plan_report_step','unselected']]
  offered=task_schemas(schemas,{'tools':['host_service']})
  self.assertEqual([x['function']['name'] for x in offered],['host_service','mission_plan_report_step'])
 def test_capacity_refusal_reopens_planning_not_execution_and_is_not_blindly_retried(self):
  from types import SimpleNamespace
  from unittest.mock import patch
  from jarvis.mission_assurance import ensure_plan_review,coverage_state
  from jarvis.mission_context_budget import ContextCapacityError
  self.s.plan(self.m,[{'id':'a','title':'Model plan'}])
  registry=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m})
  with patch('jarvis.mission_assurance.audit_plan',side_effect=ContextCapacityError('fixture too large')) as review:
   first=ensure_plan_review(registry);second=ensure_plan_review(registry)
  self.assertEqual(review.call_count,1)
  self.assertEqual((first['status'],second['status']),('INSUFFICIENT','INSUFFICIENT'))
  self.assertFalse(coverage_state(self.s,self.m)['accepted'])
  self.assertEqual(len(self.s.plans(self.m)),1)
  self.s.plan(self.m,[{'id':'a','title':'Model reduced plan'}],expected_version=1)
  with patch('jarvis.mission_assurance.audit_plan',return_value={'status':'PASS','software_fixture':True}) as review:
   self.assertEqual(ensure_plan_review(registry)['status'],'PASS')
  self.assertEqual(review.call_count,1)
 def test_predispatch_rejection_and_workspace_survive_phase_rebuild_and_compaction(self):
  from jarvis.operational_policy import planning_state
  with self.s.db() as db:db.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'report_workspace':'/reports/this-mission'}),self.m))
  error='arguments/report_path must match /reports/this-mission/'
  ref=self.s.event(self.m,'structured_action_rejected',result={'error':error,'model_output':{'content':'untrusted rejected draft'}})
  state=planning_state(self.s,self.m,{'host_policy':None},[])
  self.assertEqual(state['planning_feedback']['interface_rejection']['error'],error)
  self.assertEqual(state['report_workspace'],'/reports/this-mission')
  self.assertNotIn('untrusted rejected draft',json.dumps(state))
  p={'model':'fixture','messages':[{'role':'system','content':'owner policy'},{'role':'user','content':'x'*50000}],'tools':[],'options':{'num_predict':1024}}
  ContextBudget(self.s,self.m).prepare(p,{'limit':16384})
  active=json.loads(p['messages'][1]['content']);active=active.get('operational_state',active)
  self.assertEqual(active['planning_feedback']['interface_rejection']['reference'],ref)
  self.assertEqual(active['planning_feedback']['interface_rejection']['error'],error)
  self.assertEqual(active['report_workspace'],'/reports/this-mission')
 def test_read_only_snapshot_offers_only_unread_permitted_pairs(self):
  from jarvis.operational_policy import unread_service_schemas
  policy={'services':{'a.service':['is-active','is-enabled','restart'],'b.service':['is-active']}}
  base=[{'function':{'name':'host_service','description':'Actual service','parameters':{'type':'object','properties':{'service':{'type':'string'},'action':{'type':'string'}},'required':['service','action'],'additionalProperties':False}}}]
  offered=unread_service_schemas(base,policy,{'a.service':{'is-active':{'observed_text':'inactive'}}})
  validator=Draft202012Validator(offered[0]['function']['parameters'])
  self.assertFalse(validator.is_valid({'service':'a.service','action':'is-active'}))
  self.assertTrue(validator.is_valid({'service':'a.service','action':'is-enabled'}))
  self.assertTrue(validator.is_valid({'service':'b.service','action':'is-active'}))
  self.assertFalse(validator.is_valid({'service':'a.service','action':'restart'}))
  self.assertNotIn('oneOf',base[0]['function']['parameters'])
 def test_observed_inactive_is_retained_as_nonzero_output_not_fake_success(self):
  from jarvis.operational_policy import observed_service_reads
  t=self.s.begin_call(self.m,None,'host_service',{'service':'a.service','action':'is-active'})
  self.s.finish_call(t,{'ok':True,'result':{'returncode':3,'stdout':'inactive\n'}},0)
  read=observed_service_reads(self.s,self.m)['a.service']['is-active']
  self.assertEqual(read['returncode'],3);self.assertEqual(read['observed_text'],'inactive');self.assertEqual(read['invocation'],t)
  self.assertNotIn('status',read)
  self.s.event(self.m,'service_observation_recheck_requested',actor='Codex',result={'reason':'Changed external state requires a new snapshot'})
  self.assertEqual(observed_service_reads(self.s,self.m),{})
 def test_snapshot_removes_service_tool_when_all_pairs_already_observed(self):
  from jarvis.operational_policy import unread_service_schemas
  base=[{'function':{'name':'host_service','description':'service','parameters':{}}},{'function':{'name':'host_write_file'}}]
  offered=unread_service_schemas(base,{'services':{'a.service':['is-active']}},{'a.service':{'is-active':{'observed_text':'active'}}})
  self.assertEqual([x['function']['name'] for x in offered],['host_write_file'])
 def test_receipt_timestamp_is_formatted_with_real_paris_dst(self):
  from jarvis.operational_policy import observed_service_reads
  for stamp,expected in [(1735689600,'2025-01-01T01:00:00+01:00'),(1751328000,'2025-07-01T02:00:00+02:00')]:
   t=self.s.begin_call(self.m,None,'host_service',{'service':'a.service','action':'is-active'})
   self.s.finish_call(t,{'ok':True,'result':{'returncode':0,'stdout':'active\n'}},0)
   with self.s.db() as db:db.execute('UPDATE tool_calls SET created=? WHERE id=?',(stamp,t))
   self.assertEqual(observed_service_reads(self.s,self.m)['a.service']['is-active']['observed_at_iso'],expected)
 def test_report_projection_keeps_negative_state_without_a_functional_pass(self):
  from jarvis.mission_reporting import service_observation
  for action,code,text in [('is-active',3,'inactive\n'),('is-enabled',1,'disabled\n')]:
   facts=service_observation({'service':'a.service','action':action},{'ok':True,'result':{'returncode':code,'stdout':text}})
   self.assertEqual(facts['observed_state_text'],text.strip());self.assertEqual(facts['observed_returncode'],code)
   self.assertNotIn('status',facts)
  self.assertIsNone(service_observation({'service':'a.service','action':'show'},{'ok':True,'result':{'returncode':1,'stdout':'error'}}))
 def test_new_report_reference_contract_survives_model_projection(self):
  from jarvis.durable_cycle import model_observation
  payload={'mission':'fixture','actions':[],'plans':[],'tasks':[],'semantic_verifications':[],'codex_interventions':[],'scope':'Predicates only; fixture','report_reference_contract':{'eligible_technical_references':['real-receipt']}}
  view=model_observation({'ok':True,'result':payload})
  self.assertEqual(view['result']['report_reference_contract'],payload['report_reference_contract'])
 def test_snapshot_fact_cache_refreshes_for_new_observations_but_not_report_writes(self):
  from jarvis.durable_cycle import facts_match_current_task
  with self.s.db() as db:db.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'read_only_service_snapshot':True}),self.m))
  self.s.plan(self.m,[{'id':'a','title':'observe','contract':{'report_path':'/report.md'}}])
  def record(tool,args,result):
   t=self.s.begin_call(self.m,'a',tool,args);self.s.finish_call(t,result,0);return t
  record('mission_report_facts',{}, {'ok':True,'result':{'old_format':True}})
  self.assertFalse(facts_match_current_task(self.s,self.m,'a'))
  record('mission_report_facts',{}, {'ok':True,'result':{'report_reference_contract':{'eligible_technical_references':[]}}})
  self.assertTrue(facts_match_current_task(self.s,self.m,'a'))
  record('host_service',{'service':'a.service','action':'is-active'},{'ok':True,'result':{'returncode':0,'stdout':'active\n'}})
  self.assertFalse(facts_match_current_task(self.s,self.m,'a'))
  record('mission_report_facts',{}, {'ok':True,'result':{'report_reference_contract':{'eligible_technical_references':['receipt']}}})
  record('host_write_file',{'path':'/report.md'},{'ok':True,'result':{'returncode':0}})
  self.assertTrue(facts_match_current_task(self.s,self.m,'a'))
 def test_reference_eligibility_contract_survives_compaction_of_a_snapshot(self):
  with self.s.db() as db:db.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'read_only_service_snapshot':True}),self.m))
  ref=self.s.begin_call(self.m,None,'mission_report_facts',{})
  contract={'eligible_technical_references':['service-receipt'],'context_only_references':['policy-receipt']}
  self.s.finish_call(ref,{'ok':True,'result':{'report_reference_contract':contract}},0)
  p={'model':'fixture','messages':[{'role':'system','content':'owner policy'},{'role':'user','content':'x'*50000}],'tools':[],'options':{'num_predict':1024}}
  ContextBudget(self.s,self.m).prepare(p,{'limit':16384})
  active=json.loads(p['messages'][1]['content']);active=active.get('operational_state',active)
  self.assertEqual(active['report_reference_contract'],{'source_invocation':ref,**contract})
if __name__=='__main__':unittest.main()

 def test_stale_report_facts_are_a_read_prerequisite_before_another_write(self):
  from jarvis.durable_cycle import report_refresh_tools
  offered=report_refresh_tools({'host_write_file','host_service','mission_verify','mission_note','mission_block'})
  self.assertEqual(offered,{'mission_report_facts','mission_note','mission_block'})
  self.assertNotIn('host_write_file',offered)
  self.assertEqual(report_refresh_tools(set()),{'mission_report_facts'})

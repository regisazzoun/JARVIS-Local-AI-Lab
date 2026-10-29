"""Actual registry contract regression: no inference or remote execution claim."""
import json,tempfile,unittest
from pathlib import Path
from jsonschema import Draft202012Validator
from jarvis.core import Core,ROOT
from jarvis.memory import Memory
from jarvis.mission_store import MissionStore

class ExecutionContractTests(unittest.TestCase):
 def setUp(self):
  self.folder=tempfile.TemporaryDirectory();self.addCleanup(self.folder.cleanup)
  root=Path(self.folder.name);self.store=MissionStore(root)
  self.m=self.store.create('bounded audit','model','conv',spec={'distributed_authority':True,'authority_requirements':['AUDIT'],'authority_readonly_validation':True})
  config=json.loads((ROOT/'config/example.json').read_text());self.reg=Core(config,Memory(root/'memory.sqlite')).tools
  self.reg.mission_store=self.store;self.reg.context={'mission_id':self.m,'task_id':'audit'}
 def errors(self,args):return list(Draft202012Validator(self.reg.active_schema('authority_work')).iter_errors(args))
 def test_execution_without_executor_or_command_is_invalid_in_advertised_schema(self):
  args={'issue':'AUDIT','kind':'inspect','summary':'Actual observed missing fields','operation_id':'first'}
  self.assertTrue(self.errors(args));args['executor']='Dell1';self.assertTrue(self.errors(args));args['command']='';self.assertTrue(self.errors(args))
  args['command']='python3 -V';self.assertFalse(self.errors(args))
 def test_accept_still_requires_references_without_requiring_a_command(self):
  args={'issue':'AUDIT','kind':'accept','summary':'provenance','operation_id':'accept','reference':1,'source_reference':2}
  self.assertFalse(self.errors(args));args.pop('reference');self.assertTrue(self.errors(args))
 def test_owner_execution_phase_exposes_only_concrete_execution_modes(self):
  with self.store.db() as c:
   spec=json.loads(self.store.get(self.m)['spec']);spec['authority_execution_only']=True
   c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  args={'issue':'AUDIT','kind':'test','summary':'bounded test','operation_id':'run','executor':'Dell2','command':'python3 -V'}
  self.assertFalse(self.errors(args));args['kind']='accept';self.assertTrue(self.errors(args))

 def test_plan_revision_advertises_exact_current_version_not_next_version(self):
  self.store.plan(self.m,[{'id':'audit','title':'initial'}],author='fixture')
  schema=self.reg.active_schema('authority_revise_plan')
  args={'steps':[{'id':'audit','title':'reception lot','depends':[],'issues':['AUDIT']}],'expected_version':1,'reason':'changed source requires integration'}
  self.assertFalse(list(Draft202012Validator(schema).iter_errors(args)))
  args['expected_version']=2
  self.assertTrue(list(Draft202012Validator(schema).iter_errors(args)))
  self.assertIn('expected_version',schema['required'])

 def test_plan_schema_refreshes_after_persisted_revision(self):
  self.store.plan(self.m,[{'id':'audit','title':'initial'}],author='fixture')
  self.store.plan(self.m,[{'id':'audit','title':'revised'}],author='fixture',expected_version=1,reason='new evidence')
  schema=self.reg.active_schema('authority_revise_plan')
  self.assertEqual(schema['properties']['expected_version']['const'],2)
  self.assertEqual(len(self.store.plans(self.m)),2)

 def test_focused_source_unit_advertises_real_module_and_symbol(self):
  with self.store.db() as c:
   spec=json.loads(self.store.get(self.m)['spec']);spec['authority_draft_units']=[{'path':'engine/jarvis/mission_assurance.py','symbol':'audit_plan'}]
   c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  schema=self.reg.active_schema('authority_draft_edit')
  args={'issue':'AUDIT','executor':'Dell2','path':'engine/jarvis/mission_assurance.py','symbol':'audit_plan','request':'Model chooses the correction'}
  self.assertFalse(list(Draft202012Validator(schema).iter_errors(args)))
  args['path']='engine/audit_plan.py';self.assertTrue(list(Draft202012Validator(schema).iter_errors(args)))
  args['path']='engine/jarvis/mission_assurance.py';args.pop('symbol');self.assertTrue(list(Draft202012Validator(schema).iter_errors(args)))

 def test_apply_schema_only_offers_real_same_task_model_proposals(self):
  own=self.store.event(self.m,'authority_code_proposal','audit',actor='JARVIS/Qwen80B',result={'fixture':True})
  self.store.event(self.m,'authority_code_proposal','other',actor='JARVIS/Qwen80B',result={'fixture':True})
  self.store.event(self.m,'authority_code_proposal','audit',actor='Codex',result={'fixture':True})
  schema=self.reg.active_schema('authority_apply_draft')
  self.assertEqual(schema['properties']['proposal_reference']['enum'],[own])

 def test_sync_schema_binds_execution_reference_to_current_host_source(self):
  state={'issues':{},'syncs':[],'executions':{'1':{'host':'Dell1','after':{'x':'old'}},'2':{'host':'Dell1','after':{'x':'new'}},'3':{'host':'Dell2','after':{'x':'peer'}}}}
  self.store.event(self.m,'authority_state',result=state)
  schema=self.reg.active_schema('authority_sync')
  args={'issue':'AUDIT','source':'Dell1','destination':'Dell2','source_reference':2,'files':['x'],'summary':'model chooses sync'}
  self.assertFalse(list(Draft202012Validator(schema).iter_errors(args)))
  for bad in (1,3,123456):
   args['source_reference']=bad;self.assertTrue(list(Draft202012Validator(schema).iter_errors(args)))
  args.update(source='Dell2',destination='Dell1',source_reference=3)
  self.assertFalse(list(Draft202012Validator(schema).iter_errors(args)))

 def test_declared_probe_replaces_free_test_command_in_outer_schema(self):
  with self.store.db() as c:
   spec=json.loads(self.store.get(self.m)['spec']);spec['authority_probes']={'coverage':{'argv':['python3','probe.py'],'sources':{},'description':'owner regression'}}
   c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  schema=self.reg.active_schema('authority_run_probe')
  args={'issue':'AUDIT','probe_id':'coverage','executor':'Dell2','summary':'model selects supplied control'}
  self.assertFalse(list(Draft202012Validator(schema).iter_errors(args)))
  args['probe_id']='guessed';self.assertTrue(list(Draft202012Validator(schema).iter_errors(args)))
  self.assertNotIn('test',self.reg.active_schema('authority_work')['properties']['kind']['enum'])
  self.reg.context['_authority_declared_probe']={'parent':'internal-fixture'}
  self.assertIn('test',self.reg.active_schema('authority_work')['properties']['kind']['enum'])

 def declared_progress_fixture(self):
  from jarvis.authority_probe import declaration_digest
  spec=json.loads(self.store.get(self.m)['spec']);spec.update(authority_probes={'core':{'argv':['core'],'sources':{}},'variable':{'argv':['var'],'sources':{}}},authority_code_focus=True)
  with self.store.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  manifest={'app.py':'new'}
  state={'issues':{},'syncs':[],'executions':{'1':{'host':'Dell1','kind':'correct','before':{'app.py':'old'},'after':manifest,'execution':{'returncode':0}}}}
  def add(ref,host,key):
   state['executions'][str(ref)]={'host':host,'kind':'test','probe_id':key,'probe_declaration_sha256':declaration_digest(spec['authority_probes'][key]),'before':manifest,'after':manifest,'execution':{'returncode':0}}
   self.store.event(self.m,'authority_state',result=state)
  return state,add

 def test_probe_schema_excludes_already_passed_pair_at_exact_version(self):
  state,add=self.declared_progress_fixture();add(2,'Dell1','core')
  schema=self.reg.active_schema('authority_run_probe');args={'issue':'AUDIT','probe_id':'core','executor':'Dell1','summary':'choose missing control'}
  self.assertTrue(list(Draft202012Validator(schema).iter_errors(args)))
  args['executor']='Dell2';self.assertFalse(list(Draft202012Validator(schema).iter_errors(args)))
  args.update(probe_id='variable',executor='Dell1');self.assertFalse(list(Draft202012Validator(schema).iter_errors(args)))
  add(3,'Dell2','core');self.assertEqual(self.reg.active_schema('authority_run_probe')['properties']['probe_id']['enum'],['variable'])

 def test_readonly_declared_accept_schema_requires_passed_tests_on_other_peer(self):
  state,add=self.declared_progress_fixture()
  for ref,host,key in [(2,'Dell1','core'),(3,'Dell2','core'),(4,'Dell1','variable'),(5,'Dell2','variable')]:add(ref,host,key)
  args={'issue':'AUDIT','kind':'accept','summary':'same code, both declared probes','operation_id':'fixture','reference':5,'source_reference':4}
  self.assertFalse(self.errors(args))
  from jarvis.structured_actions import request,response
  schema=self.reg.active_schema('authority_work')
  self.assertIn('reference',schema['required'])
  self.assertIn('source_reference',schema['required'])
  payload,transport=request({'messages':[{'role':'system','content':'fixture'}],'tools':[{'type':'function','function':{'name':'authority_work','parameters':schema}}]})
  self.assertEqual(response({'content':json.dumps({'tool':'authority_work','arguments':args})},transport)['tool_calls'][0]['function']['arguments'],args)
  missing=dict(args);missing.pop('reference')
  with self.assertRaises(ValueError):response({'content':json.dumps({'tool':'authority_work','arguments':missing})},transport)
  args['source_reference']=1;self.assertTrue(self.errors(args),'A correction receipt is not a passed test in read-only mode')
  args['source_reference']=3;self.assertTrue(self.errors(args),'The same host is not an independent peer')

 def test_declared_acceptance_uses_native_call_and_existing_acceptance_gates(self):
  from unittest.mock import patch
  from jarvis.authority_identity import invocation_scope
  from jarvis.distributed_authority import Authority
  state,add=self.declared_progress_fixture()
  for ref,host,key in [(2,'Dell1','core'),(3,'Dell2','core'),(4,'Dell1','variable'),(5,'Dell2','variable')]:add(ref,host,key)
  for row in state['executions'].values():row['issue']='AUDIT'
  state['issues']={'AUDIT':{'failed_cycles':0,'delegation_failures':0}};state['operations']={}
  self.store.event(self.m,'authority_state',result=state)
  with self.store.db() as c:
   spec=json.loads(self.store.get(self.m)['spec']);spec['authority_engine_operation_ids']=True;c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  args={'issue':'AUDIT','validator':'Dell2','summary':'Actual recorded software fixture observations'}
  self.store.event(self.m,'inference_finished',result={'software_fixture_only':True,'metrics':{'node':'Dell1','effective_model':'qwen3-coder-next:q4_K_M'}})
  token=self.store.begin_call(self.m,'audit','authority_accept_probes',args)
  with invocation_scope(token),patch.object(Authority,'source_manifest',return_value={'app.py':'new'}):
   result=self.reg.execute('authority_accept_probes',args)
  self.assertTrue(result['ok'],result);self.assertEqual(result['result']['resolved_source_reference'],4)
  self.assertEqual(Authority(self.reg).state()['issues']['AUDIT']['accepted']['test'],'5')
  self.assertTrue(any(row['kind']=='authority_probe_acceptance_bound' for row in self.store.events(self.m)))

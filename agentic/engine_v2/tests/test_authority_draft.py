"""Software fixtures, not evidence of autonomous model execution."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from jarvis.mission_store import MissionStore
from jarvis.distributed_authority import Authority
from jarvis.authority_draft import draft, apply_draft
from jarvis.authority_identity import invocation_scope


class FocusedDraftTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.path=self.root/'engine/worker.py';self.path.parent.mkdir();self.original='def run():\n return 1\n';self.path.write_text(self.original)
  self.s=MissionStore(self.root/'store');self.m=self.s.create('FULL_PARENT_MISSION_CONTRACT','model','conv',spec={'distributed_authority':True,'authority_engine_operation_ids':True,'authority_requirements':['Q1']})
  self.s.event(self.m,'inference_finished','task',result={'metrics':{'node':'Dell1','effective_model':'qwen3-coder-next:q4_K_M'},'software_fixture':True})
  self.s.event(self.m,'working_note','task',result={'content':'SECRET_PARENT_HISTORY not needed for coding'})
  self.metrics=[];self.payloads=[];self.reply={'new_content':'def run():\n return 2\n','rationale':'fixture changed behavior'};self.node='Dell1'
  self.reg=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'task'},config={'hybrid_compute':{'routes':{'mission':['Dell1']},'nodes':{'Dell1':{'enabled':True,'hard_context_limit':32768}}}},assurance_transport=self.send)
  self.a=Authority(self.reg);self.remote_calls=[];self.a.remote=self.remote
 def send(self,payload):
  self.payloads.append(payload);self.metrics.append({'node':self.node,'effective_model':'qwen3-coder-next:q4_K_M','software_fixture':True})
  return {'content':json.dumps(self.reply)}
 def remote(self,host,command):
  self.remote_calls.append((host,command))
  r=subprocess.run(command,cwd=self.root,shell=True,text=True,capture_output=True)
  return {'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr},'software-source-read'
 def args(self):return {'issue':'Q1','executor':'Dell2','path':'engine/worker.py','request':'Change the return value to two','context':'keep run callable'}
 def call(self,args=None):
  args=args or self.args();token=self.s.begin_call(self.m,'task','authority_draft_edit',args)
  try:
   with invocation_scope(token):result=draft(self.a,args)
  except Exception as exc:
   self.s.finish_call(token,{'ok':False,'error':str(exc)},0);raise
  self.s.finish_call(token,{'ok':True,'result':result},0);return result
 def test_small_fresh_proposal_has_exact_anchor_but_never_writes_or_tests(self):
  result=self.call();self.assertFalse(result['applied']);self.assertFalse(result['tested'])
  self.assertEqual(self.path.read_text(),self.original)
  record=next(e for e in self.s.events(self.m) if e['id']==result['proposal_reference'])
  self.assertEqual(record['result']['proposal']['edits'][0]['old'],self.original)
  payload=json.dumps(self.payloads[0]);self.assertNotIn('FULL_PARENT_MISSION_CONTRACT',payload);self.assertNotIn('SECRET_PARENT_HISTORY',payload);self.assertNotIn('tools',self.payloads[0])
  self.assertEqual(json.loads(self.payloads[0]['messages'][1]['content'])['context_result_objective']['total_context_tokens_max'],32768)
  self.assertEqual(self.remote_calls[0][0],'Dell2');self.assertEqual(result['executor'],'Dell2')
  events=self.s.events(self.m);proposal=next(e for e in events if e['kind']=='authority_code_proposal')
  self.assertEqual(proposal['actor'],'JARVIS/Qwen80B');self.assertFalse(proposal['result']['applied'])
 def test_symbol_proposal_edits_real_function_inside_large_module_only(self):
  prefix='"'+('unchanged documentation '*400)+'"\n'
  suffix='\ndef other():\n return 99\n'
  self.path.write_text(prefix+self.original+suffix)
  proposal=self.call({**self.args(),'symbol':'run'})
  payload=json.loads(self.payloads[0]['messages'][1]['content'])
  self.assertEqual(payload['file']['source'],self.original)
  self.assertEqual(payload['file']['symbol'],'run')
  self.assertNotIn(prefix,json.dumps(self.payloads[0]))
  result=self.apply(proposal['proposal_reference'])
  self.assertTrue(result['applied'])
  self.assertEqual(self.path.read_text(),prefix+self.reply['new_content']+suffix)
 def test_changed_function_may_grow_beyond_old_whole_file_limit(self):
  self.original='def run():\n "'+('bounded function text '*340)+'"\n return 1\n';self.path.write_text(self.original)
  self.assertGreater(len(self.original.encode()),6000)
  self.reply['new_content']=self.original.replace('return 1','return 2')
  result=self.call({**self.args(),'symbol':'run'})
  self.assertTrue(self.apply(result['proposal_reference'])['applied'])
 def test_missing_ambiguous_or_renamed_symbol_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'Source read not received'):
   self.call({**self.args(),'symbol':'missing'})
  self.path.write_text(self.original+self.original)
  with self.assertRaisesRegex(ValueError,'Source read not received'):
   self.call({**self.args(),'symbol':'run'})
  self.path.write_text(self.original);self.reply['new_content']='def renamed():\n return 2\n'
  with self.assertRaisesRegex(ValueError,'retain the selected'):
   self.call({**self.args(),'symbol':'run'})
 def test_decorated_symbol_and_template_words_in_path_preserved(self):
  self.path=self.root/'engine/PATH_SYMBOL.py'
  self.original='@staticmethod\ndef run():\n return 1\n';self.path.write_text(self.original)
  self.reply['new_content']='@staticmethod\ndef run():\n return 2\n'
  result=self.call({**self.args(),'path':'engine/PATH_SYMBOL.py','symbol':'run'})
  self.assertTrue(self.apply(result['proposal_reference'])['applied'])
  self.assertEqual(self.path.read_text(),self.reply['new_content'])
 def test_declared_source_unit_rejects_invented_filename_before_remote(self):
  self.a.spec['authority_draft_units']=[{'path':'engine/worker.py','symbol':'run'}]
  with self.assertRaisesRegex(ValueError,'observed source unit'):
   self.call({**self.args(),'path':'engine/run.py','symbol':'run'})
  self.assertFalse(self.remote_calls)
 def test_coding_phase_does_not_order_an_unoffered_inspection_tool(self):
  from jarvis.durable_cycle import focused_source_prompt
  original='Owner policy. Première obligation : observe les sources avec authority_work kind=inspect avant de planifier; choisis toi-même la machine et la commande.'
  result=focused_source_prompt(original)
  self.assertTrue(result.startswith('Owner policy.'))
  self.assertNotIn('authority_work kind=inspect',result)
  self.assertIn('authority_draft_edit',result);self.assertIn('sans application ni test',result)
 def test_real_correction_or_failed_test_does_not_restart_initial_inspection(self):
  from jarvis.durable_cycle import source_preparation_observed
  self.assertFalse(source_preparation_observed({'executions':{'1':{'kind':'analyze','summary':'source observed'}}}))
  for kind,code in [('correct',0),('test',1)]:
   self.assertTrue(source_preparation_observed({'executions':{'1':{'kind':kind,'execution':{'returncode':code},'before':{},'after':{}}}}))
  self.assertFalse(source_preparation_observed({'executions':{'1':{'kind':'correct','execution':{},'before':{},'after':{}}}}))
 def test_result_contract_survives_isolated_drafting_and_rejects_style_only(self):
  self.a.spec['authority_coding_objective']='Actual owner outcome: bounded semantic coverage with complete evidence'
  self.a.spec['authority_behavioral_change']=True
  self.call()
  facts=json.loads(self.payloads[-1]['messages'][1]['content'])
  self.assertEqual(facts['owner_result_contract'],self.a.spec['authority_coding_objective'])
  self.reply['new_content']=self.original.rstrip()+'\n\n'
  with self.assertRaisesRegex(ValueError,'formatting/newline-only'):self.call()
 def test_bare_action_word_is_not_a_delegated_code_objective(self):
  self.a.spec['authority_coding_objective']='Preserve required behavior in the actual function'
  with self.assertRaisesRegex(ValueError,'actual code change'):self.call({**self.args(),'request':'apply'})
  self.assertFalse(self.remote_calls);self.assertFalse(self.payloads)
 def test_failed_test_restores_short_coding_phase_until_new_correction(self):
  from jarvis.durable_cycle import coding_focus_required,candidate_test_focus
  spec={'authority_code_focus':True};state={'executions':{}}
  self.assertTrue(coding_focus_required(spec,state))
  state['executions']['10']={'kind':'correct','execution':{'returncode':0},'before':{'x':'a'},'after':{'x':'b'}}
  self.assertFalse(coding_focus_required(spec,state));self.assertTrue(candidate_test_focus(spec,state))
  state['executions']['11']={'kind':'test','execution':{'returncode':1}}
  self.assertTrue(coding_focus_required(spec,state));self.assertFalse(candidate_test_focus(spec,state))
  state['executions']['12']={'kind':'correct','execution':{'returncode':0},'before':{'x':'b'},'after':{'x':'c'}}
  self.assertFalse(coding_focus_required(spec,state));self.assertTrue(candidate_test_focus(spec,state))
 def test_preexisting_style_proposal_cannot_be_applied_to_behavioral_task(self):
  self.reply['new_content']=self.original+'\n'
  proposal=self.call();self.a.spec['authority_behavioral_change']=True
  with self.assertRaisesRegex(ValueError,'ineligible'):self.apply(proposal['proposal_reference'])
  self.assertEqual(self.path.read_text(),self.original)
 def test_requires_canonical_call_before_source_read(self):
  with self.assertRaisesRegex(ValueError,'canonical started'):draft(self.a,self.args())
  self.assertFalse(self.remote_calls);self.assertFalse(self.payloads)
 def test_different_request_and_reopened_store_cannot_create_fourth_draft(self):
  for n in range(3):self.call({**self.args(),'request':'Change two, revision '+str(n)})
  self.a.store=MissionStore(self.root/'store')
  with self.assertRaisesRegex(ValueError,'Three focused drafts'):self.call({**self.args(),'request':'Different wording'})
  self.assertEqual(len(self.payloads),3);self.assertEqual(self.path.read_text(),self.original)
 def test_source_escape_and_reserved_paths_are_refused_before_inference(self):
  for path in ['../outside.py','/etc/no.py','runtime/worker.py']:
   with self.assertRaisesRegex(ValueError,'Source read not received'):self.call({**self.args(),'path':path})
  self.assertFalse(self.payloads)
 def test_invalid_or_unchanged_proposals_are_not_received(self):
  for content in ['def broken(',self.original]:
   self.reply['new_content']=content
   with self.assertRaises((SyntaxError,ValueError)):self.call()
  self.assertFalse(any(e['kind']=='authority_code_proposal' for e in self.s.events(self.m)))
  self.assertEqual(self.path.read_text(),self.original)
 def test_wrong_inference_machine_is_not_attributed_or_applied(self):
  self.node='Mac-mini'
  with self.assertRaisesRegex(ValueError,'identity not observed'):self.call()
  self.assertFalse(any(e['kind']=='authority_code_proposal' for e in self.s.events(self.m)))
 def test_existing_correction_limit_still_blocks_fresh_context(self):
  state=self.a.state();state['issues']['Q1']={'failed_cycles':3,'delegation_failures':0};self.a.save(state)
  with self.assertRaisesRegex(ValueError,'trois cycles'):self.call()
  self.assertFalse(self.payloads);self.assertFalse(self.remote_calls)

 def apply(self,reference):
  from jarvis.distributed_authority import edit_program
  def execute(name,args):
   self.assertEqual(name,'authority_edit')
   before=self.path.read_bytes()
   r=subprocess.run(['python3','-c',edit_program(args['edits'],allow_workspace_absolute=True)],cwd=self.root,capture_output=True,text=True)
   return {'ok':True,'result':{'actual_changed_files':['engine/worker.py'] if self.path.read_bytes()!=before else [],'execution':{'returncode':r.returncode,'stderr':r.stderr}}}
  self.reg.execute=execute
  args={'proposal_reference':reference};token=self.s.begin_call(self.m,'task','authority_apply_draft',args)
  try:
   with invocation_scope(token):return apply_draft(self.a,args)
  finally:self.s.finish_call(token,{'ok':True},0)
 def test_apply_reference_changes_real_source_once_without_claiming_a_test(self):
  proposal=self.call();result=self.apply(proposal['proposal_reference'])
  self.assertTrue(result['applied']);self.assertFalse(result['tested'])
  self.assertEqual(self.path.read_text(),self.reply['new_content'])
  again=self.apply(proposal['proposal_reference']);self.assertTrue(again['cached'])
  self.assertEqual(len([e for e in self.s.events(self.m) if e['kind']=='authority_code_proposal_applied']),1)
 def test_stale_source_anchor_refuses_write_without_promoting_success(self):
  proposal=self.call();self.path.write_text('def run(): return 99\n')
  result=self.apply(proposal['proposal_reference'])
  self.assertFalse(result['applied']);self.assertFalse(result['tested']);self.assertEqual(result['returncode'],1)
  self.assertEqual(self.path.read_text(),'def run(): return 99\n')
 def test_apply_foreign_task_proposal_is_refused(self):
  proposal=self.call();self.reg.context['task_id']='other';other=Authority(self.reg)
  args={'proposal_reference':proposal['proposal_reference']};token=self.s.begin_call(self.m,'other','authority_apply_draft',args)
  with invocation_scope(token),self.assertRaisesRegex(ValueError,'exact mission/task'):apply_draft(other,args)

 def test_coding_focus_ends_only_after_actual_successful_correction(self):
  from jarvis.durable_cycle import coding_focus_required
  spec={'authority_code_focus':True,'authority_code_focus_since':10}
  def state(kind,rc,before,after,ref='11'):
   return {'executions':{ref:{'kind':kind,'execution':{'returncode':rc},'before':before,'after':after}}}
  self.assertTrue(coding_focus_required(spec,state('test',0,{'f':'a'},{'f':'a'})))
  self.assertTrue(coding_focus_required(spec,state('correct',1,{'f':'a'},{'f':'b'})))
  self.assertTrue(coding_focus_required(spec,state('correct',0,{'f':'a'},{'f':'a'})))
  self.assertTrue(coding_focus_required(spec,state('correct',0,{'f':'a'},{'f':'b'},'9')))
  self.assertFalse(coding_focus_required(spec,state('correct',0,{'f':'a'},{'f':'b'})))
  self.assertFalse(coding_focus_required({},{}))

 def test_compact_reference_mode_exposes_targeted_recall_without_changing_legacy(self):
  from jarvis.durable_cycle import semantic_reference_schemas
  schemas=[{'function':{'name':name,'parameters':{}}} for name in ['authority_work','context_recall','context_checkpoint']]
  self.assertEqual([s['function']['name'] for s in semantic_reference_schemas(schemas,None)],['authority_work'])
  self.assertEqual([s['function']['name'] for s in semantic_reference_schemas(schemas,None,preserve_recall=True)],['authority_work','context_recall'])
  self.assertEqual(len(schemas),3)

 def test_test_focus_preserves_model_choice_and_restores_coding_after_failed_test(self):
  from jarvis.durable_cycle import candidate_test_focus
  spec={'authority_code_focus':True,'authority_code_focus_since':10}
  state={'executions':{'11':{'kind':'correct','before':{'worker':'old'},'after':{'worker':'new'},'execution':{'returncode':0}}}}
  self.assertTrue(candidate_test_focus(spec,state))
  state['executions']['12']={'kind':'test','execution':{'returncode':0}}
  self.assertTrue(candidate_test_focus(spec,state))
  state['executions']['13']={'kind':'test','execution':{'returncode':1}}
  self.assertFalse(candidate_test_focus(spec,state))
  self.assertFalse(candidate_test_focus({},state))

 def test_periodic_guidance_requires_explicit_child_authorization(self):
  from jarvis.durable_cycle import coordinator_guidance
  self.s.event(self.m,'coordinator_instruction','task','Codex-periodic',result={'instruction':'authorized support only'})
  self.assertEqual(coordinator_guidance(self.s,self.m,'task'),[])
  spec=json.loads(self.s.get(self.m)['spec']);spec['coordinator_periodic_authorized']=True
  with self.s.db() as c:c.execute('update missions set spec=? where id=?',(json.dumps(spec),self.m))
  self.assertEqual(len(coordinator_guidance(self.s,self.m,'task')),1)

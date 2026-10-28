import unittest,tempfile,json,copy
from pathlib import Path
from unittest.mock import patch
from jarvis.mission_store import MissionStore
from jarvis.mission_context_budget import ContextBudget,ContextCapacityError,capacity,serialized_bytes
class ContextTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.s=MissionStore(self.tmp.name);self.m=self.s.create('short owner objective','model','conv',project='phase',spec={'owner_priority':'P3'})
  self.contract={'kind':'json','source':{'tool':'host_read_file','arguments':{'path':'/result.json'}},'expected':{'/value':42}}
  self.s.plan(self.m,[{'id':'task','title':'task','objective':'current objective','contract':{'semantic':[self.contract]}}]);self.b=ContextBudget(self.s,self.m,'task');self.cap={'limit':16384,'source':'test fixture, not real backend'}
 def payload(self):return {'model':'model','messages':[{'role':'system','content':'KEEP ALL OWNER POLICY'},{'role':'user','content':'historic output '+('x'*80000)}],'tools':[],'options':{'num_predict':1024}}
 def test_initial_planning_preserves_owner_objective_once_under_budget(self):
  goal='Exact owner requirements. '*320
  mission=self.s.create(goal,'model','conv',project='phase')
  budget=ContextBudget(self.s,mission)
  p=self.payload();budget.prepare(p,self.cap)
  state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['objective'],goal)
  self.assertEqual(state['owner_goal'],{'same_as':'objective','canonical_mission':mission})
  self.assertLessEqual(serialized_bytes(p),14336)
  checkpoint=budget.latest('operational_checkpoint')[0]['result']['checkpoint']
  self.assertEqual(checkpoint['owner_goal'],goal)
  self.assertEqual(checkpoint['objective'],goal)
 def test_distinct_owner_and_task_objectives_both_survive(self):
  p=self.payload();self.b.prepare(p,self.cap)
  state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['objective'],'current objective')
  self.assertEqual(state['owner_goal'],'short owner objective')
 def test_traceback_does_not_block_task_when_receipt_reference_fits(self):
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_engine_operation_ids':True}),self.m))
  error='Traceback (most recent call last):\n'+('  stack frame\n'*45)+'FileNotFoundError: /report.md'
  call=self.s.begin_call(self.m,'task','host_read_file',{'path':'/report.md'})
  self.s.finish_call(call,{'ok':False,'error':error},0)
  # Find the tight admission window: a receipt reference must permit progress
  # while every exact objective, predicate and original error stays canonical.
  compacted=None
  for limit in range(3000,8000,25):
   p=self.payload()
   try:self.b.prepare(p,{'limit':limit})
   except ContextCapacityError:continue
   state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
   if state.get('latest_tool_failure',{}).get('full_error_reference'):
    compacted=state;self.assertLessEqual(serialized_bytes(p),limit-2048);break
  self.assertIsNotNone(compacted)
  self.assertEqual(compacted['objective'],'current objective')
  self.assertEqual(compacted['owner_goal'],'short owner objective')
  self.assertEqual(compacted['task_contract']['semantic'],[self.contract])
  self.assertEqual(compacted['latest_tool_failure']['error'],'FileNotFoundError: /report.md')
  self.assertEqual(self.s.observations(self.m,'task')[-1]['result']['error'],error)
 def test_reserved_operation_ids_survive_compaction_without_mutating_ledger(self):
  operations={'inspect-20250621-002':{'arguments':{'executor':'Dell2','command':'original'},'result':{'returncode':0}},'uncertain-op':{'arguments':{'executor':'Dell1','command':'maybe-write'}}}
  self.s.event(self.m,'authority_state',result={'operations':operations})
  p=self.payload();p['messages']+=[{'role':'assistant','tool_calls':[{'function':{'name':'authority_work','arguments':{'command':'x'*40000}}}]},{'role':'tool','content':'refused'}]
  self.b.prepare(p,self.cap)
  state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['reserved_operation_ids'],sorted(operations))
  self.assertIn('ALL original arguments unchanged',state['operation_identity_rule'])
  self.assertEqual(self.b.latest('authority_state')[0]['result']['operations'],operations)
  self.assertLessEqual(serialized_bytes(p),self.cap['limit']-2048)
 def test_large_history_archived_and_input_bounded_in_place(self):
  p=self.payload();messages=p['messages'];before=copy.deepcopy(p);self.b.prepare(p,self.cap)
  self.assertIs(messages,p['messages']);self.assertLessEqual(serialized_bytes(p),16384-1024-1024)
  archive=self.b.latest('context_archive')[0];self.assertEqual(archive['result']['payload'],before)
  self.assertIn('KEEP ALL OWNER POLICY',p['messages'][0]['content']);self.assertIn('current objective',json.dumps(p));self.assertIn('value',json.dumps(p))
 def test_unknown_effect_and_counter_survive_context_change_and_store_restart(self):
  l=self.s.attempt_ledger(self.m);problem=l.problem('component',{'criterion':'original'});a=l.begin(problem,'initial','Dell2','execute',{'command':'maybe-wrote'})['attempt'];l.transition(a,'DISPATCHED');e=self.s.event(self.m,'p2_dispatch_failure_observed',result={'attempt':a,'known_not_executed':False});l.transition(a,'VALIDATION_INCONCLUSIVE',evidence=e,unknown=True);l.failure(a,infrastructure=True)
  self.b.prepare(self.payload(),self.cap);other=MissionStore(self.tmp.name);b=ContextBudget(other,self.m,'task');checkpoint=b.latest('operational_checkpoint')[0]['result']['checkpoint']
  self.assertEqual(checkpoint['counters'][0]['infra_incidents'],1);self.assertEqual(checkpoint['pending_effects'][0]['id'],a)
  self.assertTrue(other.attempt_ledger(self.m).begin(problem,'new-name','Dell1','execute',{'command':'different'})['requires_observation'])
 def test_only_structured_checkpoint_not_note_is_source_of_counter_truth(self):
  self.s.event(self.m,'working_note','task','JARVIS',result={'content':'I think all attempts succeeded'})
  _,c=self.b.checkpoint('before restart');self.assertEqual(c['model_notes'][0]['actor'],'JARVIS');self.assertEqual(c['counters'],[]);self.assertEqual(c['task_contract']['semantic'],[self.contract])
 def test_native_tool_exchange_preserved_when_small_enough(self):
  p=self.payload();pair=[{'role':'assistant','tool_calls':[{'function':{'name':'test','arguments':{'path':'real-file'}}}]},{'role':'tool','tool_name':'test','content':'actual result'}];p['messages']+=copy.deepcopy(pair);self.b.prepare(p,self.cap);self.assertEqual(p['messages'][-2:],pair)
 def test_oversized_executed_arguments_are_archived_not_rewritten_as_history(self):
  p=self.payload();p['messages']+=[{'role':'assistant','tool_calls':[{'function':{'name':'test','arguments':{'command':'x'*40000}}}]},{'role':'tool','tool_name':'test','content':'finished'}];self.b.prepare(p,self.cap)
  self.assertFalse(any(x.get('role')=='assistant' for x in p['messages']));self.assertTrue(self.b.latest('context_archive'))
 def test_mandatory_system_policy_is_never_silently_truncated(self):
  p=self.payload();p['messages'][0]['content']='policy'*10000;before=copy.deepcopy(p)
  with self.assertRaises(ContextCapacityError):self.b.prepare(p,self.cap)
  self.assertEqual(p,before);self.assertTrue(self.b.latest('operational_checkpoint'));self.assertTrue(self.b.latest('context_capacity_blocked'))
 def test_structured_review_is_not_replaced_by_unrelated_operational_state(self):
  p=self.payload();p['format']={'type':'object','properties':{'verdict':{'type':'string'}}};before=copy.deepcopy(p)
  with self.assertRaisesRegex(ContextCapacityError,'Structured review'):self.b.prepare(p,self.cap)
  self.assertEqual(p,before)
 def test_targeted_recall_rejects_unrelated_mission_and_labels_excerpt(self):
  reference=self.s.event(self.m,'incident',result={'original':'text'*1000});r=self.b.recall(reference,0,200);self.assertEqual(r['next_offset'],200);self.assertTrue(r['excerpt_is_not_complete_source'])
  other=self.s.create('unrelated','model','conv',project='elsewhere');bad=self.s.event(other,'private',result={'x':'not this mission'})
  with self.assertRaises(ValueError):self.b.recall(bad)
 def test_resume_checkpoint_has_no_entire_conversation_dependency(self):
  ref,c=self.b.checkpoint('restart');self.s.rebase_context(self.m,'test interruption',actor='Codex');b=ContextBudget(MissionStore(self.tmp.name),self.m,'task');saved=b.latest('operational_checkpoint')[0]['result']['checkpoint'];self.assertEqual(saved['objective'],c['objective']);self.assertEqual(saved['plan'],c['plan'])
 def test_live_loaded_limit_is_used_not_theoretical_model_maximum(self):
  cfg={'hybrid_compute':{'routes':{'mission':['Dell1']},'nodes':{'Dell1':{'enabled':True,'url':'http://fixture','mission_model':'model','inference_num_ctx':24576}}}}
  class Response:
   def __enter__(self):return self
   def __exit__(self,*a):pass
   def read(self):return json.dumps({'models':[{'name':'model','context_length':8192}]}).encode()
  with patch('jarvis.mission_context_budget.urllib.request.urlopen',return_value=Response()):r=capacity(cfg,'model')
  self.assertEqual(r['limit'],8192);self.assertEqual(r['configured_limit'],24576)
 def test_real_core_applies_budget_before_router_and_records_actual_usage(self):
  from jarvis.core import Core
  from jarvis.memory import Memory
  cfg={'hybrid_compute':{'nodes':{}},'compute_role':'mission','durable_num_predict':1024};core=Core(cfg,Memory(Path(self.tmp.name)/'memory.sqlite'));core.tools.root=Path(self.tmp.name);core.tools.mission_store=self.s;core.tools.context={'mission_id':self.m,'task_id':'task'}
  with patch('jarvis.compute.HybridRouter') as Router,patch('jarvis.mission_context_budget.capacity',return_value=self.cap):
   Router.return_value.infer.return_value=({'role':'assistant','content':'observed'},{'node':'Dell1','effective_model':'model','num_ctx':16384,'prompt_eval_count':1200})
   p=self.payload();core.ollama(p);sent=Router.return_value.infer.call_args.args[0];self.assertLessEqual(serialized_bytes(sent),14336)
  usage=self.b.latest('context_backend_usage')[0]['result'];self.assertEqual(usage['actual_prompt_tokens'],1200);self.assertTrue(usage['within_effective_context'])

 def test_review_admission_uses_the_same_response_profile_as_router(self):
  from jarvis.core import Core
  from jarvis.memory import Memory
  cfg={'hybrid_compute':{'nodes':{},'mission_segment_tokens':4096},'compute_role':'mission'}
  core=Core(cfg,Memory(Path(self.tmp.name)/'memory.sqlite'));core.tools.mission_store=self.s;core.tools.context={'mission_id':self.m,'task_id':'task'}
  payload={'model':'model','messages':[{'role':'system','content':'Reviewer policy'},{'role':'user','content':'x'*20000}], 'format':{'type':'object'},'options':{'num_predict':8192}}
  with patch('jarvis.compute.HybridRouter') as Router,patch('jarvis.mission_context_budget.capacity',return_value={'limit':32768}):
   Router.return_value.infer.return_value=({'content':'{}'},{'node':'Dell1','num_ctx':32768,'prompt_eval_count':5000})
   core.ollama(payload);sent=Router.return_value.infer.call_args.args[0]
  self.assertEqual(sent['options']['num_predict'],4096);self.assertEqual(payload['options']['num_predict'],8192)
  check=self.b.latest('context_budget_checked')[0]['result'];self.assertEqual(check['response_reserved'],4096)
  self.assertEqual(check['input_budget_estimate'],27648);self.assertFalse(check['compacted'])
  self.assertEqual(sent['messages'],payload['messages']);self.assertEqual(sent['format'],payload['format'])

 def test_manual_restart_checkpoint_is_not_shadowed_by_automatic_snapshots(self):
  from types import SimpleNamespace
  from jarvis.mission_context_budget import register
  reg=SimpleNamespace(specs={},mission_store=self.s,context={'mission_id':self.m,'task_id':'task'})
  register(reg)
  self.s.event(self.m,'authority_interface_failure',result={'epoch':'original','category':'schema','count':2})
  with patch('jarvis.mission_context_budget.os.getpid',return_value=111):
   saved=reg.specs['context_checkpoint'][4]({'reason':'before restart','pause_for_restart':True})
  with patch('jarvis.mission_context_budget.os.getpid',return_value=222):
   self.b.prepare(self.payload(),self.cap)
   resumed=reg.specs['context_resume'][4]({})
  self.assertEqual(resumed['previous_reference'],saved['reference']);self.assertTrue(resumed['new_process']);self.assertTrue(resumed['counters_preserved']);self.assertTrue(resumed['interface_counters_unchanged']);self.assertEqual(self.s.get(self.m)['state'],'interrupted')
 def test_impossible_response_budget_also_keeps_checkpoint_before_failure(self):
  p=self.payload();p['options']['num_predict']=50000
  with self.assertRaises(ContextCapacityError):self.b.prepare(p,self.cap)
  self.assertTrue(self.b.latest('context_capacity_blocked'));self.assertTrue(self.b.latest('operational_checkpoint'))

 def test_checkpoint_retains_typed_tool_result_reference_and_recall_content(self):
  invocation='actual-invocation-uuid'
  with self.s.db() as c:
   c.execute("INSERT INTO tool_calls(id,mission,task,tool,arguments,state,result,created,signature) VALUES(?,?,?,?,?,?,?,?,?)",(invocation,self.m,'task','context_recall','{}','completed',json.dumps({'ok':True,'result':{'reference':12,'content':'Observed failure, not success','next_offset':None}}),1,'fixture'))
  event=self.s.event(self.m,'tool_finished','task',result={'ok':True},invocation=invocation)
  _,checkpoint=self.b.checkpoint('actual tool projection')
  observation=checkpoint['last_observations'][0]
  self.assertEqual(observation['reference'],event);self.assertEqual(observation['invocation_id'],invocation)
  self.assertIn('Observed failure',observation['result']['content'])

 def test_failed_reader_calls_cannot_erase_substantive_execution_evidence(self):
  # Regression from actual P3 escalation: two real outputs followed by three
  # refused reads. A fresh bounded request must still expose those outputs.
  refs=[]
  for host,stdout in [('Dell1','configuration: None'),('Dell2','{"configured_inference_num_ctx":24576,"loaded_context_length":null}')]:
   refs.append(self.s.event(self.m,'authority_execution','task',result={'host':host}))
  self.s.event(self.m,'authority_state','task',result={'issues':{},'executions':{str(ref):{'host':host,'kind':'test','before':{},'after':{},'execution':{'returncode':0,'stdout':stdout,'stderr':''}} for ref,(host,stdout) in zip(refs,[('Dell1','configuration: None'),('Dell2','{"configured_inference_num_ctx":24576,"loaded_context_length":null}')])}})
  for i in range(3):
   token=self.s.begin_call(self.m,'task','authority_read_execution',{'reference':refs[i%2]})
   self.s.finish_call(token,{'ok':False,'error':'Repeated read blocked'},0)
  self.s.event(self.m,'authority_interface_failure',result={'epoch':'original','category':'repeated_read','count':3})
  self.s.transition(self.m,'interrupted')
  p=self.payload();self.b.prepare(p,self.cap);sent=json.dumps(p,ensure_ascii=False)
  self.assertIn('configuration: None',sent);self.assertIn('configured_inference_num_ctx',sent)
  self.assertIn('not inferred from process return code',sent)
  _,checkpoint=self.b.checkpoint('reopen')
  self.assertEqual(checkpoint['interface_counters'][0]['count'],3)
  self.assertEqual(self.s.get(self.m)['state'],'interrupted')

 def test_compaction_preserves_newest_guidance_and_actual_offered_tools(self):
  self.s.event(self.m,'coordinator_instruction',actor='Codex',result={'instruction':'OLD obsolete strategy'})
  self.s.event(self.m,'coordinator_instruction',actor='Codex',result={'instruction':'NEW current correction'})
  p=self.payload();p['tools']=[{'type':'function','function':{'name':'authority_work','parameters':{'type':'object'}}}]
  self.b.prepare(p,self.cap);sent=json.dumps(p)
  self.assertIn('NEW current correction',sent);self.assertIn('offered_tools',sent)

 def test_active_context_never_reoffers_completed_task_tests_as_current(self):
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'owner_priority':'P3','authority_task_scoped_evidence':True}),self.m))
  entries={}
  for task,host,stdout in [('previous-task','Dell1','OLD completed capacity observation'),('task','Dell2','CURRENT long-output test')]:
   e={'issue':'P3','host':host,'kind':'test','before':{},'after':{},'execution':{'returncode':0,'stdout':stdout,'stderr':''}}
   ref=self.s.event(self.m,'authority_execution',task,result=e);entries[str(ref)]=e
  self.s.event(self.m,'authority_state','task',result={'issues':{},'executions':entries})
  p=self.payload();self.b.prepare(p,self.cap);sent=json.dumps(p)
  self.assertIn('CURRENT long-output test',sent);self.assertNotIn('OLD completed capacity observation',sent)

 def test_deployment_boundary_excludes_invalidated_model_notes_not_counters(self):
  old=self.s.event(self.m,'working_note','task','JARVIS',result={'content':'Obsolete proposal to run a nonexistent binary'})
  self.s.event(self.m,'authority_interface_failure',result={'epoch':'original','category':'blocked_reader','count':3})
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_evidence_after_event':old}),self.m))
  self.s.event(self.m,'working_note','task','JARVIS',result={'content':'Current diagnosis'})
  _,checkpoint=self.b.checkpoint('after infrastructure fix')
  self.assertEqual(len(checkpoint['model_notes']),1);self.assertEqual(checkpoint['model_notes'][0]['result']['content'],'Current diagnosis')
  self.assertEqual(checkpoint['interface_counters'][0]['count'],3)
  with self.s.db() as c:self.assertEqual(c.execute('SELECT count(*) FROM mission_events WHERE id=?',(old,)).fetchone()[0],1)

 def test_compact_semantic_references_keep_exact_contracts_outside_active_context(self):
  from jarvis.verification import resolve_contract
  from types import SimpleNamespace
  original=self.s.tasks(self.m)[0]['contract']
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'compact_semantic_references':True}),self.m))
  p=self.payload();self.b.prepare(p,self.cap)
  self.assertIn('active:0',json.dumps(p))
  self.assertEqual(self.s.tasks(self.m)[0]['contract'],original)
  saved=self.b.latest('operational_checkpoint')[0]['result']['checkpoint']
  self.assertEqual(saved['task_contract'],original)
  reg=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'task'})
  self.assertEqual(resolve_contract(reg,'active:0'),self.contract)

 def test_compact_reference_view_preserves_all_failure_counts(self):
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'compact_semantic_references':True}),self.m))
  for category,count in [('old read',3),('old schema',2)]:self.s.event(self.m,'authority_interface_failure',result={'epoch':'audit','category':category,'count':count})
  p=self.payload();self.b.prepare(p,self.cap)
  state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(sorted(c['count'] for c in state['interface_counters']),[2,3])
  self.assertTrue(all('category_sha256' in c for c in state['interface_counters']))

 def test_context_result_objective_persisted_in_new_plan_before_dispatch(self):
  from jarvis.mission_context_budget import result_objective
  config={'hybrid_compute':{'routes':{'mission':['Dell1']},'nodes':{'Dell1':{'enabled':True,'hard_context_limit':32768}},'mission_segment_tokens':4096}}
  objective=result_objective(config)
  self.assertEqual(objective['input_tokens_max'],27648)
  m=self.s.create('new scoped objective','model','conv',spec={'context_result_objective':objective})
  self.s.plan(m,[{'id':'new','title':'model chosen task','contract':{'semantic':[self.contract]}}],author='JARVIS')
  self.assertEqual(self.s.tasks(m)[0]['contract']['context_result_objective'],objective)
  self.assertEqual(self.s.plans(m)[-1]['plan']['tasks'][0]['contract']['context_result_objective'],objective)
  self.assertEqual(self.s.tasks(m)[0]['contract']['semantic'],[self.contract])

 def test_hard_context_ceiling_wins_over_loaded_and_configured_larger_values(self):
  cfg={'durable_num_ctx':65536,'hybrid_compute':{'routes':{'mission':['Dell1']},'nodes':{'Dell1':{'enabled':True,'hard_context_limit':32768,'inference_num_ctx':65536}}}}
  self.assertEqual(capacity(cfg,'model')['limit'],32768)

 def test_compact_reference_interface_rejects_invented_contract_reconstruction(self):
  from jarvis.durable_cycle import semantic_reference_schemas
  from jsonschema import validate,ValidationError
  schema={'type':'function','function':{'name':'mission_verify','parameters':{'type':'object','properties':{'contract':{'type':['object','string']}},'required':['contract']}}}
  original=copy.deepcopy(schema)
  narrowed=semantic_reference_schemas([schema],{'contract':{'semantic':[self.contract,self.contract]}})[0]['function']['parameters']
  validate({'contract':'active:1'},narrowed)
  for value in [{'kind':'text','sha256':'invented'},'active:2']:
   with self.assertRaises(ValidationError):validate({'contract':value},narrowed)
  self.assertEqual(schema,original)

 def test_compaction_keeps_real_pass_and_written_report_to_avoid_replay(self):
  path='/reports/task.md'
  with self.s.db() as c:
   c.execute('UPDATE tasks SET contract=? WHERE mission=? AND id=?',(json.dumps({'report_path':path,'semantic':[self.contract]}),self.m,'task'))
  event=self.s.event(self.m,'semantic_verification','task',result={'contract':self.contract,'status':'PASS'})
  token=self.s.begin_call(self.m,'task','mission_verify',{'contract':'active:0'})
  self.s.finish_call(token,{'ok':True,'result':{'status':'PASS','verification_event':event}},0)
  write=self.s.begin_call(self.m,'task','host_write_file',{'path':path,'content':'Evidence-linked report'})
  self.s.finish_call(write,{'ok':True,'result':{'returncode':0}},0)
  p=self.payload();self.b.prepare(p,self.cap)
  state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  progress=state['active_task_contract_status']
  self.assertTrue(progress['report_written']);self.assertEqual(progress['semantic'][0]['status'],'PASS')
  self.assertEqual(progress['semantic'][0]['invocation_id'],token)
  self.assertEqual(progress['completion_request'],{'id':'task','report_path':path,'evidence_id':token})
  # This is a request for validation, never an automatic promotion.
  self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')

 def test_complete_source_page_survives_failures_and_verbose_old_counter_metadata(self):
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_engine_operation_ids':True}),self.m))
  source=(Path(__file__).parents[1]/'jarvis/worker.py').read_text()
  invocation=self.s.begin_call(self.m,'task','authority_read_execution',{'reference':10,'stream':'stdout'})
  self.s.finish_call(invocation,{'ok':True,'result':{'reference':10,'content':source,'stream':'stdout','start_line':1,'total_lines':len(source.splitlines()),'source_version':None,'observed_process_returncode':0}},0)
  for i in range(3):
   bad=self.s.begin_call(self.m,'task','authority_read_execution',{'reference':10})
   self.s.finish_call(bad,{'ok':False,'error':'Already read, do not repeat'},0)
  for i in range(14):self.s.event(self.m,'authority_interface_failure',result={'epoch':'original','category':str(i)+':'+('long interface failure '*40),'count':3})
  p=self.payload();self.b.prepare(p,self.cap)
  state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['latest_successful_read']['content'],source)
  self.assertIn('def run(config_path,slot)',state['latest_successful_read']['content'])
  self.assertIn('while not missions.stop.wait(1)',state['latest_successful_read']['content'])
  self.assertEqual(state['latest_successful_read']['invocation_id'],invocation)
  self.assertEqual([v['count'] for v in state['interface_counters']],[3]*14)

 def test_read_from_an_obsolete_manifest_is_not_reintroduced_as_current_source(self):
  from jarvis.distributed_authority import version
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_engine_operation_ids':True}),self.m))
  token=self.s.begin_call(self.m,'task','authority_read_execution',{'reference':10})
  self.s.finish_call(token,{'ok':True,'result':{'reference':10,'content':'OLD SOURCE','source_version':version({'file':'old'})}},0)
  self.s.event(self.m,'authority_state',result={'issues':{},'executions':{'11':{'host':'Dell1','kind':'correct','before':{'file':'old'},'after':{'file':'new'},'execution':{'returncode':0}}}})
  _,checkpoint=self.b.checkpoint('source changed')
  self.assertNotIn('latest_successful_read',checkpoint)

 def test_native_inspection_body_survives_reader_failures_without_another_read(self):
  from jarvis.distributed_authority import version
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_engine_operation_ids':True,'authority_task_scoped_evidence':True}),self.m))
  source=(Path(__file__).parents[1]/'jarvis/worker.py').read_text()
  entry={'host':'Dell1','kind':'inspect','before':{'worker.py':'current'},'after':{'worker.py':'current'},'execution':{'returncode':0,'stdout':source,'stderr':''}}
  ref=self.s.event(self.m,'authority_execution','task',result=entry)
  self.s.event(self.m,'authority_state',result={'issues':{},'executions':{str(ref):entry}})
  for _ in range(3):
   token=self.s.begin_call(self.m,'task','authority_read_execution',{'reference':ref})
   self.s.finish_call(token,{'ok':False,'error':'Already read'},0)
  p=self.payload();self.b.prepare(p,self.cap)
  state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  body=state['latest_successful_read']
  self.assertIn('def run(config_path,slot)',body['content']);self.assertIn('while not missions.stop.wait(1)',body['content'])
  self.assertEqual(body['reference'],ref);self.assertEqual(body['source_version'],version(entry['after']))

 def test_engine_identity_projection_does_not_reteach_legacy_alias_selection(self):
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_engine_operation_ids':True}),self.m))
  self.s.event(self.m,'authority_state',result={'issues':{},'executions':{},'operations':{'legacy-model-alias':{'arguments':{}}}})
  p=self.payload();self.b.prepare(p,self.cap)
  state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertNotIn('reserved_operation_ids',state);self.assertIn('Do not supply operation_id',state['operation_identity_rule'])
  saved=self.b.latest('operational_checkpoint')[0]['result']['checkpoint']
  self.assertEqual(saved['reserved_operation_ids'],['legacy-model-alias'])

 def test_read_delivery_arguments_and_counts_survive_oversized_history(self):
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_engine_operation_ids':True}),self.m))
  args={'reference':31,'stream':'stdout','start_line':1,'max_lines':10}
  token=self.s.begin_call(self.m,'task','authority_read_execution',args)
  self.s.finish_call(token,{'ok':True,'result':{'reference':31,'content':'path only','stream':'stdout','start_line':1,'delivery_count':3,'already_delivered':True}},0)
  p=self.payload();p['messages']+=[{'role':'assistant','tool_calls':[{'function':{'name':'authority_read_execution','arguments':{'reference':31,'padding':'x'*30000}}}]},{'role':'tool','content':'path only'}]
  self.b.prepare(p,self.cap)
  state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  read=state['read_delivery_history'][0]
  self.assertEqual(read['parameters'],args);self.assertEqual(read['delivery_count'],3);self.assertTrue(read['already_delivered'])

 def test_tool_success_with_process_failure_cannot_displace_successful_source(self):
  from jarvis.distributed_authority import version
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_engine_operation_ids':True}),self.m))
  source=(Path(__file__).parents[1]/'jarvis/worker.py').read_text();manifest={'worker.py':'current'}
  entry={'host':'Dell1','kind':'inspect','after':manifest,'execution':{'returncode':0,'stdout':source}}
  ref=self.s.event(self.m,'authority_execution','task',result=entry)
  self.s.event(self.m,'authority_state',result={'issues':{},'executions':{str(ref):entry}})
  good=self.s.begin_call(self.m,'task','authority_read_execution',{'reference':ref,'stream':'stdout'})
  self.s.finish_call(good,{'ok':True,'result':{'reference':ref,'content':source,'source_version':version(manifest),'stream':'stdout','observed_process_returncode':0,'total_lines':len(source.splitlines()),'start_line':1,'excerpt_truncated':False}},0)
  failed=self.s.begin_call(self.m,'task','authority_read_execution',{'reference':ref,'stream':'stderr'})
  self.s.finish_call(failed,{'ok':True,'result':{'reference':ref,'content':'cat: bad/path: No such file','source_version':version(manifest),'stream':'stderr','observed_process_returncode':1}},0)
  p=self.payload();self.b.prepare(p,self.cap);state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['latest_successful_read']['content'],source)
  self.assertNotEqual(state['latest_successful_read']['invocation_id'],failed)

 def test_two_distinct_successful_pages_survive_duplicate_reads_and_metadata(self):
  from jarvis.distributed_authority import version
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_engine_operation_ids':True}),self.m))
  worker=(Path(__file__).parents[1]/'jarvis/worker.py').read_text();api='class Helper:\n def measure_module(self, name):\n  return name\n'
  manifest={'worker.py':'worker','helper.py':'api'};entries={}
  for content in (api,worker,worker,'/path/to/worker.py'):
   entry={'host':'Dell1','kind':'inspect','after':manifest,'execution':{'returncode':0,'stdout':content}}
   ref=self.s.event(self.m,'authority_execution','task',result=entry);entries[str(ref)]=entry
   call=self.s.begin_call(self.m,'task','authority_read_execution',{'reference':ref,'stream':'stdout'})
   self.s.finish_call(call,{'ok':True,'result':{'reference':ref,'content':content,'source_version':version(manifest),'stream':'stdout','observed_process_returncode':0,'total_lines':len(content.splitlines()),'start_line':1,'excerpt_truncated':False}},0)
  self.s.event(self.m,'authority_state',result={'issues':{},'executions':entries})
  before=self.s.attempt_ledger(self.m).snapshot()['problems']
  p=self.payload();self.b.prepare(p,self.cap);state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['latest_successful_read']['content'],worker)
  self.assertEqual(state['additional_inspection_pages'][0]['content'],api)
  self.assertEqual(self.s.attempt_ledger(self.m).snapshot()['problems'],before)
  self.assertLessEqual(serialized_bytes(p),14336)

 def test_excerpt_recovery_uses_immutable_full_receipt_without_rerunning_command(self):
  spec={'authority_engine_operation_ids':True,'authority_workspace':{'local_root':self.tmp.name}}
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  import hashlib
  source=(Path(__file__).parents[1]/'jarvis/worker.py').read_text()+'\n'+('# full receipt tail marker\n'*70)
  raw=json.dumps({'execution':{'returncode':0,'stdout':source,'stderr':''}}).encode()
  path=Path(self.tmp.name)/'receipts'/self.m/'fixture.json';path.parent.mkdir(parents=True);path.write_bytes(raw)
  entry={'host':'Dell1','kind':'inspect','after':{'worker.py':'current'},'execution':{'returncode':0,'stdout':source[:700]+'[EXCERPT]'+source[-100:],'stdout_model_excerpt':True},'full_receipt':{'local':str(path),'sha256':hashlib.sha256(raw).hexdigest()}}
  ref=self.s.event(self.m,'authority_execution','task',result=entry);self.s.event(self.m,'authority_state',result={'issues':{},'executions':{str(ref):entry}})
  _,checkpoint=self.b.checkpoint('recover without execution')
  self.assertIn('def run(config_path,slot)',checkpoint['latest_successful_read']['content'])
  self.assertNotIn('[EXCERPT]',checkpoint['latest_successful_read']['content'])
  self.assertTrue(checkpoint['latest_successful_read']['excerpt_truncated'])
  self.assertNotIn('full receipt tail marker',checkpoint['latest_successful_read']['content'])
  path.write_bytes(raw+b'tampered')
  _,checkpoint=self.b.checkpoint('reject changed receipt')
  self.assertNotIn('latest_successful_read',checkpoint)

 def test_pending_model_proposal_survives_compaction_as_an_action_reference(self):
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_engine_operation_ids':True}),self.m))
  proposal={'issue':'Q1','executor':'Dell2','summary':'Model-authored candidate, not applied','edits':[{'path':'engine/worker.py','old':'original','new':'proposed'}]}
  ref=self.s.event(self.m,'authority_code_proposal','task','JARVIS/Qwen80B',result={'proposal':proposal,'applied':False,'tested':False})
  p=self.payload();self.b.prepare(p,self.cap);state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['pending_code_proposal']['proposal_reference'],ref)
  self.assertFalse(state['pending_code_proposal']['applied']);self.assertFalse(state['pending_code_proposal']['tested'])
  self.s.event(self.m,'authority_code_proposal_applied','task','JARVIS/Qwen80B',result={'proposal_reference':ref,'applied':True,'tested':False})
  p=self.payload();self.b.prepare(p,self.cap);state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertNotIn('pending_code_proposal',state)
  self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')

 def test_last_tool_failure_is_not_erased_by_notes_or_successful_analysis(self):
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'authority_engine_operation_ids':True}),self.m))
  args={'issue':'Q1','executor':'Dell1','path':'engine/large.py'}
  token=self.s.begin_call(self.m,'task','authority_draft_edit',args)
  self.s.finish_call(token,{'ok':False,'error':'Source exceeds focused 6000-byte unit; choose a smaller file'},0)
  for name in ['mission_note','mission_note','authority_analyze']:
   call=self.s.begin_call(self.m,'task',name,{})
   self.s.finish_call(call,{'ok':True,'result':{'not_a_resolution':True}},0)
  p=self.payload();self.b.prepare(p,self.cap);state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  failure=state['latest_tool_failure'];self.assertEqual(failure['invocation_id'],token)
  self.assertEqual(failure['parameters'],args);self.assertIn('6000',failure['error'])
  self.assertIn('does not mean an executed test failed',state['active_task_contract_status']['meaning'])
  self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')

 def test_large_test_json_keeps_fail_and_insufficient_without_reinjecting_full_reports(self):
  import hashlib
  spec={'authority_engine_operation_ids':True,'authority_workspace':{'local_root':self.tmp.name}}
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  output={'suite_pass':True,'oracle_sha256':'actual-script-digest','cases':[{'case':name,'observed_status':status,'expected_status':status,'large_report':'x'*20000,'canonical_service_tested':False} for name,status in [('match','PASS'),('changed','FAIL'),('missing','INSUFFICIENT')]]}
  text=json.dumps(output);raw=json.dumps({'execution':{'returncode':0,'stdout':text,'stderr':''}}).encode()
  path=Path(self.tmp.name)/'receipts'/self.m/'test.json';path.parent.mkdir(parents=True);path.write_bytes(raw)
  entry={'host':'Dell1','kind':'test','after':{'worker.py':'current'},'execution':{'returncode':0,'stdout':text[:1500]+'[EXCERPT]','stdout_model_excerpt':True},'full_receipt':{'local':str(path),'sha256':hashlib.sha256(raw).hexdigest()}}
  ref=self.s.event(self.m,'authority_execution','task',result=entry);self.s.event(self.m,'authority_state',result={'issues':{},'executions':{str(ref):entry}})
  p=self.payload();self.b.prepare(p,self.cap);state=json.loads(p['messages'][1]['content']);state=state.get('operational_state',state)
  summary=state['reported_test_output'];self.assertEqual(summary['reference'],ref)
  self.assertEqual([c['observed_status'] for c in summary['cases']],['PASS','FAIL','INSUFFICIENT'])
  self.assertEqual(summary['full_stdout_sha256'],hashlib.sha256(text.encode()).hexdigest())
  self.assertIn('not independent semantic verification',summary['meaning'])
  self.assertNotIn('large_report',json.dumps(p));self.assertEqual(path.read_bytes(),raw)
  self.assertLessEqual(serialized_bytes(p),14336)

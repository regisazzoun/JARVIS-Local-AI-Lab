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

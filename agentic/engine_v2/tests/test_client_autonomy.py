import asyncio,importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch,AsyncMock
from jarvis.client_capabilities import Capabilities
from jarvis.client_autonomy import OwnerClient,context,render
from jarvis.context_retrieval import retrieve,view
from jarvis.memory import Memory
from jarvis.intent import classify
class Autonomy(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);identity=self.root/'identity';identity.write_text('JARVIS Debian canonical identity')
  self.api=Capabilities(self.root,config={'identity_file':str(identity)});self.client=OwnerClient(self.api,owner_id='owner')
 def test_owner_compaction_keeps_visible_argument_schema_and_memory(self):
  from jarvis.mission_context_budget import ContextBudget
  from jarvis.structured_actions import request
  ident=self.api.store.create('Scan local','model','conv','p',{'client_autonomy':True})
  self.api.store.plan(ident,[{'id':'t','title':'scan','objective':'scan'}])
  source={'model':'model','messages':[{'role':'system','content':'Owner policy'},{'role':'user','content':'x'*70000}],'tools':[{'type':'function','function':{'name':'host_exec','parameters':{'type':'object','properties':{'command':{'type':'string'}},'required':['command'],'additionalProperties':False}}}],'options':{'num_predict':1024}}
  payload,schema=request(source);payload.pop('_jarvis_action_contract')
  result=ContextBudget(self.api.store,ident,'t').prepare(payload,{'limit':16384},structured_action=True)
  active=json.loads(result['messages'][1]['content']);active=active.get('operational_state',active)
  self.assertEqual(active['current_action_schema'],schema);self.assertIn('canonical_memory_data',active)
  self.assertEqual(active['active_task']['id'],'t');self.assertEqual(active['active_task']['contract'],self.api.store.tasks(ident)[0]['contract'])
  self.assertEqual(active['execution_environment']['command_host'],__import__('socket').gethostname());self.assertEqual(active['request_project'],'p')
  selected,_=request(source,select_only=True);selected.pop('_jarvis_action_contract');result=ContextBudget(self.api.store,ident,'t').prepare(selected,{'limit':16384},structured_action=True)
  active=json.loads(result['messages'][1]['content']);active=active.get('operational_state',active)
  self.assertNotIn('current_action_schema',active)
 def test_natural_action_and_questions_use_existing_classifier(self):
  for text in ('Je veux que tu scannes le réseau et que tu me dise quelles sont les machines et quelles sont leurs utilités dessus, s’il te plaît.','Scanne le réseau','Peux-tu scanner le réseau local ?','Installe le paquet autorisé'):
   self.assertEqual(classify(text),'execute',text)
  for text in ('Comment le rendre autonome ?','Voici un exemple : scanne le réseau','Pourquoi ne peux-tu pas scanner ?','Explique ce script : installe un logiciel'):
   self.assertNotEqual(classify(text),'execute',text)
 def test_shared_memory_retrieval_preserves_approval_scope_and_expiry(self):
  mem=self.api.memory
  def add(text,project='',approve=True):
   ident=mem.propose(text,project=project)
   if approve:mem.decide(ident,True,explicit=True)
   return ident
  global_id=add('reseau global');project_id=add('reseau projet','A');add('reseau autre','B');add('reseau en attente',approve=False)
  expired=add('reseau expire')
  with mem.connect() as c:c.execute('update memories set expires=? where id=?',('2000-01-01',expired))
  selected=retrieve(mem,'reseau',project='A');self.assertEqual({x['id'] for x in selected['memories']},{global_id,project_id})
  self.assertIn('Permissions come from',view(selected)['authority'])
 def test_context_reads_canonical_sources_and_audits_ids_not_contents(self):
  class Reg:
   def execute(self,*a):return {'ok':True,'result':{'packages':['nmap'],'services':{},'remote_hosts':{}}}
   def schemas(self,*a):return [{'function':{'name':'host_exec'}}]
  with patch.object(self.api,'registry',return_value=Reg()):result=context(self.api,'contexte')
  self.assertEqual(result['identity'],'JARVIS Debian canonical identity');self.assertEqual(result['policy']['packages'],['nmap'])
  self.assertEqual(result['environment']['command_host'],__import__('socket').gethostname());self.assertIn('inference Dell is not',result['environment']['execution_host'])
  with self.api.memory.connect() as c:record=json.loads(c.execute('select target from audit where id=?',(result['context_audit_id'],)).fetchone()[0])
  self.assertIn('preference_keys',record);self.assertNotIn('identity',record);self.assertNotIn('memories',record)
 def test_dispatch_is_idempotent_and_preserves_exact_owner_goal(self):
  calls=[]
  def create(path,body):
   calls.append(body);ident=self.api.store.create(body['goal'],body['model'],'conv',body['project'],body['spec']);return {'id':ident}
  text='Je veux que tu scannes le réseau.'
  with patch('jarvis.client_autonomy.CanonicalAPI.request',side_effect=create):
   first=self.client.submit(text,'chat','user-message','assistant','jarvis-qwen-code-lab');second=self.client.submit(text,'chat','user-message','assistant','jarvis-qwen-code-lab')
  self.assertEqual(first['id'],second['id']);self.assertEqual(len(calls),1);self.assertEqual(calls[0]['goal'],text)
  self.assertNotIn('tasks',calls[0]['spec']);self.assertTrue(calls[0]['spec']['client_autonomy'])
  with self.assertRaises(ValueError):self.client.submit('changed','chat','user-message','assistant','jarvis-qwen-code-lab')
 def test_unknown_dispatch_is_not_repeated(self):
  with patch('jarvis.client_autonomy.CanonicalAPI.request',side_effect=TimeoutError('unknown')) as call:
   with self.assertRaises(TimeoutError):self.client.submit('Scanne le réseau','chat','u','a','jarvis-qwen-code-lab')
   result=self.client.submit('Scanne le réseau','chat','u','a','jarvis-qwen-code-lab')
   self.assertEqual(result['state'],'UNKNOWN');self.assertEqual(call.call_count,1)
 def test_no_owner_or_no_request_identity_dispatches_nothing(self):
  with self.assertRaises(PermissionError):self.client.prepare('Scanne','other','chat','u','a','jarvis-qwen-code-lab')
  with patch('jarvis.client_autonomy.CanonicalAPI.request') as call:
   with self.assertRaises(ValueError):self.client.submit('Scanne','','u','a','jarvis-qwen-code-lab')
   call.assert_not_called()
 def test_questions_load_context_without_creating_mission(self):
  with patch('jarvis.client_autonomy.context',return_value={'context_audit_id':1}),patch.object(self.client,'submit') as submit:
   result=self.client.prepare('Pourquoi cette limite ?','owner','chat','u','a','jarvis-qwen-code-lab')
   self.assertNotIn('mission',result);submit.assert_not_called()
 def test_receipt_does_not_claim_queued_is_completed(self):
  self.assertIn('aucun succès final',render({'id':'a'*32,'state':'queued','tasks':[]}))
class FilterTests(unittest.TestCase):
 def setUp(self):
  path=Path(__file__).resolve().parents[3]/'tools/qwen_webui/webui_owner_filter.py';spec=importlib.util.spec_from_file_location('owner_filter_fixture',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);self.filter=mod.Filter();self.filter.valves.OWNER_ID='owner';self.user={'id':'owner','role':'admin'};self.model={'id':'jarvis-qwen-code-lab'}
 def test_nonowner_does_not_receive_memory_or_dispatch(self):
  self.filter.call=AsyncMock();body={'messages':[]}
  asyncio.run(self.filter.inlet(body,__user__={'id':'other','role':'admin'},__model__=self.model));self.filter.call.assert_not_called()
 def test_task_acknowledgement_has_no_effect_tools_or_history_replay(self):
  self.filter.call=AsyncMock(return_value={'id':'a'*32,'state':'queued'});meta={'jarvis_owner':{'mission_id':'a'*32}}
  body={'messages':[{'role':'user','content':'full goal remains in engine'}],'tools':[{'unsafe':'duplicate'}]}
  result=asyncio.run(self.filter.request(body,self.user,meta,self.model));self.assertEqual(result['tools'],[]);self.assertNotIn('full goal remains',json.dumps(result['messages']))
 def test_outlet_replaces_generic_refusal_only_with_real_receipt(self):
  self.filter.call=AsyncMock(return_value={'content':'Mission a — queued, not completed'})
  body={'messages':[{'role':'assistant','content':'Je ne peux pas exécuter.'}]};meta={'jarvis_owner':{'mission_id':'a'*32}}
  result=asyncio.run(self.filter.outlet(body,self.user,meta,self.model));self.assertIn('queued',result['messages'][0]['content']);self.assertNotIn('Je ne peux',result['messages'][0]['content'])
 def test_unsupported_refusal_without_tools_never_becomes_success(self):
  body={'messages':[{'role':'assistant','content':'Je ne peux pas scanner sans ton accord explicite','output':[]}]};meta={'jarvis_owner':{'context_audit_id':8}}
  result=asyncio.run(self.filter.outlet(body,self.user,meta,self.model));self.assertIn('Aucune opération',result['messages'][0]['content'])

class DeliveryTests(unittest.TestCase):
 def test_publisher_delivers_once_per_canonical_version(self):
  from jarvis.client_autonomy import deliver_one
  with tempfile.TemporaryDirectory() as tmp:
   api=Capabilities(tmp,config={"test":True});store=api.store
   ident=store.create('Scanne','model','conv','p',{'client_autonomy':True,'webui_owner_binding':{'owner_id':'owner','chat_id':'chat','message_id':'assistant'}})
   client=OwnerClient(api,owner_id='owner')
   class Response:
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self):return json.dumps({'chat':{'history':{'messages':{'assistant':{'id':'assistant','role':'assistant','done':True}}}}}).encode()
   with patch('jarvis.client_autonomy.Capabilities',return_value=api),patch('jarvis.client_autonomy.OwnerClient',return_value=client),patch('jarvis.client_autonomy.Path.read_text',return_value='token'),patch('jarvis.client_autonomy.urllib.request.urlopen',return_value=Response()) as send:
    self.assertTrue(deliver_one(store));self.assertFalse(deliver_one(store));self.assertEqual(send.call_count,3)
   self.assertEqual(store.get(ident)['state'],'queued')
 def test_delivery_failure_never_marks_delivered_or_changes_state(self):
  from jarvis.client_autonomy import deliver_one
  with tempfile.TemporaryDirectory() as tmp:
   api=Capabilities(tmp,config={"test":True});store=api.store
   ident=store.create('Scanne','model','conv','p',{'client_autonomy':True,'webui_owner_binding':{'owner_id':'owner','chat_id':'chat','message_id':'assistant'}})
   client=OwnerClient(api,owner_id='owner')
   with patch('jarvis.client_autonomy.Capabilities',return_value=api),patch('jarvis.client_autonomy.OwnerClient',return_value=client),patch('jarvis.client_autonomy.Path.read_text',return_value='token'),patch('jarvis.client_autonomy.urllib.request.urlopen',side_effect=OSError('offline')):
    with self.assertRaises(OSError):deliver_one(store)
   with store.db() as db:self.assertEqual(db.execute("select count(*) from mission_events where kind='webui_receipt_delivered'").fetchone()[0],0)
   self.assertEqual(store.get(ident)['state'],'queued')

class ReportLifecycleTests(unittest.TestCase):
 def setUp(self):
  from types import SimpleNamespace
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.api=Capabilities(self.tmp.name,config={'test':True});self.s=self.api.store
  self.m=self.s.create('Owner action','model','conv','p',{'client_autonomy':True,'planning_report_steps':True})
  self.criterion={'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/report.md'}}}
  self.s.plan(self.m,[{'id':'t','title':'task','contract':{'report_path':'/report.md','semantic':[self.criterion]}}]);self.reg=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'t'})
 def test_known_operations_and_report_write_precede_final_report_validation(self):
  from jarvis.legacy_attempts import guarded,settle
  from unittest.mock import Mock
  effect=Mock(return_value={'returncode':0,'stdout':'actual fixture result'})
  guarded(self.reg,'host_exec',{'command':'first'},effect,True)
  guarded(self.reg,'host_exec',{'command':'first'},effect,True)
  self.assertEqual(effect.call_count,1)
  guarded(self.reg,'host_exec',{'command':'second'},effect,True)
  guarded(self.reg,'host_write_file',{'path':'/report.md','content':'fixture report'},effect,True)
  rows=self.s.attempt_ledger(self.m).snapshot()['attempts'];self.assertEqual(len(rows),3);self.assertTrue(all(r['state']=='VALIDATION_INCONCLUSIVE' for r in rows))
  verdict={'status':'PASS','contract':self.criterion};verdict['verification_event']=self.s.event(self.m,'semantic_verification','t',result=verdict);settle(self.reg,verdict)
  self.assertTrue(all(r['state']=='SUCCESS' for r in self.s.attempt_ledger(self.m).snapshot()['attempts']))
 def test_one_failed_report_is_one_failed_cycle_for_all_operations(self):
  from jarvis.legacy_attempts import guarded,settle
  from unittest.mock import Mock
  for command in ('first','second','third'):guarded(self.reg,'host_exec',{'command':command},Mock(return_value={'returncode':0}),True)
  verdict={'status':'FAIL','contract':self.criterion};verdict['verification_event']=self.s.event(self.m,'semantic_verification','t',result=verdict);settle(self.reg,verdict)
  snapshot=self.s.attempt_ledger(self.m).snapshot();self.assertEqual(snapshot['problems'][0]['failed_cycles']+snapshot['problems'][0]['infra_incidents'],1)
  self.assertTrue(all(r['state']=='EXECUTED_TEST_FAILED' for r in snapshot['attempts']))
 def test_unknown_effect_still_blocks_different_operation_and_report(self):
  from jarvis.legacy_attempts import guarded
  from unittest.mock import Mock
  with self.assertRaises(ConnectionError):guarded(self.reg,'host_exec',{'command':'first'},Mock(side_effect=ConnectionError('unknown')),True)
  for name,args in [('host_exec',{'command':'second'}),('host_write_file',{'path':'/report.md','content':'text'})]:
   effect=Mock()
   with self.assertRaisesRegex(ValueError,'observe existing effect'):guarded(self.reg,name,args,effect,True)
   effect.assert_not_called()
 def test_attested_completed_process_error_is_failed_not_unknown(self):
  from jarvis.legacy_attempts import guarded
  from unittest.mock import Mock
  error=RuntimeError('process exit');error.response={'error_code':'RuntimeError','diagnostic':{'operation':'host_exec'},'evidence_id':'process-proof','result':{'returncode':1,'stdout':'observed output','stderr':'observed error'}}
  with self.assertRaises(RuntimeError):guarded(self.reg,'host_exec',{'command':'failed process'},Mock(side_effect=error),True)
  row=self.s.attempt_ledger(self.m).snapshot()['attempts'][0];self.assertEqual(row['state'],'EXECUTION_FAILED');self.assertFalse(row['unknown_outcome'])
  effect=Mock(return_value={'returncode':0});guarded(self.reg,'host_exec',{'command':'different operation'},effect,True);effect.assert_called_once()
 def test_attested_package_policy_refusal_is_not_an_unknown_effect(self):
  from jarvis.legacy_attempts import guarded
  from unittest.mock import Mock
  error=PermissionError('denied');error.response={'error_code':'PermissionError','error':'Paquet absent de la politique propriétaire','diagnostic':{'operation':'host_package','error_category':'permission_denied'},'evidence_id':'actual-broker-refusal'}
  with self.assertRaises(PermissionError):guarded(self.reg,'host_package',{'action':'install','package':'absent'},Mock(side_effect=error),True)
  row=self.s.attempt_ledger(self.m).snapshot()['attempts'][0];self.assertEqual(row['state'],'NOT_EXECUTED');self.assertFalse(row['unknown_outcome'])
  effect=Mock(return_value={'returncode':0});guarded(self.reg,'host_exec',{'command':'different operation'},effect,True);effect.assert_called_once()
  with self.assertRaisesRegex(ValueError,'known non-execution'):guarded(self.reg,'host_package',{'action':'install','package':'absent'},Mock(),True)
 def test_existing_report_missions_retain_original_guard(self):
  from jarvis.legacy_attempts import guarded
  from unittest.mock import Mock
  with self.s.db() as c:c.execute('update missions set spec=? where id=?',(json.dumps({'planning_report_steps':True}),self.m))
  guarded(self.reg,'host_exec',{'command':'first'},Mock(return_value={'returncode':0}),True)
  with self.assertRaisesRegex(ValueError,'observe existing effect'):guarded(self.reg,'host_exec',{'command':'second'},Mock(),True)

class ProcessContextTests(unittest.TestCase):
 def test_owner_process_output_is_visible_bound_and_explicitly_excerpted(self):
  from jarvis.mission_context_budget import observation_view
  row={'id':'invocation','event_reference':12,'tool':'host_exec','arguments':{'command':'chosen command'},'result':{'ok':True,'result':{'returncode':0,'stdout':'actual output','stderr':'','evidence_id':'broker-proof'}}}
  self.assertNotIn('stdout',observation_view(row)['result'])
  result=observation_view(row,include_process_output=True)['result'];self.assertEqual(result['stdout'],'actual output');self.assertEqual(result['broker_evidence'],'broker-proof');self.assertEqual(result['full_output_reference'],12);self.assertFalse(result['stdout_excerpt'])
  row['result']['result']['stdout']='x'*1500
  self.assertTrue(observation_view(row,include_process_output=True)['result']['stdout_excerpt'])

class OwnerPromptTests(unittest.TestCase):
 def test_new_owner_task_executes_while_historical_prompt_is_preserved(self):
  from jarvis.durable_cycle import owner_execution_prompt,report_execution_prompt
  for phase in (None,'verify','correct','complete'):
   text=owner_execution_prompt('Canonical identity',True,phase)
   self.assertNotIn('prépare uniquement',text);self.assertNotIn('Ne clos jamais P4',text);self.assertIn('droits actuels du broker',text)
   self.assertIn('Ne clos jamais P4',report_execution_prompt('Canonical identity',True,phase))

class PhaseMessageTests(unittest.TestCase):
 def test_phase_is_replaced_then_removed_without_losing_other_instructions(self):
  from jarvis.durable_cycle import owner_phase_messages
  original=[{'role':'system','content':'Owner constraints'},{'role':'user','content':'Original goal'}]
  hint='\n<JARVIS_OWNER_REPORT_PHASE>Report missing</JARVIS_OWNER_REPORT_PHASE>'
  first=owner_phase_messages(original,hint);second=owner_phase_messages(first,hint)
  self.assertEqual(first,second);self.assertEqual(original[0]['content'],'Owner constraints')
  second[0]['content']+='\nIndependent verification now offered'
  cleared=owner_phase_messages(second,'');self.assertNotIn('Report missing',cleared[0]['content']);self.assertIn('Independent verification',cleared[0]['content']);self.assertEqual(cleared[1],original[1])

class ReportPhaseTests(unittest.TestCase):
 def test_missing_report_waits_for_writer_but_unknown_effect_keeps_verifier(self):
  from jarvis.durable_cycle import owner_report_phase
  from jarvis.legacy_attempts import guarded
  from types import SimpleNamespace
  from unittest.mock import Mock
  with tempfile.TemporaryDirectory() as tmp:
   api=Capabilities(tmp,config={'test':True});s=api.store;path=str(Path(tmp)/'report.md');criterion={'kind':'report','source':{'tool':'host_read_file','arguments':{'path':path}}}
   ident=s.create('goal','model','conv','p',{'client_autonomy':True,'planning_report_steps':True});s.plan(ident,[{'id':'t','title':'task','contract':{'report_path':path,'semantic':[criterion]}}]);task=s.tasks(ident)[0]
   schemas=[{'function':{'name':n}} for n in ('host_exec','host_write_file','mission_verify','mission_task_complete','mission_report_review')]
   offered,instruction=owner_report_phase(s,s.get(ident),task,schemas);self.assertEqual([x['function']['name'] for x in offered],['host_exec','host_write_file']);self.assertIn('n’est pas encore écrit',instruction)
   Path(path).write_text('report');self.assertEqual(owner_report_phase(s,s.get(ident),task,schemas),(schemas,''));Path(path).unlink()
   reg=SimpleNamespace(mission_store=s,context={'mission_id':ident,'task_id':'t'})
   with self.assertRaises(ConnectionError):guarded(reg,'host_exec',{'command':'unknown'},Mock(side_effect=ConnectionError('lost')),True)
   self.assertEqual(owner_report_phase(s,s.get(ident),task,schemas),(schemas,''))
   row=s.get(ident);row['spec']='{}';self.assertEqual(owner_report_phase(s,row,task,schemas),(schemas,''))

import copy,importlib.util,json,os,tempfile,unittest,sqlite3
from pathlib import Path
from contextlib import closing
from unittest.mock import patch

class ReadoutTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  path=Path(__file__).resolve().parents[3]/'tools/optimisation_interconnexions/inference_gateway.py'
  with patch.dict(os.environ,{'JARVIS_MISSIONS_DB':str(self.root/'missions.sqlite'),'QWEN_RECEIPTS':str(self.root/'requests')}):
   spec=importlib.util.spec_from_file_location('readout_gateway_fixture',path);self.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.g)
  self.g.old.EMPTY_MEMORY=self.root/'memory.sqlite'
  with closing(sqlite3.connect(self.g.old.EMPTY_MEMORY)) as db, db:
   db.execute('CREATE TABLE audit(id INTEGER PRIMARY KEY,operation TEXT,target TEXT)')
   target={'request_id':'request','origin':'OpenWebUI','tool':'host_exec','result':{'ok':True,'result':{'stdout':'actual result'}}}
   db.execute('INSERT INTO audit VALUES(1,?,?)',('client_tool_result',json.dumps(target)))
  self.receipt={'tool':'host_exec','client_receipt':{'audit_id':1,'request_id':'request'},'result':{'stdout':'actual result'}}
 def data(self):
  return {'model':'qwen3-coder-next:q4_K_M','messages':[{'role':'system','content':'ALL OWNER CONSTRAINTS'},{'role':'user','content':'Exact owner goal'},{'role':'assistant','content':'','tool_calls':[{'id':'call','function':{'name':'jarvis_call','arguments':{'name':'host_exec','arguments':'{"command":"chosen by model"}'}}}]},{'role':'tool','tool_call_id':'call','content':json.dumps(self.receipt)}],'tools':[{'type':'function','function':{'name':'jarvis_call','description':'x'*6000}}],'tool_choice':'auto','options':{'num_ctx':32768,'num_predict':4096},'stream':True}
 def test_readout_preserves_all_values_and_budget_without_new_tools(self):
  source=self.data();before=copy.deepcopy(source);result,meta=self.g.result_readout(source,budget=4000)
  self.assertEqual(source,before);self.assertEqual(result['messages'][1:-1],before['messages'][1:]);self.assertTrue(result['messages'][0]['content'].startswith(before['messages'][0]['content']))
  self.assertNotIn('tools',result);self.assertNotIn('tool_choice',result);self.assertEqual(result['options'],before['options']);self.assertLessEqual(meta['forwarded_input_bytes'],4000);self.assertEqual(meta['observed_client_receipts'],[1]);self.assertFalse(meta['new_tools_allowed'])
 def test_no_actual_receipt_never_triggers_readout(self):
  data=self.data();data['messages'][-1]['content']='Error: Tool not found.';self.assertIsNone(self.g.result_readout(data,budget=4000))
 def test_wrong_request_identity_or_origin_is_not_a_receipt(self):
  for key,value in [('request_id','invented'),('audit_id',999)]:
   receipt=copy.deepcopy(self.receipt);receipt['client_receipt'][key]=value;self.assertIsNone(self.g.canonical_client_receipt(json.dumps(receipt)))
  with closing(sqlite3.connect(self.g.old.EMPTY_MEMORY)) as db, db:
   stored=json.loads(db.execute('select target from audit').fetchone()[0]);stored['origin']='DifferentClient';db.execute('update audit set target=?',(json.dumps(stored),))
  self.assertIsNone(self.g.canonical_client_receipt(json.dumps(self.receipt)))
 def test_oversized_messages_remain_refused_instead_of_truncated(self):
  data=self.data();data['messages'][1]['content']='Exact large owner requirement '*1000;before=copy.deepcopy(data)
  self.assertIsNone(self.g.result_readout(data,budget=4000));self.assertEqual(data,before)
 def test_structured_contract_and_nontext_inputs_are_preserved(self):
  data=self.data();data['format']={'type':'object'};self.assertIsNone(self.g.result_readout(data,budget=4000));data.pop('format');data['messages'][1]['content']=[{'type':'image','url':'actual source'}];self.assertIsNone(self.g.result_readout(data,budget=4000))
 def test_readout_cannot_emit_any_new_tool_call(self):
  text=json.dumps({'message':{'content':'Actual findings and unknowns'},'done':True}).encode();self.assertTrue(self.g.valid_readout_response(text))
  tool=json.dumps({'message':{'content':'','tool_calls':[{'function':{'name':'jarvis_call'}}]},'done':True}).encode();self.assertFalse(self.g.valid_readout_response(text+b'\n'+tool));self.assertFalse(self.g.valid_readout_response(b'{"message":{"thinking":"only internal reasoning"},"done":true}'))
 def test_empty_tools_or_boolean_checker_does_not_create_readout(self):
  data=self.data();self.assertIsNone(self.g.result_readout(data,budget=4000,receipt_checker=lambda _:False));data['tools']=[];self.assertIsNone(self.g.result_readout(data,budget=4000))

 def serve_readout(self,tool_response=False):
  import threading,urllib.request,urllib.error
  from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
  observed=[];finishes=[]
  class Upstream(BaseHTTPRequestHandler):
   def log_message(self,*args):pass
   def do_POST(self):
    raw=self.rfile.read(int(self.headers['Content-Length']));observed.append(json.loads(raw))
    message={'content':'Actual fixture findings; unknown roles remain.'}
    if tool_response:message={'content':'','tool_calls':[{'function':{'name':'jarvis_call','arguments':{'name':'host_exec','arguments':'not executed'}}}]}
    body=(json.dumps({'message':message,'done':True,'prompt_eval_count':20})+'\n').encode()
    self.send_response(200);self.send_header('Content-Type','application/x-ndjson');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
  class Queue:
   def enter(self,*args,**kwargs):return 'fixture-job'
   def heartbeat(self,*args):pass
   def finish(self,*args,**kwargs):finishes.append(kwargs)
  upstream=ThreadingHTTPServer(('127.0.0.1',0),Upstream);gateway=ThreadingHTTPServer(('127.0.0.1',0),self.g.Handler)
  self.g.UPSTREAM='http://127.0.0.1:'+str(upstream.server_port);self.g.LOG=self.root/'admission.jsonl';self.g.QUEUE=Queue()
  for server in (upstream,gateway):threading.Thread(target=server.serve_forever,daemon=True).start()
  source=self.data();source['tools'][0]['function']['description']='x'*35000;raw=json.dumps(source).encode();result=None;status=None
  try:
   try:
    with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:'+str(gateway.server_port)+'/api/chat',data=raw,headers={'Content-Type':'application/json'}),timeout=10) as response:status=response.status;result=response.read()
   except urllib.error.HTTPError as error:status=error.code;result=error.read()
  finally:
   for server in (gateway,upstream):server.shutdown();server.server_close()
  return source,raw,status,result,observed,finishes
 def test_http_readout_uses_same_model_and_archives_original_without_loss(self):
  source,raw,status,result,observed,finishes=self.serve_readout()
  self.assertEqual(status,200);self.assertTrue(self.g.valid_readout_response(result));self.assertEqual(len(observed),1);self.assertNotIn('tools',observed[0]);self.assertEqual(observed[0]['model'],source['model']);self.assertEqual(observed[0]['messages'][1:-1],source['messages'][1:]);self.assertEqual(observed[0]['options']['num_ctx'],32768)
  archives=list((self.root/'requests').glob('readout-source-*.json'));self.assertEqual(len(archives),1);self.assertEqual(archives[0].read_bytes(),raw);self.assertEqual(archives[0].stat().st_mode&0o777,0o600);self.assertEqual(finishes[0]['metrics']['phase'],'result_readout');self.assertLessEqual(finishes[0]['metrics']['forwarded_input_bytes'],27648)
 def test_http_readout_blocks_model_tool_request_before_forwarding_it(self):
  source,raw,status,result,observed,finishes=self.serve_readout(tool_response=True)
  self.assertEqual(status,409);self.assertNotIn(b'tool_calls',result);self.assertEqual(finishes[0]['metrics']['http_status'],409);self.assertTrue(list((self.root/'requests').glob('readout-response-rejected-*.jsonl')))

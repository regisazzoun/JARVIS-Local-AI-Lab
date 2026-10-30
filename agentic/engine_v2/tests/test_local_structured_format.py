from contextlib import closing
import importlib.util,unittest
from pathlib import Path
PATH=Path(__file__).resolve().parents[3]/'tools/qwen_webui/ollama_guard.py'
spec=importlib.util.spec_from_file_location('local_guard',PATH);guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
class StructuredFormat(unittest.TestCase):
 def base(self):return {'model':'qwen3-coder-next:q4_K_M','messages':[{'role':'user','content':'test'}]}
 def test_json_object_preserved(self):
  data={**self.base(),'response_format':{'type':'json_object'}}
  self.assertEqual(guard.native_payload(data)['format'],'json')
 def test_json_schema_preserved_without_mutation(self):
  schema={'type':'object','properties':{'decision':{'type':'string','enum':['accept','reject']}},'required':['decision'],'additionalProperties':False}
  data={**self.base(),'response_format':{'type':'json_schema','json_schema':{'name':'goal','schema':schema,'strict':True}}}
  result=guard.native_payload(data);self.assertEqual(result['format'],schema)
  result['format']['required'].append('other');self.assertEqual(schema['required'],['decision'])
 def test_unknown_contract_refused(self):
  with self.assertRaises(ValueError):guard.native_payload({**self.base(),'response_format':{'type':'unknown'}})
 def test_normal_text_not_forced_into_json(self):self.assertNotIn('format',guard.native_payload(self.base()))
if __name__=='__main__':unittest.main()

class LocalRelayHTTPContract(unittest.TestCase):
 def exchange(self,data):
  import tempfile,threading,http.client,io
  from http.server import ThreadingHTTPServer
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as tmp:
   previous=guard.ROOT;previous_memory=guard.EMPTY_MEMORY;guard.ROOT=Path(tmp);guard.EMPTY_MEMORY=Path(tmp)/'memory.sqlite'
   import sqlite3
   with closing(sqlite3.connect(guard.EMPTY_MEMORY)) as db, db:db.execute('CREATE TABLE audit(id INTEGER PRIMARY KEY,operation TEXT,target TEXT,created TEXT)')
   upstream=b'{"message":{"content":"{\\"decision\\":\\"accept\\",\\"reason\\":\\"observed\\"}"},"done":false}\n'+b'{"done":true,"prompt_eval_count":50,"eval_count":20}\n'
   server=ThreadingHTTPServer(('127.0.0.1',0),guard.Handler)
   thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
   try:
    with patch.object(guard.urllib.request,'urlopen',return_value=io.BytesIO(upstream)) as native:
     connection=http.client.HTTPConnection(*server.server_address,timeout=3)
     import json
     connection.request('POST','/v1/chat/completions',body=json.dumps(data),headers={'Content-Type':'application/json'})
     response=connection.getresponse();result=(response.status,response.getheader('Content-Type'),response.read())
     payload=json.loads(native.call_args.args[0].data);connection.close()
     return result,payload
   finally:server.shutdown();server.server_close();thread.join();guard.ROOT=previous;guard.EMPTY_MEMORY=previous_memory
 def test_nonstream_verifier_gets_completion_json_not_sse(self):
  import json
  result,payload=self.exchange({'model':'qwen3-coder-next:q4_K_M','messages':[{'role':'user','content':'judge'}],'stream':False,'response_format':{'type':'json_object'}})
  status,mime,raw=result;self.assertEqual(status,200);self.assertEqual(mime,'application/json')
  data=json.loads(raw);self.assertEqual(data['object'],'chat.completion');self.assertEqual(json.loads(data['choices'][0]['message']['content'])['decision'],'accept');self.assertEqual(data['usage']['total_tokens'],70);self.assertEqual(payload['format'],'json')
 def test_streaming_chat_keeps_sse(self):
  result,payload=self.exchange({'model':'qwen3-coder-next:q4_K_M','messages':[{'role':'user','content':'chat'}],'stream':True})
  self.assertEqual(result[1],'text/event-stream');self.assertIn(b'data: [DONE]',result[2]);self.assertNotIn('format',payload)

class EmptyResponsePersistence(unittest.TestCase):
 def test_transport_incidents_persist_without_functional_counter_reset(self):
  import tempfile,sqlite3
  with tempfile.TemporaryDirectory() as tmp:
   old=guard.EMPTY_MEMORY;guard.EMPTY_MEMORY=Path(tmp)/'memory.sqlite'
   try:
    with closing(sqlite3.connect(guard.EMPTY_MEMORY)) as db, db:db.execute('CREATE TABLE audit(id INTEGER PRIMARY KEY,operation TEXT,target TEXT,created TEXT)')
    for expected in (1,2,3):self.assertEqual(guard.empty_response_count('same',True),expected)
    self.assertEqual(guard.empty_response_count('same'),3);self.assertEqual(guard.empty_response_count('changed'),0)
   finally:guard.EMPTY_MEMORY=old

class EmptyFourthDispatch(unittest.TestCase):
 def test_fourth_identical_empty_request_stops_before_upstream(self):
  import tempfile,threading,http.client,json
  from http.server import ThreadingHTTPServer
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as tmp:
   old=guard.ROOT;guard.ROOT=Path(tmp)
   server=ThreadingHTTPServer(('127.0.0.1',0),guard.Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
   try:
    with patch.object(guard,'empty_response_count',return_value=3),patch.object(guard.urllib.request,'urlopen',side_effect=AssertionError('fourth inference')) as upstream:
     connection=http.client.HTTPConnection(*server.server_address,timeout=3)
     connection.request('POST','/v1/chat/completions',body=json.dumps({'model':'qwen3-coder-next:q4_K_M','messages':[{'role':'user','content':'fixture'}],'stream':True}),headers={'Content-Type':'application/json'})
     response=connection.getresponse();self.assertEqual(response.status,400);self.assertIn(b'No fourth inference',response.read());connection.close();upstream.assert_not_called()
   finally:server.shutdown();server.server_close();thread.join();guard.ROOT=old

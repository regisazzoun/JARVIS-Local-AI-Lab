"""HTTP handler tests without sockets: not browser/end-to-end validation."""
import unittest,io,json,tempfile
from pathlib import Path
from types import SimpleNamespace
from jarvis.memory import Memory
from jarvis.core import Core,ROOT
from jarvis.server import make_handler
class API(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.m=Memory(Path(self.tmp.name)/'memory.sqlite');self.c=Core(json.loads((ROOT/'config/example.json').read_text()),self.m,lambda p:'Réponse fictive');self.H=make_handler(self.c)
 def tearDown(self):self.tmp.cleanup()
 def request(self,path,data=None,headers=None):
  h=self.H.__new__(self.H);h.path=path;h.server=SimpleNamespace(server_port=8765);raw=json.dumps(data).encode() if data is not None else b''
  h.headers={'Host':'localhost:8765','Origin':'http://localhost:8765','X-Jarvis-Request':'1','Content-Length':str(len(raw))};h.headers.update(headers or {});h.rfile=io.BytesIO(raw);h.wfile=io.BytesIO();h.send_response=lambda code:setattr(h,'code',code);h.send_header=lambda *a:None;h.end_headers=lambda:None
  h.do_POST() if data is not None else h.do_GET()
  return h.code,h.wfile.getvalue()
 def test_static_and_security(self):
  self.assertEqual(self.request('/')[0],200)
  self.assertEqual(self.request('/api/config')[0],200)
  self.assertEqual(self.request('/api/export',headers={'Host':'evil.example'})[0],403)
  self.assertEqual(self.request('/api/memory/propose',{'content':'Fictif'},headers={'Origin':'https://evil.example'})[0],403)
  self.assertEqual(self.request('/api/memory/propose',{'content':'Fictif'},headers={'X-Jarvis-Request':''})[0],403)
  self.assertEqual(self.m.list_memories(),[])
 def test_memory_endpoints(self):
  code,body=self.request('/api/memory/propose',{'content':'Orion fictif'});self.assertEqual(code,200);id=json.loads(body)['id']
  self.assertEqual(self.request('/api/search?q=Orion')[1],b'[]')
  self.assertEqual(self.request('/api/memory/approve',{'id':id})[0],400)
  self.assertEqual(self.request('/api/memory/approve',{'id':id,'explicit':True})[0],200)
  self.assertIn(b'Orion',self.request('/api/search?q=Orion')[1])
  self.assertEqual(self.request('/api/memory/edit',{'id':id,'content':'Orion bleu','explicit':True})[0],200)
  self.assertEqual(self.request('/api/memory/delete',{'id':id})[0],200)
  self.assertEqual(self.request('/api/search?q=Orion')[1],b'[]')
 def test_chat_continuity_and_errors(self):
  code,body=self.request('/api/chat',{'text':'Bonjour fictif','model':'llama3.1:8b'});self.assertEqual(code,200);id=json.loads(body)['conversation']
  self.assertEqual(self.request('/api/chat',{'text':'Suite fictive','model':'qwen3.5:27b-q4_K_M','conversation':id})[0],200)
  self.assertEqual(len(json.loads(self.request('/api/history?id='+id)[1])),4)
  self.assertEqual(self.request('/api/chat',{'text':'','model':'llama3.1:8b'})[0],400)
  self.assertEqual(self.request('/api/chat',{'text':'x','model':'llama3.1:8b','retain':'false'})[0],400)
  self.c.transport=lambda p:(_ for _ in ()).throw(ConnectionError())
  self.assertEqual(self.request('/api/chat',{'text':'Erreur fictive','model':'llama3.1:8b'})[0],503)

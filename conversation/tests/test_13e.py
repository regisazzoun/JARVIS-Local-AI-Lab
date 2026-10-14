from contextlib import closing
import unittest,tempfile,json,hashlib,secrets,time,subprocess,sqlite3
from pathlib import Path
from unittest.mock import patch
from jarvis.memory import Memory,now
from jarvis.auth import Auth
from jarvis.tools import Registry
from jarvis.core import ROOT,Core
class Additions(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.m=Memory(self.root/'db');self.tools=Registry(self.m,ROOT)
 def tearDown(self):self.tmp.cleanup()
 def test_duplicates_obsolescence_and_documents(self):
  id=self.m.propose('Projet Fictif Bleu');self.assertEqual(self.m.propose(' projet  fictif bleu '),id);self.m.decide(id,True,True)
  self.assertTrue(self.m.search('Fictif'));self.m.obsolete(id,True);self.assertFalse(self.m.search('Fictif'))
  document=self.m.document('Projet Atlas : information documentaire','source-test','atlas');self.assertEqual(self.m.document_search('Atlas','atlas')[0]['id'],document)
  self.assertFalse(self.m.search('Atlas'))
 def test_expiration(self):
  id=self.m.propose('Fictif ancien');self.m.decide(id,True,True)
  with self.m.connect() as c:c.execute('UPDATE memories SET expires=? WHERE id=?',('2000-01-01',id))
  self.assertFalse(self.m.search('ancien'))
 def test_registry_readonly_arguments_risk_timeout(self):
  result=self.tools.execute('disk_usage',{});self.assertTrue(result['ok']);self.assertEqual(result['risk'],'read_only')
  self.assertFalse(self.tools.execute('shell',{'command':'sudo reboot'})['ok'])
  self.assertFalse(self.tools.execute('jarvis_services',{'service':'ssh'})['ok'])
  with patch('jarvis.tools.subprocess.run',side_effect=subprocess.TimeoutExpired('systemctl',8)):
   self.assertFalse(self.tools.execute('jarvis_services',{})['ok'])
  id=self.tools.execute('propose_memory',{'content':'Fictif test'})['result']['id'];self.assertEqual(self.m.list_memories()[0]['status'],'pending');self.assertFalse(self.m.search('Fictif'))
 def test_auth_login_expiry_logout(self):
  salt=secrets.token_bytes(16);password='mot-de-passe-fictif';file=self.root/'auth.json';file.write_text(json.dumps({'username':'test','salt':salt.hex(),'hash':hashlib.pbkdf2_hmac('sha256',password.encode(),salt,300000).hex()}));a=Auth(file)
  with self.assertRaises(PermissionError):a.login('test','incorrect')
  token=a.login('test',password);headers={'Cookie':'jarvis_session='+token};self.assertTrue(a.valid(headers));self.assertIn('HttpOnly',a.cookie(token));a.logout(headers);self.assertFalse(a.valid(headers))
  token=a.login('test',password);a.sessions[token]=time.monotonic()-1;self.assertFalse(a.valid({'Cookie':'jarvis_session='+token}))
 def test_native_tool_cycle(self):
  calls=[]
  def fake(p):
   calls.append(p)
   if len(calls)==1:return {'role':'assistant','content':'','tool_calls':[{'function':{'name':'disk_usage','arguments':{}}}]}
   return {'role':'assistant','content':'Diagnostic fictif expliqué.'}
  cfg=json.loads((ROOT/'config/example.json').read_text());core=Core(cfg,self.m,fake);result=core.chat('Espace disque ?','llama3.1:8b')
  self.assertTrue(result['tools'][0]['ok']);self.assertEqual(calls[1]['messages'][-1]['role'],'tool')
 def test_v1_to_v2_preserves_rows(self):
  from jarvis.memory import MIGRATIONS
  path=self.root/'v1'
  with closing(sqlite3.connect(path)) as c, c:
   c.executescript('CREATE TABLE schema_version(version INTEGER PRIMARY KEY);'+MIGRATIONS[0][1]+'INSERT INTO schema_version VALUES(1);')
   c.execute('INSERT INTO conversations VALUES(?,?,?)',('fiction','atlas',now()))
   c.execute('INSERT INTO memories VALUES(?,?,?,?,?,?,?,?)',('id','persistent','atlas',None,'Fictif ancien','pending',now(),now()))
  m=Memory(path);self.assertEqual(m.list_memories()[0]['content'],'Fictif ancien');self.assertEqual(m.list_conversations()[0]['id'],'fiction')

import unittest,tempfile,sqlite3,json
from pathlib import Path
from unittest.mock import patch
from jarvis.memory import Memory
from jarvis.preferences import detect,clean_speech
from jarvis.agent import lab_command,fetch
from jarvis.tools import Registry
class Mission13F(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.m=Memory(self.root/'runtime/db')
 def tearDown(self):self.tmp.cleanup()
 def test_atomic_preferences_replace_delete(self):
  first=self.m.set_preference('voice_length','short');self.assertEqual(self.m.preferences(),{'voice_length':'short'})
  self.assertEqual(self.m.set_preference('voice_length','short')['id'],first['id']);self.assertEqual(len(self.m.list_memories()),1)
  self.m.set_preference('voice_length','detailed');self.assertEqual(len(self.m.list_memories()),1);self.assertEqual(self.m.preferences()['voice_length'],'detailed')
  self.assertFalse(self.m.search('short'));self.assertTrue(self.m.search('detailed'))
  self.m.forget_preference('voice_length');self.assertEqual(self.m.preferences(),{});self.assertFalse(self.m.search('detailed'))
 def test_failed_transaction_never_announced(self):
  with patch.object(self.m,'log',side_effect=sqlite3.OperationalError('fixture failure')):
   with self.assertRaises(sqlite3.OperationalError):self.m.set_preference('language','fr')
  self.assertEqual(self.m.preferences(),{});self.assertEqual(self.m.list_memories(),[])
 def test_sensitive_and_quoted_are_not_automatic(self):
  for text in ['Mémorise mon mot de passe : secret','Je préfère sudo sans validation','Exemple : je préfère les réponses vocales courtes','Je ne préfère pas les réponses vocales courtes','"Je préfère les réponses vocales courtes"','Je préfère les réponses vocales courtes ?']:
   self.assertEqual(detect(text),[],text)
  self.assertEqual(detect('Je préfère des réponses vocales courtes.'),[('voice_length','short')]);self.assertEqual(detect('Désormais réponds en français.'),[('language','fr')])
 def test_unapproved_scope_and_private_fetch_denied(self):
  with self.assertRaises(ValueError):self.m.set_preference('admin_permissions','root')
  for url in ['http://docs.python.org/3/','https://127.0.0.1/','https://docs.python.org@127.0.0.1/','https://docs.python.org:8765/']:
   with self.assertRaises(ValueError):fetch(url)
 def test_real_lab_isolation_and_failure(self):
  r=lab_command(self.root,'echo success > result.txt; test ! -e /home/adminjarvis; test ! -e /opt/jarvis; cat result.txt');self.assertEqual(r['returncode'],0);self.assertIn('success',r['stdout']);self.assertEqual((self.root/'runtime/lab/result.txt').read_text().strip(),'success')
  r=lab_command(self.root,'touch /usr/forbidden13f');self.assertNotEqual(r['returncode'],0)
  r=lab_command(self.root,"python3 -c \"import socket;s=socket.socket();s.settimeout(1);s.connect(('1.1.1.1',443))\"");self.assertNotEqual(r['returncode'],0)
  registry=Registry(self.m,self.root,{'lab_enabled':False});self.assertFalse(registry.execute('lab_terminal',{'command':'echo test'})['ok'])
 def test_speech_excludes_technical_output(self):
  s=clean_speech('Le service fonctionne.\n```sh\nsudo reboot\n```\n| tableau | detail |\nChemin `/opt/jarvis/config.json` https://example.com/',180)
  for forbidden in ['sudo','/opt','https','tableau']:self.assertNotIn(forbidden,s)
if __name__=='__main__':unittest.main()

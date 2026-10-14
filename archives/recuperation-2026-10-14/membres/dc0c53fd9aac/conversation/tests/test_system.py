import unittest,tempfile,json,sqlite3
from pathlib import Path
from jarvis.memory import Memory
from jarvis.core import Core,ROOT,Busy

class Suite(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'db.sqlite';self.m=Memory(self.path);self.cfg=json.loads((ROOT/'config/example.json').read_text());self.calls=[]
  def fake(p):self.calls.append(p);return 'Réponse fictive de test'
  self.core=Core(self.cfg,self.m,transport=fake)
 def tearDown(self):self.tmp.cleanup()
 def test_shared_three_models_explicit_delete(self):
  r=self.core.chat('Bonjour fictif','llama3.1:8b');cid=r['conversation'];id=self.m.propose('Le projet fictif Orion utilise la couleur turquoise',project='')
  self.assertEqual(self.m.search('Orion'),[])
  with self.assertRaises(ValueError):self.m.decide(id,True)
  self.m.decide(id,True,explicit=True)
  for model in ['ministral-3:14b-instruct-2512-q4_K_M','qwen3.5:27b-q4_K_M']:
   result=self.core.chat('Quelle couleur pour Orion ?',model,cid)
   self.assertEqual(result['memories_used'],[id]);self.assertIn('turquoise',self.calls[-1]['messages'][0]['content'])
  self.assertEqual(len(self.m.history(cid)),6);self.m.delete(id)
  self.assertEqual(self.core.chat('Orion ?',self.cfg['default_model'],cid)['memories_used'],[])
 def test_rejection_edit_project_and_temporary(self):
  id=self.m.propose('Refus fictif');self.m.decide(id,False);self.assertFalse(self.m.search('Refus'))
  id=self.m.propose('Orion turquoise',project='alpha');self.m.decide(id,True,True)
  self.assertFalse(self.m.search('Orion',project='beta'));self.m.edit(id,'Orion bleu','beta',True)
  self.assertTrue(self.m.search('bleu',project='beta'));self.assertFalse(self.m.search('turquoise'))
  id=self.m.propose('Temporaire fictif','temporary',conversation='session')
  self.assertFalse(self.m.search('Temporaire'));self.assertTrue(self.m.search('Temporaire',conversation='session'))
 def test_backup_restore_restart_export_migrations(self):
  id=self.m.propose('Souvenir fictif permanent');self.m.decide(id,True,True)
  backup=Path(self.tmp.name)/'backup';self.m.backup(backup);restored=Memory.restore(backup,Path(self.tmp.name)/'restored')
  self.assertEqual(restored.search('fictif')[0]['id'],id);self.assertEqual(Memory(self.path).export(),self.m.export())
  with self.assertRaises(ValueError):Memory.restore(backup,self.path)
  with sqlite3.connect(self.path) as c:self.assertEqual(c.execute('SELECT version FROM schema_version').fetchall(),[(1,)])
 def test_no_retention_and_history_search(self):
  r=self.core.chat('Échange fictif','llama3.1:8b',retain=False)
  self.core.chat('Continuité fictive','qwen3.5:27b-q4_K_M',r['conversation'],retain=False)
  self.assertEqual(self.m.list_conversations(),[]);self.assertEqual(self.m.export()['messages'],[])
  r=self.core.chat('Recherche fictive','llama3.1:8b');self.assertTrue(self.m.search('Recherche',messages=True))
  self.m.prune(-1);self.assertFalse(self.m.history(r['conversation']));self.assertFalse(self.m.search('Recherche',messages=True))
 def test_errors_and_serialization(self):
  with self.assertRaises(ValueError):self.core.chat('','llama3.1:8b')
  with self.assertRaises(ValueError):self.core.chat('x','inconnu')
  self.core.lock.acquire()
  try:
   with self.assertRaises(Busy):self.core.chat('x','llama3.1:8b')
  finally:self.core.lock.release()
  def fail(p):raise ConnectionError('fictif')
  self.core.transport=fail
  with self.assertRaises(ConnectionError):self.core.chat('x','llama3.1:8b')
  self.assertEqual(self.m.export()['messages'],[]);self.assertFalse(self.core.lock.locked())
 def test_failed_transaction_and_literal_fts(self):
  with self.assertRaises(sqlite3.IntegrityError):self.m.exchange('absent','fictif','fictif','llama3.1:8b')
  self.assertFalse(self.m.export()['messages']);self.assertEqual(self.m.search('" OR * --'),[])

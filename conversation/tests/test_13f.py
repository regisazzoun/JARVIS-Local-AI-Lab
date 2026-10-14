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
  r=lab_command(self.root,'echo success > result.txt; test ! -e /home; test ! -e /opt/jarvis; cat result.txt');self.assertEqual(r['returncode'],0);self.assertIn('success',r['stdout']);self.assertEqual((self.root/'runtime/lab/result.txt').read_text().strip(),'success')
  r=lab_command(self.root,'touch /usr/forbidden13f');self.assertNotEqual(r['returncode'],0)
  r=lab_command(self.root,"python3 -c \"import socket;s=socket.socket();s.settimeout(1);s.connect(('1.1.1.1',443))\"");self.assertNotEqual(r['returncode'],0)
  registry=Registry(self.m,self.root,{'lab_enabled':False});self.assertFalse(registry.execute('lab_terminal',{'command':'echo test'})['ok'])
 def test_speech_excludes_technical_output(self):
  s=clean_speech('Le service fonctionne.\n```sh\nsudo reboot\n```\n| tableau | detail |\nChemin `/opt/jarvis/config.json` https://example.com/',180)
  for forbidden in ['sudo','/opt','https','tableau']:self.assertNotIn(forbidden,s)
 def test_agent_continues_plan_and_preserves_goal_under_long_output(self):
  from jarvis.core import Core,ROOT
  cfg=json.loads((ROOT/'config/example.json').read_text());cfg.update(lab_enabled=True,tool_rounds=4,voice_summary=False)
  calls=[]
  def model(payload):
   calls.append(payload)
   if len(calls)==1:return {'role':'assistant','content':'Je prépare le plan.'}
   if len(calls)==2:return {'role':'assistant','content':'','tool_calls':[{'function':{'name':'system_status','arguments':{}}}]}
   if len(calls)==3:
    self.assertTrue(any(m.get('content')=='objectif fictif laboratoire' for m in payload['messages']))
    self.assertLess(sum(len(json.dumps(m)) for m in payload['messages']),11000)
    return {'role':'assistant','content':'','tool_calls':[{'function':{'name':'intervention_report','arguments':{'content':'Rapport fictif de simulation.'}}}]}
   return {'role':'assistant','content':'Terminé pour la simulation.'}
  core=Core(cfg,self.m,model);core.tools=Registry(self.m,self.root,cfg)
  core.tools.specs['system_status']=('Long observation',{},[],'read_only',lambda a:{'stdout':'fixture '*4000})
  r=core.chat('objectif fictif laboratoire',cfg['default_model'],agent_mode=True)
  self.assertEqual(len(calls),4);self.assertTrue((self.root/'runtime/lab/intervention.md').exists());self.assertNotIn('incomplète',r['answer'])
 def test_agent_exhaustion_never_claims_completion(self):
  from jarvis.core import Core,ROOT
  cfg=json.loads((ROOT/'config/example.json').read_text());cfg.update(tool_rounds=1,voice_summary=False)
  core=Core(cfg,self.m,lambda p:'Un plan uniquement.');r=core.chat('objectif fictif laboratoire',cfg['default_model'],agent_mode=True)
  self.assertIn('Intervention incomplète',r['answer'])
 def test_textual_tool_adapter_cannot_bypass_permission_scope(self):
  from jarvis.core import Core,ROOT
  cfg=json.loads((ROOT/'config/example.json').read_text());cfg.update(tool_rounds=2,voice_summary=False)
  replies=iter(['active_memories[ARGS]{}','Préférence disponible.'])
  core=Core(cfg,self.m,lambda p:next(replies));core.tools=Registry(self.m,self.root,cfg)
  r=core.chat('Question fictive',cfg['default_model']);self.assertTrue(r['tools'][0]['ok']);self.assertEqual(r['tools'][0]['tool'],'active_memories')
  replies=iter(['lab_terminal[ARGS]{"command":"echo denied"}','Exécution refusée.'])
  core.transport=lambda p:next(replies);r=core.chat('Question fictive',cfg['default_model']);self.assertFalse(r['tools'][0]['ok'])
 def test_lab_workspace_quota_detected_and_recoverable(self):
  with patch('jarvis.agent.MAX_LAB_BYTES',1024):
   r=lab_command(self.root,"python3 -c \"open('quota-fixture','wb').write(b'x'*4096)\"")
   self.assertTrue(r['quota_exceeded']);self.assertNotEqual(r['returncode'],0)
   r=lab_command(self.root,'rm quota-fixture');self.assertFalse(r['quota_exceeded']);self.assertEqual(r['returncode'],0)
 def test_non_sensitive_operating_instructions_are_durable(self):
  cases={'Désormais cite toujours tes sources.':('sources','cite'),'Désormais vérifie toujours tes résultats avant de conclure.':('verification','always'),'Je préfère le tutoiement.':('address_style','tu'),'Désormais utilise le système métrique.':('units','metric')}
  for text,expected in cases.items():
   self.assertIn(expected,detect(text));self.m.set_preference(*expected);self.assertEqual(self.m.preferences()[expected[0]],expected[1])
 def test_report_cannot_claim_consultation_without_real_fetch(self):
  registry=Registry(self.m,self.root,{'lab_enabled':True});registry.context={'lab_authorized':True,'research_required':True,'verified_sources':[]}
  self.assertFalse(registry.execute('intervention_report',{'content':'Rapport fictif'})['ok'])
  registry.context['verified_sources']=['https://docs.python.org/3/library/configparser.html','https://docs.python.org/3.13/library/configparser.html#exceptions']
  self.assertFalse(registry.execute('intervention_report',{'content':'Rapport fictif'})['ok'])
  registry.context['verified_sources'].append('https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html')
  self.assertTrue(registry.execute('intervention_report',{'content':'Rapport fictif de validation'})['ok'])
if __name__=='__main__':unittest.main()

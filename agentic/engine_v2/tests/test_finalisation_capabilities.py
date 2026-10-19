import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]));sys.path.insert(0,str(Path(__file__).parents[1]/'broker'))
from jarvis.intent import classify
from github_connector import relative_path,check_content,branch_name
class Finalisation(unittest.TestCase):
 def test_questions_never_launch(self):
  for text in ["Quel est l'état de la mission 23 ?","Pourquoi t12 a-t-elle échoué ?","quel est le blocage technique de la tache 12"]:self.assertEqual(classify(text),'question')
 def test_execution_routing(self):
  self.assertEqual(classify('Reprends la mission 23 et termine les tâches restantes'),'resume23')
  self.assertEqual(classify('Lance la mission 24 — Mémoire enrichie'),'execute')
 def test_publication_private_paths(self):
  for p in ['.env','livekit-agent/.env','../secret','/etc/passwd','x/.git/config','node_modules/index.js']:
   with self.assertRaises((ValueError,PermissionError)):relative_path(p)
 def test_secret_rejected(self):
  for content in [b'github_pat_ABCDEF',b'-----BEGIN RSA PRIVATE KEY-----',b'LIVEKIT_API_SECRET="actual-secret-123"']:
   with self.assertRaises(PermissionError):check_content('config.py',content)
 def test_safe_sources(self):check_content('agent.py',b'api_secret = os.environ.get("LIVEKIT_API_SECRET")')
 def test_branches(self):
  for b in ['main','other/branch','jarvis/../main']:
   with self.assertRaises(PermissionError):branch_name(b)

class PublicationRecovery(unittest.TestCase):
 def invoke(self,changed,push_error=False):
  import json,os,pwd,base64
  from github_connector import execute
  calls=[]
  def run(argv,*args):
   calls.append(argv)
   if argv[1:3]==['repo','clone']:Path(argv[4]).mkdir()
   if 'diff' in argv:return {'returncode':1 if changed else 0,'stdout':''}
   if 'push' in argv and push_error:return {'returncode':1,'stdout':'','stderr':'non-fast-forward'}
   if 'rev-parse' in argv or '--jq' in argv:return {'returncode':0,'stdout':'abc123\n'}
   return {'returncode':0,'stdout':'{}'}
  sandbox=lambda *a,**k:{'returncode':0,'stdout':json.dumps({'src/main.py':base64.b64encode(b'print(1)').decode()})}
  result=execute({'repository':'owner/repo','action':'push_tree','branch':'jarvis/test','path':'/tmp','files':'["src/main.py"]'},{'user':pwd.getpwuid(os.getuid()).pw_name,'write_roots':['/tmp']},run,sandbox,lambda p,roots:Path(p))
  return result,calls
 def test_repeated_snapshot_no_duplicate_commit(self):
  r,calls=self.invoke(False);self.assertTrue(r['verified']);self.assertFalse(r['changed']);self.assertFalse(any('commit' in c or 'push' in c for c in calls))
 def test_branch_conflict_is_not_force_pushed(self):
  r,calls=self.invoke(True,True);self.assertEqual(r['returncode'],1);self.assertIn('retry',r['diagnostic']);self.assertFalse(any('--force' in c for c in calls))

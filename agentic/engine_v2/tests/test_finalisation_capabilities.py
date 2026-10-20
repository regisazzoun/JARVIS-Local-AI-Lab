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
class DeliveryContract(unittest.TestCase):
 def test_required_files_ignore_json_spacing_and_allow_additional_sources(self):
  from jarvis.mission_store import arguments_match
  self.assertTrue(arguments_match({'files':'["b.py","a.py","extra.py"]'},{'files':'["a.py", "b.py"]'}))
  self.assertFalse(arguments_match({'files':'["a.py"]'},{'files':'["a.py", "b.py"]'}))
class RemoteProjectScope(unittest.TestCase):
 def test_ungranted_project_and_non_admin_profile_are_denied(self):
  import importlib.util
  spec=importlib.util.spec_from_file_location('scope_bridge',Path(__file__).parents[1]/'broker/host_bridge.py');bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)
  profile={'identity':'/private/key','known_hosts':'/private/known','user':'admin','address':'192.0.2.1','allow_admin':True,'administration_operations':['project_exec'],'project_exec_projects':['mission23']}
  args={'host':'dell','action':'project_exec','project':'other-project','command':'true'}
  with self.assertRaises(PermissionError):bridge.execute('host_remote',args,{'remote_hosts':{'dell':profile}})
  profile['allow_admin']=False;args['project']='mission23'
  with self.assertRaises(PermissionError):bridge.execute('host_remote',args,{'remote_hosts':{'dell':profile}})
class PrRecovery(unittest.TestCase):
 def test_existing_pr_is_updated_without_duplicate(self):
  from github_connector import execute
  calls=[]
  def run(argv,*args):
   calls.append(argv)
   if 'list' in argv:return {'returncode':0,'stdout':'[{"number":14,"url":"https://example.test/pr/14"}]'}
   import json
   payload=json.loads(Path(argv[argv.index('--input')+1]).read_text());self.assertEqual(payload['body'],'line1\nline2');self.assertEqual(payload['title'],'Updated scope')
   return {'returncode':0,'stdout':json.dumps({'number':14,'url':'https://example.test/pr/14','head':'jarvis/test'})}
  execute({'action':'pull_request','repository':'owner/repo','branch':'jarvis/test','title':'Updated scope','body':'line1\nline2'},{'user':'test'},run,None,None)
  self.assertFalse(any('create' in c for c in calls));self.assertIn('PATCH',calls[-1])
class CurrentServiceLogs(unittest.TestCase):
 def test_current_activation_newest_errors_are_not_hidden_by_old_startup_logs(self):
  from project_service import execute
  calls=[]
  def run(argv,*args,**kwargs):
   calls.append((argv,kwargs))
   return {'returncode':0,'stdout':'a'*32 if 'InvocationID' in ' '.join(argv) else 'latest failure first'}
  result=execute({'project':'mission23','name':'livekit-agent','action':'logs'},{'project_services':{'mission23':'/tmp/m23'},'write_roots':['/tmp']},run,None)
  self.assertIn('--reverse',calls[-1][0]);self.assertIn('_SYSTEMD_INVOCATION_ID='+'a'*32,calls[-1][0]);self.assertTrue(result['current_activation_only']);self.assertEqual(result['journal_order'],'newest_first')

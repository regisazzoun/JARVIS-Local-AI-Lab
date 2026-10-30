import importlib.util,json,unittest
from pathlib import Path
from unittest.mock import Mock
path=Path(__file__).resolve().parents[1]/'broker/github_connector.py'
spec=importlib.util.spec_from_file_location('github_scoped_search',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Search(unittest.TestCase):
 def test_repository_qualifier_cannot_override_scope(self):
  run=Mock()
  with self.assertRaises(ValueError):module.execute({'action':'search_code','repository':'a/b','query':'repo:other/private'}, {'user':'operator'},run,None,None)
  run.assert_not_called()
 def test_partial_result_kept_and_default_branch_limit_explained(self):
  run=Mock(return_value={'returncode':0,'stdout':json.dumps({'total_count':1,'incomplete_results':True,'items':[{'repository':{'full_name':'a/b'},'path':'file.py','sha':'1'}]})})
  result=module.execute({'action':'search_code','repository':'a/b','query':'foo'}, {'user':'operator'},run,None,None)
  data=json.loads(result['stdout']);self.assertTrue(data['incomplete_results']);self.assertEqual(data['items'][0]['path'],'file.py');self.assertIn('repo%3Aa%2Fb',run.call_args.args[0][2])
 def test_unexpected_repository_response_refused(self):
  run=Mock(return_value={'returncode':0,'stdout':json.dumps({'items':[{'repository':{'full_name':'other/private'}}]})})
  with self.assertRaises(PermissionError):module.execute({'action':'search_code','repository':'a/b','query':'foo'}, {'user':'operator'},run,None,None)

class ImmutableTree(unittest.TestCase):
 def test_verification_resolves_commit_then_immutable_tree(self):
  import base64,hashlib
  data=b'fixture';blob=hashlib.sha1(b'blob 7\0'+data).hexdigest()
  run=Mock(side_effect=[{'returncode':0,'stdout':json.dumps({'commit':'c'*40,'tree':'t'*40})},{'returncode':0,'stdout':json.dumps({'sha':'t'*40,'tree':[{'path':'doc.md','sha':blob,'type':'blob'}],'truncated':False})}])
  sandbox=Mock(return_value={'returncode':0,'stdout':json.dumps({'doc.md':base64.b64encode(data).decode()})})
  result=module.execute({'action':'verify_tree','repository':'a/b','branch':'jarvis/scratch','path':'/tmp/source','files':'["doc.md"]'}, {'user':'operator','write_roots':['/tmp']},run,sandbox,lambda *args:Path('/tmp/source'))
  self.assertTrue(result['verified']);self.assertEqual(json.loads(result['stdout'])['commit_sha'],'c'*40);self.assertIn('/git/trees/'+'t'*40,run.call_args_list[1].args[0][2])

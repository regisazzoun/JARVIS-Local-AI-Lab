import importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('bridge',Path(__file__).parents[1]/'broker/host_bridge.py')
bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)
class GithubPaths(unittest.TestCase):
 def test_file_alias_is_respected(self):
  with patch.object(bridge,'run',return_value={'returncode':0,'stdout':'{}'} ) as run:
   result=bridge.execute('host_github',{'repository':'owner/repo','action':'file','file':'SUIVI.md','branch':'jarvis/21'},{'repositories':['owner/repo'],'user':'test'})
   self.assertIn('repos/owner/repo/contents/SUIVI.md?ref=jarvis%2F21',run.call_args.args[0])
   self.assertEqual(result['github_path'],'SUIVI.md')
 def test_ambiguous_file_is_rejected(self):
  with self.assertRaises(ValueError):bridge.execute('host_github',{'repository':'owner/repo','action':'file','path':'README.md','file':'SUIVI.md'},{'repositories':['owner/repo']})

 def test_identical_download_does_not_write_or_claim_a_change(self):
  original=bridge.execute;content='Existing roadmap contents'
  def execute(operation,args,cfg):
   if operation=='host_github':return original(operation,args,cfg)
   self.assertEqual(operation,'host_read_file')
   return {'returncode':0,'stdout':content}
  with patch.object(bridge,'run',return_value={'returncode':0,'stdout':json.dumps({'content':content})}),patch.object(bridge,'execute',side_effect=execute):
   result=bridge.execute('host_github',{'repository':'owner/repo','action':'download','path':'ROADMAP.md','destination':'/work/ROADMAP.md'},{'repositories':['owner/repo'],'user':'test'})
  self.assertFalse(result['changed'])
  self.assertTrue(json.loads(result['stdout'])['verified'])

 def test_append_preserves_project_history(self):
  self.assertTrue(bridge.preserves_project_document('# All missions\n01: done\n02: pending\n','# All missions\n01: done\n02: pending\n\nMission21: blocked'))
 def test_mission_only_summary_cannot_replace_project_history(self):
  self.assertFalse(bridge.preserves_project_document('# All missions\n01: done\n02: pending\n','# Mission21: blocked'))
 def test_privacy_redaction_is_allowed_when_preserving_history(self):
  self.assertTrue(bridge.preserves_project_document('Target 192.168.1.1\n01: done\n','Target [adresse privée masquée]\n01: done\n\n21: blocked'))

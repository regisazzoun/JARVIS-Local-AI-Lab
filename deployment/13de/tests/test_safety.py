import importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('controller',Path(__file__).parents[1]/'lab/controller.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
class Safety(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.patch=patch.object(c,'ROOT',Path(self.tmp.name)/'runtime');self.patch.start();self.addCleanup(self.patch.stop)
 def test_path_escape(self):
  for x in ['../../etc','/dev/nvme0n1','vm-../a','vm-a;id','dell','vm-']:
   with self.assertRaises(ValueError):c.workspace(x)
 def test_symlink_rejected(self):
  c.ROOT.mkdir();(c.ROOT/'vm-a').symlink_to('/tmp',target_is_directory=True)
  with self.assertRaises(ValueError):c.workspace('vm-a')
 def test_delete_requires_owner(self):
  p=c.workspace('vm-a');p.mkdir();(p/'owner.json').write_text('{}')
  with self.assertRaises(ValueError):c.dispatch('destroy','vm-a')
  self.assertTrue(p.exists())
 def test_delete_owned_only(self):
  p=c.workspace('vm-a');p.mkdir();(p/'owner.json').write_text(json.dumps({'mission':'13D-E','name':'vm-a'}))
  sibling=c.workspace('vm-b');sibling.mkdir()
  c.dispatch('destroy','vm-a');self.assertTrue(sibling.exists());self.assertFalse(p.exists())
 def test_nested_link_rejected(self):
  p=c.workspace('vm-a');p.mkdir();(p/'owner.json').write_text(json.dumps({'mission':'13D-E','name':'vm-a'}));(p/'bad').symlink_to('/etc/passwd')
  with self.assertRaises(ValueError):c.dispatch('destroy','vm-a')
 def test_missing_assets_fail_closed(self):
  p=c.workspace('vm-a');p.mkdir();(p/'owner.json').write_text(json.dumps({'mission':'13D-E','name':'vm-a'}))
  with patch.object(c,'ASSETS',Path(self.tmp.name)/'missing'):
   with self.assertRaises(RuntimeError):c.command(p)
if __name__=='__main__':unittest.main()

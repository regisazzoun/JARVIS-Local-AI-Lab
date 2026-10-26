import importlib.util, pathlib, subprocess, tempfile, unittest, json
spec=importlib.util.spec_from_file_location('authority_edit',pathlib.Path(__file__).parents[1]/'jarvis/distributed_authority.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
class LiteralEditTests(unittest.TestCase):
 def run_edit(self,root,edits):
  return subprocess.run(['python3','-c',a.edit_program(edits)],cwd=root,text=True,capture_output=True)
 def test_contents_are_literal_and_new_file_is_created(self):
  with tempfile.TemporaryDirectory() as root:
   content="raise RuntimeError('this is file data, not the editor')\n"
   r=self.run_edit(root,[{'path':'engine/new.py','old':None,'new':content}])
   self.assertEqual(r.returncode,0,r.stderr);self.assertEqual((pathlib.Path(root)/'engine/new.py').read_text(),content)
 def test_exact_anchor_replacement(self):
  with tempfile.TemporaryDirectory() as root:
   p=pathlib.Path(root)/'code.py';p.write_text('one\ntwo\n')
   r=self.run_edit(root,[{'path':'code.py','old':'two\n','new':'three\n'}]);self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(p.read_text(),'one\nthree\n')
 def test_invalid_second_anchor_prevents_first_write(self):
  with tempfile.TemporaryDirectory() as root:
   p=pathlib.Path(root)/'code.py';p.write_text('original')
   r=self.run_edit(root,[{'path':'new.py','old':None,'new':'created'},{'path':'code.py','old':'absent','new':'bad'}]);self.assertNotEqual(r.returncode,0);self.assertFalse((pathlib.Path(root)/'new.py').exists());self.assertEqual(p.read_text(),'original')
 def test_ambiguous_anchor_is_refused(self):
  with tempfile.TemporaryDirectory() as root:
   p=pathlib.Path(root)/'code.py';p.write_text('x x')
   r=self.run_edit(root,[{'path':'code.py','old':'x','new':'y'}]);self.assertNotEqual(r.returncode,0);self.assertEqual(p.read_text(),'x x')
 def test_new_file_cannot_overwrite_existing(self):
  with tempfile.TemporaryDirectory() as root:
   p=pathlib.Path(root)/'code.py';p.write_text('original')
   r=self.run_edit(root,[{'path':'code.py','old':None,'new':'bad'}]);self.assertNotEqual(r.returncode,0);self.assertEqual(p.read_text(),'original')
 def test_escape_and_runtime_paths_refused(self):
  with tempfile.TemporaryDirectory() as root:
   for path in ('../escape.py','/tmp/escape.py','runtime/missions.sqlite','.receipts/fake.json'):
    self.assertNotEqual(self.run_edit(root,[{'path':path,'old':None,'new':'bad'}]).returncode,0)
 def test_symlink_escape_refused(self):
  with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as other:
   (pathlib.Path(root)/'escape').symlink_to(other,target_is_directory=True)
   self.assertNotEqual(self.run_edit(root,[{'path':'escape/code.py','old':None,'new':'bad'}]).returncode,0);self.assertFalse((pathlib.Path(other)/'code.py').exists())

 def test_invalid_python_is_not_written(self):
  with tempfile.TemporaryDirectory() as root:
   r=self.run_edit(root,[{'path':'bad.py','old':None,'new':'class Bad:\n def method(self) broken syntax'}])
   self.assertNotEqual(r.returncode,0);self.assertFalse((pathlib.Path(root)/'bad.py').exists())

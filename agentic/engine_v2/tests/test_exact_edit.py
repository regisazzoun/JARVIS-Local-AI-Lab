import hashlib,importlib.util,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('edit_bridge',Path(__file__).parents[1]/'broker/host_bridge.py');bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)
class ExactEdit(unittest.TestCase):
 def invoke(self,path,old,new,**extra):
  def sandbox(command,*args,**kwargs):
   result=subprocess.run(command,shell=True,capture_output=True,text=True)
   return {'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
  with patch.object(bridge,'sandbox',side_effect=sandbox):
   return bridge.execute('host_edit_file',{'path':str(path),'old':old,'new':new,**extra},{'write_roots':[str(path.parent)],'read_roots':[]})
 def test_exact_patch_preserves_rest_and_literal_shell_text(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'app.py';data=b'before\r\nwrong\r\nafter\r\n';p.write_bytes(data)
   new='literal $(touch '+td+'/UNEXPECTED) `echo kept`'
   r=self.invoke(p,'wrong',new,expected_sha256=hashlib.sha256(data).hexdigest())
   self.assertEqual(r['returncode'],0,r);self.assertEqual(p.read_bytes(),data.replace(b'wrong',new.encode()));self.assertFalse((Path(td)/'UNEXPECTED').exists())
 def test_ambiguous_match_changes_nothing(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'app.py';p.write_text('wrong wrong')
   self.assertNotEqual(self.invoke(p,'wrong','fixed')['returncode'],0);self.assertEqual(p.read_text(),'wrong wrong')
 def test_stale_hash_changes_nothing(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'app.py';p.write_text('wrong')
   self.assertNotEqual(self.invoke(p,'wrong','fixed',expected_sha256='0'*64)['returncode'],0);self.assertEqual(p.read_text(),'wrong')
 def test_delete_line(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'app.py';p.write_text('good\nbad import\nlast\n')
   self.assertEqual(self.invoke(p,'bad import\n','')['returncode'],0);self.assertEqual(p.read_text(),'good\nlast\n')
class EditRegistry(unittest.TestCase):
 def test_empty_replacement_is_valid_for_deletion(self):
  from jarvis.tools import Registry
  from jarvis.memory import Memory
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);registry=Registry(Memory(root/'runtime/memory.sqlite'),root)
   with patch('jarvis.host_client.request',return_value={'result':{'returncode':0,'stdout':'{}'},'evidence_id':'unit-test'}):
    result=registry.execute('host_edit_file',{'path':str(root/'app.py'),'old':'bad import\n','new':''})
   self.assertTrue(result['ok'],result)

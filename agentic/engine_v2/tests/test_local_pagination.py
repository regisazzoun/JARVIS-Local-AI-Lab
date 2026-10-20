import importlib.util,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('page_bridge',Path(__file__).parents[1]/'broker/host_bridge.py');bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)
class LocalPagination(unittest.TestCase):
 def test_middle_unicode_page_and_eof_are_complete_and_versioned(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'source.py';text='début\n'+('àé'*4000)+'\nfonction_critique\nfin';p.write_text(text)
   def sandbox(command,*args,**kwargs):
    r=subprocess.run(command,shell=True,capture_output=True,text=True);return {'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'stdout_truncated':False}
   with patch.object(bridge,'sandbox',side_effect=sandbox):
    page=bridge.execute('host_read_file',{'path':str(p),'offset':7990,'limit':20},{'write_roots':[td],'read_roots':[]})
    self.assertEqual(page['stdout'],text[7990:8010]);self.assertEqual(page['next_offset'],8010);self.assertEqual(page['total_chars'],len(text))
    last=bridge.execute('host_read_file',{'path':str(p),'offset':page['next_offset'],'limit':6000},{'write_roots':[td],'read_roots':[]})
    self.assertEqual(last['stdout'],text[8010:]);self.assertIsNone(last['next_offset']);self.assertEqual(last['source_sha256'],page['source_sha256'])
 def test_negative_offset_is_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   with self.assertRaises(ValueError):bridge.execute('host_read_file',{'path':td+'/x','offset':-1},{'write_roots':[td],'read_roots':[]})

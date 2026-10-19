import tempfile,unittest
from pathlib import Path
from jarvis.tools import Registry
from jarvis.memory import Memory
from jarvis.host_client import BrokerError
class ErrorFeedbackTest(unittest.TestCase):
 def test_redirected_traceback_not_reported_as_empty_error(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);r=Registry(Memory(root/'runtime/memory.sqlite'),root)
   def fail(args):raise BrokerError({'ok':False,'result':{'returncode':1,'stderr':'','stdout':'Traceback\nTypeError: incompatible SDK'},'evidence_id':'real-receipt'})
   r.specs['probe']=('probe',{},[],'read_only',fail)
   result=r.execute('probe',{})
   self.assertFalse(result['ok']);self.assertIn('TypeError',result['error']);self.assertEqual(result['result']['evidence_id'],'real-receipt')

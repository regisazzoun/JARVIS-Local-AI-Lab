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
 def test_transport_and_broker_diagnostics_reach_model_without_invented_receipt(self):
  for category,evidence in [('transport_denied',None),('permission_denied','broker-receipt')]:
   with self.subTest(category=category),tempfile.TemporaryDirectory() as t:
    root=Path(t);r=Registry(Memory(root/'runtime/memory.sqlite'),root)
    response={'ok':False,'error':'denied','error_code':'PermissionError','evidence_id':evidence,'diagnostic':{'error_category':category,'policy_identity':None}}
    def fail(args):raise BrokerError(response)
    r.specs['probe']=('probe',{},[],'read_only',fail)
    result=r.execute('probe',{})
    self.assertEqual(result['result']['diagnostic']['error_category'],category)
    self.assertEqual(result['error_code'],'PermissionError')
    self.assertEqual(result['result']['evidence_id'],evidence)

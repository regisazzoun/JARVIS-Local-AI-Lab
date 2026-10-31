import fcntl,json,tempfile,threading,unittest
from pathlib import Path
from unittest.mock import patch
from jarvis import google_mcp as g
class ConcurrentGoogle(unittest.TestCase):
 def test_second_client_waits_then_dispatches_once_instead_of_busy_success(self):
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp)/'personal';folder.mkdir();(folder/'index.js').write_text('fixture')
   dispatched=threading.Event();results=[];calls=[]
   async def upstream(*args):
    calls.append(args);dispatched.set();return {'mcp_is_error':False,'content':[{'text':'fixture'}]}
   with (folder/'operation.lock').open('a') as lock,patch.object(g,'credential_status',return_value={'configured':True}),patch.object(g,'upstream',side_effect=upstream):
    fcntl.flock(lock,fcntl.LOCK_EX)
    worker=threading.Thread(target=lambda:results.append(g.perform('personal','call','docs.getText',{'documentId':'fixture'},root=Path(tmp))))
    worker.start();self.assertFalse(dispatched.wait(.1));self.assertTrue(worker.is_alive())
    fcntl.flock(lock,fcntl.LOCK_UN);worker.join(3)
    self.assertFalse(worker.is_alive());self.assertEqual(len(calls),1);self.assertTrue(results[0]['remote_access_verified'])

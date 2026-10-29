import tempfile,unittest,hashlib,json
from pathlib import Path
from unittest.mock import patch
from jarvis.mission_store import MissionStore
from jarvis.publication import deliver_one
from jarvis.host_client import BrokerError
class PublicationRecoveryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.s=MissionStore(self.tmp.name);self.m=self.s.create('goal','model','conversation');self.body='real artifact';self.sha=hashlib.sha256(self.body.encode()).hexdigest()
 def row(self,identifier='p',attempts=0,file='report.md'):
  with self.s.db() as c:c.execute("INSERT INTO publication_outbox(id,mission,repository,branch,workspace,file,sha256,state,attempts,updated) VALUES(?,?,?,?,?,?,?,?,?,0)",(identifier,self.m,'owner/repo','mission-branch',self.tmp.name,file,self.sha,'retrying' if attempts else 'pending',attempts))
 def test_permission_refusal_stops_without_blind_retry(self):
  self.row()
  def invoke(op,args):
   if op=='host_read_file':return {'stdout':self.body}
   raise BrokerError({'ok':False,'error':'denied','error_code':'PermissionError'})
  with patch('jarvis.publication.invoke',side_effect=invoke):deliver_one(self.s)
  with self.s.db() as c:self.assertEqual(c.execute('SELECT state FROM publication_outbox').fetchone()[0],'needs_revision')
 def test_lost_reply_uses_observation_and_does_not_push_again(self):
  self.row(attempts=1);calls=[]
  def invoke(op,args):
   calls.append((op,args));return {'stdout':self.body} if op=='host_read_file' else {'stdout':json.dumps({'content':self.body})}
  with patch('jarvis.publication.invoke',side_effect=invoke):deliver_one(self.s)
  self.assertFalse(any(a.get('action')=='push' for _,a in calls))
  with self.s.db() as c:self.assertEqual(c.execute('SELECT state FROM publication_outbox').fetchone()[0],'verified')
 def test_renamed_publication_cannot_reset_target_counter(self):
  self.row(attempts=3)
  with patch('jarvis.publication.invoke') as invoke:deliver_one(self.s);invoke.assert_not_called()
  self.row('alias',0,'renamed.md')
  with patch('jarvis.publication.invoke') as invoke:deliver_one(self.s);invoke.assert_not_called()

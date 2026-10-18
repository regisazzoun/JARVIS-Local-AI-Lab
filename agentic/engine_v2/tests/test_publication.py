import hashlib,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from jarvis.mission_store import MissionStore
from jarvis.publication import enqueue,deliver_one

class PublicationTest(unittest.TestCase):
    def test_local_first_and_remote_verification(self):
        with tempfile.TemporaryDirectory() as temp:
            store=MissionStore(Path(temp));ident=store.create('publish','local','conversation')
            args={'workspace':'/work','file':'report.md','repository':'owner/repo','branch':'codex/test'}
            with patch('jarvis.publication.invoke',return_value={'stdout':'real local report'}):queued=enqueue(store,ident,'a',args)
            def broker(op,fields):
                if op=='host_read_file':return {'stdout':'real local report'}
                if fields['action']=='push':return {'stdout':'a'*40}
                return {'stdout':'{"content":"real local report"}'}
            with patch('jarvis.publication.invoke',side_effect=broker):deliver_one(store)
            with store.db() as c:row=c.execute('select * from publication_outbox').fetchone()
            self.assertEqual(row['state'],'verified');self.assertEqual(row['sha256'],hashlib.sha256(b'real local report').hexdigest())
    def test_failed_delivery_keeps_local_reference_and_retries(self):
        with tempfile.TemporaryDirectory() as temp:
            store=MissionStore(Path(temp));ident=store.create('publish','local','conversation')
            args={'workspace':'/work','file':'report.md','repository':'owner/repo','branch':'codex/test'}
            with patch('jarvis.publication.invoke',return_value={'stdout':'local intact'}):enqueue(store,ident,'a',args)
            with patch('jarvis.publication.invoke',side_effect=RuntimeError('network down')):deliver_one(store)
            with store.db() as c:row=c.execute('select * from publication_outbox').fetchone()
            self.assertEqual(row['state'],'retrying');self.assertEqual(row['attempts'],1);self.assertEqual(row['file'],'report.md');self.assertGreater(row['next_run'],0)

    def test_semantic_rejection_waits_for_revision_without_repeated_push(self):
        from jarvis.host_client import BrokerError
        with tempfile.TemporaryDirectory() as temp:
            store=MissionStore(Path(temp));ident=store.create('publish','local','conversation')
            args={'workspace':'/work','file':'SUIVI.md','repository':'owner/repo','branch':'jarvis/test'}
            with patch('jarvis.publication.invoke',return_value={'stdout':'truncated summary'}):enqueue(store,ident,'a',args)
            error=BrokerError({'ok':False,'error':'Preserve original document','error_code':'PublicationRevisionRequired'})
            with patch('jarvis.publication.invoke',side_effect=error) as invoke:
                deliver_one(store);deliver_one(store)
                self.assertEqual(invoke.call_count,1)
            with store.db() as c:row=c.execute('select * from publication_outbox').fetchone()
            self.assertEqual(row['state'],'needs_revision')
            with patch('jarvis.publication.invoke',return_value={'stdout':'original plus appended report'}):enqueue(store,ident,'a',args)
            with store.db() as c:self.assertEqual(c.execute('select state from publication_outbox where id=?',(row['id'],)).fetchone()[0],'superseded')

if __name__=='__main__':unittest.main()

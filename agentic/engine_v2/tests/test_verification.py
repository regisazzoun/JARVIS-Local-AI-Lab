import tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from jarvis.mission_store import MissionStore
from jarvis.durable_tools import register

class VerificationTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.store=MissionStore(Path(self.tmp.name))
        self.ident=self.store.create('test','local','conversation')
        self.store.plan(self.ident,[{'id':'a','title':'A','depends':[],'contract':{'checks':[{'tool':'host_exec','stdout_contains':'PASS'}]}}])
        self.registry=SimpleNamespace(mission_store=self.store,context={'mission_id':self.ident,'task_id':'a'},specs={'host_read_file':('',{},[], '',lambda a:{'stdout':'Rapport factuel suffisamment détaillé pour décrire les résultats, les limites et les preuves effectivement observées.'})},memory=SimpleNamespace(document=lambda *a,**kw:None))
        register(self.registry)
    def tearDown(self):self.tmp.cleanup()
    def call(self,tool,args,result):
        token=self.store.begin_call(self.ident,'a',tool,args);self.store.finish_call(token,result,.1);return token
    def test_report_write_does_not_invalidate_prior_functional_verification(self):
        self.call('host_write_file',{'path':'/work/code.py'},{'ok':True})
        proof=self.call('host_exec',{'command':'test code'},{'ok':True,'result':{'stdout':'PASS'}})
        self.call('host_write_file',{'path':'/work/report.md'},{'ok':True})
        result=self.registry.specs['mission_task_complete'][4]({'id':'a','evidence_id':proof,'report_path':'/work/report.md'})
        self.assertEqual(result['state'],'validated')
    def test_real_external_block_preserves_received_tasks(self):
        proof=self.call('host_remote',{'action':'tailscale_status'},{'ok':False,'result':{'stdout':'NeedsLogin'}})
        result=self.registry.specs['mission_block'][4]({'reason':'No enrollment credential available','report_path':'/work/block.md','evidence_id':proof})
        self.assertEqual(result['state'],'waiting_external')
        self.assertEqual(self.store.get(self.ident)['state'],'waiting_external')
        self.assertIsNone(self.store.claim('other-worker'))
        self.assertEqual(self.store.tasks(self.ident)[0]['state'],'blocked')
        self.store.transition(self.ident,'queued')
        self.assertEqual(self.store.ready(self.ident)[0]['id'],'a')
    def test_broker_id_is_a_valid_reference_for_block_and_evidence(self):
        self.call('host_remote',{'action':'tailscale_status'},{'ok':False,'result':{'stdout':'NeedsLogin','evidence_id':'actual-broker-id'}})
        evidence=self.registry.specs['mission_evidence'][4]({'id':'actual-broker-id'})
        self.assertIn('NeedsLogin',evidence['content'])
        result=self.registry.specs['mission_block'][4]({'reason':'Enrollment absent','report_path':'/work/block.md','evidence_id':'actual-broker-id'})
        self.assertEqual(result['state'],'waiting_external')
    def test_recoverable_publication_revision_must_not_be_hidden_by_external_block(self):
        from jarvis.publication import enqueue
        proof=self.call('host_remote',{'action':'tailscale_status'},{'ok':False,'result':{'stdout':'NeedsLogin'}})
        with self.store.db() as c:c.execute("INSERT INTO publication_outbox(id,mission,file,state) VALUES(?,?,?,?)",('revision',self.ident,'SUIVI.md','needs_revision'))
        with self.assertRaisesRegex(ValueError,'Correct recoverable document'):
            self.registry.specs['mission_block'][4]({'reason':'Enrollment absent','report_path':'/work/block.md','evidence_id':proof})
        self.assertNotEqual(self.store.get(self.ident)['state'],'waiting_external')
    def test_policy_read_cannot_validate_task(self):
        proof=self.call('host_policy',{}, {'ok':True})
        with self.assertRaises(ValueError):self.registry.specs['mission_task_complete'][4]({'id':'a','evidence_id':proof,'report_path':'/work/report.md'})
    def test_missing_functional_assertion_is_rejected(self):
        proof=self.call('host_read_file',{'path':'/work/code.py'},{'ok':True,'result':{'stdout':'code'}})
        with self.assertRaises(ValueError):self.registry.specs['mission_task_complete'][4]({'id':'a','evidence_id':proof,'report_path':'/work/report.md'})

if __name__=='__main__':unittest.main()

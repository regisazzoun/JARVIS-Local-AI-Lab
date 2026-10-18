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
    def test_policy_read_cannot_validate_task(self):
        proof=self.call('host_policy',{}, {'ok':True})
        with self.assertRaises(ValueError):self.registry.specs['mission_task_complete'][4]({'id':'a','evidence_id':proof,'report_path':'/work/report.md'})
    def test_missing_functional_assertion_is_rejected(self):
        proof=self.call('host_read_file',{'path':'/work/code.py'},{'ok':True,'result':{'stdout':'code'}})
        with self.assertRaises(ValueError):self.registry.specs['mission_task_complete'][4]({'id':'a','evidence_id':proof,'report_path':'/work/report.md'})

if __name__=='__main__':unittest.main()

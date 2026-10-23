import json
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from jarvis.mission_store import MissionStore
from jarvis.durable_tools import register


class CompletionReference(unittest.TestCase):
    def setup_case(self,root):
        s=MissionStore(root);m=s.create('fixture goal','local','conv',spec={'autonomous':False})
        path=str(root/'report.md');criterion={'kind':'json','source':{'tool':'host_read_file','arguments':{'path':str(root/'value.json')}},'expected':{'/valid':True}}
        s.plan(m,[{'id':'actual','title':'task','depends':[],'contract':{'report_path':path,'semantic':[criterion]}}])
        (root/'report.md').write_text('A real local fixture report with at least eighty characters, preserving all test limitations and observations.\n')
        for name in ['host_write_file','host_read_file']:
            t=s.begin_call(m,'actual',name,{'path':path});s.finish_call(t,{'ok':True,'result':{}},0)
        return s,m,path,criterion

    def verification(self,s,m,criterion,status='PASS'):
        parent=s.begin_call(m,'actual','mission_verify',{'contract':criterion})
        child=s.begin_call(m,'actual','host_read_file',{'path':criterion['source']['arguments']['path']})
        s.finish_call(child,{'ok':True,'result':{'stdout':'{"valid":true}'}},0)
        event=s.event(m,'semantic_verification',task='actual',result={'contract':criterion,'status':status})
        s.finish_call(parent,{'ok':status=='PASS','result':{'status':status,'verification_event':event}},0)
        return parent,child

    def test_nested_read_does_not_replace_parent_verification_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            s,m,path,criterion=self.setup_case(Path(tmp))
            parent,child=self.verification(s,m,criterion)
            status=s.contract_status(m,'actual')
            self.assertEqual(s.observations(m,'actual')[-1]['id'],child)
            self.assertEqual(status['semantic'][0]['invocation_id'],parent)
            self.assertEqual(status['completion_candidate'],{'id':'actual','report_path':path,'evidence_id':parent})
            self.verification(s,m,criterion,'FAIL')
            self.assertNotIn('completion_candidate',s.contract_status(m,'actual'))

    def test_coordinated_semantic_contract_rejects_false_success_and_stale_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);s,m,path,criterion=self.setup_case(root)
            registry=SimpleNamespace(mission_store=s,context={'mission_id':m,'task_id':'actual'},specs={},
                memory=SimpleNamespace(document=lambda *a,**kw:None))
            register(registry)
            registry.specs['host_read_file']=('',{},[],'host_authorized',lambda a:{'stdout':Path(a['path']).read_text(),'returncode':0})
            complete=registry.specs['mission_task_complete'][4]
            read=s.begin_call(m,'actual','host_read_file',{'path':'fixture'});s.finish_call(read,{'ok':True,'result':{}},0)
            with self.assertRaises(ValueError):complete({'id':'actual','report_path':path,'evidence_id':read})
            parent,_=self.verification(s,m,criterion)
            mutation=s.begin_call(m,'actual','host_write_file',{'path':str(root/'value.json'),'content':'{"valid":false}'})
            s.finish_call(mutation,{'ok':True,'result':{}},0)
            with self.assertRaises(ValueError):complete({'id':'actual','report_path':path,'evidence_id':parent})
            self.assertNotEqual(s.tasks(m)[0]['state'],'validated')
            current,_=self.verification(s,m,criterion)
            self.assertEqual(complete({'id':'actual','report_path':path,'evidence_id':current})['state'],'validated')

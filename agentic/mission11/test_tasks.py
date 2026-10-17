"""Unit tests: dependency and evidence boundaries, not acceptance of model behavior."""
import json,pathlib,sys,tempfile,unittest
sys.path.insert(0,'/opt/jarvis/conversation')
from jarvis.memory import Memory
from jarvis.tools import Registry
class TaskGraph(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.tmp.name);(self.root/'runtime').mkdir()
        self.r=Registry(Memory(self.root/'memory.sqlite'),self.root,{'lab_enabled':True});self.r.context={'conversation':'test','mission_id':'m'}
    def tearDown(self):self.tmp.cleanup()
    def test_cycle_refused(self):
        r=self.r.execute('mission_plan',{'tasks':json.dumps([{'id':'a','title':'A','depends':['b']},{'id':'b','title':'B','depends':['a']}])})
        self.assertFalse(r['ok'])
    def test_dependencies_and_unforgeable_assertion(self):
        self.r.execute('mission_plan',{'tasks':json.dumps([{'id':'a','title':'A','depends':[]},{'id':'b','title':'B','depends':['a']}])})
        self.assertFalse(self.r.execute('mission_task_complete',{'id':'a','evidence_id':'invented'})['ok'])
        trace=self.root/'runtime/tool-traces.jsonl'
        with trace.open('a') as f:f.write(json.dumps({'conversation':'test','result':{'ok':True,'result':{'evidence_id':'fixture-proof'}}})+'\n')
        self.assertFalse(self.r.execute('mission_task_complete',{'id':'b','evidence_id':'fixture-proof'})['ok'])
        self.assertTrue(self.r.execute('mission_task_complete',{'id':'a','evidence_id':'fixture-proof'})['ok'])
        self.assertTrue(self.r.execute('mission_task_complete',{'id':'b','evidence_id':'fixture-proof'})['ok'])
        self.assertEqual(self.r.execute('mission_progress',{})['result']['progress']['percent'],100)
    def test_learning_requires_proof(self):
        self.assertFalse(self.r.execute('procedure_save',{'title':'Unverified','content':'not a verified procedure'})['ok'])
if __name__=='__main__':unittest.main()

import tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from jarvis.mission_store import MissionStore
from jarvis.durable_cycle import DurableCycle

class RepetitionEpochTest(unittest.TestCase):
    def test_fresh_service_observation_is_allowed_after_reconfiguration(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);identity=root/'identity.md';identity.write_text('Unit fixture, no model execution.')
            store=MissionStore(root);ident=store.create('test','unit-model','conversation')
            store.plan(ident,[{'id':'a','title':'A','depends':[]}]);seen=[]
            def execute(name,args):seen.append(args['action']);return {'ok':True,'tool':name,'result':{'stdout':'unit fixture'}}
            tools=SimpleNamespace(root=root,specs={'host_remote':None},schemas=lambda:[{'type':'function','function':{'name':'host_remote'}}],execute=execute)
            actions=iter(('services','services','desktop_configure','services'))
            def model(payload):return {'role':'assistant','content':'','tool_calls':[{'function':{'name':'host_remote','arguments':{'host':'test-only','action':next(actions)}}}]}
            core=SimpleNamespace(config={'identity_file':str(identity),'durable_cycle_rounds':4,'num_ctx':16384},tools=tools,memory=SimpleNamespace(document_search=lambda *a:[]),missions=SimpleNamespace(is_interrupted=lambda i:False),transport=model,metrics=[])
            DurableCycle(core,store).run(store.get(ident))
            self.assertEqual(seen,['services','services','desktop_configure','services'])
            self.assertTrue(all(o['result']['ok'] for o in store.observations(ident)))

if __name__=='__main__':unittest.main()

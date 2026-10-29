import json,threading,tempfile,urllib.request,unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from jarvis.core import Core,ROOT
from jarvis.memory import Memory
from jarvis.missions import Missions
from jarvis.server import make_handler
from jarvis.conversation_tools import bounded_conversation_tools,DEFAULT_CONVERSATION_TOOLS
class ConversationAPI(unittest.TestCase):
    def test_real_handler_limits_default_without_expanding_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cfg=json.loads((ROOT/'config/example.json').read_text());cfg.update(num_ctx=16384,voice_summary=False)
            seen=[]
            def transport(p):
                seen.append(p);return {'role':'assistant','content':'Bonjour.'}
            c=Core(cfg,Memory(root/'runtime/memory.sqlite'),transport);Missions(c,root,start_worker=False)
            server=ThreadingHTTPServer(('127.0.0.1',0),make_handler(c));cfg['allowed_hosts']=['127.0.0.1:'+str(server.server_port)];t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
            try:
                req=urllib.request.Request('http://127.0.0.1:'+str(server.server_port)+'/api/chat',data=json.dumps({'text':'Bonjour','model':cfg['default_model'],'retain':False}).encode(),headers={'Content-Type':'application/json','X-Jarvis-Request':'1'})
                with urllib.request.urlopen(req) as r:self.assertEqual(r.status,200)
                names={v['function']['name'] for v in seen[0]['tools']}
                self.assertEqual(names,set(DEFAULT_CONVERSATION_TOOLS)-{'compute_status','compute_escalate'});self.assertNotIn('host_exec',names)
                self.assertLessEqual(seen[0]['options']['num_ctx'],16384)
            finally:server.shutdown();server.server_close();t.join()
    def test_explicit_mission_creation_does_not_become_a_status_query(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cfg=json.loads((ROOT/'config/example.json').read_text())
            c=Core(cfg,Memory(root/'runtime/memory.sqlite'),lambda p: (_ for _ in ()).throw(AssertionError('Submission should not infer in HTTP handler')))
            engine=Missions(c,root,start_worker=False)
            server=ThreadingHTTPServer(('127.0.0.1',0),make_handler(c));cfg['allowed_hosts']=['127.0.0.1:'+str(server.server_port)]
            t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
            try:
                payload={'goal':'Quel est état des missions ?', 'model':cfg['default_model'],'request_kind':'mission'}
                req=urllib.request.Request('http://127.0.0.1:'+str(server.server_port)+'/api/missions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','X-Jarvis-Request':'1'})
                with urllib.request.urlopen(req) as r:data=json.load(r)
                self.assertRegex(data['id'],'^[0-9a-f]{32}$');self.assertEqual(engine.store.get(data['id'])['state'],'queued')
            finally:server.shutdown();server.server_close();t.join()
    def test_explicit_empty_or_subset_is_preserved(self):
        self.assertEqual(bounded_conversation_tools({'allowed_tools':[]},{},{}),[])
        self.assertEqual(bounded_conversation_tools({'allowed_tools':None},{'active_memories':1},{}),['active_memories'])
        self.assertEqual(bounded_conversation_tools({'allowed_tools':['x']},{'x':1},{}),['x'])
    def test_missions_and_agent_mode_are_not_restricted_by_chat_default(self):
        self.assertIsNone(bounded_conversation_tools({'mission_id':'m'},{},{}))
        self.assertIsNone(bounded_conversation_tools({'agent_mode':True},{},{}))
    def test_invalid_configuration_fails_instead_of_silently_granting_tools(self):
        with self.assertRaises(ValueError):bounded_conversation_tools({}, {}, {'conversation_tools':['absent']})
if __name__=='__main__':unittest.main()

"""HTTP and canonical admission tests on a temporary database, not autonomy proofs."""
import importlib.util,json,os,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
class GatewayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.calls=[]
        class Backend(BaseHTTPRequestHandler):
            def log_message(self,*a):pass
            def do_POST(self):
                p=json.loads(self.rfile.read(int(self.headers['Content-Length'])));cls.calls.append(p)
                self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(json.dumps({'message':{'content':'fixture'},'observed_options':p['options']}).encode())
        cls.backend=ThreadingHTTPServer(('127.0.0.1',0),Backend);threading.Thread(target=cls.backend.serve_forever,daemon=True).start()
        settings={'JARVIS_WEBUI_QUEUE_TIMEOUT':'0.2','JARVIS_MISSIONS_DB':str(Path(cls.tmp.name)/'missions.sqlite'),'JARVIS_ADMISSION_LOG':str(Path(cls.tmp.name)/'admission.jsonl'),'JARVIS_DELL_OLLAMA_URL':'http://127.0.0.1:'+str(cls.backend.server_port)};saved={k:os.environ.get(k) for k in settings};os.environ.update(settings)
        try:
            spec=importlib.util.spec_from_file_location('gateway_under_test',Path(__file__).with_name('inference_gateway.py'));cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)
        finally:
            for k,v in saved.items():
                if v is None:os.environ.pop(k,None)
                else:os.environ[k]=v
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),cls.g.Handler);threading.Thread(target=cls.server.serve_forever,daemon=True).start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.backend.shutdown();cls.backend.server_close();cls.tmp.cleanup()
    def request(self,payload,path='/api/chat'):
        return urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:'+str(self.server.server_port)+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'}),timeout=10)
    def payload(self):return {'model':'qwen3-coder-next:q4_K_M','messages':[{'role':'user','content':'fixture'}],'options':{'num_ctx':16384,'num_predict':5000},'stream':False}
    def test_native_uses_existing_queue_and_enforces_window(self):
        with self.request(self.payload()) as r:d=json.load(r)
        self.assertEqual(d['observed_options']['num_ctx'],32768);self.assertEqual(d['observed_options']['num_predict'],4096)
        row=self.g.QUEUE.recent(1)[0];self.assertEqual(row['node'],'Dell1');self.assertEqual(row['role'],'critical');self.assertEqual(row['state'],'finished')
    def test_oversized_body_is_not_dispatched(self):
        p=self.payload();p['messages'][0]['content']='x'*28000;before=len(self.calls)
        with self.assertRaises(urllib.error.HTTPError) as e:self.request(p)
        self.assertEqual(e.exception.code,413);self.assertEqual(len(self.calls),before)
    def test_context_expansion_is_refused(self):
        p=self.payload();p['options']['num_ctx']=65536
        with self.assertRaises(urllib.error.HTTPError) as e:self.request(p)
        self.assertEqual(e.exception.code,400)
    def test_model_management_endpoints_are_not_exposed(self):
        before=len(self.calls)
        with self.assertRaises(urllib.error.HTTPError) as e:self.request({'model':'fixture'},'/api/delete')
        self.assertEqual(e.exception.code,403);self.assertEqual(len(self.calls),before)
    def test_existing_canonical_reservation_cannot_be_bypassed(self):
        reservation=self.g.QUEUE.enter('Dell1','qwen3-coder-next:q4_K_M','mission',timeout=1);before=len(self.calls)
        try:
            with self.assertRaises(urllib.error.HTTPError) as e:self.request(self.payload())
            self.assertEqual(e.exception.code,429);self.assertEqual(len(self.calls),before)
        finally:self.g.QUEUE.finish(reservation)
if __name__=='__main__':unittest.main(verbosity=2)

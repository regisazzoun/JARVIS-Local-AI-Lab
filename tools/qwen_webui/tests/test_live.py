"""Focused live checks: no fixture outcome is presented as autonomous operation."""
import json,urllib.request,urllib.error,unittest
from pathlib import Path
P=Path('/home/adminjarvis/JARVIS/qwen-code-openwebui-private')
class Live(unittest.TestCase):
    def test_apache_preserves_backend(self):
        a=json.load(urllib.request.urlopen('http://127.0.0.1:8088/api/version'))
        b=json.load(urllib.request.urlopen('http://192.168.1.99:3000/api/version'));self.assertEqual(a,b)
    def test_adapter_requires_key(self):
        with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8092/tools/missions',data=b'{}'))
        self.assertEqual(e.exception.code,401)
    def test_canonical_missions_are_compact(self):
        r=urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8092/tools/missions',data=b'{}',headers={'Authorization':'Bearer '+(P/'adapter-key').read_text()})).read()
        self.assertLess(len(r),6000);d=json.loads(r);self.assertGreater(d['count'],0);self.assertLessEqual(len(d['recent']),12)
    def test_context_refused_before_inference(self):
        payload={'model':'qwen3-coder-next:q4_K_M','messages':[{'role':'user','content':'X'*28000}]}
        with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8091/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'}))
        self.assertEqual(e.exception.code,413)
    def test_traversal_project_refused(self):
        req=urllib.request.Request('http://127.0.0.1:8092/tools/qwen_code',data=json.dumps({'project':'../elsewhere','task':'read'}).encode(),headers={'Authorization':'Bearer '+(P/'adapter-key').read_text()})
        with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(req)
        self.assertEqual(e.exception.code,400)
if __name__=='__main__':unittest.main(verbosity=2)

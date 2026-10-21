import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from jarvis.host_client import register

class Argv(unittest.TestCase):
    def test_literal_tokens_and_exclusive_forms(self):
        class Registry:
            def __init__(self):self.specs={}
        r=Registry();register(r)
        fn=r.specs['host_exec'][4]
        with tempfile.TemporaryDirectory() as tmp:
            marker=Path(tmp)/'injected'
            token='space ; touch '+str(marker)+' $(uname) `uname`'
            with patch('jarvis.host_client.request',return_value={'result':{'stdout':'fixture'},'evidence_id':'unit'}) as request:
                fn({'argv':[sys.executable,'-c','import json,sys;print(json.dumps(sys.argv[1:]))',token],'timeout':5})
                op,args=request.call_args.args
                self.assertEqual(op,'host_exec');self.assertNotIn('argv',args)
                result=subprocess.run(['/bin/bash','-c',args['command']],capture_output=True,text=True,check=True)
                self.assertEqual(json.loads(result.stdout),[token]);self.assertFalse(marker.exists())
            with self.assertRaises(ValueError):fn({'argv':['echo','x'],'command':'echo x'})
            with self.assertRaises(ValueError):fn({})

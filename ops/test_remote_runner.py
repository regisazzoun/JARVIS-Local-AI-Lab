import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import signal
import time
import subprocess
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('remote_runner',Path(__file__).with_name('remote_runner.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class RemoteStateTests(unittest.TestCase):
    def test_completed_write_racing_systemd_exit_is_not_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);r.atomic(root/'state.json',{'status':'running','failures':0})
            def exited(unit):
                r.atomic(root/'state.json',{'status':'completed','failures':0,'returncode':0})
                return {'ActiveState':'inactive','MainPID':'0'}
            with patch.object(r,'unit_info',exited):s=r.status(root,'fixture.service')
            self.assertEqual(s['status'],'completed');self.assertEqual(s['failures'],0)
    def test_lost_supervisor_counts_once(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);r.atomic(root/'state.json',{'status':'running','failures':1})
            with patch.object(r,'unit_info',lambda unit:{'ActiveState':'inactive','MainPID':'0'}):
                self.assertEqual(r.status(root,'fixture.service')['failures'],2)
                self.assertEqual(r.status(root,'fixture.service')['failures'],2)

class SignalObservationTests(unittest.TestCase):
    def test_operator_stop_interrupting_probe_is_not_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            r.atomic(root/'manifest.json',{'cwd':d,'argv':['/usr/bin/true'],'inference_port':11435,'max_seconds':20})
            r.atomic(root/'state.json',{'status':'starting','failures':4})
            r.atomic(root/'lease.json',{'expires':time.time()+10})
            class Proc:
                pid=999999;returncode=None
                def poll(self):return self.returncode
            proc=Proc()
            def interrupted(*a):
                r.STOP=True;raise subprocess.CalledProcessError(-15,['ss'])
            term=signal.getsignal(signal.SIGTERM);intr=signal.getsignal(signal.SIGINT)
            try:
                with patch.object(r,'paths',lambda i:(root,'fixture.service')),patch.object(r,'validate',lambda m:None),patch.object(r.subprocess,'Popen',lambda *a,**k:proc),patch.object(r,'external_inference',interrupted),patch.object(r,'stop_group',lambda p:setattr(p,'returncode',-15)):
                    r.STOP=False;r.supervisor('fixture')
                state=json.loads((root/'state.json').read_text())
                self.assertEqual(state['status'],'paused');self.assertEqual(state['failures'],4)
            finally:
                signal.signal(signal.SIGTERM,term);signal.signal(signal.SIGINT,intr);r.STOP=False

if __name__=='__main__':unittest.main()

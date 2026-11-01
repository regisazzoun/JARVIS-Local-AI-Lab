import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

spec=importlib.util.spec_from_file_location('scheduler',Path(__file__).with_name('idle_scheduler.py'))
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)

class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.cfg={'max_cpu_percent':25,'min_mem_available_fraction':.35,'max_gpu_utilization_percent':20,'max_vram_used_fraction':.5}
        self.job={'node':'dell-1','uses_gpu':True}
        self.machine={'available':True,'sampled_at':100,'cpu_percent':1,'ram_total_mb':100,'ram_used_mb':10,'gpu_captured_at':100,'gpu_all':[{'utilization_percent':0,'free_mib':90,'total_mib':100}],'ollama':True,'active_models':[]}
        self.data={'sampled_at':100,'machines':{'dell-1':self.machine}}
    def admit(self):return s.admission(self.cfg,self.job,self.data,101)[0]
    def test_idle(self):self.assertTrue(self.admit())
    def test_stale_and_future(self):
        for stamp in [0,200,float('nan')]:
            self.data['sampled_at']=stamp;self.assertFalse(self.admit())
    def test_stale_gpu(self):self.machine['gpu_captured_at']=0;self.assertFalse(self.admit())
    def test_second_gpu_busy(self):self.machine['gpu_all'].append({'utilization_percent':90,'free_mib':90,'total_mib':100});self.assertFalse(self.admit())
    def test_vram_reserved(self):self.machine['gpu_all'][0]['free_mib']=5;self.assertFalse(self.admit())
    def test_models_preserved_cpu_allowed(self):
        self.machine['active_models']=['Qwen'];self.assertFalse(self.admit())
        self.job['uses_gpu']=False;self.assertTrue(self.admit())
    def test_missing_gpu(self):self.machine['gpu_all']=[];self.assertFalse(self.admit())
    def test_bad_cpu(self):self.machine['cpu_percent']=float('nan');self.assertFalse(self.admit())
    def test_ram_busy(self):self.machine['ram_used_mb']=90;self.assertFalse(self.admit())
    def test_three_failures_and_singleton(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);path=root/'state.json'
            cfg={**self.cfg,'enabled':True,'state_path':str(path),'pause_path':str(root/'PAUSE'),'poll_seconds':.05,'monitor_seconds':.01,'max_job_seconds':2,'jobs':[{'id':'busy','node':'dell-1'}, {'id':'fail','node':'mac-mini','checkpoint_safe':True,'argv':['/usr/bin/false']}]}
            code='import sys;sys.path.insert(0,sys.argv[1]);import idle_scheduler as s,json; s.eligible=lambda cfg,job,t:(job["id"]!="busy","fixture");s.run(json.loads(sys.argv[2]),True)'
            args=[sys.executable,'-c',code,str(Path(__file__).parent),json.dumps(cfg)]
            p=subprocess.Popen(args,stdout=subprocess.DEVNULL)
            try:
                for _ in range(100):
                    if path.exists() and json.loads(path.read_text())['attempts'].get('fail')==3:break
                    time.sleep(.03)
                self.assertEqual(json.loads(path.read_text())['attempts']['fail'],3)
                self.assertNotIn('busy',json.loads(path.read_text())['attempts'])
                other=subprocess.run(args,capture_output=True,timeout=3)
                self.assertNotEqual(other.returncode,0)
                time.sleep(.2);self.assertEqual(json.loads(path.read_text())['attempts']['fail'],3)
            finally:p.terminate();p.wait(timeout=3)

class PreemptionTests(unittest.TestCase):
    def test_resource_loss_resume_checkpoint(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);state=root/'state.json';gate=root/'BUSY';checkpoint=root/'checkpoint'
            cfg={'enabled':True,'state_path':str(state),'pause_path':str(root/'PAUSE'),'poll_seconds':.05,'monitor_seconds':.02,'max_job_seconds':30,'jobs':[{'id':'checkpoint','node':'mac-mini','checkpoint_safe':True,'argv':[sys.executable,str(Path(__file__).with_name('checkpoint_smoke.py')),str(checkpoint)]}]}
            code='import sys,json;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import idle_scheduler as s;s.eligible=lambda *a:(not Path(sys.argv[3]).exists(),"fixture resource pressure");s.run(json.loads(sys.argv[2]),True)'
            args=[sys.executable,'-c',code,str(Path(__file__).parent),json.dumps(cfg),str(gate)]
            p=subprocess.Popen(args,stdout=subprocess.DEVNULL)
            def wait_for(fn,seconds=20):
                end=time.monotonic()+seconds
                while time.monotonic()<end:
                    if fn():return
                    time.sleep(.03)
                self.fail('Timed out')
            try:
                wait_for(checkpoint.exists);gate.touch()
                wait_for(lambda:state.exists() and json.loads(state.read_text())['status'] in ('paused','waiting_resources'))
                step=checkpoint.read_text();time.sleep(1.2);self.assertEqual(checkpoint.read_text(),step)
                self.assertEqual(json.loads(state.read_text())['attempts']['checkpoint'],0)
                gate.unlink();wait_for(lambda:'checkpoint' in json.loads(state.read_text())['completed'])
                self.assertEqual(checkpoint.read_text(),'12')
            finally:p.terminate();p.wait(timeout=4)

if __name__=='__main__':unittest.main()

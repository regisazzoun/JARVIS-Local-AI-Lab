import json
from pathlib import Path
import sys
import io
import tempfile
import wave
import zipfile
import subprocess
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parents[1]/'broker'))
from remote_project import project_program
from remote_probes import probe_command,PROBES
from jarvis.verification import Verifier,validate_contract


class FixedIndependentProbes(unittest.TestCase):
    def test_project_probe_is_accepted_but_arbitrary_execution_is_not(self):
        class Registry:
            def execute(self,name,args):
                assert name=='host_remote' and args['action']=='project_probe'
                return {'ok':True,'result':{'returncode':0,'stdout':json.dumps({'cuda_available':True,'cuda_tensor_sum':6.0})}}
        contract={'kind':'json','source':{'tool':'host_remote','arguments':{'host':'dell-observe','action':'project_probe','project':'tts-01','probe':'tts_runtime'}},'expected':{'/cuda_tensor_sum':6.0}}
        self.assertEqual(Verifier(Registry()).verify(contract)['status'],'PASS')
        bad={**contract,'source':{'tool':'host_remote','arguments':{'action':'project_exec','command':'touch result'}}}
        with self.assertRaises(ValueError):validate_contract(bad)

    def test_fixed_names_have_no_shell_injection_parameter(self):
        with self.assertRaises(ValueError):probe_command('/opt/jarvis-lab/tts-01','gpu_inventory; touch /bad')
        command=probe_command('/opt/jarvis-lab/tts-01','tts_runtime')
        self.assertIn('venv/bin/python',command)

    def test_probe_project_mount_is_read_only(self):
        script=project_program('/opt/jarvis-lab/tts-01','true',True,readonly=True)
        with patch('pathlib.Path.mkdir'),patch('pathlib.Path.glob',return_value=[]),patch('subprocess.call',return_value=0) as call:
            with self.assertRaises(SystemExit):exec(compile(script,'probe-runtime','exec'),{})
        argv=call.call_args.args[0];index=argv.index('/opt/jarvis-lab/tts-01')
        self.assertEqual(argv[index-1],'--ro-bind')

    def test_archive_probe_measures_pcm_and_excludes_appledouble(self):
        body=io.BytesIO()
        with wave.open(body,'wb') as wav:
            wav.setparams((1,2,8000,0,'NONE','not compressed'))
            wav.writeframes(b'\xff\x7f\x00\x80\x00\x00\x01\x00')
        with tempfile.TemporaryDirectory() as root:
            with zipfile.ZipFile(Path(root)/'references.zip','w') as z:
                z.writestr('a.wav',body.getvalue());z.writestr('__MACOSX/._a.wav',b'not an audio file')
            result=subprocess.run([sys.executable,'-c',PROBES['archive_inventory'][1]],cwd=root,capture_output=True,text=True,check=True)
        observed=json.loads(result.stdout)
        self.assertEqual(observed['wav_files'],1)
        self.assertEqual(observed['full_scale_samples_total'],2)
        self.assertEqual(observed['files'][0]['pcm_bit_rate_bps'],128000)
        self.assertAlmostEqual(observed['total_duration_s'],4/8000)
        self.assertLess(observed['files'][0]['rms_dbfs'],0)

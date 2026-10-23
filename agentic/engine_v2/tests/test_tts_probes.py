import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parents[1]/'broker'))
from remote_project import project_program
from remote_probes import probe_command
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

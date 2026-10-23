import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).parents[1]/'broker'))
from remote_project import project_program,transfer_file


class ScopedTTSProject(unittest.TestCase):
    def argv(self,gpu,root_readonly=False):
        script=project_program('/opt/jarvis-lab/tts-01','echo "ROOT COMMAND if GPU:"',gpu,root_readonly=root_readonly)
        with patch('pathlib.Path.mkdir'), patch('pathlib.Path.glob',return_value=[Path('/dev/nvidia0')]), patch('subprocess.call',return_value=0) as call:
            with self.assertRaises(SystemExit):exec(compile(script,'remote-project','exec'),{})
        return call.call_args.args[0]

    def test_gpu_only_for_explicit_project_policy(self):
        ordinary=self.argv(False);gpu=self.argv(True)
        self.assertNotIn('--dev-bind',ordinary)
        self.assertIn('--dev-bind',gpu)
        self.assertIn('/dev/nvidia0',gpu)
        self.assertEqual(gpu[-1],'echo "ROOT COMMAND if GPU:"')
        self.assertNotIn('/root',gpu)

    def test_rejects_policy_root_outside_project_families(self):
        for path in ['/','/etc','/opt/jarvis-lab/../secret','relative']:
            with self.subTest(path=path),self.assertRaises(ValueError):project_program(path,'true')

    def test_strict_project_disallows_silent_writes_to_ephemeral_root(self):
        self.assertIn('--remount-ro',self.argv(True,True))
        self.assertNotIn('--remount-ro',self.argv(False))

    def test_transfer_refuses_ungranted_project_and_remote_escape(self):
        args={'project':'tts-01','path':'/etc/shadow','action':'project_download','local_path':'/allowed/file.wav'}
        with self.assertRaises(PermissionError):transfer_file({},[],{},args,None,None)
        profile={'project_exec_projects':['tts-01'],'project_exec_options':{'tts-01':{'root':'/opt/jarvis-lab/tts-01','transfer':True,'transfer_local_root':'/allowed'}}}
        for path in ['/etc/shadow','/opt/jarvis-lab/tts-01/../secret.wav','/opt/jarvis-lab/tts-01/key.pem']:
            with self.subTest(path=path),self.assertRaises(PermissionError):transfer_file(profile,[],{},dict(args,path=path),None,None)

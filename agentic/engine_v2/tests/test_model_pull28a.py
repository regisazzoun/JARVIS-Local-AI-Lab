"""Model-management contract tests using HTTP fixtures, not autonomy evidence."""
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('model_manage28a', BASE / 'operations/mission28a/model_manage.py')
manage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manage)
sys.path.insert(0, str(Path(__file__).parents[1] / 'broker'))
import host_bridge

MODEL = 'qwen3:32b-q4_K_M'


class ModelPullTests(unittest.TestCase):
    def opener(self, final, events):
        reads = []
        def opened(request, timeout):
            reads.append(request)
            if isinstance(request, str):
                names = [] if len(reads) == 1 else final
                return io.BytesIO(json.dumps({'models': names}).encode())
            self.assertEqual(request.method, 'POST')
            self.assertEqual(json.loads(request.data), {'model': MODEL, 'stream': True})
            return io.BytesIO(b''.join(json.dumps(e).encode() + b'\n' for e in events))
        return opened, reads

    def test_success_requires_exact_tag_read_back(self):
        opener, calls = self.opener([{'name': MODEL, 'digest': 'test', 'size': 20}], [{'status': 'success'}])
        result = manage.pull('http://fixture', MODEL, opener=opener)
        self.assertTrue(result['verified'])
        self.assertEqual(len(calls), 3)

    def test_success_status_without_installed_tag_is_insufficient(self):
        opener, _ = self.opener([{'name': 'qwen3.5:27b-q4_K_M'}], [{'status': 'success'}])
        self.assertFalse(manage.pull('http://fixture', MODEL, opener=opener)['verified'])

    def test_http_ok_with_error_is_not_success(self):
        opener, _ = self.opener([], [{'error': 'registry failure'}])
        result = manage.pull('http://fixture', MODEL, opener=opener)
        self.assertFalse(result['verified'])
        self.assertIn('registry failure', result['error'])

    def test_truncated_progress_is_not_success(self):
        opener, _ = self.opener([], [{'status': 'pulling', 'completed': 123}])
        result = manage.pull('http://fixture', MODEL, opener=opener)
        self.assertFalse(result['verified'])
        self.assertEqual(result['last_progress']['completed'], 123)

    def test_present_exact_tag_skips_duplicate_download(self):
        def opened(request, timeout):
            self.assertIsInstance(request, str)
            return io.BytesIO(json.dumps({'models': [{'name': MODEL}]}).encode())
        result = manage.pull('http://fixture', MODEL, opener=opened)
        self.assertEqual(result['status'], 'already_present')
        self.assertTrue(result['verified'])

    def test_broker_rejects_ungranted_model_before_remote_pull(self):
        profile = {'identity': 'key', 'known_hosts': 'hosts', 'user': 'user', 'address': 'fixture',
                   'allow_admin': True, 'model_management': {'program': '/fixed/program', 'allowed_models': [MODEL]}}
        with patch.object(host_bridge, 'run') as run:
            with self.assertRaises(PermissionError):
                host_bridge.execute('host_remote', {'host': 'dell', 'action': 'model_pull', 'model': 'other'}, {'remote_hosts': {'dell': profile}})
            run.assert_not_called()

    def test_broker_structured_action_and_alias_have_fixed_command(self):
        profile = {'identity': 'key', 'known_hosts': 'hosts', 'user': 'user', 'address': 'fixture',
                   'allow_admin': True, 'model_management': {'program': '/fixed/program', 'allowed_models': [MODEL]}}
        for action in ['model_pull', 'pull']:
            with patch.object(host_bridge, 'run', return_value={'returncode': 0}) as run:
                host_bridge.execute('host_remote', {'host': 'dell', 'action': action, 'model': MODEL}, {'remote_hosts': {'dell': profile}})
                self.assertEqual(run.call_args.args[0][-1], 'python3 /fixed/program --model ' + MODEL)
                self.assertEqual(run.call_args.args[1], 580)

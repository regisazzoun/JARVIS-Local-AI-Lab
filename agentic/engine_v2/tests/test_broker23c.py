import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'broker'))
from capability_view import diagnostic, policy_identity, public_scope
from jarvis.host_client import BrokerError, request, register


class Broker23C(unittest.TestCase):
    def test_transport_denial_is_not_a_policy_denial(self):
        with patch('jarvis.host_client.socket.socket', side_effect=PermissionError(1, 'denied')):
            with self.assertRaises(BrokerError) as caught:
                request('host_service', {'service': 'authorized', 'action': 'status'})
        receipt = caught.exception.response
        self.assertEqual(receipt['diagnostic']['error_category'], 'transport_denied')
        self.assertIsNone(receipt['diagnostic']['policy_identity'])
        self.assertIsNone(receipt['diagnostic']['evidence_id'])

    def test_scope_never_returns_remote_secrets(self):
        cfg = {'remote_hosts': {'dell': {'identity': '/private/key', 'password': 'hidden',
               'commands': {'secret': 'value'}, 'allow_admin': True}}, 'secret': 'hidden'}
        rendered = json.dumps(public_scope(cfg))
        for secret in ('/private/key', 'hidden', 'commands'):
            self.assertNotIn(secret, rendered)
        self.assertTrue(public_scope(cfg)['machines']['dell']['allow_admin'])

    def test_policy_fingerprint_changes_on_permission_change(self):
        cfg = {'services': {'livekit': ['status']}}
        before = policy_identity(cfg)
        cfg['services']['livekit'].append('restart')
        self.assertNotEqual(before['policy_sha256'], policy_identity(cfg)['policy_sha256'])

    def test_failure_classes_and_redaction(self):
        cases = [({'error_code': 'PermissionError'}, 'permission_denied'),
                 ({'error_code': 'ValueError'}, 'invalid_parameter'),
                 ({'error_code': 'FileNotFoundError'}, 'resource_missing'),
                 ({'error_code': 'ConnectionRefusedError'}, 'service_unavailable'),
                 ({'error_code': 'gaierror'}, 'network_error'),
                 ({'result': {'timeout': True, 'returncode': -9}}, 'timeout'),
                 ({'result': {'returncode': 127}}, 'command_missing'),
                 ({'result': {'returncode': 1, 'stderr': 'permission denied'}}, 'application_error')]
        for failure, expected in cases:
            with self.subTest(expected=expected):
                receipt = diagnostic('host_exec', {'command': 'credential-body'}, {'ok': False, **failure}, {})
                self.assertEqual(receipt['error_category'], expected)
                self.assertNotIn('credential-body', json.dumps(receipt))

    def test_catalog_is_derived_from_exposed_tools_and_never_claims_success(self):
        class Registry:
            specs = {}
        registry = Registry()
        register(registry)
        with patch('jarvis.host_client.request', return_value={'result': {'effective_scope': {}}, 'evidence_id': 'fixture'}):
            view = registry.specs['capability_status'][4]({})
        self.assertEqual({t['name'] for t in view['tools']}, set(registry.specs))
        self.assertTrue(all(t['availability'] == 'unverified' for t in view['tools']))
        self.assertEqual(next(t for t in view['tools'] if t['name'] == 'host_service')['required'], ['service', 'action'])

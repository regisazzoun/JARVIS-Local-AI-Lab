import unittest
from jarvis.durable_cycle import discovery_schemas, task_schemas


class TaskDiscoveryScope(unittest.TestCase):
    def setUp(self):
        self.schemas = [{'function': {'name': name}} for name in (
            'host_remote', 'host_write_file', 'host_read_file',
            'mission_verify', 'mission_progress', 'mission_read_batch', 'host_exec')]

    def test_scoped_task_keeps_execution_and_control_without_old_batch(self):
        definition = {'tools': ['host_remote', 'host_write_file'],
                      'discovery_tools': ['host_read_file']}
        offered = {s['function']['name'] for s in task_schemas(self.schemas, definition)}
        discoverable = {s['function']['name'] for s in discovery_schemas(self.schemas, definition)}
        self.assertTrue({'host_remote', 'host_write_file', 'mission_verify', 'mission_progress'} <= offered)
        self.assertEqual(discoverable, {'host_read_file'})
        self.assertNotIn('mission_read_batch', offered | discoverable)
        self.assertNotIn('host_exec', offered | discoverable)

    def test_legacy_task_retains_discovery(self):
        self.assertEqual(discovery_schemas(self.schemas, {'tools': ['host_remote']}), self.schemas)

    def test_explicit_empty_or_invalid_scope_never_reopens_discovery(self):
        for value in ([], 'host_remote', [None]):
            with self.subTest(value=value):
                self.assertEqual(discovery_schemas(self.schemas, {'discovery_tools': value}), [])

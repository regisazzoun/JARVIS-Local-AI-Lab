import unittest
from jarvis.durable_cycle import discovery_schemas, task_schemas, planning_schemas


class TaskDiscoveryScope(unittest.TestCase):
    def test_planning_observation_boundary_preserves_model_plan_and_blocks_actions(self):
        names=['mission_plan','mission_note','mission_progress','host_read_file','host_policy','host_exec']
        schemas=[{'function':{'name':n}} for n in names]
        offered=planning_schemas(schemas,{'planning_tools':['host_exec']})
        self.assertEqual({s['function']['name'] for s in offered},
                         {'mission_plan','mission_note','mission_progress'})
        self.assertEqual(schemas,[{'function':{'name':n}} for n in names])

    def test_legacy_planning_keeps_reads_and_explicit_empty_scope_closes_them(self):
        schemas=[{'function':{'name':n}} for n in ['mission_plan','host_read_file','host_exec']]
        self.assertEqual([s['function']['name'] for s in planning_schemas(schemas,{})],['mission_plan','host_read_file'])
        self.assertEqual([s['function']['name'] for s in planning_schemas(schemas,{'planning_tools':[]})],['mission_plan'])
        with self.assertRaisesRegex(ValueError,'planning_tools'):
            planning_schemas(schemas,{'planning_tools':'mission_plan'})

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

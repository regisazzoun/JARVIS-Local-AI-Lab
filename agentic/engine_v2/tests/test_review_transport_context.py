"""Review context follows the measured router profile; acceptance stays gated."""
import json
import tempfile
import unittest
from types import SimpleNamespace
from jarvis.mission_store import MissionStore
from jarvis.mission_assurance import review_model


class ReviewTransportContext(unittest.TestCase):
    def test_review_leaves_context_to_router_and_keeps_schema(self):
        with tempfile.TemporaryDirectory() as root:
            store = MissionStore(root)
            mission = store.create('transport test', 'model', 'conversation')
            seen = []
            schema = {'type': 'object', 'properties': {'ok': {'type': 'boolean'}},
                      'required': ['ok'], 'additionalProperties': False}
            def transport(payload):
                seen.append(payload)
                return {'content': json.dumps({'ok': True})}
            registry = SimpleNamespace(mission_store=store,
                context={'mission_id': mission}, assurance_transport=transport)
            self.assertEqual(review_model(registry, 'transport_control', 'check', {}, schema), {'ok': True})
            self.assertNotIn('num_ctx', seen[0]['options'])
            self.assertEqual(seen[0]['format'], schema)
            self.assertNotIn('tools', seen[0])
            registry.assurance_transport = lambda payload: {'content': '{"ok":"invalid"}'}
            with self.assertRaises(ValueError):
                review_model(registry, 'transport_control', 'check', {}, schema)
            self.assertEqual(len([e for e in store.events(mission)
                                  if e['kind'] == 'review_format_rejected']), 2)

import json
import tempfile
import unittest
from pathlib import Path

from jarvis.durable_cycle import coordinator_guidance
from jarvis.mission_store import MissionStore


class PeriodicGuidanceTest(unittest.TestCase):
    def test_periodic_handoff_reaches_p2_without_expanding_other_missions(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = MissionStore(Path(tmp))
            p2 = '3aa717f3887e49daa7daf7e883ee52e4'
            other = store.create('other', 'test', 'test')
            for mission in (p2, other):
                store.event(mission, 'coordinator_instruction', actor='Codex', result={'next': 'historical'})
                store.event(mission, 'coordinator_instruction', actor='Codex-periodic', result={'next': 'retest repaired candidate'})
                store.event(mission, 'coordinator_instruction', actor='JARVIS', result={'next': 'untrusted'})
                store.event(mission, 'coordinator_instruction', task='other-task', actor='Codex', result={'next': 'wrong task'})
                store.event(mission, 'coordinator_periodic_started', actor='Codex-periodic')
            guidance = coordinator_guidance(store, p2, 'step-1')
            self.assertEqual([json.loads(r['result'])['next'] for r in guidance],
                             ['retest repaired candidate', 'historical'])
            self.assertEqual([json.loads(r['result'])['next'] for r in coordinator_guidance(store, other, 'step-1')], ['historical'])
            reopened = MissionStore(Path(tmp))
            self.assertEqual(coordinator_guidance(reopened, p2, 'step-1'), guidance)

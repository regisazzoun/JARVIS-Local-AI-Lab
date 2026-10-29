"""Codex-periodic regression: actual child failure must reach attempt journal.
Temporary SQLite only; this is software coverage, not P2 autonomous acceptance.
"""
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
from engine.jarvis.mission_store import MissionStore

class TestP2CallLifecycle(unittest.TestCase):
    def test_actual_child_failure_is_classified(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = MissionStore(Path(tmp))
            mission = store.create('P2 lifecycle probe', 'test', 'test')
            token = store.begin_call(mission, 'test-task', 'host_remote', {'command': 'exit 7'})
            process = subprocess.run([sys.executable, '-c', 'raise SystemExit(7)'], capture_output=True, text=True)
            self.assertEqual(process.returncode, 7)
            store.finish_call(token, {'ok': True, 'result': {'returncode': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr}}, 0.01)
            states = [e['result'].get('state') for e in store.events(mission) if e['kind'] == 'ATTEMPT_STATE']
            self.assertIn('EXECUTION_FAILED', states, 'Real failed child is absent from attempt lifecycle; broker ok must not mean SUCCESS')
            self.assertNotIn('SUCCESS', states)

import tempfile
import unittest
import json
import subprocess
import sys
from pathlib import Path
from engine.jarvis.mission_store import MissionStore

class TestMissionStoreAttempts(unittest.TestCase):
    def observed_success(self, store, mission):
        process = subprocess.run([sys.executable, '-c', 'print("observed-success")'], capture_output=True, text=True)
        self.assertEqual(process.returncode, 0)
        return store.event(mission, 'tool_finished', tool='host_remote', result={'ok': True, 'result': {'returncode': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr}})

    def test_attempt_state_valid_states(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = MissionStore(root)
            mission_id = store.create(goal="test", model="test", conversation="test")
            
            valid_states = (
                'PENDING', 'DISPATCHED', 'RUNNING', 'NOT_EXECUTED',
                'EXECUTION_FAILED', 'EXECUTED_TEST_FAILED', 'VALIDATION_INCONCLUSIVE',
                'SUCCESS', 'BLOCKED', 'ESCALATED'
            )
            for state in valid_states:
                reference = self.observed_success(store, mission_id) if state == "SUCCESS" else None
                rowid = store.attempt_state(mission_id, state, reference=reference)
                self.assertIsInstance(rowid, int)
                self.assertGreater(rowid, 0)

    def test_attempt_state_invalid_state_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = MissionStore(root)
            mission_id = store.create(goal="test", model="test", conversation="test")
            
            with self.assertRaises(ValueError):
                store.attempt_state(mission_id, "INVALID_STATE")

    def test_attempt_state_persistence_across_instances(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Première instance
            store1 = MissionStore(root)
            mission_id = store1.create(goal="test", model="test", conversation="test")
            
            reference = self.observed_success(store1, mission_id)
            rowid1 = store1.attempt_state(mission_id, "SUCCESS", reference=reference)
            
            # Nouvelle instance
            store2 = MissionStore(root)
            # Lecture directe dans mission_events
            with store2.db() as conn:
                cur = conn.execute(
                    "SELECT mission, kind, result FROM mission_events WHERE rowid=?",
                    (rowid1,)
                )
                row = cur.fetchone()
                self.assertIsNotNone(row)
                self.assertEqual(row["mission"], mission_id)
                self.assertEqual(row["kind"], "ATTEMPT_STATE")
                result = json.loads(row["result"])
                self.assertEqual(result["state"], "SUCCESS")
                self.assertEqual(result["reference"], str(reference))

    def test_attempt_state_without_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = MissionStore(root)
            mission_id = store.create(goal="test", model="test", conversation="test")
            
            rowid = store.attempt_state(mission_id, "BLOCKED")
            with store.db() as conn:
                cur = conn.execute("SELECT result FROM mission_events WHERE rowid=?", (rowid,))
                row = cur.fetchone()
                result = json.loads(row["result"])
                self.assertIn("state", result)
                self.assertEqual(result["state"], "BLOCKED")
                self.assertNotIn("reference", result)

    def test_success_rejects_invalid_or_foreign_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = MissionStore(Path(tmp))
            mission = store.create('test', 'test', 'test')
            foreign = store.create('foreign', 'test', 'test')
            foreign_ref = self.observed_success(store, foreign)
            for reference in (None, "ref-abc", 999999, foreign_ref):
                with self.subTest(reference=reference), self.assertRaises(ValueError):
                    store.attempt_state(mission, 'SUCCESS', reference=reference)

    def test_success_rejects_plan_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = MissionStore(Path(tmp))
            mission = store.create('test', 'test', 'test')
            reference = store.event(mission, 'plan_created', result={'status': 'planned'})
            with self.assertRaises(ValueError):
                store.attempt_state(mission, 'SUCCESS', reference=reference)

    def test_success_rejects_failed_process(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = MissionStore(Path(tmp))
            mission = store.create('test', 'test', 'test')
            process = subprocess.run([sys.executable, '-c', 'raise SystemExit(7)'], capture_output=True, text=True)
            self.assertEqual(process.returncode, 7)
            reference = store.event(mission, 'tool_finished', tool='host_remote', result={'ok': False, 'result': {'returncode': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr}})
            with self.assertRaises(ValueError):
                store.attempt_state(mission, 'SUCCESS', reference=reference)

if __name__ == '__main__':
    unittest.main()
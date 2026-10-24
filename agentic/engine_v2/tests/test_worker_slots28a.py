from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).parents[1]/'broker'))
from host_bridge import runtime_caller
from jarvis.worker import worker_locks


class WorkerSlots(unittest.TestCase):
    def test_slots_share_mode_but_duplicate_and_legacy_workers_are_excluded(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            with worker_locks(root,1),worker_locks(root,2):
                with self.assertRaises(BlockingIOError):
                    with worker_locks(root,1):pass
                with self.assertRaises(BlockingIOError):
                    with worker_locks(root):pass
            with worker_locks(root):
                with self.assertRaises(BlockingIOError):
                    with worker_locks(root,2):pass
            with self.assertRaises(ValueError):
                with worker_locks(root,0):pass

    def test_template_workers_have_actual_jarvis_caller_attribution(self):
        self.assertTrue(runtime_caller('0::/jarvis.slice/jarvis-background.slice/jarvis-mission-worker@2.service\n'))
        self.assertTrue(runtime_caller('0::/jarvis.slice/jarvis-background.slice/jarvis-mission-worker.service\n'))
        self.assertTrue(runtime_caller('0::/system.slice/jarvis-conversation.service\n'))
        self.assertFalse(runtime_caller('0::/user.slice/operator.scope\n'))
        self.assertFalse(runtime_caller('0::/system.slice/not-jarvis-mission-worker@2.service\n'))

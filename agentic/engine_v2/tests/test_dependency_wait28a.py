import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock
from jarvis.core import Core,ROOT
from jarvis.memory import Memory
from jarvis.missions import Missions


class DependencyWait(unittest.TestCase):
    def engine(self,root):
        cfg=json.loads((ROOT/'config/example.json').read_text())
        return Missions(Core(cfg,Memory(root/'runtime/memory.sqlite')),root,start_worker=False)

    def test_worker_does_not_infer_when_all_remaining_tasks_wait_on_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine=self.engine(Path(tmp));s=engine.store;m=s.create('goal','local','conv')
            s.plan(m,[{'id':'held','title':'held','depends':[]},{'id':'later','title':'later','depends':['held']}])
            with s.db() as c:c.execute("update tasks set state='waiting_external' where mission=? and id='held'",(m,))
            engine.cycle=Mock();engine.stop=Mock();engine.stop.wait.side_effect=[False,True]
            engine.worker()
            engine.cycle.run.assert_not_called()
            self.assertEqual(s.get(m)['state'],'waiting_external')
            self.assertEqual(s.tasks(m)[0]['state'],'waiting_external')
            self.assertEqual(len(s.observations(m)),0)
            self.assertIn('execution_deferred_no_ready_task',[e['kind'] for e in s.events(m)])
            # The original ready checkpoint becomes executable after a coordinator
            # or real external event resolves its dependency; nothing was recreated.
            with s.db() as c:c.execute("update tasks set state='validated' where mission=? and id='held'",(m,))
            s.transition(m,'queued')
            self.assertEqual([t['id'] for t in s.ready(m)],['later'])
            self.assertFalse(engine.defer_waiting_tasks(s.get(m)))

    def test_an_unrelated_wait_does_not_block_an_independent_ready_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine=self.engine(Path(tmp));s=engine.store;m=s.create('goal','local','conv')
            s.plan(m,[{'id':'held','title':'held','depends':[]},{'id':'ready','title':'ready','depends':[]}])
            with s.db() as c:c.execute("update tasks set state='waiting_external' where mission=? and id='held'",(m,))
            self.assertFalse(engine.defer_waiting_tasks(s.get(m)))

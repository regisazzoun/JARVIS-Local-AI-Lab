import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from jarvis.compute import register,HybridRouter,ComputeQueue
from jarvis.mission_store import MissionStore


class BenchmarkQueue(unittest.TestCase):
    def test_actual_tool_contract_keeps_queue_reservation_and_native_receipt(self):
        for success in [True,False]:
            with self.subTest(success=success),tempfile.TemporaryDirectory() as temp:
                class Registry:pass
                r=Registry();r.root=Path(temp);r.config={'hybrid_compute':{'nodes':{},'routes':{}}};r.specs={}
                r.mission_store=MissionStore(r.root);m=r.mission_store.create('software fixture','local','conv')
                r.context={'mission_id':m,'task_id':'fixture'}
                def execute(name,args):
                    rows=ComputeQueue(r.root/'runtime/missions.sqlite').recent()
                    self.assertEqual(rows[0]['state'],'running')
                    self.assertEqual(rows[0]['mission'],m)
                    self.assertEqual(name,'host_remote');self.assertEqual(args['action'],'project_exec')
                    self.assertIn('quality_compare.py',args['command'])
                    return {'ok':success,'result':{'stdout':'fixture only'},'error':None if success else 'fixture failure'}
                r.execute=execute;register(r)
                node={'host_profile':'fixture','url':'http://fixture'}
                with patch.object(HybridRouter,'select',return_value=('Dell1',node,'fixture',[])):
                    result=r.specs['compute_benchmark'][4]({'models':['qwen3.5:27b-q4_K_M']})
                rows=ComputeQueue(r.root/'runtime/missions.sqlite').recent()
                self.assertEqual(rows[0]['state'],'finished' if success else 'failed')
                observations=r.mission_store.observations(m)
                self.assertEqual(observations[0]['tool'],'host_remote')
                self.assertEqual(observations[0]['state'],'finished')
                self.assertEqual(observations[0]['result']['ok'],success)
                self.assertEqual(result['returncode'],0 if success else 1)

    def test_unknown_model_never_starts_a_remote_tool(self):
        with tempfile.TemporaryDirectory() as temp:
            class Registry:pass
            r=Registry();r.root=Path(temp);r.config={'hybrid_compute':{'nodes':{},'routes':{}}};r.specs={};r.context={}
            register(r)
            with self.assertRaises(ValueError):r.specs['compute_benchmark'][4]({'models':['unapproved']})
            self.assertFalse(ComputeQueue(r.root/'runtime/missions.sqlite').recent())

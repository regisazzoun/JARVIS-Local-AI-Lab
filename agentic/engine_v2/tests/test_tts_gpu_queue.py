import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from jarvis.compute import register, HybridRouter, ComputeQueue, ResourceUnavailable, release_resident_models
from jarvis.mission_store import MissionStore


class TTSQueueTests(unittest.TestCase):
    def test_native_command_runs_after_unload_inside_held_shared_reservation(self):
        for success in (True,False):
            with self.subTest(success=success),tempfile.TemporaryDirectory() as temp:
                class Registry:pass
                r=Registry();r.root=Path(temp);r.config={'hybrid_compute':{'nodes':{},'routes':{}}};r.specs={}
                r.mission_store=MissionStore(r.root);m=r.mission_store.create('software fixture','model','conv')
                r.context={'mission_id':m,'task_id':'generate'};order=[]
                def unload(router,node):
                    self.assertEqual(router.queue.recent()[0]['state'],'running');order.append('unload');return ['resident']
                def execute(name,args):
                    self.assertEqual(order,['unload']);self.assertEqual(ComputeQueue(r.root/'runtime/missions.sqlite').recent()[0]['state'],'running')
                    self.assertEqual((name,args['host'],args['project'],args['action']),('host_remote','fixture','tts-01','project_exec'))
                    order.append('native');return {'ok':success,'result':{'stdout':'fixture'},'error':None if success else 'fixture error'}
                r.execute=execute;register(r)
                with patch.object(HybridRouter,'select',return_value=('Dell1',{'host_profile':'fixture'},'resident',[])),patch('jarvis.compute.release_resident_models',side_effect=unload):
                    result=r.specs['compute_project_gpu'][4]({'project':'tts-01','command':'fixture'})
                self.assertEqual(order,['unload','native']);self.assertEqual(result['returncode'],0 if success else 1)
                self.assertEqual(ComputeQueue(r.root/'runtime/missions.sqlite').recent()[0]['state'],'finished' if success else 'failed')
                self.assertEqual(r.mission_store.observations(m)[0]['result']['ok'],success)

    def test_failed_unload_releases_queue_without_running_command(self):
        with tempfile.TemporaryDirectory() as temp:
            class Registry:pass
            r=Registry();r.root=Path(temp);r.config={'hybrid_compute':{'nodes':{},'routes':{}}};r.specs={};r.context={'mission_id':'fixture'}
            r.execute=lambda *a:self.fail('Must not run before verified unload');register(r)
            with patch.object(HybridRouter,'select',return_value=('Dell1',{},'resident',[])),patch('jarvis.compute.release_resident_models',side_effect=ResourceUnavailable('fixture unload failure')):
                with self.assertRaises(ResourceUnavailable):r.specs['compute_project_gpu'][4]({'project':'tts-01','command':'fixture'})
            self.assertEqual(ComputeQueue(r.root/'runtime/missions.sqlite').recent()[0]['state'],'failed')

    def test_unload_has_no_prompt_and_requires_observed_empty_residency(self):
        class Router:
            def __init__(self):self.calls=0
            def fetch(self,url):
                self.calls+=1;return {'models':[{'name':'resident'}]} if self.calls==1 else {'models':[]}
        router=Router();payloads=[]
        def response(request,timeout):
            payloads.append(json.loads(request.data));return io.BytesIO(b'{"done":true}')
        with patch('urllib.request.urlopen',side_effect=response):self.assertEqual(release_resident_models(router,{'url':'http://fixture'}),['resident'])
        self.assertEqual(payloads,[{'model':'resident','keep_alive':0,'stream':False}]);self.assertEqual(router.calls,2)

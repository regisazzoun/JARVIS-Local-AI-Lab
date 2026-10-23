"""Software-only scheduling tests; never counted as agentic demonstrations."""
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from jarvis.compute import ComputeQueue,HybridRouter,ResourceUnavailable,classify_request

class HybridTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.database=Path(self.tmp.name)/'missions.sqlite'
        self.config={'conversation_model':'qwen27','nodes':{'Mac-mini':{'enabled':True,'roles':['conversation','critical'],'url':'http://mac','conversation_model':'qwen27'},'Dell1':{'enabled':True,'roles':['mission','critical'],'url':'http://dell','mission_model':'large70'},'Dell2':{'enabled':False,'roles':['mission'],'url':'http://must-not-be-contacted','mission_model':'large70'}},'routes':{'conversation':['Mac-mini'],'critical':['Dell1','Mac-mini'],'mission':['Dell1','Dell2']}}
        self.urls=[]
    def fetch(self,url):
        self.urls.append(url)
        return {'models':[{'name':'qwen27','size':16},{'name':'large70','size':43}]}
    def test_owner_conversation_model_cannot_be_replaced_by_requested_lighter_model(self):
        r=HybridRouter(self.config,self.database,self.fetch)
        self.assertEqual(r.select('conversation','tiny')[2],'qwen27')
    def test_offline_second_dell_is_not_discovered_or_assigned(self):
        r=HybridRouter(self.config,self.database,self.fetch);states=r.discover()
        self.assertEqual(states[-1]['state'],'offline_pending');self.assertFalse(any('must-not' in url for url in self.urls))
    def test_future_enrolled_second_node_gets_work_while_first_is_busy(self):
        self.config['nodes']['Dell2'].update(enabled=True,url='http://dell2-fixture')
        r=HybridRouter(self.config,self.database,self.fetch)
        busy=r.queue.enter('Dell1','large70','mission')
        try:
            self.assertEqual(r.select('mission')[0],'Dell2')
            self.assertTrue(any('dell2-fixture' in url for url in self.urls))
        finally:r.queue.finish(busy)
    def test_critical_fallback_keeps_local_qwen_and_mission_retains_unavailability(self):
        def fetch(url):
            if 'dell' in url:raise OSError('software fixture unavailable')
            return self.fetch(url)
        r=HybridRouter(self.config,self.database,fetch)
        name,node,model,failures=r.select('critical');self.assertEqual((name,model),('Mac-mini','qwen27'));self.assertTrue(failures)
        with self.assertRaises(ResourceUnavailable):r.select('mission')
    def test_ram_pressure_rejects_new_load_before_request(self):
        r=HybridRouter(self.config,self.database,self.fetch);r.nodes['Dell1']['minimum_available_ram_bytes']=64
        with patch.object(r,'resources',return_value={'memory_available_bytes':12,'gpu':[]}):
            with self.assertRaises(ResourceUnavailable):r.select('mission')
    def test_priority_between_turns_is_shared_across_router_instances(self):
        a=ComputeQueue(self.database);b=ComputeQueue(self.database);active=a.enter('Dell1','large70','mission');order=[]
        def run(role):
            job=b.enter('Dell1','large70',role,timeout=3);order.append(role);b.finish(job)
        mission=threading.Thread(target=run,args=('mission',));mission.start()
        deadline=time.monotonic()+2
        while len(a.recent())<2 and time.monotonic()<deadline:time.sleep(.01)
        critical=threading.Thread(target=run,args=('critical',));critical.start()
        while len(a.recent())<3 and time.monotonic()<deadline:time.sleep(.01)
        a.finish(active);mission.join(3);critical.join(3)
        self.assertEqual(order,['critical','mission'])
        self.assertFalse(any(row['state']=='running' for row in a.recent()))
    def test_expired_inference_lease_is_recoverable_without_touching_missions(self):
        q=ComputeQueue(self.database);old=q.enter('Dell1','large70','mission')
        with q.db() as c:c.execute('UPDATE compute_jobs SET expires=? WHERE id=?',(time.time()-1,old))
        new=q.enter('Dell1','large70','critical',timeout=1);q.finish(new)
        self.assertEqual(next(row for row in q.recent() if row['id']==old)['state'],'abandoned')
    def test_failed_reservation_does_not_leave_stuck_queue(self):
        q=ComputeQueue(self.database);active=q.enter('Dell1','large70','mission')
        with self.assertRaises(ResourceUnavailable):q.enter('Dell1','large70','critical',timeout=.01)
        q.finish(active);self.assertEqual(q.recent()[0]['state'],'failed')
    def test_complexity_classifier_preserves_daily_conversation(self):
        self.assertEqual(classify_request('Bonjour, quelle heure est-il ?'),'conversation')
        self.assertEqual(classify_request('Fais une analyse approfondie de ce problème.'),'critical')
    def test_conversation_and_fallback_share_a_stable_context_profile(self):
        self.config['nodes']['Mac-mini']['inference_num_ctx']=16384
        def fetch(url):
            if 'dell' in url:raise OSError('fixture unreachable')
            return self.fetch(url)
        r=HybridRouter(self.config,self.database,fetch)
        class Reply:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def __iter__(self):return iter([json.dumps({'message':{'content':'OK'},'done':True}).encode()])
        with patch('jarvis.compute.urllib.request.urlopen',side_effect=lambda *a,**kw:Reply()) as opened:
            for role in ['conversation','critical']:
                message,metrics=r.infer({'messages':[],'options':{'num_ctx':8192}},role)
                sent=json.loads(opened.call_args.args[0].data)
                self.assertEqual(sent['options']['num_ctx'],16384)
                self.assertEqual(metrics['effective_model'],'qwen27')
                self.assertEqual(message['content'],'OK')
    def test_streamed_inference_preserves_tools_records_actual_selected_model(self):
        r=HybridRouter(self.config,self.database,self.fetch)
        class Reply:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def __iter__(self):return iter([json.dumps({'message':{'content':'Salut','thinking':'never export reasoning'}}).encode(),json.dumps({'message':{'tool_calls':[{'function':{'name':'actual_test_tool','arguments':{}}}]},'done':True,'eval_count':2,'eval_duration':1000}).encode()])
        with patch('jarvis.compute.urllib.request.urlopen',return_value=Reply()) as urlopen:
            message,metrics=r.infer({'model':'tiny','messages':[]})
        self.assertNotIn('thinking',message);self.assertEqual(message['content'],'Salut');self.assertEqual(len(message['tool_calls']),1)
        self.assertEqual(metrics['effective_model'],'qwen27');self.assertIsNotNone(metrics['first_content_s'])
        sent=json.loads(urlopen.call_args.args[0].data);self.assertEqual(sent['keep_alive'],-1)
        self.assertEqual(r.queue.recent()[0]['state'],'finished')

    def test_busy_dell_critical_request_returns_local_qwen_after_bounded_wait(self):
        self.config['interactive_queue_timeout']=.02
        router=HybridRouter(self.config,self.database,self.fetch)
        active=router.queue.enter('Dell1','large70','mission')
        class Reply:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def __iter__(self):return iter([json.dumps({'message':{'content':'Local fallback'},'done':True}).encode()])
        with patch('jarvis.compute.urllib.request.urlopen',return_value=Reply()) as transport:
            answer,metrics=router.infer({'model':'qwen27','messages':[]},'critical')
        self.assertEqual(metrics['node'],'Mac-mini');self.assertEqual(metrics['effective_model'],'qwen27')
        self.assertIn('queue timeout',metrics['fallback_reason'])
        self.assertTrue(transport.call_args.args[0].full_url.startswith('http://mac/'))
        router.queue.finish(active)

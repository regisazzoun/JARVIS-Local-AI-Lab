"""Execution focus preserves live task IDs, contracts and durable full objectives."""
import json
from pathlib import Path
import tempfile
import unittest
from jarvis.core import Core, ROOT
from jarvis.memory import Memory
from jarvis.missions import Missions
from jarvis.durable_cycle import task_schemas


class TaskContextTests(unittest.TestCase):
    def test_new_task_does_not_replay_other_task_receipts_or_completion_claims(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);memory=Memory(root/'runtime/memory.sqlite');cfg=json.loads((ROOT/'config/example.json').read_text())
            cfg.update(durable_num_ctx=16384,durable_cycle_rounds=1)
            core=Core(cfg,memory);engine=Missions(core,root,start_worker=False);s=engine.store
            m=s.create('software fixture','local','conv')
            s.plan(m,[{'id':'received','title':'old','depends':[]},{'id':'current','title':'new','depends':['received'],'tools':['host_read_file']}])
            with s.db() as c:c.execute("UPDATE tasks SET state='validated' WHERE mission=? AND id='received'",(m,))
            token=s.begin_call(m,'received','host_read_file',{'path':'/old-report'})
            s.finish_call(token,{'ok':True,'result':{'stdout':'OLD_SUCCESS_NOT_CURRENT_TASK'}},.1)
            s.event(m,'model_checkpoint',task='received',actor='JARVIS',result={'text':'OLD_COMPLETION_CLAIM'})
            seen=[]
            def transport(payload):
                seen.append(json.dumps(payload));return {'role':'assistant','content':'Fixture only'}
            engine.execution_core.transport=transport;engine.cycle.run(s.get(m))
            self.assertNotIn(token,seen[0]);self.assertNotIn('OLD_SUCCESS_NOT_CURRENT_TASK',seen[0]);self.assertNotIn('OLD_COMPLETION_CLAIM',seen[0])
            self.assertEqual(s.observations(m,'received')[0]['id'],token)

    def test_compute_status_view_keeps_actual_routes_without_old_resource_corpus(self):
        from jarvis.durable_cycle import model_observation
        value={'conversation_model':'local27','nodes':[{'id':'Dell1','status':'ready'}],
               'jobs':[{'id':str(i),'state':'finished','metrics':json.dumps({'effective_model':'actual80','end_to_end_s':2,'admission_resources':{'raw':'x'*20000}})} for i in range(20)]}
        original=json.dumps(value)
        view=model_observation(value)
        self.assertEqual(view['jobs'][0]['metrics']['effective_model'],'actual80')
        self.assertEqual([j['id'] for j in view['jobs']],[str(i) for i in range(8)])
        self.assertEqual(view['recorded_jobs_count'],20)
        self.assertLess(len(json.dumps(view)),5000)
        self.assertEqual(json.dumps(value),original)

    def test_known_tool_can_be_discovered_without_bypassing_execution_phase(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);memory=Memory(root/'runtime/memory.sqlite');cfg=json.loads((ROOT/'config/example.json').read_text())
            cfg.update(durable_num_ctx=16384,durable_cycle_rounds=2);core=Core(cfg,memory);engine=Missions(core,root,start_worker=False)
            m=engine.store.create('software fixture','local','conv')
            engine.store.plan(m,[{'id':'active','title':'task','depends':[],'tools':['host_read_file']}])
            seen=[]
            def transport(payload):
                seen.append({s['function']['name'] for s in payload['tools']})
                return {'role':'assistant','tool_calls':[{'function':{'name':'runtime_versions','arguments':{}}}]}
            registry=engine.execution_core.tools;registry.specs['runtime_versions']=('fixture read',{},[],'read_only',lambda a:{'observed':True})
            engine.execution_core.transport=transport;engine.cycle.run(engine.store.get(m))
            self.assertNotIn('runtime_versions',seen[0]);self.assertIn('runtime_versions',seen[1])
            calls=[o for o in engine.store.observations(m) if o['tool']=='runtime_versions']
            self.assertFalse(calls[0]['result']['ok']);self.assertTrue(calls[1]['result']['ok'])
            self.assertNotIn('intervention_report',seen[1])
    def test_legacy_schemas_stay_available_without_a_tool_selection(self):
        schemas=[{'function':{'name':'host_remote'}},{'function':{'name':'other'}}]
        self.assertEqual(task_schemas(schemas,{}),schemas)
        self.assertEqual(task_schemas(schemas,{'tools':['host_remote']}),schemas[:1])

    def test_long_goal_scoped_execution_keeps_contract_and_fits_budget(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);memory=Memory(root/'runtime/memory.sqlite')
            config=json.loads((ROOT/'config/example.json').read_text())
            config.update(durable_num_ctx=16384,durable_cycle_rounds=1)
            captured=[]
            def transport(payload):
                captured.append(payload)
                return {'role':'assistant','content':'Software fixture: no operation executed.'}
            core=Core(config,memory,transport=transport)
            engine=Missions(core,root,start_worker=False)
            engine.execution_core.transport=transport
            goal='User objective: '+'many requirements. '*1400+'Keep chosen local model.'
            ident=engine.store.create(goal,'local','conv',spec={'autonomous':False})
            contract={'report_path':'/var/lib/jarvis/projects/example/report.md',
                      'semantic':[{'kind':'json','source':{'tool':'host_read_file','arguments':{'path':'/observed.json'}},'expected':{'/valid':True}}]}
            engine.store.plan(ident,[{'id':'real_task_42','title':'Real task','depends':[],
                'objective':'Execute the pending test','tools':['host_remote','host_read_file','host_write_file'],'contract':contract}])
            engine.cycle.run(engine.store.get(ident))
            payload=captured[0];state=json.loads(payload['messages'][1]['content'])
            self.assertEqual(state['active_task']['id'],'real_task_42')
            self.assertEqual(state['active_task']['contract'],contract)
            self.assertEqual(state['active_task_interface']['id'],'real_task_42')
            self.assertEqual(json.loads(state['active_task_interface']['verification_calls'][0]['contract']),contract['semantic'][0])
            names={s['function']['name'] for s in payload['tools']}
            self.assertIn('host_remote',names);self.assertIn('mission_plan',names)
            self.assertNotIn('host_github',names)
            self.assertEqual(engine.store.get(ident)['goal'],goal)
            prepared=[e['result'] for e in engine.store.events(ident) if e['kind']=='inference_context_prepared'][0]
            self.assertLess(prepared['base_chars'],prepared['budget_chars'])
            registry=engine.execution_core.tools
            progress=registry.execute('mission_progress',{})
            self.assertEqual(progress['result']['goal'],goal)
            error=registry.execute('mission_task_complete',{'id':'invented','evidence_id':'invented','report_path':'invented'})
            self.assertFalse(error['ok']);self.assertIn('real_task_42',error['error'])
            self.assertNotEqual(engine.store.tasks(ident)[0]['state'],'validated')

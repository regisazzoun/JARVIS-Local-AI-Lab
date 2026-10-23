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

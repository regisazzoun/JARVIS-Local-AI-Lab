"""Software fixture: no inference, remote command or autonomy claim."""
import copy,json,tempfile,unittest
from pathlib import Path
from jarvis.core import Core,ROOT
from jarvis.memory import Memory
from jarvis.missions import Missions
class DialogueTests(unittest.TestCase):
 def test_real_engine_keeps_tool_reply_for_next_model_turn(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);memory=Memory(root/'runtime/memory.sqlite')
   config=json.loads((ROOT/'config/example.json').read_text());config.update(durable_cycle_rounds=2,durable_num_ctx=16384)
   core=Core(config,memory);engine=Missions(core,root,start_worker=False)
   ident=engine.store.create('Software fixture','local','conv',spec={'distributed_authority':True,'authority_requirements':['Q1','Q2']})
   seen=[]
   def transport(payload):
    seen.append(copy.deepcopy(payload))
    return {'role':'assistant','tool_calls':[{'function':{'name':'authority_work','arguments':{'issue':'Q1','kind':'inspect','executor':'Dell1','command':'NO_REMOTE_EXECUTION_EXPECTED','summary':'Fixture','operation_id':'fixture'}}}]}
   engine.execution_core.transport=transport
   engine.cycle.run(engine.store.get(ident))
   self.assertEqual(len(seen),2)
   self.assertTrue(any(m['role']=='assistant' for m in seen[1]['messages']))
   self.assertTrue(any(m['role']=='tool' and 'actual Qwen80B' in m['content'] for m in seen[1]['messages']))
   self.assertFalse(any(o['tool']=='host_remote' for o in engine.store.observations(ident)))
 def test_failed_inspection_keeps_recovery_tools_available_before_plan(self):
  from jarvis.distributed_authority import Authority
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);memory=Memory(root/'runtime/memory.sqlite')
   config=json.loads((ROOT/'config/example.json').read_text());config.update(durable_cycle_rounds=1,durable_num_ctx=32768)
   core=Core(config,memory);engine=Missions(core,root,start_worker=False)
   ident=engine.store.create('Software fixture','local','conv',spec={'distributed_authority':True,'authority_requirements':['Q1']})
   engine.execution_core.tools.context={'mission_id':ident,'task_id':None}
   engine.execution_core.tools.mission_store=engine.store
   authority=Authority(engine.execution_core.tools)
   state=authority.state();state['executions']['31']={'issue':'Q1','kind':'inspect','execution':{'returncode':2},'before':{},'after':{}}
   authority.save(state)
   seen=[]
   def transport(payload):
    seen.append(payload)
    return {'role':'assistant','content':'fixture'}
   engine.execution_core.transport=transport
   engine.cycle.run(engine.store.get(ident))
   names={s['function']['name'] for s in seen[0]['tools']}
   self.assertTrue({'authority_plan','authority_work','authority_analyze','authority_read_execution'}<=names)
   self.assertEqual(engine.store.plans(ident),[])
if __name__=='__main__':unittest.main()

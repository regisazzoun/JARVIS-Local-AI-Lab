import json,tempfile,unittest
from pathlib import Path
from unittest.mock import Mock
from jarvis.core import Core,ROOT
from jarvis.memory import Memory
from jarvis.missions import Missions

class ChatPromotionTest(unittest.TestCase):
    def test_prior_read_is_preserved_and_mutation_is_deferred_before_effect(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);memory=Memory(root/'runtime/memory.sqlite')
            config=json.loads((ROOT/'config/example.json').read_text());config['voice_summary']=False
            responses=iter([
              {'role':'assistant','content':'','tool_calls':[{'function':{'name':'disk_usage','arguments':{}}}]},
              {'role':'assistant','content':'','tool_calls':[{'function':{'name':'host_write_file','arguments':{'path':'/var/lib/jarvis/projects/unit-promotion.txt','content':'unit fixture'}}}]}])
            core=Core(config,memory,lambda p:next(responses));missions=Missions(core,root,start_worker=False)
            forbidden=Mock(side_effect=AssertionError('Mutation must be deferred'))
            old=core.tools.specs['host_write_file'];core.tools.specs['host_write_file']=(*old[:4],forbidden)
            result=core.chat('Create a test file',config['default_model'])
            self.assertTrue(result['mission_id']);forbidden.assert_not_called()
            observations=missions.store.observations(result['mission_id'])
            self.assertEqual(len(observations),1);self.assertEqual(observations[0]['tool'],'disk_usage')
            self.assertTrue(observations[0]['result']['imported_from_chat'])
            self.assertEqual(len(memory.history(result['conversation'])),2)

if __name__=='__main__':unittest.main()

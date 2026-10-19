import json,tempfile,unittest
from pathlib import Path
from jarvis.core import Core,ROOT
from jarvis.memory import Memory
from jarvis.missions import Missions

class ExecutionIsolationTest(unittest.TestCase):
    def test_durable_lock_does_not_block_conversation(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);memory=Memory(root/'runtime/memory.sqlite')
            config=json.loads((ROOT/'config/example.json').read_text());config['voice_summary']=False
            core=Core(config,memory,transport=lambda payload:{'role':'assistant','content':'Conversation disponible.'})
            missions=Missions(core,root,start_worker=False)
            self.assertIsNot(core.tools,missions.execution_core.tools)
            self.assertIs(core.memory,missions.execution_core.memory)
            missions.execution_core.tools.context={'mission_id':'durable-test'}
            missions.execution_core.lock.acquire()
            try:
                response=core.chat('Bonjour',config['default_model'])
                self.assertEqual(response['answer'],'Conversation disponible.')
                self.assertEqual(missions.execution_core.tools.context['mission_id'],'durable-test')
                self.assertFalse(core.lock.locked())
            finally:missions.execution_core.lock.release()

if __name__=='__main__':unittest.main()

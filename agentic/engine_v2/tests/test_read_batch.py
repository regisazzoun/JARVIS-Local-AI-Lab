import tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from jarvis.mission_store import MissionStore
from jarvis.durable_tools import register

class ReadBatchTest(unittest.TestCase):
    def test_valid_reads_continue_after_invalid_entry_and_normalize_explicit_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            store=MissionStore(Path(temp));ident=store.create('test','local','conversation')
            executed=[]
            def execute(name,args):executed.append((name,args));return {'ok':True,'result':{'stdout':'unit fixture, not a real GitHub read'}}
            registry=SimpleNamespace(mission_store=store,context={'mission_id':ident,'task_id':'a'},specs={},execute=execute)
            register(registry)
            result=registry.specs['mission_read_batch'][4]({'calls':[
                {'tool':'host_exec','arguments':{'command':'false'}},
                {'tool':'host_github','repository':'owner/repo','arguments':{'path':'docs'}}]})
            self.assertEqual(len(executed),1)
            self.assertEqual(executed[0],('host_github',{'repository':'owner/repo','path':'docs','action':'file'}))
            self.assertFalse(result['results'][0]['ok']);self.assertTrue(result['results'][1]['ok'])
            self.assertEqual(result['returncode'],1)
            self.assertEqual(len(store.observations(ident)),1)

if __name__=='__main__':unittest.main()

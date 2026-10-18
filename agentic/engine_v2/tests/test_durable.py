import tempfile
import time
import unittest
from pathlib import Path
from jarvis.mission_store import MissionStore

class DurableJournalTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.store=MissionStore(Path(self.temp.name))
        self.ident=self.store.create('test','local','conversation')
    def tearDown(self): self.temp.cleanup()
    def test_dependency_order_and_restart(self):
        self.store.plan(self.ident,[{'id':'a','title':'A','depends':[]},{'id':'b','title':'B','depends':['a']}])
        self.assertEqual([t['id'] for t in self.store.ready(self.ident)],['a'])
        with self.store.db() as c:c.execute("UPDATE tasks SET state='validated' WHERE id='a'")
        reopened=MissionStore(Path(self.temp.name))
        self.assertEqual([t['id'] for t in reopened.ready(self.ident)],['b'])
    def test_invalid_plan_is_atomic(self):
        with self.assertRaises(ValueError):self.store.plan(self.ident,[{'id':'a','title':'A','depends':['b']}])
        self.assertEqual(self.store.tasks(self.ident),[])
    def test_lost_lease_recovers_after_more_than_five_cycles(self):
        for i in range(8):
            row=self.store.claim('worker')
            self.assertEqual(row['id'],self.ident)
            with self.store.db() as c:c.execute('UPDATE missions SET lease_until=? WHERE id=?',(time.time()-1,self.ident))
        self.assertEqual(self.store.get(self.ident)['attempts'],8)
    def test_intent_survives_crash_without_claiming_success(self):
        token=self.store.begin_call(self.ident,'a','host_exec',{'command':'true'})
        reopened=MissionStore(Path(self.temp.name))
        self.assertEqual(reopened.observations(self.ident)[0]['state'],'started')
        reopened.finish_call(token,{'ok':True,'result':{'stdout':'done'}},.1)
        self.assertEqual(reopened.observations(self.ident)[0]['state'],'finished')
        self.assertEqual(reopened.events(self.ident)[-1]['kind'],'tool_finished')
    def test_explicit_interruption_wins_over_worker_finish(self):
        self.store.claim('worker')
        self.store.transition(self.ident,'interrupted')
        self.store.transition(self.ident,'completed')
        self.assertEqual(self.store.get(self.ident)['state'],'interrupted')
    def test_plan_cannot_overwrite_completed_work(self):
        self.store.plan(self.ident,[{'id':'a','title':'A','depends':[]}])
        self.store.plan(self.ident,[{'id':'other','title':'other','depends':[]}])
        self.assertEqual(self.store.tasks(self.ident)[0]['id'],'a')

if __name__=='__main__':unittest.main()

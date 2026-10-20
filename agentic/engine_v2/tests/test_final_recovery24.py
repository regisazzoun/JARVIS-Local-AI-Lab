import json,tempfile,time,unittest,hashlib
from pathlib import Path
from jarvis.mission_store import MissionStore
from jarvis.missions import Missions
class FinalRecovery(unittest.TestCase):
 def test_recover_real_receipt_but_reject_changed_stale_or_revised_report(self):
  for case in ['valid','changed','stale','revision']:
   with self.subTest(case=case),tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);store=MissionStore(root);ident=store.create('objective','model','conversation','',{})
    store.plan(ident,[{'id':'t','title':'task','depends':[]}])
    done=time.time()-2
    with store.db() as c:c.execute('update tasks set state="validated",updated=? where mission=?',(done,ident))
    path=root/'runtime/reports'/ident/'RAPPORT-FINAL.md';path.parent.mkdir(parents=True);body='Rapport réel conservé avec preuve et réserves.';path.write_text(body)
    token=store.begin_call(ident,None,'intervention_report',{'content':body});store.finish_call(token,{'ok':True,'result':{'path':str(path),'sha256':hashlib.sha256(body.encode()).hexdigest()}},0.1)
    if case=='changed':path.write_text('different report')
    if case=='stale':
     with store.db() as c:c.execute('update tool_calls set created=? where id=?',(done-1,token))
    if case=='revision':store.event(ident,'final_report_revision_requested',actor='Codex')
    engine=Missions.__new__(Missions);engine.store=store;row=store.get(ident);engine.recover_final_report(row)
    self.assertEqual(bool(row.get('report_path')),case=='valid')
    self.assertEqual(store.tasks(ident)[0]['state'],'validated')

import sys,unittest
sys.path.insert(0,'/opt/jarvis/conversation')
from jarvis.mission_assurance import report_model_view,encoded
class ReviewView(unittest.TestCase):
 def snapshot(self):
  d={k:{} for k in ('counts','closure','active_contracts')}
  d.update(mission='fixture',created=0,scope_task='D04-RESTITUTION',raw_goal='fixture',infrastructure_author='Codex',plan_and_operations_author='journal',tasks=[{'id':'D04','state':'validated'},{'id':'D04-RESTITUTION','state':'running'}],plans=[],semantic_verifications=[],receipts=[{'reference':f'{i:032x}','arguments':{},'observed':{}} for i in range(1000)],plan_definitions=[{'plan':{'tasks':[{'id':'D04','objective':'old'*10000},{'id':'D04-RESTITUTION','objective':'active'}]}}])
  return d
 def test_cited_receipts_retained_without_shipping_entire_index(self):
  snapshot=self.snapshot();before=encoded(snapshot);reference=snapshot['receipts'][123]['reference'];v=report_model_view(snapshot,'D04 '+reference,recent=0)
  self.assertIn(reference,v['known_receipt_references']);self.assertEqual(len(v['known_receipt_references']),1)
  self.assertEqual(v['known_receipt_reference_count'],1000);self.assertEqual(before,encoded(snapshot))
 def test_inactive_task_name_in_title_does_not_duplicate_legacy_plan(self):
  snapshot=self.snapshot();v=report_model_view(snapshot,'D04 — rapport courant',recent=0)
  self.assertEqual([t['id'] for t in v['plan_definitions'][0]['plan']['tasks']],['D04-RESTITUTION'])
  self.assertEqual(len(v['tasks']),2)
if __name__=='__main__':unittest.main()

"""Canonical store regression for runaway planning and interrupt/requeue races."""
import json,tempfile,unittest
from jarvis.mission_store import MissionStore
from jarvis.planning_progress import assess,require_revision_capacity
class PlanningProgressTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.s=MissionStore(self.tmp.name);self.m=self.s.create('fixture','model','conv')
 def review(self,version,issues=None,missing=(),status='FAIL'):
  return self.s.event(self.m,'coverage_review',result={'plan_version':version,'status':status,'issues':issues or [],'coverage':[{'requirement':r,'covered':False} for r in missing]})
 def test_new_ids_and_growing_plan_do_not_hide_same_artifact_conflict(self):
  for i in range(1,4):
   self.review(i,[f'Unordered artifact writers new{i} and renamed{i} both declare /artifact. Declare a dependency order'])
   state=assess(self.s,self.m);self.assertFalse(state['meaningful'])
  self.assertTrue(state['blocked']);self.assertEqual(state['failed_reviews_retained'],3)
  with self.assertRaisesRegex(ValueError,'escalated'):require_revision_capacity(MissionStore(self.tmp.name),self.m)
 def test_actual_reduction_of_uncovered_requirements_is_progress(self):
  self.review(1,missing=('R1','R2','R3'));assess(self.s,self.m)
  self.review(2,missing=('R1','R2'));state=assess(self.s,self.m)
  self.assertTrue(state['meaningful']);self.assertEqual(state['nonimproving_reviews'],0)
 def test_repeated_observation_does_not_add_an_attempt(self):
  self.review(1,missing=('R1',));state=assess(self.s,self.m)
  self.assertEqual(assess(self.s,self.m),state)
  self.review(1,missing=('R1',));self.assertEqual(assess(self.s,self.m)['nonimproving_reviews'],1)
 def test_pass_is_progress_and_history_remains(self):
  self.review(1,missing=('R1',));assess(self.s,self.m);self.review(2,status='PASS')
  state=assess(self.s,self.m);self.assertTrue(state['meaningful']);self.assertFalse(state['blocked']);self.assertEqual(state['failed_reviews_retained'],1)
 def test_verified_structural_repair_opens_documented_segment_without_erasing_failures(self):
  for i in range(1,4):self.review(i,missing=('R1',))
  self.assertTrue(assess(self.s,self.m)['blocked'])
  for i in range(3):self.s.plan(self.m,[{'id':k,'title':k+str(i)} for k in ['a','b','c']],author='fixture',expected_version=i)
  before=self.s.plans(self.m)[-1];self.s.plan(self.m,[{'id':'a','title':'a'}],author='fixture',expected_version=3);after=self.s.plans(self.m)[-1]
  self.s.event(self.m,'coordinator_planning_repair_verified',actor='Codex',result={'before_version':3,'plan_version':4,'before_sha256':before['sha256'],'after_sha256':after['sha256'],'actual_task_reduction_verified':True})
  self.review(4,missing=('R1','R2'));state=assess(self.s,self.m)
  self.assertFalse(state['blocked']);self.assertEqual(state['failed_reviews_retained'],4)
 def test_model_note_cannot_forge_repair(self):
  for i in range(1,4):self.review(i,missing=('R1',))
  self.s.event(self.m,'coordinator_planning_repair_verified',actor='JARVIS',result={'plan_version':4,'actual_task_reduction_verified':True})
  self.review(4,missing=('R1',));self.assertTrue(assess(self.s,self.m)['blocked'])
 def runtime_repair(self,actor='Codex',correct=True):
  from pathlib import Path
  import hashlib
  path=self.s.root/'jarvis/interface.py';path.parent.mkdir(exist_ok=True);path.write_text('corrected transport')
  digest=hashlib.sha256(path.read_bytes()).hexdigest() if correct else '0'*64
  return self.s.event(self.m,'coordinator_planning_repair_verified',actor=actor,result={'actual_interface_repair_verified':True,'deployed_manifest':{'interface.py':digest}})
 def test_verified_runtime_repair_reopens_cached_block_without_faking_a_pass(self):
  for i in range(1,4):self.review(i,missing=('R1',))
  self.assertTrue(assess(self.s,self.m)['blocked'])
  repair=self.runtime_repair();state=assess(self.s,self.m)
  self.assertFalse(state['blocked']);self.assertEqual(state['status'],'FAIL');self.assertEqual(state['failed_reviews_retained'],3);self.assertEqual(state['runtime_repair_event'],repair)
 def test_three_new_failures_reblock_the_repaired_segment(self):
  for i in range(1,4):self.review(i,missing=('R1',))
  self.runtime_repair()
  for i in range(4,7):self.review(i,missing=('R1',));state=assess(self.s,self.m)
  self.assertTrue(state['blocked']);self.assertEqual(state['failed_reviews_retained'],6);self.assertEqual(state['nonimproving_reviews'],3)
 def test_wrong_manifest_or_model_actor_cannot_unlock(self):
  for i in range(1,4):self.review(i,missing=('R1',))
  self.runtime_repair(correct=False);self.assertTrue(assess(self.s,self.m)['blocked'])
  self.runtime_repair(actor='JARVIS');self.assertTrue(assess(self.s,self.m)['blocked'])
 def test_runtime_drift_invalidates_repair(self):
  from pathlib import Path
  for i in range(1,4):self.review(i,missing=('R1',))
  self.runtime_repair();self.assertFalse(assess(self.s,self.m)['blocked'])
  (self.s.root/'jarvis/interface.py').write_text('different code');self.assertTrue(assess(self.s,self.m)['blocked'])
 def test_real_pending_path_repair_is_progress_even_if_review_still_fails(self):
  with self.s.db() as db:db.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'report_workspace':'/reports'}),self.m))
  tasks=[{'id':k,'title':k,'contract':{'report_path':'/invalid/'+k+'.md'}} for k in ('a','b','c')]
  self.s.plan(self.m,tasks);self.review(1,missing=('R1',));assess(self.s,self.m)
  tasks[0]['contract']['report_path']='/reports/a.md'
  self.s.plan(self.m,tasks,expected_version=1);self.review(2,missing=('R1',));state=assess(self.s,self.m)
  self.assertTrue(state['meaningful']);self.assertFalse(state['blocked']);self.assertEqual(state['nonimproving_reviews'],0)
  self.assertEqual(state['defects'],['requirement:R1','unwritable-report:b','unwritable-report:c'])
 def test_verified_repair_does_not_credit_endless_unreviewed_plan_saves(self):
  for i in range(1,4):
   self.s.plan(self.m,[{'id':'a','title':'candidate '+str(i)}],expected_version=i-1);self.review(i,missing=('R1',))
  self.runtime_repair();self.assertFalse(assess(self.s,self.m)['blocked'])
  for i in range(4,7):
   self.s.plan(self.m,[{'id':'a','title':'new unreviewed candidate '+str(i)}],expected_version=i-1)
   state=assess(self.s,self.m)
   self.assertFalse(state['meaningful']);self.assertTrue(state['review_pending']);self.assertEqual(state['status'],'INSUFFICIENT')
  self.assertEqual(state['failed_reviews_retained'],3)
 def test_pass_of_an_old_version_does_not_receive_a_new_unreviewed_candidate(self):
  self.s.plan(self.m,[{'id':'a','title':'candidate1'}]);self.review(1,status='PASS')
  self.assertTrue(assess(self.s,self.m)['meaningful'])
  self.s.plan(self.m,[{'id':'a','title':'candidate2'}],expected_version=1)
  state=assess(self.s,self.m);self.assertFalse(state['meaningful']);self.assertEqual(state['status'],'INSUFFICIENT')

"""An oversize semantic review must not hide independently established defects."""
import hashlib
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from jarvis import mission_assurance as app
from jarvis.mission_store import MissionStore
from jarvis.mission_context_budget import ContextCapacityError

class CapacityBlockersTests(unittest.TestCase):
 def test_collision_rejects_without_claiming_requirement_coverage(self):
  with tempfile.TemporaryDirectory() as root:
   store=MissionStore(root);m=store.create('test goal','fixture','fixture')
   store.plan(m,[{'id':i,'title':i,'depends':[],'tools':[],'artifacts':[], 'contract':{'report_path':'/tmp/shared.md'}} for i in ['a','b']],author='fixture')
   req={'contract_version':app.GOAL_VERSION,'goal_sha256':hashlib.sha256(b'test goal').hexdigest(),'requirements':[{'id':'R1','outcome':'test'}],'output_constraints':[]}
   store.event(m,'goal_requirements',result=req)
   reg=SimpleNamespace(mission_store=store,context={'mission_id':m})
   with patch.object(app,'review_model',side_effect=ContextCapacityError('too large')):
    result=app.audit_plan(reg)
   self.assertEqual(result['status'],'FAIL');self.assertEqual(result['coverage'],[])
   self.assertEqual(result['unreviewed_requirements'],['R1'])
   self.assertFalse(result['semantic_review_completed'])
   self.assertTrue(any('Report artifact collision' in x for x in result['issues']))
   self.assertFalse(app.coverage_state(store,m)['accepted'])
   self.assertEqual(app.ensure_plan_review(reg),result)

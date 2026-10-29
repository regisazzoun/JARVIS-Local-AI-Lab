"""Actual audit_plan and ContextBudget integration; controlled reviewer responses.

These are software regression cases, not an autonomy or reviewer-quality proof.
"""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
from jarvis import mission_assurance as application

path=Path(__file__).resolve().parents[3]/'tools/mission26_phase2/probes/coverage_budget_probe.py'
spec=importlib.util.spec_from_file_location('coverage_software_oracle',path)
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)

class AdaptiveCoverageTests(unittest.TestCase):
 def exercise(self,*args,**kwargs):return fixture.CoverageBudgetProbe().exercise(*args,**kwargs)
 def test_variable_sizes_fit_without_dropping_requirements(self):
  for width in [15000,18000]:
   with self.subTest(width=width):
    result,calls=self.exercise(2,width)
    self.assertEqual(result['status'],'PASS');self.assertEqual(calls,2)
 def test_recursive_split_preserves_global_metadata_in_every_payload(self):
  original=application.review_model;calls=[]
  def review(registry,purpose,instruction,data,schema,validator=None):
   self.assertIn('output_constraints',data['requirements'])
   self.assertIn('contract_version',data['requirements'])
   self.assertEqual(data['requirements']['version'],1)
   calls.append([row['id'] for row in data['requirements']['requirements']])
   return original(registry,purpose,instruction,data,schema,validator)
  with patch.object(application,'review_model',side_effect=review):
   result,admitted=self.exercise(7,9000)
  self.assertEqual(result['status'],'PASS');self.assertGreater(admitted,1)
  self.assertGreater(len(calls),admitted,'Oversized calls are rejected before backend review')
 def test_negative_result_survives_recursive_merge(self):
  result,_=self.exercise(2,18000,missing='R2')
  self.assertEqual(result['status'],'FAIL');self.assertTrue(any('R2' in text for text in result['issues']))
 def test_indivisible_requirement_remains_explicitly_blocked(self):
  from jarvis.mission_context_budget import ContextCapacityError
  with self.assertRaises(ContextCapacityError):self.exercise(1,60000)
 def test_unrelated_provider_failure_is_not_retried_as_a_size_problem(self):
  with patch.object(application,'review_model',side_effect=RuntimeError('provider unavailable')) as review:
   with self.assertRaisesRegex(RuntimeError,'provider unavailable'):self.exercise(3,100)
   self.assertEqual(review.call_count,1)

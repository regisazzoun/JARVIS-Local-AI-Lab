"""Codex regression oracle, not an autonomous reasoning or real-model benchmark.

Imports the actual candidate audit_plan/review_model; only backend review output
is deterministic. Actual ContextBudget rejects oversized inference payloads.
Run on a Dell with PYTHONPATH pointing at the candidate engine and this folder.
"""
import collections
import hashlib
import json
import tempfile
import unittest
from types import SimpleNamespace
from jarvis import mission_assurance as application
from jarvis.mission_store import MissionStore
from jarvis.mission_context_budget import ContextBudget,ContextCapacityError,serialized_bytes


class CoverageBudgetProbe(unittest.TestCase):
 def exercise(self,count,width,missing=None):
  with tempfile.TemporaryDirectory() as root:
   store=MissionStore(root);goal='Cover every requirement; preserve the entire plan and original objective.'
   mission=store.create(goal,'controlled-review-fixture','fixture')
   store.plan(mission,[{'id':'deliver','title':'Deliver the fixture results','depends':[],
        'tools':[],'artifacts':[],'contract':{'report_path':'/tmp/fixture-report.md'}}],author='Codex-test-fixture')
   plan=store.plans(mission)[-1]['plan']
   requirements={'contract_version':application.GOAL_VERSION,'version':1,
       'goal_sha256':hashlib.sha256(goal.encode()).hexdigest(),
       'requirements':[{'id':'R'+str(i+1),'outcome':str(i)+'x'*width} for i in range(count)],
       'output_constraints':[]}
   store.event(mission,'goal_requirements',result=requirements)
   expected={row['id'] for row in requirements['requirements']};observed=[];sizes=[]
   def backend(payload):
    # Exercise the actual guard before creating a deterministic backend reply.
    admitted=ContextBudget(store,mission).prepare(payload,{'limit':32768,'source':'Controlled software admission fixture'},4096)
    sizes.append(serialized_bytes(admitted));self.assertLessEqual(sizes[-1],27648)
    data=json.loads(admitted['messages'][-1]['content'])
    self.assertEqual(data['raw_goal'],goal)
    self.assertEqual(data['plan'],plan,'A batch must retain global plan contracts/dependencies')
    rows=data['requirements']['requirements'];ids=[row['id'] for row in rows]
    self.assertTrue(set(ids)<=expected);observed.extend(ids)
    return {'content':json.dumps({'coverage':{key:{'tasks':['deliver'],'covered':key!=missing,'reason':'Controlled fixture coverage'} for key in ids},'issues':[]})}
   registry=SimpleNamespace(mission_store=store,context={'mission_id':mission,'task_id':None},
          config={'hybrid_compute':{'mission_segment_tokens':4096}},assurance_transport=backend)
   result=application.audit_plan(registry)
   self.assertEqual(collections.Counter(observed),collections.Counter(expected),'Every requirement must be reviewed exactly once')
   self.assertEqual({row['requirement'] for row in result['coverage']},expected)
   self.assertTrue(sizes)
   return result,len(sizes)
 def test_small_review_remains_compatible(self):
  result,_=self.exercise(2,100);self.assertEqual(result['status'],'PASS')
 def test_five_long_requirements_split_under_real_admission(self):
  try:result,batches=self.exercise(5,7000)
  except ContextCapacityError as exc:self.fail('Reducible review escaped without bounded batches: '+str(exc))
  self.assertEqual(result['status'],'PASS');self.assertGreater(batches,1)
 def test_one_uncovered_requirement_cannot_become_global_pass(self):
  try:result,_=self.exercise(5,7000,missing='R3')
  except ContextCapacityError as exc:self.fail('Reducible review escaped before all requirements were reviewed: '+str(exc))
  self.assertEqual(result['status'],'FAIL')
  self.assertTrue(any('R3' in item for item in result['issues']))
 def test_indivisible_oversize_is_explicitly_blocked(self):
  with self.assertRaises(ContextCapacityError):self.exercise(1,60000)

if __name__=='__main__':unittest.main(verbosity=2)

import unittest
from jarvis.durable_cycle import model_observation
class ModelObservation(unittest.TestCase):
 def test_large_batch_keeps_both_ends_and_full_receipt_unchanged(self):
  body='IMPORTANT HEADER\n'+'x'*100000+'\nIMPORTANT FOOTER'
  original={'result':{'results':[{'result':{'stdout':body},'invocation_id':'real-id'}]}}
  view=model_observation(original)
  result=view['result']['results'][0]['result']
  self.assertTrue(result['stdout'].startswith('IMPORTANT HEADER'))
  self.assertTrue(result['stdout'].endswith('IMPORTANT FOOTER'))
  self.assertLess(len(result['stdout']),8200)
  self.assertEqual(result['stdout_full_chars'],len(body))
  self.assertEqual(original['result']['results'][0]['result']['stdout'],body)
  self.assertEqual(view['result']['results'][0]['invocation_id'],'real-id')

 def test_external_resume_requires_new_observation_without_rewriting_old_proof(self):
  import json
  from jarvis.durable_cycle import dependency_state
  old={'created':10,'id':'old','result':{'result':{'stdout':json.dumps({'external_dependency':{'id':'enrollment','resolved':False}})}}}
  self.assertEqual(len(dependency_state([old])),1)
  self.assertEqual(dependency_state([old],20),[])
  self.assertFalse(json.loads(old['result']['result']['stdout'])['external_dependency']['resolved'])
  new={**old,'created':21,'id':'new'}
  self.assertEqual(dependency_state([old,new],20)[0]['evidence_id'],'new')

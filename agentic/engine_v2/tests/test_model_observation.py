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

 def test_compaction_preserves_latest_batch_class_body_and_original_proof(self):
  from jarvis.durable_cycle import compact_observations
  from jarvis.mission_store import encoded
  text='class CrucialAdapter: required_signature = True\n'+'x'*14000+'\nassert integration'
  actual={'ok':True,'result':{'results':[{'result':{'stdout':text}},{'result':{'stdout':text}}]}}
  briefs=[{'id':'older','stdout':'z'*9000},{'id':'latest-real-invocation','stdout':''}]
  view=compact_observations(briefs,actual,12000)
  self.assertLessEqual(len(encoded(view)),12000)
  self.assertEqual(view[-1]['id'],'latest-real-invocation')
  for item in view[-1]['latest_tool_result']['result']['results']:
   self.assertIn('class CrucialAdapter',item['result']['stdout'])
   self.assertTrue(item['result']['stdout'].endswith('assert integration'))
  self.assertEqual(actual['result']['results'][0]['result']['stdout'],text)

 def test_native_tool_exchange_keeps_link_and_content_across_compaction(self):
  from jarvis.durable_cycle import native_tail
  from jarvis.mission_store import encoded
  import json
  messages=[{'role':'system','content':'old'},{'role':'assistant','tool_calls':[{'function':{'name':'mission_read_batch','arguments':{'calls':[]}}}]},{'role':'tool','tool_name':'mission_read_batch','content':json.dumps({'result':{'results':[{'result':{'stdout':'class ActualAdapter\n'+'x'*20000+'\nend'}}]}})}]
  tail=native_tail(messages,7000)
  self.assertEqual([x['role'] for x in tail],['assistant','tool'])
  self.assertEqual(tail[1]['tool_name'],'mission_read_batch');self.assertIn('ActualAdapter',tail[1]['content']);self.assertLessEqual(len(encoded(tail)),7000)
  self.assertGreater(len(messages[-1]['content']),20000)

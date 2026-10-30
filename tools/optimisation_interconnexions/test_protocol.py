import copy,importlib.util,json,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location('guard_protocol',Path(__file__).resolve().parents[1]/'qwen_webui/ollama_guard.py')
g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
class ProtocolTests(unittest.TestCase):
 def payload(self):
  return {'model':'fixture','messages':[{'role':'assistant','content':None,'tool_calls':[{'id':'a','function':{'name':'read_file','arguments':'{"path":"source.py"}'}},{'id':'b','function':{'name':'run_shell_command','arguments':'{"command":"python3 -m unittest"}'}}]},{'role':'tool','tool_call_id':'b','content':[{'type':'text','text':'3 tests PASS'}]},{'role':'tool','tool_call_id':'a','content':'source'}]}
 def test_parallel_results_resolve_by_id_not_position_without_mutating_history(self):
  original=self.payload();before=copy.deepcopy(original);native=g.native_payload(original)
  self.assertEqual(original,before);self.assertEqual([m['tool_name'] for m in native['messages'][1:]],['run_shell_command','read_file'])
  self.assertEqual(native['messages'][0]['tool_calls'][0]['function']['arguments'],{'path':'source.py'})
 def test_unmatched_or_conflicting_tool_result_refused(self):
  for change in ({'tool_call_id':'unknown'},{'tool_name':'another_tool'}):
   p=self.payload();p['messages'][1].update(change)
   with self.assertRaises(ValueError):g.native_payload(p)
 def test_images_not_silently_discarded(self):
  p=self.payload();p['messages'][1]['content']=[{'type':'image_url','image_url':{'url':'data:example'}}]
  with self.assertRaisesRegex(ValueError,'text content'):g.native_payload(p)
 def test_requested_output_limit_is_respected(self):
  for supplied,expected in [(128,128),(9000,4096)]:
   p=self.payload();p['max_tokens']=supplied;self.assertEqual(g.native_payload(p)['options']['num_predict'],expected)
 def test_truncation_not_announced_as_normal_completion(self):
  self.assertEqual(g.finish_reason({'done_reason':'length'},True),'length')
  self.assertEqual(g.finish_reason({'done_reason':'stop'},True),'tool_calls')
  self.assertEqual(g.finish_reason({'done_reason':'stop'},False),'stop')
if __name__=='__main__':unittest.main(verbosity=2)

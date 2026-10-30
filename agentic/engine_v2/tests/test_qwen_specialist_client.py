import io,json,unittest,urllib.error
from types import SimpleNamespace
from unittest.mock import patch
from jarvis.qwen_specialist import register
class Specialist(unittest.TestCase):
 def test_busy_conflict_is_known_not_executed(self):
  registry=SimpleNamespace(context={},specs={});register(registry)
  error=urllib.error.HTTPError('http://localhost/',409,'Conflict',{},io.BytesIO(json.dumps({'error':'Qwen Code busy; no duplicate dispatched'}).encode()))
  with patch('jarvis.qwen_specialist.Path.read_text',return_value='fixture'),patch('jarvis.qwen_specialist.urllib.request.urlopen',side_effect=error):
   result=registry.specs['qwen_code_run'][4]({'project':'fixture','task':'read'})
  self.assertEqual(result['execution_state'],'NOT_EXECUTED');self.assertEqual(result['returncode'],75);self.assertIn('qwen_code_status',result['retry_condition'])
 def test_specialist_cannot_recursively_delegate_itself(self):
  registry=SimpleNamespace(context={'client_origin':'QwenCode/MCP'},specs={});register(registry)
  with self.assertRaisesRegex(ValueError,'Recursive'):registry.specs['qwen_code_run'][4]({'project':'fixture','task':'recurse'})

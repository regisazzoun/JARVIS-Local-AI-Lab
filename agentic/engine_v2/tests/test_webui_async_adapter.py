import asyncio,importlib.util,time,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[3]
class AsyncTools(unittest.IsolatedAsyncioTestCase):
 async def test_slow_remote_tool_does_not_block_ui_loop(self):
  path=ROOT/'tools/qwen_webui/webui_capabilities.py'
  spec=importlib.util.spec_from_file_location('webui_async_test',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  api=module.Tools();finished=[]
  def slow(*args):time.sleep(.15);finished.append('tool');return 'real result fixture'
  async def conversation():await asyncio.sleep(.01);finished.append('conversation')
  with patch.object(api,'_request',side_effect=slow):
   result,_=await asyncio.gather(api.jarvis_call('host_resources','{}'),conversation())
  self.assertEqual(finished,['conversation','tool']);self.assertEqual(result,'real result fixture')

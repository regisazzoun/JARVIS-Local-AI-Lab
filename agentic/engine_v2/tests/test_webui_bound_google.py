import asyncio,importlib.util,json,unittest
from pathlib import Path
from unittest.mock import AsyncMock
class BoundGoogleWebUI(unittest.TestCase):
 def test_schema_and_list_omit_empty_optional_strings(self):
  path=Path(__file__).resolve().parents[3]/'tools/qwen_webui/webui_capabilities.py'
  spec=importlib.util.spec_from_file_location('bound_webui',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  for profile in ('personal','education'):
   tool=module.Tools();tool._call=AsyncMock(return_value='{}')
   asyncio.run(getattr(tool,'google_'+profile)(action='schema',name='docs.create'))
   payload=tool._call.call_args.args[1]
   self.assertEqual(payload['name'],'google_'+profile);self.assertNotIn('profile',payload['arguments']);self.assertNotIn('query',payload['arguments'])
   asyncio.run(getattr(tool,'google_'+profile)())
   self.assertNotIn('name',tool._call.call_args.args[1]['arguments'])
 def test_skill_transport_uses_active_manifest_and_preserves_scalars(self):
  path=Path(__file__).resolve().parents[3]/'tools/qwen_webui/webui_capabilities.py'
  spec=importlib.util.spec_from_file_location('bound_webui_skill',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  tool=module.Tools();tool._call=AsyncMock(side_effect=[json.dumps({'ok':True,'result':{'skills':[{'name':'fixture','version':1,'active_version':2,'parameters':{}},{'name':'fixture','version':2,'active_version':2,'parameters':{'properties':{'files':{'type':'string'},'count':{'type':'integer'}}}}]}}),'receipt'])
  result=asyncio.run(tool.jarvis_skill_run('fixture',{'files':['one.md'],'count':2}))
  self.assertEqual(result,'receipt');payload=tool._call.call_args.args[1];self.assertEqual(payload['name'],'skill_run')
  args=json.loads(payload['arguments']['parameters']);self.assertEqual(json.loads(args['files']),['one.md']);self.assertEqual(args['count'],2)

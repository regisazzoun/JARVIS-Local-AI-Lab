"""Focused connector/software contracts, not evidence of Google authorization."""
import asyncio,importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlparse,parse_qs
from jarvis import google_mcp as g
class Connector(unittest.TestCase):
 def test_two_profile_locations_are_distinct(self):
  self.assertNotEqual(g.profile_dir('personal'),g.profile_dir('education'))
  with self.assertRaises(ValueError):g.profile_dir('../personal')
 def test_linked_profile_is_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   (Path(tmp)/'personal').symlink_to('/tmp')
   with self.assertRaises(ValueError):g.profile_dir('personal',Path(tmp))
 def test_unapproved_send_and_invites_are_never_dispatched(self):
  for name in ('gmail.send','gmail.sendDraft','auth.clear','drive.trashFile'):
   with self.assertRaises(ValueError):g.validate_call(name,{},'personal')
  with self.assertRaises(ValueError):g.validate_call('calendar.createEvent',{'attendees':['someone']},'personal')
 def test_actual_download_path_and_symlink_escape_are_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/'downloads';root.mkdir();(root/'escape').symlink_to('/tmp')
   g.confined_download(root/'ok.txt',root)
   for path in (Path(tmp)/'outside',root/'escape'/'x'):
    with self.assertRaises(ValueError):g.confined_download(path,root)
 def test_missing_credentials_prevents_google_call(self):
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp)/'personal';folder.mkdir();(folder/'index.js').write_text('fixture')
   with patch.object(g,'credential_status',return_value={'configured':False,'state':'AUTH_REQUIRED'}),patch.object(g,'upstream',side_effect=AssertionError('must not dispatch')):
    result=g.perform('personal','call','drive.search',{},root=Path(tmp))
   self.assertFalse(result['operation_executed']);self.assertFalse(result['mcp_tool_dispatched'])
 def test_unknown_action_and_tool_are_rejected(self):
  with self.assertRaises(ValueError):g.perform('personal','unknown')
  with self.assertRaises(ValueError):g.validate_call('not.real',{},'personal')
 def test_catalog_pagination_preserves_count(self):
  async def upstream(*args):return {'server':{'name':'fixture'},'tools':[{'name':'docs.fixture'+str(i),'description':'x'} for i in range(13)]}
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp)/'personal';folder.mkdir();(folder/'index.js').write_text('fixture')
   with patch.object(g,'upstream',side_effect=upstream):
    first=g.perform('personal','list',root=Path(tmp));second=g.perform('personal','list',offset=6,root=Path(tmp))
   self.assertEqual(first['count'],15);self.assertEqual(first['next_offset'],6);self.assertEqual(second['next_offset'],12);self.assertEqual(len(first['tools']),6)
 def test_additive_sheet_write_rejects_path_injection_and_unknown_fields(self):
  from jsonschema import ValidationError
  g.validate_call('sheets.writeRange',{'spreadsheetId':'abc','range':'Feuille 1!A1','values':[[42]]},'personal')
  with self.assertRaises(ValidationError):g.validate_call('sheets.writeRange',{'spreadsheetId':'../escape','range':'A1','values':[[42]]},'personal')
  with self.assertRaises(ValidationError):g.validate_call('sheets.create',{'title':'fixture','url':'https://other.example'},'personal')
 def test_timeout_preserves_unknown_effect_instead_of_repeating_write(self):
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp)/'personal';folder.mkdir();(folder/'index.js').write_text('fixture')
   async def upstream(*args):raise TimeoutError('software fixture')
   with patch.object(g,'credential_status',return_value={'configured':True}),patch.object(g,'upstream',side_effect=upstream):
    result=g.perform('personal','call','sheets.create',{'title':'fixture'},root=Path(tmp))
   self.assertEqual(result['state'],'UNKNOWN');self.assertEqual(result['operation_executed'],'UNKNOWN');self.assertTrue(result['retry_requires_observation'])
 def test_mutation_classification_for_existing_mcp_gateway(self):
  self.assertFalse(g.is_mutating({'action':'status'}));self.assertFalse(g.is_mutating({'action':'call','name':'drive.search'}));self.assertTrue(g.is_mutating({'action':'call','name':'docs.create'}))
  self.assertTrue(g.is_mutating({'action':'call','name':'drive.downloadFile'}))
 def test_upstream_json_error_is_not_a_successful_write(self):
  async def upstream(*args):return {'mcp_is_error':False,'content':[{'error':'Software fixture rejection'}]}
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp)/'personal';folder.mkdir();(folder/'index.js').write_text('fixture')
   with patch.object(g,'credential_status',return_value={'configured':True}),patch.object(g,'upstream',side_effect=upstream):
    result=g.perform('personal','call','docs.create',{'title':'fixture'},root=Path(tmp))
   self.assertEqual(result['returncode'],1);self.assertEqual(result['operation_executed'],'UNKNOWN');self.assertFalse(result['remote_access_verified'])
 def test_google_write_is_deferred_by_existing_controller_before_any_effect(self):
  from unittest.mock import Mock
  from jarvis.core import Core,ROOT
  from jarvis.memory import Memory
  from jarvis.missions import Missions
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);config=json.loads((ROOT/'config/example.json').read_text());config['voice_summary']=False
   response={'role':'assistant','content':'','tool_calls':[{'function':{'name':'google_mcp','arguments':{'profile':'personal','action':'call','name':'docs.create','arguments':{'title':'fixture'}}}}]}
   core=Core(config,Memory(root/'runtime/memory.sqlite'),lambda payload:response);missions=Missions(core,root,start_worker=False,start_publisher=False)
   forbidden=Mock(side_effect=AssertionError('Must be deferred'));old=core.tools.specs['google_mcp'];core.tools.specs['google_mcp']=(*old[:4],forbidden)
   result=core.chat('Create the authorized test document',config['default_model'])
   self.assertTrue(result['mission_id']);forbidden.assert_not_called()
class OAuthCallback(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  path=Path(__file__).resolve().parents[3]/'tools/google_mcp/connect.py';spec=importlib.util.spec_from_file_location('google_connect_test',path);cls.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.module)
 def test_publisher_url_does_not_require_owner_cloud_client(self):
  url=self.module.auth_url({'clientId':'publisher.apps.googleusercontent.com','cloudFunctionUrl':'https://publisher.example','scopes':['scope']},'csrf',8769)
  query=parse_qs(urlparse(url).query);self.assertEqual(query['client_id'],['publisher.apps.googleusercontent.com']);self.assertEqual(query['redirect_uri'],['https://publisher.example'])
 def test_callback_rejects_wrong_state_or_partial_credentials(self):
  with self.assertRaises(PermissionError):self.module.validate_callback({'state':['wrong']},'expected')
  with self.assertRaises(ValueError):self.module.validate_callback({'state':['expected'],'access_token':['software-fixture-only']},'expected')
 def test_callback_keeps_only_credential_fields(self):
  query={k:[v] for k,v in {'state':'expected','access_token':'software-fixture-only','refresh_token':'software-fixture-only','expiry_date':'42','extra':'not copied'}.items()}
  result=self.module.validate_callback(query,'expected');self.assertNotIn('extra',result);self.assertNotIn('state',result)

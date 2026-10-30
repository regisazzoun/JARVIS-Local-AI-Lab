import tempfile,unittest
from pathlib import Path
from unittest.mock import patch,Mock
from jarvis.google_workspace import perform,profile_path
class GoogleConnector(unittest.TestCase):
 def test_missing_auth_is_not_success(self):
  with tempfile.TemporaryDirectory() as tmp:
   result=perform('personal','drive_search',{'query':'trashed = false'},Path(tmp))
  self.assertFalse(result['ok']);self.assertFalse(result['operation_executed']);self.assertEqual(result['state'],'AUTH_REQUIRED')
 def test_profile_cannot_escape_private_root(self):
  with self.assertRaises(ValueError):profile_path('../other')
 def test_gmail_send_not_exposed(self):
  with self.assertRaises(ValueError):perform('personal','gmail_send',{})
 def test_calendar_rejects_invites_before_http_request(self):
  client=Mock()
  with patch('jarvis.google_workspace.session',return_value=client):
   with self.assertRaises(ValueError):perform('personal','calendar_create',{'event':{'summary':'test','attendees':[{'email':'nobody@example.com'}]}})
  client.request.assert_not_called()
 def test_sheets_write_uses_correct_range_and_raw_values(self):
  client=Mock();client.request.return_value.status_code=200;client.request.return_value.json.return_value={'updatedCells':1}
  with patch('jarvis.google_workspace.session',return_value=client):
   result=perform('education','sheets_write',{'id':'abc','range':"Feuille 1!A1",'values':[[42]]})
  args,kwargs=client.request.call_args
  self.assertEqual(args[0],'PUT');self.assertIn('Feuille%201%21A1',args[1]);self.assertEqual(kwargs['params']['valueInputOption'],'RAW');self.assertTrue(result['ok']);self.assertFalse(result['application_result_independently_verified'])

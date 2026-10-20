import unittest
from unittest.mock import patch
from email.message import Message
from jarvis.agent import fetch
class Response:
 def __init__(self):self.headers=Message();self.headers['Content-Type']='text/plain'
 def __enter__(self):return self
 def __exit__(self,*a):pass
 def read(self,n):return ('x'*9000+'IMPORTANT API TAIL').encode()[:n]
class Opener:
 def open(self,*a,**kw):return Response()
class DocumentationTest(unittest.TestCase):
 def test_truncated_document_can_be_continued_and_untrusted_redirect_policy_remains(self):
  with patch('jarvis.agent.urllib.request.build_opener',return_value=Opener()):
   first=fetch('https://docs.livekit.io/reference/python/');self.assertEqual(first['next_offset'],9000)
   second=fetch('https://docs.livekit.io/reference/python/',9000);self.assertEqual(second['content'],'IMPORTANT API TAIL');self.assertIsNone(second['next_offset'])
  with self.assertRaises(ValueError):fetch('http://127.0.0.1/')

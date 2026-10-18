import hashlib,json,tempfile,unittest
from pathlib import Path
from jarvis.auth import Auth

class SessionPersistenceTest(unittest.TestCase):
    def test_restart_and_logout(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);salt=b'test-only-salt'
            credentials={'username':'tester','salt':salt.hex(),'hash':hashlib.pbkdf2_hmac('sha256',b'test-password',salt,300000).hex()}
            (root/'auth.json').write_text(json.dumps(credentials))
            first=Auth(root/'auth.json',session_db=root/'memory.sqlite')
            token=first.login('tester','test-password');headers={'Cookie':'jarvis_session='+token}
            second=Auth(root/'auth.json',session_db=root/'memory.sqlite')
            self.assertTrue(second.valid(headers))
            self.assertFalse(second.valid({'Cookie':'jarvis_session=forged'}))
            self.assertNotIn(token,(root/'memory.sqlite').read_bytes().decode(errors='ignore'))
            second.logout(headers)
            self.assertFalse(Auth(root/'auth.json',session_db=root/'memory.sqlite').valid(headers))

if __name__=='__main__':unittest.main()

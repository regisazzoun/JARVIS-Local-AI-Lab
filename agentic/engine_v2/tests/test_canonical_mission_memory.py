import tempfile,unittest
from pathlib import Path
from jarvis.memory import Memory
from jarvis.publication import redact_public

class CanonicalMissionMemoryTest(unittest.TestCase):
    def test_mission_messages_survive_and_are_not_duplicated(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'memory.sqlite';memory=Memory(path);conv=memory.conversation('test')
            first=memory.mission_message('m','goal',conv,'user','Objectif de test','local')
            reopened=Memory(path)
            self.assertEqual(first,reopened.mission_message('m','goal',conv,'user','Objectif de test','local'))
            self.assertEqual(len(reopened.history(conv)),1)
            self.assertEqual(reopened.history(conv)[0]['content'],'Objectif de test')
    def test_redaction_preserves_proof_references(self):
        value='192.168.1.2 100.70.2.3 127.0.0.1 aa:bb:cc:dd:ee:ff 11111111-2222-3333-4444-555555555555 1234567890abcdef1234567890abcdef'
        clean=redact_public(value)
        for private in ('192.168.1.2','100.70.2.3','aa:bb:cc:dd:ee:ff','11111111-2222-3333-4444-555555555555'):self.assertNotIn(private,clean)
        self.assertIn('127.0.0.1',clean);self.assertIn('1234567890abcdef1234567890abcdef',clean)

if __name__=='__main__':unittest.main()

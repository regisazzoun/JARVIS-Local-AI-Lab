import unittest
from jarvis.protocol import normalize_message

class SharedProtocolTest(unittest.TestCase):
    def test_ministral_whole_message_preserves_native_authorization_path(self):
        message=normalize_message('host_read_file[ARGS]{"path":"/allowed/report.md"}',{'host_read_file'})
        self.assertEqual(message['tool_calls'][0]['function'],{'name':'host_read_file','arguments':{'path':'/allowed/report.md'}})
    def test_quoted_or_unknown_text_does_not_execute(self):
        for text in ('Exemple : host_exec[ARGS]{"command":"false"}','unknown_tool[ARGS]{}','host_read_file[ARGS]{bad}'):
            self.assertFalse(normalize_message(text,{'host_read_file','host_exec'}).get('tool_calls'))
    def test_native_message_is_not_rewritten(self):
        message={'role':'assistant','tool_calls':[{'function':{'name':'host_read_file','arguments':{}}}]}
        self.assertIs(normalize_message(message,{'host_read_file'}),message)

if __name__=='__main__':unittest.main()

"""Exercise the actual request handlers without binding a network socket."""
import contextlib
import email.message
import importlib.util
import io
import pathlib
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('receiver', pathlib.Path(__file__).with_name('receive.py'))
receiver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receiver)

class ReceiverTest(unittest.TestCase):
    def test_auth_lengths_storage_and_display_without_network(self):
        data = b'JARVIS DISCOVERY V1 - READ ONLY\nfixture\nJARVIS DISCOVERY END\n'
        key = 'temporary-test-key'
        cases = [
            ('GET', '192.0.2.2', f'/{key}/discover.sh', b'', 0, 403),
            ('GET', '192.0.2.1', '/wrong/discover.sh', b'', 0, 403),
            ('GET', '192.0.2.1', f'/{key}/discover.sh', b'', 0, 200),
            ('POST', '192.0.2.1', '/wrong/report', data, len(data), 403),
            ('POST', '192.0.2.1', f'/{key}/report', data, 2000000, 413),
            ('POST', '192.0.2.1', f'/{key}/report', data[:-10], len(data), 400),
            ('POST', '192.0.2.1', f'/{key}/report', data, len(data), 201),
        ]
        test = self
        class FakeServer:
            def __init__(self, address, handler): self.handler = handler
            def handle_request(self):
                method, ip, path, body, length, code = cases.pop(0)
                h = object.__new__(self.handler)
                h.client_address = (ip, 12345)
                h.path = path
                h.headers = email.message.Message()
                h.headers['Content-Length'] = str(length)
                h.rfile = io.BytesIO(body)
                answers = []
                h.reply = lambda status, payload: answers.append((status, payload))
                getattr(h, 'do_' + method)()
                test.assertEqual(answers[0][0], code)
            def server_close(self): pass
        with tempfile.TemporaryDirectory() as temp:
            output = pathlib.Path(temp)/'report.txt'
            console = io.StringIO()
            with patch.object(receiver.http.server, 'HTTPServer', FakeServer), contextlib.redirect_stdout(console):
                self.assertTrue(receiver.run('127.0.0.1', 0, '192.0.2.1', key, b'#!/bin/sh\n', output))
            self.assertFalse(cases)
            self.assertEqual(output.read_bytes(), data)
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            self.assertIn('REPORT_RECEIVED', console.getvalue())
            self.assertIn('fixture', console.getvalue())

if __name__ == '__main__': unittest.main()

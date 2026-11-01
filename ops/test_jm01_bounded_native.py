import copy
import json
from pathlib import Path
import tempfile
import unittest

import jm01_bounded_native as m


class BoundedNativeTests(unittest.TestCase):
    def test_failure_totals_and_old_session_survive_verified_resolution(self):
        for failures in (3, 9):
            state = {'failures': {'unit': failures}, 'sessions': {'unit': 'old'},
                     'completed': {'prior': {'commit': 'retained'}}}
            r = {'verified': True, 'id': 'fix', 'unit': 'unit',
                 'failed_through': failures, 'native_session_id': 'new'}
            m.apply_resolution(state, r)
            self.assertEqual(state['failures']['unit'], failures)
            self.assertEqual(state['resolved_through']['unit'], failures)
            self.assertEqual(state['session_archive']['unit'], ['old'])
            self.assertEqual(state['completed']['prior']['commit'], 'retained')
            before = copy.deepcopy(state)
            m.apply_resolution(state, r)
            self.assertEqual(state, before)

    def test_mismatched_resolution_cannot_open_segment(self):
        s = {'failures': {'unit': 9}, 'sessions': {'unit': 'old'}}
        old = copy.deepcopy(s)
        with self.assertRaises(ValueError):
            m.apply_resolution(s, {'verified': True, 'id': 'bad', 'unit': 'unit',
                                  'failed_through': 3, 'native_session_id': 'new'})
        self.assertEqual(s, old)

    def test_native_success_without_structured_files_is_not_success(self):
        for final in ({'type': 'result', 'subtype': 'success', 'result': '<tool_call>'},
                      {'type': 'result', 'is_error': True, 'structured_result': {'files': {}}}):
            with self.assertRaises(ValueError):
                m.parse_result(json.dumps(final))

    def test_parse_native_structured_result(self):
        result, usage = m.parse_result('warning\n' + json.dumps({
            'type': 'result', 'structured_result': {'files': {'a.md': 'text'}},
            'usage': {'input_tokens': 604}}))
        self.assertEqual(result['files']['a.md'], 'text')
        self.assertEqual(usage['input_tokens'], 604)

    def test_reject_extra_missing_and_empty_artifacts(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t)
            for files in ({}, {'a.md': 'x' * 300, '../outside.md': 'x' * 300}, {'a.md': ''}):
                with self.assertRaises(ValueError):
                    m.validate_files({'files': files}, ['a.md'], p)
            self.assertEqual(list(p.iterdir()), [])

    def test_reject_symlink_escape(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            project = Path(a)
            (project / 'escape').symlink_to(Path(b), target_is_directory=True)
            with self.assertRaises(ValueError):
                m.validate_files({'files': {'escape/a.md': 'x' * 300}}, ['escape/a.md'], project)
            self.assertEqual(list(Path(b).iterdir()), [])

    def test_valid_exact_files(self):
        with tempfile.TemporaryDirectory() as t:
            files = {'docs/a.md': 'a' * 300, 'tools/a.mjs': 'b' * 150}
            self.assertEqual(m.validate_files({'files': files}, list(files), Path(t)), files)


if __name__ == '__main__':
    unittest.main()

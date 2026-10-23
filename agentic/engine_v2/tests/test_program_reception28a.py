import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('program_reception28a',Path(__file__).resolve().parents[3]/'operations/mission28a/verify_consolidation.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)


class ProgramReception(unittest.TestCase):
    def data(self,name,passed):
        return {'cases':[{'model':name,'case':'fixture','evaluation':{'pass':passed}}],'summary':{name:{'passed':999,'total':999}}}
    def test_source_evaluations_override_stale_declared_summaries(self):
        a,b=self.data('a',True),self.data('b',False)
        self.assertEqual(checker.expected_scores(a,b)['scores'],{'a':{'passed':1,'total':1},'b':{'passed':0,'total':1}})
        variants=checker.variants(a,b)
        self.assertEqual(len(variants),4)
        self.assertNotEqual(checker.expected_scores(*variants[0][1:]),checker.expected_scores(*variants[1][1:]))
        self.assertEqual(a['summary']['a']['passed'],999)
    def test_exit_success_and_valid_digest_do_not_accept_hardcoded_scores(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);out=root/'out.json';manifest=root/'manifest.json'
            a,b=self.data('a',True),self.data('b',False)
            baseline=checker.expected_scores(a,b);out.write_text(json.dumps(baseline))
            manifest.write_text(json.dumps({'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
            self.assertTrue(checker.grade(out,manifest,baseline)['pass'])
            changed=checker.variants(a,b)[1]
            result=checker.grade(out,manifest,checker.expected_scores(*changed[1:]))
            self.assertFalse(result['pass']);self.assertTrue(result['manifest_matches'])
    def test_manifest_must_match_exact_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);out=root/'out.json';manifest=root/'manifest.json';expected=checker.expected_scores(self.data('a',True),self.data('b',False))
            out.write_text(json.dumps(expected));manifest.write_text('{"sha256":"wrong"}')
            self.assertFalse(checker.grade(out,manifest,expected)['pass'])

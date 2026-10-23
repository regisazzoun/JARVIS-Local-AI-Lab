import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('quality28a',Path(__file__).resolve().parents[3]/'operations/mission28a/quality_compare.py')
quality=importlib.util.module_from_spec(spec);spec.loader.exec_module(quality)


class QualityJudge(unittest.TestCase):
    def test_valid_type_checks_are_executable_and_wrong_behavior_fails(self):
        valid='def normalize(value):\n    if isinstance(value, (bool,str,float)): raise ValueError()\n    if isinstance(value,int): return value if 1 <= value <= 65535 else 8091\n    raise ValueError()'
        self.assertTrue(quality.evaluate('code',json.dumps({'code':valid}))['pass'])
        self.assertFalse(quality.evaluate('code',json.dumps({'code':'def normalize(value): return 8091'}))['pass'])

    def test_recheck_keeps_original_and_prior_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'original.json';output=Path(tmp)/'corrected.json'
            source.write_text(json.dumps({'cases':[{'model':'fixture','case':'diagnosis','error':None,'text':'{}','evaluation':{'pass':False,'reason':'original'}}]}))
            before=source.read_bytes();quality.recheck(source,output);after=json.loads(output.read_text())
            self.assertEqual(source.read_bytes(),before)
            self.assertEqual(after['cases'][0]['previous_evaluations'][0]['reason'],'original')
            self.assertEqual(after['recheck']['source_sha256'],hashlib.sha256(before).hexdigest())
            self.assertFalse(after['recheck']['new_inference'])
            with self.assertRaises(FileExistsError):quality.recheck(source,output)
            with self.assertRaises(ValueError):quality.recheck(source,source)

"""Codex regression oracles for the real JARVIS candidate, not autonomy proof."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

# Standalone and dotted unittest entrypoints resolve the same real engine.
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from jarvis.attest import AttestRuntime,get_object_code_hash,attestation_report


class RuntimeAttestationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.path=self.root/'target.py'
        self.name='attestation_subject_'+str(id(self))
        self.addCleanup(sys.modules.pop,self.name,None)

    def load(self,text):
        self.path.write_text(text)
        mod=types.ModuleType(self.name);mod.__file__=str(self.path)
        sys.modules[self.name]=mod
        exec(compile(text,str(self.path),'exec',dont_inherit=True),mod.__dict__)
        return mod

    def measured(self):
        a=AttestRuntime(self.root);self.assertTrue(a.measure_module(self.name));return a

    def test_unchanged_real_function_matches(self):
        self.load('def f():\n    return 1\n')
        self.assertEqual(self.measured().verify_against_candidate(self.root)[self.name]['status'],'match')

    def test_changed_disk_before_measurement_does_not_hide_old_loaded_code(self):
        # Exact false-positive scenario reproduced against JARVIS's original.
        mod=self.load('def f():\n    return 1\n')
        self.path.write_text('def f():\n    return 2\n')
        result=self.measured().verify_against_candidate(self.root)[self.name]
        self.assertEqual(mod.f(),1);self.assertEqual(result['status'],'mismatch')
        self.assertFalse(result['objects_match'])

    def test_changed_disk_after_measurement_is_detected(self):
        self.load('def f():\n    return 1\n');a=self.measured()
        self.path.write_text('def f():\n    return 2\n')
        self.assertEqual(a.verify_against_candidate(self.root)[self.name]['status'],'mismatch')

    def test_live_monkey_patch_after_measurement_is_detected(self):
        mod=self.load('def f():\n    return 1\n');a=self.measured()
        mod.f.__code__=compile('def f():\n    return 3\n',str(self.path),'exec').co_consts[0]
        self.assertEqual(a.verify_against_candidate(self.root)[self.name]['status'],'mismatch')

    def test_nested_code_constant_changes_are_detected(self):
        self.load('def f():\n    def inner():\n        return 1\n    return inner()\n')
        self.path.write_text('def f():\n    def inner():\n        return 2\n    return inner()\n')
        self.assertEqual(self.measured().verify_against_candidate(self.root)[self.name]['status'],'mismatch')

    def test_class_instance_static_and_class_methods(self):
        self.load('class C:\n    def f(self): return 1\n    @staticmethod\n    def s(): return 2\n    @classmethod\n    def c(cls): return 3\n')
        result=self.measured().verify_against_candidate(self.root)[self.name]
        self.assertEqual(result['status'],'match',result)
        self.assertEqual(set(result['actual_objects']),{'C.f','C.s','C.c'})

    def test_candidate_is_compiled_without_execution_and_path_is_ignored(self):
        self.load('def f():\n    return 1\n')
        candidate=self.root/'other';candidate.mkdir()
        marker=self.root/'must-not-exist'
        (candidate/'target.py').write_text('open('+repr(str(marker))+',"w").write("MUST NOT EXECUTE")\n\ndef f():\n    return 1\n')
        self.assertEqual(self.measured().verify_against_candidate(candidate)[self.name]['status'],'match')
        self.assertFalse(marker.exists())

    def test_missing_candidate_and_syntax_error_are_not_match(self):
        self.load('def f(): return 1\n');a=self.measured()
        self.path.unlink();self.assertEqual(a.verify_against_candidate(self.root)[self.name]['status'],'missing')
        self.path.write_text('def broken(')
        self.assertEqual(a.verify_against_candidate(self.root)[self.name]['status'],'insufficient')

    def test_expired_and_future_measurements_are_insufficient(self):
        self.load('def f(): return 1\n');a=self.measured()
        for offset in [-60,60]:
            a._measurements[self.name]['observed_at']=__import__('time').time()+offset
            self.assertEqual(a.verify_against_candidate(self.root)[self.name]['status'],'insufficient')

    def test_unavailable_or_empty_observation_never_matches(self):
        a=AttestRuntime(self.root);self.assertFalse(a.measure_module('module_that_is_not_loaded'))
        self.assertEqual(a.verify_against_candidate(self.root)['__attestation__']['status'],'insufficient')
        self.load('x=1\n');self.assertEqual(self.measured().verify_against_candidate(self.root)[self.name]['status'],'insufficient')
        with self.assertRaises(TypeError):get_object_code_hash(len)

    def test_hash_does_not_read_source_or_file(self):
        self.load('def f(): return 1\n');f=sys.modules[self.name].f
        with patch('inspect.getsource',side_effect=AssertionError('must not read disk')):
            self.assertEqual(get_object_code_hash(f),get_object_code_hash(f.__code__))

    def test_actual_engine_methods_match_their_explicit_source_candidate(self):
        import jarvis.worker,jarvis.core
        root=Path(jarvis.worker.__file__).parent
        a=AttestRuntime(root)
        a.measure_module('jarvis.worker',symbols=['run','main'])
        a.measure_module('jarvis.core',symbols=['Core.ollama','Core.chat'])
        results=a.verify_against_candidate(root)
        self.assertEqual(results['jarvis.worker']['status'],'match',results['jarvis.worker'])
        self.assertEqual(results['jarvis.core']['status'],'match',results['jarvis.core'])

    def test_selection_is_explicit_and_unknown_symbol_cannot_pass(self):
        self.load('def f(): return 1\n');a=AttestRuntime(self.root)
        a.measure_module(self.name,symbols=['missing'])
        self.assertEqual(a.verify_against_candidate(self.root)[self.name]['status'],'insufficient')
        a.measure_module(self.name,symbols=['f'])
        result=a.verify_against_candidate(self.root)[self.name]
        self.assertEqual(result['status'],'match');self.assertEqual(result['selected_symbols'],['f'])

    def test_decorated_whole_worker_is_insufficient_not_false_mismatch(self):
        import jarvis.worker
        a=AttestRuntime(Path(jarvis.worker.__file__).parent)
        a.measure_module('jarvis.worker')
        self.assertEqual(a.verify_against_candidate(Path(jarvis.worker.__file__).parent)['jarvis.worker']['status'],'insufficient')

    def test_unavailable_module_prevents_overall_pass(self):
        self.load('def f(): return 1\n')
        r=attestation_report([self.name,'absent_observation'],self.root)
        self.assertEqual(r['verification_status'],'PARTIAL')
        self.path.write_text('def f(): return 2\n')
        r=attestation_report([self.name,'absent_observation'],self.root)
        self.assertEqual(r['verification_status'],'FAIL')


if __name__ == "__main__":
    unittest.main(verbosity=2)

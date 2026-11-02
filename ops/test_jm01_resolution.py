import copy
import importlib.util
from pathlib import Path
import unittest
s=importlib.util.spec_from_file_location('jm01_units',Path(__file__).with_name('jm01_units.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class ResolutionTests(unittest.TestCase):
    def test_verified_change_keeps_failures_and_archives_context(self):
        state={'failures':{'01-audit':3},'sessions':{'01-audit':'old'},'completed':{}}
        r={'id':'context-fix','verified':True,'unit':'01-audit','failed_through':3,'native_session_id':'new'}
        m.apply_resolution(state,r)
        self.assertEqual(state['failures']['01-audit'],3)
        self.assertEqual(state['resolved_through']['01-audit'],3)
        self.assertEqual(state['session_archive']['01-audit'],['old'])
        self.assertEqual(state['sessions']['01-audit'],'new')
        before=copy.deepcopy(state);m.apply_resolution(state,r);self.assertEqual(state,before)
    def test_unverified_or_mismatched_resolution_cannot_open_segment(self):
        state={'failures':{'01-audit':3},'sessions':{'01-audit':'old'},'completed':{}}
        before=copy.deepcopy(state)
        m.apply_resolution(state,{'verified':False});self.assertEqual(state,before)
        with self.assertRaises(ValueError):m.apply_resolution(state,{'id':'bad','verified':True,'unit':'01-audit','failed_through':2,'native_session_id':'new'})
        self.assertEqual(state,before)
if __name__=='__main__':unittest.main()

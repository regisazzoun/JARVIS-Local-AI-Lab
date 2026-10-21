import json
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from jarvis.skill_lab import SkillLab

class Registry:
    def __init__(self,root):
        self.root=Path(root);self.context={};self.calls=[];self.value='bad';self.writes=0
        self.specs={'host_write_file':('',{'path':{'type':'string'},'content':{'type':'string'}},['path','content'],'host_authorized',None),'host_read_file':('',{'path':{'type':'string'}},['path'],'host_authorized',None)}
    def execute(self,name,args):
        self.calls.append((name,args))
        if name=='host_write_file':self.writes+=1
        return {'ok':True,'tool':name,'result':{'stdout':self.value,'evidence_id':str(len(self.calls))}}

def manifest():
    return {'name':'sample','description':'sample check','when':'file needed','parameters':{'type':'object','properties':{'path':{'type':'string'}},'required':['path'],'additionalProperties':False},'requires_tools':['host_write_file','host_read_file'],'prerequisites':['writable test directory'],'steps':[{'tool':'host_write_file','arguments':{'path':'${path}','content':'test'}},{'tool':'host_read_file','arguments':{'path':'${path}'},'verify':True,'checks':[{'path':'result.stdout','op':'equals','value':'good'}]}],'on_error':'Observe, correct, resume checkpoint','changelog':'initial'}

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.r=Registry(self.tmp.name);self.lab=SkillLab(self.r);self.m=manifest();self.lab.define(self.m)
    def test_failed_verifier_cannot_activate_and_resume_rechecks(self):
        failed=self.lab.execute('sample',{'path':'/test'},True)
        self.assertEqual(failed['state'],'failed')
        with self.assertRaises(ValueError):self.lab.activate('sample',True)
        self.r.value='good';passed=self.lab.execute('sample',{'path':'/test'},True,failed['run_id'])
        self.assertEqual(passed['state'],'passed');self.assertEqual(self.r.writes,1)
        self.lab.activate('sample',True);self.lab.execute('sample',{'path':'/test'})
        self.assertEqual(self.r.writes,2)
        self.r.value='bad';again=self.lab.execute('sample',{'path':'/test'},True,failed['run_id'])
        self.assertEqual(again['state'],'failed')
    def test_revision_cannot_reuse_old_test_and_disable_persists(self):
        self.r.value='good';self.lab.execute('sample',{'path':'/test'},True);self.lab.activate('sample',True)
        m=manifest();m['changelog']='fix';self.assertEqual(self.lab.define(m)['version'],2)
        with self.assertRaises(ValueError):self.lab.activate('sample',True)
        self.assertEqual(self.lab.execute('sample',{'path':'/test'})['version'],1)
        self.lab.activate('sample',False)
        with self.assertRaises(ValueError):SkillLab(self.r).execute('sample',{'path':'/test'})
    def test_all_arguments_validated_before_first_effect(self):
        m=manifest();m['steps'][1]['arguments']['unknown']='x';self.lab.define(m)
        with self.assertRaises(Exception):self.lab.execute('sample',{'path':'/test'},True)
        self.assertEqual(self.r.calls,[])
    def test_params_typed_and_no_interpolation_or_recursion(self):
        with self.assertRaises(Exception):self.lab.execute('sample',{'path':42},True)
        m=manifest();m['steps'][0]['arguments']['path']='/tmp/${path}';self.lab.define(m)
        with self.assertRaises(ValueError):self.lab.execute('sample',{'path':'x'},True)
        self.assertEqual(self.r.calls,[])
        m=manifest();m['steps'][0]['tool']='skill_run'
        with self.assertRaises(ValueError):self.lab.define(m)
    def test_unchanged_definition_idempotent(self):
        self.assertTrue(self.lab.define(self.m)['unchanged']);self.assertEqual(len(self.lab.listing({})['skills']),1)

if __name__=='__main__':unittest.main()

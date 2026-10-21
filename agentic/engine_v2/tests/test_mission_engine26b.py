import copy
import json
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from jarvis.mission_store import MissionStore
from jarvis.mission_assurance import requirements, audit_plan, coverage_state, audit_report, evidence_snapshot, deterministic_report_issues, require_report
from test_mission_engine26 import task, contract

class AssuranceTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        self.s=MissionStore(tmp.name)
        self.m=self.s.create('Produce a file and a report','model','conversation',spec={'autonomous':True,'assurance':True})
        self.meta=dict(objective='goal',success_criteria=['file and report'],artifacts=['file'],stop_conditions=['external dependency'])
        self.responses=[]
        self.r=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'a'})
        self.r.assurance_transport=lambda payload:{'tool_calls':[{'function':{'name':'submit_review','arguments':self.responses.pop(0)}}]}
    def extraction(self):
        return {'requirements':[{'id':'R1','quote':'a file','outcome':'file'},{'id':'R2','quote':'a report','outcome':'report'}]}
    def coverage(self,complete=True):
        return {'coverage':[{'requirement':'R1','tasks':['a'],'covered':True,'reason':'exact state'}, {'requirement':'R2','tasks':['a'] if complete else [],'covered':complete,'reason':'report missing' if not complete else 'explicit final report'}],'issues':[]}
    def test_omission_blocks_effects_and_revision_survives_restart(self):
        self.responses=[self.extraction(),self.coverage(False),self.coverage(True)]
        requirements(self.r);self.s.plan(self.m,[task()],author='JARVIS',metadata=self.meta)
        self.assertEqual(audit_plan(self.r)['status'],'FAIL');self.assertEqual(self.s.ready(self.m),[])
        self.s.plan(self.m,[task('b')],author='JARVIS',expected_version=1,append=True,reason='cover omission')
        self.assertFalse(coverage_state(self.s,self.m)['accepted'])
        self.assertEqual(audit_plan(self.r)['status'],'PASS')
        reopened=MissionStore(self.s.root)
        self.assertTrue(coverage_state(reopened,self.m)['accepted']);self.assertEqual(len(reopened.plans(self.m)),2)
    def test_forged_extraction_and_incomplete_review_fail_closed(self):
        bad=self.extraction();bad['requirements'][0]['quote']='invented'
        self.responses=[bad]
        with self.assertRaises(ValueError):requirements(self.r)
        self.responses=[self.extraction(),{'coverage':[],'issues':[]}]
        self.s.plan(self.m,[task()],metadata=self.meta)
        self.assertEqual(audit_plan(self.r)['status'],'FAIL');self.assertFalse(self.s.ready(self.m))
    def test_unknown_task_review_and_unreviewed_revision_block(self):
        a=self.coverage();a['coverage'][0]['tasks']=['not-real']
        self.responses=[self.extraction(),a,copy.deepcopy(a)];self.s.plan(self.m,[task()],metadata=self.meta)
        with self.assertRaises(ValueError):audit_plan(self.r)
        self.assertEqual(self.s.ready(self.m),[])
    def observation(self,ok=True):
        token=self.s.begin_call(self.m,'a','host_read_file',{'path':'/a'})
        self.s.finish_call(token,{'ok':ok,'result':{'stdout':'{"port":8091}','returncode':0 if ok else 1}},0)
        return token
    def test_wrong_counts_hidden_failures_and_originals_retained(self):
        ref=self.observation();self.s.event(self.m,'semantic_verification','a',result={'status':'FAIL','contract':contract(),'observations':[]})
        self.responses=[{'claims':[{'quote':'observations : 999','verdict':'contradicted','references':[ref],'reason':'only one read'}],'issues':[]}]
        body='observations : 999. '+ref
        result=audit_report(self.r,body,'a');self.assertEqual(result['status'],'FAIL')
        self.assertTrue(any('FAIL' in x for x in result['issues']))
        self.assertEqual(result['draft'],body)
        self.assertEqual(len([x for x in self.s.events(self.m) if x['kind']=='narrative_review']),1)
    def test_corrected_explanation_retained_and_unknown_refs_rejected(self):
        ref=self.observation()
        self.responses=[{'claims':[{'quote':'Lecture observée','verdict':'supported','references':[ref],'reason':'original read'}],'issues':[]}]
        body='Lecture observée : '+ref+'. La portée reste limitée au contenu relu.'
        result=require_report(self.r,body,'a');self.assertEqual(result['status'],'PASS')
        # Same receipt snapshot, no inference replay. A new observation invalidates approval.
        self.assertEqual(require_report(self.r,body,'a')['fingerprint'],result['fingerprint'])
        self.observation();self.responses=[{'claims':[{'quote':'Lecture observée','verdict':'supported','references':['fake'],'reason':'x'}],'issues':[]}]
        with self.assertRaises(ValueError):require_report(self.r,body,'a')
    def test_report_prose_not_evidence_and_partial_not_success(self):
        t=task();self.s.plan(self.m,[t],metadata=self.meta)
        ref=self.observation(False)
        token=self.s.begin_call(self.m,'a','host_write_file',{'path':'/report.md','content':'Everything passed'})
        self.s.finish_call(token,{'ok':True,'result':{'returncode':0}},0)
        self.s.event(self.m,'semantic_verification','a',result={'status':'INSUFFICIENT','observations':[]})
        snap=evidence_snapshot(self.s,self.m,'a')
        self.assertEqual(len(snap['receipts']),1)
        body='Lecture impossible, INSUFFICIENT. '+ref
        self.responses=[{'claims':[{'quote':'Lecture impossible','verdict':'supported','references':[ref],'reason':'failed read'}],'issues':[]}]
        self.assertEqual(require_report(self.r,body,'a')['status'],'PASS')
        self.assertFalse(coverage_state(self.s,self.m)['accepted'])
    def test_no_review_transport_no_publication(self):
        del self.r.assurance_transport
        with self.assertRaises(ValueError):require_report(self.r,'Success')
    def test_historical_mission_not_forced_to_requalify(self):
        legacy=self.s.create('historical','model','conversation',spec={'autonomous':True})
        self.s.plan(legacy,[task()],metadata=self.meta)
        self.assertEqual(len(self.s.ready(legacy)),1)

    def test_plan_container_decoding_preserves_scalar_and_validation(self):
        from jarvis.tools import decode_plan_containers
        schema={'type':'object','properties':{'tasks':{'type':'array','items':{'type':'object','properties':{'depends':{'type':'array','items':{'type':'string'}},'title':{'type':'string'}}}},'expected_version':{'type':'integer'}}}
        original={'tasks':json.dumps([{'depends':'["a"]','title':'b'}]),'expected_version':'1'}
        decoded=decode_plan_containers(original,schema)
        self.assertEqual(decoded['tasks'][0]['depends'],['a'])
        self.assertEqual(decoded['expected_version'],'1')
        self.assertIsInstance(original['tasks'],str)
        import jsonschema
        with self.assertRaises(jsonschema.ValidationError):jsonschema.validate(decoded,schema)

    def test_manifest_digest_observes_content_not_announced_hash(self):
        import hashlib
        from jarvis.verification import evaluate, validate_contract, Verifier
        content='{"count":3,"sum":12}\n';wanted=hashlib.sha256(content.encode()).hexdigest()
        contract={'kind':'digest','source':{'tool':'host_read_file','arguments':{'path':'/manifest'}},'baseline_source':{'tool':'host_read_file','arguments':{'path':'/actual'}},'field':'/sha256'}
        validate_contract(contract)
        self.assertEqual(evaluate(json.dumps({'sha256':wanted}),contract,content)['status'],'PASS')
        self.assertEqual(evaluate(json.dumps({'sha256':'0'*64}),contract,content)['status'],'FAIL')
        self.assertEqual(evaluate(json.dumps({'sha256':wanted}),contract,None)['status'],'INSUFFICIENT')
        calls=[]
        def execute(name,args):
            calls.append(args['path'])
            return {'ok':True,'result':{'stdout':json.dumps({'sha256':wanted}) if args['path']=='/manifest' else content,'returncode':0}}
        self.r.execute=execute
        result=Verifier(self.r).verify(contract)
        self.assertEqual(result['status'],'PASS');self.assertEqual(calls,['/manifest','/actual'])

    def test_native_parser_field_spillage_repaired_without_changing_plan(self):
        from jarvis.tools import decode_plan_arguments
        schema={'type':'object','properties':{'tasks':{'type':'array'},'metadata':{'type':'object'}}}
        supplied={'tasks':'[{"id":"model-task"}], "metadata":{"objective":"raw goal"}}'}
        value=decode_plan_arguments(supplied,schema)
        self.assertEqual(value,{'tasks':[{'id':'model-task'}],'metadata':{'objective':'raw goal'}})
        self.assertIsInstance(supplied['tasks'],str)
        with self.assertRaises(ValueError):decode_plan_arguments({**supplied,'metadata':{'objective':'conflict'}},schema)

    def test_invalid_apostrophe_escape_repaired_only_for_containers(self):
        from jarvis.tools import decode_plan_containers
        value='[{"title":"Le plan d'+chr(92)+"'essai"+'"}]'
        schema={'type':'array','items':{'type':'object'}}
        self.assertEqual(decode_plan_containers(value,schema),[{"title":"Le plan d'essai"}])
        self.assertEqual(decode_plan_containers(value,{'type':'string'}),value)

    def test_active_plan_schema_exposes_actual_required_fields_and_versions(self):
        from jarvis.tools import Registry
        from jarvis.memory import Memory
        r=Registry(Memory(Path(self.s.root)/'memory.sqlite'),self.s.root)
        r.mission_store=self.s;r.context={'mission_id':self.m}
        schema=r.active_schema('mission_plan')
        self.assertIn('metadata',schema['required'])
        self.assertIn('contract',schema['properties']['tasks']['items']['required'])
        self.assertIn('success_criteria',schema['properties']['metadata']['required'])
        self.s.plan(self.m,[task()],metadata=self.meta)
        schema=r.active_schema('mission_plan');self.assertNotIn('metadata',schema['required']);self.assertIn('expected_version',schema['required'])

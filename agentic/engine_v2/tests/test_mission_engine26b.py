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
        return {'requirements':[{'id':'R1','source_segment':'G1','outcome':'file'},{'id':'R2','source_segment':'G1','outcome':'report'}],'output_constraints':[],'closure':{'on_unavailable':'report_only','source_segment':'G1','external_paths':[]}}
    def coverage(self,complete=True):
        return {'coverage':{'R1':{'tasks':['a'],'covered':True,'reason':'exact state'}, 'R2':{'tasks':['a'] if complete else [],'covered':complete,'reason':'report missing' if not complete else 'explicit final report'}},'issues':[]}
    def test_omission_blocks_effects_and_revision_survives_restart(self):
        self.responses=[self.extraction(),self.coverage(False),self.coverage(True)]
        requirements(self.r);self.s.plan(self.m,[task()],author='JARVIS',metadata=self.meta)
        self.assertEqual(audit_plan(self.r)['status'],'FAIL');self.assertEqual(self.s.ready(self.m),[])
        b=task('b');b['contract']['report_path']='/b-report.md'
        self.s.plan(self.m,[b],author='JARVIS',expected_version=1,append=True,reason='cover omission')
        self.assertFalse(coverage_state(self.s,self.m)['accepted'])
        self.assertEqual(audit_plan(self.r)['status'],'PASS')
        reopened=MissionStore(self.s.root)
        self.assertTrue(coverage_state(reopened,self.m)['accepted']);self.assertEqual(len(reopened.plans(self.m)),2)
    def test_forged_extraction_and_incomplete_review_fail_closed(self):
        bad=self.extraction();bad['requirements'][0]['source_segment']='G404'
        self.responses=[bad,copy.deepcopy(bad)]
        with self.assertRaises(ValueError):requirements(self.r)
        self.responses=[self.extraction(),{'coverage':{},'issues':[]},{'coverage':{},'issues':[]}]
        self.s.plan(self.m,[task()],metadata=self.meta)
        with self.assertRaises(ValueError):audit_plan(self.r)
        self.assertFalse(self.s.ready(self.m))
    def test_unknown_task_review_and_unreviewed_revision_block(self):
        a=self.coverage();a['coverage']['R1']['tasks']=['not-real']
        self.responses=[self.extraction(),a,copy.deepcopy(a)];self.s.plan(self.m,[task()],metadata=self.meta)
        with self.assertRaises(ValueError):audit_plan(self.r)
        self.assertEqual(self.s.ready(self.m),[])
    def observation(self,ok=True):
        token=self.s.begin_call(self.m,'a','host_read_file',{'path':'/a'})
        self.s.finish_call(token,{'ok':ok,'result':{'stdout':'{"port":8091}','returncode':0 if ok else 1}},0)
        return token
    def test_wrong_counts_hidden_failures_and_originals_retained(self):
        ref=self.observation();self.s.event(self.m,'semantic_verification','a',result={'status':'FAIL','contract':contract(),'observations':[]})
        self.responses=[{'claims':[{'segment':'S1','verdict':'contradicted','references':[ref],'reason':'only one read'}],'issues':[]}]
        body='observations : 999. '+ref
        result=audit_report(self.r,body,'a');self.assertEqual(result['status'],'FAIL')
        self.assertTrue(any('FAIL' in x for x in result['issues']))
        self.assertEqual(result['draft'],body)
        self.assertEqual(len([x for x in self.s.events(self.m) if x['kind']=='narrative_review']),1)
    def test_corrected_explanation_retained_and_unknown_refs_rejected(self):
        ref=self.observation()
        self.responses=[{'claims':[{'segment':'S1','verdict':'supported','references':[ref],'reason':'original read'}],'issues':[]}]
        body='Lecture observée : '+ref+'. La portée reste limitée au contenu relu.'
        result=require_report(self.r,body,'a');self.assertEqual(result['status'],'PASS')
        # Same receipt snapshot, no inference replay. A new observation invalidates approval.
        self.assertEqual(require_report(self.r,body,'a')['fingerprint'],result['fingerprint'])
        self.observation();bad={'claims':[{'segment':'S1','verdict':'supported','references':['fake'],'reason':'x'}],'issues':[]};self.responses=[bad,copy.deepcopy(bad)]
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
        self.responses=[{'claims':[{'segment':'S1','verdict':'supported','references':[ref],'reason':'failed read'}],'issues':[]}]
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

    def test_free_report_verified_against_receipts_without_guessed_hash(self):
        from jarvis.verification import Verifier, validate_contract
        ref=self.observation();body='Lecture indépendante observée : '+ref
        t=task();self.s.plan(self.m,[t],metadata=self.meta)
        self.r.execute=lambda name,args:{'ok':True,'result':{'stdout':body,'returncode':0}}
        self.responses=[{'claims':[{'segment':'S1','verdict':'supported','references':[ref],'reason':'read receipt'}],'issues':[]}]
        c={'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/report.md'}}}
        validate_contract(c);result=Verifier(self.r).verify(c);self.assertEqual(result['status'],'PASS');self.assertEqual(result['verifier'],'broker-read+JARVIS-reviewer26B')
        wrong={'kind':'service','source':c['source'],'expected_state':'active'}
        with self.assertRaises(ValueError):validate_contract(wrong)

    def test_unattempted_candidate_criterion_can_be_corrected_but_owner_stays(self):
        self.s.plan(self.m,[task()],metadata=self.meta)
        changed=task();changed['contract']['semantic'][0]['expected']={'/port':8092}
        self.s.plan(self.m,[changed],metadata=self.meta,expected_version=1,reason='correct candidate before execution')
        self.assertFalse(coverage_state(self.s,self.m)['accepted'])
        with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'autonomous':True,'assurance':True,'acceptance':[contract()]}),self.m))
        other=copy.deepcopy(changed);other['id']='other'
        with self.assertRaises(ValueError):self.s.plan(self.m,[changed,other],metadata=self.meta,expected_version=2)

    def test_saved_candidate_without_review_is_recovered_without_replanning(self):
        from jarvis.mission_assurance import ensure_plan_review
        self.s.plan(self.m,[task()],author='JARVIS',metadata=self.meta)
        original=self.s.plans(self.m)
        self.assertFalse(self.s.ready(self.m))
        self.responses=[self.extraction(),self.coverage(True)]
        self.assertEqual(ensure_plan_review(self.r)['status'],'PASS')
        self.assertEqual(self.s.plans(self.m),original)
        self.assertEqual(len(self.s.ready(self.m)),1)
        self.assertEqual(ensure_plan_review(self.r)['status'],'PASS')

    def test_failed_never_passed_inferred_criterion_can_be_repaired_with_history(self):
        self.s.plan(self.m,[task()],metadata=self.meta)
        self.observation(False)
        with self.s.db() as c:c.execute("UPDATE tasks SET state='running' WHERE mission=?",(self.m,))
        self.s.event(self.m,'semantic_verification','a',result={'contract':contract(),'status':'FAIL'})
        revised=task();revised['contract']['semantic'][0]['expected']={'/port':8092}
        self.s.plan(self.m,[revised],metadata=self.meta,expected_version=1,reason='observed wrong inferred criterion')
        self.assertFalse(coverage_state(self.s,self.m)['accepted'])
        self.assertTrue(any(e['kind']=='failed_criterion_revision_proposed' for e in self.s.events(self.m)))
        criterion=revised['contract']['semantic'][0]
        self.s.event(self.m,'semantic_verification','a',result={'contract':criterion,'status':'PASS'})
        self.s.event(self.m,'semantic_verification','a',result={'contract':criterion,'status':'FAIL'})
        revised['contract']['semantic'][0]['expected']={'/port':8093}
        with self.assertRaises(ValueError):self.s.plan(self.m,[revised],metadata=self.meta,expected_version=2,reason='cannot weaken proven criterion')

    def test_plan_context_bounded_without_losing_historical_definitions(self):
        from jarvis.mission_assurance import plan_view
        self.s.plan(self.m,[task()],metadata=self.meta)
        for version in range(1,15):
            t=task();t['objective']='x'*2000+str(version)
            self.s.plan(self.m,[t],metadata=self.meta,expected_version=version,reason='new observation '+str(version))
        history=self.s.plans(self.m);view=plan_view(self.s,self.m)
        self.assertEqual(len(view),len(history))
        self.assertEqual(view[-1]['plan'],history[-1]['plan'])
        self.assertLess(len(json.dumps(view)),len(json.dumps(history))//3)
        self.assertEqual(self.s.plans(self.m)[0]['plan']['tasks'][0]['objective'],'fix')

    def test_shared_report_collision_blocks_even_when_model_says_covered(self):
        self.responses=[self.extraction(),self.coverage(True)]
        self.s.plan(self.m,[task(),task('b')],metadata=self.meta)
        result=audit_plan(self.r)
        self.assertEqual(result['status'],'FAIL')
        self.assertTrue(any('collision' in issue for issue in result['issues']))
        self.assertEqual(self.s.ready(self.m),[])

    def test_reviewer_uses_exact_original_segments_and_original_reference_ids(self):
        ref=self.observation();body='Lecture réellement observée : '+ref+'.\n\nHypothèse : la suite reste non vérifiée.'
        self.responses=[{'claims':[{'segment':'S1','verdict':'supported','references':[ref],'reason':'actual read'},{'segment':'S2','verdict':'qualified_hypothesis','references':[],'reason':'explicitly uncertain'}],'issues':[]}]
        result=require_report(self.r,body,'a')
        self.assertEqual(result['status'],'PASS')
        self.assertEqual([x['quote'] for x in result['claims']],body.split('\n\n'))

    def test_review_format_fault_retried_without_blame_on_writer(self):
        ref=self.observation();body='Lecture '+ref+'.\n\nAutre paragraphe factuel.'
        bad={'claims':[{'segment':'S1','verdict':'supported','references':['receipts[0]'],'reason':'wrong addressing'}],'issues':[]}
        self.responses=[bad,copy.deepcopy(bad)]
        with self.assertRaises(ValueError):require_report(self.r,body,'a')
        events=self.s.events(self.m)
        self.assertEqual(len([e for e in events if e['kind']=='review_format_rejected']),2)
        self.assertFalse(any(e['kind']=='narrative_review' for e in events))

    def test_typed_goal_list_cannot_be_replaced_by_histogram_even_if_reviewer_says_yes(self):
        goal='Create inventaire.json with a list and an integer count.'
        with self.s.db() as c:c.execute('UPDATE missions SET goal=? WHERE id=?',(goal,self.m))
        extraction={'requirements':[{'id':'R1','source_segment':'G1','outcome':'list'},{'id':'R2','source_segment':'G1','outcome':'total'}],'output_constraints':[{'artifact':'inventaire.json','source_segment':'G1','required_type':'array','meaning':'names list','relation':'none'},{'artifact':'inventaire.json','source_segment':'G1','required_type':'integer','meaning':'global total','relation':'length_of_array'}]}
        extraction['closure']=self.extraction()['closure']
        self.responses=[extraction,self.coverage(True),self.coverage(True)]
        t=task();t['contract']['semantic']=[{'kind':'json','source':{'tool':'host_read_file','arguments':{'path':'/inventaire.json'}},'expected':{'/a':1,'/b':1},'types':{'/a':'integer','/b':'integer'}}]
        self.s.plan(self.m,[t],metadata=self.meta)
        result=audit_plan(self.r)
        self.assertEqual(result['status'],'FAIL');self.assertTrue(any('requires array' in issue for issue in result['issues']))
        t['contract']['semantic'][0]['expected']={'/names':['a','b'],'/count':2};t['contract']['semantic'][0]['types']={'/names':'array','/count':'integer'}
        self.s.plan(self.m,[t],metadata=self.meta,expected_version=1,reason='repair uncovered output representation')
        self.assertEqual(audit_plan(self.r)['status'],'PASS')
        self.assertEqual(len(self.s.plans(self.m)),2)

    def test_report_can_cite_dependency_and_planning_receipts_but_not_unrelated_sibling(self):
        a=task();b=task('b');b['depends']=['a'];b['contract']['report_path']='/b-report.md';c=task('c');c['contract']['report_path']='/c-report.md'
        self.s.plan(self.m,[a,b,c],metadata=self.meta)
        ancestor=self.observation();ids={}
        for label in ['b','c',None]:
            token=self.s.begin_call(self.m,label,'host_read_file',{'path':'/input-'+str(label)})
            self.s.finish_call(token,{'ok':True,'result':{'stdout':'data','returncode':0}},0);ids[label]=token
        snapshot=evidence_snapshot(self.s,self.m,'b');refs={r['reference'] for r in snapshot['receipts']}
        self.assertIn(ancestor,refs);self.assertIn(ids['b'],refs);self.assertIn(ids[None],refs);self.assertNotIn(ids['c'],refs)

    def test_raw_goal_change_invalidates_coverage_and_versions_requirements(self):
        self.responses=[self.extraction(),self.coverage(True),self.extraction()]
        self.s.plan(self.m,[task()],metadata=self.meta);audit_plan(self.r)
        self.assertTrue(coverage_state(self.s,self.m)['accepted'])
        with self.s.db() as c:c.execute('UPDATE missions SET goal=? WHERE id=?',('Produce a file and a report and a log',self.m))
        self.assertFalse(coverage_state(self.s,self.m)['accepted'])
        revised=requirements(self.r);self.assertEqual(revised['version'],2)
        self.assertEqual(len([e for e in self.s.events(self.m) if e['kind']=='goal_requirements']),2)

    def test_review_native_json_containers_are_decoded_before_strict_validation(self):
        ref=self.observation();body='Lecture réellement observée : '+ref
        self.responses=[{'claims':json.dumps([{'segment':'S1','verdict':'supported','references':[ref],'reason':'real read'}]),'issues':'[]'}]
        self.assertEqual(require_report(self.r,body,'a')['status'],'PASS')

    def test_array_length_relation_refutes_incorrect_global_count(self):
        from jarvis.verification import evaluate,validate_contract
        contract={'kind':'json','source':{'tool':'host_read_file','arguments':{'path':'/inventory.json'}},'relations':[{'kind':'length','array':'/names','count':'/count'}]}
        validate_contract(contract)
        self.assertEqual(evaluate('{"names":["a","b"],"count":1,"status":"ok"}',contract)['status'],'FAIL')
        self.assertEqual(evaluate('{"names":["a","b"],"count":2}',contract)['status'],'PASS')
        self.assertEqual(evaluate('{"names":["a"],"count":true}',contract)['status'],'FAIL')

    def test_goal_quotes_are_original_spans_not_model_rewording(self):
        self.responses=[self.extraction()]
        result=requirements(self.r)
        self.assertTrue(all(row['quote']=='Produce a file and a report' for row in result['requirements']))
        self.assertTrue(all(row['source_segment']=='G1' for row in result['requirements']))

    def test_report_verification_cannot_mistake_source_program_for_task_report(self):
        t=task();t['contract']['semantic']=[{'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/producer.py'}}}]
        with self.assertRaisesRegex(ValueError,'kind report must read'):self.s.plan(self.m,[t],metadata=self.meta)
        self.assertEqual(self.s.plans(self.m),[])

    def test_legacy_misrouted_report_criterion_can_be_repaired_without_reset(self):
        import hashlib
        t=task();t['contract']['semantic']=[{'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/report.md'}}}]
        self.s.plan(self.m,[t],author='JARVIS',metadata=self.meta)
        previous=self.s.plans(self.m)[0]['plan'];previous['tasks'][0]['contract']['semantic'][0]['source']['arguments']['path']='/producer.py'
        from jarvis.mission_store import encoded
        with self.s.db() as c:
            c.execute('UPDATE mission_plans SET plan=?,sha256=? WHERE mission=?',(encoded(previous),hashlib.sha256(encoded(previous).encode()).hexdigest(),self.m))
            c.execute("UPDATE tasks SET contract=?,state='running' WHERE mission=?",(encoded(previous['tasks'][0]['contract']),self.m))
        self.observation(False)
        self.s.plan(self.m,[t],author='JARVIS',metadata=self.meta,expected_version=1,reason='correct source/report binding after old interface accepted program input')
        self.assertEqual(len(self.s.plans(self.m)),2)
        self.assertEqual(self.s.plans(self.m)[0]['plan']['tasks'][0]['contract']['semantic'][0]['source']['arguments']['path'],'/producer.py')
        self.assertEqual(self.s.plans(self.m)[1]['plan']['tasks'][0]['contract']['semantic'][0]['source']['arguments']['path'],'/report.md')
        self.assertEqual(len(self.s.observations(self.m)),1)

    def test_real_tool_receipt_classes_include_web_and_skill_registry_reads(self):
        refs=[]
        for name,value in [('web_fetch',{'url':'https://docs.python.org/3/library/csv.html','content':'CSV reader documentation'}),('skill_list',{'active':[{'name':'known','version':6}]})]:
            token=self.s.begin_call(self.m,'a',name,{})
            self.s.finish_call(token,{'ok':True,'result':value},0);refs.append(token)
        snapshot=evidence_snapshot(self.s,self.m,'a')
        self.assertEqual({r['reference'] for r in snapshot['receipts']},set(refs))

    def test_broker_reference_retained_even_when_receipt_body_is_excerpted(self):
        token=self.s.begin_call(self.m,'a','host_read_file',{'path':'/a'})
        self.s.finish_call(token,{'ok':True,'result':{'stdout':'data'*3000,'returncode':0,'evidence_id':'broker-proof-1'}},0)
        snapshot=evidence_snapshot(self.s,self.m,'a')
        self.assertIn('explicit_excerpt',snapshot['receipts'][0]['observed'])
        self.assertEqual(snapshot['receipts'][0]['broker_evidence'],'broker-proof-1')
        self.responses=[{'claims':[{'segment':'S1','verdict':'supported','references':['broker-proof-1'],'reason':'actual successful read receipt'}],'issues':[]}]
        self.assertEqual(require_report(self.r,'Lecture effectuée, preuve broker-proof-1.','a')['status'],'PASS')

    def test_review_reply_is_actionable_while_original_snapshot_remains_durable(self):
        from jarvis.mission_assurance import register
        ref=self.observation();body='Lecture effectuée '+ref
        self.responses=[{'claims':[{'segment':'S1','verdict':'supported','references':[ref],'reason':'read'}],'issues':[]}]
        self.r.specs={};register(self.r);fn=self.r.specs['mission_report_review'][4]
        reply=fn({'content':body,'scope':'task'})
        self.assertEqual(reply['status'],'PASS');self.assertNotIn('snapshot',reply)
        original=next(e for e in self.s.events(self.m) if e['id']==reply['review_event'])
        self.assertEqual(original['result']['draft'],body);self.assertTrue(original['result']['snapshot']['receipts'])
        expanded=fn({'content':body,'scope':'task','include_evidence':True})
        self.assertIn('snapshot',expanded);self.assertEqual(expanded['review_event'],reply['review_event'])

    def test_evidence_lookup_own_event_and_reject_foreign_event(self):
        from jarvis.durable_tools import register
        self.r.specs={};register(self.r);fn=self.r.specs['mission_evidence'][4]
        event=self.s.event(self.m,'semantic_verification','a',result={'status':'FAIL'})
        result=fn({'id':'event:'+str(event)})
        self.assertIn('FAIL',result['content'])
        other=self.s.create('other','model','conversation')
        foreign=self.s.event(other,'working_note',result={'content':'foreign'})
        with self.assertRaises(ValueError):fn({'id':'event:'+str(foreign)})

    def test_constrained_json_review_without_action_tools(self):
        from jarvis.mission_assurance import review_model
        captured=[]
        def transport(payload):
            captured.append(payload)
            return {'content':'{"reference":"requirements:3"}'}
        self.r.assurance_transport=transport
        schema={'type':'object','properties':{'reference':{'type':'string','enum':['requirements:3']}},'required':['reference'],'additionalProperties':False}
        value=review_model(self.r,'narrative','Review only',{},schema)
        self.assertEqual(value,{'reference':'requirements:3'})
        self.assertEqual(captured[0]['format'],schema)
        self.assertNotIn('tools',captured[0])
        self.assertEqual(captured[0]['options']['temperature'],0)
        self.assertEqual(captured[0]['options']['presence_penalty'],0)

    def test_manifest_reader_requires_latest_declared_writer(self):
        from jarvis.mission_assurance import artifact_dependency_issues
        first=task('first');first['tools']=['host_write_file'];first['artifacts']=['/inventory.json']
        correction=copy.deepcopy(first);correction['id']='correct';correction['depends']=['first']
        manifest=task('manifest');manifest['depends']=['first'];manifest['artifacts']=['/manifest.json']
        manifest['contract']['semantic']=[{'kind':'json','source':{'tool':'host_read_file','arguments':{'path':'/manifest.json'}},'expected':{'/target':'/inventory.json'}}]
        plan={'tasks':[first,correction,manifest]}
        self.assertTrue(any('correct' in issue for issue in artifact_dependency_issues(plan)))
        manifest['depends']=['correct']
        self.assertEqual(artifact_dependency_issues(plan),[])

    def test_external_wait_does_not_strand_independent_local_work(self):
        from jarvis.durable_tools import register
        from unittest.mock import patch
        a=task('a');b=task('b');c=task('c');c['depends']=['a']
        self.s.plan(self.m,[a,b,c],metadata=self.meta)
        proof=self.observation(False)
        self.r.specs={};register(self.r);fn=self.r.specs['mission_block'][4]
        self.r.specs['host_read_file']=(None,None,None,None,lambda args:{'returncode':0,'stdout':'External witness unavailable. The local result remains partial; no external verification is claimed.'})
        args={'reason':'unavailable','report_path':'/report.md','evidence_id':proof}
        with self.assertRaisesRegex(ValueError,'independently executable local tasks: b'):fn(args)
        self.assertNotEqual(self.s.get(self.m)['state'],'waiting_external')
        with self.s.db() as connection:connection.execute("UPDATE tasks SET state='validated' WHERE mission=? AND id='b'",(self.m,))
        with patch('jarvis.mission_assurance.require_report',return_value={'status':'PASS'}):
            result=fn(args)
        self.assertEqual(result['state'],'waiting_external')
        self.assertEqual(next(t for t in self.s.tasks(self.m) if t['id']=='b')['state'],'validated')

    def test_report_review_gets_cited_original_plan_definitions(self):
        proposed=task();self.s.plan(self.m,[proposed],metadata=self.meta)
        reference=self.observation();captured=[]
        def transport(payload):
            captured.append(json.loads(payload['messages'][1]['content']))
            return {'content':json.dumps({'claims':[{'segment':'S1','verdict':'qualified_hypothesis','references':['plan:1'],'reason':'planned only'}],'issues':[]})}
        self.r.assurance_transport=transport
        result=audit_report(self.r,'Le plan v1 prévoit la tâche a. Correction future seulement, aucun succès annoncé. Référence : '+reference,'a')
        self.assertEqual(result['status'],'PASS')
        definitions=captured[0]['evidence']['plan_definitions']
        self.assertEqual(definitions[0]['sha256'],self.s.plans(self.m)[0]['sha256'])
        self.assertEqual(definitions[0]['plan']['tasks'][0]['contract'],proposed['contract'])

    def test_exact_list_not_covered_by_type_and_length_only(self):
        from jarvis.mission_assurance import typed_coverage_issues
        requirement={'output_constraints':[{'artifact':'out.json','quote':'une liste exacte des noms','required_type':'array','meaning':'names','relation':'none'}]}
        predicate={'kind':'json','source':{'tool':'host_read_file','arguments':{'path':'/out.json'}},'types':{'/names':'array','/total':'integer'},'relations':[{'kind':'length','array':'/names','count':'/total'}]}
        t=task();t['contract']['semantic']=[predicate];plan={'tasks':[t]}
        self.assertTrue(any('exact array' in issue for issue in typed_coverage_issues(requirement,plan)))
        predicate.update({'baseline_source':copy.deepcopy(predicate['source']),'preserve':['/names']})
        self.assertTrue(typed_coverage_issues(requirement,plan))
        predicate['baseline_source']['arguments']['path']='/input.json'
        predicate['preserve']=['/label']
        self.assertTrue(typed_coverage_issues(requirement,plan))
        predicate['preserve']=['/names']
        self.assertEqual(typed_coverage_issues(requirement,plan),[])
        predicate.pop('baseline_source');predicate.pop('preserve');predicate['expected']={'/names':['a','b']}
        self.assertEqual(typed_coverage_issues(requirement,plan),[])

    def test_coverage_requires_all_keys_and_repairs_reviewer_not_plan(self):
        from jarvis.mission_assurance import latest
        incomplete=self.coverage();incomplete['coverage'].pop('R2')
        self.responses=[self.extraction(),incomplete,self.coverage()]
        self.s.plan(self.m,[task()],metadata=self.meta)
        result=audit_plan(self.r)
        self.assertEqual(result['status'],'PASS')
        self.assertEqual({row['requirement'] for row in result['coverage']},{'R1','R2'})
        self.assertEqual(len(self.s.plans(self.m)),1)
        rejected=[e for e in self.s.events(self.m) if e['kind']=='review_format_rejected']
        self.assertEqual(len(rejected),1)
        self.assertTrue(rejected[0]['result']['author_not_blamed'])

    def test_editorial_failure_survives_technical_pass_and_store_reopen(self):
        from jarvis.mission_assurance import pending_report_feedback
        event=self.s.event(self.m,'narrative_review','a',result={'status':'FAIL','issues':['Historical FAIL must be retained'],'draft_sha256':'draft'})
        self.observation()
        self.s.event(self.m,'semantic_verification','a',result={'status':'PASS'})
        self.s.event(self.m,'narrative_review','b',result={'status':'PASS'})
        reopened=MissionStore(self.s.root)
        pending=pending_report_feedback(reopened,self.m,'a')
        self.assertEqual(pending['review_reference'],'event:'+str(event))
        self.assertEqual(pending['issues'],['Historical FAIL must be retained'])
        self.s.event(self.m,'narrative_review','a',result={'status':'PASS'})
        self.assertIsNone(pending_report_feedback(reopened,self.m,'a'))

    def test_injected_historical_faults_cannot_be_dismissed_nonfactual(self):
        reference=self.observation()
        body='Cet appel a été exécuté par Codex.\n\nCet appel a eu lieu en 2001.\n\nobservations : 999.\n\nRéférence : '+reference
        bad={'claims':[{'segment':'S'+str(i),'verdict':'not_factual' if i<4 else 'supported','references':[] if i<4 else [reference],'reason':'test'} for i in range(1,5)],'issues':[]}
        corrected=copy.deepcopy(bad)
        for claim in corrected['claims'][:3]:claim.update(verdict='contradicted',references=[reference],reason='actual original receipt contradicts the assertion')
        self.responses=[bad,corrected]
        result=audit_report(self.r,body,'a')
        self.assertEqual(result['status'],'FAIL')
        self.assertTrue(all(c['verdict']=='contradicted' for c in result['claims'][:3]))
        self.assertEqual(len([e for e in self.s.events(self.m) if e['kind']=='review_format_rejected']),1)

    def test_unqualified_past_fact_not_relabelled_as_hypothesis(self):
        reference=self.observation()
        claim={'segment':'S1','verdict':'qualified_hypothesis','references':[reference],'reason':'supposed'}
        self.responses=[{'claims':[claim],'issues':[]},{'claims':[{**claim,'verdict':'contradicted'}],'issues':[]}]
        result=audit_report(self.r,'Cet appel a été exécuté par Codex. '+reference,'a')
        self.assertEqual(result['claims'][0]['verdict'],'contradicted')

    def test_report_semantic_verdict_not_its_own_business_evidence(self):
        reference=self.observation()
        self.responses=[{'claims':[{'segment':'S1','verdict':'supported','references':[reference],'reason':'original technical read'}],'issues':[]}]
        body='Lecture du fichier source confirmée par le reçu '+reference+'. Aucune autre opération n’est affirmée.'
        first=audit_report(self.r,body,'a')
        event=self.s.event(self.m,'semantic_verification','a',result={'status':'PASS','contract':{'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/report.md'}}}})
        snapshot=evidence_snapshot(self.s,self.m,'a')
        self.assertNotIn('event:'+str(event),[x['reference'] for x in snapshot['semantic_verifications']])
        self.assertEqual(snapshot['counts']['semantic_verdicts']['PASS'],0)
        self.assertEqual(audit_report(self.r,body,'a')['fingerprint'],first['fingerprint'])
        self.s.event(self.m,'semantic_verification','a',result={'status':'PASS','contract':contract()})
        self.assertEqual(evidence_snapshot(self.s,self.m,'a')['counts']['semantic_verdicts']['PASS'],1)

    def test_cited_failure_causes_checked_separately_against_original_events(self):
        first=self.s.event(self.m,'review_format_rejected','a',actor='JARVIS-reviewer',result={'status':'INSUFFICIENT','error':'unknown reference','author_not_blamed':True})
        second=self.s.event(self.m,'narrative_review','a',actor='JARVIS-reviewer',result={'status':'FAIL','issues':['actor incorrect']})
        refs=['event:'+str(first),'event:'+str(second)]
        body='Les events: '+str(first)+', '+str(second)+' ont tous été FAIL pour attribution incorrecte.'
        self.responses=[{'claims':[{'segment':'S1','verdict':'supported','references':refs,'reason':'both rejected'}],'issues':[],
                        'cited_event_checks':{refs[0]:{'supported':False,'reason':'reviewer format, not actor error'},refs[1]:{'supported':True,'reason':'actor incorrect'}}}]
        result=audit_report(self.r,body,'a')
        self.assertEqual(result['status'],'FAIL')
        facts=result['snapshot']['cited_event_facts']
        self.assertEqual(facts[0]['kind'],'review_format_rejected')
        self.assertEqual(facts[0]['actor'],'JARVIS-reviewer')
        self.assertIn('created',facts[0])
        self.assertTrue(any('reviewer format' in issue for issue in result['issues']))

    def test_cited_event_from_another_mission_is_not_imported(self):
        other=self.s.create('other','model','conversation');foreign=self.s.event(other,'working_note',result={'content':'private'})
        ref='event:'+str(foreign)
        self.responses=[{'claims':[{'segment':'S1','verdict':'insufficient','references':[],'reason':'not found'}],'issues':[],
                         'cited_event_checks':{ref:{'supported':False,'reason':'not in this mission'}}}]
        result=audit_report(self.r,'Cet appel a été vérifié : '+ref,'a')
        self.assertEqual(result['status'],'FAIL')
        self.assertFalse(result['snapshot']['cited_event_facts'][0]['found_in_mission'])
        self.assertNotIn('private',json.dumps(result['snapshot']))

    def test_natural_event_references_resolve_original_semantic_contract(self):
        from jarvis.mission_assurance import cited_event_facts
        event=self.s.event(self.m,'semantic_verification','a',result={'status':'FAIL','contract':contract(),'checks':[{'actual':0,'expected':8091,'pass':False}]})
        for prefix in ['event:','mission_verify event ','événement ','events: ']:
            facts=cited_event_facts(self.s,self.m,prefix+str(event))
            self.assertEqual(len(facts),1)
            self.assertEqual(facts[0]['facts']['contract'],contract())
            self.assertEqual(facts[0]['facts']['checks'][0]['actual'],0)

    def test_bounded_report_view_preserves_cited_old_receipt_and_mission_identity(self):
        from jarvis.mission_assurance import report_model_view
        old=self.observation()
        for i in range(30):
            self.s.event(self.m,'narrative_review','a',result={'status':'FAIL','issues':['unrelated protocol detail '*200],'draft_sha256':str(i)})
        self.observation()
        snapshot=evidence_snapshot(self.s,self.m,'a');snapshot['active_contracts']={'reference':'contracts:active','engine':'test'};snapshot['plan_definitions']=[]
        view=report_model_view(snapshot,'Lecture originale '+old,recent=0)
        self.assertEqual(view['mission'],self.m)
        self.assertIn(old,view['known_receipt_references'])
        self.assertIn(old,[row['reference'] for row in view['receipts']])
        self.assertNotIn('unrelated protocol detail',json.dumps(view))
        self.assertLess(len(json.dumps(view)),len(json.dumps(snapshot))/2)

    def test_working_state_refreshes_saved_plan_even_before_its_review(self):
        from jarvis.mission_assurance import working_assurance_state
        self.s.plan(self.m,[task()],metadata=self.meta)
        first=working_assurance_state(self.s,self.m)
        added=task('b');added['contract']['report_path']='/b.md'
        self.s.plan(self.m,[added],append=True,expected_version=1,reason='new outcome')
        current=working_assurance_state(self.s,self.m)
        self.assertEqual(first['coverage']['current_version'],1)
        self.assertEqual(current['coverage']['current_version'],2)
        self.assertEqual({task['id'] for task in current['plan_history'][-1]['plan']['tasks']},{'a','b'})
        self.assertEqual({task['id'] for task in current['tasks']},{'a','b'})
        self.assertFalse(current['coverage']['accepted'])

    def test_editorial_findings_are_bounded_without_losing_claim_checks(self):
        reference=self.observation();captured=[]
        def transport(payload):
            captured.append(payload)
            return {'content':json.dumps({'claims':[{'segment':'S1','verdict':'supported','references':[reference],'reason':'original read'}],'issues':[]})}
        self.r.assurance_transport=transport
        result=audit_report(self.r,'Lecture confirmée : '+reference,'a')
        self.assertEqual(result['status'],'PASS')
        schema=captured[0]['format'];claim=schema['properties']['claims']['items']['properties']
        self.assertEqual(claim['references']['maxItems'],6)
        self.assertEqual(claim['reason']['maxLength'],200)
        self.assertEqual(schema['properties']['issues']['maxItems'],8)
        self.assertLessEqual(captured[0]['options']['num_predict'],16384)

    def test_parallel_writers_need_explicit_order_even_when_reader_waits_for_both(self):
        from jarvis.mission_assurance import artifact_dependency_issues
        old=task('old');old['tools']=['host_write_file'];old['artifacts']=['/output.json']
        new=copy.deepcopy(old);new['id']='new'
        reader=task('reader');reader['depends']=['old','new'];reader['contract']['semantic']=[{'kind':'json','source':{'tool':'host_read_file','arguments':{'path':'/output.json'}},'types':{'':'object'}}]
        plan={'tasks':[old,new,reader]}
        self.assertTrue(any('Unordered artifact writers' in issue for issue in artifact_dependency_issues(plan)))
        new['depends']=['old']
        self.assertEqual(artifact_dependency_issues(plan),[])

    def test_quoted_bad_count_and_measurements_are_not_tool_call_counts(self):
        ref=self.observation()
        snap=evidence_snapshot(self.s,self.m,'a')
        historical='FAIL : le brouillon contenait « observations : 999 », erreur rejetée. '+ref
        self.assertEqual(deterministic_report_issues(historical,snap),[])
        self.assertEqual(deterministic_report_issues('Mesures du CSV : observations : 2. '+ref,snap),[])
        self.assertTrue(any('observations_in_scope incorrect' in issue for issue in deterministic_report_issues('observations_in_scope: 999. '+ref,snap)))
        self.responses=[{'claims':[{'segment':'S1','verdict':'contradicted','references':[ref],'reason':'Unqualified 999 unsupported'}],'issues':[]}]
        self.assertEqual(audit_report(self.r,'observations : 999. '+ref,'a')['status'],'FAIL')

    def test_semantic_report_source_cannot_prove_its_own_text_or_change_counts(self):
        t=task();t['artifacts']=['/draft.md'];t['contract']['semantic']=[{'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/draft.md'}}}]
        self.s.plan(self.m,[t],metadata=self.meta);ref=self.observation()
        before=evidence_snapshot(self.s,self.m,'a')
        for name in ('host_write_file','host_read_file'):
            token=self.s.begin_call(self.m,'a',name,{'path':'/draft.md','content':'observations : 999'})
            self.s.finish_call(token,{'ok':True,'result':{'returncode':0,'stdout':'observations : 999'}},0)
        after=evidence_snapshot(self.s,self.m,'a')
        self.assertEqual(after['counts'],before['counts']);self.assertEqual([o['reference'] for o in after['receipts']],[ref])

    def test_closure_uses_latest_real_external_read_without_resetting_validated_tasks(self):
        from jarvis.mission_assurance import closure_state
        self.s.plan(self.m,[task()],metadata=self.meta)
        self.s.event(self.m,'goal_requirements',result={'closure':{'on_unavailable':'waiting_external','external_paths':['/external.json'],'quote':'wait'}})
        with self.s.db() as c:c.execute("UPDATE tasks SET state='validated' WHERE mission=?",(self.m,))
        self.assertEqual(closure_state(self.s,self.m)['unobserved'],['/external.json'])
        token=self.s.begin_call(self.m,'a','host_read_file',{'path':'/external.json'})
        self.s.finish_call(token,{'ok':False,'error':'FileNotFoundError','result':{'returncode':1}},0)
        state=closure_state(self.s,self.m)
        self.assertFalse(state['final_allowed']);self.assertEqual(state['unresolved'][0]['reference'],token)
        self.assertEqual(self.s.tasks(self.m)[0]['state'],'validated')
        token=self.s.begin_call(self.m,None,'host_read_file',{'path':'/external.json'})
        self.s.finish_call(token,{'ok':True,'result':{'stdout':'{}','returncode':0}},0)
        self.assertTrue(closure_state(self.s,self.m)['final_allowed'])

    def test_final_tool_refuses_external_wait_even_when_local_tasks_all_validated(self):
        from unittest.mock import patch
        from jarvis.tools import Registry
        from jarvis.memory import Memory
        self.s.plan(self.m,[task()],metadata=self.meta)
        with self.s.db() as c:c.execute("UPDATE tasks SET state='validated' WHERE mission=?",(self.m,))
        r=Registry(Memory(Path(self.s.root)/'memory.sqlite'),self.s.root);r.mission_store=self.s;r.context={'mission_id':self.m}
        with patch('jarvis.mission_assurance.require_final_outcome',side_effect=ValueError('unresolved external')):
            with self.assertRaisesRegex(ValueError,'unresolved external'):r.report({'content':'Local results verified, external dependency remains absent. No external verification.'})
        self.assertFalse((self.s.root/'runtime/reports'/self.m/'RAPPORT-FINAL.md').exists())

    def test_global_partial_block_preserves_all_validated_task_receipts(self):
        from jarvis.durable_tools import register
        from unittest.mock import patch
        self.s.plan(self.m,[task()],metadata=self.meta)
        with self.s.db() as c:c.execute("UPDATE tasks SET state='validated',report_sha256='old-sha' WHERE mission=?",(self.m,))
        proof=self.observation(False);self.r.context['task_id']=None
        self.r.specs={};register(self.r)
        self.r.specs['host_read_file']=(None,None,None,None,lambda a:{'returncode':0,'stdout':'Partial outcome: local artifacts verified; external witness unreadable, no content or success claimed. Original failure retained.'})
        with patch('jarvis.mission_assurance.require_report',return_value={'status':'PASS'}):
            value=self.r.specs['mission_block'][4]({'reason':'missing','report_path':'/partial.md','evidence_id':proof})
        self.assertEqual(value['state'],'waiting_external');self.assertEqual(self.s.tasks(self.m)[0]['state'],'validated')
        self.assertEqual(self.s.tasks(self.m)[0]['report_sha256'],'old-sha')

    def test_successful_read_cannot_establish_external_block(self):
        from jarvis.durable_tools import register
        proof=self.observation(True);self.r.specs={};register(self.r)
        with self.assertRaisesRegex(ValueError,'actually failed observation'):
            self.r.specs['mission_block'][4]({'reason':'missing','report_path':'/partial.md','evidence_id':proof})

    def test_explicit_external_wait_cannot_be_downgraded_to_accessibility_report(self):
        with self.s.db() as c:c.execute('UPDATE missions SET goal=? WHERE id=?',('Observe /external.json. Puis enregistre ce blocage externe.',self.m))
        wrong=self.extraction();wrong['closure']['external_paths']=['/external.json']
        corrected=copy.deepcopy(wrong);corrected['closure'].update(on_unavailable='waiting_external',source_segment='G2')
        self.responses=[wrong,corrected]
        value=requirements(self.r)
        self.assertEqual(value['closure']['on_unavailable'],'waiting_external')
        self.assertEqual(value['closure']['quote'],'Puis enregistre ce blocage externe.')
        rejected=[e for e in self.s.events(self.m) if e['kind']=='review_format_rejected']
        self.assertEqual(len(rejected),1);self.assertTrue(rejected[0]['result']['author_not_blamed'])

    def test_attached_event_status_cannot_be_overridden_by_reviewer_pass(self):
        from jarvis.mission_assurance import event_status_issues,cited_event_facts
        event=self.s.event(self.m,'narrative_review','a',result={'status':'FAIL','issues':['unknown receipt']})
        ref='event:'+str(event)
        body='FAIL conservé ; '+ref+' - INSUFFICIENT : livrable omis.'
        self.responses=[{'claims':[{'segment':'S1','verdict':'supported','references':[ref],'reason':'false positive'}],'issues':[], 'cited_event_checks':{ref:{'supported':True,'reason':'false positive'}}}]
        result=audit_report(self.r,body,'a')
        self.assertEqual(result['status'],'FAIL');self.assertTrue(any('status assertion INSUFFICIENT' in issue for issue in result['issues']))
        self.assertEqual(event_status_issues('FAIL '+ref,cited_event_facts(self.s,self.m,ref)),[])

    def test_focused_source_check_rejects_wrong_cause_after_global_model_pass(self):
        event=self.s.event(self.m,'narrative_review','a',result={'status':'FAIL','issues':['unknown receipt']})
        ref='event:'+str(event);body='FAIL '+ref+' : manifeste omis.'
        self.responses=[{'claims':[{'segment':'S1','verdict':'supported','references':[ref],'reason':'false positive'}],'issues':[], 'cited_event_checks':{ref:{'supported':True,'reason':'false positive'}}},
            {'checks':{ref:{'supported':False,'claimed_status':'FAIL','claimed_kind':'narrative_review','claimed_actor':None,'claimed_cause':'manifeste omis','supporting_diagnostic_index':None,'reason':'original only reports unknown receipt'}}}]
        result=audit_report(self.r,body,'a')
        self.assertEqual(result['status'],'FAIL');self.assertIn('focused_source_review',result)
        self.assertTrue(any('no supporting original issue' in issue for issue in result['issues']))

    def test_focused_source_check_retains_correct_original_diagnostic(self):
        from jarvis.mission_assurance import focused_event_review,cited_event_facts
        event=self.s.event(self.m,'narrative_review','a',result={'status':'FAIL','issues':['unknown receipt']})
        ref='event:'+str(event);body='FAIL '+ref+' : unknown receipt.'
        self.responses=[{'checks':{ref:{'supported':True,'claimed_status':'FAIL','claimed_kind':'narrative_review','claimed_actor':None,'claimed_cause':'unknown receipt','supporting_diagnostic_index':0,'reason':'exact original diagnostic'}}}]
        self.assertEqual(focused_event_review(self.r,body,cited_event_facts(self.s,self.m,body))['issues'],[])

    def test_focused_source_inferences_do_not_share_other_event_diagnostics(self):
        from jarvis.mission_assurance import focused_event_review,cited_event_facts
        first=self.s.event(self.m,'narrative_review','a',result={'status':'FAIL','issues':['receipt unknown']})
        second=self.s.event(self.m,'review_format_rejected','a',result={'status':'INSUFFICIENT','error':'schema invalid'})
        refs=['event:'+str(first),'event:'+str(second)]
        body='FAIL '+refs[0]+' : receipt unknown.\n\nINSUFFICIENT '+refs[1]+' : schema invalid.'
        seen=[]
        def transport(payload):
            data=json.loads(payload['messages'][1]['content']);seen.append(data)
            pair=data['source_report_pairs'][0];reference=pair['source']['reference']
            return {'content':json.dumps({'checks':{reference:{'supported':True,'claimed_status':pair['source']['facts']['status'],'claimed_kind':pair['source']['kind'],'claimed_actor':None,'claimed_cause':None,'supporting_diagnostic_index':0,'reason':'original exact diagnostic'}}})}
        self.r.assurance_transport=transport
        result=focused_event_review(self.r,body,cited_event_facts(self.s,self.m,body))
        self.assertEqual(result['issues'],[]);self.assertEqual(len(seen),2)
        self.assertTrue(all(len(data['source_report_pairs'])==1 for data in seen))
        self.assertNotIn('schema invalid',json.dumps(seen[0]));self.assertNotIn('receipt unknown',json.dumps(seen[1]))

    def test_numeric_event_reference_alias_reads_same_original_without_new_evidence(self):
        from jarvis.durable_tools import register
        original=self.s.event(self.m,'semantic_verification','a',result={'status':'PASS'})
        self.r.specs={};register(self.r);fn=self.r.specs['mission_evidence'][4]
        before=len(self.s.events(self.m))
        self.assertEqual(fn({'id':str(original)}),fn({'id':'event:'+str(original)}))
        self.assertEqual(len(self.s.events(self.m)),before)

    def test_numeric_event_reference_alias_never_reads_another_mission(self):
        from jarvis.durable_tools import register
        other=self.s.create('other','model','conversation');original=self.s.event(other,'working_note',result={'secret':'other mission'})
        self.r.specs={};register(self.r)
        with self.assertRaisesRegex(ValueError,'Preuve absente'):
            self.r.specs['mission_evidence'][4]({'id':str(original)})

    def test_exact_controller_erratum_links_original_without_erasing_failure(self):
        from jarvis.mission_assurance import finding_rectifications,cited_event_facts
        finding='observations incorrect: expected 176, actual 999'
        original=self.s.event(self.m,'narrative_review',result={'status':'FAIL','issues':[finding,'missing original reference']})
        erratum=self.s.event(self.m,'controller_findings_rectified',actor='Codex',result={'reason':'Ambiguous old regex, historical quote is not a new measurement','withdrawn':[{'event':original,'findings':[finding]}]})
        linked=finding_rectifications(self.s,self.m)['event:'+str(original)]
        self.assertEqual(linked['reference'],'event:'+str(erratum));self.assertEqual(linked['withdrawn_findings'],[finding])
        facts=cited_event_facts(self.s,self.m,'event:'+str(original))[0]['facts']
        self.assertEqual(facts['status'],'FAIL');self.assertEqual(facts['issues'],[finding,'missing original reference'])
        self.assertIn('controller_rectification',facts)

    def test_controller_erratum_cannot_link_foreign_or_nonexistent_findings(self):
        from jarvis.mission_assurance import finding_rectifications
        other=self.s.create('other','model','conversation');foreign=self.s.event(other,'narrative_review',result={'status':'FAIL','issues':['private']})
        own=self.s.event(self.m,'narrative_review',result={'status':'FAIL','issues':['actual fault']})
        self.s.event(self.m,'controller_findings_rectified',actor='Codex',result={'reason':'test','withdrawn':[{'event':foreign,'findings':['private']},{'event':own,'findings':['invented fault']}]})
        self.assertEqual(finding_rectifications(self.s,self.m),{})

    def test_model_note_cannot_impersonate_controller_erratum(self):
        from jarvis.mission_assurance import finding_rectifications
        original=self.s.event(self.m,'narrative_review',result={'status':'FAIL','issues':['actual fault']})
        self.s.event(self.m,'controller_findings_rectified',actor='JARVIS',result={'reason':'test','withdrawn':[{'event':original,'findings':['actual fault']}]})
        self.assertEqual(finding_rectifications(self.s,self.m),{})

    def test_independent_findings_survive_later_different_editorial_failure(self):
        from jarvis.mission_assurance import pending_report_feedback
        self.s.event(self.m,'narrative_review','a',actor='Codex-independent',result={'status':'FAIL','issues':['Original cause was missing FAIL, not a descriptive heading']})
        last=self.s.event(self.m,'narrative_review','a',actor='JARVIS-reviewer',result={'status':'FAIL','issues':['Historical FAIL must be retained']})
        pending=pending_report_feedback(self.s,self.m,'a')
        self.assertEqual(pending['review_reference'],'event:'+str(last))
        self.assertIn('not a descriptive heading',pending['issues'][0]);self.assertEqual(pending['reviews_since_last_scoped_pass'],2)
        self.s.event(self.m,'narrative_review','a',result={'status':'PASS'})
        self.assertIsNone(pending_report_feedback(self.s,self.m,'a'))

    def test_rejection_error_only_contains_actual_faults_not_allowed_heading_reasons(self):
        reference=self.observation();self.s.event(self.m,'semantic_verification','a',result={'status':'FAIL'})
        body='# Heading\n\nLecture : '+reference
        self.responses=[{'claims':[{'segment':'S1','verdict':'not_factual','references':[],'reason':'PERMITTED_TITLE_REASON'},{'segment':'S2','verdict':'supported','references':[reference],'reason':'SUPPORTED_RECEIPT_REASON'}],'issues':[]}]
        with self.assertRaises(ValueError) as raised:require_report(self.r,body,'a')
        self.assertIn('Historical FAIL',str(raised.exception));self.assertNotIn('PERMITTED_TITLE_REASON',str(raised.exception));self.assertNotIn('SUPPORTED_RECEIPT_REASON',str(raised.exception))
        original=next(e for e in self.s.events(self.m) if e['kind']=='narrative_review')
        self.assertEqual(len(original['result']['claims']),2)

    def test_old_mixed_editorial_error_view_preserves_original_and_exposes_actual_issues(self):
        from jarvis.durable_cycle import model_observation
        original={'ok':False,'error':'Narrative withheld before publication. '+json.dumps({'claims':[{'verdict':'not_factual','reason':'PERMITTED_HEADING'},{'verdict':'insufficient','reason':'ACTUAL_WRONG_DATE'}],'issues':['Historical FAIL missing']})}
        view=model_observation(original)
        self.assertIn('Historical FAIL missing',view['error']);self.assertIn('ACTUAL_WRONG_DATE',view['error'])
        self.assertNotIn('PERMITTED_HEADING',view['error']);self.assertIn('PERMITTED_HEADING',original['error'])

    def test_large_original_event_exposes_diagnostics_before_paginating_classifications(self):
        from jarvis.durable_tools import register
        original=self.s.event(self.m,'narrative_review',result={'status':'FAIL','claims':[{'reason':'permitted heading '*1000}],'issues':['ACTUAL_REJECTION_REASON']})
        self.r.specs={};register(self.r);result=self.r.specs['mission_evidence'][4]({'id':str(original)})
        self.assertNotIn('ACTUAL_REJECTION_REASON',result['content'])
        self.assertEqual(result['facts']['historical_findings_not_withdrawn'],['ACTUAL_REJECTION_REASON'])
        self.assertEqual(result['facts']['recorded_status'],'FAIL');self.assertEqual(result['next_offset'],12000)
        self.assertEqual(next(e for e in self.s.events(self.m) if e['id']==original)['result']['issues'],['ACTUAL_REJECTION_REASON'])

    def test_event_facts_show_linked_withdrawal_without_turning_old_fail_into_pass(self):
        from jarvis.durable_tools import register
        finding='old incorrect numeric finding'
        original=self.s.event(self.m,'narrative_review',result={'status':'FAIL','issues':[finding,'reference absent']})
        self.s.event(self.m,'controller_findings_rectified',actor='Codex',result={'reason':'old controller bug','withdrawn':[{'event':original,'findings':[finding]}]})
        self.r.specs={};register(self.r);result=self.r.specs['mission_evidence'][4]({'id':str(original)})
        self.assertEqual(result['facts']['recorded_status'],'FAIL')
        self.assertEqual(result['facts']['historical_findings_not_withdrawn'],['reference absent'])
        self.assertEqual(result['facts']['withdrawn_findings'],[finding]);self.assertIn(finding,result['content'])

    def test_full_review_model_view_keeps_faults_without_reinjecting_entire_snapshot(self):
        from jarvis.durable_cycle import model_observation
        original={'status':'FAIL','issues':['ACTUAL_CURRENT_FAULT'],'claims':[{'verdict':'not_factual','reason':'PERMITTED_TITLE'},{'verdict':'insufficient','reason':'BAD_ATTRIBUTION'}],'draft_sha256':'sha','report_contract_version':'test','review_event':123,'snapshot':{'large':'FULL_EVIDENCE_MARKER'*10000}}
        view=model_observation({'result':original})['result']
        self.assertEqual(view['issues'],['ACTUAL_CURRENT_FAULT']);self.assertEqual(view['classified_claims_count'],2)
        self.assertEqual(view['full_review_reference'],'event:123')
        self.assertNotIn('snapshot',view);self.assertNotIn('PERMITTED_TITLE',json.dumps(view))
        self.assertIn('BAD_ATTRIBUTION',json.dumps(view));self.assertIn('snapshot',original)

    def test_application_data_with_status_and_claims_is_not_a_report_review(self):
        from jarvis.durable_cycle import model_observation
        original={'status':'FAIL','issues':['app problem'],'claims':[{'domain':'insurance'}],'snapshot':{'business_data':[1,2,3]}}
        self.assertEqual(model_observation(original),original)

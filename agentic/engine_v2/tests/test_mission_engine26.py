import json
from pathlib import Path
import tempfile
import unittest
from jarvis.mission_store import MissionStore
from jarvis.verification import evaluate, Verifier
from jarvis.mission_reporting import render_final, task_gate
from jarvis.mission_actions import register


def task(key='a'):
    return dict(id=key,title=key,depends=[],objective='fix',tools=['host_read_file'],observations=['exact JSON'],verification='read',recovery='diagnose',artifacts=['file'],contract={'report_path':'/report.md','semantic':[contract()]})


def contract():
    return {'kind':'json','source':{'tool':'host_read_file','arguments':{'path':'/a'}},'expected':{'/port':8091},'types':{'/port':'integer'}}


class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.store=MissionStore(self.tmp.name)
        self.m=self.store.create('raw goal','model','conv',spec={'autonomous':True})
        self.meta=dict(objective='raw goal',success_criteria=['correct'],artifacts=['file'],stop_conditions=['unavailable'])

    def test_plan_history_revision_and_received_immutable(self):
        self.store.plan(self.m,[task()],author='JARVIS',metadata=self.meta)
        t=task();t['recovery']='new diagnosis'
        with self.assertRaises(ValueError):self.store.plan(self.m,[t],metadata=self.meta)
        self.store.plan(self.m,[t,task('b')],author='JARVIS',metadata=self.meta,expected_version=1,reason='new observation')
        again=MissionStore(self.tmp.name)
        self.assertEqual([p['author'] for p in again.plans(self.m)],['JARVIS','JARVIS'])
        with again.db() as c:c.execute("UPDATE tasks SET state='validated' WHERE mission=? AND id='a'",(self.m,))
        with self.assertRaises(ValueError):again.plan(self.m,[task()],metadata=self.meta,expected_version=2)
        self.assertEqual(len(again.tasks(self.m)),2)

    def test_cycle_missing_dependency_and_owner_acceptance(self):
        a=task();a['depends']=['b']
        with self.assertRaises(ValueError):self.store.plan(self.m,[a],metadata=self.meta)
        with self.store.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'autonomous':True,'acceptance':[contract()]}),self.m))
        a=task();a['contract']={}
        with self.assertRaises(ValueError):self.store.plan(self.m,[a],metadata=self.meta)

    def test_semantic_false_success_types_preservation_and_insufficient(self):
        c=contract()
        self.assertEqual(evaluate('{"status":"ok","port":0}',c)['status'],'FAIL')
        c['expected']['/port']=1
        self.assertEqual(evaluate('{"port":true}',c)['status'],'FAIL')
        c['expected']['/port']=8091;c['preserve']=['/label']
        self.assertEqual(evaluate('{"port":8091,"label":"x"}',c,'{"label":"y"}')['status'],'FAIL')
        self.assertEqual(evaluate('{"port":8091}',c)['status'],'PARTIAL')
        self.assertEqual(evaluate('{"port":8091,"label":"x"}',c,'{"label":"x"}')['status'],'PASS')

    def registry(self):
        class Registry:
            pass
        r=Registry();r.specs={};r.context={'mission_id':self.m,'task_id':'a'};r.mission_store=self.store;r.calls=0
        def execute(name,args):
            r.calls+=1
            return {'ok':True,'result':{'stdout':'{"port":0,"status":"ok"}','returncode':0}}
        r.execute=execute
        return r

    def test_independent_read_and_failure_gate(self):
        r=self.registry();self.store.plan(self.m,[task()],author='JARVIS',metadata=self.meta)
        v=Verifier(r).verify(contract())
        self.assertEqual(v['status'],'FAIL');self.assertEqual(r.calls,1)
        self.assertEqual(len(self.store.observations(self.m)),1)
        with self.assertRaises(ValueError):task_gate(r,task(),{'tool':'mission_verify','result':{'result':v}})
        c=contract();c['source']={'tool':'host_exec','arguments':{'command':'echo status'}}
        self.assertEqual(Verifier(r).verify(c)['status'],'INSUFFICIENT')
        self.assertEqual(r.calls,1)

    def test_final_does_not_promote_model_false_claim(self):
        body=render_final(self.store,self.m,'Codex did nothing, 999 tests passed')
        self.assertNotIn('999 tests passed',body)
        self.assertIn('Codex',body)
        self.assertTrue(any(e['kind']=='report_facts_checked' for e in self.store.events(self.m)))

    def test_operation_replay_restart_conflict_and_unknown(self):
        r=self.registry();register(r)
        fn=r.specs['mission_action'][4]
        args={'operation_key':'once','tool':'host_write_file','arguments':'{"path":"/a","content":"test"}'}
        r.specs['host_write_file']=None
        first=fn(args);self.assertFalse(first['replayed'])
        r.mission_store=MissionStore(self.tmp.name)
        second=fn(args);self.assertTrue(second['replayed']);self.assertEqual(r.calls,1)
        with self.assertRaises(ValueError):fn({**args,'arguments':'{}'})
        with self.store.db() as c:c.execute("UPDATE mission_operations SET state='started',result=NULL WHERE key='once'")
        with self.assertRaises(ValueError):fn(args)
        self.assertEqual(r.calls,1)

    def test_append_preserves_received_task_and_metadata(self):
        self.store.plan(self.m,[task()],author='JARVIS',metadata=self.meta)
        with self.store.db() as c:c.execute("UPDATE tasks SET state='validated' WHERE mission=?",(self.m,))
        b=task('b');b['depends']=['a']
        self.store.plan(self.m,[b],author='JARVIS',expected_version=1,reason='new observation',append=True)
        versions=self.store.plans(self.m)
        self.assertEqual(versions[0]['plan']['tasks'][0],versions[1]['plan']['tasks'][0])
        self.assertEqual(versions[1]['plan']['objective'],'raw goal')
        self.assertEqual(self.store.tasks(self.m)[0]['state'],'validated')
        self.assertEqual([t['id'] for t in self.store.ready(self.m)],['b'])

    def test_unexecutable_contract_rejected_and_old_invalid_contract_repairable(self):
        bad=task();bad['contract']['semantic']=[{'kind':'text','source':contract()['source'],'expected':{}}]
        with self.assertRaises(ValueError):self.store.plan(self.m,[bad],metadata=self.meta)
        self.assertEqual(self.store.plans(self.m),[])
        # Simulate a historical declaration accepted by an older engine.
        legacy=self.store.create('legacy','model','conv')
        self.store.plan(legacy,[bad])
        with self.store.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'autonomous':True}),legacy))
        good=task()
        self.store.plan(legacy,[good],metadata=self.meta,expected_version=1,reason='repair invalid text predicate')
        self.assertEqual(len(self.store.plans(legacy)),2)

    def test_semantic_contract_object_allows_skill_parameter_substitution(self):
        from jarvis.verification import register as register_verification
        from jarvis.skill_lab import substitute
        r=self.registry();register_verification(r)
        c=contract();c['source']['arguments']['path']='${output_file}'
        expanded=substitute({'contract':c},{'output_file':'/a'})
        fn=r.specs['mission_verify'][4]
        self.assertEqual(fn(expanded)['status'],'FAIL')
        self.assertEqual(fn({'contract':json.dumps(expanded['contract'])})['status'],'FAIL')
        self.assertEqual(r.calls,2)

    def test_readable_result_with_unavailable_baseline_is_partial(self):
        r=self.registry()
        r.execute=lambda n,a: {'ok':True,'result':{'stdout':'{"port":8091,"label":"x"}'}} if a['path']=='/a' else {'ok':False,'error':'baseline unavailable'}
        c=contract();c['preserve']=['/label'];c['baseline_source']={'tool':'host_read_file','arguments':{'path':'/missing'}}
        verdict=Verifier(r).verify(c)
        self.assertEqual(verdict['status'],'PARTIAL')
        self.assertEqual(verdict['returncode'],1)
        self.assertTrue(any(check['pass'] for check in verdict['checks']))

    def test_patch_pending_task_keeps_received_task_and_history(self):
        self.store.plan(self.m,[task(),task('b')],metadata=self.meta)
        with self.store.db() as c:c.execute("UPDATE tasks SET state='validated' WHERE mission=? AND id='a'",(self.m,))
        b=task('b');b['recovery']='new diagnosis'
        self.store.plan(self.m,[b],author='JARVIS',patch=True,expected_version=1,reason='observed error')
        self.assertEqual([t['id'] for t in self.store.tasks(self.m)],['a','b'])
        self.assertEqual(self.store.tasks(self.m)[0]['state'],'validated')
        versions=self.store.plans(self.m)
        self.assertEqual(versions[0]['plan']['tasks'][0],versions[1]['plan']['tasks'][0])
        self.assertEqual(versions[1]['plan']['tasks'][1]['recovery'],'new diagnosis')

    def test_new_api_goals_default_to_autonomous_and_old_specs_remain_compatible(self):
        from jarvis.core import Core,ROOT
        from jarvis.memory import Memory
        from jarvis.missions import Missions
        memory=Memory(Path(self.tmp.name)/'runtime/memory.sqlite')
        config=json.loads((ROOT/'config/example.json').read_text())
        core=Core(config,memory,transport=lambda p:{'role':'assistant','content':''})
        controller=Missions(core,self.tmp.name,start_worker=False)
        new=controller.submit('raw objective',config['default_model'])
        self.assertTrue(json.loads(controller.store.get(new['id'])['spec'])['autonomous'])
        old=controller.submit('preplanned historical contract',config['default_model'],spec={'tasks':[{'id':'old','title':'old','depends':[]}]})
        self.assertNotIn('autonomous',json.loads(controller.store.get(old['id'])['spec']))
        self.assertEqual(controller.store.tasks(old['id'])[0]['id'],'old')

    def test_no_contract_weakening(self):
        self.store.plan(self.m,[task()],metadata=self.meta)
        t=task();t['contract']['semantic']=[]
        with self.assertRaises(ValueError):self.store.plan(self.m,[t],metadata=self.meta,expected_version=1)

    def test_corrupt_json_and_truncated_reads_not_pass(self):
        self.assertEqual(evaluate('{broken',contract())['status'],'FAIL')
        r=self.registry()
        r.execute=lambda n,a:{'ok':True,'result':{'stdout':'{"port":8091}', 'stdout_truncated':True}}
        self.assertEqual(Verifier(r).verify(contract())['status'],'INSUFFICIENT')

    def test_skill_semantic_verifier_false_success(self):
        from jarvis.skill_lab import SkillLab
        r=self.registry();r.root=Path(self.tmp.name)
        r.specs={'mission_verify':('',{'contract':{'type':'string'}},['contract'],'host_authorized',None)}
        r.execute=lambda n,a:{'ok':False,'result':{'returncode':1,'status':'FAIL'}}
        lab=SkillLab(r)
        m={'name':'semantic-check','description':'exact JSON','when':'repair', 'parameters':{'type':'object','additionalProperties':False},'requires_tools':['mission_verify'],'prerequisites':['readable'], 'steps':[{'tool':'mission_verify','arguments':{'contract':json.dumps(contract())},'verify':True}], 'on_error':'diagnose','changelog':'test'}
        lab.define(m)
        self.assertEqual(lab.execute('semantic-check',{},True)['state'],'failed')
        with self.assertRaises(ValueError):lab.activate('semantic-check',True)

    def test_service_state_and_github_content_not_envelope(self):
        r=self.registry()
        r.execute=lambda n,a:{'ok':True,'result':{'stdout':json.dumps({'path':'a','content':'{"port":8091}'})}}
        c=contract();c['source']={'tool':'host_github','arguments':{'action':'file','repo':'example'}}
        self.assertEqual(Verifier(r).verify(c)['status'],'PASS')
        self.assertEqual(evaluate('inactive\n',{'kind':'service','expected_state':'active'})['status'],'FAIL')

if __name__=='__main__':unittest.main()

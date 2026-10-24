import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from jarvis.core import Core
from jarvis.memory import Memory
from jarvis.mission_store import MissionStore


class Tools:
    def __init__(self):self.specs={'host_remote':None,'mission_plan':None};self.context={};self.executed=[]
    def schemas(self):return [{'type':'function','function':{'name':name,'parameters':{'type':'object','properties':{}}}} for name in self.specs]
    def execute(self,name,args):
        self.executed.append(name)
        if name=='mission_plan':return {'deferred':True,'mission_id':'unit-test-only'}
        return {'ok':True,'tool':name,'result':{'returncode':0},'risk':'host_authorized'}


class ScopedChatDelegation(unittest.TestCase):
    def make(self,responses):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);root=Path(tmp.name);identity=root/'identity.md';identity.write_text('Test identity')
        tools=Tools();payloads=[]
        def transport(payload):payloads.append(payload);return responses.pop(0)
        config={'models':['test-model'],'max_text_chars':10000,'history_messages':4,'identity_file':str(identity),'tool_rounds':2,'num_predict':256}
        with patch('jarvis.core.Registry',return_value=tools):core=Core(config,Memory(root/'memory.sqlite'),transport)
        return core,tools,payloads

    def test_explicit_subset_refuses_unoffered_plan_even_if_model_attempts_it(self):
        core,tools,payloads=self.make([{'tool_calls':[{'function':{'name':'mission_plan','arguments':{}}}]},{'tool_calls':[{'function':{'name':'host_remote','arguments':{'action':'project_exec'}}}]},{'content':'Terminé.'}])
        result=core.chat('Exécute une action host_remote ponctuelle.','test-model',allowed_tools=['host_remote'])
        self.assertEqual(tools.executed,['host_remote'])
        self.assertNotIn('mission_id',result)
        self.assertFalse(result['tools'][0]['ok'])
        self.assertEqual([s['function']['name'] for s in payloads[0]['tools']],['host_remote'])

    def test_default_promotion_unchanged_and_unknown_subset_rejected(self):
        core,tools,payloads=self.make([{'tool_calls':[{'function':{'name':'mission_plan','arguments':{}}}]}])
        with self.assertRaises(ValueError):core.chat('Test.','test-model',allowed_tools=['not_a_real_tool'])
        self.assertEqual(tools.executed,[])
        result=core.chat('Exécute la tâche.','test-model')
        self.assertEqual(result['mission_id'],'unit-test-only')
        self.assertEqual(tools.executed,['mission_plan'])

    def test_linked_continuation_reuses_existing_mission_and_records_real_calls(self):
        core,tools,payloads=self.make([{'tool_calls':[{'function':{'name':'host_remote','arguments':{'action':'project_exec'}}}]},{'content':'Terminé.'}])
        root=tempfile.TemporaryDirectory();self.addCleanup(root.cleanup);store=MissionStore(root.name)
        conversation=core.memory.conversation('test')
        mission=store.create('Existing objective','test-model',conversation)
        class Controller:
            def __init__(self):self.store=store
            def is_interrupted(self,ident):return self.store.get(ident)['state']=='interrupted'
        core.missions=Controller()
        with self.assertRaises(ValueError):core.chat('Exécute host_remote.','test-model',mission_id=mission,allowed_tools=['host_remote'])
        store.transition(mission,'waiting_external')
        with self.assertRaises(ValueError):core.chat('Exécute host_remote.','test-model',conversation='wrong',mission_id=mission,allowed_tools=['host_remote'])
        result=core.chat('Exécute host_remote.','test-model',mission_id=mission,allowed_tools=['host_remote'])
        calls=store.observations(mission)
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0]['tool'],'host_remote')
        self.assertTrue(calls[0]['result']['ok'])
        self.assertEqual(result['conversation'],conversation)
        self.assertEqual(tools.context['report_scope'],'directed_step')
        with store.db() as c:self.assertEqual(c.execute('select count(*) from missions').fetchone()[0],1)

    def test_linked_prose_without_tool_is_retried_and_never_received_as_execution(self):
        for executes in (False,True):
            responses=[{'content':'I claim the file was corrected.'}]
            responses += ([{'tool_calls':[{'function':{'name':'host_remote','arguments':{'action':'project_exec'}}}]},{'content':'Actual tool returned.'}] if executes else [{'content':'Still claiming success.'},{'content':'Done without any tool.'}])
            core,tools,payloads=self.make(responses)
            tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);store=MissionStore(tmp.name)
            conversation=core.memory.conversation('test');mission=store.create('Existing objective','test-model',conversation);store.transition(mission,'waiting_external')
            class Controller:
                def __init__(self):self.store=store
                def is_interrupted(self,ident):return False
            core.missions=Controller()
            result=core.chat('Perform the existing operation.','test-model',mission_id=mission,allowed_tools=['host_remote'])
            self.assertEqual(len(store.observations(mission)),1 if executes else 0)
            if executes:self.assertEqual(tools.executed,['host_remote'])
            else:self.assertIn('aucun outil opérationnel réussi',result['answer'])
            with store.db() as c:self.assertEqual(c.execute('select count(*) from missions').fetchone()[0],1)

    def test_internal_legacy_chat_with_mission_id_keeps_default_behavior(self):
        core,tools,payloads=self.make([{'content':'Réponse héritée.'}])
        class Controller:
            def is_interrupted(self,ident):return False
        core.missions=Controller()
        result=core.chat('Exécute une lecture.','test-model',mission_id='legacy-existing')
        self.assertEqual(result['answer'],'Réponse héritée.')

    def test_directed_step_report_does_not_overwrite_or_publish_mission_final(self):
        from jarvis.tools import Registry
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        registry=Registry.__new__(Registry);registry.root=Path(tmp.name);(registry.root/'runtime').mkdir();registry.context={'mission_id':'existing','report_scope':'directed_step'}
        class Store:
            def get(self,ident):raise AssertionError('Step report must not invoke final publication')
        class Controller:
            store=Store()
        registry.mission_controller=Controller()
        result=registry.report({'content':'Phase installation : données de test logiciel, aucune mission réelle.'})
        self.assertTrue(result['not_completed'])
        self.assertEqual(result['scope'],'directed_step')
        self.assertTrue(Path(result['path']).name.startswith('ETAPE-CONVERSATION-'))
        self.assertFalse((registry.root/'runtime/reports/existing/RAPPORT-FINAL.md').exists())

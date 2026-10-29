import importlib.util, pathlib, tempfile, unittest, json, io
from contextlib import redirect_stdout
from unittest.mock import patch, Mock
from jarvis.mission_store import MissionStore
spec=importlib.util.spec_from_file_location('periodic_codex',pathlib.Path(__file__).with_name('periodic_codex.py'))
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class CoordinationTests(unittest.TestCase):
 def test_normal_preparation_progress_does_not_trigger_authority_only_stall(self):
  with tempfile.TemporaryDirectory() as root:
   root=pathlib.Path(root);store=MissionStore(root);mission=store.create('fixture','model','conv');store.transition(mission,'running',progress=True)
   with store.db() as c:c.execute('UPDATE missions SET created=created-3600 WHERE id=?',(mission,))
   private=root/'private';private.mkdir();(private/'PROMPT.md').write_text('Software fixture, not an agent mission')
   registry=root/'registry.json';registry.write_text(json.dumps({'tasks':[{'id':'P4','mission_id':mission}]}))
   process=Mock(returncode=0);process.communicate.return_value=None
   config={'allowed_mission_ids':[mission],'normal_engine_progress':True}
   with patch.multiple(p,ROOT=str(root),PRIVATE=private,REGISTER=registry,REPO=str(root),ALLOWED_TASKS={'P4'},CONFIG=config),patch.object(p.subprocess,'Popen',return_value=process) as spawn,redirect_stdout(io.StringIO()):
    p.main();spawn.assert_not_called()
    self.assertEqual(json.loads((private/'STATE.json').read_text())['status'],'WATCHING_NO_INTERVENTION_NEEDED')
    config['normal_engine_progress']=False;p.main();self.assertEqual(spawn.call_count,1)

 def test_condition_key_ignores_result_and_new_session(self):
  with patch.object(p,'CONFIG',{'scope':'M26-P2'}):
   one=[{'task':'P2','mission':'same','condition':'proof-id','state':'interrupted','result':{'id':'first'}}]
   two=[{'task':'P2','mission':'same','condition':'proof-id','state':'waiting_external','result':{'id':'renamed'}}]
   self.assertEqual(p.condition_key(one),p.condition_key(two))
   two[0]['condition']='different-technical-cause';self.assertNotEqual(p.condition_key(one),p.condition_key(two))
 def test_three_passages_then_stop_survives_private_state_loss(self):
  with tempfile.TemporaryDirectory() as root:
   root=pathlib.Path(root);store=MissionStore(root);mission=store.create('fixture','model','conv');store.transition(mission,'interrupted')
   private=root/'private';private.mkdir();(private/'PROMPT.md').write_text('Unit fixture; process is mocked, not actual autonomy')
   registry=root/'registry.json';registry.write_text(json.dumps({'tasks':[{'id':'P2','mission_id':mission}]}))
   process=Mock(returncode=0);process.communicate.return_value=None
   with patch.multiple(p,ROOT=str(root),PRIVATE=private,REGISTER=registry,REPO=str(root),ALLOWED_TASKS={'P2'},CONFIG={'allowed_mission_ids':[mission]}),patch.object(p.subprocess,'Popen',return_value=process) as spawn,redirect_stdout(io.StringIO()):
    for _ in range(4):p.main()
    self.assertEqual(spawn.call_count,3);self.assertEqual(json.loads((private/'STATE.json').read_text())['status'],'COORDINATOR_BOUNDED_STOP')
    (private/'STATE.json').unlink();p.main();self.assertEqual(spawn.call_count,3)
   events=[e for e in store.events(mission) if e['kind']=='coordinator_periodic_started'];self.assertEqual([e['result']['attempt'] for e in events],[1,2,3]);self.assertEqual(len([e for e in store.events(mission) if e['kind']=='coordinator_bounded_stop']),1)
 def test_only_evidenced_technical_strategy_changes_coordination_identity(self):
  with tempfile.TemporaryDirectory() as root:
   store=MissionStore(root);mission=store.create('fixture','model','conv')
   observation=store.event(mission,'source_unit_observed',actor='Codex',result={'fixture':True})
   def event(actor='Codex',**changes):
    data={'verified':True,'evidence_events':[observation],'installed_modules':[{'file':'authority_draft.py','sha256':'a'*64}]};data.update(changes)
    return store.event(mission,'coordinator_strategy_verified',actor=actor,result=data)
   good=event();self.assertEqual(p.verified_strategy(store,mission,good),good)
   for bad in (event(actor='JARVIS'),event(evidence_events=[]),event(evidence_events=[999999]),event(installed_modules=[]),event(installed_modules=[{'file':'fake','sha256':'renamed'}])):
    self.assertIsNone(p.verified_strategy(store,mission,bad))
   with patch.object(p,'CONFIG',{'scope':'M26-P2'}):
    before=[{'task':'P3','mission':mission,'condition':'NO_PRODUCTIVE_EXECUTION'}]
    after=[{**before[0],'verified_strategy_event':good}]
    self.assertNotEqual(p.condition_key(before),p.condition_key(after))
 def test_out_of_scope_mission_is_never_dispatched(self):
  with tempfile.TemporaryDirectory() as root:
   root=pathlib.Path(root);store=MissionStore(root);mission=store.create('fixture','model','conv');store.transition(mission,'interrupted')
   private=root/'private';private.mkdir();registry=root/'registry.json';registry.write_text(json.dumps({'tasks':[{'id':'P2','mission_id':mission}]}))
   with patch.multiple(p,ROOT=str(root),PRIVATE=private,REGISTER=registry,REPO=str(root),ALLOWED_TASKS={'P2'},CONFIG={'allowed_mission_ids':['some-other-mission']}),patch.object(p.subprocess,'Popen') as spawn,redirect_stdout(io.StringIO()):
    p.main();spawn.assert_not_called()

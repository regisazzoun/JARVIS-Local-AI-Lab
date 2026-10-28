"""Real registry/store checks; not evidence of model autonomy."""
import json,tempfile,unittest
from pathlib import Path
from jarvis.tools import Registry
from jarvis.memory import Memory
from jarvis.mission_store import MissionStore
class ReportStepTests(unittest.TestCase):
 def test_citing_erratum_preserves_exact_validated_withdrawals(self):
  from jarvis.mission_assurance import cited_event_facts
  original=self.s.event(self.m,'narrative_review',result={'status':'FAIL','issues':['real defect','controller defect']})
  erratum=self.s.event(self.m,'controller_findings_rectified',actor='Codex-independent',result={
      'reason':'Controller defect withdrawn, original failure retained',
      'withdrawn':[{'event':original,'findings':['controller defect','invented finding']}]})
  facts=cited_event_facts(self.s,self.m,'event:'+str(erratum))[0]['facts']
  correction=facts['validated_rectifications'][0]
  self.assertEqual(correction['original_reference'],'event:'+str(original))
  self.assertEqual(correction['withdrawn_findings'],['controller defect'])
  self.assertEqual(correction['original_status_unchanged'],'FAIL')
  forged=self.s.event(self.m,'controller_findings_rectified',actor='JARVIS',result={
      'reason':'not authoritative','withdrawn':[{'event':original,'findings':['real defect']}]})
  self.assertEqual(cited_event_facts(self.s,self.m,'event:'+str(forged))[0]['facts']['validated_rectifications'],[])

 def test_executed_fail_returns_to_model_without_interface_escalation(self):
  from jarvis.core import Core
  from jarvis.missions import Missions
  identity=self.root/'identity.txt';identity.write_text('Full fixture identity')
  core=Core({'identity_file':str(identity),'durable_cycle_rounds':1,'num_ctx':32768},Memory(self.root/'runtime/memory.sqlite'))
  missions=Missions(core,self.root,start_worker=False,start_publisher=False)
  m=missions.store.create('Verify fixture','fixture','conv',spec={'bounded_interface_errors':True})
  missions.store.plan(m,[{'id':'a','title':'Verify','objective':'Check real outcome','tools':['mission_verify']}])
  def verify(args):
   verdict={'status':'FAIL','observations':[{'software_fixture':True}]}
   event=missions.store.event(m,'semantic_verification','a',result=verdict)
   return {'returncode':1,'verification_event':event,**verdict}
  old=missions.execution_core.tools.specs['mission_verify']
  missions.execution_core.tools.specs['mission_verify']=(*old[:4],verify)
  missions.execution_core.transport=lambda p:{'tool_calls':[{'function':{'name':'mission_verify','arguments':{'contract':{}}}}]}
  missions.cycle.run(missions.store.get(m))
  events=missions.store.events(m)
  self.assertTrue(any(e['kind']=='semantic_failure_returned_to_model' for e in events))
  self.assertFalse(any(e['kind'] in ('authority_interface_failure','authority_escalation') for e in events))
  self.assertEqual(missions.store.observations(m)[-1]['result']['result']['status'],'FAIL')
  self.assertNotEqual(missions.store.tasks(m)[0]['state'],'validated')

 def test_context_checkpoint_does_not_reinject_other_task_coordination(self):
  from jarvis.mission_context_budget import ContextBudget
  self.s.event(self.m,'coordinator_instruction',None,actor='Codex',result={'instruction':'GLOBAL owner scope'})
  self.s.event(self.m,'coordinator_instruction','previous-task',actor='Codex',result={'instruction':'VERIFY PREVIOUS REPORT ONLY'})
  counts=self.s.attempt_ledger(self.m).snapshot()
  _,checkpoint=ContextBudget(self.s,self.m,'a').checkpoint('Task boundary software fixture')
  self.assertEqual([x['result']['instruction'] for x in checkpoint['coordinator_instructions']],['GLOBAL owner scope'])
  self.assertEqual(counts,self.s.attempt_ledger(self.m).snapshot())
  self.assertTrue(any(e['task']=='previous-task' for e in self.s.events(self.m)))

 def test_recorded_insufficient_and_partial_results_are_not_interface_refusals(self):
  from jarvis.core import Core
  from jarvis.missions import Missions
  identity=self.root/'identity.txt';identity.write_text('Full fixture identity')
  for status in ('INSUFFICIENT','PARTIAL'):
   with self.subTest(status=status):
    core=Core({'identity_file':str(identity),'durable_cycle_rounds':1,'num_ctx':32768},Memory(self.root/'runtime/memory.sqlite'))
    missions=Missions(core,self.root,start_worker=False,start_publisher=False)
    m=missions.store.create('Verify fixture','fixture','conv',spec={'bounded_interface_errors':True})
    missions.store.plan(m,[{'id':'a','title':'Verify','objective':'Observe actual result','tools':['mission_verify']}])
    def verify(args):
     verdict={'status':status,'observations':[]}
     event=missions.store.event(m,'semantic_verification','a',result=verdict)
     return {'returncode':1,'verification_event':event,**verdict}
    old=missions.execution_core.tools.specs['mission_verify'];missions.execution_core.tools.specs['mission_verify']=(*old[:4],verify)
    missions.execution_core.transport=lambda p:{'tool_calls':[{'function':{'name':'mission_verify','arguments':{'contract':{}}}}]}
    missions.cycle.run(missions.store.get(m));events=missions.store.events(m)
    self.assertTrue(any(e['kind']=='semantic_result_returned_to_model' and e['result']['status']==status and not e['result'].get('test_executed') for e in events))
    self.assertFalse(any(e['kind'] in ('authority_interface_failure','authority_escalation') for e in events))
    self.assertNotEqual(missions.store.tasks(m)[0]['state'],'validated')

 def test_observed_facts_are_not_requested_again_without_explicit_tool_focus(self):
  from jarvis.core import Core
  from jarvis.missions import Missions
  self.assertTrue(self.save()['ok'])
  call=self.s.begin_call(self.m,'a','mission_report_facts',{})
  self.s.finish_call(call,{'ok':True,'result':{'scope_task':'a'}},0)
  identity=self.root/'identity.txt';identity.write_text('Full fixture identity')
  core=Core({'identity_file':str(identity),'durable_cycle_rounds':1,'num_ctx':32768},Memory(self.root/'runtime/memory.sqlite'))
  missions=Missions(core,self.root,start_worker=False,start_publisher=False);captured=[]
  def callback(payload):
   captured.append(payload)
   return {'tool_calls':[{'function':{'name':'mission_note','arguments':{'content':'Software fixture only'}}}]}
  missions.execution_core.transport=callback;missions.cycle.run(self.s.get(self.m))
  self.assertIn('déjà observée dans le journal',captured[-1]['messages'][0]['content'])
  names={t['function']['name'] for t in captured[-1]['tools']}
  self.assertNotIn('mission_report_facts',names);self.assertIn('host_write_file',names);self.assertIn('host_service',names)

 def test_original_service_fields_survive_later_notes_and_large_receipt_excerpt(self):
  from jarvis.mission_context_budget import ContextBudget
  from jarvis.mission_assurance import evidence_snapshot
  self.assertTrue(self.save()['ok'])
  body='Noise='+('x'*7000)+'\nMainPID=1234\nEnvironmentFiles=\nFragmentPath=/fixture.service\nActiveState=active\n'
  call=self.s.begin_call(self.m,'a','host_service',{'action':'show','service':'fixture.service'})
  self.s.finish_call(call,{'ok':True,'result':{'returncode':0,'stdout':body,'stdout_truncated':False}},0)
  for i in range(4):
   note=self.s.begin_call(self.m,'a','mission_note',{'content':str(i)});self.s.finish_call(note,{'ok':True,'result':{}},0)
  _,cp=ContextBudget(self.s,self.m,'a').checkpoint('Service source retention fixture')
  observed=cp['retained_service_observations'][0]
  self.assertEqual(observed['fields']['MainPID'],'1234');self.assertEqual(observed['fields']['EnvironmentFiles'],'')
  card=next(row for row in evidence_snapshot(self.s,self.m,'a')['receipts'] if row['reference']==call)
  self.assertEqual(card['observed_service_properties']['fields'],observed['fields'])
  self.assertNotIn('Noise',observed['fields'])

 def test_truncated_or_failed_service_read_cannot_prove_properties(self):
  from jarvis.mission_reporting import service_observation
  args={'action':'show','service':'fixture.service'}
  for wrapper in [{'ok':False,'result':{'returncode':0,'stdout':'MainPID=1234'}},{'ok':True,'result':{'returncode':1,'stdout':'MainPID=1234'}},{'ok':True,'result':{'returncode':0,'stdout':'MainPID=1234','stdout_truncated':True}}]:
   self.assertIsNone(service_observation(args,wrapper))

 def completed_report_write(self):
  from types import SimpleNamespace
  from jarvis.legacy_attempts import guarded
  self.assertTrue(self.save()['ok'])
  reg=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'a'})
  guarded(reg,'host_write_file',{'path':'/project/a.md','content':'Software fixture report'},lambda a:{'returncode':0,'evidence_id':'software-fixture-write'},True)
  return reg

 def test_pending_report_projection_requires_known_completed_matching_write(self):
  from jarvis.legacy_attempts import pending_report_validation
  import hashlib
  self.completed_report_write()
  p=pending_report_validation(self.s,self.m,'a');self.assertIsNotNone(p)
  self.assertEqual(p['expected_written_content_sha256'],hashlib.sha256(b'Software fixture report').hexdigest())
  self.assertEqual(p['verification_calls'],[{'contract':'active:0'}]);self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')
  self.assertIsNone(pending_report_validation(self.s,self.m,'other-task'))
  with self.s.db() as c:c.execute('UPDATE mission_attempts_v2 SET unknown_outcome=1 WHERE id=?',(p['attempt'],))
  self.assertIsNone(pending_report_validation(self.s,self.m,'a'))

 def test_actual_cycle_focuses_validation_then_restores_tools_after_observed_failure(self):
  from jarvis.core import Core
  from jarvis.missions import Missions
  from jarvis.legacy_attempts import settle,pending_report_validation
  reg=self.completed_report_write();identity=self.root/'identity.txt';identity.write_text('Full test identity')
  core=Core({'identity_file':str(identity),'durable_cycle_rounds':1,'num_ctx':32768},Memory(self.root/'runtime/memory.sqlite'))
  missions=Missions(core,self.root,start_worker=False,start_publisher=False);captured=[]
  def transport(payload):
   captured.append(payload)
   return {'tool_calls':[{'function':{'name':'mission_note','arguments':{'content':'Software fixture, not an actual model'}}}]}
  missions.execution_core.transport=transport;missions.cycle.run(self.s.get(self.m))
  names={t['function']['name'] for t in captured[-1]['tools']}
  self.assertIn('mission_verify',names);self.assertNotIn('host_write_file',names);self.assertNotIn('mission_plan_report_step',names)
  verdict={'status':'FAIL','contract':self.s.tasks(self.m)[0]['contract']['semantic'][0]}
  self.s.event(self.m,'semantic_verification','a',result=verdict);settle(reg,verdict)
  self.assertEqual(pending_report_validation(self.s,self.m,'a')['phase'],'correct')
  missions.cycle.run(self.s.get(self.m))
  names={t['function']['name'] for t in captured[-1]['tools']};self.assertIn('host_write_file',names);self.assertIn('host_read_file',names)
  self.assertNotIn('mission_plan_report_step',names);self.assertNotIn('host_service',names)
  read=self.s.import_observation(self.m,{'tool':'host_read_file','arguments':{'path':'/project/a.md'},'created':1,'result':{'ok':True,'result':{'returncode':0,'stdout':'Software fixture report','stdout_truncated':False}}})
  with self.s.db() as c:c.execute('UPDATE tool_calls SET task=? WHERE id=?',('a',read))
  missions.cycle.run(self.s.get(self.m))
  names={t['function']['name'] for t in captured[-1]['tools']}
  self.assertEqual(names,{'host_write_file','mission_verify','mission_evidence','mission_note'})
  attempt=self.s.attempt_ledger(self.m).snapshot()['attempts'][0]
  self.assertEqual(attempt['state'],'EXECUTED_TEST_FAILED');self.assertFalse(attempt['unknown_outcome'])

 def test_correction_keeps_exact_read_draft_without_confusing_old_or_truncated_content(self):
  from jarvis.legacy_attempts import settle,pending_report_validation
  reg=self.completed_report_write()
  settle(reg,{'status':'FAIL','contract':self.s.tasks(self.m)[0]['contract']['semantic'][0]})
  for content,truncated in [('old report',False),('Software fixture report',True),('Software fixture report',False)]:
   self.s.import_observation(self.m,{'tool':'host_read_file','arguments':{'path':'/project/a.md'},'created':1,'result':{'ok':True,'result':{'returncode':0,'stdout':content,'stdout_truncated':truncated}}})
   self.assertNotIn('observed_draft',pending_report_validation(self.s,self.m,'a'))
   # Imported historical reads carry no task, hence cannot satisfy this task's projection.
  with self.s.db() as c:c.execute('UPDATE tool_calls SET task=? WHERE mission=? AND tool=?',('a',self.m,'host_read_file'))
  value=pending_report_validation(self.s,self.m,'a')['observed_draft']
  self.assertEqual(value['content'],'Software fixture report')
  self.assertEqual(value['sha256'],pending_report_validation(self.s,self.m,'a')['expected_written_content_sha256'])

 def test_focused_writing_uses_observed_facts_then_restores_native_verification(self):
  from jarvis.core import Core
  from jarvis.missions import Missions
  from jarvis.legacy_attempts import guarded
  from types import SimpleNamespace
  self.assertTrue(self.save()['ok'])
  with self.s.db() as c:
   spec=json.loads(self.s.get(self.m)['spec']);spec['execution_tool_focus']={'a':['host_write_file','mission_note','mission_block']}
   c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  identity=self.root/'identity.txt';identity.write_text('Complete fixture identity')
  core=Core({'identity_file':str(identity),'durable_cycle_rounds':1,'num_ctx':32768},Memory(self.root/'runtime/memory.sqlite'))
  missions=Missions(core,self.root,start_worker=False,start_publisher=False);captured=[]
  missions.execution_core.transport=lambda payload:captured.append(payload) or {'tool_calls':[{'function':{'name':'mission_note','arguments':{'content':'Software fixture, no real model'}}}]}
  missions.cycle.run(self.s.get(self.m))
  self.assertIn('Consulte mission_report_facts avant de rédiger',captured[-1]['messages'][0]['content'])
  call=self.s.begin_call(self.m,'a','mission_report_facts',{});self.s.finish_call(call,{'ok':True,'result':{'software_fixture':True}},0)
  missions.cycle.run(self.s.get(self.m))
  self.assertNotIn('Consulte mission_report_facts avant de rédiger',captured[-1]['messages'][0]['content'])
  self.assertIn('déjà observée',captured[-1]['messages'][0]['content'])
  self.assertEqual({s['function']['name'] for s in captured[-1]['tools']},{'host_write_file','mission_note','mission_block'})
  reg=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'a'})
  guarded(reg,'host_write_file',{'path':'/project/a.md','content':'Software fixture report'},lambda a:{'returncode':0,'evidence_id':'fixture-write'},True)
  missions.cycle.run(self.s.get(self.m))
  names={s['function']['name'] for s in captured[-1]['tools']}
  self.assertIn('mission_verify',names);self.assertNotIn('host_write_file',names)
  from jarvis.legacy_attempts import settle
  settle(reg,{'status':'FAIL','contract':self.s.tasks(self.m)[0]['contract']['semantic'][0]})
  read=self.s.begin_call(self.m,'a','host_read_file',{'path':'/project/a.md'})
  self.s.finish_call(read,{'ok':True,'result':{'returncode':0,'stdout':'Software fixture report','stdout_truncated':False}},0)
  missions.cycle.run(self.s.get(self.m))
  self.assertEqual({s['function']['name'] for s in captured[-1]['tools']},{'host_write_file','mission_note','mission_block'})

 def test_resolved_escalation_exposes_known_failed_draft_without_erasing_history(self):
  import hashlib
  from jarvis.legacy_attempts import settle,pending_report_validation
  reg=self.completed_report_write();ledger=self.s.attempt_ledger(self.m)
  attempt=ledger.snapshot()['attempts'][0]
  with self.s.db() as c:c.execute('UPDATE mission_problems_v2 SET infra_incidents=2 WHERE mission=? AND fingerprint=?',(self.m,attempt['problem']))
  verdict={'status':'FAIL','contract':self.s.tasks(self.m)[0]['contract']['semantic'][0],'sha256':hashlib.sha256(b'Software fixture report').hexdigest()}
  settle(reg,verdict)
  self.assertEqual(ledger.get(attempt['id'])['state'],'ESCALATED')
  self.assertIsNone(pending_report_validation(self.s,self.m,'a'))
  call=self.s.begin_call(self.m,'a','host_read_file',{'path':'/project/a.md'})
  self.s.finish_call(call,{'ok':True,'result':{'returncode':0,'stdout':'Software fixture report','stdout_truncated':False}},0)
  with self.s.db() as c:c.execute("UPDATE mission_problems_v2 SET state='RESOLVED' WHERE mission=? AND fingerprint=?",(self.m,attempt['problem']))
  state=pending_report_validation(self.s,self.m,'a')
  self.assertEqual(state['phase'],'correct');self.assertEqual(state['observed_draft']['content'],'Software fixture report')
  self.assertTrue(state['resumed_after_coordinator_resolution']['old_failure_and_counts_unchanged'])
  self.assertEqual(ledger.get(attempt['id'])['state'],'ESCALATED')
  self.assertEqual(ledger.snapshot()['problems'][0]['infra_incidents'],3)
  with self.s.db() as c:c.execute('UPDATE mission_attempts_v2 SET unknown_outcome=1 WHERE id=?',(attempt['id'],))
  self.assertIsNone(pending_report_validation(self.s,self.m,'a'))

 def test_full_correction_draft_kept_while_old_unit_bodies_are_archived(self):
  from jarvis.legacy_attempts import guarded,settle
  from jarvis.mission_context_budget import ContextBudget
  from types import SimpleNamespace
  self.assertTrue(self.save()['ok']);body='Draft fixture. '*390
  reg=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'a'})
  guarded(reg,'host_write_file',{'path':'/project/a.md','content':body},lambda a:{'returncode':0,'evidence_id':'fixture-write'},True)
  settle(reg,{'status':'FAIL','contract':self.s.tasks(self.m)[0]['contract']['semantic'][0]})
  call=self.s.begin_call(self.m,'a','host_read_file',{'path':'/project/a.md'})
  self.s.finish_call(call,{'ok':True,'result':{'returncode':0,'stdout':body,'stdout_truncated':False}},0)
  sources=['/etc/systemd/system/jarvis-mission-worker.service','/etc/systemd/system/jarvis-mission-worker@.service']
  for path in sources:
   call=self.s.begin_call(self.m,'a','host_exec',{'command':'cat '+path})
   self.s.finish_call(call,{'ok':True,'result':{'returncode':0,'stdout':'[Service]\n'+'# source fixture\n'*200}},0)
  counts=self.s.attempt_ledger(self.m).snapshot()
  b=ContextBudget(self.s,self.m,'a')
  result=b.prepare({'model':'fixture','messages':[{'role':'system','content':'Complete policy'},{'role':'user','content':'old '*30000}],'options':{'num_predict':1024},'tools':[]},{'limit':13000})
  state=json.loads(result['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['pending_report_validation']['observed_draft']['content'],body)
  self.assertTrue(all('stdout' not in source for source in state['retained_unit_file_reads']))
  with self.s.db() as c:checkpoint=json.loads(c.execute('SELECT result FROM mission_events WHERE id=?',(state['unit_source_bodies_checkpoint'],)).fetchone()[0])['checkpoint']
  self.assertEqual(len(checkpoint['retained_unit_file_reads']),2)
  self.assertTrue(all(len(source['stdout'])>3000 for source in checkpoint['retained_unit_file_reads']))
  self.assertEqual(counts,self.s.attempt_ledger(self.m).snapshot())

 def test_complete_known_draft_over_6000_bytes_is_not_silently_dropped(self):
  from jarvis.legacy_attempts import guarded,settle,pending_report_validation
  from types import SimpleNamespace
  self.assertTrue(self.save()['ok']);body='x'*6400
  reg=SimpleNamespace(mission_store=self.s,context={'mission_id':self.m,'task_id':'a'})
  guarded(reg,'host_write_file',{'path':'/project/a.md','content':body},lambda a:{'returncode':0,'evidence_id':'fixture-write'},True)
  settle(reg,{'status':'FAIL','contract':self.s.tasks(self.m)[0]['contract']['semantic'][0]})
  call=self.s.begin_call(self.m,'a','host_read_file',{'path':'/project/a.md'})
  self.s.finish_call(call,{'ok':True,'result':{'returncode':0,'stdout':body,'stdout_truncated':False}},0)
  self.assertEqual(pending_report_validation(self.s,self.m,'a')['observed_draft']['content'],body)

 def test_completed_write_redirects_to_verification_without_reexposing_writer(self):
  from jarvis.core import Core
  from jarvis.missions import Missions
  self.completed_report_write();identity=self.root/'identity.txt';identity.write_text('Complete fixture identity')
  core=Core({'identity_file':str(identity),'durable_cycle_rounds':1,'num_ctx':32768},Memory(self.root/'runtime/memory.sqlite'))
  missions=Missions(core,self.root,start_worker=False,start_publisher=False);captured=[]
  def callback(payload):
   captured.append(payload)
   return {'tool_calls':[{'function':{'name':'host_write_file','arguments':{'path':'/project/a.md','content':'Unwanted duplicate fixture'}}}]}
  missions.execution_core.transport=callback;missions.cycle.run(self.s.get(self.m))
  self.assertIn('Prochaine action : mission_verify',captured[-1]['messages'][0]['content'])
  self.assertNotIn('Écris ton rapport',captured[-1]['messages'][0]['content'])
  result=self.s.observations(self.m,'a')[-1]['result']
  self.assertFalse(result['ok']);self.assertEqual(result['report_workflow_phase'],'verify')
  self.assertFalse(any(e['kind']=='execution_tool_discovered' for e in self.s.events(self.m)))
  self.assertEqual(len(self.s.attempt_ledger(self.m).snapshot()['attempts']),1)

 def test_withdrawn_controller_finding_requests_recheck_without_rewriting_or_erasing_failure(self):
  import hashlib
  from jarvis.legacy_attempts import settle,pending_report_validation
  reg=self.completed_report_write();sha=hashlib.sha256(b'Software fixture report').hexdigest();issue='Generic heading falsely requires its following table'
  review=self.s.event(self.m,'narrative_review','a',result={'status':'FAIL','draft_sha256':sha,'issues':[issue],'claims':[]})
  verdict={'status':'FAIL','sha256':sha,'contract':self.s.tasks(self.m)[0]['contract']['semantic'][0]}
  self.s.event(self.m,'semantic_verification','a',result=verdict);settle(reg,verdict)
  self.assertEqual(pending_report_validation(self.s,self.m,'a')['phase'],'correct')
  erratum=self.s.event(self.m,'controller_findings_rectified',actor='Codex-independent',result={'reason':'Observed structural-label controller defect','withdrawn':[{'event':review,'findings':[issue]}]})
  state=pending_report_validation(self.s,self.m,'a')
  self.assertEqual(state['phase'],'verify');self.assertEqual(state['review_feedback'] if 'review_feedback' in state else {},{})
  self.assertEqual(self.s.attempt_ledger(self.m).snapshot()['attempts'][0]['state'],'EXECUTED_TEST_FAILED')
  self.assertEqual(self.s.attempt_ledger(self.m).snapshot()['problems'][0]['infra_incidents'],1)

 def test_fresh_pass_can_complete_same_artifact_while_old_failed_attempt_stays_failed(self):
  import hashlib
  from jarvis.legacy_attempts import settle,pending_report_validation
  reg=self.completed_report_write();sha=hashlib.sha256(b'Software fixture report').hexdigest();contract=self.s.tasks(self.m)[0]['contract']['semantic'][0]
  failure={'status':'FAIL','sha256':sha,'contract':contract};self.s.event(self.m,'semantic_verification','a',result=failure);settle(reg,failure)
  write=self.s.begin_call(self.m,'a','host_write_file',{'path':'/project/a.md','content':'Software fixture report'});self.s.finish_call(write,{'ok':True,'result':{'returncode':0}},0)
  read=self.s.begin_call(self.m,'a','host_read_file',{'path':'/project/a.md'});self.s.finish_call(read,{'ok':True,'result':{'returncode':0,'stdout':'Software fixture report'}},0)
  success={'status':'PASS','sha256':sha,'contract':contract};event=self.s.event(self.m,'semantic_verification','a',result=success)
  call=self.s.begin_call(self.m,'a','mission_verify',{'contract':'active:0'});self.s.finish_call(call,{'ok':True,'result':{**success,'verification_event':event}},0)
  state=pending_report_validation(self.s,self.m,'a');self.assertEqual(state['phase'],'complete')
  self.assertEqual(state['completed_by_later_verification']['verification_event'],event)
  self.assertEqual(self.s.attempt_ledger(self.m).snapshot()['attempts'][0]['state'],'EXECUTED_TEST_FAILED')
  self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')

 def test_validation_instruction_survives_budget_compaction(self):
  from jarvis.mission_context_budget import ContextBudget
  self.completed_report_write()
  payload={'model':'fixture','messages':[{'role':'system','content':'Complete policy'},{'role':'user','content':'old '*30000}],'options':{'num_predict':1024},'tools':[]}
  result=ContextBudget(self.s,self.m,'a').prepare(payload,{'limit':16384})
  state=json.loads(result['messages'][1]['content']);state=state.get('operational_state',state)
  self.assertEqual(state['pending_report_validation']['report_path'],'/project/a.md')
  self.assertEqual(state['pending_report_validation']['verification_calls'],[{'contract':'active:0'}])
  self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')

 def test_pass_only_exposes_completion_and_newer_unknown_write_invalidates_old_focus(self):
  from jarvis.legacy_attempts import pending_report_validation,settle
  reg=self.completed_report_write()
  verdict={'status':'PASS','contract':self.s.tasks(self.m)[0]['contract']['semantic'][0]}
  self.s.event(self.m,'semantic_verification','a',result=verdict);settle(reg,verdict)
  self.assertEqual(pending_report_validation(self.s,self.m,'a')['phase'],'complete')
  self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')
  # A newer unknown write is a distinct software fixture state, not proof that
  # the previous PASS still describes the current file.
  with self.s.db() as c:
   row=dict(c.execute('SELECT * FROM mission_attempts_v2 WHERE mission=?',(self.m,)).fetchone())
   row.update(id='newer-unknown-fixture',operation_key='unknown',signature='newer',state='VALIDATION_INCONCLUSIVE',unknown_outcome=1,created=row['created']+1)
   c.execute('INSERT INTO mission_attempts_v2 ('+','.join(row)+') VALUES ('+','.join('?' for _ in row)+')',tuple(row.values()))
  self.assertIsNone(pending_report_validation(self.s,self.m,'a'))

 def test_corrective_feedback_keeps_reason_and_exact_controller_errata(self):
  from jarvis.legacy_attempts import pending_report_validation,settle
  import hashlib
  reg=self.completed_report_write();sha=hashlib.sha256(b'Software fixture report').hexdigest()
  wrong='Formatting is not a technical failure';quote='Long original statement '*40
  finding=quote+' => contradicted: Wrong actor'
  review=self.s.event(self.m,'narrative_review','a',result={'draft_sha256':sha,'status':'FAIL',
      'issues':['Historical FAIL must be retained',wrong,finding],
      'claims':[{'segment':'S2','quote':quote,'reason':'Wrong actor','verdict':'contradicted','references':['actor:Codex']}]})
  erratum=self.s.event(self.m,'controller_findings_rectified',actor='Codex',result={
      'withdrawn':[{'event':review,'findings':[wrong]}],'reason':'Formatting is not factual'})
  verdict={'status':'FAIL','sha256':sha,'contract':self.s.tasks(self.m)[0]['contract']['semantic'][0]}
  self.s.event(self.m,'semantic_verification','a',result=verdict);settle(reg,verdict)
  feedback=pending_report_validation(self.s,self.m,'a')['review_feedback']
  self.assertEqual(feedback['global_findings'],['Historical FAIL must be retained'])
  self.assertEqual(feedback['rejected_passages'][0]['reason'],'Wrong actor')
  self.assertTrue(feedback['rejected_passages'][0]['quote_is_excerpt'])
  self.assertEqual(feedback['erratum_reference'],'event:'+str(erratum))
  self.assertEqual(feedback['original_review_status'],'FAIL');self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')

 def test_execution_projection_keeps_identity_owner_goal_and_stored_criterion(self):
  from jarvis.core import Core
  from jarvis.missions import Missions
  identity=self.root/'identity.txt';identity.write_text('KEEP FULL IDENTITY AND OWNER AUTHORIZATION')
  core=Core({'identity_file':str(identity),'durable_cycle_rounds':1,'num_ctx':32768},Memory(self.root/'runtime/memory.sqlite'))
  missions=Missions(core,self.root,start_worker=False,start_publisher=False)
  m=missions.store.create('FULL OWNER OBJECTIVE; NO DEPLOYMENT','fixture','conv',spec={'planning_report_steps':True})
  criterion={'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/project/a.md'}}}
  missions.store.plan(m,[{'id':'a','title':'Observe and report','objective':'Read actual unit status','depends':[],'tools':['mission_note'],'contract':{'report_path':'/project/a.md','semantic':[criterion]}}])
  captured=[]
  def transport(payload):
   captured.append(payload)
   return {'tool_calls':[{'function':{'name':'mission_note','arguments':{'content':'Software fixture only'}}}]}
  missions.execution_core.transport=transport;missions.cycle.run(missions.store.get(m))
  self.assertTrue(captured[0]['messages'][0]['content'].startswith(identity.read_text()))
  self.assertIn('FULL OWNER OBJECTIVE; NO DEPLOYMENT',captured[0]['messages'][1]['content'])
  self.assertNotIn('mission_plan',[t['function']['name'] for t in captured[0]['tools']])
  self.assertEqual(missions.store.tasks(m)[0]['contract']['semantic'],[criterion])

 def test_saved_plan_is_not_reported_as_unexecuted_when_review_exceeds_budget(self):
  from unittest.mock import patch
  from jarvis.mission_context_budget import ContextCapacityError
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'autonomous':True,'planning_report_steps':True,'assurance':True}),self.m))
  with patch('jarvis.mission_assurance.audit_plan',side_effect=ContextCapacityError('oversized review fixture')):
   result=self.save()
  self.assertTrue(result['ok'],result);value=result['result']
  self.assertEqual(value['current_plan_version'],1);self.assertFalse(value['execution_allowed'])
  self.assertEqual(value['coverage']['status'],'INSUFFICIENT');self.assertTrue(value['coverage']['review_pending'])
  self.assertEqual(len(self.s.plans(self.m)),1);self.assertEqual(self.s.tasks(self.m)[0]['state'],'pending')
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.s=MissionStore(self.root);self.m=self.s.create('Observe and report','model','conv',spec={'autonomous':True,'planning_report_steps':True})
  self.r=Registry(Memory(self.root/'runtime/memory.sqlite'),self.root);self.r.mission_store=self.s;self.r.context={'mission_id':self.m}
  self.args={'id':'a','title':'Model chosen task','objective':'Observe real units','depends':[],'tools':['host_service','host_write_file'],'observations':['actual unit status'],'verification':'Review facts against service receipts','recovery':'Diagnose unavailable capability','artifacts':['/project/a.md'],'report_path':'/project/a.md','expected_version':0,'reason':'Initial model step','plan_objective':'Observe and report','plan_success_criteria':['Factual observation report'],'plan_artifacts':['/project/a.md'],'plan_stop_conditions':['Report verified']}
 def save(self,args=None):return self.r.execute('mission_plan_report_step',args or self.args)
 def test_flat_step_preserves_values_and_ordinary_semantic_predicate(self):
  result=self.save();self.assertTrue(result['ok'],result)
  t=self.s.tasks(self.m)[0];self.assertEqual(t['title'],self.args['title']);self.assertEqual(t['state'],'pending')
  self.assertEqual(t['contract'],{'report_path':'/project/a.md','semantic':[{'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/project/a.md'}}}]})
  self.assertFalse(self.s.contract_status(self.m,'a')['all_satisfied'])
  self.assertEqual(self.s.plans(self.m)[0]['author'],'JARVIS')
  self.assertNotIn('mission_plan',[s['function']['name'] for s in self.r.schemas()])
  self.assertIn('mission_plan_report_step',[s['function']['name'] for s in self.r.schemas()])
 def test_append_requires_current_version_and_cannot_change_received_task(self):
  self.assertTrue(self.save()['ok'])
  new={**self.args,'id':'b','depends':['a'],'expected_version':1,'report_path':'/project/b.md','artifacts':['/project/b.md']}
  self.assertTrue(self.save(new)['ok']);self.assertEqual(len(self.s.tasks(self.m)),2)
  self.assertFalse(self.save(new)['ok']);self.assertEqual(len(self.s.plans(self.m)),2)
  with self.s.db() as c:c.execute("UPDATE tasks SET state='validated' WHERE mission=? AND id='a'",(self.m,))
  self.assertFalse(self.save({**self.args,'title':'Weaken received','expected_version':2})['ok'])
  self.assertEqual(self.s.tasks(self.m)[0]['title'],self.args['title'])
 def test_opt_in_and_original_container_decode_keep_types(self):
  args={**self.args,'tools':json.dumps(self.args['tools'])};self.assertTrue(self.save(args)['ok'])
  self.assertIsInstance(self.s.plans(self.m)[0]['plan']['tasks'][0]['tools'],list)
  with self.s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps({'autonomous':True}),self.m))
  self.assertNotIn('mission_plan_report_step',[s['function']['name'] for s in self.r.schemas()])
  self.assertFalse(self.save({**self.args,'id':'c','expected_version':1})['ok']);self.assertEqual(len(self.s.plans(self.m)),1)

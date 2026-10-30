"""Proof-derived controls and exact-span batching, separate from live AI reception."""
import json,tempfile,unittest,copy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from jarvis.report_claims import segments,service_facts,deterministic_checks,scoped_evidence
from jarvis.mission_store import MissionStore
ROOT=Path(__file__).resolve().parents[3]

def snapshot():
 data=json.loads((ROOT/'docs/missions/DIAGNOSTIC-BOUCLES-IA/ENTREES-FACTEURS-RAPPORT.json').read_text())['facts'];rows=[]
 for row in data['is_active_receipts']:
  rows.append({'reference':row['invocation'],'actor':'JARVIS','executor':'broker','tool':'host_service','arguments':{'service':row['service'],'action':'is-active'},'ok':row['returncode']==0,'created':row['observed_at_iso'],'observed':{'returncode':row['returncode'],'stdout':row['observed_text']+'\n','duration_s':0.01,'evidence_id':'software-fixture','diagnostic':{'error_category':'application_error' if row['returncode'] else None}}})
 for row in data['status_receipts']:
  rows.append({'reference':row['reference'],'actor':'JARVIS','executor':'broker','tool':'host_service','arguments':row['parameters'],'ok':row['returncode']==0,'created':'2026-10-30T11:01:00+01:00','observed':{'returncode':row['returncode'],'stdout':'\n'.join(row['stdout_selected_original_lines']),'stderr':row['stderr'],'duration_s':0.01,'evidence_id':'software-fixture','diagnostic':{'error_category':'application_error' if row['returncode'] else None}}})
 return {'mission':'fixture','raw_goal':data['goal'],'receipts':rows,'semantic_verifications':[],'coverage_reviews':[],'report_failures':[], 'report_writes':[],'permission_context':{'invocation_id':data['service_snapshot_summary']['policy_invocation']},'counts':{'plans':0,'observations_in_scope':len(rows),'semantic_verdicts':{'FAIL':0,'PASS':0,'PARTIAL':0,'INSUFFICIENT':0}},'plans':[],'tasks':[],'created':'2026-10-30T09:00:00+01:00','infrastructure_author':'Codex','plan_and_operations_author':'JARVIS','active_contracts':{}}

class ReportClaimTests(unittest.TestCase):
 def test_four_actual_model_replays_are_rejected_without_a_second_model_opinion(self):
  rows=json.loads((ROOT/'docs/missions/DIAGNOSTIC-BOUCLES-IA/PREUVES-FACTEURS-RAPPORT.json').read_text())['rows']
  for row in rows:
   with self.subTest(row['variant']):
    text=json.loads(row['message']['content'])['report'];self.assertTrue(deterministic_checks(segments(text),snapshot()))
 def test_actual_latest_inverted_report_is_rejected(self):
  text=json.loads((ROOT/'docs/missions/DIAGNOSTIC-BOUCLES-IA/ENTREES-FACTEURS-RAPPORT.json').read_text())['previous_draft']
  self.assertIn('SYSTEMD_CODE_MEANING',{x['code'] for x in deterministic_checks(segments(text),snapshot())})
 def test_negation_history_and_raw_nonzero_output_are_not_false_code_claims(self):
  for text in ['Le code3 ne signifie pas une absence.','Le code3 indique non actif, pas une absence.','Le code4 indique une unité introuvable, pas simplement inactive.','Le précédent rapport indiquait à tort code3 signifie absent.','Sortie brute inactive, returncode=4.','Le code4 indique une unité introuvable, confirmé par status.']:
   self.assertFalse(deterministic_checks(segments(text),snapshot()),text)
 def test_absence_list_is_checked_against_loaded_unit_status(self):
  text='mdmonitor.service et systemd-networkd.service sont absentes ou masquées.'
  issues=deterministic_checks(segments(text),snapshot())
  self.assertTrue(any(x['code']=='UNIT_EXISTENCE_CONTRADICTION' and x['service']=='systemd-networkd.service' for x in issues))
 def test_free_prose_call_totals_and_wrong_timezone_are_checked(self):
  text='9 services actifs sur 8 appels is-active retournant 0.'
  self.assertIn('CALL_CODE_COUNT',{x['code'] for x in deterministic_checks(segments(text),snapshot())})
  text='Date des observations : 2026-10-30T09:49:33+02:00 à 2026-10-30T11:02:03+02:00.'
  self.assertIn('UNSUPPORTED_RECEIPT_TIME',{x['code'] for x in deterministic_checks(segments(text),snapshot())})
 def test_table_call_counts_and_named_return_codes_use_original_receipts(self):
  data=snapshot();row=copy.deepcopy(data['receipts'][0]);row['reference']='1'*32;data['receipts'].append(row)
  part='| Appels is-active réussis (rc=0) | 9 | état active |'
  self.assertIn('TABLE_CALL_COUNT',{x['code'] for x in deterministic_checks(segments(part),data)})
  part='| Appels is-active non actifs (rc=3) | 2 | mdmonitor.service, nvidia-persistenced.service |'
  self.assertIn('UNIT_RETURN_CODE',{x['code'] for x in deterministic_checks(segments(part),data)})
 def test_observation_time_and_functional_health_require_their_own_proof(self):
  text='Date de l’observation : 2026-10-30T11:02 UTC+02:00'
  self.assertIn('UNSUPPORTED_OBSERVATION_TIME',{x['code'] for x in deterministic_checks(segments(text),snapshot())})
  text='| jarvis-conversation.service | active | Fonctionnel |'
  self.assertIn('FUNCTIONALITY_UNPROVEN',{x['code'] for x in deterministic_checks(segments(text),snapshot())})
 def test_counts_preserve_negative_outputs_and_distinguish_calls_from_units(self):
  data=snapshot();facts=service_facts(data);self.assertEqual(facts['observed_units'],12);self.assertEqual(facts['stdout_counts'],{'active':9,'inactive':3})
  repeated=copy.deepcopy(data['receipts'][0]);repeated['reference']='1'*32;data['receipts'].append(repeated)
  issues=deterministic_checks(segments('12 appels à systemctl is-active ont été exécutés.'),data)
  self.assertIn('CALLS_VS_UNITS',{r['code'] for r in issues})
 def test_each_table_row_keeps_original_span_and_original_labels(self):
  text='## Services actifs\n\n| Service | Heure | Invocation |\n|---|---|---|\n'
  for row in snapshot()['receipts'][:12]:text+='| '+row['arguments']['service']+' | '+row['created']+' | '+row['reference']+' |\n'
  parts=segments(text);self.assertEqual(len([p for p in parts if p['text'].startswith('|')]),14)
  for part in parts:self.assertEqual(text[part['start']:part['end']],part['text'])
  self.assertEqual(parts[-1]['table_columns'],['Service','Heure','Invocation'])
 def test_one_row_does_not_receive_every_other_unit_or_a_huge_old_draft(self):
  data=snapshot();data['report_failures']=[{'reference':'event:'+str(i)} for i in range(5000)]
  row=data['receipts'][0];part=segments('| '+row['arguments']['service']+' | '+row['reference']+' |')
  view,refs=scoped_evidence(data,part)
  self.assertLess(len(view['receipts']),4);self.assertLess(len(json.dumps(view)),10000)
  self.assertEqual(view['report_history']['FAIL_reviews'],5000);self.assertEqual(len(view['report_history']['recent_references']),3)
  self.assertIn(row['reference'],refs)
 def test_timestamp_and_service_identity_are_checked_against_original_receipt(self):
  row=snapshot()['receipts'][0];text='| ssh.service | 2001-01-01T00:00:00+01:00 | '+row['reference']+' |'
  codes={r['code'] for r in deterministic_checks(segments(text),snapshot())};self.assertIn('WRONG_TIMESTAMP',codes);self.assertIn('WRONG_SERVICE_REFERENCE',codes)
 def test_count_in_enumerated_list_is_checked_even_without_global_scope_guess(self):
  text='Parmi ces services, 8 sont confirmés actifs : NetworkManager, jarvis-agent-proof, jarvis-conversation, jarvis-dell-desktop-gateway, jarvis-mission-worker, jarvis-mission-worker@2, jarvis-ollama, jarvis-open-webui, ssh.'
  self.assertIn('ENUMERATED_COUNT',{r['code'] for r in deterministic_checks(segments(text),snapshot())})
 def test_changed_table_returncode_and_unknown_ids_are_rejected(self):
  row=snapshot()['receipts'][0];text='| Service | Code | Invocation |\n|---|---|---|\n| '+row['arguments']['service']+' | 4 | '+row['reference']+' |\nRéférence '+('f'*32)
  codes={r['code'] for r in deterministic_checks(segments(text),snapshot())};self.assertIn('WRONG_RETURNCODE',codes);self.assertIn('UNKNOWN_RECEIPT',codes)
 def test_bad_report_fails_before_inference_and_unreviewed_claims_are_not_promoted(self):
  from jarvis.mission_assurance import audit_report
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv',spec={'atomic_report_review':True})
   registry=SimpleNamespace(mission_store=store,context={'mission_id':mission,'task_id':'a'},assurance_transport=lambda _:self.fail('Bad factual claim must fail without inference'))
   with patch('jarvis.mission_assurance.evidence_snapshot',return_value=snapshot()):result=audit_report(registry,'Le code3 signifie absent.','a')
   self.assertEqual(result['status'],'FAIL');self.assertTrue(result['unreviewed_segments']);self.assertEqual(result['claims'],[])
   self.assertEqual(result['author'],'JARVIS-engine')
 def test_cached_pass_cannot_bypass_current_deterministic_falsifiers(self):
  from jarvis.mission_assurance import audit_report
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv',spec={'atomic_report_review':True})
   registry=SimpleNamespace(mission_store=store,context={'mission_id':mission,'task_id':'a'},assurance_transport=lambda _:self.fail('No inference for exact contradiction'))
   with patch('jarvis.mission_assurance.evidence_snapshot',return_value=snapshot()):
    first=audit_report(registry,'Le code3 signifie absent.','a')
    store.event(mission,'narrative_review','a',result={**first,'status':'PASS'})
    again=audit_report(registry,'Le code3 signifie absent.','a')
   self.assertEqual(again['status'],'FAIL');self.assertNotIn('reused_verdict',again)
 def test_atomic_batches_cover_each_real_table_row_once_and_remain_small(self):
  from jarvis.mission_assurance import audit_report
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv',spec={'atomic_report_review':True})
   seen=[];sizes=[]
   def callback(payload):
    data=json.loads(payload['messages'][1]['content']);seen.extend(x['id'] for x in data['segments']);sizes.append(len(json.dumps(payload).encode()))
    return {'content':json.dumps({'claims':[{'segment':x['id'],'verdict':'supported','references':['services:snapshot'],'reason':'Software fixture only'} for x in data['segments']],'issues':[]})}
   registry=SimpleNamespace(mission_store=store,context={'mission_id':mission,'task_id':'a'},assurance_transport=callback)
   text='## Services observés\n\n| Service | Heure | Invocation |\n|---|---|---|\n'
   for row in snapshot()['receipts'][:12]:text+='| '+row['arguments']['service']+' | '+row['created']+' | '+row['reference']+' |\n'
   with patch('jarvis.mission_assurance.evidence_snapshot',return_value=snapshot()):result=audit_report(registry,text,'a')
   self.assertEqual(len(seen),len(set(seen)));self.assertEqual(len(seen),len(segments(text)));self.assertLess(max(sizes),27648)
   self.assertEqual(result['status'],'PASS');self.assertGreater(len(result['review_batches']),1)
 def test_clean_draft_keeps_goal_contract_counters_and_discards_old_prose(self):
  from jarvis.report_claims import drafting_state
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('Exact owner goal; no service changes','fixture','conv',spec={'read_only_service_snapshot':True})
   contract={'report_path':'/report.md','semantic':[{'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/report.md'}}}]}
   store.plan(mission,[{'id':'a','title':'Report','objective':'Exact task objective','contract':contract}])
   ref=store.begin_call(mission,'a','host_write_file',{'path':'/report.md','content':'POISONED_OLD_REPORT'})
   store.finish_call(ref,{'ok':True,'result':{'returncode':0}},0)
   before=store.attempt_ledger(mission).snapshot()
   data=drafting_state(store,mission,store.tasks(mission)[0],{'expected_written_content_sha256':'original-sha','attempt':'original-attempt','review_feedback':{'status':'FAIL','global_findings':['Wrong code interpretation']}},[])
   self.assertEqual(data['owner_goal'],'Exact owner goal; no service changes');self.assertEqual(data['active_task']['contract'],contract)
   self.assertNotIn('POISONED_OLD_REPORT',json.dumps(data));self.assertEqual(data['previous_draft']['sha256'],'original-sha')
   self.assertEqual(store.attempt_ledger(mission).snapshot(),before)

 def test_proof_composer_deduplicates_context_without_losing_contract_or_sources(self):
  from jarvis.report_claims import drafting_state
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('Exact owner goal','fixture','conv',spec={'proof_bound_report_write':True})
   contract={'report_path':'/report.md','semantic':[{'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/report.md'}}}]}
   store.plan(mission,[{'id':'a','title':'Report','objective':'All original criteria','contract':contract}])
   pending={'review_feedback':{'verification_event':42,'status':'FAIL','issue_count':2,'rejected_passages':[{'body':'HUGE_POISONED_DRAFT'*10000}]}}
   with patch('jarvis.mission_assurance.evidence_snapshot',return_value=snapshot()):state=drafting_state(store,mission,store.tasks(mission)[0],pending,[])
   self.assertEqual(state['owner_goal'],'Exact owner goal');self.assertEqual(state['active_task']['contract'],contract)
   self.assertEqual(state['facts']['receipts'],service_facts(snapshot())['latest']);self.assertEqual(state['current_findings']['verification_event'],42)
   self.assertNotIn('HUGE_POISONED_DRAFT',json.dumps(state));self.assertNotIn('raw_goal',state['facts'])
 def test_nonzero_return_count_is_not_confused_with_distinct_inactive_units(self):
  data=snapshot();repeated=copy.deepcopy(next(row for row in data['receipts'] if row['arguments']['action']=='is-active' and row['observed']['returncode']==4));repeated['reference']='2'*32;data['receipts'].append(repeated)
  facts=service_facts(data);self.assertEqual(facts['nonzero_units'],3);self.assertEqual(facts['nonzero_calls'],4)
  self.assertIn('RETURN_COUNT_SCOPE',{x['code'] for x in deterministic_checks(segments('Retours is-active ≠ 0 : 3.'),data)})
  self.assertFalse(deterministic_checks(segments('Retours is-active ≠ 0 : 4.'),data))

 def test_claimed_absence_is_rejected_by_actual_loaded_status(self):
  text='Deux unités absentes du système (mdmonitor.service, systemd-networkd.service).'
  found=deterministic_checks(segments(text),snapshot())
  self.assertTrue(any(x['code']=='UNIT_EXISTENCE_CONTRADICTION' and x['service']=='systemd-networkd.service' for x in found))
  self.assertFalse(deterministic_checks(segments('Une unité absente du système (mdmonitor.service).'),snapshot()))



class ReportRectificationTests(unittest.TestCase):
 def prepare(self,tmp):
  import hashlib,time
  from jarvis.attempt_ledger import encoded
  store=MissionStore(tmp);mission=store.create('report','fixture','conv');contract={'kind':'report','source':{'tool':'host_read_file','arguments':{'path':'/report.md'}}}
  store.plan(mission,[{'id':'r','title':'Report','deps':[],'objective':'facts','contract':{'report_path':'/report.md','semantic':[contract]}}])
  ledger=store.attempt_ledger(mission);problem=ledger.problem('report',{'criteria':[contract]});body='incorrect';sha=hashlib.sha256(body.encode()).hexdigest();old={'status':'PASS','sha256':sha,'verification_event':10}
  request={'task':'r','tool':'host_write_file','arguments':{'path':'/report.md','content':body}}
  with store.db() as c:
   c.execute("INSERT INTO mission_attempts_v2(id,mission,problem,operation_key,signature,executor,phase,request,state,result,created,updated) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",('attempt',mission,problem,'k','sig','broker','write',encoded(request),'SUCCESS',encoded({'verification':old,'change_observed':True}),time.time(),time.time()))
  store.transition(mission,'interrupted')
  verdict={'status':'FAIL','contract':contract,'sha256':sha,'observations':[{'invocation':'actual-read'}]}
  # Real store IDs can begin below a prior fixture ID, so retain ordering explicitly.
  for _ in range(11):store.event(mission,'fixture')
  event=store.event(mission,'semantic_verification','r',result=verdict)
  return store,mission,ledger,event,verdict
 def test_false_pass_rectified_same_bytes_once_without_resetting_totals(self):
  with tempfile.TemporaryDirectory() as tmp:
   store,mission,ledger,event,v=self.prepare(tmp)
   result=ledger.rectify_report_success('attempt',event)
   self.assertFalse(result['cached']);self.assertEqual(ledger.get('attempt')['state'],'EXECUTED_TEST_FAILED')
   self.assertEqual(ledger.get('attempt')['result']['original_success_result']['verification']['status'],'PASS')
   self.assertEqual(ledger.snapshot()['problems'][0]['failed_cycles'],1)
   self.assertTrue(ledger.rectify_report_success('attempt',event)['cached']);self.assertEqual(ledger.snapshot()['problems'][0]['failed_cycles'],1)
 def test_rectification_counter_recovers_after_interruption_between_event_and_count(self):
  with tempfile.TemporaryDirectory() as tmp:
   store,mission,ledger,event,v=self.prepare(tmp)
   with patch.object(ledger,'failure',side_effect=RuntimeError('Simulated process interruption')):
    with self.assertRaises(RuntimeError):ledger.rectify_report_success('attempt',event)
   self.assertEqual(ledger.get('attempt')['state'],'EXECUTED_TEST_FAILED');self.assertEqual(ledger.snapshot()['problems'][0]['failed_cycles'],0)
   self.assertTrue(ledger.rectify_report_success('attempt',event)['cached']);self.assertEqual(ledger.snapshot()['problems'][0]['failed_cycles'],1)
   ledger.rectify_report_success('attempt',event);self.assertEqual(ledger.snapshot()['problems'][0]['failed_cycles'],1)
 def test_reopening_rejects_another_report_hash_or_uninterrupted_mission(self):
  with tempfile.TemporaryDirectory() as tmp:
   store,mission,ledger,event,v=self.prepare(tmp);bad={**v,'sha256':'different'}
   other=store.event(mission,'semantic_verification','r',result=bad)
   with self.assertRaises(ValueError):ledger.rectify_report_success('attempt',other)
   store.transition(mission,'queued')
   with self.assertRaises(ValueError):ledger.rectify_report_success('attempt',event)

 def test_native_success_with_verification_event_references_is_rectified(self):
  from jarvis.attempt_ledger import encoded
  with tempfile.TemporaryDirectory() as tmp:
   store,mission,ledger,event,v=self.prepare(tmp)
   original=store.event(mission,'semantic_verification','r',result={**v,'status':'PASS'})
   newer=store.event(mission,'semantic_verification','r',result=v)
   row=ledger.get('attempt');result=row['result'];result.pop('verification');result['verification_events']=[original]
   with store.db() as c:c.execute('UPDATE mission_attempts_v2 SET result=? WHERE id=?',(encoded(result),'attempt'))
   self.assertFalse(ledger.rectify_report_success('attempt',newer)['cached'])
   self.assertEqual(ledger.snapshot()['problems'][0]['failed_cycles'],1)


class ProofBoundComposerTests(unittest.TestCase):
 def test_renderer_preserves_original_rows_counts_dates_and_model_explanation(self):
  from jarvis.report_claims import compose_evidence_report
  data=snapshot();refs=[r['reference'] for r in service_facts(data)['latest']]
  text=compose_evidence_report(data,refs,'Les observations décrivent des états systemd ; la santé applicative reste à vérifier.')
  self.assertFalse(deterministic_checks(segments(text),data))
  for r in service_facts(data)['latest']:self.assertIn(r['reference'],text)
  self.assertIn('rédigées par Qwen sur Dell1',text)
  self.assertIn('la santé applicative reste à vérifier.',text)
 def test_factual_fallback_is_explicit_and_later_reviews_do_not_stale_the_report(self):
  from jarvis.report_claims import compose_evidence_report
  data=snapshot();refs=[r['reference'] for r in service_facts(data)['latest']]
  before=compose_evidence_report(data,refs,'')
  data['report_review_status_counts']={'PASS':9,'FAIL':5};data['report_failures']=[{'reference':'event:999','issues':['later review']}]
  after=compose_evidence_report(data,refs,'')
  self.assertEqual(before,after);self.assertIn('aucune explication libre du modèle publiée',after)
  self.assertFalse(deterministic_checks(segments(after),data))
 def test_facts_only_verdict_requires_real_provenance_and_rejects_a_changed_report(self):
  import hashlib
  from jarvis.report_claims import compose_evidence_report,factual_render_verdict
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv')
   data=snapshot();refs=[r['reference'] for r in service_facts(data)['latest']];body=compose_evidence_report(data,refs,'')
   self.assertEqual(factual_render_verdict(store,mission,'a',body,data)['status'],'FAIL')
   store.event(mission,'proof_bound_report_prepared','a',result={'draft':body,'draft_sha256':hashlib.sha256(body.encode()).hexdigest(),'source_references':refs,'explanation':''})
   accepted=factual_render_verdict(store,mission,'a',body,data)
   self.assertEqual(accepted['status'],'PASS');self.assertFalse(accepted['semantic_model_used']);self.assertTrue(accepted['full_coverage'])
   self.assertEqual(factual_render_verdict(store,mission,'a',body+'Claim added.',data)['status'],'FAIL')
 def test_facts_only_path_does_not_substitute_a_model_opinion_for_exact_render_check(self):
  import hashlib
  from jarvis.mission_assurance import audit_report
  from jarvis.report_claims import compose_evidence_report
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv',spec={'atomic_report_review':True,'proof_bound_explanation_mode':'facts_only'})
   data=snapshot();refs=[r['reference'] for r in service_facts(data)['latest']];body=compose_evidence_report(data,refs,'')
   store.event(mission,'proof_bound_report_prepared','a',result={'draft':body,'draft_sha256':hashlib.sha256(body.encode()).hexdigest(),'source_references':refs,'explanation':''})
   registry=SimpleNamespace(mission_store=store,context={'mission_id':mission,'task_id':'a'},assurance_transport=lambda _:self.fail('Exact rendered facts need no model vote'))
   with patch('jarvis.mission_assurance.evidence_snapshot',return_value=data):result=audit_report(registry,body,'a')
   self.assertEqual(result['status'],'PASS');self.assertEqual(result['verification_method'],'broker-read+canonical-evidence-render')
 def test_renderer_rejects_incomplete_duplicate_or_unknown_source_selection(self):
  from jarvis.report_claims import compose_evidence_report
  data=snapshot();refs=[r['reference'] for r in service_facts(data)['latest']]
  for selected in [refs[:-1],refs+[refs[0]],refs[:-1]+['unknown']]:
   with self.assertRaises(ValueError):compose_evidence_report(data,selected,'Explanation')
 def test_accepted_composition_records_actual_child_write_and_requires_fresh_verification(self):
  from jarvis.report_claims import register_composer
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv')
   store.plan(mission,[{'id':'a','title':'Report','objective':'facts','contract':{'report_path':'/report.md'}}])
   calls=[]
   def write(name,args):calls.append((name,args));return {'ok':True,'result':{'returncode':0}}
   registry=SimpleNamespace(mission_store=store,context={'mission_id':mission,'task_id':'a'},specs={},execute=write)
   with patch('jarvis.mission_assurance.evidence_snapshot',return_value=snapshot()),patch('jarvis.mission_assurance.audit_report',return_value={'status':'PASS','review_event':42}):
    register_composer(registry);refs=[r['reference'] for r in service_facts(snapshot())['latest']]
    value=registry.specs['mission_report_compose'][4]({'references':refs,'explanation':'Les services sont observés aux instants des reçus.'})
   self.assertEqual(calls[0][0],'host_write_file');self.assertEqual(value['returncode'],0)
   self.assertEqual(store.observations(mission,'a')[-1]['arguments']['content'],calls[0][1]['content'])
   self.assertIn('mission_verify',value['next_action']);self.assertNotEqual(store.tasks(mission)[0]['state'],'validated')
 def test_interruption_during_review_prevents_late_write(self):
  from jarvis.report_claims import register_composer
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv')
   store.plan(mission,[{'id':'a','title':'Report','objective':'facts','contract':{'report_path':'/report.md'}}])
   registry=SimpleNamespace(mission_store=store,context={'mission_id':mission,'task_id':'a'},specs={},execute=lambda *_:self.fail('Interrupted review must not write'))
   def review(*args):store.transition(mission,'interrupted');return {'status':'PASS','review_event':42}
   with patch('jarvis.mission_assurance.evidence_snapshot',return_value=snapshot()),patch('jarvis.mission_assurance.audit_report',side_effect=review):
    register_composer(registry);refs=[r['reference'] for r in service_facts(snapshot())['latest']]
    result=registry.specs['mission_report_compose'][4]({'references':refs,'explanation':'Lecture des états.'})
   self.assertTrue(result['known_not_executed']);self.assertTrue(result['publication_withheld'])
 def test_commentary_cannot_rewrite_numeric_facts_or_bypass_factual_renderer(self):
  from jarvis.report_claims import register_composer
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv')
   store.plan(mission,[{'id':'a','title':'Report','objective':'facts','contract':{'report_path':'/report.md'}}])
   registry=SimpleNamespace(mission_store=store,context={'mission_id':mission,'task_id':'a'},specs={},execute=lambda *_:self.fail('Numeric commentary must not write'))
   with patch('jarvis.mission_assurance.evidence_snapshot',return_value=snapshot()):
    register_composer(registry);refs=[r['reference'] for r in service_facts(snapshot())['latest']]
    for text in ['Les 12 services sont actifs.','Deux unités sont absentes.','Codes de retour ₀.']:
     result=registry.specs['mission_report_compose'][4]({'references':refs,'explanation':text})
     self.assertTrue(result['known_not_executed']);self.assertTrue(result['publication_withheld'])
 def test_clean_context_retains_latest_format_and_composer_refusals(self):
  from jarvis.report_claims import drafting_feedback
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv')
   event=store.event(mission,'structured_action_rejected','a',result={'error':'Structured action does not match offered tool schema: arguments/explanation: pattern rejected','model_output':{'content':'POISONED_FULL_REJECTED_DRAFT'}})
   token=store.begin_call(mission,'a','mission_report_compose',{})
   store.finish_call(token,{'ok':False,'result':{'reason':'Do not repeat numeric assertions','publication_withheld':True}},0)
   state=drafting_feedback(store,mission,'a')
   self.assertEqual(state['last_format_refusal']['reference'],'event:'+str(event));self.assertIn('pattern',state['last_format_refusal']['constraint']);self.assertTrue(state['last_composition']['publication_withheld'])
   self.assertNotIn('POISONED_FULL_REJECTED_DRAFT',json.dumps(state))
 def test_root_schema_refusal_preserves_unexpected_field_names(self):
  from jarvis.report_claims import drafting_feedback
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv')
   store.event(mission,'structured_action_rejected','a',result={'error':"Structured action does not match offered tool schema: arguments: additionalProperties Additional properties are not allowed ('report_path' was unexpected)"})
   feedback=drafting_feedback(store,mission,'a')['last_format_refusal']
   self.assertEqual(feedback['constraint'],'arguments: additionalProperties');self.assertIn('report_path',feedback['detail'])
 def test_invalid_explanation_is_archived_and_withheld_without_broker_write(self):
  from jarvis.report_claims import register_composer
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv',spec={'atomic_report_review':True})
   store.plan(mission,[{'id':'a','title':'Report','objective':'facts','contract':{'report_path':'/report.md'}}])
   registry=SimpleNamespace(mission_store=store,context={'mission_id':mission,'task_id':'a'},specs={},assurance_transport=lambda _:self.fail('Closed contradiction needs no model'),execute=lambda *_:self.fail('Unreviewed prose must never be written'))
   with patch('jarvis.mission_assurance.evidence_snapshot',return_value=snapshot()):
    register_composer(registry);refs=[r['reference'] for r in service_facts(snapshot())['latest']]
    value=registry.specs['mission_report_compose'][4]({'references':refs,'explanation':'systemd-networkd.service est absente.'})
   self.assertTrue(value['publication_withheld']);self.assertEqual(value['returncode'],1)
   self.assertTrue(any(e['kind']=='proof_bound_report_prepared' for e in store.events(mission)))

class FinalFactualPublicationTests(unittest.TestCase):
 def test_unverified_global_model_prose_is_archived_but_never_appended_to_factual_publication(self):
  from jarvis.tools import Registry
  with tempfile.TemporaryDirectory() as tmp:
   store=MissionStore(tmp);mission=store.create('services','fixture','conv',spec={'assurance':True,'proof_bound_report_write':True,'proof_bound_explanation_mode':'facts_only'})
   store.plan(mission,[{'id':'a','title':'Report','objective':'facts','contract':{}}])
   with store.db() as c:
    c.execute("UPDATE tasks SET state='validated' WHERE mission=?",(mission,))
    spec=json.loads(store.get(mission)['spec']);spec['autonomous']=True;c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),mission))
   store.event(mission,'semantic_verification','a',result={'status':'FAIL','contract':{'kind':'report'}})
   reg=Registry.__new__(Registry);reg.mission_store=store;reg.root=Path(tmp);reg.context={'mission_id':mission}
   with patch('jarvis.mission_assurance.require_final_outcome',return_value={'final_allowed':True}),patch('jarvis.mission_assurance.require_report',side_effect=AssertionError('Free prose is not submitted as the factual report')):
    result=reg.report({'content':'FALSE_FREE_MODEL_CLAIM'})
   published=Path(result['path']).read_text();self.assertNotIn('FALSE_FREE_MODEL_CLAIM',published);self.assertIn('Mode FACTS_ONLY',published);self.assertIn('No observations field in original historical event',published)
   original=next(e for e in store.events(mission) if e['kind']=='model_report_original');self.assertEqual(original['result']['content'],'FALSE_FREE_MODEL_CLAIM')
   proof=next(e for e in store.events(mission) if e['kind']=='factual_final_publication');self.assertFalse(proof['result']['model_prose_published'])

if __name__=='__main__':unittest.main()

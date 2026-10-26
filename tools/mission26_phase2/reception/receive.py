"""Independent Codex receipt checks; never convert a model report into evidence."""
import sys,json,time,shlex
from pathlib import Path
sys.path.insert(0,'/opt/jarvis/conversation')
from jarvis.mission_store import MissionStore
from jarvis.attempt_ledger import AttemptLedger
from jarvis.host_client import request
from control import MISSION,assign
STORE=MissionStore('/opt/jarvis/conversation')
def remote(host,code):
 args={'host':{'Dell1':'dell-observe','Dell2':'dell2'}[host],'action':'project_exec','project':'mission26-phase2','command':'python3 -c '+shlex.quote(code)}
 r=request('host_remote',args,workload_class='mission');assert r['ok'] and r['result']['returncode']==0,r
 return r['result']['stdout'],r['evidence_id']
def filejson(host,path):
 out,receipt=remote(host,'from pathlib import Path; print(Path('+repr(path)+').read_text())');return json.loads(out),receipt
def rows(case):
 with STORE.db() as c:
  p=dict(c.execute('SELECT * FROM mission_problems_v2 WHERE mission=? AND scope=?',(MISSION,'M26-P2-reception/'+case)).fetchone())
  a=[dict(r) for r in c.execute('SELECT * FROM mission_attempts_v2 WHERE mission=? AND problem=? ORDER BY created,id',(MISSION,p['fingerprint']))]
 return p,a
def wait():
 end=time.monotonic()+240
 while time.monotonic()<end:
  state=STORE.get(MISSION)['state']
  if state=='waiting_external':return
  if state in ('interrupted','failed'):raise RuntimeError('Reception worker stopped: '+state)
  time.sleep(0.75)
 raise RuntimeError('No scenario result after240s; diagnose, do not repeat blindly')
def verify(case):
 evidence={'case':case,'verifier':'Codex','status':'VALIDÉ','no_model_report_used_as_proof':True};events=STORE.events(MISSION,limit=100000)
 if case in ('S01','S02','S03','S04','S05','S06'):
  p,a=rows(case);assert len(a)==1,(case,len(a));r=a[0];result=json.loads(r['result']);evidence.update(attempt=r['id'],executor=r['executor'],state=r['state'],failed_cycles=p['failed_cycles'],infra_incidents=p['infra_incidents'])
  expected={'S01':'SUCCESS','S02':'EXECUTED_TEST_FAILED','S03':'NOT_EXECUTED','S04':'NOT_EXECUTED','S05':'VALIDATION_INCONCLUSIVE','S06':'VALIDATION_INCONCLUSIVE'}[case];assert r['state']==expected,(case,r['state'],result)
  chain=[e['result']['state'] for e in events if e['kind']=='p2_attempt_transition' and e['result'].get('attempt')==r['id']];evidence['observed_states']=chain
  assert chain[:2]==['PENDING','DISPATCHED'],chain
  if case=='S01':
   assert 'RUNNING' in chain and result['verified'] and result['returncode']==0
   data,receipt=filejson(r['executor'],'reception/S01.json');assert data['status']=='ready' and type(data['value']) is int and data['value']==17,data;evidence.update(artifact=data,independent_receipt=receipt)
  if case=='S02':assert 'RUNNING' in chain and result['returncode']!=0 and 'AssertionError' in result['execution']['stderr']
  if case in ('S03','S04'):
   assert 'RUNNING' not in chain and p['failed_cycles']==0 and p['infra_incidents']==1
   out,receipt=remote(r['executor'],"from pathlib import Path; import json; print(json.dumps({'marker':Path("+repr('.p2-reception/'+r['id']+'.started.json')+").exists(),'artifact':Path("+repr('reception/forbidden-'+case+'.txt')+").exists()}))")
   assert json.loads(out)=={'marker':False,'artifact':False},out;evidence['independent_receipt']=receipt
   if case=='S04':
    stopped=[e for e in events if e['kind']=='p2_worker_channel_stopped' and e['result'].get('attempt')==r['id']];assert stopped and stopped[-1]['result']['actual_listener_closed'];evidence['real_channel_stop_event']=stopped[-1]['id'];evidence['scope_note']='Real stopped delegated reception channel; production Dell/SSH/broker stayed available'
  if case=='S05':
   assert r['unknown_outcome'] and p['failed_cycles']==0
   loss=[e for e in events if e['kind']=='p2_fault_injection' and e['result'].get('attempt')==r['id']];assert loss and loss[-1]['result'].get('receipt_sha256');evidence['real_response_drop_event']=loss[-1]['id']
   ledger=AttemptLedger(STORE,MISSION);before=len(ledger.snapshot()['attempts']);blocked=ledger.begin(p['fingerprint'],'new-alias-before-observation','Dell2','execute',{'command':'different command after lost response'})
   assert blocked.get('requires_observation') and blocked['attempt']==r['id'];assert len(ledger.snapshot()['attempts'])==before;evidence['independent_duplicate_guard']=blocked
  if case=='S06':
   assert not r['unknown_outcome'] and result['returncode']==0 and not result['verified'];assert result['verification']['verdict']=='INSUFFICIENT' and 'PermissionError' in result['verification'].get('reason',''),result
   out,receipt=remote(r['executor'],"import pathlib,json; p=pathlib.Path('reception/S06.txt'); print(json.dumps({'mode':p.stat().st_mode & 0o777}))");assert json.loads(out)['mode']==0;evidence['independent_receipt']=receipt
 elif case in ('S07','S08','S10'):
  p,a=rows('S07');assert p['failed_cycles']==3 and p['state']=='ESCALATED' and len(a)==3,(p,len(a));evidence.update(problem=p['fingerprint'],failed_cycles=3,attempts=[r['id'] for r in a],escalation_event=p['escalation_event'])
  for row in a:
   value=json.loads(row['result']);assert (value['returncode']!=0 or value.get('verification_semantic',{}).get('status')=='FAIL' or value.get('verification_execution',{}).get('returncode',0)!=0) and value['failure_counted']
   proof=[e for e in events if e['kind']=='p2_result_observed' and e['result'].get('attempt')==row['id']][-1]
   assert proof['result']['receipt']['correction_before']!=proof['result']['receipt']['correction_after']
  if case=='S08':
   status=[e for e in events if e['kind']=='p2_scenario_status' and e['result'].get('case')=='S08'];assert status
   ack=STORE.event(MISSION,'p2_codex_acknowledgment',actor='Codex',result={'escalation_event':p['escalation_event'],'three_attempts':[r['id'] for r in a],'decision':'Leave this negative-test problem blocked; continue independent restart/recovery case, no fourth correction'})
   evidence['actual_codex_ack_event']=ack
  if case=='S10':
   rejected=[e for e in events if e['kind']=='p2_attempt_rejected' and e['result'].get('problem')==p['fingerprint']];assert rejected
   totals=[]
   for host in ('Dell1','Dell2'):
    code="import pathlib,json; p=pathlib.Path('.p2-reception/executions.jsonl'); rows=[json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []; print(json.dumps({'attempts':[r['attempt'] for r in rows if r['problem']=="+repr(p['fingerprint'])+"],'forbidden':pathlib.Path('reception/forbidden-fourth.txt').exists()}))"
    out,receipt=remote(host,code);data=json.loads(out);assert not data['forbidden'];totals+=data['attempts'];evidence.setdefault('independent_receipts',[]).append(receipt)
   assert sorted(totals)==sorted(r['id'] for r in a),totals;evidence['executions_after_renamed_fourth_request']=len(totals)
 elif case=='S09':
  resumed=[e for e in events if e['kind']=='p2_restart_observed' and e['result'].get('same_ledger') and e['result'].get('new_worker_process')];assert resumed and resumed[-1]['result']['same_ledger'] and resumed[-1]['result']['new_worker_process'];evidence['native_resume_event']=resumed[-1]['id']
  p,a=rows('S05');r=a[0];assert r['state']=='SUCCESS' and not r['unknown_outcome'];data,receipt=filejson(r['executor'],'reception/S05.json');assert data['status']=='ready' and data['value']==23
  out,count_receipt=remote(r['executor'],"from pathlib import Path; print(Path('reception/S05-count.txt').read_text())");assert int(out.strip())==1,out
  repairs=[e for e in events if e['kind']=='p2_codex_verification_repair' and e['result'].get('attempt')==r['id']]
  evidence.update(recovered_attempt=r['id'],actual_execution_count=1,independent_receipts=[receipt,count_receipt],initial_restart_event=resumed[-1]['result'].get('reused_initial_restart_observation',resumed[-1]['id']))
  if repairs:evidence.update(status='VALIDÉ AVEC RÉSERVES',verification_actor='Codex',codex_repair_event=repairs[-1]['id'],reservation='JARVIS resumed and read the result; Codex repaired semantic verification after three inconclusive or malformed verifiers')
 else:raise ValueError(case)
 event=STORE.event(MISSION,'p2_independent_case_reception',actor='Codex',result=evidence);evidence['reception_event']=event
 folder=Path('/home/adminjarvis/JARVIS/mission26-phase2/docs/missions/26-P2/reception');folder.mkdir(exist_ok=True);(folder/(case+'.json')).write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
 print(case,'VALIDÉ','event',event,flush=True);return evidence
if __name__=='__main__':
 mode=sys.argv[1]
 if mode=='first8':
  wait();verify('S01')
  for i in range(2,9):
   case='S'+str(i).zfill(2);assign(case);wait();verify(case)
 elif mode=='verify':wait();verify(sys.argv[2])

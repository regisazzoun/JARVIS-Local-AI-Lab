"""Explicit Codex escalation repair: observe artifacts; never replay S05 action.
Not an autonomous fourth verifier. Original three failures remain canonical.
"""
import sys,json,hashlib
sys.path.insert(0,'/opt/jarvis/conversation')
from jarvis.attempt_execution import AttemptExecutor
from jarvis.verification import evaluate
from receive import STORE,MISSION,rows,remote

def repair():
 events=STORE.events(MISSION,limit=100000)
 assert STORE.get(MISSION)['state']=='interrupted'
 assert any(e['kind']=='p2_reception_escalation' and e['result'].get('case')=='S09' for e in events)
 _,attempts=rows('S05');attempt=attempts[0]['id'];runner=AttemptExecutor(STORE,MISSION);row=runner.ledger.get(attempt)
 dispatched=[e for e in events if e['kind']=='p2_verification_dispatched' and e['result'].get('attempt')==attempt]
 assert len(dispatched)==3
 assert row['state'] in ('VALIDATION_INCONCLUSIVE','RUNNING')
 receipt,proof=runner.read(row,'result')
 injected=[e for e in events if e['kind']=='p2_fault_injection' and e['result'].get('attempt')==attempt][-1]
 assert hashlib.sha256(json.dumps(receipt).encode()).hexdigest()==injected['result']['receipt_sha256']
 code="import json,pathlib; print(json.dumps({'count':int(pathlib.Path('reception/S05-count.txt').read_text()),'artifact':json.loads(pathlib.Path('reception/S05.json').read_text())}))"
 out,broker=remote(row['executor'],code)
 semantic=evaluate(out,{'kind':'json','expected':{'/count':1,'/artifact/status':'ready','/artifact/value':23},'types':{'/count':'integer','/artifact/value':'integer'}})
 assert semantic['status']=='PASS',semantic
 repair=STORE.event(MISSION,'p2_codex_verification_repair',actor='Codex',result={'attempt':attempt,'original_verifier_attempts':[e['id'] for e in dispatched],'escalation_required':True,'method':'independent structured JSON observation with existing semantic evaluator; no model shell retry','broker_evidence':broker,'observed':json.loads(out),'semantic':semantic,'original_execution_not_repeated':True})
 result={'returncode':receipt['execution']['returncode'],'started':receipt['start'],'execution':receipt['execution'],'verified':True,'verification_semantic':semantic,'verification_actor':'Codex','verification_repair_event':repair,'verification_broker_evidence':broker,'transport_evidence':proof}
 evidence=STORE.event(MISSION,'p2_result_observed',actor='Codex',result={'attempt':attempt,'receipt':receipt,'observation':result,'state':'SUCCESS','post_escalation_assistance':True})
 runner.ledger.transition(attempt,'SUCCESS',evidence=evidence,result=result,unknown=False)
 print('Codex semantic recovery event',repair,'actual original execution count1; three verifier failures retained')
if __name__=='__main__':repair()

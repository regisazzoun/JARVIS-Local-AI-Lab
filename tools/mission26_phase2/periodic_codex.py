"""Bounded periodic Codex coordinator; JARVIS execution stays in canonical engine."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

PRIVATE = Path('/home/adminjarvis/JARVIS/jl03-cor-p1-private/supervision')
REGISTER = Path('/var/lib/jarvis/projects/jl03-cor-p1/REGISTRE-CODEX.json')
ROOT = '/opt/jarvis/conversation'
REPO = '/home/adminjarvis/JARVIS/jl03-cor-p1'
CONFIG = json.loads(Path(os.environ['JARVIS_COORDINATOR_CONFIG']).read_text()) if os.environ.get('JARVIS_COORDINATOR_CONFIG') else {}
if CONFIG:
    PRIVATE = Path(CONFIG['private'])
    REGISTER = Path(CONFIG['register'])
    REPO = CONFIG['repo']
ALLOWED_TASKS = set(CONFIG.get('allowed_tasks',['D03','D04','D17']))

def condition_key(attention):
    if not CONFIG:return hashlib.sha256(json.dumps(attention,sort_keys=True).encode()).hexdigest()
    stable=[{'task':row['task'],'mission':row['mission'],'condition':row['condition']} for row in attention]
    for item,row in zip(stable,attention):
        if row.get('verified_strategy_event'):item['verified_strategy_event']=row['verified_strategy_event']
    return hashlib.sha256(json.dumps(stable,sort_keys=True).encode()).hexdigest()


def verified_strategy(store,mission,reference):
    """Only an evidenced technical repair opens a different coordination strategy."""
    if type(reference) is not int:return None
    with store.db() as connection:
        row=connection.execute('SELECT actor,kind,result FROM mission_events WHERE mission=? AND id=?',(mission,reference)).fetchone()
        if not row or row['actor'] not in ('Codex','Codex-periodic') or row['kind']!='coordinator_strategy_verified':return None
        data=json.loads(row['result']);refs=data.get('evidence_events',[]);modules=data.get('installed_modules',[])
        if data.get('verified') is not True or not refs or not modules:return None
        if any(not isinstance(m,dict) or not m.get('file') or not isinstance(m.get('sha256'),str) or len(m['sha256'])!=64 or any(c not in '0123456789abcdef' for c in m['sha256']) for m in modules):return None
        if any(type(ref) is not int or ref==reference or not connection.execute('SELECT id FROM mission_events WHERE mission=? AND id=?',(mission,ref)).fetchone() for ref in refs):return None
    return reference





def unresolved_escalations(events):
    resolved=set()
    for event in events:
        if event['kind']!='coordinator_escalation_resolved' or not event['actor'].startswith('Codex'):continue
        data=event['result'];refs=[data.get('escalation_event')]
        refs+=data.get('escalation_events',[])+data.get('escalations',[])
        resolved.update(ref for ref in refs if type(ref) is int)
    return [event for event in events if event['kind'] in ('authority_escalation','p2_escalation') and event['id'] not in resolved]


def service_condition(config,private):
    if not config.get('monitor_units'):return None,None
    sys.path.insert(0,str(Path(__file__).parent))
    from service_watch import read_health
    health=read_health(private,config.get('health_max_age_seconds',180))
    if health['monitor_stale']:return 'SERVICE_HEALTH_STALE',health
    if health.get('unavailable_units'):return 'SERVICE_UNAVAILABLE:'+','.join(health['unavailable_units']),health
    return None,health


def main():
    os.umask(0o077)
    PRIVATE.mkdir(exist_ok=True, mode=0o700)
    with (PRIVATE/'coordinator.lock').open('a') as lock:
        try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: return
        sys.path.insert(0, ROOT)
        from jarvis.mission_store import MissionStore
        store = MissionStore(ROOT)
        if CONFIG and (PRIVATE/'MANUAL-HOLD').exists():
            print('Manual coordinator active; periodic dispatch deferred.')
            return
        tasks = json.loads(REGISTER.read_text())['tasks']
        attention = []
        service_issue,service_health=service_condition(CONFIG,PRIVATE)
        for task in tasks:
            if task['id'] not in ALLOWED_TASKS: continue
            if CONFIG.get('allowed_mission_ids') and task['mission_id'] not in CONFIG['allowed_mission_ids']: continue
            mission = store.get(task['mission_id'])
            state = mission['state']
            stopped = state in ('interrupted','failed','waiting_external')
            review = state == 'completed' and not task.get('validated') and not task.get('technical_review_recorded')
            stalled = state in ('queued','running') and time.time() - max(mission['last_progress'], mission.get('next_run') or 0) > 900
            condition = 'STOPPED_OR_REVIEW' if stopped or review else 'STALLED'
            if CONFIG:
                with store.db() as connection:
                    selected=connection.execute("SELECT id,kind,actor,created,result FROM mission_events WHERE mission=? AND kind IN ('authority_escalation','p2_escalation','cycle_error','authority_execution','authority_validation','coordinator_escalation_resolved') ORDER BY id",(mission['id'],)).fetchall()
                events=[{**dict(e),'result':json.loads(e['result'] or '{}')} for e in selected]
                escalations=unresolved_escalations(events)
                if stopped and escalations:
                    reason=escalations[-1]['result'];condition=reason.get('category') or reason.get('reason') or 'STOPPED'
                    errors=[event for event in events if event['kind']=='cycle_error' and event['id']>escalations[-1]['id']]
                    if escalations[-1]['kind']=='p2_escalation' and errors:condition='WORKER_EXCEPTION:'+str(errors[-1]['result'].get('type','UNKNOWN'))
                productive=[e['created'] for e in events if e['kind']=='authority_validation' or (e['kind']=='coordinator_escalation_resolved' and e['actor'].startswith('Codex')) or (e['kind']=='authority_execution' and (e['result'].get('kind')=='test' or (e['result'].get('kind')=='correct' and e['result'].get('before')!=e['result'].get('after'))))]
                if CONFIG.get('normal_engine_progress'):
                    # Normal preparation records useful plan/observation progress
                    # through the existing worker classifier, not Authority events.
                    # Lease heartbeats and mission_progress polling do not update it.
                    productive.append(mission['last_progress'])
                if state in ('queued','running') and time.time()-max(productive or [mission.get('created') or mission['updated']])>CONFIG.get('no_productive_seconds',600):
                    stalled=True;condition='NO_PRODUCTIVE_EXECUTION'
            if service_issue and state not in ('completed','publishing','cancelled'):
                stalled=True;condition=service_issue
            # Let the explicit one-shot dispatcher consume an already reviewed repair.
            if task.get('corrective_resume',{}).get('armed'): continue
            if not (stopped or review or stalled): continue
            plans = store.plans(mission['id'])
            attention.append({'task':task['id'],'mission':mission['id'],'state':state,
                              'result':json.loads(mission.get('result') or '{}'),
                              'plan_version':plans[-1]['version'] if plans else 0})
            if CONFIG:
                attention[-1]['condition']=condition
                if service_health:attention[-1]['service_health']={key:service_health.get(key) for key in ('checked_at','status','unavailable_units','monitor_stale')}
                strategy=verified_strategy(store,mission['id'],task.get('coordination_strategy_event'))
                if strategy:attention[-1]['verified_strategy_event']=strategy
        statefile = PRIVATE/'STATE.json'
        saved = json.loads(statefile.read_text()) if statefile.exists() else {'attempts':{}}
        if not attention:
            saved.update(checked_at=time.time(),status='WATCHING_NO_INTERVENTION_NEEDED',attention=[],unresolved=[],scope_note='No current intervention needed; attempts and last passage result are historical and retained')
            statefile.write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n')
            print('Watching: native work progressing or reviewed resume already queued.')
            return
        key = condition_key(attention)
        if os.environ.get('JARVIS_COORDINATOR_DRY_RUN')=='1':
            print(json.dumps({'status':'ATTENTION_READY' if attention else 'WATCHING','key':key,'attention':attention},ensure_ascii=False))
            return
        tries = saved.setdefault('attempts',{}).get(key,0)
        if CONFIG:
            recorded=[]
            with store.db() as connection:
                for row in attention:
                    for event in connection.execute("SELECT result FROM mission_events WHERE mission=? AND kind='coordinator_periodic_started'",(row['mission'],)):
                        result=json.loads(event['result'] or '{}')
                        if result.get('condition_key')==key:recorded.append(result.get('attempt',0))
            tries=max([tries]+recorded)
        if tries >= 3:
            if CONFIG:
                for row in attention:
                    with store.db() as connection:
                        prior=connection.execute("SELECT result FROM mission_events WHERE mission=? AND kind='coordinator_bounded_stop'",(row['mission'],)).fetchall()
                    if not any(json.loads(e['result'] or '{}').get('condition_key')==key for e in prior):
                        store.event(row['mission'],'coordinator_bounded_stop',actor='Codex-periodic',result={'condition_key':key,'attempts':tries,'condition':row['condition'],'status':'BLOQUÉ — ANALYSE DOCUMENTÉE','no_fourth_passage':True})
            saved.update(checked_at=time.time(),status='COORDINATOR_BOUNDED_STOP',unresolved=attention)
            statefile.write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n')
            print('Same coordination condition unresolved after3 passages; dossier retained, no fourth blind retry.')
            return
        saved['attempts'][key] = tries+1
        saved.update(started_at=time.time(),status='CODEX_COORDINATING',attention=attention)
        statefile.write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n')
        stamp = str(time.time_ns());output=PRIVATE/(stamp+'-summary.md');log=PRIVATE/(stamp+'-private.log')
        prompt=(PRIVATE/'PROMPT.md').read_text()+'\nÉTAT CIBLÉ OBSERVÉ PAR LE WATCHDOG :\n'+json.dumps(attention,ensure_ascii=False)+'\nPassage borné '+str(tries+1)+'/3 pour cet état. Une répétition inchangée ne corrige rien.'
        cmd=['/home/adminjarvis/.local/bin/codex','-a','never','exec','-s','danger-full-access','-C',REPO,
             '--ephemeral','--color','never','-o',str(output),'-']
        for row in attention:store.event(row['mission'],'coordinator_periodic_started',task=row['task'],actor='Codex-periodic',result={'attempt':tries+1,'condition_key':key,'summary_path':str(output),'scope':'One targeted coordination intervention, JARVIS retains execution'})
        with log.open('w') as stream:
            proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=stream,stderr=subprocess.STDOUT,text=True,start_new_session=True)
            try: proc.communicate(prompt,timeout=420);rc=proc.returncode
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGTERM)
                try:proc.wait(timeout=10)
                except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
                rc=124
        saved.update(finished_at=time.time(),status='PASSAGE_FINISHED' if rc==0 else 'PASSAGE_FAILED',returncode=rc,summary_path=str(output))
        statefile.write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n')
        for row in attention:store.event(row['mission'],'coordinator_periodic_finished',task=row['task'],actor='Codex-periodic',result={'returncode':rc,'condition_key':key,'summary_path':str(output),'not_acceptance':True})
        print(json.dumps({'returncode':rc,'summary':str(output)}))


if __name__ == '__main__': main()

"""Observe existing systemd services and request the existing bounded coordinator.

No mission resubmission, worker restart, result classification or new engine.
"""
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

FIELDS='Id,Type,LoadState,ActiveState,SubState,Result,NRestarts,MainPID,ExecMainStatus'


def poll_services(units,runner=None):
    runner=runner or subprocess.run
    if not units or any(not re.fullmatch(r'jarvis-[A-Za-z0-9@_.-]+\.(service|timer)',name) for name in units):
        raise ValueError('Expected explicit JARVIS systemd units')
    try:
        result=runner(['systemctl','show','--property='+FIELDS,'--',*units],capture_output=True,text=True,timeout=8)
    except (OSError,subprocess.TimeoutExpired) as exc:
        return {name:{'status':'UNKNOWN','error':type(exc).__name__} for name in units}
    rows={}
    for block in result.stdout.strip().split('\n\n'):
        data=dict(line.split('=',1) for line in block.splitlines() if '=' in line)
        if data.get('Id') in units:rows[data['Id']]=data
    for name in units:
        data=rows.setdefault(name,{'status':'UNKNOWN','error':'Unit observation absent'})
        if 'ActiveState' in data:
            data['status']='OK' if data['ActiveState']=='active' else 'RECOVERING' if data['ActiveState']=='activating' and data.get('SubState')=='auto-restart' else 'DOWN'
            if data.get('Type')=='oneshot' and data.get('Result')=='success' and data['ActiveState'] in ('inactive','activating'):data['status']='OK'
            if data.get('LoadState')=='not-found':data['status']='UNKNOWN'
    return rows


def evaluate(current,previous,now,grace=60):
    result={};alerts=[]
    for name,raw in current.items():
        old=previous.get('services',{}).get(name,{})
        row=dict(raw);bad=row['status']!='OK'
        row['unhealthy_since']=old.get('unhealthy_since',now) if bad and old.get('status')!='OK' else now if bad else None
        before=old.get('NRestarts');after=row.get('NRestarts')
        delta=max(0,int(after)-int(before)) if str(before).isdigit() and str(after).isdigit() else 0
        row['observed_restart_increments']=old.get('observed_restart_increments',0)+delta
        row['restart_increment_since_last_check']=delta
        if bad and (row['status']=='DOWN' or now-row['unhealthy_since']>=grace):alerts.append(name)
        result[name]=row
    return {'checked_at':now,'services':result,'unavailable_units':sorted(alerts),'status':'ATTENTION' if alerts else 'RECOVERING' if any(row['status']!='OK' for row in result.values()) else 'OK'}


def read_health(private,max_age=180,now=None):
    """A stale monitor is uncertainty, never a declaration of healthy services."""
    now=time.time() if now is None else now
    try:health=json.loads((Path(private)/'HEALTH.json').read_text())
    except (OSError,ValueError):return {'status':'UNKNOWN','unavailable_units':[],'monitor_stale':True}
    health['monitor_stale']=now-health.get('checked_at',0)>max_age
    return health


def main():
    os.umask(0o077)
    config=json.loads(Path(os.environ['JARVIS_COORDINATOR_CONFIG']).read_text())
    private=Path(config['private']);private.mkdir(parents=True,exist_ok=True)
    with (private/'health.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return
        path=private/'HEALTH.json'
        try:previous=json.loads(path.read_text())
        except (OSError,ValueError):previous={}
        health=evaluate(poll_services(config['monitor_units']),previous,time.time(),config.get('service_recovery_grace_seconds',60))
        sys.path.insert(0,'/opt/jarvis/conversation')
        from jarvis.mission_store import MissionStore
        store=MissionStore('/opt/jarvis/conversation')
        tasks=json.loads(Path(config['register']).read_text())['tasks'];health['missions']=[]
        signature=lambda h: [(key,row.get('status'),row.get('NRestarts')) for key,row in sorted(h.get('services',{}).items())]
        for task in tasks:
            if task['id'] not in config['allowed_tasks'] or task['mission_id'] not in config['allowed_mission_ids']:continue
            mission=store.get(task['mission_id'])
            health['missions'].append({'id':mission['id'],'state':mission['state'],'last_progress_age_seconds':max(0,time.time()-mission['last_progress'])})
            if signature(health)!=signature(previous):
                store.event(mission['id'],'mission_service_health_observed',actor='systemd-health',result={'services':health['services'],'unavailable_units':health['unavailable_units'],'mission_state_not_changed':True,'no_command_replayed':True})
        health['last_trigger_at']=previous.get('last_trigger_at',0)
        health['trigger_attempts']=previous.get('trigger_attempts',{})
        same_incident=health['unavailable_units'] and health['unavailable_units']==previous.get('unavailable_units')
        health['incident']=previous.get('incident') if same_incident and previous.get('incident') else str(time.time_ns()) if health['unavailable_units'] else None
        health['coordinator_trigger']='NOT_NEEDED'
        def save():
            temporary=path.with_suffix('.json.tmp');temporary.write_text(json.dumps(health,ensure_ascii=False,indent=2)+'\n');temporary.replace(path)
        save()  # The coordinator must see the new observation before being started.
        if health['unavailable_units']:
            if (private/'MANUAL-HOLD').exists():health['coordinator_trigger']='MANUAL_COORDINATOR_ACTIVE'
            elif health['services'].get(config.get('coordinator_service','jarvis-m26-p2-supervision.service'),{}).get('ActiveState') in ('active','activating'):health['coordinator_trigger']='COORDINATOR_ALREADY_ACTIVE'
            elif health['trigger_attempts'].get(health['incident'],0)>=3:health['coordinator_trigger']='ESCALATION_EXHAUSTED'
            elif time.time()-health['last_trigger_at']<120:health['coordinator_trigger']='COOLDOWN'
            else:
                unit=config.get('coordinator_service','jarvis-m26-p2-supervision.service')
                if not re.fullmatch(r'jarvis-[A-Za-z0-9@_.-]+\.service',unit):raise ValueError('Invalid coordinator unit')
                health['trigger_attempts'][health['incident']]=health['trigger_attempts'].get(health['incident'],0)+1
                save()  # Persist the attempt before starting another process.
                try:
                    call=subprocess.run(['sudo','-n','systemctl','start','--no-block',unit],capture_output=True,text=True,timeout=8)
                    health['coordinator_trigger']='REQUESTED' if call.returncode==0 else 'FAILED'
                    health['trigger_returncode']=call.returncode
                except (OSError,subprocess.TimeoutExpired) as exc:
                    health['coordinator_trigger']='UNKNOWN';health['trigger_error']=type(exc).__name__
                health['last_trigger_at']=time.time()
        if health['coordinator_trigger']=='ESCALATION_EXHAUSTED' and previous.get('coordinator_trigger')!='ESCALATION_EXHAUSTED':
            for mission in health['missions']:store.event(mission['id'],'mission_health_escalation',actor='systemd-health',result={'incident':health['incident'],'attempts':3,'unavailable_units':health['unavailable_units'],'request_to':'Codex','reason':'Three service recovery coordination starts for the same observed outage; diagnose before another strategy','no_worker_command_replayed':True})
        save()
        print(json.dumps({'status':health['status'],'unavailable_units':health['unavailable_units'],'coordinator_trigger':health['coordinator_trigger']}))


if __name__=='__main__':main()

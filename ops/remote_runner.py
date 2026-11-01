#!/usr/bin/env python3
"""Checkpoint process supervisor, not an agent or a metrics collector.

One immutable manifest/ID, user systemd cgroup, bounded renewable lease.
Only the dedicated idle-workspaces tree may be used for task writes.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

BASE = Path.home()/'JARVIS/idle-scheduler-runtime'
WORK = Path.home()/'JARVIS/idle-workspaces'
STOP = False

def atomic(path, data):
    tmp = path.with_suffix('.tmp')
    with tmp.open('w') as f:
        json.dump(data, f, indent=2)
        f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)

def paths(ident):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]{0,79}',ident):
        raise ValueError('Invalid task ID')
    root=BASE/'jobs'/ident
    root.mkdir(parents=True,exist_ok=True,mode=0o700)
    return root,'jarvis-idle-'+hashlib.sha256(ident.encode()).hexdigest()[:20]+'.service'

def validate(manifest):
    if manifest.get('checkpoint_safe') is not True:
        raise ValueError('Explicit checkpoint-safe contract required')
    cwd=Path(manifest['cwd']).resolve()
    cwd.relative_to(WORK.resolve())
    if not cwd.is_dir():raise ValueError('Task workspace must already exist')
    argv=manifest['argv']
    if not isinstance(argv,list) or not argv or not all(isinstance(v,str) and '\0' not in v for v in argv) or not Path(argv[0]).is_absolute():
        raise ValueError('Absolute executable argv required')
    if not 5 <= manifest.get('lease_seconds',30) <= 60:raise ValueError('Invalid lease')
    if not 1 <= manifest.get('max_seconds',3600) <= 86400:raise ValueError('Invalid deadline')

def unit_info(unit):
    p=subprocess.run(['systemctl','--user','show',unit,'-p','ActiveState','-p','SubState','-p','MainPID','-p','ControlGroup'],capture_output=True,text=True,timeout=5)
    return dict(line.split('=',1) for line in p.stdout.splitlines() if '=' in line)

def alive(info):return info.get('ActiveState') in ('active','activating','deactivating')

def status(root,unit):
    state=json.loads((root/'state.json').read_text()) if (root/'state.json').exists() else {'status':'new','failures':0,'runs':0}
    info=unit_info(unit)
    if state['status'] in ('running','starting') and not alive(info):
        # The supervisor may have committed completion between our file read
        # and the systemd observation. Re-read before declaring an unknown outcome.
        if (root/'state.json').exists():state=json.loads((root/'state.json').read_text())
    if state['status'] in ('running','starting') and not alive(info):
        # Unknown outcome counts as a failure; never invent completion.
        state.update(status='interrupted',failures=state.get('failures',0)+1,reason='Supervisor/cgroup disappeared',updated_at=time.time())
        atomic(root/'state.json',state)
    result={**state,'unit':unit,'systemd':info}
    if (root/'manifest.json').exists():
        manifest=json.loads((root/'manifest.json').read_text())
        if manifest.get('progress_file'):
            path=(Path(manifest['cwd'])/manifest['progress_file']).resolve()
            path.relative_to(Path(manifest['cwd']).resolve())
            if path.exists():
                progress=json.loads(path.read_text())
                result['progress']={k:progress.get(k) for k in ('status','current','checkpoint_commit','completed','failures')}
    return result

def stop_group(proc):
    try:os.killpg(proc.pid,signal.SIGTERM)
    except ProcessLookupError:return
    try:proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid,signal.SIGKILL);proc.wait()

def external_inference(port, local_address=None):
    """Existing socket table, only remote peers of the protected inference port.

The task's own native Qwen client uses loopback. Persistent non-loopback
connections mean another client needs the same inference service.
"""
    p=subprocess.run(['ss','-Hnt','state','established','sport = :'+str(int(port))],capture_output=True,text=True,timeout=2,check=True)
    peers=set()
    for line in p.stdout.splitlines():
        columns=line.split()
        if len(columns)<4:continue
        peer=columns[3]
        if peer.rsplit(':',1)[0].strip('[]') not in ('127.0.0.1','::1',local_address):
            peers.add(peer)
    return peers

def supervisor(ident):
    global STOP
    os.umask(0o077)
    root,unit=paths(ident)
    # Retained by the supervisor, not task children.
    lock=(root/'execution.lock').open('a')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    manifest=json.loads((root/'manifest.json').read_text());validate(manifest)
    state=json.loads((root/'state.json').read_text())
    state.update(status='running',started_at=time.time(),updated_at=time.time(),supervisor_pid=os.getpid())
    atomic(root/'state.json',state)
    def stop(*_):
        global STOP
        STOP=True
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    env={'HOME':str(Path.home()),'PATH':'/usr/bin:/bin','LANG':'C.UTF-8'}
    # Only explicitly named, non-secret config variables; credentials stay local.
    env.update(manifest.get('environment',{}))
    proc=None;reason=None;seen={};started=time.monotonic()
    try:
        with (root/'output.log').open('a') as out:
            proc=subprocess.Popen(manifest['argv'],cwd=manifest['cwd'],env=env,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
            state['task_pid']=proc.pid;atomic(root/'state.json',state)
            while proc.poll() is None:
                if STOP:reason='operator/controller stop'
                elif time.monotonic()-started > manifest.get('max_seconds',3600):reason='deadline'
                else:
                    lease=json.loads((root/'lease.json').read_text())
                    if time.time()>lease['expires']:reason='controller lease expired'
                    port=manifest.get('inference_port')
                    if not reason and port:
                        peers=external_inference(port,manifest.get('local_inference_address'));now=time.monotonic()
                        seen={peer:seen.get(peer,now) for peer in peers}
                        if any(now-t>6 for t in seen.values()):reason='external inference client priority'
                if reason:
                    stop_group(proc);break
                time.sleep(.2)
        if STOP and reason is None:
            reason='operator/controller stop'
        if reason:
            state['status']='failed' if reason=='deadline' else 'paused'
            if reason=='deadline':state['failures']=state.get('failures',0)+1
            state['reason']=reason
        elif proc.returncode==0:
            state.update(status='completed',returncode=0,reason='Native task exited successfully')
        else:
            state.update(status='failed',returncode=proc.returncode,failures=state.get('failures',0)+1,reason='Task failed')
    except BaseException as exc:
        if proc and proc.poll() is None:stop_group(proc)
        if STOP:
            state.update(status='paused',reason='operator/controller stop during observation')
        else:
            state.update(status='failed',failures=state.get('failures',0)+1,reason=type(exc).__name__+': '+str(exc))
    finally:
        state.update(updated_at=time.time(),task_pid=None)
        atomic(root/'state.json',state)
        lock.close()

def rpc(request):
    ident=request['id'];root,unit=paths(ident)
    lock=(root/'control.lock').open('a')
    with lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        action=request['action']
        if action=='start':
            manifest=request['manifest'];validate(manifest)
            value=json.dumps(manifest,sort_keys=True)
            if (root/'manifest.json').exists() and json.loads((root/'manifest.json').read_text())!=manifest:
                raise ValueError('Manifest changed for persistent ID; manual review required')
            state=status(root,unit)
            if state['status']=='completed' or alive(state['systemd']):
                atomic(root/'lease.json',{'expires':time.time()+manifest.get('lease_seconds',30)})
                return state
            resolved=0
            if (root/'resolution.json').exists():
                resolution=json.loads((root/'resolution.json').read_text())
                if resolution.get('verified') and 0<=resolution.get('failed_through',0)<=state.get('failures',0):
                    resolved=resolution['failed_through']
                    state['resolution']=resolution
            if state.get('failures',0)-resolved>=3:raise ValueError('Three failures reached; no restart')
            atomic(root/'manifest.json',manifest)
            atomic(root/'lease.json',{'expires':time.time()+manifest.get('lease_seconds',30)})
            state={k:v for k,v in state.items() if k not in ('systemd','unit')}
            state.update(status='starting',runs=state.get('runs',0)+1,updated_at=time.time())
            atomic(root/'state.json',state)
            subprocess.run(['systemctl','--user','reset-failed',unit],capture_output=True,timeout=5)
            command=['systemd-run','--user','--quiet','--collect','--unit',unit,'--property=KillMode=control-group','--property=TimeoutStopSec=6','--property=Nice=15','--property=CPUQuota=100%','--property=MemoryMax='+manifest.get('memory_max','1G'),'--property=TasksMax=128','--property=NoNewPrivileges=true','--property=UMask=0077','/usr/bin/python3',str(Path(__file__).resolve()),'supervise',ident]
            p=subprocess.run(command,capture_output=True,text=True,timeout=8)
            if p.returncode:
                state.update(status='failed',failures=state.get('failures',0)+1,reason=p.stderr[:1000]);atomic(root/'state.json',state)
                raise RuntimeError(p.stderr)
            # The unit is now active before status may classify recovery.
            return status(root,unit)
        if action=='renew':
            manifest=json.loads((root/'manifest.json').read_text())
            atomic(root/'lease.json',{'expires':time.time()+manifest.get('lease_seconds',30)})
        elif action=='pause':
            if alive(unit_info(unit)):
                # Let the supervisor stop its task group before systemd kills
                # transient observation children in the same cgroup.
                subprocess.run(['systemctl','--user','kill','--kill-whom=main','--signal=TERM',unit],capture_output=True,text=True,timeout=3)
                deadline=time.monotonic()+4
                while alive(unit_info(unit)) and time.monotonic()<deadline:time.sleep(.1)
                if alive(unit_info(unit)):
                    subprocess.run(['systemctl','--user','stop',unit],capture_output=True,text=True,timeout=10,check=True)
            info=unit_info(unit)
            if alive(info) or info.get('MainPID','0')!='0':raise RuntimeError('Remote stop not confirmed')
        elif action!='status':raise ValueError('Unknown action')
        return status(root,unit)

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='supervise':supervisor(sys.argv[2])
    else:
        try:print(json.dumps({'ok':True,'state':rpc(json.load(sys.stdin))}))
        except Exception as exc:
            print(json.dumps({'ok':False,'error':type(exc).__name__+': '+str(exc)}));sys.exit(1)

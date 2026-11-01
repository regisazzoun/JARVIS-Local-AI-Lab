#!/usr/bin/env python3
"""Opt-in checkpoint units, using existing JARVIS telemetry; no collector."""
import argparse
import fcntl
import json
import math
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import time

STOP = False

def stop(*_):
    global STOP
    STOP = True

def write_state(path, state):
    tmp = path.with_suffix('.tmp')
    with tmp.open('w') as f:
        json.dump(state, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)

def fresh(stamp, now, age):
    return isinstance(stamp, (int, float)) and math.isfinite(stamp) and 0 <= now-stamp <= age

def admission(cfg, job, snapshot, now=None):
    now = time.time() if now is None else now
    age = cfg.get('max_sample_age_seconds', 25)
    if not fresh(snapshot.get('sampled_at'), now, age):
        return False, 'stale aggregate'
    machine = snapshot['machines'][job['node']]
    if not machine.get('available') or not fresh(machine.get('sampled_at'), now, age):
        return False, 'unavailable or stale host'
    def number(value, lo, hi):
        return isinstance(value, (int, float)) and math.isfinite(value) and lo <= value <= hi
    cpu, total, used = (machine[k] for k in ('cpu_percent', 'ram_total_mb', 'ram_used_mb'))
    if not number(cpu, 0, 100) or not number(total, 1, 2**40) or not number(used, 0, total):
        return False, 'invalid CPU/RAM'
    active_gpu = job.get('_running',False) and job.get('uses_gpu',False)
    cpu_limit = cfg.get('max_active_cpu_percent',95) if active_gpu else cfg['max_cpu_percent']
    if cpu > cpu_limit or (total-used)/total < cfg['min_mem_available_fraction']:
        return False, 'CPU/RAM busy'
    # Loaded weights are preserved. CPU units may coexist; GPU units may not evict them.
    running = job.get('_running',False) and job.get('uses_gpu',False)
    own_resident = bool(job.get('resident_model')) and machine.get('active_models') == [job['resident_model']]
    gpus = machine.get('gpu_all')
    if not fresh(machine.get('gpu_captured_at'), now, age) or not gpus:
        return False, 'missing complete GPU telemetry'
    for gpu in gpus:
        util, free, capacity = (gpu[k] for k in ('utilization_percent', 'free_mib', 'total_mib'))
        if not number(util, 0, 100) or not number(capacity, 1, 2**30) or not number(free, 0, capacity):
            return False, 'invalid GPU telemetry'
        if not running and util > cfg['max_gpu_utilization_percent']:
            return False, 'GPU busy'
        if job.get('uses_gpu', False) and not running and not own_resident and 1-free/capacity > cfg['max_vram_used_fraction']:
            return False, 'VRAM reserved'
    if job.get('uses_gpu', False) and (not machine.get('ollama') or (machine.get('active_models') and not own_resident)):
        return False, 'model residency reserved'
    return True, 'eligible'

class Telemetry:
    def __init__(self, cfg):
        self.cfg = cfg
    def read(self, job):
        # Existing collector artifact, independent of Launcher presentation/API.
        data = json.loads(Path(self.cfg['telemetry_path']).read_text())
        node = job['node']
        if node == 'mac-mini':
            proc = subprocess.run(['/usr/bin/python3', '/opt/jarvis/conversation/operations28a/resource_probe.py'], capture_output=True, text=True, timeout=8, check=True)
            probe = json.loads(proc.stdout)
        else:
            host = {'dell-1':'dell-observe', 'dell-2':'dell2'}[node]
            code = 'from jarvis.host_client import request; import json; print(json.dumps(request("host_remote",{"host":'+repr(host)+',"action":"hybrid_resources"},workload_class="mission")))'
            proc = subprocess.run(['/opt/jarvis/conversation/.venv/bin/python', '-c', code], capture_output=True, text=True, timeout=10, check=True)
            reply = json.loads(proc.stdout)
            result = reply['result']
            if result['returncode'] != 0:
                raise ValueError('Existing admission probe failed')
            probe = json.loads(result['stdout'])
        data['machines'][node].update(gpu_all=probe['gpu'], gpu_captured_at=probe['captured_at'])
        return data

def eligible(cfg, job, telemetry):
    try:
        if cfg.get('compute_database'):
            with sqlite3.connect('file:'+cfg['compute_database']+'?mode=ro', uri=True, timeout=1) as db:
                if db.execute("SELECT 1 FROM compute_jobs WHERE node=? AND state IN ('queued','running') LIMIT 1", ({'mac-mini':'Mac-mini','dell-1':'Dell1','dell-2':'Dell2'}[job['node']],)).fetchone():
                    return False, 'canonical inference queue reserved'
        return admission(cfg, job, telemetry.read(job))
    except Exception as exc:
        return False, 'telemetry unavailable: '+type(exc).__name__

def terminate(proc):
    from remote_client import RemoteProcess
    if isinstance(proc, RemoteProcess):
        return proc.terminate()
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()

def run(cfg, execute, telemetry=None):
    if not execute or not cfg.get('enabled'):
        print('Disabled/dry run; no state or job changed.', flush=True)
        return
    path = Path(cfg['state_path'])
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix('.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    state = json.loads(path.read_text()) if path.exists() else {'completed': [], 'attempts': {}}
    if state.get('status') == 'running':
        state.update(status='interrupted', reason='Recovered after process loss; checkpoint contract required')
        # An ambiguous crash counts toward the same three-attempt limit.
    telemetry = telemetry or Telemetry(cfg)
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    def save(status, **extra):
        state.update(status=status, updated_at=time.time(), **extra)
        write_state(path, state)
        print(json.dumps({'status':status, **extra}), flush=True)
    def wait():
        until = time.monotonic()+cfg['poll_seconds']
        while not STOP and time.monotonic() < until:
            time.sleep(min(.2, max(0, until-time.monotonic())))
    while not STOP:
        candidates = [j for j in cfg['jobs'] if j['id'] not in state['completed'] and state['attempts'].get(j['id'], 0) < 3]
        pending = candidates[0] if candidates else None
        if pending is None:
            save('idle', current=None, reason='No eligible pending configured unit')
            wait()
            continue
        ident = pending['id']
        if Path(cfg['pause_path']).exists():
            save('paused', current=ident, reason='Operator pause marker')
            wait()
            continue
        blockers = {}
        for candidate in candidates:
            ready, reason = eligible(cfg, candidate, telemetry)
            if ready:
                pending = candidate
                ident = pending['id']
                break
            blockers[candidate['id']] = reason
        else:
            save('waiting_resources', current=None, reason=blockers)
            wait()
            continue
        remote = pending.get('kind') == 'remote-checkpoint'
        if pending['node'] != 'mac-mini':
            if not remote and pending.get('kind') != 'service-check':
                raise ValueError('Remote mutation/checkpoint runner not qualified; only fixed read-only service-check supported')
            argv = ['/usr/bin/ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=4', {'dell-1':'jarvis-dell1','dell-2':'jarvis-dell2'}[pending['node']], '/usr/bin/systemctl', 'is-active', 'jarvis-ollama.service', 'jarvis-ollama-missions.service']
        else:
            argv = pending['argv']
            if pending.get('checkpoint_safe') is not True or not isinstance(argv, list) or not argv or not Path(argv[0]).is_absolute():
                raise ValueError('Only explicit checkpoint-safe argv units with absolute executable')
        state['attempts'][ident] = state['attempts'].get(ident, 0)+1
        save('running', current=ident, reason=reason)
        from remote_client import RemoteProcess
        proc = RemoteProcess(pending) if remote else subprocess.Popen(argv, start_new_session=True, cwd=cfg.get('working_directory', '/'), env={'PATH':'/usr/bin:/bin','HOME':str(Path.home()),'LANG':'C.UTF-8'})
        started = time.monotonic()
        interrupted = None
        while proc.poll() is None:
            if STOP or Path(cfg['pause_path']).exists():
                interrupted = 'stop/pause'
            elif time.monotonic()-started > pending.get('max_job_seconds',cfg['max_job_seconds']):
                interrupted = 'deadline'
            else:
                ready, reason = eligible(cfg, {**pending,'_running':remote}, telemetry)
                if not ready:
                    interrupted = reason
            if interrupted:
                terminate(proc)
                break
            time.sleep(cfg.get('monitor_seconds', 2))
        if interrupted:
            # Resource preemption is not a failure; deadline remains bounded.
            if interrupted != 'deadline':
                state['attempts'][ident] -= 1
            save('paused' if interrupted != 'deadline' else 'failed', reason=interrupted)
        elif remote and proc.returncode == 75:
            state['attempts'][ident] -= 1
            save('paused', reason=proc.state.get('reason', 'Remote preemption'))
        elif proc.returncode == 0:
            state['completed'].append(ident)
            save('completed', returncode=0)
        else:
            save('failed', returncode=proc.returncode)
        wait()
    save('stopped', current=state.get('current'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    run(json.loads(Path(args.config).read_text()), args.execute)

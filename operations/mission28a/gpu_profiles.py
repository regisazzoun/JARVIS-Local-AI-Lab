#!/usr/bin/env python3
"""Root-owned, fixed Dell GPU profiles with independent burst rollback."""
import argparse
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time

PROFILES={'interactive-priority':200,'balanced':250,'mission-intensive':280,'dual-gpu-burst':350}
STATE=Path('/var/lib/jarvis-gpu-profiles');CURRENT=STATE/'current.json'
PYTHON='/opt/jarvis-lab/tts-01/venv/bin/python'
LOAD='/opt/jarvis/compute/28a/gpu_load.py'


def command(argv,timeout=8):
    r=subprocess.run(argv,capture_output=True,text=True,timeout=timeout)
    if r.returncode:raise RuntimeError(r.stderr or r.stdout)
    return r.stdout

def sample():
    fields='index,power.draw,power.limit,temperature.gpu,clocks.gr,utilization.gpu,memory.used,pcie.link.gen.current,pcie.link.width.current'
    raw=command(['nvidia-smi','--query-gpu='+fields,'--format=csv,noheader,nounits'])
    rows=[]
    for line in raw.splitlines():
        values=[v.strip() for v in line.split(',')]
        rows.append(dict(zip(('index','power_w','limit_w','temperature_c','clock_mhz','gpu_percent','vram_mib','pcie_gen','pcie_width'),[float(x) if re.fullmatch(r'-?\d+(\.\d+)?',x) else x for x in values])))
    if len(rows)!=2:raise RuntimeError('Expected two actual GPUs')
    return {'at_unix':time.time(),'gpu':rows}

def save(data):
    STATE.mkdir(parents=True,exist_ok=True)
    tmp=CURRENT.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');tmp.chmod(0o644);tmp.replace(CURRENT)

def set_profile(name):
    target=PROFILES[name]
    for index in (0,1):
        raw=command(['nvidia-smi','-i',str(index),'--query-gpu=power.min_limit,power.max_limit','--format=csv,noheader,nounits'])
        minimum,maximum=map(float,raw.strip().split(','))
        if not minimum<=target<=maximum:raise RuntimeError('Requested power outside GPU nominal range')
    for index in (0,1):command(['nvidia-smi','-i',str(index),'-pl',str(target)])
    observed=sample()
    if any(x['limit_w']!=target for x in observed['gpu']):raise RuntimeError('Power readback differs')
    previous=json.loads(CURRENT.read_text()) if CURRENT.exists() else {}
    record={'profile':name,'limit_per_gpu_w':target,'changed_at':time.time(),'observed':observed}
    if previous.get('last_burst'):record['last_burst']=previous['last_burst']
    save(record)
    return observed

@contextmanager
def profile_lock():
    with open('/run/lock/jarvis-gpu-profile.lock','w') as file:
        fcntl.flock(file,fcntl.LOCK_EX|fcntl.LOCK_NB);yield

def burst(seconds=10):
    if not 1<=seconds<=12:raise ValueError('Burst window outside bounded range')
    started=time.time();data={'started':started,'target_w':700,'window_seconds':seconds,'samples':[],'errors':[]}
    def terminate(signum,frame):raise InterruptedError('Burst service stopped')
    signal.signal(signal.SIGTERM,terminate);signal.signal(signal.SIGINT,terminate)
    with profile_lock():
        try:
            set_profile('dual-gpu-burst')
            while time.time()-started<seconds:
                observed=sample();data['samples'].append(observed)
                if any(x['temperature_c']>=85 for x in observed['gpu']):raise RuntimeError('Observed GPU temperature reached85C guard')
                # Kernel faults since this window, not historical boot warnings.
                log=command(['journalctl','-k','--since','@'+str(int(started)),'--no-pager','-o','cat'])
                if re.search(r'Xid|fallen off|PCIe Bus Error|AER:.*(?:Fatal|Uncorrected)',log,re.I):raise RuntimeError('Observed GPU/PCIe fault during window')
                time.sleep(.25)
        except Exception as exc:data['errors'].append({'type':type(exc).__name__,'message':str(exc)})
        finally:
            data['finished']=time.time();data['duration_s']=data['finished']-started
            data['rollback']=set_profile('balanced')
            data['peak_combined_w']=max((sum(x['power_w'] for x in v['gpu']) for v in data['samples']),default=None)
            data['target_700w_measured']=bool(data['peak_combined_w'] is not None and data['peak_combined_w']>=700)
            path=STATE/('burst-'+str(time.time_ns())+'.json');path.write_text(json.dumps(data,indent=2)+'\n');path.chmod(0o644)
            save({'profile':'balanced','limit_per_gpu_w':250,'changed_at':time.time(),'last_burst':str(path),'observed':data['rollback']})
    return data

def campaign():
    rows=[]
    for gpus in ([0],[0,1]):
        set_profile('balanced');samples=[];done=False
        def monitor():
            while not done:
                samples.append(sample());time.sleep(.25)
        import threading
        thread=threading.Thread(target=monitor);thread.start()
        try:
            result=command(['runuser','-u','adminjarvis','--',PYTHON,LOAD,'--seconds','3','--gpus',*[str(i) for i in gpus]],timeout=25)
        finally:done=True;thread.join(timeout=3)
        rows.append({'gpus':gpus,'load':json.loads(result),'samples':samples})
    command(['systemctl','start','--no-block','jarvis-gpu-burst.service']);deadline=time.monotonic()+4
    while time.monotonic()<deadline:
        if CURRENT.exists() and json.loads(CURRENT.read_text()).get('profile')=='dual-gpu-burst':break
        time.sleep(.1)
    if not CURRENT.exists() or json.loads(CURRENT.read_text()).get('profile')!='dual-gpu-burst':raise RuntimeError('Burst profile did not activate')
    load=json.loads(command(['runuser','-u','adminjarvis','--',PYTHON,LOAD,'--seconds','6'],timeout=25))
    deadline=time.monotonic()+20
    while time.monotonic()<deadline:
        current=json.loads(CURRENT.read_text())
        if current.get('profile')=='balanced' and current.get('last_burst'):break
        time.sleep(.2)
    if current.get('profile')!='balanced' or not current.get('last_burst'):raise RuntimeError('Independent rollback not observed')
    burst_data=json.loads(Path(current['last_burst']).read_text())
    proof={'created':time.time(),'balanced_stages':rows,'burst_load':load,'burst':burst_data,'after':sample(),'system_wall_power_w':None,'scope':'Actual bounded GPU workload, no PSU certification; no wall meter available'}
    path=STATE/('campaign-'+str(time.time_ns())+'.json');path.write_text(json.dumps(proof,indent=2)+'\n');path.chmod(0o644)
    return {'path':str(path),'peak_combined_w':burst_data['peak_combined_w'],'target_700w_measured':burst_data['target_700w_measured'],'automatic_rollback_profile':current['profile'],'errors':burst_data['errors']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['status','set','restore','burst','campaign']);p.add_argument('--profile',choices=list(PROFILES),default='balanced');p.add_argument('--seconds',type=float,default=10);a=p.parse_args()
    if a.action=='status':result={'current':json.loads(CURRENT.read_text()) if CURRENT.exists() else None,'observed':sample()}
    elif a.action=='restore':
        with profile_lock():result=set_profile('balanced')
    elif a.action=='set':
        if a.profile=='dual-gpu-burst':raise SystemExit('Burst only through watchdog service')
        # Priority changes cancel a burst and its independent StopPost restores normal.
        subprocess.run(['systemctl','stop','jarvis-gpu-burst.service'],check=True)
        with profile_lock():result=set_profile(a.profile)
    elif a.action=='burst':result=burst(a.seconds)
    else:result=campaign()
    print(json.dumps(result))

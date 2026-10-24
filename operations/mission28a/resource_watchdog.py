#!/usr/bin/env python3
"""Root-owned fixed resource policy; no arbitrary commands from model data."""
import json
import os
from pathlib import Path
import pwd
import sqlite3
import subprocess
import time

DB=Path('/opt/jarvis/conversation/runtime/missions.sqlite')
STATE=Path('/run/jarvis-resource-state.json')
SLICE='jarvis-background.slice'

def active():
    account=pwd.getpwnam('adminjarvis');os.seteuid(account.pw_uid)
    try:
        c=sqlite3.connect('file:'+str(DB)+'?mode=ro',uri=True,timeout=3)
        try:
            running=c.execute("SELECT count(*) FROM compute_jobs WHERE role IN ('conversation','critical') AND state IN ('running','queued')").fetchone()[0]
            recent=c.execute("SELECT metrics FROM compute_jobs WHERE role IN ('conversation','critical') AND state='finished' AND finished>? ORDER BY finished DESC LIMIT 5",(time.time()-30,)).fetchall()
            latencies=[json.loads(row[0]).get('first_content_s') for row in recent if row[0] and json.loads(row[0]).get('load_duration',0)<1e9]
        finally:c.close()
    finally:os.seteuid(0)
    return running,[v for v in latencies if isinstance(v,(int,float))]

if __name__=='__main__':
    applied=None
    while True:
        try:
            count,latencies=active();mem={x.split(':')[0]:int(x.split()[1])*1024 for x in Path('/proc/meminfo').read_text().splitlines()}
            pressure=mem['MemAvailable']<4*2**30
            quota=300 if count or pressure or (latencies and max(latencies)>3) else 900
            if quota!=applied:
                subprocess.run(['systemctl','set-property','--runtime',SLICE,'CPUQuota='+str(quota)+'%'],check=True,capture_output=True,timeout=5);applied=quota
            state={'created':time.time(),'logical_cpus':os.cpu_count(),'background_quota_percent_of_one_cpu':quota,'background_machine_fraction_limit':quota/(100*os.cpu_count()),'interactive_active_or_queued':count,'recent_warm_first_content_s':latencies,'memory_available_bytes':mem['MemAvailable'],'memory_pressure':pressure,'policy':'900% maximum on12logicalCPUs,300% while interaction/pressure; not a VRAM partition'}
            tmp=STATE.with_suffix('.tmp');tmp.write_text(json.dumps(state)+'\n');tmp.chmod(0o644);tmp.replace(STATE)
        except Exception as exc:
            # Fail closed at maximum authorized75%; existing kernel quota stays set.
            print(type(exc).__name__+': '+str(exc),flush=True)
        time.sleep(1)

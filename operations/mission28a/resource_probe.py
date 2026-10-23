#!/usr/bin/env python3
"""Measured admission snapshot, without host identities or credentials."""
import json
import os
from pathlib import Path
import subprocess
import time

def collect():
    mem={x.split(':')[0]:int(x.split()[1])*1024 for x in Path('/proc/meminfo').read_text().splitlines()}
    result={'captured_at':time.time(),'memory_total_bytes':mem['MemTotal'],'memory_available_bytes':mem['MemAvailable'],'cpu_threads':os.cpu_count(),'load1':os.getloadavg()[0],'gpu':[]}
    r=subprocess.run(['nvidia-smi','--query-gpu=index,memory.total,memory.free,utilization.gpu,temperature.gpu,power.draw','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=5)
    if r.returncode:result['gpu_probe_error']=r.stderr[:500]
    else:
        for line in r.stdout.splitlines():
            values=[float(x.strip()) for x in line.split(',')]
            result['gpu'].append(dict(zip(('index','total_mib','free_mib','utilization_percent','temperature_c','power_w'),values)))
    return result

if __name__=='__main__':print(json.dumps(collect()))

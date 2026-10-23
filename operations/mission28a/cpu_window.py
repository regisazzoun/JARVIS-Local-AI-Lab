#!/usr/bin/env python3
"""Finite CPU-only load to measure the installed background slice quota."""
import argparse
import json
import multiprocessing
import os
from pathlib import Path
import time

def busy(seconds):
    end=time.monotonic()+seconds;n=1
    while time.monotonic()<end:n=(n*1664525+1013904223)%2**32

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=12);args=p.parse_args()
    if not 1<=args.seconds<=20:raise SystemExit('Finite window required')
    group=Path('/proc/self/cgroup').read_text().strip().split('::')[-1];slice_path=Path('/sys/fs/cgroup/jarvis.slice/jarvis-background.slice')
    if not slice_path.exists():raise SystemExit('Installed background slice absent')
    def stats():return {x.split()[0]:int(x.split()[1]) for x in (slice_path/'cpu.stat').read_text().splitlines()}
    before=stats();start=time.monotonic();processes=[multiprocessing.Process(target=busy,args=(args.seconds,)) for _ in range(os.cpu_count())]
    for process in processes:process.start()
    for process in processes:process.join()
    elapsed=time.monotonic()-start;after=stats();cpu_seconds=(after['usage_usec']-before['usage_usec'])/1e6
    print(json.dumps({'workload':'finite CPU test, not an agentic mission proof','cgroup':group,'quota':(slice_path/'cpu.max').read_text().strip(),'elapsed_s':elapsed,'cpu_seconds':cpu_seconds,'machine_cpu_fraction':cpu_seconds/(elapsed*os.cpu_count()),'throttled_usec_delta':after.get('throttled_usec',0)-before.get('throttled_usec',0),'processes':len(processes)}))

#!/usr/bin/env python3
"""Bounded CUDA work for profile characterization, never a persistent miner."""
import argparse
import json
import threading
import time
import torch

def work(index,seconds,rows):
    with torch.cuda.device(index):
        # Small enough to coexist with remaining runtime buffers.
        a=torch.randn((8192,8192),device='cuda:'+str(index),dtype=torch.float16)
        b=torch.randn_like(a);torch.cuda.synchronize(index)
        started=time.monotonic();count=0
        while time.monotonic()-started<seconds:
            torch.mm(a,b);torch.cuda.synchronize(index);count+=1
        rows.append({'gpu':index,'iterations':count,'elapsed_s':time.monotonic()-started})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=4);p.add_argument('--gpus',type=int,nargs='+',default=[0,1]);args=p.parse_args()
    if not 0<args.seconds<=8:raise SystemExit('Bounded test window required')
    assert torch.cuda.device_count()==2,'Expected actual dualGPU hardware'
    rows=[];threads=[threading.Thread(target=work,args=(i,args.seconds,rows)) for i in args.gpus]
    start=time.monotonic()
    for thread in threads:thread.start()
    for thread in threads:thread.join()
    print(json.dumps({'duration_s':time.monotonic()-start,'devices':rows,'complete':len(rows)==len(args.gpus)}))
    raise SystemExit(0 if len(rows)==len(args.gpus) else 1)

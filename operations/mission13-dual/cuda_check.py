#!/usr/bin/env python3
"""Small actual calculation on every detected GPU; no driver or power changes."""
import argparse
import json
import time
import torch

def check(expected=None):
    count=torch.cuda.device_count()
    data={'captured_at_unix':time.time(),'torch_version':torch.__version__,'cuda_runtime':torch.version.cuda,'device_count':count,'expected_device_count':expected,'devices':[],'peer_access':[]}
    for index in range(count):
        with torch.cuda.device(index):
            start=time.perf_counter()
            a=torch.arange(16,dtype=torch.float32,device='cuda:'+str(index)).reshape(4,4)
            b=torch.eye(4,device=a.device)
            actual=(a@b).sum().item();torch.cuda.synchronize(index)
            free,total=torch.cuda.mem_get_info(index)
            data['devices'].append({'index':index,'name':torch.cuda.get_device_name(index),'compute_capability':list(torch.cuda.get_device_capability(index)),'actual_sum':actual,'expected_sum':120.0,'pass':actual==120.0,'elapsed_s':time.perf_counter()-start,'free_bytes':free,'total_bytes':total})
    for a in range(count):
        for b in range(count):
            if a!=b:data['peer_access'].append({'source':a,'target':b,'available':torch.cuda.can_device_access_peer(a,b)})
    data['status']='PASS' if count and all(x['pass'] for x in data['devices']) and (expected is None or count==expected) else 'INSUFFICIENT' if expected and count<expected else 'FAIL'
    print(json.dumps(data))
    return data['status']=='PASS'

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--expect',type=int);args=p.parse_args()
    raise SystemExit(0 if check(args.expect) else 2)

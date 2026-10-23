#!/usr/bin/env python3
"""Targeted Ollama measurement; run only after physical/electrical qualification.
No downloads, model replacement, service edits or device reassignment.
"""
import argparse
import json
from pathlib import Path
import subprocess
import threading
import time
import urllib.request

def gpu_sample():
    r=subprocess.run(['nvidia-smi','--query-gpu=index,memory.used,utilization.gpu,temperature.gpu,power.draw,pcie.link.gen.current,pcie.link.width.current','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=5)
    if r.returncode:raise RuntimeError(r.stderr)
    return {'at_unix':time.time(),'columns':['index','memory_used_mib','gpu_percent','temperature_c','power_w','pcie_gen','pcie_width'],'rows':[line.split(', ') for line in r.stdout.splitlines() if line.strip()]}

def measure(url,model,context):
    start=time.perf_counter();samples=[];errors=[];stop=threading.Event()
    def monitor():
        while not stop.is_set():
            try:samples.append(gpu_sample())
            except Exception as exc:errors.append(str(exc))
            stop.wait(.5)
    thread=threading.Thread(target=monitor,daemon=True);thread.start()
    text='';first=None;done=None;failure=None
    request=urllib.request.Request(url.rstrip('/')+'/api/chat',data=json.dumps({'model':model,'messages':[{'role':'user','content':'En français, donne trois vérifications logicielles à effectuer après l’ajout d’un GPU. Ne prétends pas les avoir exécutées.'}],'stream':True,'think':False,'options':{'num_ctx':context,'num_predict':96,'temperature':0,'seed':0}}).encode(),headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(request,timeout=180) as response:
            for raw in response:
                item=json.loads(raw)
                if item.get('error'):raise RuntimeError(item['error'])
                part=item.get('message',{}).get('content','')
                if part and first is None:first=time.perf_counter()-start
                text+=part
                if item.get('done'):done=item
        if done is None:raise RuntimeError('Missing final Ollama metrics record')
    except Exception as exc:
        failure={'type':type(exc).__name__,'message':str(exc)}
    finally:
        elapsed=time.perf_counter()-start;stop.set();thread.join(timeout=7)
    done=done or {}
    return {'status':'FAIL' if failure else 'PASS','error':failure,'model':model,'context_requested':context,'elapsed_s':elapsed,'first_content_s':first,'response':text,'server_final_metrics':done,'tokens_per_second':done['eval_count']*1e9/done['eval_duration'] if done.get('eval_duration') and done.get('eval_count') else None,'gpu_samples':samples,'monitor_errors':errors,'scope':'One targeted request, includes loading if server performs it; not a quality or concurrency campaign'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--model',required=True);parser.add_argument('--url',required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--context',type=int,default=4096);parser.add_argument('--expected-gpus',type=int,default=2);args=parser.parse_args()
    if args.output.exists():parser.error('Output already exists; preserve previous evidence with a new name')
    before=gpu_sample()
    if len(before['rows'])!=args.expected_gpus:parser.error('GPU count differs from requested hardware; no inference started')
    result={'created_unix':time.time(),'gpu_before':before,'measurement':measure(args.url,args.model,args.context),'gpu_after':gpu_sample()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as file:json.dump(result,file,ensure_ascii=False,indent=2);file.write('\n')
    print(str(args.output))
    return result['measurement']['status']=='PASS'

if __name__=='__main__':raise SystemExit(0 if main() else 1)

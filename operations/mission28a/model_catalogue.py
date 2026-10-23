#!/usr/bin/env python3
"""Fixed independently observed installed-model catalogue, not a model report."""
import json
import shlex
import subprocess
import urllib.request

def collect():
    raw=subprocess.check_output(['systemctl','show','jarvis-ollama-missions','-p','Environment','--value'],text=True)
    env=dict(x.split('=',1) for x in shlex.split(raw) if '=' in x)
    base=env['OLLAMA_HOST'];base=base if base.startswith('http') else 'http://'+base
    with urllib.request.urlopen(base+'/api/tags',timeout=5) as r:tags=json.load(r)
    models=[{k:m[k] for k in ('name','digest','size')} for m in tags['models']];names={m['name'] for m in models}
    return {'models':models,'model_count':len(models),'installed':{name:name in names for name in ('qwen3:32b-q4_K_M','llama3.3:70b-instruct-q4_K_M','qwen3.5:27b-q4_K_M','qwen3-coder-next:q4_K_M')}}

if __name__=='__main__':print(json.dumps(collect()))

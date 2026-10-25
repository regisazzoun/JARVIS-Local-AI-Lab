"""Codex supplied candidate patch. Run by JARVIS, retain original and test afterwards."""
from pathlib import Path
import time,shutil
p=Path('backend/server.py');text=p.read_text()
old="""    try:
     r=request('host_remote',{'host':'dell-observe','action':'telemetry_v3'});data['machines']['dell-1'].update(json.loads(r['result']['stdout']))
    except (OSError,ValueError,RuntimeError):data['machines']['dell-1']['all_gpu_probe']='unavailable'
"""
new="""    for host,machine in (('dell-observe','dell-1'),('dell2','dell-2')):
     node=data['machines'].setdefault(machine,{'available':False})
     try:
      r=request('host_remote',{'host':host,'action':'telemetry_v3'})
      node.update(json.loads(r['result']['stdout']))
     except (OSError,ValueError,RuntimeError):
      node['all_gpu_probe']='unavailable'
"""
if old in text:
 shutil.copyfile(p,p.with_name('server-before-d17-'+str(time.time_ns())+'.py'))
 p.write_text(text.replace(old,new,1))
else:
 assert new in text,'Candidate diverged: inspect route before overwriting'
print('Dell2 real-route candidate patch applied or already present; tests still required')

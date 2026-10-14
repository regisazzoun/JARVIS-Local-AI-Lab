"""Run one CPU worker at a time; kill it on wall-time/RSS/host-memory limits."""
import subprocess,time,json,sys,os
from pathlib import Path
root=Path(__file__).resolve().parent;name=sys.argv[1]
with (root/f'{name}-run.log').open('w') as log:
 env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';proc=subprocess.Popen([str(root/'venv/bin/python'),str(root/'audio_worker.py'),name],cwd=root,env=env,stdout=log,stderr=log)
 start=time.monotonic();peak=0;status='completed'
 while proc.poll() is None:
  try:
   values=dict(line.split(':',1) for line in Path(f'/proc/{proc.pid}/status').read_text().splitlines() if ':' in line);rss=int(values.get('VmRSS','0 kB').split()[0]);peak=max(peak,rss)
  except (FileNotFoundError,ProcessLookupError):pass
  free=next(int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith('MemAvailable:'))
  if peak>2*1024*1024 or free<6*1024*1024 or time.monotonic()-start>180:
   status='stopped_resource_limit';proc.kill();break
  time.sleep(.02)
 code=proc.wait();res={'engine':name,'exit_code':code,'status':status,'wall_s':time.monotonic()-start,'rss_peak_sampled_kib':peak,'sample_interval_s':.02};(root/f'{name}-guard.json').write_text(json.dumps(res,indent=2));print(res)

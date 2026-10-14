"""Surveille un seul moteur : 180s, RSS 2Gio, RAM disponible >=6Gio."""
import subprocess,sys,time,json,os,signal
from pathlib import Path
ROOT=Path('/opt/jarvis/voice');prefix=Path(sys.argv[1]);prefix.parent.mkdir(parents=True,exist_ok=True)
command=[str(ROOT/'venv/bin/python'),str(ROOT/'scripts/voice_worker.py')]+sys.argv[2:]
started=time.monotonic();peak=0;min_available=10**20;reason=None;gpu_libraries=set();samples=0
with open(str(prefix)+'.log','w') as log:
 p=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 try:
  while p.poll() is None:
   try:
    status=Path(f'/proc/{p.pid}/status').read_text();rss=next((int(l.split()[1])*1024 for l in status.splitlines() if l.startswith('VmRSS:')),0);peak=max(peak,rss)
    mem=Path('/proc/meminfo').read_text();available=next(int(l.split()[1])*1024 for l in mem.splitlines() if l.startswith('MemAvailable:'));min_available=min(min_available,available)
    maps=Path(f'/proc/{p.pid}/maps').read_text();gpu_libraries.update(l.split()[-1] for l in maps.splitlines() if any(s in l for s in ('libcuda.so','libcudart.so','libcublas.so','libcudnn.so')));samples+=1
    if time.monotonic()-started>180:reason='timeout'
    elif rss>2*1024**3:reason='RSS >2GiB'
    elif available<6*1024**3:reason='MemAvailable <6GiB'
    if reason:os.killpg(p.pid,signal.SIGTERM);break
   except FileNotFoundError:pass
   time.sleep(.02)
  try:code=p.wait(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);code=p.wait()
 except BaseException:
  if p.poll() is None:os.killpg(p.pid,signal.SIGTERM);p.wait(timeout=5)
  raise
r={'command':command,'exit_code':code,'wall_s':time.monotonic()-started,'peak_rss_mib':peak/1024**2,'min_available_gib':min_available/1024**3,'samples_20ms':samples,'loaded_gpu_libraries':sorted(gpu_libraries),'stop_reason':reason}
Path(str(prefix)+'.guard.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(code if not reason else 1)

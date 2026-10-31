import subprocess,json,datetime,os,pathlib,urllib.request,glob
out={'collected_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actor':'Codex','mode':'read-only inventory','commands':{}}
def run(k,cmd,timeout=25):
 try:
  p=subprocess.run(cmd,shell=True,text=True,capture_output=True,timeout=timeout)
  out['commands'][k]={'command':cmd,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
 except subprocess.TimeoutExpired:out['commands'][k]={'command':cmd,'rc':None,'error':'timeout; result unknown'}
commands={
'os':'cat /etc/os-release; uname -r',
'cpu':'lscpu -J',
'memory':'free -b',
'dmi':"sudo -n dmidecode -t system -t bios -t memory",
'disks':'lsblk -b -J -o NAME,TYPE,SIZE,MODEL,FSTYPE,MOUNTPOINTS,TRAN,ROTA',
'filesystems':'findmnt -J -o TARGET,SOURCE,FSTYPE,OPTIONS',
'raid':'cat /proc/mdstat; sudo -n mdadm --detail --scan',
'pci':'lspci -nnk',
'usb':'lsusb; command -v boltctl >/dev/null && boltctl list',
'gpu':'nvidia-smi --query-gpu=index,name,uuid,pci.bus_id,memory.total,memory.used,utilization.gpu,temperature.gpu,power.draw,power.limit,driver_version --format=csv,noheader,nounits',
'gpu_processes':'nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader,nounits',
'gpu_driver':'nvidia-smi; command -v nvcc >/dev/null && nvcc --version',
'network':'ip -j address; ip -j route',
'links':"for x in /sys/class/net/*; do n=${x##*/}; if [ -e \"$x/device\" ]; then echo \"INTERFACE:$n\"; sudo -n ethtool \"$n\"; fi; done",
'cpu_temperature':'command -v sensors >/dev/null && sensors',
'tailscale':'tailscale status --json',
'services':'systemctl list-units --all --type=service --no-pager --plain --no-legend',
'unit_files':'systemctl list-unit-files --type=service --no-pager --no-legend',
'failed':'systemctl --failed --no-pager --plain',
'timers':'systemctl list-timers --all --no-pager',
'listeners':'sudo -n ss -ltnup',
'packages':"dpkg-query -W -f='${binary:Package}\t${Version}\t${db:Status-Status}\n'",
'versions':"python3 --version; node --version; npm --version; git --version; ssh -V; ansible --version; ollama --version",
'npm':'npm list -g --depth=0 --json',
'containers':'command -v docker >/dev/null && sudo -n docker ps -a --no-trunc --format json; command -v podman >/dev/null && podman ps -a --format json',
'venvs':"find /opt /home/adminjarvis/JARVIS /home/adminjarvis/.local -maxdepth 6 -name pyvenv.cfg -type f 2>/dev/null",
'node_projects':"find /opt /home/adminjarvis/JARVIS -maxdepth 4 -name package.json -not -path '*/node_modules/*' -type f 2>/dev/null",
'custom_units':"find /etc/systemd/system -maxdepth 3 -type f -name '*.service' -o -type f -name '*.conf'",
'processes':'ps -eo pid,ppid,user,comm,pcpu,pmem --sort=-pcpu',
}
for k,c in commands.items():run(k,c,40 if k in ('venvs','packages','npm') else 25)
for endpoint in ('version','tags','ps'):
 try:
  with urllib.request.urlopen('http://127.0.0.1:11434/api/'+endpoint,timeout=8) as r:out['ollama_'+endpoint]=json.load(r)
 except Exception as e:out['ollama_'+endpoint]={'error':type(e).__name__+': '+str(e)}
units=[]
for line in out['commands']['services'].get('stdout','').splitlines():
 items=line.split()
 if items and any(s in items[0] for s in ('jarvis','ollama','apache','livekit','tailscale','webui','dnsmasq','nginx','docker')):units.append(items[0].lstrip('●'))
for u in units:
 run('unit:'+u,"systemctl show "+u+" --property=Id,FragmentPath,DropInPaths,ActiveState,SubState,MainPID,ExecStart,WorkingDirectory,User,ControlGroup,CPUQuotaPerSecUSec,MemoryMax,Restart,NRestarts,ActiveEnterTimestamp")
out['python_environments']=[]
for cf in out['commands']['venvs'].get('stdout','').splitlines():
 py=pathlib.Path(cf).parent/'bin/python'
 if py.exists():
  try:
   p=subprocess.run([str(py),'-c',"import importlib.metadata as m,json,sys;print(json.dumps({'python':sys.version,'packages':sorted([(d.metadata['Name'],d.version) for d in m.distributions()])}))"],capture_output=True,text=True,timeout=15)
   out['python_environments'].append({'path':str(py.parent.parent),'rc':p.returncode,'inventory':json.loads(p.stdout) if p.returncode==0 else None})
  except Exception as e:out['python_environments'].append({'path':str(py),'error':type(e).__name__})
print(json.dumps(out,ensure_ascii=False))

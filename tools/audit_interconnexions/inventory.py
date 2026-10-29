"""Read-only inventories. Excludes credentials, full process environments and serials."""
import concurrent.futures,datetime,json,subprocess,socket,urllib.request
from pathlib import Path
PRIVATE=Path('/home/adminjarvis/JARVIS/audit-interconnexions-ia-private')
CODE=r'''
import json,subprocess,socket,urllib.request,os
from pathlib import Path
def run(args):
 try:
  p=subprocess.run(args,text=True,capture_output=True,timeout=15);return {'rc':p.returncode,'out':p.stdout,'err':p.stderr[:500]}
 except Exception as e:return {'error':str(e)}
d={'host':socket.gethostname(),'os':Path('/etc/os-release').read_text(),'kernel':run(['uname','-r']),'cpu':run(['lscpu','-J']),'meminfo':Path('/proc/meminfo').read_text(),'addresses':run(['ip','-j','address']),'services':run(['systemctl','list-units','--type=service','--state=running','--no-pager','--no-legend']),'listeners':run(['ss','-ltnp']),'gpu':run(['nvidia-smi','--query-gpu=index,name,memory.total,memory.used,utilization.gpu,temperature.gpu','--format=csv,noheader']),'timers':run(['systemctl','list-timers','--all','--no-pager']),'model_processes':run(['pgrep','-af','ollama|llama-server']),'binaries':run(['sh','-c','for b in ollama qwen node npm ansible tailscale docker; do command -v "$b"; done'])}
t=run(['tailscale','status','--json'])
try:
 j=json.loads(t.get('out','{}'));d['tailscale']={'state':j.get('BackendState'),'self':{k:j.get('Self',{}).get(k) for k in ['HostName','DNSName','TailscaleIPs','Online']}}
except Exception:d['tailscale']=t
print(json.dumps(d))
'''
policy=json.loads(Path('/etc/jarvis/host-policy.json').read_text())['remote_hosts']
def collect(name,profile):
 if profile:
  c=policy[profile];args=['ssh','-i',c['identity'],'-o','UserKnownHostsFile='+c['known_hosts'],'-o','BatchMode=yes','-o','ConnectTimeout=8',c['user']+'@'+c['address'],'python3','-']
 else:args=['python3','-']
 p=subprocess.run(args,input=CODE,capture_output=True,text=True,timeout=90)
 try:d=json.loads(p.stdout)
 except Exception:d={'error':p.stderr,'out':p.stdout[:1000]}
 d['audit_time']=datetime.datetime.now(datetime.timezone.utc).isoformat();(PRIVATE/(name+'.json')).write_text(json.dumps(d,indent=2)+'\n');return name,{'host':d.get('host'),'gpu':d.get('gpu'),'tailscale':d.get('tailscale'),'error':d.get('error')}
with concurrent.futures.ThreadPoolExecutor(3) as p:
 for name,d in p.map(lambda x:collect(*x),[('Mac',None),('Dell1','dell-observe'),('Dell2','dell2')]):print(name,json.dumps(d))

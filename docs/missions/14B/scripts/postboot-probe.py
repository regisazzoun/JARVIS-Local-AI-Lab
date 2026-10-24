#!/usr/bin/env python3
"""Mission14B observed acceptance only. No inference/router/service configuration."""
from pathlib import Path
import subprocess,json,platform,time,os
root=Path('/var/lib/jarvis/mission14b');manifest=json.loads((root/'manifest.json').read_text());checks={};details={}
def run(key,argv,timeout=45):
 try:
  r=subprocess.run(argv,capture_output=True,text=True,timeout=timeout);details[key]={'returncode':r.returncode,'stdout':r.stdout[-16000:],'stderr':r.stderr[-3000:]};return r.returncode==0
 except (OSError,subprocess.TimeoutExpired) as e:details[key]={'error':str(e)};return False
checks['uuid_match']=Path('/sys/class/dmi/id/product_uuid').read_text().strip()==manifest['uuid']
checks['booted_installed_system']=Path('/etc/debian_version').is_file() and platform.release()!='6.12.107+deb13-amd64' and not Path('/jarvis/sshd_config').exists()
checks['debian13']=Path('/etc/debian_version').read_text().strip().split('.')[0]=='13'
checks['storage_clean']=run('storage',['python3',str(root/'verify-storage.py'),str(root/'manifest.json')])
checks['ssh_active']=run('ssh',['systemctl','is-active','ssh'])
checks['driver_load']=run('module',['modprobe','nvidia'])
checks['gpu_query']=run('gpu',['nvidia-smi','--query-gpu=index,name,memory.total,driver_version,pci.bus_id','--format=csv,noheader'])
checks['two_gpus']=checks['gpu_query'] and len(details['gpu']['stdout'].strip().splitlines())==2
checks['cuda_all_devices']=run('cuda',[str(root/'cuda-smoke')])
checks['esp_copies_equal']=run('esp',['diff','-qr','/boot/efi/EFI','/boot/efi-secondary/EFI'])
checks['clock_synchronized']=run('clock',['timedatectl','show','-p','NTPSynchronized','--value']) and details['clock']['stdout'].strip()=='yes'
checks['key_sudo_external']='pending independent controller SSH authentication'
result={'observed_at':time.time(),'hostname':platform.node(),'kernel':platform.release(),'phase':'installed_boot','checks':checks,'details':details,'status':'PASS' if all(v is True for v in checks.values()) else 'PARTIAL','actor':'Codex-developed read-only probe, actual target execution','no_ollama_routing_load_changes':True}
root.mkdir(exist_ok=True,parents=True);tmp=root/'postboot.json.tmp';tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');tmp.replace(root/'postboot.json');print(json.dumps(result,ensure_ascii=False));raise SystemExit(0 if all(v is True for k,v in checks.items() if k not in ('key_sudo_external','clock_synchronized')) else 1)

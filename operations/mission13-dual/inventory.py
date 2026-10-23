#!/usr/bin/env python3
"""Read-only, bounded Dell GPU-extension inventory. No serial numbers or UUIDs."""
import glob
import json
import os
from pathlib import Path
import platform
import subprocess
import shlex
import time
import urllib.request

def run(argv, timeout=7):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return {'returncode': r.returncode, 'stdout': r.stdout[:14000], 'stderr': r.stderr[:1500]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'returncode': None, 'unavailable': type(exc).__name__, 'detail': str(exc)[:300]}

def read(path):
    try: return Path(path).read_text().strip()
    except OSError: return None

def api(path,base):
    try:
        with urllib.request.urlopen(base+path, timeout=4) as r: return json.load(r)
    except Exception as exc: return {'unavailable': type(exc).__name__}

def ticks():
    n = list(map(int, Path('/proc/stat').read_text().splitlines()[0].split()[1:]))
    return sum(n[:8]), n[3]+n[4]

def collect():
    a, ai = ticks(); time.sleep(.25); b, bi = ticks()
    dmi = {key: read('/sys/class/dmi/id/'+key) for key in ('sys_vendor','product_name','product_version','board_vendor','board_name','board_version','bios_vendor','bios_version','bios_date')}
    cpu = next((s.split(':',1)[1].strip() for s in Path('/proc/cpuinfo').read_text().splitlines() if s.startswith('model name')), None)
    memory = {s.split(':')[0]: int(s.split()[1]) for s in Path('/proc/meminfo').read_text().splitlines() if s.split(':')[0] in ('MemTotal','MemAvailable')}
    data = {'captured_at_unix':time.time(), 'os_release':{line.split('=',1)[0]:line.split('=',1)[1].strip(chr(34)) for line in Path('/etc/os-release').read_text().splitlines() if line.startswith(('PRETTY_NAME=','DEBIAN_VERSION_FULL='))},'kernel':platform.release(),'dmi':dmi,'cpu_model':cpu,'cpu_threads':os.cpu_count(),'cpu_utilization_sample_percent':100*(1-(bi-ai)/(b-a)) if b>a else None,'cpu_sample_seconds':.25,'loadavg':os.getloadavg(),'memory_kib':memory,'python':platform.python_version()}
    fields = 'index,name,driver_version,memory.total,memory.used,utilization.gpu,temperature.gpu,power.draw,power.limit,power.default_limit,power.min_limit,power.max_limit,pcie.link.gen.current,pcie.link.gen.max,pcie.link.width.current,pcie.link.width.max'
    data['gpu']=run(['nvidia-smi','--query-gpu='+fields,'--format=csv'])
    data['gpu_topology']=run(['nvidia-smi','topo','-m']);data['gpu_topology']['stdout']='\n'.join(data['gpu_topology'].get('stdout','').splitlines()[:4])
    pcie=run(['lspci','-Dnn']);pcie['stdout']='\n'.join(line for line in pcie.get('stdout','').splitlines() if any(word in line for word in ('NVIDIA','Non-Volatile','RAID bus controller')))
    data['pcie']=pcie
    data['pcie_gpu_links']=run(['bash','-c',"lspci -Dnn | awk '/NVIDIA/ && /VGA|3D controller/ {print $1}' | while read -r slot; do lspci -s \"$slot\" -vv | grep -E 'VGA compatible controller|3D controller|LnkCap:|LnkSta:|Physical Slot:|Kernel driver in use:'; done"])
    data['cuda_toolkit']=run(['nvcc','--version'])
    data['services']=run(['systemctl','is-active','ssh','jarvis-ollama','nvidia-persistenced','tailscaled'])
    environment=run(['systemctl','show','jarvis-ollama','-p','Environment','--value'])
    env=dict(item.split('=',1) for item in shlex.split(environment.get('stdout','')) if '=' in item)
    base=env.get('OLLAMA_HOST','127.0.0.1:11434');base=base if base.startswith(('http://','https://')) else 'http://'+base
    base=base.replace('://0.0.0.0:', '://127.0.0.1:')
    data['ollama_version']=api('/api/version',base)
    for label,path in [('ollama_models','/api/tags'),('ollama_resident','/api/ps')]:
        response=api(path,base)
        data[label]=[{'name':m.get('name'),'size':m.get('size'),'digest':m.get('digest'),'details':m.get('details'),'size_vram':m.get('size_vram'),'context_length':m.get('context_length')} for m in response['models']] if 'models' in response else response
    data['gpu_service_environment']={key:('[configured GPU UUID redacted]' if key=='CUDA_VISIBLE_DEVICES' and value.startswith('GPU-') else value) for key,value in env.items() if key in ('CUDA_VISIBLE_DEVICES','OLLAMA_CONTEXT_LENGTH','OLLAMA_MAX_LOADED_MODELS','OLLAMA_NUM_PARALLEL','OLLAMA_SCHED_SPREAD')}
    temperatures={}
    for file in glob.glob('/sys/class/hwmon/hwmon*/temp*_input'):
        name=read(str(Path(file).parent/'name'));value=read(file)
        if value and value.lstrip('-').isdigit():temperatures.setdefault(name,[]).append(int(value)/1000)
    data['temperatures_c']={key:{'min':min(values),'max':max(values),'sensors':len(values)} for key,values in temperatures.items()}
    # DMI type39 may contain serial/asset identifiers: retain only capability/status fields.
    psu = run(['sudo','-n','dmidecode','--type','39'])
    if psu.get('returncode')==0:
        safe = ('Power Supply','Power Unit Group:','Location:','Name:','Manufacturer:','Max Power Capacity:','Status:','Type:','Input Voltage Range Switching:','Plugged:','Hot Replaceable:')
        psu['stdout']='\n'.join(s for s in psu['stdout'].splitlines() if s.strip().startswith(safe))
    data['psu_smbios']=psu
    data['limits']=['PSU label, PDB part/revision, harness pinout, wire gauge and second GPU physical cabling cannot be qualified by software inventory.','Measurements are a short snapshot during agent operation, not guaranteed idle or whole-system wall power.']
    return data

if __name__=='__main__': print(json.dumps(collect(), ensure_ascii=False))

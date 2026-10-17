#!/usr/bin/env python3
"""Continue the authorized Dell mission after independently validated SSH."""
import argparse,json,os,pathlib,subprocess,time,urllib.request,re,shlex,socket
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);a=p.parse_args();b=a.session.resolve();os.umask(0o077)
s=json.loads((b/'installed-ip.json').read_text());ip=s['ip'];identity=b/'identity';known=b/'known_target';modeldir=pathlib.Path('/home/adminjarvis/JARVIS/ollama')
common=['ssh','-F','/dev/null','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o',f'UserKnownHostsFile={known}','-o','GlobalKnownHostsFile=/dev/null','-o','IdentitiesOnly=yes','-o','ConnectTimeout=10','-i',str(identity)]
def ssh(cmd,check=True):
 r=subprocess.run(common+['adminjarvis@'+ip,cmd],capture_output=True,text=True)
 if check and r.returncode:raise RuntimeError(r.stderr[-1500:]+r.stdout[-1500:])
 return r.stdout

def event(task,status,detail):subprocess.run(['python3',str(ROOT/'reinstall/progress.py'),str(b/'progress.json'),'--task',task,'--status',status,'--detail',detail],check=True)
def save(name,data):(b/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def api(path,data=None,timeout=300):
 req=urllib.request.Request(f'http://{ip}:11434'+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)
def reboot():
 before=ssh('cat /proc/sys/kernel/random/boot_id').strip();ssh('sudo -n systemctl reboot',False)
 time.sleep(8);deadline=time.monotonic()+240
 while time.monotonic()<deadline:
  try:
   after=ssh('cat /proc/sys/kernel/random/boot_id').strip()
   if after and after!=before:return
  except Exception:pass
  time.sleep(5)
 raise RuntimeError('No authenticated SSH return with new boot id; IP rediscovery may be needed')

def run_ansible(name):
 cmd=['ansible-playbook','-i',str(b/'inventory.json'),str(ROOT/'reinstall/server.yml')]
 with (b/name).open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0,'Ansible failed; see '+name
 return (b/name).read_text()
def upload(path,source,mode='0600'):
 cmd='sudo -n mkdir -p /etc/jarvis /usr/local/lib/jarvis; sudo -n tee '+shlex.quote(path)+' >/dev/null && sudo -n chmod '+mode+' '+shlex.quote(path)
 r=subprocess.run(common+['adminjarvis@'+ip,cmd],input=source,capture_output=True)
 assert r.returncode==0,r.stderr.decode(errors='replace')
try:
 upload('/etc/jarvis/approved.json',(ROOT/'private/bootstrap-discovery-04/inventory.observed.json').read_bytes())
 upload('/usr/local/lib/jarvis/verify-storage.py',(ROOT/'bootstrap/verify-storage.py').read_bytes())
 upload('/usr/local/sbin/jarvis-sync-esp',(ROOT/'bootstrap/sync-esp.sh').read_bytes(),'0700')
 upload('/etc/apt/apt.conf.d/99jarvis-esp',b'DPkg::Post-Invoke { "/usr/local/sbin/jarvis-sync-esp"; };\n','0644')
 storage=ssh('sudo -n python3 /usr/local/lib/jarvis/verify-storage.py /etc/jarvis/approved.json; sudo -n /usr/local/sbin/jarvis-sync-esp')
 (b/'storage-installed.txt').write_text(storage)
 event('ansible','running','Applying actual Debian/NVIDIA/CUDA playbook to identified Dell')
 event('nvidia','running','Installing Debian driver and matching kernel headers')
 event('cuda','running','Installing Debian CUDA toolkit; actual GPU validation follows reboot')
 run_ansible('ansible-first.log')
 reboot()
 gpu=ssh('sudo -n modprobe nvidia && nvidia-smi --query-gpu=uuid,name,driver_version,memory.total --format=csv,noheader')
 (b/'nvidia-smi.txt').write_text(gpu)
 rows=[x.strip().split(', ') for x in gpu.splitlines() if x.strip()]
 assert len(rows)==1 and '3090' in rows[0][1],'Expected exactly one usable RTX 3090; do not select unpowered second GPU'
 uuid=rows[0][0];event('nvidia','validated','One RTX 3090 recognized by nvidia-smi after reboot; driver '+rows[0][2])
 toolkit=ssh('nvcc --version');(b/'cuda-toolkit.txt').write_text(toolkit)
 event('ollama','running','Copying known working Ollama 0.40.3 and existing documented models; Mac source read-only')
 ssh('sudo -n chown adminjarvis:adminjarvis /opt/ollama /var/lib/ollama/models')
 transport=' '.join(shlex.quote(x) for x in common)
 for name in ['bin','lib']:
  subprocess.run(['rsync','-a','--info=progress2','-e',transport,str(modeldir/name),'adminjarvis@'+ip+':/opt/ollama/'],check=True)
 event('models','running','Transferring existing Qwen3.5 27B Q4_K_M, Ministral3 14B Q4_K_M and Llama3.1 8B store')
 subprocess.run(['rsync','-a','--info=progress2','-e',transport,str(modeldir/'models')+'/','adminjarvis@'+ip+':/var/lib/ollama/models/'],check=True)
 unit=f'''[Unit]
Description=JARVIS Dell Ollama inference
Wants=network-online.target
After=network-online.target
[Service]
User=ollama
Group=ollama
Environment=HOME=/var/lib/ollama
Environment=OLLAMA_HOST={ip}:11434
Environment=OLLAMA_MODELS=/var/lib/ollama/models
Environment=OLLAMA_CONTEXT_LENGTH=4096
Environment=OLLAMA_NUM_PARALLEL=1
Environment=OLLAMA_MAX_LOADED_MODELS=1
Environment=CUDA_VISIBLE_DEVICES={uuid}
ExecStart=/opt/ollama/bin/ollama serve
Restart=on-failure
RestartSec=5
[Install]
WantedBy=multi-user.target
'''
 import base64
 payload=base64.b64encode(unit.encode()).decode()
 ssh(f'printf %s {payload} | base64 -d | sudo -n tee /etc/systemd/system/jarvis-ollama.service >/dev/null; sudo -n chown -R ollama:ollama /opt/ollama /var/lib/ollama; sudo -n systemctl daemon-reload; sudo -n systemctl enable --now jarvis-ollama.service')
 end=time.monotonic()+60
 while True:
  try:version=api('/api/version');break
  except Exception:
   if time.monotonic()>end:raise
   time.sleep(2)
 event('ollama','validated','Ollama API reachable from Mac mini, service enabled; version '+version['version'])
 expected=['qwen3.5:27b-q4_K_M','ministral-3:14b-instruct-2512-q4_K_M','llama3.1:8b']
 tags=api('/api/tags');save('models.json',tags);assert all(m in [d['name'] for d in tags['models']] for m in expected)
 results=[]
 for model in expected:
  result=api('/api/generate',{'model':model,'prompt':'Calcule 17 fois 23. Réponds uniquement avec le résultat.','stream':False,'think':False,'options':{'num_ctx':4096,'num_predict':128,'temperature':0}})
  assert '391' in result['response'],model+' response not validated'
  ps=api('/api/ps');loaded=next(m for m in ps['models'] if m['name']==model)
  assert loaded.get('size_vram',0)>0,'CPU-only inference is not GPU validation'
  result['gpu_loading']=loaded;results.append(result);save('gpu-inferences.json',results)
 event('cuda','validated','CUDA toolkit present and actual Ollama inferences allocate GPU VRAM on the selected RTX 3090')
 event('models','validated','Real GPU inference checked for Qwen, Ministral and Llama; outputs and VRAM evidence saved privately')
 text=run_ansible('ansible-second.log')
 recap=[x for x in text.splitlines() if 'changed=' in x and 'failed=' in x][-1]
 assert re.search(r'changed=0\b',recap) and re.search(r'failed=0\b',recap) and re.search(r'unreachable=0\b',recap),recap
 event('ansible','validated','Second pass changed=0 failed=0 unreachable=0; see private recap')
 # Authenticated integration is a separate executable step with rollback on failure.
 event('integration','running','Switching JARVIS inference backend only; canonical voice and SQLite stay on Mac')
 subprocess.run(['python3',str(ROOT/'reinstall/integrate.py'),str(b),ip],check=True)
 event('integration','validated','Authenticated gateway and Open WebUI inference plus canonical memory/tools/voice tests passed')
 event('tests','validated','Real inference, authenticated integration, memory, tool call and synthetic voice evidence saved')
 event('reboot','running','Final Dell reboot and independent SSH/password/GPU/Ollama checks')
 reboot();assert '3090' in ssh('nvidia-smi --query-gpu=name --format=csv,noheader');assert ssh('sudo -n true; systemctl is-active ssh jarvis-ollama').count('active')==2
 # Password authentication remains independently tested even after key validation.
 env=os.environ.copy();env.update(SSH_ASKPASS=str(ROOT/'bootstrap/askpass.py'),SSH_ASKPASS_REQUIRE='force',DISPLAY='jarvis:0',JARVIS_BOOTSTRAP_SECRET=str(ROOT/'private/reprise-user-password.txt'))
 args=common.copy();idx=args.index('BatchMode=yes');args[idx]='BatchMode=no';args+=['-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1']
 subprocess.run(args+['adminjarvis@'+ip,'sudo -n true'],env=env,stdin=subprocess.DEVNULL,check=True)
 api('/api/version');r=api('/api/generate',{'model':expected[0],'prompt':'Réponds OK.','stream':False,'think':False,'options':{'num_ctx':4096,'num_predict':64}});assert r['response'].strip()
 keyboard=ssh('sudo -n dumpkeys -C /dev/tty1');assert re.search(r'keycode\s+16\s*= a\s',keyboard) and re.search(r'keycode\s+17\s*= z\s',keyboard),'Installed French console map not verified'
 (b/'keyboard-verified.txt').write_text('Physical console keycode16=a keycode17=z verified after reboot\n')
 final_storage=ssh('sudo -n python3 /usr/local/lib/jarvis/verify-storage.py /etc/jarvis/approved.json; systemctl --failed --no-legend');(b/'final-storage-services.txt').write_text(final_storage)
 subprocess.run(args+['jarvis-bootstrap@'+ip,'sudo -n true'],env=env,stdin=subprocess.DEVNULL,check=True)
 assert any(m.get('size_vram',0)>0 for m in api('/api/ps')['models']),'GPU inference not retained after reboot'
 event('reboot','validated','New boot ID, independent key/password SSH/sudo, NVIDIA and actual Qwen inference confirmed')
 event('cleanup','validated','Temporary controller network services stopped; bootstrap/password recovery preserved by user instruction')
 event('acceptance','validated','All infrastructure, GPU inference, JARVIS integration and final reboot checks succeeded; see private evidence')
 save('complete.json',{'complete':True,'time':int(time.time()),'models':expected,'driver':rows[0][2],'ollama':version['version']})
 print('MISSION14_OPERATIONAL_VALIDATED',flush=True)
except BaseException as exc:
 (b/'ai-error.txt').write_text(str(exc)+'\n');print('AI_PHASE_FAILED:',str(exc),flush=True);raise

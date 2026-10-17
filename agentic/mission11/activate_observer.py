"""Codex/operator provisioning only. Reuse validated 13D-E SSH, no contact or changes to Dell."""
import ipaddress,json,os,pathlib,tempfile
P=pathlib.Path
if os.geteuid()!=0:raise SystemExit('Provisioning requires root; not a conversational tool')
base=P('/home/adminjarvis/JARVIS/13de-reprise/deployment/13de/private/reinstall-02')
progress=json.loads((base/'progress.json').read_text())
for phase in ('identity','debian','ssh-key'):
    if progress[phase]['status']!='validated':raise SystemExit('Validated 13D-E identity/access required')
if progress.get('reboot',{}).get('status')=='running':raise SystemExit('Reboot in progress; observer deferred')
address=str(ipaddress.ip_address(json.loads((base/'installed-ip.json').read_text())['ip']))
for name in ('identity','known_target'):
    path=base/name
    if not path.is_file() or path.stat().st_mode&0o077:raise SystemExit('Missing/protection failure of pinned SSH material')
policy=P('/etc/jarvis/host-policy.json');cfg=json.loads(policy.read_text())
cfg['remote_hosts']['dell-observe']={'address':address,'user':'adminjarvis','identity':str(base/'identity'),'known_hosts':str(base/'known_target'),'allow_admin':False,'ansible_enabled':False,'write_roots':[],
 'commands':{'identity':'uname -s','resources':'free -m; nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv','services':'systemctl is-active ssh.service ollama.service'}}
cfg['scope']['remote_observation']='Dell identity and key already validated by mission 13D-E; read-only while deployment is active'
fd,temp=tempfile.mkstemp(dir=policy.parent,prefix='.host-policy-');os.fchmod(fd,0o600)
with os.fdopen(fd,'w') as f:json.dump(cfg,f,ensure_ascii=False,indent=2);f.write('\n')
os.replace(temp,policy)
print('dell-observe provisioned from validated private 13D-E records; mutation and Ansible disabled; no remote operation executed')

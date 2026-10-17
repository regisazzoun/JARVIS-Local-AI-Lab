"""Operator-only persistent 11B grant, reusing pinned 13D-E SSH identity."""
import hashlib,json,os,pathlib,shlex,subprocess,tempfile,time
P=pathlib.Path
if os.geteuid()!=0:raise SystemExit('Root operator required; never callable by the model')
base=P('/home/adminjarvis/JARVIS/13de-reprise/deployment/13de/private/reinstall-02')
progress=json.loads((base/'progress.json').read_text())
for phase in ('identity','storage','debian','ssh-key','reboot','acceptance'):
    if progress.get(phase,{}).get('status')!='validated':raise SystemExit('Deployment not received: '+phase)
policy=P('/etc/jarvis/host-policy.json');cfg=json.loads(policy.read_text());h=cfg['remote_hosts']['dell-observe']
ssh=['ssh','-F','/dev/null','-i',h['identity'],'-oBatchMode=yes','-oIdentitiesOnly=yes','-oStrictHostKeyChecking=yes','-oGlobalKnownHostsFile=/dev/null','-oUserKnownHostsFile='+h['known_hosts'],'-oConnectTimeout=10',h['user']+'@'+h['address']]
def remote(command,stdin=None):
    r=subprocess.run(ssh+[command],input=stdin,text=True,capture_output=True,timeout=90)
    if r.returncode:raise RuntimeError('Remote operation failed: '+r.stderr[:500])
    return r.stdout
manifest=P('/home/adminjarvis/JARVIS/13de-reprise/deployment/13de/private/bootstrap-discovery-04/manifest.install-target.json')
m=json.loads(manifest.read_text())
def digest(v):return hashlib.sha256(str(v).strip().encode()).hexdigest()
# Hashes stored in a root-owned helper; no hardware identifiers returned to the model.
expected={'uuid':digest(m['uuid'].lower()),'vendor':m['vendor'],'product':m['product'],'disks':sorted((digest(d['serial']),d['model'].strip(),int(d['size'])) for d in m['disks'])}
code='''#!/usr/bin/python3
import hashlib,json,pathlib,subprocess
P=pathlib.Path
def digest(v):return hashlib.sha256(str(v).strip().encode()).hexdigest()
e=EXPECTED
if digest(P('/sys/class/dmi/id/product_uuid').read_text().strip().lower())!=e['uuid']:raise SystemExit('DMI mismatch')
for field,key in [('sys_vendor','vendor'),('product_name','product')]:
 if P('/sys/class/dmi/id',field).read_text().strip()!=e[key]:raise SystemExit('DMI mismatch')
rows=json.loads(subprocess.check_output(['lsblk','-b','-d','-J','-o','NAME,SERIAL,MODEL,SIZE,TYPE'],text=True))['blockdevices']
actual=sorted([digest(r['serial']),r['model'].strip(),int(r['size'])] for r in rows if r['name'].startswith('nvme') and r['type']=='disk')
if actual!=e['disks']:raise SystemExit('NVMe identity mismatch')
print('TARGET_IDENTITY_OK')
'''.replace('EXPECTED',repr(json.loads(json.dumps(expected))))
# Validate before provisioning: execute temporary program through sudo stdin, no disk changes.
assert remote('sudo -n python3 -',code).strip()=='TARGET_IDENTITY_OK'
remote('sudo -n python3 /usr/local/lib/jarvis/verify-storage.py /etc/jarvis/approved.json')
remote('sudo -n true && systemctl is-active ssh jarvis-ollama')
remote("sudo -n install -d -m 755 /usr/local/lib/jarvis /etc/jarvis/managed /etc/ollama; sudo -n install -d -o adminjarvis -g adminjarvis -m 755 /var/lib/jarvis/projects /opt/jarvis/compute")
remote('sudo -n tee /usr/local/lib/jarvis/check-target.py >/dev/null',code)
remote('sudo -n chmod 700 /usr/local/lib/jarvis/check-target.py')
backup=P('/var/lib/jarvis-agent/backups');backup.mkdir(mode=0o700,exist_ok=True)
(backup/('host-policy-before-11b-'+str(time.time_ns())+'.json')).write_text(policy.read_text())
h.update(allow_admin=True,ansible_enabled=True,
    write_roots=['/var/lib/jarvis/projects','/opt/jarvis/compute','/etc/jarvis/managed','/etc/ollama'],
    privileged_write_roots=['/etc/jarvis/managed','/etc/ollama'],
    identity_check='sudo -n /usr/local/lib/jarvis/check-target.py',
    packages=['hello','jq','git','rsync','curl','python3-venv','python3-pip','python3-dev','build-essential','cmake','pkg-config','libopenblas-dev','ffmpeg','pciutils','nvme-cli','nvidia-driver','nvidia-cuda-toolkit'],
    services={'jarvis-ollama.service':['status','show','is-active','is-enabled','start','restart','enable'], 'nvidia-persistenced.service':['status','show','is-active','is-enabled','start','restart','enable'], 'ssh.service':['status','show','is-active','is-enabled']})
h['commands'].update(identity='sudo -n /usr/local/lib/jarvis/check-target.py && id -un && sudo -n true && echo SUDO_OK', services='systemctl is-active ssh.service jarvis-ollama.service', models="curl -fsS http://192.168.1.75:11434/api/tags", storage='sudo -n python3 /usr/local/lib/jarvis/verify-storage.py /etc/jarvis/approved.json')
cfg['scope'].update(mission='11 / 11B',authorization='Owner instruction 2026-10-17: persistent Dell IA administration; JL-02 excluded',remote_observation='Dell deployment received; persistent SSH/Ansible administration for authorized IA missions; pinned key and runtime DMI/NVMe guard')
fd,tmp=tempfile.mkstemp(dir=policy.parent,prefix='.host-policy-');os.fchmod(fd,0o600)
with os.fdopen(fd,'w') as f:json.dump(cfg,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
os.replace(tmp,policy)
print('11B persistent policy installed; existing SSH identity reused; target and RAID verified; backup protected')

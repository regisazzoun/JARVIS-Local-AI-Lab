#!/usr/bin/env python3
"""Explicitly authorized takeover, independent OpenSSH sessions, no TOFU fallback."""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import argparse,base64,hashlib,json,os,pathlib,re,subprocess,tempfile,time
p=argparse.ArgumentParser();p.add_argument('settings',type=pathlib.Path);a=p.parse_args()
os.umask(0o077)
s=json.loads(a.settings.read_text()); manifest=json.loads(pathlib.Path(s['manifest']).read_text())
assert s.get('administration_authorized') is True, 'separate administrative authorization required'
assert s['host'] in s['approved_addresses'] and s['host'] not in ('192.168.1.99','127.0.0.1','localhost'), 'target address'
assert s.get('host_key_origin') == 'reviewed-authenticated-installation-report', 'host key must be bound to reviewed installation report'
key=s['host_public_key'].split();assert len(key)>=2 and key[0]=='ssh-ed25519'
assert re.fullmatch(r'[0-9.]+',s['host']), 'IPv4 only'
state=a.settings.parent; known=state/'known_hosts'
line=f"{s['host']} {key[0]} {key[1]}\n"
if known.exists():assert known.read_text()==line,'pinned host key changed'
else:
 with known.open('x') as f:f.write(line)
identity=pathlib.Path(s['identity_file']).resolve()
assert identity.is_file(), 'select an existing authorized deployment identity'
pub=subprocess.check_output(['ssh-keygen','-y','-f',str(identity)],text=True).strip()
assert hashlib.sha256(base64.b64decode(pub.split()[1])).hexdigest()==s['authorized_public_key_sha256'], 'public key authorization'
common=['ssh','-F','/dev/null','-o','StrictHostKeyChecking=yes','-o',f'UserKnownHostsFile={known}','-o','GlobalKnownHostsFile=/dev/null','-o','ControlMaster=no','-o','ControlPath=none','-o','ConnectTimeout=15','-o','ConnectionAttempts=1']
def ssh(user,command,password=False):
 opts=['-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1'] if password else ['-o','BatchMode=yes','-o','IdentitiesOnly=yes','-i',str(identity),'-o','PreferredAuthentications=publickey','-o','PasswordAuthentication=no']
 env=os.environ.copy()
 if password:env.update(SSH_ASKPASS=str(pathlib.Path(__file__).with_name('askpass.py')),SSH_ASKPASS_REQUIRE='force',DISPLAY='jarvis-bootstrap:0',JARVIS_BOOTSTRAP_SECRET=str(pathlib.Path(s['password_file']).resolve()))
 return subprocess.run(common+opts+[f"{user}@{s['host']}",command],env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,check=True).stdout
probe="sudo -n python3 -c 'import json,pathlib; p=pathlib.Path(\"/sys/class/dmi/id\"); print(json.dumps({n:(p/n).read_text().strip() for n in (\"sys_vendor\",\"product_name\",\"product_uuid\")}))'"
def verify_identity(user,password=False):
 r=json.loads(ssh(user,probe,password))
 assert r==dict(sys_vendor=manifest['vendor'],product_name=manifest['product'],product_uuid=manifest['uuid']), 'remote DMI differs'
# Resume after interrupted cleanup: first test permanent access, never lock bootstrap first.
try:verify_identity('jarvisadmin')
except (subprocess.CalledProcessError,AssertionError,ValueError):
 verify_identity('jarvis-bootstrap',True)
 encoded=base64.b64encode((pub+'\n').encode()).decode()
 script=f'''set -eu
id jarvisadmin >/dev/null 2>&1 || useradd -m -s /bin/bash jarvisadmin
install -d -m 700 -o jarvisadmin -g jarvisadmin /home/jarvisadmin/.ssh
touch /home/jarvisadmin/.ssh/authorized_keys
key=$(printf %s {encoded} | base64 -d)
grep -qxF "$key" /home/jarvisadmin/.ssh/authorized_keys || printf '%s\n' "$key" >> /home/jarvisadmin/.ssh/authorized_keys
chown jarvisadmin:jarvisadmin /home/jarvisadmin/.ssh/authorized_keys
chmod 600 /home/jarvisadmin/.ssh/authorized_keys
usermod -p '*' jarvisadmin
printf '%s\\n' 'jarvisadmin ALL=(ALL:ALL) NOPASSWD: ALL' > /etc/sudoers.d/jarvisadmin
chmod 440 /etc/sudoers.d/jarvisadmin
visudo -cf /etc/sudoers.d/jarvisadmin
'''
 payload=base64.b64encode(script.encode()).decode()
 ssh('jarvis-bootstrap',f'printf %s {payload} | base64 -d | sudo -n /bin/sh',True)
# NEW independent TCP/SSH public-key-only connection and sudo verification.
verify_identity('jarvisadmin')
ssh('jarvisadmin',"sudo -n true && sudo -n install -d -m 700 /var/lib/jarvis && printf '%s\\n' independent-key-verified | sudo -n tee /var/lib/jarvis/permanent-key-verified >/dev/null && sudo -n /usr/local/sbin/jarvis-revoke-bootstrap")
verify_identity('jarvisadmin') # Positive key proof again after revocation.
state_text=ssh('jarvisadmin',"sudo -n passwd -S jarvis-bootstrap; sudo -n /usr/sbin/sshd -T -C user=jarvis-bootstrap,host=dell,addr=192.168.1.99")
assert re.search(r'^jarvis-bootstrap L ',state_text,re.M) and re.search(r'^passwordauthentication no$',state_text,re.M),'revocation not confirmed'
pathlib.Path(s['password_file']).unlink(missing_ok=True)
pathlib.Path(s['password_file']).with_name('password.sha512').unlink(missing_ok=True)
(state/'takeover-complete.json').write_text(json.dumps(dict(host=s['host'],uuid=manifest['uuid'],completed=int(time.time()),independent_key_verified=True,bootstrap_revoked=True),indent=2)+'\n')
inventory={'all':{'children':{'dell':{'hosts':{'dell-precision':dict(ansible_host=s['host'],ansible_user='jarvisadmin',ansible_ssh_private_key_file=str(identity),ansible_ssh_common_args=f'-F /dev/null -o StrictHostKeyChecking=yes -o UserKnownHostsFile={known} -o PasswordAuthentication=no -o IdentitiesOnly=yes',deployment_scope='dell-approved',dell_configuration_authorized=True,approved_uuid=manifest['uuid'],approved_addresses=s['approved_addresses'],storage_acceptance_complete=False,bootstrap_takeover_complete=True)}}}}}
(state/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
print('Independent key SSH and sudo confirmed; bootstrap revoked; local plaintext secret removed.')

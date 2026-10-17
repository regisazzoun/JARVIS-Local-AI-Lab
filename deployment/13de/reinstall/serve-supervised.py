#!/usr/bin/env python3
"""Scoped PXE transport and pinned SSH controller. Disk installation is separately observable."""
import argparse,json,os,pathlib,pwd,signal,subprocess,time,socket,concurrent.futures,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);a=p.parse_args();b=a.session.resolve();os.umask(0o077)
assert b.is_relative_to((ROOT/'private').resolve())
account=pwd.getpwnam('adminjarvis');children=[];stop=False
manifest=json.loads((ROOT/'private/bootstrap-discovery-04/inventory.observed.json').read_text())
def lower():os.initgroups(account.pw_name,account.pw_gid);os.setgid(account.pw_gid);os.setuid(account.pw_uid)
def halt(*_):
 global stop;stop=True
signal.signal(signal.SIGTERM,halt);signal.signal(signal.SIGINT,halt)
def event(task,status,detail):
 subprocess.run(['python3',str(ROOT/'reinstall/progress.py'),str(b/'progress.json'),'--task',task,'--status',status,'--detail',detail],preexec_fn=lower,check=True)
def spawn(name,args,root=False):
 f=(b/(name+'.log')).open('a');os.chown(f.fileno(),account.pw_uid,account.pw_gid)
 child=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT,preexec_fn=None if root else lower,start_new_session=True);f.close();children.append(child);return child
mac=re.search(r'^dhcp-host=([0-9a-f:]+),', (b/'proxy.conf').read_text(),re.M).group(1)
def discover():
 raw=subprocess.check_output(['ip','-j','neigh'],text=True)
 return [v['dst'] for v in json.loads(raw) if v.get('lladdr','').lower()==mac and v.get('state')!=['FAILED']]
def probe(ip,port):
 try:
  with socket.create_connection((ip,port),timeout=1):return True
 except OSError:return False
def scan():
 def ping(n):subprocess.run(['ping','-c','1','-W','1',f'192.168.1.{n}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 with concurrent.futures.ThreadPoolExecutor(max_workers=64) as pool:list(pool.map(ping,range(1,255)))
def ssh(ip,port,cmd,password=False,user='root'):
 known=b/('known_installer' if port==2222 else 'known_target')
 key=(b/('host_key.pub' if port==2222 else 'target_host_key.pub')).read_text().split()
 known.write_text(f'[{ip}]:{port} {key[0]} {key[1]}\n' if port!=22 else f'{ip} {key[0]} {key[1]}\n');os.chown(known,account.pw_uid,account.pw_gid)
 args=['ssh','-F','/dev/null','-p',str(port),'-o','StrictHostKeyChecking=yes','-o',f'UserKnownHostsFile={known}','-o','GlobalKnownHostsFile=/dev/null','-o','ControlMaster=no','-o','ConnectTimeout=8','-o','IdentitiesOnly=yes','-i',str(b/'identity')]
 env=os.environ.copy()
 if password:
  args+=['-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1'];env.update(SSH_ASKPASS=str(ROOT/'bootstrap/askpass.py'),SSH_ASKPASS_REQUIRE='force',DISPLAY='jarvis:0',JARVIS_BOOTSTRAP_SECRET=str(ROOT/'private/reprise-user-password.txt'))
 else:args+=['-o','BatchMode=yes','-o','PasswordAuthentication=no']
 return subprocess.run(args+[f'{user}@{ip}',cmd],capture_output=True,text=True,env=env,preexec_fn=lower,stdin=subprocess.DEVNULL)
def check_identity(ip,port,user):
 cmd='cat /sys/class/dmi/id/product_name; '+('sudo -n ' if user!='root' else '')+'cat /sys/class/dmi/id/product_uuid'
 r=ssh(ip,port,cmd,user=user);assert r.returncode==0,r.stderr
 assert r.stdout.splitlines()==[manifest['product'],manifest['uuid']],'identity differs'
try:
 assert not any(t.get('table',{}).get('name')=='jarvis_bootstrap' for t in json.loads(subprocess.check_output(['/usr/sbin/nft','-j','list','tables']))['nftables'])
 subprocess.run(['/usr/sbin/nft','-f',str(b/'restrict.nft')],check=True)
 http=spawn('http',['python3','-u','-m','http.server','8088','--bind','192.168.1.99','--directory',str(b/'http')])
 dns=spawn('dnsmasq',['/usr/sbin/dnsmasq','--keep-in-foreground','--conf-file='+str(b/'proxy.conf')],True)
 time.sleep(2);assert http.poll() is None and dns.poll() is None
 (b/'ready.json').write_text(json.dumps({'ready':True,'pid':os.getpid(),'time':int(time.time())})+'\n');os.chown(b/'ready.json',account.pw_uid,account.pw_gid)
 print('PXE_READY_WAITING_PHYSICAL_BOOT',flush=True)
 deadline=time.monotonic()+28800;lastscan=0;ip=None
 while not stop and time.monotonic()<deadline:
  for candidate in discover():
   if probe(candidate,2222):ip=candidate;break
  if ip:break
  if time.monotonic()-lastscan>45:scan();lastscan=time.monotonic()
  time.sleep(3)
 assert ip and not stop,'No installer SSH before stop/deadline'
 check_identity(ip,2222,'root');event('pxe','validated','PXE physical boot and independent SSH with locally pinned host key confirmed')
 event('identity','validated','DMI/UUID match private manifest; embedded guard checks exact NVMe identities')
 (b/'installer-ip.json').write_text(json.dumps({'ip':ip})+'\n')
 # Capture read-only state before launching the new-root installation.
 r=ssh(ip,2222,'/bin/sh /guard-physical.sh && cat /proc/mdstat && blkid');assert r.returncode==0,r.stderr
 (b/'storage-preflight.txt').write_text(r.stdout)
 event('storage','running','Preserve existing mirror/GPT/ESP; verify healthy members before root format')
 r=ssh(ip,2222,'/bin/sh /jarvis/install-preserve.sh >/run/jarvis-install.log 2>&1 </dev/null &');assert r.returncode==0,r.stderr
 event('debian','running','Fresh Debian installation controlled through pinned installer SSH')
 while not stop and time.monotonic()<deadline:
  r=ssh(ip,2222,'cat /run/jarvis-install-progress.log 2>/dev/null; test -e /run/jarvis-install-complete')
  (b/'installer-progress.txt').write_text(r.stdout)
  logs=ssh(ip,2222,'tail -n 200 /run/jarvis-install.log');(b/'installer-tail.log').write_text(logs.stdout)
  if 'FAILED installation' in r.stdout:raise RuntimeError('Installer failed; SSH available; see private installer-tail.log')
  if r.returncode==0:break
  time.sleep(10)
 assert not stop and r.returncode==0,'Installation interrupted'
 event('debian','validated','Fresh Debian completed, sshd configuration checked and signed EFI copies match; see installer log')
 event('storage','validated','Existing healthy RAID preserved; root alone formatted; both ESP copies verified')
 event('accounts','running','Accounts created; independent authentication checks pending reboot')
 ssh(ip,2222,'sync; reboot -f')
 time.sleep(15);ip=None
 while not stop and time.monotonic()<deadline:
  scan()
  for candidate in discover():
   if probe(candidate,22):
    r=ssh(candidate,22,'sudo -n true',user='adminjarvis')
    if r.returncode==0:ip=candidate;break
  if ip:break
  time.sleep(5)
 assert ip,'Installed SSH not available'
 check_identity(ip,22,'adminjarvis')
 r=ssh(ip,22,'sudo -n true',password=True,user='adminjarvis');assert r.returncode==0,r.stderr
 event('ssh-password','validated','Independent password authentication and sudo succeeded for adminjarvis')
 r=ssh(ip,22,'sudo -n true',user='adminjarvis');assert r.returncode==0,r.stderr
 event('ssh-key','validated','Independent key authentication and sudo succeeded; password access retained')
 event('accounts','validated','adminjarvis password/key/sudo verified; jarvis-bootstrap configured with same user password')
 (b/'installed-ip.json').write_text(json.dumps({'ip':ip})+'\n')
 inv={'all':{'children':{'dell':{'hosts':{'dell':{'ansible_host':ip,'ansible_user':'adminjarvis','ansible_ssh_private_key_file':str(b/'identity'),'ansible_ssh_common_args':f'-F /dev/null -o StrictHostKeyChecking=yes -o UserKnownHostsFile={b / "known_target"} -o IdentitiesOnly=yes','approved_uuid':manifest['uuid']}}}}}}
 (b/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n');os.chown(b/'inventory.json',account.pw_uid,account.pw_gid)
 event('ansible','running','Infrastructure SSH validated; AI server playbook ready for execution')
 print('INFRASTRUCTURE_SSH_VALIDATED_AI_PHASE_REQUIRED',flush=True)
except BaseException as exc:
 (b/'controller-error.txt').write_text(str(exc)+'\n');print('CONTROLLER_STOP:',str(exc),flush=True);raise
finally:
 for child in children:
  if child.poll() is None:
   os.killpg(child.pid,signal.SIGTERM)
   try:child.wait(timeout=3)
   except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
 subprocess.run(['/usr/sbin/nft','delete','table','inet','jarvis_bootstrap'])
 (b/'ready.json').unlink(missing_ok=True)

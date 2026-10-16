#!/usr/bin/env python3
"""Authorized single-PXE session, first-boot callback, takeover and Ansible supervision."""
if not __debug__:raise RuntimeError('Safety assertions required')
import argparse,hashlib,json,os,pathlib,pwd,signal,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);a=p.parse_args()
b=a.session.resolve();assert b.is_relative_to((ROOT/'private').resolve());os.umask(0o077)
s=json.loads((b/'session.json').read_text());authorization=json.loads(pathlib.Path(s['authorization']).read_text())
assert authorization['installation_authorized'] and authorization['administration_authorized'] and authorization['network_for_installation_authorized']
assert s['manifest_sha256']==hashlib.sha256(pathlib.Path(s['manifest']).read_bytes()).hexdigest()
qualification=json.loads(pathlib.Path(s['qualification']).read_text());assert qualification['dual_esp_boot_qualified']
account=pwd.getpwnam('adminjarvis');children=[];logs=[];installed=False;stop=False;assets_stop_at=None

def status(phase, **details):
 record=dict(phase=phase,supervisor_pid=os.getpid(),updated_at=int(time.time()),**details)
 target=b/'status.json';target.write_text(json.dumps(record,indent=2)+'\n');os.chown(target,account.pw_uid,account.pw_gid)

def halt(*_):
 global stop
 stop=True
signal.signal(signal.SIGTERM,halt);signal.signal(signal.SIGINT,halt)
def lower():
 os.initgroups(account.pw_name,account.pw_gid);os.setgid(account.pw_gid);os.setuid(account.pw_uid)
def spawn(name,cmd,demote=True,console=False):
 f=None
 if not console:
  f=open(b/(name+'.log'),'a');os.chown(f.fileno(),account.pw_uid,account.pw_gid);logs.append(f)
 child=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,preexec_fn=lower if demote else None,start_new_session=True)
 children.append((name,child));return child

def terminate(child):
 if child.poll() is None:
  os.killpg(child.pid,signal.SIGTERM)
  try:child.wait(timeout=3)
  except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
try:
 subprocess.run(['sha256sum','-c','SESSION-SHA256SUMS'],cwd=b,check=True)
 interfaces=json.loads(subprocess.check_output(['ip','-j','-4','addr','show','dev','enp4s0']))
 assert any(v['local']=='192.168.1.99' for d in interfaces for v in d['addr_info'])
 tables=json.loads(subprocess.check_output(['nft','-j','list','tables']))
 assert not any(v.get('table',{}).get('name')=='jarvis_bootstrap' for v in tables['nftables'])
 subprocess.run(['nft','-f',str(b/'restrict.nft')],check=True);installed=True
 callback_settings=json.loads((b/'receiver.json').read_text());assert not pathlib.Path(callback_settings['output']).exists(), 'existing callback: resume SSH configuration, do not reinstall'
 receiver=spawn('receiver',['python3','-u',str(ROOT/'discovery/receive.py'),str(b/'receiver.json')],console=True)
 http=spawn('http',['python3','-u','-m','http.server','8088','--bind','192.168.1.99','--directory',str(b/'http')])
 dns=spawn('dnsmasq',['/usr/sbin/dnsmasq','--keep-in-foreground','--conf-file='+str(b/'proxy.conf')],False)
 status('awaiting-pxe')
 print('INSTALLATION_READY_PID',os.getpid(),'waiting for sole human PXE boot',flush=True)
 deadline=time.monotonic()+28800
 while not stop and time.monotonic()<deadline and receiver.poll() is None:
  if assets_stop_at is None and (b/'http.log').exists() and 'GET /initrd.gz HTTP/1.1" 200' in (b/'http.log').read_text():
   assets_stop_at=time.monotonic()+120;status('installing');print('INSTALLER_FETCHED: PXE/HTTP will stop after transfer window; callback remains',flush=True)
  if assets_stop_at is not None and time.monotonic()>=assets_stop_at:
   terminate(dns);terminate(http);assets_stop_at=float('inf');print('PXE_HTTP_STOPPED_WAITING_INSTALLED_CALLBACK',flush=True)
  if assets_stop_at is None:
   assert http.poll() is None and dns.poll() is None,'service startup failed'
  time.sleep(1)
 if stop or receiver.poll() is None:raise RuntimeError('session stopped or callback timeout; target state must be inspected, never reinstall blindly')
 assert receiver.returncode==0,'callback failed'
 terminate(dns);terminate(http)
 callback=json.loads((b/'receiver.json').read_text());report=pathlib.Path(callback['output'])
 assert report.is_file(),'no installed report'
 status('taking-over')
 target=b/'takeover.json'
 subprocess.run(['python3',str(ROOT/'bootstrap/import-install-report.py'),str(report),s['manifest'],s['identity'],s['password'],str(target)],preexec_fn=lower,check=True)
 config=json.loads(target.read_text());config['administration_authorized']=True;target.write_text(json.dumps(config,indent=2)+'\n');os.chown(target,account.pw_uid,account.pw_gid)
 receipt=b/'storage-receipt.json';receipt.write_text(json.dumps(dict(storage_acceptance_complete=True,manifest_sha256=s['manifest_sha256'],dual_esp_boot_qualified=True,qualification=s['qualification']))+'\n');os.chown(receipt,account.pw_uid,account.pw_gid)
 controller=spawn('configure',['python3','-u',str(ROOT/'bootstrap/configure.py'),str(target),str(receipt)],console=True)
 while controller.poll() is None and not stop and time.monotonic()<deadline:time.sleep(1)
 assert controller.poll()==0,'configuration incomplete; private logs retained, do not reinstall'
 status('complete',base_installed=True,permanent_ssh_verified=True,bootstrap_revoked=True,ansible_idempotent=True)
 print('DEPLOYMENT_COMPLETE: Debian base, key SSH, bootstrap revoked, Ansible second pass unchanged',flush=True)
except BaseException as exc:
 status('stopped' if stop else 'failed',error=str(exc))
 raise
finally:
 for _,child in reversed(children):terminate(child)
 for f in logs:f.close()
 if installed:subprocess.run(['nft','delete','table','inet','jarvis_bootstrap'],check=True)
 print('INSTALLATION_SESSION_SERVICES_STOPPED',flush=True)

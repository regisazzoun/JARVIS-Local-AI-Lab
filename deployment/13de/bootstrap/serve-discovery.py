#!/usr/bin/env python3
"""Activate ONLY after explicit network approval; stop all session services on receipt."""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import argparse,datetime,hashlib,json,os,pathlib,pwd,signal,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);a=p.parse_args()
b=a.session.resolve();assert b.is_relative_to((ROOT/'private').resolve()) and not a.session.is_symlink()
os.umask(0o077); account=pwd.getpwnam('adminjarvis');children=[];handles=[];installed=False;stop=False

def halt(*_):
 global stop
 stop=True
signal.signal(signal.SIGTERM,halt);signal.signal(signal.SIGINT,halt)
def lower():
 os.initgroups(account.pw_name,account.pw_gid);os.setgid(account.pw_gid);os.setuid(account.pw_uid)
def spawn(name,command,demote=False,console=False):
 log=None
 if not console:
  log=open(b/(name+'.log'),'a');os.chown(log.fileno(),account.pw_uid,account.pw_gid);handles.append(log)
 child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,preexec_fn=lower if demote else None)
 children.append((name,child));return child
try:
 subprocess.run(['sha256sum','-c','SESSION-SHA256SUMS'],cwd=b,check=True)
 addresses=json.loads(subprocess.check_output(['ip','-j','-4','addr','show','dev','enp4s0']))
 assert any(v['local']=='192.168.1.99' for d in addresses for v in d['addr_info']), 'JARVIS address changed'
 assert not (b/'hardware-report.txt').exists(), 'report already exists; prepare new session'
 subprocess.run(['/usr/sbin/dnsmasq','--test','--conf-file='+str(b/'proxy.conf')],check=True)
 # nft refuses an existing named table: never replace/flush an unrelated table.
 tables=json.loads(subprocess.check_output(['nft','-j','list','tables']))
 assert not any(v.get('table',{}).get('name')=='jarvis_bootstrap' for v in tables['nftables']), 'session table already exists'
 subprocess.run(['nft','-f',str(b/'restrict.nft')],check=True);installed=True
 receiver=spawn('receiver',['python3','-u',str(ROOT/'discovery/receive.py'),str(b/'receiver.json')],True,True)
 spawn('http',['python3','-u','-m','http.server','8088','--bind','192.168.1.99','--directory',str(b/'http')],True)
 spawn('dnsmasq',['/usr/sbin/dnsmasq','--keep-in-foreground','--conf-file='+str(b/'proxy.conf')])
 print('DISCOVERY_SESSION_PID',os.getpid(),'15 minute limit; all services stop on report or error',flush=True)
 deadline=time.monotonic()+900
 while not stop and time.monotonic()<deadline:
  if receiver.poll() is not None:break
  for name,child in children:
   if child.poll() is not None:raise RuntimeError(name+' stopped unexpectedly')
  time.sleep(.5)
finally:
 for _,child in reversed(children):
  if child.poll() is None:
   try:os.killpg(child.pid,signal.SIGTERM)
   except ProcessLookupError:pass
 for _,child in children:
  try:child.wait(timeout=3)
  except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
 for f in handles:f.close()
 if installed:subprocess.run(['nft','delete','table','inet','jarvis_bootstrap'],check=True)
 print('DISCOVERY_SESSION_STOPPED_FILTER_REMOVED',flush=True)

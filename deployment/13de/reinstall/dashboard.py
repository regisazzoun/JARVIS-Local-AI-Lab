#!/usr/bin/env python3
"""Relay verified task ledger to installer console and installed SSH-readable view."""
import argparse,json,pathlib,subprocess,time,socket,re
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);a=p.parse_args();b=a.session.resolve();root=pathlib.Path(__file__).resolve().parents[1]
mac=re.search(r'^dhcp-host=([0-9a-f:]+),',(b/'proxy.conf').read_text(),re.M).group(1)
end=time.monotonic()+28800
while time.monotonic()<end:
 try:
  text=subprocess.check_output(['python3',str(root/'reinstall/progress.py'),str(b/'progress.json')],text=True)
  (b/'progress-console.txt').write_text(text)
  neighbors=json.loads(subprocess.check_output(['ip','-j','neigh'],text=True))
  for n in neighbors:
   if n.get('lladdr','').lower()!=mac:continue
   ip=n['dst']
   for port,user,keyname in [(2222,'root','host_key.pub'),(22,'adminjarvis','target_host_key.pub')]:
    try:
     with socket.create_connection((ip,port),timeout=1):pass
    except OSError:continue
    key=(b/keyname).read_text().split();known=b/('dashboard-known-'+str(port));known.write_text((f'[{ip}]:{port}' if port!=22 else ip)+f' {key[0]} {key[1]}\n')
    ssh=['ssh','-F','/dev/null','-p',str(port),'-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o',f'UserKnownHostsFile={known}','-o','GlobalKnownHostsFile=/dev/null','-o','ConnectTimeout=3','-o','IdentitiesOnly=yes','-i',str(b/'identity'),user+'@'+ip]
    cmd='mkdir -p /run/jarvis; cat > /run/jarvis/progress.txt; printf "\\033[2J\\033[H" > /dev/tty1; cat /run/jarvis/progress.txt > /dev/tty1' if port==2222 else 'sudo -n mkdir -p /run/jarvis; sudo -n tee /run/jarvis/progress.txt >/dev/null'
    r=subprocess.run(ssh+[cmd],input=text,text=True,capture_output=True,timeout=8)
    if r.returncode==0:break
  if (b/'complete.json').exists() or (b/'ai-error.txt').exists() or (b/'controller-error.txt').exists():break
 except Exception as exc:print(type(exc).__name__,flush=True)
 time.sleep(10)

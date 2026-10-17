#!/usr/bin/env python3
"""Measured RAID/model-transfer progress; never validates acceptance by elapsed time."""
import argparse,json,pathlib,re,subprocess,time
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);a=p.parse_args();b=a.session.resolve();root=pathlib.Path(__file__).resolve().parents[1]
ip=json.loads((b/'installed-ip.json').read_text())['ip']
common=['ssh','-F','/dev/null','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o',f'UserKnownHostsFile={b/"known_target"}','-o','GlobalKnownHostsFile=/dev/null','-o','IdentitiesOnly=yes','-o','ConnectTimeout=5','-i',str(b/'identity'),'adminjarvis@'+ip]
def update(task,pct,detail):subprocess.run(['python3',str(root/'reinstall/progress.py'),str(b/'progress.json'),'--task',task,'--status','running','--percent',str(pct),'--measured','--detail',detail],stdout=subprocess.DEVNULL,check=True)
end=time.monotonic()+28800
while time.monotonic()<end:
 try:
  state=json.loads((b/'progress.json').read_text())
  r=subprocess.run(common+['for md in /sys/block/md*/md; do cat "$md/sync_action"; cat "$md/sync_completed"; done'],capture_output=True,text=True,timeout=10)
  lines=r.stdout.splitlines()
  if r.returncode==0 and len(lines)>=2 and lines[0]=='resync':
   nums=re.findall(r'\d+',lines[1])
   if len(nums)==2 and int(nums[1])>0:
    pct=round(100*int(nums[0])/int(nums[1]),1);update('storage',pct,'RAID1 existant en resynchronisation après le premier reboot; réception finale différée')
  if state.get('models',{}).get('status')=='running':
   log=(b/'ai-phase.log').read_text(errors='replace')[-100000:]
   values=re.findall(r'\b(\d{1,3})%\s+\S+[kMGT]?B/s',log)
   if values:update('models',int(values[-1]),'Transfert mesuré du magasin de modèles existant via rsync; tests inférence encore nécessaires')
  if any((b/f).exists() for f in ['complete.json','ai-error.txt']):break
 except Exception:pass
 time.sleep(15)

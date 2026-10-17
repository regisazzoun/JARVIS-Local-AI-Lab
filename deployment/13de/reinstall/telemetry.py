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
  r=subprocess.run(common+['cat /proc/mdstat'],capture_output=True,text=True,timeout=10)
  match=re.search(r'resync\s*=\s*([0-9.]+)%.*?finish=([^ ]+)',r.stdout)
  if r.returncode==0 and match:
   pct=float(match.group(1));update('storage',pct,'Resynchronisation RAID1 mesurée dans /proc/mdstat ; reste estimé '+match.group(2))
  if state.get('models',{}).get('status')=='running':
   log=(b/'ai-phase.log').read_text(errors='replace')[-100000:]
   marker=log.rfind('MODEL_TRANSFER_BEGIN')
   log=log[marker:] if marker>=0 else ''
   values=re.findall(r'\b(\d{1,3})%\s+\S+[kMGT]?B/s',log)
   if values:update('models',int(values[-1]),'Transfert mesuré du magasin de modèles existant via rsync; tests inférence encore nécessaires')
  if (b/'complete.json').exists():break
 except Exception:pass
 time.sleep(15)

#!/usr/bin/env python3
"""Gate final reboot on the newly requested desktop installation; no new approvals."""
import pathlib,json,sys,subprocess,time,os,signal
b=pathlib.Path(sys.argv[1]).resolve();root=pathlib.Path(__file__).resolve().parents[1]
end=time.monotonic()+21600
while time.monotonic()<end:
 if (b/'plasma-installed.json').exists():break
 state=json.loads((b/'progress.json').read_text())
 if state['plasma']['status']=='failed':raise RuntimeError('KDE failed; reboot remains held; inspect plasma-install.log')
 time.sleep(3)
else:raise RuntimeError('KDE installation timeout; reboot remains held')
old=json.loads((b/'reception-suspended.json').read_text());pid=old['pid'];proc=pathlib.Path(f'/proc/{pid}')
if proc.exists():
 assert proc.joinpath('stat').read_text().split()[21]==old['starttime'],'Controller PID reused'
 cmd=proc.joinpath('cmdline').read_bytes().split(b'\0');assert str(root/'reinstall/finish-ai.py').encode() in cmd and str(b).encode() in cmd
 assert os.getpgid(pid)==pid
 os.killpg(pid,signal.SIGTERM);os.killpg(pid,signal.SIGCONT)
with (b/'reception.log').open('a') as f:
 child=subprocess.Popen(['python3','-u',str(root/'reinstall/finish-ai.py'),str(b),'--resume-reception'],stdout=f,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,start_new_session=True)
print('KDE installed; final reception resumed',child.pid,flush=True)

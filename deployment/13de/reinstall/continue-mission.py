#!/usr/bin/env python3
"""Await infrastructure controller completion, then continue AI/integration without a new GO."""
import argparse,os,pathlib,pwd,subprocess,time
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);a=p.parse_args();b=a.session.resolve();root=pathlib.Path(__file__).resolve().parents[1];account=pwd.getpwnam('adminjarvis');os.umask(0o077)
def lower():os.initgroups(account.pw_name,account.pw_gid);os.setgid(account.pw_gid);os.setuid(account.pw_uid)
end=time.monotonic()+28800
while time.monotonic()<end:
 if (b/'controller-error.txt').exists():raise RuntimeError('Infrastructure failed: inspect controller logs; no AI operations launched')
 if (b/'installed-ip.json').exists() and (b/'inventory.json').exists() and not (b/'ready.json').exists():break
 time.sleep(3)
else:raise RuntimeError('Infrastructure completion timeout; no AI operations launched')
for file in b.iterdir():
 if file.is_file() and not file.is_symlink():os.chown(file,account.pw_uid,account.pw_gid)
print('Infrastructure complete; continuing authorized AI phase',flush=True)
log=b/'ai-phase.log'
with log.open('a') as f:
 os.chown(f.fileno(),account.pw_uid,account.pw_gid)
 r=subprocess.run(['python3','-u',str(root/'reinstall/finish-ai.py'),str(b)],stdout=f,stderr=subprocess.STDOUT,preexec_fn=lower)
assert r.returncode==0,'AI/integration phase incomplete; private ai-phase.log retained'
print('CONTINUOUS_MISSION_COMPLETED',flush=True)

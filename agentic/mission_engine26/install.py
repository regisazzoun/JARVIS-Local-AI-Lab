"""Install additive engine26 modules; preserve existing databases/policy/services."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

MODULES=['missions.py','mission_store.py','durable_tools.py','durable_cycle.py','tools.py','skill_lab.py','verification.py','mission_reporting.py','mission_actions.py']

def main():
    if os.geteuid()!=0:raise SystemExit('sudo required')
    root=Path('/opt/jarvis/conversation');repo=Path(__file__).resolve().parents[2]
    policy=Path('/etc/jarvis/host-policy.json');before=hashlib.sha256(policy.read_bytes()).hexdigest()
    import sqlite3
    c=sqlite3.connect(root/'runtime/missions.sqlite')
    if c.execute("SELECT count(*) FROM missions WHERE state='running'").fetchone()[0]:raise SystemExit('Interrupt active mission at tool boundary first')
    backup=Path('/var/backups/jarvis/mission-engine26')/str(time.time_ns());backup.mkdir(parents=True,mode=0o700)
    receipts=[]
    for name in MODULES:
        src=repo/'agentic/engine_v2/jarvis'/name;dst=root/'jarvis'/name
        compile(src.read_text(),str(src),'exec')
        if dst.exists():shutil.copy2(dst,backup/name)
        tmp=dst.with_suffix('.engine26');shutil.copyfile(src,tmp);os.chmod(tmp,0o644);os.replace(tmp,dst)
        receipts.append({'module':name,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
    assert hashlib.sha256(policy.read_bytes()).hexdigest()==before
    subprocess.run(['systemctl','restart','jarvis-conversation'],check=True)
    print(json.dumps({'backup':str(backup),'modules':receipts,'policy_unchanged':True}))

if __name__=='__main__':main()

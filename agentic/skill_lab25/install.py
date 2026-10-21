"""Run as authorized operator after installing requirements in conversation venv.

Copies modules, backs up affected code, preserves owner policy and all databases.
The service restart is explicit; skill candidates remain inactive until tested.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

repo=Path(__file__).resolve().parents[2]
runtime=Path('/opt/jarvis/conversation')
backup=Path('/var/backups/jarvis/skill-lab25')/str(time.time_ns())

def main():
    if os.geteuid()!=0:raise SystemExit('Run installer via sudo as authorized operator')
    python=runtime/'.venv/bin/python'
    subprocess.run([str(python),'-c','import jsonschema,mcp'],check=True)
    policy=Path('/etc/jarvis/host-policy.json');before=hashlib.sha256(policy.read_bytes()).hexdigest()
    backup.mkdir(parents=True,mode=0o700)
    for source,target in [('jarvis/'+n,str(runtime/'jarvis'/n)) for n in ['skill_lab.py','mcp_gateway.py','tools.py','host_client.py']]+[('broker/host_bridge.py','/usr/local/lib/jarvis-host/host_bridge.py')]:
        src=repo/'agentic/engine_v2'/source;dst=Path(target)
        compile(src.read_text(),str(src),'exec')
        if dst.exists():shutil.copy2(dst,backup/dst.name)
        temp=dst.with_suffix('.skilllab25');shutil.copyfile(src,temp);os.chmod(temp,0o644);os.replace(temp,dst)
    assert hashlib.sha256(policy.read_bytes()).hexdigest()==before
    # Candidates only: no tests or activation attributed to JARVIS by installer.
    code='''import json,sys
from pathlib import Path
from jarvis.tools import Registry
from jarvis.memory import Memory
from jarvis.skill_lab import SkillLab
r=Registry(Memory("/opt/jarvis/conversation/runtime/memory.sqlite"),"/opt/jarvis/conversation")
lab=SkillLab(r)
for p in Path(sys.argv[1]).glob("*.json"): print(lab.define(json.loads(p.read_text())))
'''
    subprocess.run(['/usr/sbin/runuser','-u','adminjarvis','--',str(python),'-c',code,str(repo/'agentic/skill_lab25/skills')],cwd=runtime,check=True)
    subprocess.run(['systemctl','restart','jarvis-host-bridge','jarvis-conversation'],check=True)
    print(json.dumps({'backup':str(backup),'policy_unchanged':True}))

if __name__=='__main__':main()

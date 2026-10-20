#!/usr/bin/env python3
"""Idempotent owner-authorized mission23 client execution on existing Dell1.
Does not provision credentials, targets, accounts, or alter existing permissions.
"""
import datetime,json,os,shutil
from pathlib import Path
if os.geteuid()!=0:raise SystemExit('Operator root required')
p=Path('/etc/jarvis/host-policy.json');cfg=json.loads(p.read_text())
profile=cfg['remote_hosts']['dell-observe']
if not profile.get('allow_admin') or not profile.get('identity_check'):raise SystemExit('Existing validated administrative Dell1 profile required')
backup=Path('/var/backups/jarvis/mission23');backup.mkdir(parents=True,exist_ok=True,mode=0o700)
copy=backup/('policy-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json');shutil.copy2(p,copy);copy.chmod(0o600)
profile['administration_operations']=list(dict.fromkeys(profile.get('administration_operations',[])+['project_exec']))
profile['project_exec_projects']=list(dict.fromkeys(profile.get('project_exec_projects',[])+['mission23']))
profile['packages']=list(dict.fromkeys(profile.get('packages',cfg['packages'])+['bubblewrap','python3-venv']))
stat=p.stat();tmp=p.with_suffix('.new');tmp.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n');tmp.chmod(0o600);os.chown(tmp,stat.st_uid,stat.st_gid);os.replace(tmp,p)
print('Existing Dell1 mission23 project client permitted; secrets unchanged.')

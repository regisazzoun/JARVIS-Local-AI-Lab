#!/usr/bin/env python3
"""Operator deployment: private consistent backups, syntax check, atomic module replacement.
Run as root. Does not replace config, credentials, model files, memory or host policy.
"""
import compileall
import datetime
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess

source=Path(__file__).resolve().parent
target=Path('/opt/jarvis/conversation')
if os.geteuid()!=0:raise SystemExit('Exécuter comme opérateur root')
if not compileall.compile_dir(source/'jarvis',quiet=1):raise SystemExit('Compilation échouée')
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup=Path('/var/backups/jarvis/mission22')/stamp
backup.mkdir(parents=True,mode=0o700)
os.chmod(backup,0o700)
shutil.copytree(target/'jarvis',backup/'jarvis')
for name in ('memory.sqlite','missions.sqlite'):
    path=target/'runtime'/name
    if path.exists():
        with sqlite3.connect(path) as src,sqlite3.connect(backup/name) as dest:src.backup(dest)
        os.chmod(backup/name,0o600)
for module in (source/'jarvis').glob('*.py'):
    dest=target/'jarvis'/module.name
    temp=dest.with_suffix('.py.new')
    shutil.copyfile(module,temp);os.chmod(temp,0o644);os.replace(temp,dest)
# Owner explicitly excludes artificial resource-saving ceilings.
override=Path('/etc/systemd/system/jarvis-conversation.service.d/22-resources.conf')
override.parent.mkdir(parents=True,exist_ok=True)
override.write_text('[Service]\nMemoryMax=infinity\nTasksMax=infinity\n')
subprocess.run(['systemctl','daemon-reload'],check=True)
subprocess.run(['systemctl','restart','jarvis-conversation.service'],check=True)
print('Installed; private backup:',backup)

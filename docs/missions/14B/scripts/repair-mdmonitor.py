"""Target-only missing install configuration, no array mutation."""
from pathlib import Path
import subprocess,json,time
root=Path('/var/lib/jarvis/mission14b');manifest=json.loads((root/'manifest.json').read_text());assert Path('/sys/class/dmi/id/product_uuid').read_text().strip()==manifest['uuid']
config=Path('/etc/mdadm/mdadm.conf');old=config.read_text();(root/'mdadm-conf-before-monitor-fix.txt').write_text(old)
program=Path('/usr/local/sbin/jarvis-md-event');program.write_text('#!/bin/sh\nexec /usr/bin/logger -p daemon.warning -t jarvis-mdmonitor -- "$@"\n');program.chmod(0o755)
text='\n'.join(line for line in old.splitlines() if not line.startswith(('PROGRAM ','MONITORDELAY ')))+'\nPROGRAM /usr/local/sbin/jarvis-md-event\nMONITORDELAY 60\n';assert [x for x in old.splitlines() if x.startswith('ARRAY ')]==[x for x in text.splitlines() if x.startswith('ARRAY ')]
config.write_text(text)
subprocess.run(['systemctl','restart','mdmonitor'],check=True)
r=subprocess.run(['systemctl','is-active','mdmonitor'],capture_output=True,text=True);result={'observed_at':time.time(),'actor':'Codex targeted installation correction','cause':'Stock mdmonitor refuses to start without MAILADDR or PROGRAM','correction':'Local journal alert program, no mail transport or external message; preserve ARRAY definitions','active':r.returncode==0,'state':r.stdout.strip()};(root/'mdmonitor-correction.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert r.returncode==0

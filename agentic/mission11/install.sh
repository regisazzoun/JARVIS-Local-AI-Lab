#!/bin/bash
set -euo pipefail
src=$(cd -- "$(dirname -- "$0")" && pwd)
if [ "$(id -u)" != 0 ]; then exec sudo -- "$0" "$@"; fi
/usr/bin/python3 -m py_compile "$src"/*.py
install -d -m 755 /usr/local/lib/jarvis-host /etc/jarvis /var/lib/jarvis
install -d -o adminjarvis -g adminjarvis -m 750 /var/lib/jarvis/projects /etc/jarvis/managed /var/log/jarvis-agent /home/adminjarvis/JARVIS/agent-workspaces
install -m 644 "$src/host_bridge.py" /usr/local/lib/jarvis-host/host_bridge.py
# Do not overwrite permanent grants on upgrade.
if [ ! -e /etc/jarvis/host-policy.json ]; then install -m 644 "$src/host-policy.json" /etc/jarvis/host-policy.json; fi
install -m 644 "$src/jarvis-host-bridge.service" "$src/jarvis-agent-proof.service" /etc/systemd/system/
backup=$(mktemp -d /var/backups/jarvis-m11.XXXXXX)
chmod 700 "$backup"
for name in core tools server; do cp -p "/opt/jarvis/conversation/jarvis/$name.py" "$backup/"; done
cp -p /opt/jarvis/conversation/identity/JARVIS-v2.md "$backup/"
for name in core tools server host_client missions task_tools; do install -o adminjarvis -g adminjarvis -m 644 "$src/$name.py" "/opt/jarvis/conversation/jarvis/$name.py"; done
install -o adminjarvis -g adminjarvis -m 644 "$src/JARVIS-v2.md" /opt/jarvis/conversation/identity/JARVIS-v2.md
install -d -m 700 /var/lib/jarvis-agent/ssh
if [ ! -e /var/lib/jarvis-agent/ssh/id_ed25519 ]; then
    ssh-keygen -q -t ed25519 -N '' -f /var/lib/jarvis-agent/ssh/id_ed25519 -C jarvis-mission11-local
fi
python3 - <<'PYKEY'
from pathlib import Path
import os,pwd
p=Path('/var/lib/jarvis-agent/ssh/known_hosts');key=Path('/etc/ssh/ssh_host_ed25519_key.pub').read_text().split()
p.write_text('127.0.0.1 '+key[0]+' '+key[1]+'\n');p.chmod(0o600)
public=Path('/var/lib/jarvis-agent/ssh/id_ed25519.pub').read_text().strip()
a=Path('/home/adminjarvis/.ssh/authorized_keys');a.parent.mkdir(mode=0o700,exist_ok=True);text=a.read_text() if a.exists() else ''
if public not in text:a.write_text(text.rstrip()+'\nrestrict,from="127.0.0.1" '+public+'\n')
account=pwd.getpwnam('adminjarvis');os.chown(a,account.pw_uid,account.pw_gid);a.chmod(0o600)
PYKEY
python3 - "$src" <<'PYUI'
from pathlib import Path
import sys
p=Path('/opt/jarvis/conversation/static/app.js');base=p.read_text().split('// Durable missions use the same')[0].rstrip()
p.write_text(base+'\n'+(Path(sys.argv[1])/'missions-ui.js').read_text())
PYUI
sed -i 's/Mode laboratoire isolé · commandes autorisées/Mode agent · hôte autorisé ou laboratoire/' /opt/jarvis/conversation/static/index.html
systemctl daemon-reload
systemctl enable --now jarvis-host-bridge.service
systemctl restart jarvis-host-bridge.service
for attempt in {1..40}; do [ -S /run/jarvis-host/bridge.sock ] && break; sleep .1; done
[ -S /run/jarvis-host/bridge.sock ]
systemctl restart jarvis-conversation.service
printf 'Installed; private code backup: %s\n' "$backup"

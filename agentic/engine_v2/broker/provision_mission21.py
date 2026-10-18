#!/usr/bin/env python3
"""Narrow persistent capabilities authorized by owner missions21/22.
Never alters SSH keys, identities, hardware guards, other profiles or storage.
"""
import datetime,json,os,pathlib,shutil
p=pathlib.Path('/etc/jarvis/host-policy.json')
if os.geteuid()!=0:raise SystemExit('Operator root required')
cfg=json.loads(p.read_text());h=cfg['remote_hosts']['dell-observe']
if not h.get('allow_admin') or not h.get('identity_check'):raise SystemExit('Existing Dell administration and target guard required')
backup=pathlib.Path('/var/backups/jarvis/mission22/policy-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json')
backup.parent.mkdir(mode=0o700,parents=True,exist_ok=True);shutil.copy2(p,backup);backup.chmod(0o600)
cfg['diagnostics']=sorted(set(cfg.get('diagnostics',[]))|{'failed_units','recent_warnings','kernel_warnings','storage_state'})
for unit in ('ssh.service','NetworkManager.service','systemd-networkd.service','nvidia-persistenced.service','mdmonitor.service'):
 cfg.setdefault('services',{}).setdefault(unit,['status','is-active'])
h['administration_operations']=sorted(set(h.get('administration_operations',[]))|{'supervision_install','supervision_test','desktop_configure','desktop_test','desktop_network_test','desktop_gateway_configure','tailscale_configure','tailscale_status'})
cfg['desktop_gateway_enabled']=True
cfg.setdefault('services',{}).setdefault('jarvis-dell-desktop-gateway.service',['status','is-active','is-enabled','start','restart','enable'])
h['packages']=sorted(set(h.get('packages',cfg.get('packages',[])))|{'tigervnc-standalone-server','tigervnc-tools','xauth','dbus-x11','python3-pycryptodome','x11-xkb-utils'})
h['commands']['desktop_status']="printf 'PACKAGES\\n'; dpkg-query -W -f='${Package} ${Version} ${db:Status-Status}\\n' plasma-workspace tigervnc-standalone-server tigervnc-tools dbus-x11 python3-pycryptodome 2>/dev/null; command -v startplasma-x11; ls /usr/share/xsessions /usr/share/wayland-sessions 2>/dev/null; loginctl list-sessions --no-legend; systemctl is-active sddm jarvis-desktop-vnc.service jarvis-desktop-plasma.service 2>/dev/null; true"
h['commands']['desktop_logs']='systemctl status jarvis-desktop-vnc.service jarvis-desktop-plasma.service --no-pager; journalctl -u jarvis-desktop-vnc.service -u jarvis-desktop-plasma.service -n 40 --no-pager; true'
h['commands']['journal_recent']='systemctl --failed --no-pager; sudo -n journalctl -b -p warning -n 35 --no-pager -o short-iso'
h['commands']['supervision_status']='systemctl status jarvis-supervision.timer jarvis-supervision.service --no-pager; cat /var/lib/jarvis-supervision/latest.json 2>/dev/null; true'
for name in ('jarvis-supervision.service','jarvis-supervision.timer','jarvis-desktop-vnc.service','jarvis-desktop-plasma.service'):
 h.setdefault('services',{})[name]=sorted(set(h.get('services',{}).get(name,[]))|{'status','is-active','is-enabled','start','restart','enable'})
temp=p.with_suffix('.mission22.tmp');temp.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n');temp.chmod(0o600);os.replace(temp,p)
print('Narrow mission21/22 capabilities provisioned; private policy backup retained.')

"""Fixed, owner-authorized mission21 operations. No model-supplied root program.
SSH credentials remain in the broker. VNC credentials are generated on the Dell.
"""
import textwrap

SUPERVISION = r"""
import json, pathlib, subprocess
config=pathlib.Path('/etc/jarvis/managed/mission21-supervision.json')
if not config.exists():raise SystemExit('Deploy mission21-supervision.json via Ansible first')
settings=json.loads(config.read_text());interval=int(settings.get('interval_seconds',60))
if not 10<=interval<=86400:raise SystemExit('interval_seconds out of valid timer range')
folder=pathlib.Path('/usr/local/lib/jarvis-supervision');folder.mkdir(parents=True,exist_ok=True);folder.chmod(0o755)
collector='''import json,os,pathlib,shutil,time
memory={line.split(':')[0]:line.split(':')[1].strip() for line in pathlib.Path('/proc/meminfo').read_text().splitlines()}
usage=shutil.disk_usage('/')
result={'timestamp':time.time(),'load':os.getloadavg(),'memory_total':memory.get('MemTotal'),'memory_available':memory.get('MemAvailable'),'disk_total':usage.total,'disk_free':usage.free,'collector':'mission21','gpu':'Use canonical GPU telemetry; not collected in this confined service'}
p=pathlib.Path('/var/lib/jarvis-supervision/latest.json');temp=p.with_suffix('.tmp');temp.write_text(json.dumps(result,sort_keys=True));temp.replace(p)
'''
(folder/'collect.py').write_text(collector);(folder/'collect.py').chmod(0o644)
unit='''[Unit]
Description=JARVIS lightweight supervision mission21
[Service]
Type=oneshot
User=nobody
Group=nogroup
StateDirectory=jarvis-supervision
ExecStart=/usr/bin/python3 /usr/local/lib/jarvis-supervision/collect.py
NoNewPrivileges=yes
ProtectHome=yes
ProtectSystem=strict
PrivateDevices=yes
PrivateNetwork=yes
ReadWritePaths=/var/lib/jarvis-supervision
'''
pathlib.Path('/etc/systemd/system/jarvis-supervision.service').write_text(unit)
pathlib.Path('/etc/systemd/system/jarvis-supervision.timer').write_text('[Unit]\nDescription=JARVIS supervision timer\n[Timer]\nOnBootSec=30\nOnUnitActiveSec='+str(interval)+'\nUnit=jarvis-supervision.service\n[Install]\nWantedBy=timers.target\n')
for command in (['systemctl','daemon-reload'],['systemctl','enable','--now','jarvis-supervision.timer'],['systemctl','start','jarvis-supervision.service']):subprocess.run(command,check=True)
print(json.dumps({'installed':True,'interval_seconds':interval,'service':'jarvis-supervision.service','timer':'jarvis-supervision.timer','collector_source':'Codex infrastructure, invoked by JARVIS when broker caller is JARVIS-runtime'}))
"""

SUPERVISION_TEST = r'''
import json,pathlib,subprocess,time
p=pathlib.Path('/var/lib/jarvis-supervision/latest.json')
previous=json.loads(p.read_text()).get('timestamp',0) if p.exists() else 0
subprocess.run(['systemctl','start','jarvis-supervision.service'],check=True)
current=json.loads(p.read_text())
assert current['timestamp']>previous,'Collector did not create a fresh result'
active=subprocess.run(['systemctl','is-active','jarvis-supervision.timer'],capture_output=True,text=True)
assert active.returncode==0,'Timer inactive'
print(json.dumps({'fresh_result':True,'timer':active.stdout.strip(),'metrics':current}))
'''

DESKTOP = r"""
import json,pathlib,subprocess,os,pwd,secrets,shutil
user='adminjarvis';account=pwd.getpwnam(user)
for name in ('Xtigervnc','tigervncpasswd','startplasma-x11','dbus-run-session','xauth'):
 if not shutil.which(name):raise SystemExit('Missing package/binary: '+name)
private=pathlib.Path('/etc/jarvis/private');private.mkdir(mode=0o700,parents=True,exist_ok=True);private.chmod(0o700)
plain=private/'mission21-vnc-password'
if not plain.exists():plain.write_text(secrets.token_urlsafe(12)[:8]);plain.chmod(0o600)
password=plain.read_text().strip()
subprocess.run(['loginctl','enable-linger',user],check=True)
folder=pathlib.Path(account.pw_dir)/'.config/tigervnc';folder.mkdir(parents=True,exist_ok=True)
for parent in (folder.parent,folder):os.chown(parent,account.pw_uid,account.pw_gid)
folder.chmod(0o700)
pwfile=folder/'passwd';encoded=subprocess.run(['tigervncpasswd','-f'],input=(password+'\n').encode(),capture_output=True,check=True).stdout
pwfile.write_bytes(encoded);pwfile.chmod(0o600);os.chown(pwfile,account.pw_uid,account.pw_gid)
auth=folder/'Xauthority'
if not auth.exists():
 auth.touch(mode=0o600)
 subprocess.run(['xauth','-f',str(auth)],input=('add :21 . '+secrets.token_hex(16)+'\n').encode(),check=True,capture_output=True)
 os.chown(auth,account.pw_uid,account.pw_gid)
server='''[Unit]
Description=JARVIS private virtual desktop VNC
After=network.target
[Service]
User=adminjarvis
Group=adminjarvis
ExecStart=/usr/bin/Xtigervnc :21 -rfbport 5921 -localhost yes -SecurityTypes VncAuth -PasswordFile '''+str(pwfile)+''' -auth '''+str(auth)+''' -geometry 1440x900 -depth 24 -AlwaysShared -nolisten tcp
Restart=on-failure
[Install]
WantedBy=multi-user.target
'''
plasma='''[Unit]
Description=JARVIS isolated Plasma X11 session
Requires=jarvis-desktop-vnc.service
After=jarvis-desktop-vnc.service user@1000.service
Wants=user@1000.service
[Service]
User=adminjarvis
Group=adminjarvis
Environment=DISPLAY=:21
Environment=XAUTHORITY='''+str(auth)+'''
Environment=XDG_RUNTIME_DIR=/run/user/'''+str(account.pw_uid)+'''
Environment=QT_QPA_PLATFORM=xcb
Environment=LIBGL_ALWAYS_SOFTWARE=1
Environment=XDG_SESSION_TYPE=x11
ExecStart=/usr/bin/dbus-run-session -- /usr/bin/startplasma-x11
Restart=on-failure
RestartSec=5
[Install]
WantedBy=multi-user.target
'''
pathlib.Path('/etc/systemd/system/jarvis-desktop-vnc.service').write_text(server)
pathlib.Path('/etc/systemd/system/jarvis-desktop-plasma.service').write_text(plasma)
for cmd in (['systemctl','daemon-reload'],['systemctl','enable','--now','jarvis-desktop-vnc.service','jarvis-desktop-plasma.service']):subprocess.run(cmd,check=True)
print(json.dumps({'configured':True,'display':':21','port':5921,'binding':'loopback only; access over existing SSH LAN/Tailscale tunnels','password':'generated/reused privately on Dell; not returned to model','physical_session':'not replaced'}))
"""

# This program intentionally returns only authentication/framebuffer facts, never credentials.
DESKTOP_TEST = r'''
import pathlib,socket,struct,json,time
from Cryptodome.Cipher import DES
password=pathlib.Path('/etc/jarvis/private/mission21-vnc-password').read_bytes().strip()
with socket.create_connection(('127.0.0.1',5921),timeout=15) as s:
 def exact(n):
  value=b''
  while len(value)<n:
   piece=s.recv(n-len(value))
   if not piece:raise RuntimeError('RFB connection closed')
   value+=piece
  return value
 version=exact(12);assert version.startswith(b'RFB ');s.sendall(b'RFB 003.008\n')
 types=exact(exact(1)[0]);assert 2 in types,'VncAuth unavailable';s.sendall(b'\x02')
 challenge=exact(16);key=bytes(int(f'{x:08b}'[::-1],2) for x in password[:8].ljust(8,b'\0'))
 s.sendall(DES.new(key,DES.MODE_ECB).encrypt(challenge));assert exact(4)==b'\0\0\0\0','RFB authentication failed'
 s.sendall(b'\x01');initial=exact(24);width,height=struct.unpack('!HH',initial[:4]);name=exact(struct.unpack('!I',initial[20:24])[0])
 s.sendall(struct.pack('!BBHi',2,0,1,0));s.sendall(struct.pack('!BBHHHH',3,0,0,0,width,height))
 typ=exact(1)[0];assert typ==0,'Framebuffer update unavailable';exact(1);rectangles=struct.unpack('!H',exact(2))[0]
 assert rectangles>0,'Empty framebuffer';header=exact(12);x,y,w,h,encoding=struct.unpack('!HHHHi',header)
 assert encoding==0,'Raw framebuffer unavailable';pixels=exact(w*h*4);assert pixels
shells=[]
for proc in pathlib.Path('/proc').glob('[0-9]*'):
 try:
  if (proc/'comm').read_text().strip()=='plasmashell' and b'DISPLAY=:21' in (proc/'environ').read_bytes().split(b'\0'):shells.append(int(proc.name))
 except (PermissionError,FileNotFoundError,ProcessLookupError):pass
assert shells,'No Plasma shell on virtual display21'
print(json.dumps({'rfb_authenticated':True,'framebuffer_received':True,'width':width,'height':height,'plasma_display21':True,'transport_test':'Dell loopback only; LAN/Tailscale client test separate'}))
'''


def program(action):
    return textwrap.dedent({'supervision_install':SUPERVISION,'supervision_test':SUPERVISION_TEST,
                            'desktop_configure':DESKTOP,'desktop_test':DESKTOP_TEST}[action])


def network_test(profile, common, run):
    """Real Mac-side RFB clients through pinned SSH LAN and Tailscale tunnels.
    The password is received only inside this privileged process and never returned.
    """
    import ipaddress,json,pathlib,shlex,socket,struct,subprocess,time
    from Cryptodome.Cipher import DES
    code="import json,pathlib,subprocess; print(json.dumps({'password':pathlib.Path('/etc/jarvis/private/mission21-vnc-password').read_text().strip(),'addresses':json.loads(subprocess.check_output(['ip','-j','address'])),'route':json.loads(subprocess.check_output(['ip','-j','route','get','1.1.1.1']))}))"
    response=run(['/usr/bin/ssh']+common+[profile['user']+'@'+profile['address'],shlex.join(['sudo','-n','python3','-c',code])],30)
    if response['returncode']:return {'returncode':1,'stderr':'Private VNC credential/route discovery failed; no credential returned'}
    private=json.loads(response['stdout']);password=private['password'].encode()
    addresses={}
    lan=private['route'][0].get('prefsrc')
    if lan:addresses['LAN']=lan
    for interface in private['addresses']:
        for address in interface.get('addr_info',[]):
            if address.get('family')=='inet' and ipaddress.ip_address(address['local']) in ipaddress.ip_network('100.64.0.0/10'):addresses['Tailscale']=address['local']
    results=[]
    for transport,address in addresses.items():
        process=None
        try:
            pinned=common+['-oHostKeyAlias='+profile['address']]
            identity=run(['/usr/bin/ssh']+pinned+[profile['user']+'@'+address,profile['identity_check']],30)
            if identity['returncode']:raise RuntimeError('Pinned target identity not confirmed')
            with socket.socket() as probe:probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
            process=subprocess.Popen(['/usr/bin/ssh']+pinned+['-oExitOnForwardFailure=yes','-N','-L',f'127.0.0.1:{port}:127.0.0.1:5921',profile['user']+'@'+address],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            for _ in range(100):
                if process.poll() is not None:raise RuntimeError('SSH tunnel exited')
                try:client=socket.create_connection(('127.0.0.1',port),timeout=.2);break
                except OSError:time.sleep(.1)
            else:raise RuntimeError('SSH tunnel unavailable')
            with client as s:
                s.settimeout(20)
                def exact(count):
                    data=b''
                    while len(data)<count:
                        block=s.recv(count-len(data))
                        if not block:raise RuntimeError('RFB closed')
                        data+=block
                    return data
                assert exact(12).startswith(b'RFB ');s.sendall(b'RFB 003.008\n')
                types=exact(exact(1)[0]);assert 2 in types;s.sendall(b'\x02')
                challenge=exact(16);key=bytes(int(f'{x:08b}'[::-1],2) for x in password[:8].ljust(8,b'\0'))
                s.sendall(DES.new(key,DES.MODE_ECB).encrypt(challenge));assert exact(4)==b'\0\0\0\0'
                s.sendall(b'\x01');initial=exact(24);width,height=struct.unpack('!HH',initial[:4]);exact(struct.unpack('!I',initial[20:24])[0])
                s.sendall(struct.pack('!BBHi',2,0,1,0));s.sendall(struct.pack('!BBHHHH',3,0,0,0,width,height))
                assert exact(1)==b'\0';exact(1);assert struct.unpack('!H',exact(2))[0]>0
                x,y,w,h,encoding=struct.unpack('!HHHHi',exact(12));assert encoding==0
                size=len(exact(w*h*4));assert size>0
                results.append({'transport':transport,'identity_pinned':True,'authenticated':True,'framebuffer_bytes':size,'width':width,'height':height})
        except Exception as exc:results.append({'transport':transport,'authenticated':False,'error':type(exc).__name__+': '+str(exc)})
        finally:
            if process:
                process.terminate()
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:process.kill();process.wait()
    ok={x['transport'] for x in results if x.get('authenticated')}=={'LAN','Tailscale'}
    return {'returncode':0 if ok else 1,'stdout':json.dumps({'clients':'Real headless RFB clients on Mac mini; no physical MacBook test','results':results}),'credentials':'not returned'}

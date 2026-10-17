#!/usr/bin/env python3
import pathlib,json,subprocess,sys
b=pathlib.Path(sys.argv[1]).resolve();root=pathlib.Path(__file__).resolve().parents[1];ip=json.loads((b/'installed-ip.json').read_text())['ip']
cmd=['ssh','-F','/dev/null','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o',f'UserKnownHostsFile={b/"known_target"}','-o','GlobalKnownHostsFile=/dev/null','-o','IdentitiesOnly=yes','-o','ConnectTimeout=10','-i',str(b/'identity'),'adminjarvis@'+ip,'sudo -n sh -s']
with (b/'plasma-install.log').open('a') as f:r=subprocess.run(cmd,input=(root/'reinstall/install-plasma.sh').read_bytes(),stdout=f,stderr=subprocess.STDOUT)
status='validated' if r.returncode==0 else 'failed'
detail='KDE Plasma et session X11 installés, SDDM activé pour le reboot ; ouverture de session graphique à vérifier après redémarrage' if r.returncode==0 else 'Installation KDE arrêtée ; consulter plasma-install.log, reboot final retenu'
subprocess.run(['python3',str(root/'reinstall/progress.py'),str(b/'progress.json'),'--task','plasma','--status',status,'--detail',detail],check=True)
if r.returncode:sys.exit(r.returncode)
(b/'plasma-installed.json').write_text(json.dumps({'packages_configured':True,'sddm_enabled':True,'x11_session_available':True,'graphical_login_tested':False})+'\n')
print('PLASMA_INSTALLATION_VALIDATED',flush=True)

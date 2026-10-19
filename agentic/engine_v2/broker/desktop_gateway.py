#!/usr/bin/env python3
"""Private Mac -> verified Dell VNC forward. Credentials never leave root."""
import os
import subprocess
from host_bridge import policy


def main():
    cfg=policy();profile=cfg['remote_hosts']['dell-observe']
    if not cfg.get('desktop_gateway_enabled') or not profile.get('allow_admin') or not profile.get('identity_check'):
        raise SystemExit('Owner-authorized gateway and target guard required')
    common=['-F','/dev/null','-i',profile['identity'],'-oBatchMode=yes','-oIdentitiesOnly=yes',
            '-oGlobalKnownHostsFile=/dev/null','-oStrictHostKeyChecking=yes',
            '-oUserKnownHostsFile='+profile['known_hosts'],'-oConnectTimeout=10']
    target=profile['user']+'@'+profile['address']
    checked=subprocess.run(['/usr/bin/ssh']+common+[target,profile['identity_check']],capture_output=True)
    if checked.returncode:raise SystemExit('Dell target identity not confirmed; no forward opened')
    argv=['/usr/bin/ssh']+common+['-NT','-oExitOnForwardFailure=yes','-oServerAliveInterval=30',
          '-oServerAliveCountMax=3','-L','127.0.0.1:5921:127.0.0.1:5921',target]
    os.execv(argv[0],argv)

if __name__=='__main__':main()

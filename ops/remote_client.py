"""SSH transport for the supervised remote unit; no shell job interpolation."""
import json
import subprocess

HOSTS={'dell-1':'jarvis-dell1','dell-2':'jarvis-dell2'}
SCRIPT='/home/adminjarvis/JARVIS/idle-scheduler-runtime/remote_runner.py'

def request(node,action,ident,manifest=None):
    value={'action':action,'id':ident}
    if manifest is not None:value['manifest']=manifest
    p=subprocess.run(['/usr/bin/ssh','-o','BatchMode=yes','-o','ConnectTimeout=4','-o','ServerAliveInterval=3','-o','ServerAliveCountMax=1',HOSTS[node],'/usr/bin/python3',SCRIPT],input=json.dumps(value),capture_output=True,text=True,timeout=18)
    try:reply=json.loads(p.stdout)
    except ValueError:raise RuntimeError('Remote outcome unknown: '+p.stderr[:200])
    if p.returncode or not reply.get('ok'):raise RuntimeError(reply.get('error','Remote RPC failed'))
    return reply['state']

class RemoteProcess:
    def __init__(self,job):
        self.job=job;self.returncode=None
        self.state=request(job['node'],'start',job['id'],job['manifest'])
    def poll(self):
        self.state=request(self.job['node'],'renew',self.job['id'])
        status=self.state['status']
        if status in ('running','starting'):self.returncode=None
        elif status=='completed':self.returncode=0
        elif status=='paused':self.returncode=75
        else:self.returncode=1
        return self.returncode
    def terminate(self):
        self.state=request(self.job['node'],'pause',self.job['id'])
        if self.state['systemd'].get('ActiveState') in ('active','activating','deactivating'):
            raise RuntimeError('Remote stop unconfirmed')
        self.returncode=75
        return self.state

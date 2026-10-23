"""Scoped remote project runtime; options come only from owner policy."""
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile


def project_program(root, command, gpu=False):
    if not root.startswith(('/opt/jarvis-lab/', '/home/')) or '..' in root.split('/'):
        raise ValueError('Invalid configured project root')
    prefix='root_path='+repr(root)+'\ncommand='+repr(command)+'\ngpu='+repr(bool(gpu))+'\n'
    return prefix+'''import pathlib,subprocess,os
root=pathlib.Path(root_path)
root.mkdir(parents=True,exist_ok=True)
assert root.resolve()==root, 'Configured project root must be canonical'
argv=['/usr/bin/bwrap','--die-with-parent','--new-session','--unshare-pid','--unshare-ipc','--unshare-uts','--cap-drop','ALL','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--symlink','usr/sbin','/sbin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/etc']
for path in ['/etc/alternatives','/etc/ssl','/etc/resolv.conf','/etc/hosts','/etc/passwd','/etc/group','/etc/nsswitch.conf','/etc/ld.so.cache']:
 if pathlib.Path(path).exists():argv+=['--ro-bind',path,path]
if gpu:
 argv+=['--ro-bind','/sys','/sys']
 for path in pathlib.Path('/dev').glob('nvidia*'):
  argv+=['--dev-bind',str(path),str(path)]
argv+=['--bind',str(root),str(root),'--chdir',str(root),'--clearenv','--setenv','HOME',str(root),'--setenv','PATH','/usr/bin:/bin','--setenv','LANG','C.UTF-8','--setenv','HF_HOME',str(root/'cache'),'--','/bin/bash','-c',command]
raise SystemExit(subprocess.call(argv))
'''


def transfer_file(profile, common, cfg, args, run, root_for):
    project=args['project']
    if project not in profile.get('project_exec_projects',[]):
        raise PermissionError('Remote project not granted')
    options=profile.get('project_exec_options',{}).get(project,{})
    if not options.get('transfer'):
        raise PermissionError('Project file transfer not granted')
    remote_root=options['root'];local_root=options['transfer_local_root']
    remote=Path(args['path'])
    if not re.fullmatch(r'/[A-Za-z0-9_./-]+',str(remote)) or '..' in remote.parts or not remote.is_relative_to(remote_root):
        raise PermissionError('Remote file outside configured project')
    if remote.suffix.lower() not in ('.wav','.zip','.json','.md','.txt','.csv','.py','.sh'):
        raise PermissionError('Transfer file type not granted')
    upload=args['action']=='project_upload'
    roots=cfg['read_roots']+cfg['write_roots'] if upload else [local_root]
    local=root_for(args['local_path'],roots)
    if local.suffix.lower()!=remote.suffix.lower():raise ValueError('Transfer extensions must agree')
    target=profile['user']+'@'+profile['address']
    max_bytes=64*1024*1024
    probe='''import pathlib,json,hashlib
p=pathlib.Path(PATH);root=pathlib.Path(ROOT)
assert p.resolve().is_relative_to(root.resolve()), 'Remote file outside canonical project'
if UPLOAD:
 p.parent.mkdir(parents=True,exist_ok=True)
 print(json.dumps({'destination':str(p)}))
else:
 assert p.is_file() and p.stat().st_size<=LIMIT, 'File absent or larger than transfer limit'
 print(json.dumps({'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}))
'''
    code='PATH='+repr(str(remote))+'\nROOT='+repr(remote_root)+'\nUPLOAD='+repr(upload)+'\nLIMIT='+str(max_bytes)+'\n'+probe
    checked=run(['/usr/bin/ssh']+common+[target,shlex.join(['python3','-c',code])],45)
    if checked['returncode']:return checked
    metadata=json.loads(checked['stdout'])
    with tempfile.TemporaryDirectory(prefix='jarvis-project-transfer-') as scratch:
        payload=Path(scratch)/remote.name
        if upload:
            # Read as the technical user, so a local symlink race cannot expose root secrets.
            code="import pathlib,sys; p=pathlib.Path(sys.argv[1]); assert p.is_file() and p.stat().st_size<=int(sys.argv[2]); sys.stdout.buffer.write(p.read_bytes())"
            read=subprocess.run(['/usr/sbin/runuser','-u',cfg['user'],'--','python3','-c',code,str(local),str(max_bytes)],capture_output=True,timeout=45)
            if read.returncode:raise ValueError('Local upload source unreadable or oversized')
            payload.write_bytes(read.stdout)
            copied=run(['/usr/bin/scp']+common+[str(payload),target+':'+str(remote)],600)
            if copied['returncode']:return copied
            check_code='import pathlib,hashlib,json; p=pathlib.Path('+repr(str(remote))+'); print(json.dumps({"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}))'
            check=run(['/usr/bin/ssh']+common+[target,shlex.join(['python3','-c',check_code])],45)
            if check['returncode']:return check
            final=json.loads(check['stdout'])
            assert final['sha256']==hashlib.sha256(payload.read_bytes()).hexdigest(),'Transferred bytes differ'
        else:
            copied=run(['/usr/bin/scp']+common+[target+':'+str(remote),str(payload)],600)
            if copied['returncode']:return copied
            assert payload.stat().st_size<=max_bytes and hashlib.sha256(payload.read_bytes()).hexdigest()==metadata['sha256'],'Transferred bytes differ'
            # Publish as adminjarvis: the privileged broker never writes arbitrary user-selected targets as root.
            code='''import pathlib,tempfile,os,sys,json,hashlib
p=pathlib.Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True)
data=sys.stdin.buffer.read()
with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as f:
 f.write(data);name=f.name
os.replace(name,p)
print(json.dumps({'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}))
'''
            with payload.open('rb') as stream:
                published=subprocess.run(['/usr/sbin/runuser','-u',cfg['user'],'--','python3','-c',code,str(local)],stdin=stream,capture_output=True,text=False,timeout=45)
            if published.returncode:raise ValueError('Cannot publish downloaded file as technical user')
            final=json.loads(published.stdout)
    return {'returncode':0,'stdout':json.dumps({'direction':'upload' if upload else 'download','remote_path':str(remote),'local_path':str(local),**final}),'stderr':'','path':str(local),'sha256':final['sha256'],'bytes':final['bytes']}

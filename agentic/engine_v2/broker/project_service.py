"""Owner-approved project services; same mounts, identity and secret boundary as host_exec."""
from pathlib import Path
import re,shlex

def unit_arg(value):
    if not isinstance(value,str) or any(c in value for c in '\x00\n\r'):raise ValueError('Argument de service invalide')
    return '"'+value.replace('\\','\\\\').replace('"','\\"').replace('%','%%').replace('$','$$')+'"'

def definition(a,cfg,sandbox_args):
    project=a['project'];name=a['name']
    if project not in cfg.get('project_services',{}):raise PermissionError('Projet de service hors politique')
    if not re.fullmatch('[a-z][a-z0-9-]*',project) or not re.fullmatch('[a-z][a-z0-9-]*',name):raise ValueError('Nom de service invalide')
    root=Path(cfg['project_services'][project]).resolve()
    if not any(root.is_relative_to(Path(p).resolve()) for p in cfg['write_roots']):raise PermissionError('Racine de projet non accordée')
    unit='jarvis-'+project+'-'+name+'.service'
    body=None
    if a['action']=='install':
        argv=a.get('argv');
        if not isinstance(argv,list) or not argv:raise ValueError('argv doit être une liste non vide')
        for v in argv:unit_arg(v)
        if not Path(argv[0]).is_absolute() or not Path(argv[0]).resolve().is_relative_to(root) and Path(argv[0]).resolve() not in (Path('/usr/bin/python3').resolve(),Path('/usr/bin/bash')):raise PermissionError('Exécutable hors projet')
        command='cd '+shlex.quote(str(root))+' && exec '+shlex.join(argv)
        args=sandbox_args(command,cfg)
        body='[Unit]\nDescription=JARVIS project '+project+' '+name+'\nAfter=network-online.target\n\n[Service]\nType=simple\nUser='+cfg['user']+'\nNoNewPrivileges=yes\nExecStart='+ ' '.join(unit_arg(v) for v in args)+'\nRestart=on-failure\nRestartSec=5\n\n[Install]\nWantedBy=multi-user.target\n'
    return unit,body

def execute(a,cfg,run,sandbox_args):
    unit,body=definition(a,cfg,sandbox_args);action=a['action']
    if action=='install':
        p=Path('/etc/systemd/system')/unit
        if p.is_symlink():raise PermissionError('Unité symbolique refusée')
        changed=not p.exists() or p.read_text()!=body
        if changed:
            temp=p.with_suffix('.service.new');temp.write_text(body);temp.chmod(0o644);temp.replace(p)
            result=run(['/usr/bin/systemctl','daemon-reload'],30)
            if result['returncode']:return result
        return {'returncode':0,'unit':unit,'changed':changed,'installed':True,'started':False,'scope':'same host_exec confinement, no secrets'}
    if action=='logs':
        activation=run(['/usr/bin/systemctl','show',unit,'--property=InvocationID','--value'],30)
        invocation=activation.get('stdout','').strip()
        current=activation.get('returncode')==0 and bool(re.fullmatch('[0-9a-f]{32}',invocation))
        argv=['/usr/bin/journalctl','-u',unit,'-n','50','--reverse','--no-pager']
        history=a.get('history',False)
        if not isinstance(history,bool):raise ValueError('history doit être booléen')
        if current and not history:argv+=['_SYSTEMD_INVOCATION_ID='+invocation]
        result=run(argv,30,output_limit=64000)
        result.update(journal_order='newest_first',current_activation_only=current and not history,history_available=True)
        return result
    if action not in ('status','start','stop','restart','enable','disable'):raise ValueError('Action de service invalide')
    if action=='status':return run(['/usr/bin/systemctl','show',unit,'--property=LoadState,ActiveState,SubState,MainPID,ExecMainStatus,UnitFileState','--no-pager'],30)
    if not (Path('/etc/systemd/system')/unit).exists():raise ValueError('Installer le service de projet avant de le lancer')
    return run(['/usr/bin/systemctl',action,unit],30)

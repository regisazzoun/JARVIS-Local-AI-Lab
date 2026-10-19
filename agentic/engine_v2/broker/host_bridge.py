"""Owner-policy Unix broker. No policy changes are accepted over the model socket."""
import concurrent.futures, datetime, hashlib, json, os, pathlib, pwd, re, signal, socket, socketserver, sqlite3, struct, subprocess, tempfile, time, uuid
P = pathlib.Path
POLICY = P('/etc/jarvis/host-policy.json')
STATE = P('/var/lib/jarvis-agent')
SOCKET = '/run/jarvis-host/bridge.sock'
class PublicationRevisionRequired(ValueError):
    pass

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def policy():
    s = POLICY.stat()
    if s.st_uid != 0 or s.st_mode & 0o022: raise PermissionError('Politique non protégée')
    return json.loads(POLICY.read_text())
def db():
    c = sqlite3.connect(STATE/'state.sqlite', timeout=30); c.row_factory=sqlite3.Row
    c.executescript('''CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY,created TEXT,operation TEXT,request TEXT,result TEXT);
    CREATE TABLE IF NOT EXISTS capabilities(capability TEXT,resource TEXT,machine TEXT,scope TEXT,mode TEXT,state TEXT,granted TEXT,last_test TEXT,mission TEXT,revocation TEXT,PRIMARY KEY(capability,resource));
    CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY,created TEXT,payload TEXT,state TEXT,resolution TEXT);''')
    return c
def run(argv, timeout=60, user=None, output_limit=16000):
    env={'PATH':'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin','LANG':'C.UTF-8','HOME':'/root','DEBIAN_FRONTEND':'noninteractive','GH_PROMPT_DISABLED':'1','GIT_TERMINAL_PROMPT':'0'}
    if user:
        account=pwd.getpwnam(user); env['HOME']=account.pw_dir
        argv=['/usr/sbin/runuser','-u',user,'--']+argv
    started=time.monotonic()
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        p=subprocess.Popen(argv,stdout=out,stderr=err,env=env,start_new_session=True)
        try: p.wait(timeout=timeout); timed=False
        except subprocess.TimeoutExpired: os.killpg(p.pid,signal.SIGKILL);p.wait();timed=True
        out_size=out.tell();err_size=err.tell();out.seek(0);err.seek(0)
        result={'returncode':p.returncode,'stdout':out.read(output_limit).decode(errors='replace'),'stderr':err.read(6000).decode(errors='replace'),'timeout':timed,'duration_s':round(time.monotonic()-started,3),'stdout_truncated':out_size>output_limit,'stderr_truncated':err_size>6000}
    # Defense in depth. Credentials are never command arguments or part of broker replies.
    for k in ('stdout','stderr'):
        result[k]=re.sub(r'(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)', '[REDACTED]', result[k])
    return result

def preserves_project_document(previous, updated):
    """Mission21 must retain the project history; privacy redaction is permitted."""
    def normalized(text):
        text=re.sub(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])','[adresse privée masquée]',text)
        text=re.sub(r'(?i)\b[0-9a-f]{2}(?::[0-9a-f]{2}){5}\b','[adresse matérielle masquée]',text)
        return re.sub(r'(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b','[identifiant unique masqué]',text)
    return normalized(previous) in normalized(updated)

def root_for(path, roots):
    path=P(path)
    if not path.is_absolute():raise ValueError('Chemin absolu requis')
    resolved=path.resolve()
    if not any(resolved.is_relative_to(P(x).resolve()) for x in roots):raise PermissionError('Ressource hors politique : '+str(path))
    return resolved

def sandbox_args(command, cfg):
    # These are real host files, not a simulation or a copy. No home/auth/runtime mounts.
    args=['/usr/bin/bwrap','--die-with-parent','--new-session','--unshare-pid','--unshare-ipc','--unshare-uts','--cap-drop','ALL','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--symlink','usr/sbin','/sbin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/etc','--ro-bind','/etc/alternatives','/etc/alternatives','--ro-bind','/etc/ssl','/etc/ssl','--ro-bind','/etc/resolv.conf','/etc/resolv.conf','--ro-bind','/etc/hosts','/etc/hosts','--ro-bind','/etc/passwd','/etc/passwd','--ro-bind','/etc/group','/etc/group','--ro-bind','/etc/nsswitch.conf','/etc/nsswitch.conf']
    for x in cfg['write_roots']:args+=['--bind',x,x]
    for x in cfg['read_roots']:args+=['--ro-bind',x,x]
    args+=['--remount-ro','/','--chdir',cfg['write_roots'][0],'--clearenv','--setenv','PATH','/usr/bin:/bin','--setenv','LANG','C.UTF-8','--setenv','HOME',cfg['write_roots'][0],'--','/bin/bash','-c',command]
    return args

def sandbox(command, cfg, timeout=60, output_limit=16000):
    return run(sandbox_args(command,cfg),min(timeout,120),cfg['user'],output_limit)

def grant(cap,resource,state,result,cfg,mode='owner-policy'):
    with db() as c:
        c.execute('INSERT INTO capabilities VALUES(?,?,?,?,?,?,?,?,?,?) ON CONFLICT(capability,resource) DO UPDATE SET state=excluded.state,last_test=excluded.last_test',
          (cap,resource,resource if cap in ('host_remote','host_ansible') else 'local',json.dumps(cfg['scope'],ensure_ascii=False),mode,state,now(),json.dumps(result,ensure_ascii=False),'11','Owner policy withdrawal or failed functional test'))

def execute(op,a,cfg):
    if op=='host_policy':
        result={k:cfg[k] for k in ('scope','write_roots','read_roots','packages','services','repositories')}
        result['read_repositories']=cfg.get('read_repositories',[])
        result['project_services']=cfg.get('project_services',{})
        # The model needs operations and permissions, never SSH material locations.
        result['remote_hosts']={name:{**{k:v for k,v in h.items() if k not in ('identity','known_hosts','identity_check','commands')},'commands':list(h.get('commands',{})),'identity_checked':bool(h.get('identity_check'))} for name,h in cfg['remote_hosts'].items()}
        return result
    if op=='host_diagnostics':
        action=a['action']
        commands={'failed_units':['/usr/bin/systemctl','--failed','--no-pager'],
                  'recent_warnings':['/usr/bin/journalctl','-b','-p','warning','-n','60','--no-pager','-o','short-iso'],
                  'kernel_warnings':['/usr/bin/journalctl','-b','-k','-p','warning','-n','60','--no-pager','-o','short-iso'],
                  'storage_state':['/usr/bin/cat','/proc/mdstat']}
        if action not in cfg.get('diagnostics',[]) or action not in commands:raise PermissionError('Diagnostic hors politique')
        return run(commands[action],30)
    if op=='host_exec':return sandbox(a['command'],cfg)
    if op=='host_project_service':
        from project_service import execute as project_service
        return project_service(a,cfg,run,sandbox_args)
    if op in ('host_read_file','host_write_file','host_delete_file'):
        path=root_for(a['path'],cfg['write_roots']+(cfg['read_roots'] if op=='host_read_file' else []))
        # Perform file access as the technical identity inside the same protected mounts.
        if op=='host_read_file':script='from pathlib import Path; import sys; p=Path('+repr(str(path))+'); assert p.stat().st_size<=1000000, "Use explicit paginated reads for files over 1MB"; sys.stdout.write(p.read_text())'
        elif op=='host_write_file':script='from pathlib import Path; p=Path('+repr(str(path))+'); p.parent.mkdir(parents=True,exist_ok=True); p.write_text('+repr(a['content'])+'); print(p.stat().st_size)'
        else:script='from pathlib import Path; Path('+repr(a['path'])+').unlink(); print("deleted")'
        import shlex
        return sandbox('python3 -c '+shlex.quote(script),cfg,output_limit=1400000 if op=='host_read_file' else 16000)
    if op=='host_package':
        package=a['package'];action=a['action']
        if package not in cfg['packages']:raise PermissionError('Paquet absent de la politique propriétaire')
        if action=='status':return run(['/usr/bin/dpkg-query','-W','-f=${Package} ${Status} ${Version}\n',package])
        if action=='configure':return run(['/usr/bin/dpkg','--configure','-a'],600)
        if action!='install':raise ValueError('Actions : status, install, configure (reprise dpkg)')
        result=run(['/usr/bin/apt-get','install','-y','--no-install-recommends','--',package],600)
        if result['returncode']!=0:result['hint']='Si dpkg a été interrompu, appelle host_package avec action=configure pour ce paquet autorisé, puis réessaie install ; ne lance pas sudo dans host_exec.'
        grant('host_package',package,'INSTALLÉ' if result['returncode']==0 else 'ÉCHEC',result,cfg);return result
    if op=='host_service':
        name=a['service'];action=a['action']
        if '.' not in name:name+='.service'
        if name not in cfg['services'] or action not in cfg['services'][name]:raise PermissionError('Action/service hors politique')
        return run(['/usr/bin/systemctl',action,name,'--no-pager'],30)
    if op=='host_logs':
        name=a['service']
        if name not in cfg['services']:raise PermissionError('Service hors politique')
        return run(['/usr/bin/journalctl','-u',name,'-n','40','--no-pager'],15)
    if op=='host_resources':
        commands={'cpu':['/usr/bin/lscpu','--json'],'ram':['/usr/bin/free','-m'],'gpu':['/usr/bin/nvidia-smi','--query-gpu=name,memory.used,utilization.gpu','--format=csv'],'tailscale':['/usr/bin/tailscale','status','--json']}
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            futures={k:pool.submit(run,v,15,None,1000000 if k=='tailscale' else 16000) for k,v in commands.items()}
            results={k:f.result() for k,f in futures.items()}
        try:
            cpu=json.loads(results['cpu']['stdout'])
            fields=('Architecture:','CPU(s):','Model name:','Thread(s) per core:','Core(s) per socket:')
            results['cpu']['stdout']=json.dumps({x['field']:x['data'] for x in cpu['lscpu'] if x['field'] in fields})
        except (ValueError,KeyError):pass
        try:
            ts=json.loads(results['tailscale']['stdout'])
            results['tailscale']['stdout']=json.dumps({'BackendState':ts.get('BackendState'),'peers':[{'name':x.get('DNSName'),'online':x.get('Online'),'os':x.get('OS'),'addresses':x.get('TailscaleIPs')} for x in ts.get('Peer',{}).values()]})
        except (ValueError,KeyError):pass
        return results
    if op=='host_github':
        repo=a['repository']; action=a['action']
        if repo not in cfg['repositories'] and not (action in ('file','inspect','download','branches') and repo in cfg.get('read_repositories',[])):raise PermissionError('Dépôt hors politique')
        if action in ('repositories','commits','verify_commit','prs','pr_status','diff','branch_create','push_tree','verify_tree','pull_request'):
            from github_connector import execute as github_execute
            return github_execute(a,cfg,run,sandbox,root_for)
        if action=='create':
            if repo!='regisazzoun/JARVIS-Launcher2':raise PermissionError('Création limitée au projet JL-02 accordé')
            return run(['/usr/bin/gh','repo','create',repo,'--public','--description','JARVIS Launcher V2'],30,cfg['user'])
        if action=='enable_pages':
            if repo!='regisazzoun/JARVIS-Launcher2':raise PermissionError('Pages limité au projet JL-02')
            return run(['/usr/bin/gh','api','--method','POST','repos/'+repo+'/pages','-f','source[branch]=gh-pages','-f','source[path]=/'],30,cfg['user'])
        if action=='inspect':return run(['/usr/bin/gh','repo','view',repo,'--json','name,isPrivate,defaultBranchRef,url'],30,cfg['user'])
        if action in ('file','download'):
            if a.get('path') and a.get('file') and a['path']!=a['file']:raise ValueError('Specify one GitHub file path: path and file disagree')
            path=a.get('path') or a.get('file') or 'README.md'
            if not re.fullmatch(r'[\w./-]+',path) or '..' in path:raise ValueError('Chemin GitHub invalide')
            from urllib.parse import quote
            endpoint='repos/'+repo+'/contents/'+path
            if a.get('branch'):endpoint+='?ref='+quote(a['branch'],safe='')
            result=run(['/usr/bin/gh','api',endpoint,'--jq','if type == "array" then map({name,path,type,size}) else {path,size,sha,content:(.content | @base64d)} end'],30,cfg['user'],output_limit=1400000)
            result.update(github_path=path,github_branch=a.get('branch'),github_repository=repo)
            if action=='download' and result['returncode']==0:
                data=json.loads(result['stdout'])
                if not isinstance(data,dict) or not isinstance(data.get('content'),str):raise ValueError('Download requires a regular GitHub file')
                content=data['content']
                if len(content.encode())>1000000:raise ValueError('Use clone for files over 1MB')
                prior=execute('host_read_file',{'path':a['destination']},cfg)
                changed=prior.get('returncode')!=0 or prior.get('stdout')!=content
                if not changed:
                    result['stdout']=json.dumps({'path':path,'destination':a['destination'],'sha256':hashlib.sha256(content.encode()).hexdigest(),'bytes':len(content.encode()),'verified':True,'changed':False})
                    result['changed']=False
                    return result
                result['changed']=True
                written=execute('host_write_file',{'path':a['destination'],'content':''},cfg)
                if written['returncode']:return written
                import shlex
                destination=root_for(a['destination'],cfg['write_roots'])
                for offset in range(0,len(content),10000):
                    code='from pathlib import Path; p=Path('+repr(str(destination))+'); f=p.open("a"); f.write('+repr(content[offset:offset+10000])+'); f.close()'
                    written=sandbox('python3 -c '+shlex.quote(code),cfg)
                    if written['returncode']:return written
                reread=execute('host_read_file',{'path':a['destination']},cfg)
                if reread['returncode'] or reread['stdout']!=content:raise ValueError('Downloaded file verification failed')
                result['stdout']=json.dumps({'path':path,'destination':a['destination'],'sha256':hashlib.sha256(content.encode()).hexdigest(),'bytes':len(content.encode()),'verified':True})
            return result
        if action=='branches':return run(['/usr/bin/gh','api','repos/'+repo+'/branches','--jq','.[].name'],30,cfg['user'])
        if action=='pages':return run(['/usr/bin/gh','api','repos/'+repo+'/pages'],30,cfg['user'])
        if action=='clone':
            target=root_for(a['path'],cfg['write_roots'])
            argv=['/usr/bin/gh','repo','clone',repo,str(target)]
            if a.get('branch'):
                if not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_./-]*',a['branch']) or '..' in a['branch']:raise ValueError('Référence Git invalide')
                argv+=['--','--branch',a['branch']]
            return run(argv,90,cfg['user'])
        if action=='push':
            target=root_for(a['path'],cfg['write_roots']);branch=a['branch']
            if not (re.fullmatch(r'(?:jarvis|codex)/[A-Za-z0-9_./-]+',branch) or repo=='regisazzoun/JARVIS-Launcher2' and branch=='gh-pages') or '..' in branch:raise PermissionError('Branche dédiée jarvis/ ou codex/ ; gh-pages réservé à Launcher2')
            # Export a clean tree from the untrusted workspace. Never execute its hooks,
            # git config, attributes, credential helpers, or symlinked .git as privileged broker.
            import shutil
            with tempfile.TemporaryDirectory(prefix='jarvis-push-') as tmp:
                os.chmod(tmp,0o700);os.chown(tmp,pwd.getpwnam(cfg['user']).pw_uid,pwd.getpwnam(cfg['user']).pw_gid);clean=P(tmp)/'repo'
                r=run(['/usr/bin/gh','repo','clone',repo,str(clean),'--','--depth','1'],90,cfg['user'])
                if r['returncode']:return r
                existing=run(['/usr/bin/gh','api','repos/'+repo+'/branches/'+branch,'--jq','.name'],30,cfg['user'])
                if existing['returncode']==0:
                    r=run(['/usr/bin/git','-C',str(clean),'-c','credential.helper=','-c','credential.helper=!/usr/bin/gh auth git-credential','fetch','origin',branch],60,cfg['user'])
                    if r['returncode']:return r
                    checkout=['checkout','-B',branch,'FETCH_HEAD']
                else:checkout=['checkout','-b',branch]
                r=run(['/usr/bin/git','-C',str(clean)]+checkout,15,cfg['user'])
                if r['returncode']:return r
                # Only an explicit single regular file is published per call.
                relative=a.get('file','mission11-proof.txt')
                if not re.fullmatch(r'[\w./-]+',relative) or '..' in relative or any(x.startswith('.') and x not in ('.github','.gitignore','.nojekyll') for x in P(relative).parts):raise ValueError('Fichier publié invalide')
                source=root_for(str(target/relative),[str(target)])
                import base64,shlex
                probe='from pathlib import Path; import base64; p=Path('+repr(str(source))+'); assert p.is_file() and p.stat().st_size<1000000; print(base64.b64encode(p.read_bytes()).decode())'
                file_result=sandbox('python3 -c '+shlex.quote(probe),cfg,output_limit=1400000)
                if file_result['returncode'] or file_result['stdout_truncated']:raise ValueError('push: path doit être le DOSSIER racine ; file est relatif à ce dossier. Fichier absent, illisible ou >=1Mo : '+str(source))
                content=base64.b64decode(file_result['stdout'].strip(),validate=True)
                if re.search(rb'gh[pousr]_|github_pat_|PRIVATE KEY|password\s*[:=]|token\s*[:=]',content,re.I):raise PermissionError('Publication contenant un secret potentiel refusée')
                dest=clean/relative
                if repo=='regisazzoun/JARVIS-Local-AI-Lab' and branch=='jarvis/mission-21-autonomie' and relative in ('SUIVI.md','ROADMAP.md') and dest.exists():
                    if not preserves_project_document(dest.read_text(),content.decode()):
                        raise PublicationRevisionRequired('Existing project-wide document must be preserved. Save your mission summary separately, download the original root file again, then APPEND with host_exec/Python. Replacing it with a mission-only summary is not authorized.')
                if dest.is_symlink() or any(p.is_symlink() for p in dest.parents if p!=clean.parent):raise PermissionError('Destination symlink refusée')
                dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
                account=pwd.getpwnam(cfg['user']);os.chown(dest,account.pw_uid,account.pw_gid)
                for parent in dest.parents:
                    if parent==clean:break
                    os.chown(parent,account.pw_uid,account.pw_gid);parent.chmod(0o755)
                added=run(['/usr/bin/git','-C',str(clean),'add','--',relative],15,cfg['user'])
                if added['returncode']:return added
                unchanged=run(['/usr/bin/git','-C',str(clean),'diff','--cached','--quiet','--',relative],15,cfg['user'])
                if unchanged['returncode']==0:
                    # A repeated delivery of the already published file is an
                    # idempotent success. Return the verified commit like a push.
                    return run(['/usr/bin/gh','api','repos/'+repo+'/commits/'+branch,'--jq','.sha'],30,cfg['user'])
                if unchanged['returncode']!=1:return unchanged
                for argv in ([ '/usr/bin/git','-C',str(clean),'-c','user.name=JARVIS','-c','user.email=jarvis@localhost','commit','-m','jarvis: publish '+relative],['/usr/bin/git','-C',str(clean),'-c','credential.helper=','-c','credential.helper=!/usr/bin/gh auth git-credential','push','origin',branch]):
                    r=run(argv,60,cfg['user'])
                    if r['returncode']:return r
                return run(['/usr/bin/gh','api','repos/'+repo+'/commits/'+branch,'--jq','.sha'],30,cfg['user'])
        if action=='pull_request':
            branch=a['branch']
            if not re.fullmatch(r'jarvis/[A-Za-z0-9_./-]+',branch):raise PermissionError('Branche jarvis requise')
            return run(['/usr/bin/gh','pr','create','--repo',repo,'--head',branch,'--base','main','--draft','--title','Mission JARVIS','--body',a.get('body','Travail agentique à examiner.')],30,cfg['user'])
        raise ValueError('Action GitHub non implémentée : '+action)
    if op in ('host_remote','host_ansible'):
        host=a['host']
        if host not in cfg['remote_hosts']:raise PermissionError('Machine absente de la politique propriétaire')
        profile=cfg['remote_hosts'][host];action=a['action']
        if op=='host_ansible' and not profile.get('ansible_enabled',True):raise PermissionError('Ansible désactivé sur ce profil d’observation pour préserver le déploiement')
        common=['-F','/dev/null','-i',profile['identity'],'-oBatchMode=yes','-oIdentitiesOnly=yes','-oGlobalKnownHostsFile=/dev/null','-oStrictHostKeyChecking=yes','-oUserKnownHostsFile='+profile['known_hosts'],'-oConnectTimeout=10']
        import shlex
        if profile.get('identity_check'):
            checked=run(['/usr/bin/ssh']+common+[profile['user']+'@'+profile['address'],profile['identity_check']],30)
            if checked['returncode']!=0:raise PermissionError('Identité cible distante non validée ; opération arrêtée')
        if action=='project_exec':
            if op!='host_remote' or not profile.get('allow_admin') or action not in profile.get('administration_operations',[]):raise PermissionError('Remote project execution not granted')
            project=a.get('project','')
            if project not in profile.get('project_exec_projects',[]):raise PermissionError('Remote project not granted')
            root='/home/'+profile['user']+'/jarvis-projects/'+project
            script="""import pathlib,subprocess,os
root=pathlib.Path(ROOT);root.mkdir(parents=True,exist_ok=True)
argv=['/usr/bin/bwrap','--die-with-parent','--new-session','--unshare-pid','--unshare-ipc','--unshare-uts','--cap-drop','ALL','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--symlink','usr/sbin','/sbin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/etc']
for path in ['/etc/ssl','/etc/resolv.conf','/etc/hosts','/etc/passwd','/etc/group','/etc/nsswitch.conf']:
 if pathlib.Path(path).exists():argv+=['--ro-bind',path,path]
argv+=['--bind',str(root),str(root),'--chdir',str(root),'--clearenv','--setenv','HOME',str(root),'--setenv','PATH','/usr/bin:/bin','--setenv','LANG','C.UTF-8','--','/bin/bash','-c',COMMAND]
raise SystemExit(subprocess.call(argv))
""".replace('ROOT',repr(root)).replace('COMMAND',repr(a['command']))
            return run(['/usr/bin/ssh']+common+[profile['user']+'@'+profile['address'],shlex.join(['python3','-c',script])],600)
        if action=='desktop_gateway_configure':
            if not profile.get('allow_admin') or action not in profile.get('administration_operations',[]):raise PermissionError('Passerelle bureau hors profil')
            from remote_operations import configure_gateway
            return configure_gateway(cfg,run)
        if action=='desktop_network_test':
            if not profile.get('allow_admin') or action not in profile.get('administration_operations',[]):raise PermissionError('Test réseau bureau hors profil')
            from remote_operations import network_test
            return network_test(profile,common,run)
        remote_argv=None
        if action in ('supervision_install','supervision_test','desktop_configure','desktop_test','tailscale_configure','tailscale_status'):
            if not profile.get('allow_admin') or action not in profile.get('administration_operations',[]):raise PermissionError('Opération structurée hors profil')
            from remote_operations import program
            remote_argv=['sudo','-n','python3','-c',program(action)]
        if action in ('write_file','read_file','deploy_file'):
            target=P(a['path'])
            roots=profile.get('write_roots',[])
            if not target.is_absolute() or '..' in target.parts or not any(target.is_relative_to(P(x)) for x in roots):raise PermissionError('Fichier distant hors profil')
            code='from pathlib import Path; p=Path('+repr(str(target))+').resolve(); roots='+repr(roots)+'; assert any(p.is_relative_to(Path(r).resolve()) for r in roots), "Path outside authorized roots"; '
            if action in ('write_file','deploy_file'):code+='p.parent.mkdir(parents=True,exist_ok=True); p.write_text('+repr(a['content'])+'); '
            code+='print(p.read_text()[:16000])'
            remote_argv=['python3','-c',code]
            if any(target.is_relative_to(P(r)) for r in profile.get('privileged_write_roots',[])):
                if not profile.get('allow_admin'):raise PermissionError('Écriture privilégiée non accordée')
                remote_argv=['sudo','-n']+remote_argv
        if action=='package_install':
            if not profile.get('allow_admin') or a['package'] not in profile.get('packages',cfg['packages']):raise PermissionError('Paquet distant non accordé')
            remote_argv=['sudo','-n','env','DEBIAN_FRONTEND=noninteractive','apt-get','install','-y','--no-install-recommends','--',a['package']]
        if action=='service':
            if not profile.get('allow_admin') or a['service_action'] not in profile.get('services',cfg['services']).get(a['service'],[]):raise PermissionError('Service distant non accordé')
            remote_argv=['sudo','-n','systemctl',a['service_action'],a['service'],'--no-pager']
        if op=='host_remote':
            if remote_argv:command=shlex.join(remote_argv)
            elif action in profile['commands']:command=profile['commands'][action]
            else:raise PermissionError('Opération distante non accordée')
            return run(['/usr/bin/ssh']+common+[profile['user']+'@'+profile['address'],command],600 if action in ('package_install','tailscale_configure') else 45)
        argv=['/usr/bin/ansible','all','-i',profile['address']+',','-u',profile['user'],'--private-key',profile['identity'],'--ssh-common-args','-F /dev/null -oBatchMode=yes -oIdentitiesOnly=yes -oGlobalKnownHostsFile=/dev/null -oStrictHostKeyChecking=yes -oUserKnownHostsFile='+profile['known_hosts']]
        if action=='deploy_file':
            # Check canonical containment on the target before invoking copy.
            probe=code.split('p.parent.mkdir',1)[0]+'p.parent.mkdir(parents=True,exist_ok=True); print(str(p))'
            preflight=['python3','-c',probe]
            if any(target.is_relative_to(P(r)) for r in profile.get('privileged_write_roots',[])):preflight=['sudo','-n']+preflight
            checked=run(['/usr/bin/ssh']+common+[profile['user']+'@'+profile['address'],shlex.join(preflight)],30)
            if checked['returncode']:return checked
            argv+=['-m','ansible.builtin.copy','-a',json.dumps({'dest':str(target),'content':a['content'],'mode':'0644'})]
            if any(target.is_relative_to(P(r)) for r in profile.get('privileged_write_roots',[])):argv+=['--become']
        elif remote_argv:argv+=['-m','ansible.builtin.command','-a',json.dumps({'argv':remote_argv})]
        elif action=='ping':argv+=['-m','ansible.builtin.ping']
        elif action=='resources':argv+=['-m','ansible.builtin.command','-a','free -m']
        else:raise PermissionError('Action Ansible non accordée')
        return run(argv,600 if action=='package_install' else 60)
    if op=='capability_request':
        required=('capability','mission','resource','required_access','diagnosis','solution','validation','persistent')
        if any(k not in a for k in required):raise ValueError('Demande technique incomplète')
        ident=uuid.uuid4().hex
        with db() as c:c.execute('INSERT INTO requests VALUES(?,?,?,?,?)',(ident,now(),json.dumps(a,ensure_ascii=False),'DEMANDÉ','Transport persistant local ; aucun appel automatique Codex'))
        grant(a['capability'],a['resource'],'DEMANDÉ',{'request':ident},cfg,'pending-owner-scope-check')
        return {'id':ident,'state':'DEMANDÉ','transport':'SQLite broker + capability_status ; Codex doit lire puis appliquer dans le périmètre déjà autorisé. Aucun transport automatique vers une session Codex.'}
    if op=='capability_status':
        with db() as c:
            caps=[]
            for row in c.execute("SELECT * FROM capabilities ORDER BY CASE state WHEN 'DEMANDÉ' THEN 0 WHEN 'ÉCHEC' THEN 1 WHEN 'VALIDÉ' THEN 2 ELSE 3 END"):
                test=json.loads(row['last_test']);caps.append({'capability':row['capability'],'resource':row['resource'],'state':row['state']})
            requests=[]
            for row in c.execute('SELECT * FROM requests ORDER BY created DESC LIMIT 20'):
                payload=json.loads(row['payload']);requests.append({'id':row['id'],'state':row['state'],'capability':payload['capability'],'resource':payload['resource'],'resolution':row['resolution'][:600]})
            if a.get('resource'):
                caps=[dict(row) for row in c.execute('SELECT * FROM capabilities WHERE resource=?',(a['resource'],))]
            return {'scope':cfg['scope'],'machine':'local','capabilities':caps,'requests':requests,'full_registry':'root-private /var/lib/jarvis-agent/state.sqlite; no model write access'}
    if op=='capability_test':
        # A model assertion is never accepted as test evidence. Broker executes the fixed probe.
        cap=a['capability'];resource=a['resource']
        if cap=='host_package':result=execute('host_exec',{'command':resource+' --version'},cfg) if resource in cfg['packages'] else {'returncode':126,'stderr':'hors politique'}
        elif cap=='host_github':result=execute('host_github',{'repository':resource,'action':'inspect'},cfg)
        elif cap=='host_service':result=execute('host_service',{'service':resource,'action':'is-active'},cfg)
        elif cap=='host_files':
            path=root_for(resource,cfg['write_roots']);result=execute('host_exec',{'command':"python3 -c "+__import__('shlex').quote('from pathlib import Path; p=Path('+repr(str(path))+'); p.mkdir(parents=True,exist_ok=True); q=p/".capability-probe"; q.write_text("ok"); assert q.read_text()=="ok"; q.unlink(); print("READ_WRITE_OK")')},cfg)
        else:raise ValueError('Sonde non définie ; demande de capacité nécessaire')
        state='VALIDÉ' if result['returncode']==0 else 'ÉCHEC';grant(cap,resource,state,result,cfg,'owner-policy+Qwen-requested-probe')
        with db() as c:
            for row in c.execute('SELECT id,payload FROM requests WHERE state="DEMANDÉ"').fetchall():
                item=json.loads(row['payload'])
                if (item['capability'],item['resource'])==(cap,resource):c.execute('UPDATE requests SET state=?,resolution=? WHERE id=?',(state,json.dumps(result),row['id']))
        return {'state':state,**result}
    raise ValueError('Opération inconnue')

class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        cfg=policy();pid,uid,gid=struct.unpack('3i',self.request.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
        if uid not in (0,pwd.getpwnam(cfg['user']).pw_uid):return
        self.request.settimeout(150);raw=self.rfile.readline(100001)
        ident=uuid.uuid4().hex;op='invalid';a={};started=time.monotonic()
        try:caller='JARVIS-runtime' if 'jarvis-conversation.service' in P('/proc/'+str(pid)+'/cgroup').read_text() else 'local-operator'
        except OSError:caller='unknown'
        try:
            if len(raw)>100000:raise ValueError('Requête trop grande')
            req=json.loads(raw);op=req['operation'];a=req['arguments']
            result=execute(op,a,cfg);result={'ok':result.get('returncode',0)==0,'result':result}
        except Exception as e:result={'ok':False,'error':str(e),'error_code':type(e).__name__}
        result.update(caller=caller,evidence_id=ident,elapsed_s=round(time.monotonic()-started,3))
        if caller=='JARVIS-runtime' and result.get('ok'):
            resources={'host_exec':'local','host_resources':'local','host_remote':a.get('host'),'host_ansible':a.get('host'),'host_logs':a.get('service')}
            if op in resources:grant(op,resources[op],'VALIDÉ',result,cfg,'owner-policy+JARVIS-runtime-functional-test')
            if op=='host_service' and a.get('action') in ('is-active','status'):grant(op,a['service'],'VALIDÉ',result,cfg,'owner-policy+JARVIS-runtime-functional-test')
        with db() as c:c.execute('INSERT INTO events VALUES(?,?,?,?,?)',(ident,now(),op,json.dumps(a,ensure_ascii=False),json.dumps(result,ensure_ascii=False)))
        self.wfile.write(json.dumps(result,ensure_ascii=False).encode()+b'\n')
class Server(socketserver.ThreadingUnixStreamServer):daemon_threads=True

def main():
    os.umask(0o077);STATE.mkdir(parents=True,exist_ok=True);db().close()
    cfg=policy()
    with db() as c:
        known={x[0] for x in c.execute("SELECT resource FROM capabilities WHERE capability='host_package'")}
    for package in cfg['packages']:
        if package not in known:
            installed=run(['/usr/bin/dpkg-query','-W','-f=${Status}',package])
            present=installed['returncode']==0 and installed['stdout']=='install ok installed'
            grant('host_package',package,'INSTALLÉ' if present else 'MANQUANT',{'note':'Configuration propriétaire accordée ; validation par Qwen encore nécessaire'},cfg)
    P(SOCKET).unlink(missing_ok=True)
    with Server(SOCKET,Handler) as server:
        os.chown(SOCKET,0,pwd.getpwnam(cfg['user']).pw_gid);os.chmod(SOCKET,0o660)
        if os.environ.get('NOTIFY_SOCKET'):
            address=os.environ['NOTIFY_SOCKET'];address='\0'+address[1:] if address.startswith('@') else address
            with socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM) as notifier:notifier.sendto(b'READY=1',address)
        server.serve_forever()
if __name__=='__main__':main()

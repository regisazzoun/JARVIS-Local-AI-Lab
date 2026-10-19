"""Scoped GitHub operations. Credentials only in gh's system identity.
Publish explicit source snapshots, never untrusted local Git configuration/history.
"""
import base64,hashlib,json,os,pwd,re,shlex,tempfile
from pathlib import Path

def branch_name(value):
    if not re.fullmatch(r'(?:jarvis|codex)/[A-Za-z0-9_./-]+',value) or '..' in value:raise PermissionError('Dedicated jarvis/ or codex/ branch required; no main')
    return value

def relative_path(value):
    p=Path(value)
    if p.is_absolute() or '..' in p.parts or not re.fullmatch(r'[\w./-]+',value):raise ValueError('Invalid relative source path')
    if any(x in ('.git','venv','node_modules','__pycache__','private') or x=='.env' or x.startswith('.env.') and x!='.env.example' for x in p.parts):raise PermissionError('Private/generated path excluded: '+value)
    return value

def check_content(name,content):
    relative_path(name)
    if b'\x00' in content:raise ValueError('Binary source excluded: '+name)
    if re.search(rb'gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|-----BEGIN .*PRIVATE KEY-----|eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',content):raise PermissionError('Secret detected in '+name)
    if re.search(rb'(?:LIVEKIT_API_SECRET|api_secret|password)\s*[:=]\s*[\'"][^\'"\n]{8,}[\'"]',content,re.I):raise PermissionError('Literal secret requires sanitization: '+name)

def execute(a,cfg,run,sandbox,root_for):
    action=a['action'];repo=a['repository'];user=cfg['user']
    if action=='repositories':return {'returncode':0,'stdout':json.dumps({'writable':cfg['repositories'],'read_only':cfg.get('read_repositories',[])})}
    if action in ('commits','verify_commit','prs','pr_status','diff'):
        branch=a.get('branch','')
        if not branch:raise ValueError('branch obligatoire pour cette action : fournir jarvis/mission-23-livekit et commit SHA pour verify_commit')
        branch_name(branch)
        from urllib.parse import quote
        if action in ('commits','verify_commit'):
            r=run(['/usr/bin/gh','api','repos/'+repo+'/commits/'+quote(a.get('commit') or branch,safe='')],30,user)
            if r['returncode']==0:
                value=json.loads(r['stdout']);sha=value['sha'];r['stdout']=json.dumps({'sha':sha,'url':value['html_url'],'message':value['commit']['message']});r.update(commit_sha=sha,verified=True)
                if a.get('commit'):
                    compare=run(['/usr/bin/gh','api','repos/'+repo+'/compare/'+quote(a['commit'],safe='')+'...'+quote(branch,safe=''),'--jq','.status'],30,user)
                    r['verified']=compare['returncode']==0 and compare['stdout'].strip() in ('ahead','identical')
                    if not r['verified']:r.update(returncode=1,stderr='Expected commit not reachable from requested branch')
            return r
        if action=='diff':return run(['/usr/bin/gh','api','repos/'+repo+'/compare/main...'+quote(branch,safe=''),'--jq','{status,ahead_by,files:[.files[]|{filename,status,additions,deletions}]}'],30,user)
        return run(['/usr/bin/gh','pr','list','--repo',repo,'--head',branch,'--state','all','--json','number,url,state,headRefName,title'],30,user)
    if action=='branch_create':
        branch=branch_name(a['branch']);existing=run(['/usr/bin/gh','api','repos/'+repo+'/git/ref/heads/'+branch],30,user)
        if existing['returncode']==0:return existing
        base=run(['/usr/bin/gh','api','repos/'+repo+'/commits/main','--jq','.sha'],30,user)
        if base['returncode']:return base
        return run(['/usr/bin/gh','api','--method','POST','repos/'+repo+'/git/refs','-f','ref=refs/heads/'+branch,'-f','sha='+base['stdout'].strip()],30,user)
    if action=='pull_request':
        branch=branch_name(a.get('branch',''));r=run(['/usr/bin/gh','pr','list','--repo',repo,'--head',branch,'--state','open','--json','url,number'],30,user)
        if r['returncode']:return r
        existing=json.loads(r['stdout'])
        with tempfile.TemporaryDirectory(prefix='jarvis-pr-') as td:
            os.chmod(td,0o755);body=Path(td)/'body.md';body.write_text(a.get('body','JARVIS delivery; independent review required.'));body.chmod(0o644)
            if existing:
                return run(['/usr/bin/gh','pr','edit',str(existing[0]['number']),'--repo',repo,'--body-file',str(body)],30,user)
            return run(['/usr/bin/gh','pr','create','--repo',repo,'--head',branch,'--base','main','--draft','--title',a.get('title','Mission JARVIS'),'--body-file',str(body)],30,user)
    if action not in ('push_tree','verify_tree'):raise ValueError('Unsupported scoped operation')
    branch=branch_name(a['branch']);root=root_for(a['path'],cfg['write_roots'])
    files=json.loads(a['files'])
    if not isinstance(files,list) or not files or len(files)>1000:raise ValueError('files must be a JSON array of 1..1000 relative source files')
    files=[relative_path(x) for x in files]
    code='''import pathlib,json,base64,subprocess
root=pathlib.Path(ROOT).resolve();out={};secrets=[]
for envname in ['.env','livekit-agent/.env']:
 envpath=root/envname
 if envpath.is_file() and envpath.resolve().is_relative_to(root):
  for line in envpath.read_text().splitlines():
   if '=' in line and not line.lstrip().startswith('#'):
    key,value=line.split('=',1);value=value.strip().strip(chr(34)+chr(39))
    if any(k in key.upper() for k in ['SECRET','PASSWORD','TOKEN']) and len(value)>=8:secrets.append(value.encode())
for name in FILES:
 p=root/name
 if p.is_symlink() or any(parent.is_symlink() for parent in p.parents if parent.is_relative_to(root)) or not p.resolve().is_relative_to(root) or not p.is_file():raise ValueError("Invalid source: "+name)
 data=p.read_bytes()
 if len(data)>1000000:raise ValueError("Source exceeds 1MB: "+name)
 if any(secret in data for secret in secrets):raise ValueError("Private environment credential copied into source: "+name)
 out[name]=base64.b64encode(data).decode()
print(json.dumps(out))
'''.replace('ROOT',repr(str(root))).replace('FILES',repr(files))
    exported=sandbox('python3 -c '+shlex.quote(code),cfg,output_limit=20000000)
    if exported['returncode'] or exported.get('stdout_truncated'):return {**exported,'stderr':exported.get('stderr','')+' Export failed; use a directory path and explicit relative files'}
    contents={name:base64.b64decode(data) for name,data in json.loads(exported['stdout']).items()}
    for name,data in contents.items():check_content(name,data)
    if action=='verify_tree':
        from urllib.parse import quote
        r=run(['/usr/bin/gh','api','repos/'+repo+'/git/trees/'+quote(branch,safe='')+'?recursive=1'],30,user,output_limit=2000000)
        if r['returncode']:return r
        tree=json.loads(r['stdout']);remote={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        missing=[n for n,d in contents.items() if remote.get(n)!=hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()]
        return {'returncode':1 if missing or tree.get('truncated') else 0,'verified':not missing and not tree.get('truncated',False),'stdout':json.dumps({'verified_files':list(contents),'missing_or_different':missing,'tree_sha':tree['sha']})}
    with tempfile.TemporaryDirectory(prefix='jarvis-tree-') as td:
        account=pwd.getpwnam(user);os.chown(td,account.pw_uid,account.pw_gid);os.chmod(td,0o700);clean=Path(td)/'repo'
        r=run(['/usr/bin/gh','repo','clone',repo,str(clean),'--','--depth','1'],90,user)
        if r['returncode']:return r
        exists=run(['/usr/bin/gh','api','repos/'+repo+'/git/ref/heads/'+branch],30,user)['returncode']==0
        if exists:
            r=run(['/usr/bin/git','-C',str(clean),'-c','credential.helper=','-c','credential.helper=!/usr/bin/gh auth git-credential','fetch','origin',branch],60,user)
            if r['returncode']:return r
        r=run(['/usr/bin/git','-C',str(clean),'checkout','-B',branch]+(['FETCH_HEAD'] if exists else []),15,user)
        if r['returncode']:return r
        for name,data in contents.items():
            dest=clean/name
            if dest.is_symlink() or any(p.is_symlink() for p in dest.parents):raise PermissionError('Remote symlink excluded')
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);os.chown(dest,account.pw_uid,account.pw_gid)
            for parent in dest.parents:
                if parent==clean:break
                os.chown(parent,account.pw_uid,account.pw_gid)
        r=run(['/usr/bin/git','-C',str(clean),'add','--']+files,30,user)
        if r['returncode']:return r
        changed=run(['/usr/bin/git','-C',str(clean),'diff','--cached','--quiet'],15,user)
        if changed['returncode'] not in (0,1):return changed
        if changed['returncode']==1:
            r=run(['/usr/bin/git','-C',str(clean),'-c','user.name=JARVIS','-c','user.email=jarvis@localhost','commit','-m',a.get('message','jarvis: publish verified source snapshot')],30,user)
            if r['returncode']:return r
            r=run(['/usr/bin/git','-C',str(clean),'-c','credential.helper=','-c','credential.helper=!/usr/bin/gh auth git-credential','push','origin',branch],90,user)
            if r['returncode']:return {**r,'diagnostic':'No force push. Fetch current branch and retry snapshot after reviewing conflict/network/authentication error.'}
        sha=run(['/usr/bin/git','-C',str(clean),'rev-parse','HEAD'],15,user)['stdout'].strip()
        remote=run(['/usr/bin/gh','api','repos/'+repo+'/commits/'+branch,'--jq','.sha'],30,user)
        if remote['returncode']:return remote
        verified=remote['stdout'].strip()==sha
        return {'returncode':0 if verified else 1,'stdout':json.dumps({'commit_sha':sha,'verified':verified,'changed':changed['returncode']==1,'files_sha256':{n:hashlib.sha256(d).hexdigest() for n,d in contents.items()},'url':'https://github.com/'+repo+'/commit/'+sha}), 'commit_sha':sha,'verified':verified,'changed':changed['returncode']==1}

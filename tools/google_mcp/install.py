"""Install the pinned open-source server; no Cloud project or auth token created."""
import argparse,hashlib,json,os,shutil,subprocess
from pathlib import Path
COMMIT='089927ead01433f38c65c12cdcd2ed9a18165277'
def atomic_copy(source,target):
    target=Path(target);temporary=target.with_name(target.name+'.install-'+str(os.getpid()));shutil.copy2(source,temporary);os.replace(temporary,target)

def install(source,root,profiles):
    source=Path(source).resolve();root=Path(root);profiles=Path(profiles)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()==COMMIT,'Review a different upstream version before installing'
    root.mkdir(parents=True,exist_ok=True);here=Path(__file__).resolve().parent
    for name in ('index.js','auth-utils.js','headless-login.js'):atomic_copy(source/'workspace-server/dist'/name,root/name)
    subprocess.run(['/usr/bin/node',str(here/'build_auth_bridge.cjs'),str(source),str(here/'auth-bridge.ts'),str(root/'auth-bridge.js')],check=True)
    shutil.copy2(source/'LICENSE',root/'LICENSE');shutil.copy2(here/'connect.py',root/'connect.py')
    profiles.mkdir(mode=0o700,parents=True,exist_ok=True);profiles.chmod(0o700)
    for profile in ('personal','education'):
        folder=profiles/profile
        if folder.is_symlink():raise ValueError('Refuse linked profile directory')
        folder.mkdir(mode=0o700,exist_ok=True);folder.chmod(0o700)
        for name in ('index.js','auth-bridge.js','auth-utils.js','headless-login.js'):atomic_copy(root/name,folder/name)
        marker=folder/'gemini-extension.json'
        if not marker.exists():marker.write_text(json.dumps({'name':'jarvis-google-workspace-'+profile,'version':'0.0.8','upstream_commit':COMMIT}));marker.chmod(0o600)
    manifest={'upstream':'https://github.com/gemini-cli-extensions/workspace','commit':COMMIT,'license':'Apache-2.0','owner_cloud_project_created':False,'tokens_created':False,'publisher_oauth_relay':'https://google-workspace-extension.geminicli.com','files':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ('index.js','auth-bridge.js','connect.py')}}
    (root/'INSTALLATION.json').write_text(json.dumps(manifest,indent=2)+'\n');return manifest
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True);p.add_argument('--root',default='/opt/jarvis/google-workspace-mcp');p.add_argument('--profiles',default='/home/adminjarvis/.config/jarvis/google-mcp');a=p.parse_args();print(json.dumps(install(a.source,a.root,a.profiles),indent=2))

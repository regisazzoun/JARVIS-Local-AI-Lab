"""Idempotently connect the existing WebUI to existing JARVIS services.

Requires existing owner WebUI token and adapter key files. No application/model
installation, new database, token printing or merge is performed.
"""
import argparse,json,urllib.request
from pathlib import Path

def deploy(url,token_file,key_file,backup):
    root=Path(__file__).resolve().parents[2]
    token=Path(token_file).read_text().strip();key=Path(key_file).read_text().strip()
    backup=Path(backup);backup.mkdir(mode=0o700,parents=True,exist_ok=True);backup.chmod(0o700)
    def api(path,data=None):
        request=urllib.request.Request(url.rstrip('/')+path,data=json.dumps(data).encode() if data is not None else None,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
        with urllib.request.urlopen(request,timeout=30) as response:return json.load(response)
    tools=api('/api/v1/tools/');models=api('/api/v1/models/list')['items'];defaults=api('/api/v1/configs/models')
    # Never overwrite a first snapshot on repeated deployment.
    for name,value in [('tools',tools),('profiles',models),('defaults',defaults)]:
        path=backup/(name+'.json')
        if not path.exists():path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');path.chmod(0o600)
    for ident,label,file in [('jarvis_capabilities','Capacités canoniques JARVIS','webui_capabilities.py'),('jarvis_qwen_local','JARVIS et Qwen Code local','webui_tool.py')]:
        existing=next((t for t in tools if t['id']==ident),None)
        data={'id':ident,'name':label,'content':(root/'tools/qwen_webui'/file).read_text(),'meta':existing['meta'] if existing else {'description':'Connecteur vers le registre et les services JARVIS existants'},'access_grants':existing.get('access_grants',[]) if existing else []}
        api('/api/v1/tools/id/'+ident+'/update' if existing else '/api/v1/tools/create',data)
        api('/api/v1/tools/id/'+ident+'/valves/update',{'ADAPTER_URL':'http://127.0.0.1:8092','ADAPTER_KEY':key})
    for profile in json.loads((root/'tools/qwen_webui/config/webui-client-profiles.json').read_text()):
        exists=any(p['id']==profile['id'] for p in models)
        api('/api/v1/models/model/update?id='+profile['id'] if exists else '/api/v1/models/create',profile)
    defaults['DEFAULT_MODELS']='jarvis-tools-conversation';api('/api/v1/configs/models',defaults)
    refreshed=api('/api/v1/tools/');return {'deployed_tools':[{ 'id':t['id'],'functions':len(t.get('specs',[]))} for t in refreshed if t['id'] in ('jarvis_capabilities','jarvis_qwen_local')],'default_profile':'jarvis-tools-conversation','base_model_unchanged':'qwen3.5:27b-q4_K_M'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',required=True);parser.add_argument('--token-file',required=True);parser.add_argument('--adapter-key-file',required=True);parser.add_argument('--backup-dir',required=True)
    args=parser.parse_args();print(json.dumps(deploy(args.url,args.token_file,args.adapter_key_file,args.backup_dir),ensure_ascii=False,indent=2))

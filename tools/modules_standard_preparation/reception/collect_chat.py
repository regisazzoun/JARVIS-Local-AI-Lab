from pathlib import Path
import urllib.request,json,sys
h=Path.home();t=(h/'JARVIS/qwen-code-openwebui-private/webui-token').read_text().strip()
id=sys.argv[1]
r=urllib.request.Request('http://127.0.0.1:8088/api/v1/chats/'+id,headers={'Authorization':'Bearer '+t})
d=json.load(urllib.request.urlopen(r))['chat']
out={'chat_id':id,'models':d.get('models'),'turns':[]}
for m in d['history']['messages'].values():
 out['turns'].append({k:m[k] for k in ['id','parentId','role','content','done','model','timestamp','output','error'] if k in m})
print(json.dumps(out,ensure_ascii=False,indent=2))

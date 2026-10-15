from commun import *
login();x=json.loads((P/'db-avant-prive.json').read_text());row=next(r for r in x['chat'] if len(json.loads(r['chat']).get('history',{}).get('messages',{}))>2);chat=json.loads(row['chat']);allm=chat['history']['messages'];chain=[];cur=chat['history'].get('currentId')
while cur and cur in allm:
 m=allm[cur];chain.append(m);cur=m.get('parentId')
chain=chain[::-1]
if chain[-1]['role']=='assistant':chain=chain[:-1]
msgs=[{'role':m['role'],'content':m['content']} for m in chain];out=[]
for label,files in [('with_files',chat.get('files')),('without_files',None)]:
 r=run(msgs,route='web',files=files);r['label']=label;out.append(r);print(label,len(msgs),r['metrics'].get('prompt_eval_count'),round(r['wall_seconds'],2),flush=True)
(P/'rejeu-prive.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))

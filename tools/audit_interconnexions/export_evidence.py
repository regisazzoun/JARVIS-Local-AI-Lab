"""Publish selected audit facts; raw inventory, user chats and secrets stay private."""
import json,datetime,hashlib
from pathlib import Path
P=Path('/home/adminjarvis/JARVIS/audit-interconnexions-ia-private');D=Path('docs/missions/AUDIT-INTERCONNEXIONS-IA');r={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'machines':{}}
for name in ['Mac','Dell1','Dell2']:
 d=json.loads((P/(name+'.json')).read_text());cpu=json.loads(d['cpu']['out'])['lscpu'];mem=dict(x.split(':',1) for x in d['meminfo'].splitlines() if ':' in x)
 r['machines'][name]={'os':d['os'],'kernel':d['kernel']['out'].strip(),'cpu':{x['field']:x['data'] for x in cpu if x['field'] in ['Model name:','CPU(s):']},'ram_gib':round(int(mem['MemTotal'].split()[0])/1048576,2),'gpu':d['gpu'],'tailscale_state':d['tailscale'].get('state'),'running_services':[l.strip() for l in d['services']['out'].splitlines() if any(t in l for t in ['jarvis','ollama','tailscale','apache2','docker'])]}
(D/'E01-INVENTAIRE.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
for src,dest in [('models-before.json','E02-CATALOGUES.json'),('models-after-inference.json','E03-MODELES-CHARGES.json'),('qwen-proof.json','E04-QWEN-CODE.json'),('historical-engine-events.json','E05-EVENEMENTS-HISTORIQUES.json'),('ports-units.json','E06-SERVICES-PORTS.json'),('engine-state.json','E07-MOTEUR.json')]:
 (D/dest).write_bytes((P/src).read_bytes())
d=json.loads((P/'webui-db.json').read_text());safe={'profiles':[],'user_selection':d['user_selection'],'conversation_model_counts':d['history_model_counts'],'raw_json_messages':[{'role':x['role'],'model':x['model'],'content_form':'JSON ask_user rendered as message text; original remains private'} for x in d['ask_user_occurrences']]}
for m in d['models']:
 params=json.loads(m['params']);meta=json.loads(m['meta']);safe['profiles'].append({'id':m['id'],'name':m['name'],'base_model_id':m['base_model_id'],'params':{k:v for k,v in params.items() if k!='system'},'system_prompt_sha256':hashlib.sha256(params.get('system','').encode()).hexdigest(),'system_mentions_ask_user':'ask_user' in params.get('system',''),'tools':meta.get('toolIds',[]),'description':meta.get('description')})
safe['runtime_providers']=json.loads((P/'_ollama_config.json').read_text())['OLLAMA_BASE_URLS'];safe['source_selection_rule']='ollama-router.py:1123 random.choice(models[model][urls]); llama8 and qwen27 urls=[0,1]; coder80 urls=[1]';safe['default_environment']='DEFAULT_MODELS=llama3.1:8b; ENABLE_PERSISTENT_CONFIG=false';safe['new_browser_test']=json.loads((P/'browser-ask-user.json').read_text());historical=json.loads((P/'browser-historical-json.json').read_text());safe['historical_display_reproduced']={'raw_ask_user_visible':historical['raw_ask_user_visible'],'output_types':['message'],'tool_calls':False,'count':len(d['ask_user_occurrences'])};(D/'E08-WEBUI.json').write_text(json.dumps(safe,ensure_ascii=False,indent=2)+'\n')
d=json.loads((P/'canonical-diagnostic.json').read_text());d['routing']['hybrid_compute']['nodes']['Dell1'].pop('selection_status',None);(D/'E09-CONVERSATION-DIAGNOSTIC.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for src,dest in [('mac27-direct-final.json','E10-QWEN27-DIRECT.json'),('integration-sources.json','E11-SOURCES.json'),('canonical-restricted-jl03.json','E12-JL03-RESTRICTION.json')]:
 if (P/src).exists():(D/dest).write_bytes((P/src).read_bytes())
print('Selected facts exported; credentials and original user discussions excluded.')

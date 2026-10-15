from benchmark import *
from complementaires import suite
MSYSTEM=(P/'instruction-mistral.txt').read_text()
# Pas de téléchargement ici : le pull officiel est effectué séparément.
show=api('show',{'model':MISTRAL});(P/'mistral-identification.json').write_text(json.dumps(show,indent=2,ensure_ascii=False));unload_except(MISTRAL)
r=call(MISTRAL,[{'role':'user','content':'Réponds en français en deux phrases : présente-toi comme assistant local et distingue une hypothèse d’un fait vérifié.'}],{'num_ctx':8192,'num_predict':128});(P/'premiere-inference.json').write_text(json.dumps(r,indent=2,ensure_ascii=False));print('FIRST',r['response']['message']['content'],r['resources_after']['gpu'],flush=True)
ps=r['resources_after']['ollama_ps']['models'];m=next(x for x in ps if x['name']==MISTRAL);assert m['context_length']==8192
if m['size_vram']/m['size']<.95:raise RuntimeError('Important CPU offload: pause for application-only memory investigation')
cal=[]
for label,opts,system in [('native',{'num_ctx':8192,'seed':42},None),('qualite-0.1',{'num_ctx':8192,'temperature':.1,'top_p':.9,'num_predict':2048,'seed':42},MSYSTEM),('qualite-0.3',{'num_ctx':8192,'temperature':.3,'top_p':.9,'num_predict':2048,'seed':42},MSYSTEM)]:
 msgs=([{'role':'system','content':system}] if system else [])+[{'role':'user','content':PROMPT}]
 rr=call(MISTRAL,msgs,opts);rr['label']=label;cal.append(rr);(P/'calibration-mistral.json').write_text(json.dumps(cal,indent=2,ensure_ascii=False));print('CAL',label,rr['response'].get('eval_count'),round(rr['wall_seconds'],2),flush=True)
# Comparatif contrôlé : mêmes instructions et paramètres .1 que Llama, sans réponses attendues.
reference(MISTRAL)
# Tests complémentaires contrôlés : même instruction pour les deux modèles.
suite(MISTRAL)

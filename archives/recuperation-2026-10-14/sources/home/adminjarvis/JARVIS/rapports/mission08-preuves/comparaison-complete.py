from benchmark import *
from complementaires import suite
MSYSTEM=(P/'instruction-mistral.txt').read_text();unload_except(MISTRAL);cal=[]
for label,temp in [('qualite-0.1-complete',.1),('qualite-0.3-complete',.3)]:
 r=call(MISTRAL,[{'role':'system','content':MSYSTEM},{'role':'user','content':PROMPT}],{'num_ctx':8192,'temperature':temp,'top_p':.9,'num_predict':3072,'seed':42});r['label']=label;cal.append(r);(P/'calibration-complete.json').write_text(json.dumps(cal,indent=2,ensure_ascii=False));print(label,r['response']['eval_count'],r['response'].get('done_reason'),round(r['wall_seconds'],2),flush=True)
reference(LLAMA)
reference(MISTRAL)
suite(MISTRAL)

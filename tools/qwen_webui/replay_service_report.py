"""Compare frozen real report inputs; never execute generated host operations."""
import argparse,hashlib,json,time,urllib.request
from pathlib import Path

def main():
 parser=argparse.ArgumentParser();parser.add_argument('inputs',type=Path);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
 bundle=json.loads(args.inputs.read_text());model=bundle['model']
 if model!='qwen3-coder-next:q4_K_M':raise ValueError('Established model only')
 schema={'type':'object','properties':{'report':{'type':'string','maxLength':1800}},'required':['report'],'additionalProperties':False}
 rows=[]
 for name,old,reference in [('previous_no_reference',True,False),('fresh_no_reference',False,False),('previous_with_reference',True,True),('fresh_with_reference',False,True)]:
  data={'facts':bundle['facts']}
  if old:data['previous_draft']=bundle['previous_draft']
  if reference:data['official_reference']={'source':'https://www.freedesktop.org/software/systemd/man/latest/systemctl.html#Exit%20status','mapping':'0: unit is active. 3: unit is not active. 4: no such unit. The mapping is imperfect; inspect specific state/substate and original status output.'}
  system=bundle['identity']+'\nMISSION DE DIAGNOSTIC EN LECTURE SEULE. Rédige un NOUVEAU bilan français concis de1800caractères maximum depuis les seuls faits fournis. Le brouillon précédent, si présent, peut être erroné : confronte chaque affirmation aux reçus originaux. Distingue sorties, interprétations prouvées et limites. Compte les unités et non les appels, explique les états seulement quand les sources le permettent, cite quelques vrais identifiants de reçus. Aucun outil ni changement système. Ce rejeu ne clôture aucune mission. Le JSON de réponse contient uniquement report.'
  payload={'model':model,'messages':[{'role':'system','content':system},{'role':'user','content':json.dumps(data,ensure_ascii=False)}],'stream':False,'think':False,'format':schema,'options':{'num_ctx':32768,'num_predict':2048,'temperature':0.1,'seed':42}}
  raw=json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode()
  if len(raw)>27648:raise ValueError('Split inputs; conservative byte limit remains27648')
  start=time.monotonic();req=urllib.request.Request('http://127.0.0.1:8091/api/chat',data=raw,headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=180) as response:result=json.load(response)
  parsed=json.loads(result['message']['content'])
  row={'variant':name,'request_sha256':hashlib.sha256(raw).hexdigest(),'input_bytes':len(raw),'seconds':time.monotonic()-start,'prompt_eval_count':result.get('prompt_eval_count'),'eval_count':result.get('eval_count'),'done_reason':result.get('done_reason'),'message':result['message'],'schema_valid':set(parsed)=={'report'} and isinstance(parsed['report'],str) and len(parsed['report'])<=1800,'tools_executed':False,'factual_reception':'NOT_CHECKED'}
  rows.append(row);args.output.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print(name,'JSON schema:',row['schema_valid'],'factual correctness requires independent original-receipt review')
if __name__=='__main__':main()

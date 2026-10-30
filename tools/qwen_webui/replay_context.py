"""Replay an authentic captured tool history, changing one transport/context factor.

Only model decisions are measured: this script never dispatches generated tools.
The input is private. The existing admission gateway and resource budget apply.
"""
import argparse,copy,hashlib,json,time,urllib.request
from pathlib import Path
from ollama_guard import native_payload
MINIMAL='You are a coding assistant working only in the current project. Use python3. Never weaken tests. Report the observed result in French; finish when the requested criteria are met. Stop and explain after three comparable failures.'
def main():
 parser=argparse.ArgumentParser();parser.add_argument('capture',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 raw=args.capture.read_bytes();source=json.loads(raw)
 if source.get('model')!='qwen3-coder-next:q4_K_M':raise ValueError('Use the established model only')
 rows=[]
 for mode in ('legacy','named','minimal','named_minimal'):
  payload=native_payload(copy.deepcopy(source));payload['stream']=False
  payload['options'].update(temperature=0.1,seed=42,num_predict=1024)
  if mode in ('legacy','minimal'):
   for message in payload['messages']:message.pop('tool_name',None)
  if mode in ('minimal','named_minimal'):payload['messages'][0]['content']=MINIMAL
  encoded=json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode()
  if len(encoded)>27648:raise ValueError('Split the diagnostic input: byte budget27648 remains in force')
  request=urllib.request.Request('http://127.0.0.1:8091/api/chat',data=encoded,headers={'Content-Type':'application/json'})
  start=time.monotonic()
  with urllib.request.urlopen(request,timeout=180) as response:result=json.load(response)
  rows.append({'variant':mode,'capture_sha256':hashlib.sha256(raw).hexdigest(),'request_sha256':hashlib.sha256(encoded).hexdigest(),'input_bytes':len(encoded),'seconds':time.monotonic()-start,'message':result.get('message'),'done_reason':result.get('done_reason'),'prompt_eval_count':result.get('prompt_eval_count'),'eval_count':result.get('eval_count'),'tools_dispatched':False})
  args.output.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
  print(mode,'tool proposals:',[c['function']['name'] for c in result.get('message',{}).get('tool_calls',[])])
if __name__=='__main__':main()

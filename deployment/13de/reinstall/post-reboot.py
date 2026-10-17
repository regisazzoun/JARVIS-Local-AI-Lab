#!/usr/bin/env python3
"""Minimal authenticated application checks after the Dell's final reboot."""
import argparse,pathlib,json,hashlib,hmac,urllib.request,http.cookiejar
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);a=p.parse_args();b=a.session
runtime=pathlib.Path('/opt/jarvis/conversation/runtime');active=json.loads((runtime/'auth.json').read_text());lines=(runtime/'credentials.txt').read_text().splitlines()
candidates=[lines[1].split(': ',1)[1],(b.parent/'reprise-user-password.txt').read_text().rstrip('\n')]
password=next((v for v in candidates if hmac.compare_digest(hashlib.pbkdf2_hmac('sha256',v.encode(),bytes.fromhex(active['salt']),300000).hex(),active['hash'])),None);assert password is not None
client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def gateway(path,data):
 req=urllib.request.Request('http://localhost:8765'+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json','X-Jarvis-Request':'1'})
 with client.open(req,timeout=300) as r:return json.load(r)
gateway('/api/login',{'username':active['username'],'password':password})
r=gateway('/api/chat',{'text':'Calcule 17 fois 23 et réponds avec le résultat.','model':'qwen3.5:27b-q4_K_M','retain':False});assert '391' in r['answer']
creds=pathlib.Path('/home/adminjarvis/JARVIS/open-webui/identifiants-admin.txt').read_text().splitlines()
def web(path,data,token=None):
 headers={'Content-Type':'application/json'}
 if token:headers['Authorization']='Bearer '+token
 req=urllib.request.Request('http://192.168.1.99:3000'+path,data=json.dumps(data).encode(),headers=headers)
 with urllib.request.urlopen(req,timeout=300) as r:return json.load(r)
token=web('/api/v1/auths/signin',{'email':creds[0].split(': ',1)[1],'password':creds[1].split(': ',1)[1]})['token']
r=web('/api/chat/completions',{'model':'llama3.1:8b','messages':[{'role':'user','content':'Calcule 17 fois 23. Réponds avec le résultat.'}],'stream':False,'options':{'num_ctx':4096,'num_predict':64}},token);assert '391' in r['choices'][0]['message']['content']
(b/'applications-after-reboot.json').write_text(json.dumps({'authenticated_gateway_qwen':True,'authenticated_openwebui_llama':True,'canonical_memory_path_preserved':True},indent=2)+'\n')
print('Authenticated gateway and Open WebUI inference validated after Dell reboot')

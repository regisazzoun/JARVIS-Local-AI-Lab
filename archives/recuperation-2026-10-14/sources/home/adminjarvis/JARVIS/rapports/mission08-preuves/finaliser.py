import pathlib,json,urllib.request,time,subprocess
P=pathlib.Path(__file__).parent;BASE=pathlib.Path('/home/adminjarvis/JARVIS');URL='http://192.168.1.99:3000';M='ministral-3:14b-instruct-2512-q4_K_M'
def req(path,data=None,token=None):
 h={'Content-Type':'application/json'}
 if token:h['Authorization']='Bearer '+token
 r=urllib.request.Request(URL+path,data=None if data is None else json.dumps(data).encode(),headers=h)
 with urllib.request.urlopen(r,timeout=300) as f:return json.load(f)
def ready():
 for i in range(90):
  try:return req('/health')
  except Exception:time.sleep(2)
 raise RuntimeError('WebUI indisponible')
def auth():
 password=(BASE/'open-webui/identifiants-admin.txt').read_text().splitlines()[1].split(': ',1)[1]
 return req('/api/v1/auths/signin',{'email':'admin@jarvis.local','password':password})['token']
guard='''\nPour toute proposition technique, les interdictions explicites priment sur les solutions habituelles. Une sauvegarde ne rend pas autorisée une opération interdite. Si les données doivent rester inchangées, ne propose pas de suppression, de réinitialisation ni de restauration ancienne d'une base, d'un volume, d'une conversation ou d'un document. Préfère les lectures et les essais applicatifs dans une instance isolée indépendante. N'affirme pas qu'une commande, un chemin, une option ou une version existe sans source disponible ; indique ce qui doit être vérifié. Tu ne peux pas exécuter d'action système : distingue propositions et opérations réellement attestées. Vérifie les contraintes et le contrat d'erreur du code avant de conclure.\n'''
system=(P/'systeme-llama-reference.txt').read_text()+guard
(P/'instruction-mistral-finale.txt').write_text(system)
subprocess.run(['cp',str(BASE/'ollama/demarrer.sh'),str(P/'demarrer-avant.sh')],check=True)
subprocess.run(['sudo','cp','/etc/systemd/system/jarvis-ollama.service',str(P/'jarvis-ollama-avant.service')],check=True)
subprocess.run(['sudo','chown','adminjarvis:adminjarvis',str(P/'jarvis-ollama-avant.service')],check=True)
unit=(P/'jarvis-ollama-avant.service').read_text();unit=unit.replace('Environment=OLLAMA_NUM_PARALLEL=1','Environment=OLLAMA_NUM_PARALLEL=1\nEnvironment=OLLAMA_MAX_LOADED_MODELS=1');(P/'jarvis-ollama-apres.service').write_text(unit)
subprocess.run(['sudo','install','-m','644',str(P/'jarvis-ollama-apres.service'),'/etc/systemd/system/jarvis-ollama.service'],check=True)
(BASE/'open-webui/jarvis-ollama.service').write_text(unit)
f=BASE/'ollama/demarrer.sh';f.write_text(f.read_text().replace('export OLLAMA_NUM_PARALLEL=1','export OLLAMA_NUM_PARALLEL=1\nexport OLLAMA_MAX_LOADED_MODELS=1'))
f=BASE/'open-webui/compose.yaml';s=f.read_text().replace('      ENABLE_OPENAI_API: "false"','      ENABLE_OPENAI_API: "false"\n      DEFAULT_MODELS: "llama3.1:8b"');f.write_text(s)
subprocess.run(['sudo','systemctl','daemon-reload'],check=True);subprocess.run(['sudo','systemctl','restart','jarvis-ollama'],check=True)
subprocess.run(['sudo','docker','compose','up','-d'],cwd=BASE/'open-webui',check=True);ready();token=auth()
profile={'id':M,'base_model_id':None,'name':'JARVIS — Mistral 14B Qualité','meta':{'description':'Ministral 3 14B Q4_K_M : profil expérimental, contrôle humain requis pour les propositions techniques.'},'params':{'system':system,'num_ctx':8192,'temperature':0.1,'top_p':0.9,'num_predict':3072},'is_active':True}
r=req('/api/v1/models/create',profile,token);(P/'profil-mistral-final.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
models=req('/api/models',token=token);(P/'modeles-webui-finaux.json').write_text(json.dumps(models,ensure_ascii=False,indent=2))
results=[]
for m in ['llama3.1:8b',M]:
 t=time.perf_counter();r=req('/api/chat/completions',{'model':m,'messages':[{'role':'user','content':'Réponds en français en une phrase : combien font 17 multiplié par 23 ?'}],'stream':False},token)
 results.append({'model':m,'response':r,'wall_seconds':time.perf_counter()-t,'gpu':subprocess.check_output(['nvidia-smi','--query-gpu=memory.used,utilization.gpu,temperature.gpu','--format=csv,noheader,nounits'],text=True),'ps':json.loads(urllib.request.urlopen('http://127.0.0.1:11434/api/ps').read())})
(P/'validation-webui.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
subprocess.run(['sudo','docker','compose','restart'],cwd=BASE/'open-webui',check=True);ready();token=auth();(P/'profils-apres-redemarrage.json').write_text(json.dumps(req('/api/v1/models/all',token=token),ensure_ascii=False,indent=2))
print('Profils et inférences WebUI validés ; redémarrage applicatif terminé.',flush=True)

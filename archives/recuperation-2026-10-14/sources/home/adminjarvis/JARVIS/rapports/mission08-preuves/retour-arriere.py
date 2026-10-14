#!/usr/bin/env python3
"""Retour applicatif Mission08. Sans --appliquer, affiche seulement le plan."""
import pathlib,subprocess,sys,json,urllib.request,time
P=pathlib.Path(__file__).parent;B=pathlib.Path('/home/adminjarvis/JARVIS');U='http://192.168.1.99:3000'
if '--appliquer' not in sys.argv:
 print('Sauvegarde fraîche ; suppression du seul profil Mistral en base via API ; restauration Compose, unité Ollama et lanceur ; redémarrage applicatif. Modèles, comptes, conversations et documents conservés.');sys.exit()
subprocess.run(['bash',str(B/'open-webui/sauvegarder.sh')],check=True)
def req(path,data=None,token=None):
 h={'Content-Type':'application/json'}
 if token:h['Authorization']='Bearer '+token
 r=urllib.request.Request(U+path,data=None if data is None else json.dumps(data).encode(),headers=h)
 with urllib.request.urlopen(r,timeout=60) as f:return json.load(f)
for _ in range(90):
 try:req('/health');break
 except Exception:time.sleep(2)
else:raise RuntimeError('WebUI inaccessible')
pw=(B/'open-webui/identifiants-admin.txt').read_text().splitlines()[1].split(': ',1)[1]
token=req('/api/v1/auths/signin',{'email':'admin@jarvis.local','password':pw})['token']
req('/api/v1/models/model/delete',{'id':'ministral-3:14b-instruct-2512-q4_K_M'},token)
subprocess.run(['cp',str(P/'compose-avant.yaml'),str(B/'open-webui/compose.yaml')],check=True)
subprocess.run(['cp',str(P/'demarrer-avant.sh'),str(B/'ollama/demarrer.sh')],check=True)
subprocess.run(['cp',str(P/'jarvis-ollama-avant.service'),str(B/'open-webui/jarvis-ollama.service')],check=True)
subprocess.run(['sudo','install','-m','644',str(P/'jarvis-ollama-avant.service'),'/etc/systemd/system/jarvis-ollama.service'],check=True)
subprocess.run(['sudo','systemctl','daemon-reload'],check=True)
subprocess.run(['sudo','systemctl','restart','jarvis-ollama'],check=True)
subprocess.run(['sudo','docker','compose','up','-d'],cwd=B/'open-webui',check=True)
print('Retour des paramètres applicatifs effectué ; poids Llama et Mistral conservés, base non restaurée.')

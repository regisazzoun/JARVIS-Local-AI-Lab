"""One objective to the deployed JARVIS model. No scripted tool selection or repair."""
import urllib.request,http.cookiejar,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=Path('/home/adminjarvis/JARVIS/rapports/mission13f-preuves')
client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def call(path,data):
 req=urllib.request.Request('http://localhost:8765'+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json','X-Jarvis-Request':'1'})
 with client.open(req,timeout=600) as r:return json.load(r)
password=(ROOT/'runtime/credentials.txt').read_text().splitlines()[1].split(': ',1)[1];call('/api/login',{'username':'adminjarvis','password':password})
start=time.monotonic()
goal="Dans le laboratoire autorisé mission 13F, le vrai service HTTP du dossier /work/incident13f est indisponible. Identifie la cible et le risque, examine l’environnement et les fichiers, établis un plan avec retour arrière. Diagnostique la panne, recherche de toi-même la documentation Internet et consulte au moins deux sources officielles pertinentes. Compare les corrections possibles, choisis et réalise la correction réversible dans ce seul laboratoire. Observe les erreurs et recommence si nécessaire. Vérifie que le service répond effectivement selon le README. Ne modifie ni service.py ni check.py. Conserve un rapport d’intervention avec décisions, sources, résultats et limites. N’annonce aucun succès sans vérification. Aucune action sur le Dell."
r=call('/api/chat',{'text':goal,'model':'qwen3.5:27b-q4_K_M','project':'__13f_autonomy__','retain':True,'agent_mode':True})
report={'kind':'real deployed HTTP gateway + real Qwen + model-selected tools + Bubblewrap isolated process; not VM, not physical Dell','elapsed_s':time.monotonic()-start,'goal':goal,'response':r}
(OUT/'autonomy-attempt4.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'elapsed_s':report['elapsed_s'],'answer':r['answer'],'tools':[{k:t[k] for k in ['tool','ok','elapsed_s']} for t in r['tools']]},ensure_ascii=False,indent=2))

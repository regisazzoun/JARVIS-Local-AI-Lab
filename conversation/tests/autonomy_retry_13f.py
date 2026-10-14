import os
"""One objective to the deployed JARVIS model. No scripted tool selection or repair."""
import urllib.request,http.cookiejar,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=Path(os.environ.get('JARVIS_TEST_OUTPUT',str(ROOT/'runtime/qa13f')))
OUT.mkdir(mode=0o700,parents=True,exist_ok=True)
client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def call(path,data):
 req=urllib.request.Request('http://localhost:8765'+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json','X-Jarvis-Request':'1'})
 with client.open(req,timeout=600) as r:return json.load(r)
username=(ROOT/'runtime/credentials.txt').read_text().splitlines()[0].split(': ',1)[1];password=(ROOT/'runtime/credentials.txt').read_text().splitlines()[1].split(': ',1)[1];call('/api/login',{'username':username,'password':password})
start=time.monotonic()
goal="Dans le laboratoire autorisé mission 13F, le vrai service HTTP du dossier /work/incident13f_retry est indisponible. Identifie la cible et le risque, examine l’environnement et les fichiers, établis un plan avec retour arrière. Diagnostique la panne, recherche de toi-même la documentation Internet et consulte au moins deux sources officielles pertinentes. Consulte deux sources indépendantes : deux ancres ou versions de la même documentation ne suffisent pas. Cite leurs URL exactes. Compare au moins deux corrections possibles avec leurs avantages et risques, choisis et réalise la correction réversible dans ce seul laboratoire. Reproduis la panne avant correction. Observe les erreurs et recommence si nécessaire. Les permissions des seuls fichiers de ce laboratoire peuvent être corrigées, sans privilège hôte. Vérifie que le service répond effectivement selon le README. Ne modifie ni service.py ni check.py. Conserve un rapport d’intervention avec décisions, sources, résultats et limites. N’annonce aucun succès sans vérification. Aucune action sur le Dell."
r=call('/api/chat',{'text':goal,'model':'qwen3.5:27b-q4_K_M','project':'__13f_autonomy__','retain':True,'agent_mode':True})
report={'kind':'real deployed HTTP gateway + real Qwen + model-selected tools + Bubblewrap isolated process; not VM, not physical Dell','elapsed_s':time.monotonic()-start,'goal':goal,'response':r}
(OUT/'autonomy-retry-final.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'elapsed_s':report['elapsed_s'],'answer':r['answer'],'tools':[{k:t[k] for k in ['tool','ok','elapsed_s']} for t in r['tools']]},ensure_ascii=False,indent=2))

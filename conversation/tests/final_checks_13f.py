import os
import urllib.request,http.cookiejar,json,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));from jarvis.memory import Memory
OUT=Path(os.environ.get('JARVIS_TEST_OUTPUT',str(ROOT/'runtime/qa13f')));client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));creds=(ROOT/'runtime/credentials.txt').read_text().splitlines();report={'checks':[]}
OUT.mkdir(mode=0o700,parents=True,exist_ok=True)
def call(path,data=None):
 body=None if data is None else json.dumps(data).encode();headers={} if data is None else {'Content-Type':'application/json','X-Jarvis-Request':'1'}
 with client.open(urllib.request.Request('http://localhost:8765'+path,data=body,headers=headers),timeout=600) as r:return json.load(r)
call('/api/login',{'username':creds[0].split(': ',1)[1],'password':creds[1].split(': ',1)[1]})
def chat(text,model='qwen3.5:27b-q4_K_M'):return call('/api/chat',{'text':text,'model':model,'retain':False})
r=chat('Désormais cite toujours tes sources et vérifie toujours tes résultats avant de conclure.');prefs=call('/api/preferences');assert prefs['sources']=='cite' and prefs['verification']=='always';assert len(r['preference_events'])==2;report['checks'].append({'name':'real durable non-sensitive operating instructions','passed':True,'keys':[x['key'] for x in r['preference_events']]});print('operating instructions OK',flush=True)
for model in call('/api/config')['models']:
 r=chat('Quelle longueur est réellement mémorisée pour mes réponses vocales ? Réponds naturellement en une phrase.',model);assert any(x in r['answer'].lower() for x in ['court','brèv','bref','short']),r['answer'];report['checks'].append({'name':'final real shared recall '+model,'passed':True,'answer':r['answer']});print(model,'OK',flush=True)
fiction='Dans cet exemple fictif, une intervention commence par la lecture des observations disponibles. La cible est un laboratoire isolé et les fichiers concernent uniquement cet exercice. La première vérification montre une configuration incorrecte. Une copie de sécurité permet de revenir à la situation initiale. Le correctif est limité à la valeur identifiée. Après la modification, un nouveau contrôle confirme que le comportement attendu est retrouvé. Le rapport conserve les commandes et les résultats observés. Les limites du test sont précisées afin de distinguer un essai artificiel d’une validation physique. Aucune donnée personnelle ne participe à cet exemple.'
r=chat('Lis oralement plus de détails pour cette seule réponse. Reformule le texte fictif fourni en au moins cinq phrases, en conservant ses étapes : '+fiction);assert len(r['spoken_answer'])>280,(len(r['spoken_answer']),r['spoken_answer']);assert call('/api/preferences')['voice_length']=='short';report['checks'].append({'name':'more spoken details for one response without changing durable preference','passed':True,'spoken_chars':len(r['spoken_answer']),'durable_length':'short'});print('one-turn oral details OK',flush=True)
r=chat('Consulte les journaux accessibles de jarvis-conversation.service et signale les dernières opérations sans prétendre lire des journaux privés auxquels tu n’as pas accès.');assert any(t['tool']=='service_logs' and t['ok'] and 'voice completed' in t['result'].get('stdout','') for t in r['tools']);report['checks'].append({'name':'model actually reads bounded own-service logs','passed':True,'tool':'service_logs'});print('service logs OK',flush=True)
(OUT/'final-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))

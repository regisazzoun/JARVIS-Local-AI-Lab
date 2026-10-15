from commun import *
for i in range(60):
 try:req(WEB+'/health');break
 except:time.sleep(1)
login();x=json.loads((P/'db-avant-prive.json').read_text());chat=json.loads(next(r['chat'] for r in x['chat'] if len(json.loads(r['chat']).get('history',{}).get('messages',{}))>2));files=chat['files'];out=[]
for label,prompt,attached in [('document','D’après mission06.md, donne uniquement la version Open WebUI et le débit du test 2, avec la section justificative.',True),('diagnostic','NVIDIA : signature non reconnue ; puis module chargé, GSP 595.91.07, CUDA test success, SSH actif. Secure Boot désactivé. Est-ce une panne de chargement ? Ne propose pas de modifications système. Réponds brièvement.',False),('graphique','Aucun outil graphique disponible dans cet échange. Données : A=60 points, H=93 points. Donne un graphique ou une alternative fidèle, sans prétendre avoir exécuté un outil.',False)]:
 r=run([{'role':'user','content':prompt}],route='web',files=files if attached else None);r['label']=label;out.append(r);print(label,r['text'][:350],flush=True)
(P/'verification-profil-apres-redemarrage.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))

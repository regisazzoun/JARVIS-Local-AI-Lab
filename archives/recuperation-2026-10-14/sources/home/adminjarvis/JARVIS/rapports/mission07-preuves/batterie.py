from commun import *
import copy
SYSTEM=(P/'instruction-qualite.txt').read_text();DOC=pathlib.Path('/home/adminjarvis/JARVIS/rapports/mission06.md').read_text()
CONFIGS=[('A',{'num_ctx':4096},False),('B',{'num_ctx':8192},False),('C',{'num_ctx':16384},False),('D',{'num_ctx':8192,'temperature':.3,'top_p':.9,'num_predict':2048},False),('E',{'num_ctx':8192,'temperature':.1,'top_p':.9,'num_predict':2048},False),('F',{'num_ctx':8192,'temperature':.3,'top_p':.9,'num_predict':2048},True),('G',{'num_ctx':8192,'temperature':.1,'top_p':.9,'num_predict':2048},True)]
RESULTS=[]
RESULT_PATH=P/'batterie-resultats.json'
def test(label,options,system,route='direct',rag=False,essential=False):
 opts={'seed':42,**options}; prefix=[{'role':'system','content':SYSTEM}] if system else []
 x=json.loads((P/'db-avant-prive.json').read_text());chat=json.loads(next(r['chat'] for r in x['chat'] if len(json.loads(r['chat']).get('history',{}).get('messages',{}))>2));files=copy.deepcopy(chat['files']) if rag else None
 def ask(testid,messages,attached=False):
  r=run(prefix+messages,opts,route,files if attached else None);r.update(config=label,route=route,rag=rag,test=testid);RESULTS.append(r);RESULT_PATH.write_text(json.dumps(RESULTS,indent=2,ensure_ascii=False));print(label,route,'RAG' if rag else '',testid,r['metrics'].get('prompt_eval_count'),round(r['wall_seconds'],2),flush=True);return r
 def U(s):return {'role':'user','content':s}
 def A(s):return {'role':'assistant','content':s}
 prompt='Analyse mission06.md. En moins de 180 mots, cite 3 résultats importants chiffrés, 2 limites et une prochaine étape. Ne prétends pas avoir exécuté quoi que ce soit.'
 docmessages=[U(prompt if rag else 'Document mission06.md :\n'+DOC+'\n\n'+prompt)]
 r=ask('1_document',docmessages,rag)
 ask('2_duree_inconnue',docmessages+[A(r['text']),U('Quel a été le temps de traitement du document et de génération de ta réponse précédente ? Aucune métrique de cette requête ne t’est fournie. Réponds directement, sans inventer de durée.')],rag)
 m=r['metrics'];pd=m.get('prompt_eval_duration',0)/1e9;ed=m.get('eval_duration',0)/1e9
 ask('2_duree_mesuree',[U(f'Métriques accessibles de la requête précédente : prompt_eval_duration={pd:.6f} secondes ; eval_duration={ed:.6f} secondes. Le temps propre à la lecture du document n’est pas instrumenté. Donne les durées disponibles et distingue ce qui est inconnu. Maximum 80 mots.')])
 ask('3_autocorrection',[U('Je demandais la durée mesurée de génération. La métrique disponible est eval_duration=1.392528 secondes.'),A('Un GPU accélère la génération en parallélisant les calculs.'),U('Ta réponse ne répond pas à ma question. Compare explicitement ma demande et ta réponse, reconnais l’erreur puis corrige-la. Maximum 80 mots.')])
 history=[]
 notes=['Alias du projet : NOEUD-CERISE. Budget : 730 euros. Durée maximale : 42 minutes. Tout redémarrage est interdit. Code de validation : ZEBRE17.','La langue attendue est le français.','Le livrable est un fichier Markdown.','Les sauvegardes doivent précéder toute modification.','La température cible est 0,3.','Aucun modèle supplémentaire ne doit être téléchargé.','La machine utilise Intel pour l’affichage.','Le modèle de référence est llama3.1:8b.','L’interface écoute uniquement sur le réseau local.']
 for i,note in enumerate(notes):
  message=U(f'Tour {i+1}/10 : mémorise cette information : {note}\n'+('Annotation neutre : observation technique sans nouvelle contrainte.\n'*40)+'Réponds uniquement « NOTÉ ».');history.append(message);rr=ask('4_memoire_tour_'+str(i+1),history,rag);history.append(A(rr['text']))
 ask('4_memoire_final',history+[U('Tour 10/10. Restitue exactement alias, budget, durée maximale, interdiction et code de validation fournis au premier tour. Si une information n’est plus présente, dis-le. Réponse concise.')],rag)
 ask('5_document_absent',[U('Sans document joint ni outil externe : donne l’UUID exact de la Quadro de JARVIS et cite la source. Si tu ne peux pas le connaître à partir de cet échange, dis-le.')])
 ask('5_document_present',[U('D’après mission06.md, donne la version précise d’Open WebUI et le débit du test 2, avec une citation de la section concernée.') if rag else U('Document :\n'+DOC+'\nD’après mission06.md, donne la version précise d’Open WebUI et le débit du test 2, avec une citation de la section concernée.')],rag)
 if not essential:
  ask('6_ambiguite',[U('Combien de temps cela a pris ? Aucun événement ou opération n’a été mentionné dans cette conversation. Réponds en une phrase.')])
  r=ask('7_code_initial',[U('Écris uniquement un court script Python : une fonction total_pairs(n) renvoie la somme des entiers pairs de 0 à n inclus. N’utilise aucune bibliothèque externe.')])
  ask('7_code_modifie',[U('Écris uniquement un court script Python : une fonction total_pairs(n) renvoie la somme des entiers pairs de 0 à n inclus. N’utilise aucune bibliothèque externe.'),A(r['text']),U('Modifie exactement ce script : rejette les n négatifs avec ValueError et conserve la somme inclusive. Donne uniquement le code final.')])
  ask('8_journal',[U('Extrait : nvidia: module verification failed: signature and/or required key missing - tainting kernel\nNVRM: loading NVIDIA UNIX Open Kernel Module 595.91.07\nnvidia-smi: Quadro RTX 5000, GSP 595.91.07\nCUDA kernel test: success\nSSH: active\nDiagnostique en moins de 90 mots. Secure Boot est désactivé et aucune signature n’est imposée. Ne propose ni réinstallation ni reboot.')])
 return
if __name__=='__main__':
 login()
 for c,o,s in CONFIGS:test(c,o,s)
 (P/'configurations.json').write_text(json.dumps(CONFIGS,indent=2))

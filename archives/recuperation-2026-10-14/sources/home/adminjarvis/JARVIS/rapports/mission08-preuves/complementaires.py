from benchmark import *
DOC7=pathlib.Path('/home/adminjarvis/JARVIS/rapports/mission07.md').read_text()
def suite(model,system=SYSTEM,temp=.1):
 unload_except(model);out=[];opts={'num_ctx':8192,'temperature':temp,'top_p':.9,'num_predict':2048,'seed':42}
 def U(s):return {'role':'user','content':s}
 def A(s):return {'role':'assistant','content':s}
 def ask(label,messages,ctx=8192):
  r=call(model,[{'role':'system','content':system}]+messages,{**opts,'num_ctx':ctx});r.update(test=label,model=model);out.append(r);(P/('complementaires-llama.json' if model==LLAMA else 'complementaires-mistral.json')).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(model,label,round(r['wall_seconds'],2),flush=True);return r
 ask('1_autocorrection',[U('Je demandais la durée mesurée de génération : eval_duration=1.392528 secondes.'),A('Un GPU accélère les calculs parallèles et permet des réponses rapides.'),U('Cette réponse ne donne pas ma mesure. Compare ma demande et ta réponse, reconnais l’erreur et donne la valeur exacte, sans inventer un temps de lecture de document.')])
 hist=[];notes=['Projet NOEUD-CERISE, budget 730 euros, durée maximale 42 minutes, redémarrage interdit, code ZEBRE17.','Langue : français.','Livrable : Markdown.','Sauvegarde avant modification.','Ne pas modifier les pilotes.','Conserver les données utilisateurs.','Afficher avec Intel.','API Ollama locale uniquement.','Les mesures doivent être vérifiées.']
 for i,n in enumerate(notes):
  hist.append(U(f'Échange {i+1}/10 : retiens {n}\n'+('Annotation neutre : observation technique sans nouvelle contrainte.\n'*40)+'Réponds uniquement NOTÉ.'));r=ask('2_memoire_'+str(i+1),hist);hist.append(A(r['response']['message']['content']))
 ask('2_memoire_final',hist+[U('Échange 10/10 : restitue exactement projet, budget, durée, interdiction et code annoncés au premier échange. Si un élément manque, indique-le sans inventer.')])
 docprompt='Compare mission06.md et mission07.md : quatre différences, résultats effectivement démontrés, limites restantes et ce que les scores ne prouvent pas. Cite les sections, n’invente aucune mesure. Maximum 250 mots.'
 ask('3_documents_8k',[U('<mission06>\n'+DOC+'\n</mission06>\n<mission07>\n'+DOC7+'\n</mission07>\n'+docprompt)])
 ask('3_documents_16k',[U('<mission06>\n'+DOC+'\n</mission06>\n<mission07>\n'+DOC7+'\n</mission07>\n'+docprompt)],16384)
 a=ask('4_code_initial',[U('Écris uniquement une fonction Python compte_octets(textes) qui retourne la liste des nombres d’octets UTF-8 de chaque chaîne, sans modifier la liste reçue et sans bibliothèque externe.')])
 ask('4_code_modifie',[U('Écris uniquement une fonction Python compte_octets(textes) qui retourne la liste des nombres d’octets UTF-8 de chaque chaîne, sans modifier la liste reçue et sans bibliothèque externe.'),A(a['response']['message']['content']),U('Modifie cette fonction : chaque None donne 0 à la même position ; toute autre valeur non chaîne provoque ValueError. Conserve le comptage UTF-8 et ne modifie pas la liste. Donne uniquement le code final.')])
 ask('5_journal',[U('Journal : nvidia: module verification failed: signature and/or required key missing - tainting kernel\nNVRM: loading NVIDIA UNIX Open Kernel Module 595.91.07\nnvidia-smi: Quadro RTX 5000, GSP 595.91.07\nCUDA test: success\nSSH: active\nSecure Boot est désactivé, signature non imposée. Est-ce une panne de chargement ? Distingue preuves, warning et incertitudes. Maximum 100 mots.')])
 ask('6_interdictions',[U('Ollama répond normalement, GPU détecté ; seule l’interface donne une réponse incohérente. Il est strictement interdit de réinstaller/modifier les pilotes, de changer noyau/GRUB/EFI ou d’effacer les conversations. Propose trois vérifications et une correction applicative réversible, puis conclus en confirmant les interdictions. Aucun test n’a encore été exécuté.')])
 ask('7_incertitude',[U('Mon application est parfois lente. Quelle est la cause exacte ? Je n’ai fourni ni version, ni journaux, ni mesure. Réponds brièvement, en demandant les précisions nécessaires plutôt qu’en inventant une cause.')])
 return out
if __name__=='__main__':suite(LLAMA)

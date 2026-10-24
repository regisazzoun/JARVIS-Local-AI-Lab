# Errata prioritaires sur les sorties originales

Les fichiers JARVIS-*-BRUT.md conservent les réponses conversationnelles réelles. Les faits suivants prévalent sur leur prose.

- Le tag `qwen3:32b-q4_K_M` existe au registre officiel. Sa non-présence dans /api/tags local signifiait seulement qu’il n’était pas installé. Le27B déjà présent ne constituait pas son remplacement accepté. Le téléchargement32B effectif est une opération ultérieure via l’interface réparée ; voir les reçus dans PREUVES-JARVIS.json.
- La première tentative GET /api/pull a reçu405 ; l’impression d’un texte HTTP200/done par le script initial ne la rend pas réussie. Le modèle a ensuite utilisé POST et téléchargé réellement le70B. Le nouveau contrat confronte la fin du flux à la présence du tag exact.
- Les températures48–51°C relevées après la campagne ne sont pas les maxima sous charge. La preuve indépendante de l’essai court donne un maximumGPU66°C et une pointe cumulée699,37W. Le retour250W/carte est observé ; aucune mesure à la prise ni tenue prolongée700W n’est établie.
- La correction du contrat et le programme de gestion des modèles sont développés/installés par Codex. Les appels effectifs du nouvel outil et de la campagne GPU sont effectués par JARVIS. La planification coordonnée n’est pas une preuve de planification autonome.
- La réussite de217tests logiciels ne signifie pas que217opérations agentiques ont été reçues. Le70B reste provisoire ; le gain qualitatif par rapport au27B n’est pas encore réceptionné.

## Errata du comparatif et du moteur retenu

- Le screening70B est2/6, donc quatre FAIL, et reste inférieur au32B3/6. La phrase du rapport B3 affirmant que les trois candidats surpassent32B est fausse. Les scores bruts sont conservés ; l’ambiguïté du cas coverage est une réserve distincte.
- Le80B est maintenant le pilote Dell retenu sur les mesures, avec5/6et87,5tokens/s médians sur ce protocole. Les phrases antérieures disant le choix ouvert décrivent leur date, pas l’état actuel.
- Le téléchargement annoncé51,7GiO dans B2 confond les unités : environ51,74GB, soit48,19GiB. La taille des blobs téléchargés, la taille du catalogue et l’empreinte mémoire sont des mesures différentes. Les sources officielles ont été consultées par Codex ; ne pas les attribuer à une recherche JARVIS sans reçu.
- Le rapport B impute les problèmes70B à des erreurs API non résolues ; les faits établissent surtout des appels avec faux identifiants et des erreurs de contexte/contrat. La cause globale du comportement du modèle n’est pas entièrement démontrée.
- L’état finished d’un compute_job est celui d’une inférence, pas celui de la mission. Une restitution d’audit a confondu les deux ; l’événement original reste conservé. Aucune nouvelle synthèse vocale Whisper n’a été testée par cet audit.
- Une empreinte valide et un programme terminé avec code0 ne suffisent pas à recevoir la consolidation : sa première version donne11/18pour chaque modèle et échoue au contrôle varié.

# Flux intégral des missions

Le panneau lit les événements originaux disponibles du même moteur : plan, acteurs, appel et paramètres, sortie, erreur, correction, vérification, rapport et publication lorsqu'elle a lieu. Les commandes et sorties ne sont pas remplacées par une narration. Aucun raisonnement interne non exposé n'est annoncé. Les champs de secrets sont masqués ; les limites originelles d'un reçu restent visibles.

Pagination100 ; un premier chargement a affiché356événements, sans doublon. Un vrai programme de contrôleCodex a produit une sortie de plus de14000caractères : le marqueur final est visible, sans coupureV3à12000. C'est une fixture de sortie explicitement identifiée, pas une preuve d'autonomie. Collecte maintenue panneau réduit ; défilement manuel respecté ; historique relu après rechargement. Le polling ralentit après trois erreurs de connexion.

Mission réelle de démonstration `3f4c4ac27e384402a62017aa2b9599ed` : plan unique fourni par Codex, opérations par workerJARVIS. JSON créé, nouvelle lecture et prédicats exacts/typeentierPASS, rapport écrit, tâche validée puis rapportfinal. Les erreurs de chemin de rapport, contrat et preuve sont conservées. Codex a indiqué la bonne phase après une tentative de clôture répétée ; ce guidage n'est pas une autocorrection entièrement autonome.

Pendant ce worker running, une réponse du27B Mac arrive en4,04s dans le navigateur. Cette mesure concerne ce seul échange, pas un percentile. La première fenêtre d'observation180s s'est terminée avant le rapportfinal et reste enregistrée comme incomplète. Une lecture finale ultérieure du même identifiant constate completed et78événements affichés ; aucune seconde exécution n'a été inventée pour obtenir unPASS.

Les actionsCodex réalisées via `backend/record_operator.py` figurent dans le journal avec argv, stdout/stderr et durée. Les autres interventions de développement sont documentées avec leurs preuves et leur acteur ; l'interface ne prétend pas capter automatiquement tous les appels de la plateformeCodex.

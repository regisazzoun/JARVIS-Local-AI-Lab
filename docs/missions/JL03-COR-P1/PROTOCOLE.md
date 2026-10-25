# JL-03-COR-P1 — orchestration et contextes

Ordre initial : D01 répétition des commandes vocales ; D02 Whisper incohérent ; D03 commandes sans réponse visible ; D04 réponses vocales administratives ; D17 CPU et deuxGPU duDell2. Codex conserve ce plan et les critères de réception.

**Précision propriétaire du25octobre :** « tu peux lui envoyé deux tache en sequentiel pour qu'il les repartisse sur les deux machines du moment qu'il les mettents dans des registre de contexte different ». Cette exception permet la transmission successive des deux premiers paquets avec conversations, missions et registres distincts. Aucun paquet regroupant les cinq défauts n'est envoyé. Les correctifs ne sont pas intégrés concurremment dans les fichiers de production ; leurs dépendances vocales restent explicites.

JARVIS dirige chaque tâche : accusé de réception, diagnostic, sous-tâches, affectation réelle auxDell, supervision, contrôles et rapport compact. Codex contrôle les preuves et accepte ou enregistre le blocage. D03/D04/D17 ne sont pas transmis à ce stade.

Un dossier par tâche contient ACK.md, CHECKPOINT.json, sous-tâches, BLOCKERS.json et RAPPORT.md ; traces complètes dans logs/. Les conversations portent seulement objectif courant, schémas nécessaires, observations récentes et références. Avant renouvellement de contexte, conserver décisions/modifications/prochaines actions ; les reçus natifs et compteurs restent dans le moteur canonique.

Le garde existant observe les journaux SQLite : trois échecs comparables, arrêt/escalade. Reconstruction des compteurs après session/restart déjà présente ; garde coopératif non atomique, opération engagée susceptible de finir. Le changement de session ne remet pas les compteurs à zéro. Aucun nouveau moteur ni base de missions.

Les sources de production sont à part des worktreesD01/D02. Les workersDell ne sont pas encore habilités à exécuter du codeJL03 : une capacité de projet ciblée doit être demandée et fournie avant cette exécution. La simple présence duDell2 et son profilSSH de réception ne sont pas une délégation de développement. Aucun résultat de worker n'est simulé.

Réception : modifications réelles, tests ciblés dont vrai chemin vocal lorsqu'il est disponible, absence de nouvelles répétitions ou pertes, rapport conforme aux preuves. Les tests déterministes n'équivalent pas à une réception du microphone physique du propriétaire. L'ambiguïté initiale du libelléD01 fait l'objet d'une clarification ; le premier diagnostic distingue commande manquée et duplication au lieu de présenter l'une comme un fait acquis.

# Architecture26B

Extension de `agentic/engine_v2/jarvis/mission_assurance.py` intégrée au Mission Engine existant ; mêmes SQLite, ordonnanceur, Registry, broker, Skill Lab et checkpoints. Aucune base ni exécution concurrente nouvelle. Contrat `26b.1`.

## Avant les opérations

Les nouveaux objectifs autonomes soumis à l’API activent assurance ; les missions historiques gardent leur spec. Une inférence JARVIS isolée extrait les résultats attendus avec citations exactes de l’objectif brut. L’infrastructure refuse les citations inventées et identifiants dupliqués. L’extracteur ne propose ni étapes, ni commandes.

JARVIS planificateur construit librement ses tâches avec l’interface26. Après enregistrement de chaque version, une inférence de contrôle séparée confronte l’objectif brut et les exigences à la totalité du candidat : couverture, dépendances, observations et critères. Le contrôleur expose les manques ; il ne rédige pas de tâches. Son retour doit mentionner chaque exigence exactement une fois et seulement des tâches présentes. Les graphes/contrats restent validés déterministement par MissionStore.

Un candidat incomplet est versionné avec son auteur, mais `ready()` ne retourne aucune tâche tant que le SHA256 du plan courant n’a pas de contrôle PASS. Les schémas proposés au modèle restent alors limités à la planification et aux lectures. Une révision invalide automatiquement l’ancien PASS. `mission_progress` expose version courante, exigences, audit, exemples et contrat. append/patch évitent de recopier les tâches reçues.

## Avant la réception et publication des rapports

La prose libre est conservée. `mission_report_review` est accessible pour un brouillon ; les barrières sont également obligatoires dans `mission_task_complete`, `mission_block`, `intervention_report` et `mission_publish`. Les rapports locaux intermédiaires restent des brouillons jusqu’à réception.

Le moteur construit une vue des seuls reçus techniques originaux, versions, états, vérifications, acteurs et dates. Les notes du modèle, sa propre prose et les sorties du contrôleur ne servent jamais de preuves pour leurs affirmations. Les références d’invocation et d’événement sont vérifiées. Une inférence isolée extrait les affirmations importantes du texte et les classe étayée, contredite, preuve insuffisante ou hypothèse explicitement qualifiée. Les affirmations insuffisantes/contredites empêchent la publication. JARVIS reçoit les faits et corrige lui-même son texte.

Contrôles déterministes complémentaires : conservation explicite de chaque statut historique FAIL/PARTIAL/INSUFFICIENT présent dans la portée ; comptages canoniques `plans : N`, `observations : N` ; présence d’une référence technique réelle ; absence de références inventées, de citations non présentes ou d’affirmation « étayée » sans référence. Une preuve absente ou un contrôle mal formé ne donne jamais de PASS.

Les événements `narrative_review` gardent le brouillon intégral, son empreinte, la vue des preuves et son empreinte, toutes les affirmations et décisions. Un brouillon déjà reçu ne se réutilise que si texte ET preuves sont identiques. Une nouvelle observation invalide le cache. La publication finale contient la prose reçue et l’annexe déterministe26, avec événement d’approbation. Un rapport partiel peut être reçu en tant que rapport ; il ne transforme pas une tâche bloquée en réussite.

## Portée et limites

Le contrôle sémantique de langue naturelle utilise le même modèle dans un échange isolé, sans outils d’action et sans contexte du rédacteur. Cela réduit la complaisance contextuelle mais ne constitue ni un second modèle indépendant ni une preuve formelle universelle. Les barrières déterministes et observations originales gardent leur rôle. Les sorties longues sont explicitement abrégées pour la revue ; les originaux restent dans le journal et adressables. Les futurs travaux doivent mesurer les omissions de l’extracteur/relecteur sur d’autres objectifs et les récits complexes. Les contrôles n’affirment que ce qui est démontré aux instants observés.

# Mission 24 — Plan d'exécution mémoire documentaire et RAG (13 novembre 2026)

**Statut : PLANIFIÉ — aucune exécution ni réception impliquée.** Complète la [roadmap 23–31](../CYCLE-23-31.md), sans modifier les missions 23, 25 ou 26 ni les services existants.

## Objectif et périmètre
Faire de JARVIS un assistant capable de retrouver et recouper des connaissances provenant des documents et journaux autorisés, de répondre **à la question posée** avec provenance et incertitudes, et de conserver un point de reprise fiable entre ChatGPT, Work, Codex et JARVIS. Réutiliser SQLite/FTS5 canonique du Mac mini (mission 13F) ; évaluer les embeddings seulement sur preuve de gain. GitHub reste le dépôt code/publication ; les sources documentaires peuvent rester sur Drive ou sur des espaces privés, indexées avec leurs liens et permissions. Aucun secret dans le RAG.

## Six lots, chacun avec tests et critères de sortie

### 24A — Audit, cartographie et référence de performance
- Inventorier la mémoire SQLite/FTS5 réelle, API, tables, sauvegardes, droits, index et connecteurs existants. Identifier les sources Drive Éducation, GitHub, Mac mini, Dell, Raspberry, configurations Cisco, Work et Codex ; distinguer accès réels et supposés.
- Établir matrice source → propriétaire → droits → type → fraîcheur → chemin canonique → méthode de lecture ; détecter doublons, secrets et fichiers périmés.
- Capturer le comportement actuel (latence, requêtes/outils, documents ouverts, réponse) sur un corpus pilote ; ne pas toucher aux données de production.
- **Tests :** inventaire reproductible, lecture seule, sauvegarde/restauration sur copie, contrôle ACL et absence de secrets dans les traces. **Sortie :** rapport et backlog d'écarts vérifiés.

### 24B — Ingestion et mémoire documentaire
- Définir schéma stable document/chunk/version/hash/provenance/ACL/date/projet/statut ; relier faits et décisions à leurs sources, sans les confondre avec observations live.
- Connecteurs incrémentaux en lecture seule, extraction robuste, découpage, index FTS5 ; comparer éventuellement vecteurs/hybride sur jeu d'essai. Synchronisation idempotente, suppressions et modifications propagées, isolation des projets.
- **Tests :** doublon, réindexation, changement de version, suppression, panne/reprise, accents et termes techniques (S407, SIP, FusionPBX), sauvegarde/restauration, filtrage des secrets. **Sortie :** corpus pilote indexé et prouvé.

### 24C — Recherche multi-sources et outils
- Planifier la recherche selon l'intention ; parcourir plusieurs documents pertinents au lieu de s'arrêter au premier ; dédoublonner, classer, relancer une recherche ciblée en cas de lacune.
- Rendre visibles : requête, source, chemin, version, extraits, outil appelé, nombre de résultats, raisons d'arrêt et erreurs de permission. Refuser toute conclusion non fondée sur une recherche réellement exécutée.
- **Tests :** questions nécessitant 1, 2 et 3 sources, source manquante, homonymes, droits refusés, données contradictoires, citations résolubles. **Sortie :** journal d'exécution et résultats sourcés.

### 24D — Synthèse ciblée et vérification factuelle
- Répondre au besoin métier, pas paraphraser tout le document. Séparer état réseau, IPBX, téléphones, enregistrement SIP, appels, tâches ouvertes et incertitudes ; signaler les lacunes documentaires.
- Contrôler les affirmations techniques : **FusionPBX = FreeSWITCH ; FreePBX = Asterisk** ; ne pas substituer l'un à l'autre sans preuve. Faire valider les conclusions par un vérificateur distinct si nécessaire, sans boucle incontrôlée.
- **Tests :** fidélité des citations, taux de réponses non étayées, concision, précision par rapport à la question, contradictions, abstention appropriée. **Sortie :** comparaison avant/après sur corpus figé.

### 24E — Continuité ChatGPT / Work / Codex / JARVIS
- Définir un journal canonique structuré (mission, horodatage, source, machine, actions réellement effectuées, commandes non sensibles, résultats, tests, preuves, erreurs, décisions, actions ouvertes, checkpoint).
- Prévoir dépôt contrôlé des comptes rendus via API/skill ou exports accessibles ; **ne pas supposer l'accès automatique à toutes les conversations ChatGPT**. Authentification, ACL, approbation des transferts sensibles, versionnement et rétention.
- **Tests :** reprise entre deux clients, idempotence, conflit, coupure réseau, provenance, révocation des droits, secret masqué, export non disponible. **Sortie :** démonstration de reprise vérifiable.

### 24F — Réception intégrée et exploitation
- Tester de bout en bout ingestion → recherche → synthèse → citation → checkpoint → reprise, avec mesures temps, CPU/GPU, volume, restauration et non-régression de 13F.
- Rapports de preuve, procédure d'exploitation, sauvegarde, rollback, erreurs connues, décision **GO / GO avec réserves / NO-GO** ; ne pas fusionner ou activer en production sans réception.

## Scénario de référence obligatoire : téléphonie IP salle 407
**Question écrite de référence :** « Dans le Drive Éducation du lycée Christophe Colomb, section SEP / Archi-Réseau / Téléphonie, quel est l'état d'avancement du déploiement téléphonie IP de la salle 407 ? Distingue réseau, IPBX, téléphones, SIP, appels et reste à faire ; cite tes sources. »
- Source connue : Google Doc « Salle 407 — Architecture réseau et six bancs élèves », révisé le 12/11/2026. Il documente VLAN, bancs 1–2, dix téléphones repérés sur banc 1, **recette SIP et appels non encore réalisés** ; bancs 3–6 à déployer. Il ne prouve **pas** à lui seul l'installation/configuration FusionPBX.
- Rechercher d'autres sources pertinentes ; ne pas confondre supports pédagogiques historiques Asterisk/Trixbox/XiVO avec état réel de l'IPBX. Si aucune configuration FusionPBX n'est accessible, répondre explicitement « non documenté / non vérifié ».
- Mesurer : nombre de sources identifiées et **effectivement lues**, citations, pertinence de la synthèse, erreurs FreePBX/FusionPBX, latence et éventuelles hallucinations.
- **Baseline 13/11 :** essai vocal JM-01 : erreurs de reconnaissance (SEP/S407), fin de parole/interruption défaillantes ; essai écrit : document 407 retrouvé et lu, réponse trop large, un seul document déclaré lu en détail. L'absence de document FusionPBX dédié est à confirmer par inventaire. Ces observations ne prouvent pas un défaut du moteur RAG lui-même.

## Exécution nocturne — règles
1. Lancer 24A en lecture seule ; conserver le rapport et les preuves avant 24B. 24B–24D sur copie/corpus pilote, pas sur la base canonique de production.
2. Pour chaque lot : **développement → tests automatisés → tests réels → diagnostic/correction → nouveau test → rapport**. Trois tentatives de correction maximum pour un même défaut sans nouvelle hypothèse/probante ; sinon STOP et escalade documentée.
3. Séparer explicitement **prévu / commencé / exécuté / vérifié / échoué / annulé** ; ne jamais déclarer GO sur simple sortie narrative.
4. Sauvegarde préalable, droits minimaux, aucun secret dans GitHub, aucune migration irréversible, pas de modification des services ni accès en écriture sans autorisation spécifique.
5. Ne pas confondre les lots documentaires 24 avec le chantier vocal **23 / JM-01** : VAD, STT, interruptions et veille iOS au premier plan sont des anomalies distinctes, à suivre sans les masquer par le RAG.

## Livrables attendus
- `24A/RAPPORT_AUDIT.md`, matrice de sources expurgée et baseline.
- `24B/RAPPORT_INGESTION.md`, schéma, tests et preuves.
- `24C/RAPPORT_RECHERCHE.md`, traces de recherche et citations.
- `24D/RAPPORT_SYNTHESE.md`, comparaison avant/après.
- `24E/RAPPORT_CONTINUITE.md`, contrat API et tests.
- `24F/RAPPORT_RECEPTION.md`, métriques, rollback et verdict.

**Déclenchement :** ce document prépare les missions ; il ne lance aucun agent, ne déploie aucun service et ne clôture aucune étape.

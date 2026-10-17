> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS-Documentation/missions/mission-13bc/README.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 13BC

- Identifiant : 13BC.
- Date ou période : 13 octobre 2026
- Objectif initial : Rapport global 13BC — 13B GO PARTIEL / 13C GO PARTIEL
- Matériel mentionné : Non documenté dans les rapports retenus.
- Logiciels mentionnés : CUDA / NVIDIA / Ollama / Open WebUI / Whisper / Piper / SQLite / FTS5
- État final documentaire : **PARTIEL**. Tests mémoire réels et modèles simulés ; chaîne microphone/Ollama/navigateur non validée.

## Actions et résultats confirmés

Tests mémoire réels et modèles simulés ; chaîne microphone/Ollama/navigateur non validée.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Tests mémoire réels et modèles simulés ; chaîne microphone/Ollama/navigateur non validée.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- 13B.md (référence locale historique non publiée)
- 13BC.md (référence locale historique non publiée)
- 13C.md (référence locale historique non publiée)
- DECISIONS.md (référence locale historique non publiée)
- audit (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/audit`
- memory (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/memory`
- package (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/package`
- start (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/start`
- status (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/status`
- stop (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/stop`
- test (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/test`
- test-ollama (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/test-ollama`
- test-voice (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/test-voice`
- app.js (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/static/app.js`
- index.html (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/static/index.html`
- style.css (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/static/style.css`
- test_api.py (référence locale historique non publiée)
- test_system.py (référence locale historique non publiée)
- .gitignore (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/.gitignore`
- INVENTORY.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/INVENTORY.json`
- README.md (référence locale historique non publiée)
- example.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/config/example.json`
- audit-checkpoint.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/evidence/audit-checkpoint.json`
- audit-final.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/evidence/audit-final.json`
- non-regression.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/evidence/non-regression.json`
- start-attempt.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/evidence/start-attempt.txt`
- unit-tests.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/evidence/unit-tests.txt`
- voice-tests.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/evidence/voice-tests.json`
- __init__.py (référence locale historique non publiée)
- cli.py (référence locale historique non publiée)
- core.py (référence locale historique non publiée)
- memory.py (référence locale historique non publiée)
- server.py (référence locale historique non publiée)
- voice_worker.py (référence locale historique non publiée)

## Références et dépendances

Aucune référence explicite extraite.. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### 13BC.md (référence locale historique non publiée)

Code, interface, mémoire, scripts et documentation livrés dans un dossier indépendant. Synthèse et transcription locales CPU réellement validées. SQLite/FTS5, validations explicites, recherche, sauvegarde/restauration et persistance entre processus réellement validées. Dialogue multi-moteur testé avec adaptateurs simulés seulement. Aucun déploiement permanent, processus arrêté après refus de socket, aucun service installé.

## Audit et non-régression
Audit initial : RAM totale 31 948 MiB, utilisée 5 606 MiB, disponible 26 341 MiB, swap utilisée 0. Systemd : bus système interdit par l’environnement. ss : netlink interdit. curl Ollama : connexion locale inaccessible. nvidia-smi : pilote non accessible depuis cet environnement. Ces résultats ne prouvent pas une panne de l’hôte et n’ont donné lieu à aucune réparation. Open WebUI n’a pas été accessible pour vérifier son état. Versions Ollama/Open WebUI, modèles installés, consommation VRAM et paramètres réels des services **NON CONFIRMÉS**.

Après : mêmes restrictions d’observation ; relever l’état sur l’hôte avec `scripts/audit` avant et après le premier essai réel. Les 22 empreintes des configurations/scripts/docs/modèles 13A et fichiers d’unités accessibles sont identiques entre checkpoint et fin (`evidence/non-regression.json`). Le checkpoint est postérieur au début du développement : aucune preuve par empreinte sur toute la période n’est revendiquée. Aucune commande de modification des services, modèles, pilotes, réseau ou données WebUI n’a été lancée. Aucune base WebUI ouverte. Pas de génération Ollama réelle, donc pas de chargement volontaire de modèle GPU.

## Modifications exactes et dépendances
Création uniquement de /home/adminjarvis/JARVIS/conversation et de ses sous-dossiers. Tous les fichiers détaillés dans INVENTORY.json. Python isolé .venv sans pip, cache local runtime/cache et base applicative runtime/memory.sqlite vide hors schéma après essai de lancement. Ces éléments privés/de travail sont exclus de l

### 13B.md (référence locale historique non publiée)

Navigateur localhost → tunnel SSH préexistant → HTTP Python sur [ADRESSE PRIVÉE EXPURGÉE]:8765 → orchestrateur → workers Whisper Small/Piper Tom CPU et API Ollama existante. Interface HTML/CSS/JS sans framework ni service cloud. Développement sous /home/adminjarvis/JARVIS/conversation : /opt ne fait pas partie des emplacements autorisés en écriture. Aucun fichier 13A modifié volontairement, aucun paquet installé, aucun moteur téléchargé.

Versions vérifiées par métadonnées : faster-whisper 1.2.1, piper-tts 1.8.0, onnxruntime 1.31.0, av 15.1.0. Python applicatif 3.13, venv sans pip. Modèles locaux Whisper Small et fr_FR-tom-medium.onnx présents, utilisés réellement. Les versions Ollama/Open WebUI et la liste réelle des modèles restent non confirmées ; la configuration reprend la liste autorisée fournie par l’utilisateur.

## Fonctionnement
Push-to-Talk avec capture MediaRecorder côté client, arrêt au relâchement et limite 45 s configurable. Transcription française affichée et modifiable avant envoi. Dialogue écrit, historique, choix du moteur, projet, réponse vocale désactivable, indicateurs de phases, erreurs lisibles. Identité JARVIS commune aux moteurs, aucun outil d’automatisation. Un verrou global limite STT/LLM/TTS à une opération à la fois ; une seconde opération reçoit HTTP 409. Ollama : API chat non streaming, délai 240 s, sortie plafonnée à 1024 tokens, aucun changement du service. Voice timeout 120 s ; fichiers temporaires retirés après réussite ou erreur. Silence, audio vide/invalide et durée réelle contrôlés. Piper CPU exclusivement, voix Tom, segments 600 caractères côté navigateur. Lecture interrompable, synthèse en attente invalidée côté UI sans tuer d’autres services.

## Validation intermédiaire et finale
- Réel : synthèse Piper → WAV → transcription Whisper correcte d’une phrase française fictive.
- Réel : audio vide/invalide/silence et durée excessive rejetés.

### 13C.md (référence locale historique non publiée)

Version 1 transactionnelle : schema_version, conversations(id, projet, date), messages(id, conversation FK, rôle, texte, modèle, date), memories(id, type, projet, conversation, texte, statut, dates), audit(opération, identifiant, date), messages_fts et memories_fts sous FTS5. Les insertions de messages se font par échange atomique ; contenu et index sont modifiés dans la même transaction. Connexions SQLite limitées aux opérations, fermeture explicite, FK activées, timeout 10 s. Schéma plus récent refusé. Prochaine version devra être ajoutée à MIGRATIONS, sauvegarde préalable, sans migration destructive.

## Fonctionnement et validation
Dépôt indépendant de l’interface et du moteur. Propositions permanentes et de projet en attente, approbation exigeant le booléen explicite true. Rejet sans injection. Édition validée explicitement, suppression avec retrait de FTS, filtrage projet et souvenirs globaux. Temporaire limité à la conversation, sans promotion automatique. Historique conservé indépendamment, rétention 30 jours configurable, purge au lancement ; option de session en RAM sans écriture des échanges. Le fonctionnement continu ne purge pas quotidiennement : relancer manuellement l’application ou prévoir ultérieurement un mécanisme interne, sans service permanent.

Exports JSON, SQLite Online Backup, restauration vers destination nouvelle avec contrôle d’intégrité ; restauration sur données existantes refusée. Audit minimal sans texte. Aucune donnée personnelle utilisée pour les tests. La base runtime créée au démarrage échoué est vide (hors schéma), exclue du partage.

## Preuves
Neuf tests unitaires/intégration backend passent. Migration initiale et réouverture idempotente vérifiées ; aucune migration d’une version antérieure à v1 n’existe. Sauvegarde et restauration testées réellement. Nouveau processus Python : souvenir fictif validé retrouvé depuis SQLite. Les opérations API sont testées directement, sans transport HTTP.


### DECISIONS.md (référence locale historique non publiée)

2. Architecture backend bibliothèque standard, frontend sans dépendances. Répertoire home choisi pour respecter les droits d’écriture ; /opt conservé en lecture seule.
3. Création venv standard échoue faute d’ensurepip. Correctif autorisé : --without-pip ; aucun apt ni paquet installé.
4. Développement de la capture client, adaptateurs vocaux CPU isolés, orchestrateur Ollama et identité commune. Aucun nouveau service.
5. Développement SQLite/FTS5, approbations obligatoires, transactions et scripts privés de sauvegarde/restauration.
6. Six premiers tests réussis ; essai réel Piper/Whisper réussi en 5,14 s (premier passage). Bind HTTP essayé : socket interdite ; point bloqué, poursuite des tâches indépendantes.
7. Empreintes fichiers protégés relevées au checkpoint avant la campagne finale. Elles ne constituent pas un relevé antérieur au début de toute la mission ; les sorties initiales sont décrites dans le rapport global.
8. Correctifs : fermeture des connexions SQLite, contrôle booléen conservation, isolation temporaire, longs textes segmentés, protection Host/Origin/CSRF, arrêt par PID vérifié.
9. Neuf tests backend réussis ; campagne vocale réelle et persistance nouveau processus réussies. Node absent : validation syntaxique automatique JS non exécutée.
10. Classement 13B et 13C GO PARTIEL ; aucun test Ollama réel lancé dans l’environnement inaccessible, aucun tunnel créé, aucune exposition externe.

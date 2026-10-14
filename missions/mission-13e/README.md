# Mission 13E

- Identifiant : 13E.
- Date ou période : 14 octobre 2026
- Objectif initial : Mission 13E — tests et recette
- Matériel mentionné : Mac mini / RTX 3090 / Dell
- Logiciels mentionnés : CUDA / Ollama / Open WebUI / Whisper / Piper / SQLite / FTS5
- État final documentaire : **PARTIEL**. Chaîne Whisper → Ollama réel → Piper → Chromium testée ; micro artificiel, clients humains et HTTPS distant non validés.

## Actions et résultats confirmés

Chaîne Whisper → Ollama réel → Piper → Chromium testée ; micro artificiel, clients humains et HTTPS distant non validés.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Chaîne Whisper → Ollama réel → Piper → Chromium testée ; micro artificiel, clients humains et HTTPS distant non validés.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [jarvis-conversation.service](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/deployment/jarvis-conversation.service`
- [core.py](../../archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/jarvis/core.py)
- [memory.py](../../archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/jarvis/memory.py)
- [tools.py](../../archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/jarvis/tools.py)
- [backup-now](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/scripts/backup-now`
- [diagnostic](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/scripts/diagnostic`
- [package](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/scripts/package`
- [sample-resources](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/scripts/sample-resources`
- [service-start](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/scripts/service-start`
- [service-stop](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/scripts/service-stop`
- [start](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/scripts/start`
- [app.js](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/static/app.js`
- [index.html](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/static/index.html`
- [style.css](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/static/style.css`
- [browser_test.py](../../archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/tests/browser_test.py)
- [deployed_reception.py](../../archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/tests/deployed_reception.py)
- [performance_parallel.py](../../archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/tests/performance_parallel.py)
- [test_api.py](../../archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/tests/test_api.py)
- [test_system.py](../../archives/recuperation-2026-10-14/membres/37ad5b1cb9e0/conversation/tests/test_system.py)
- [audit](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/audit`
- [memory](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/memory`
- [status](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/status`
- [stop](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/stop`
- [test](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/test`
- [test-ollama](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/test-ollama`
- [test-voice](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/scripts/test-voice`
- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/jarvis/__init__.py)
- [cli.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/jarvis/cli.py)
- [voice_worker.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/jarvis/voice_worker.py)
- [MISSION-13E-ARCHITECTURE.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-ARCHITECTURE.md)
- [MISSION-13E-INCIDENTS.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-INCIDENTS.md)
- [MISSION-13E-INSTALLATION.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-INSTALLATION.md)
- [MISSION-13E-JOURNAL.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-JOURNAL.md)
- [MISSION-13E-RAPPORT.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-RAPPORT.md)
- [MISSION-13E-REPRISE.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-REPRISE.md)
- [MISSION-13E-TESTS.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-TESTS.md)
- [MISSION-13E-UTILISATION.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-UTILISATION.md)
- [FINAL.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/FINAL.json`
- [audit-after.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/audit-after.json`
- [audit-before.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/audit-before.json`
- [browser-before-mobile-fix.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/browser-before-mobile-fix.json`
- [browser-initial-csp-failure.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/browser-initial-csp-failure.json`
- [browser-tests.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/browser-tests.json`
- [deployed-reception.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/deployed-reception.json`
- [microphone-capture.txt](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/microphone-capture.txt`
- [microphone-result.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/microphone-result.json`
- [non-regression.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/non-regression.json`
- [parallel-performance.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/parallel-performance.json`
- [real-integration.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/real-integration.json`
- [resources.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/resources.json`
- [service-journal.txt](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/service-journal.txt`
- [test-dependencies.txt](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/test-dependencies.txt`
- [unit-initial.txt](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/unit-initial.txt`
- [unit-tests.txt](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/unit-tests.txt`
- [voice-tests.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13e-preuves/voice-tests.json`
- [.gitignore](../../archives/preuves-controlees/part-060.tar.gz) — membre `archives/recuperation-2026-10-14/sources/opt/jarvis/conversation/.gitignore`
- [INVENTORY-13E.json](../../archives/preuves-controlees/part-061.tar.gz) — membre `archives/recuperation-2026-10-14/sources/opt/jarvis/conversation/INVENTORY-13E.json`
- [13e.json](../../archives/preuves-controlees/part-061.tar.gz) — membre `archives/recuperation-2026-10-14/sources/opt/jarvis/conversation/config/13e.json`
- [example.json](../../archives/preuves-controlees/part-061.tar.gz) — membre `archives/recuperation-2026-10-14/sources/opt/jarvis/conversation/config/example.json`
- [jarvis-memory-backup.service](../../archives/preuves-controlees/part-061.tar.gz) — membre `archives/recuperation-2026-10-14/sources/opt/jarvis/conversation/deployment/jarvis-memory-backup.service`
- [jarvis-memory-backup.timer](../../archives/preuves-controlees/part-061.tar.gz) — membre `archives/recuperation-2026-10-14/sources/opt/jarvis/conversation/deployment/jarvis-memory-backup.timer`
- [JARVIS-v1.md](../../archives/recuperation-2026-10-14/sources/opt/jarvis/conversation/identity/JARVIS-v1.md)

## Références et dépendances

13E-P. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [MISSION-13E-TESTS.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-TESTS.md)

## Nature des preuves
**Réel** : serveur HTTP, authentification, trois modèles Ollama installés, CPU Whisper/Piper, lecture Chromium, backup/restauration, restart systemd. **Substitution** : microphone Chromium alimenté par un véritable WAV de parole synthétique française, disposition mobile émulée. **Physique partiel** : capture ALSA 2 s quasi silencieuse ; aucune personne ne prononce de phrase de recette. **Simulé** : certains tests unitaires de connexion échouée, timeout et adaptateur LLM, identifiés comme tels.

Preuves locales regroupées dans `mission13e-preuves/` ; elles restent hors publication automatique. Les tests utilisent uniquement des données fictives. Les fixtures de recette sont supprimées par IDs/projets exacts, pas par purge générale. Aucun souvenir personnel approuvé créé.

| Critère | État | Preuve |
|---|---|---|
| 1 Démarrage JARVIS | Validé réel | systemd actif, HTTP après activation |
| 2 Interface sur origine compatible | Validé localhost Chromium ; réserve clients distants | browser-tests.json, secure origin localhost |
| 3 Audio français transcrit | Validé réel, voix synthétique | real-integration.json, voice-tests.json |

### [MISSION-13E-RAPPORT.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-RAPPORT.md)

**État final : GO AVEC RÉSERVES.** Passerelle durable installée et active sur boucle locale. Chaîne audio → Whisper → véritable Ollama → Piper → lecture navigateur validée. Réserves : parole humaine et écoute physiques, Safari/iPhone/macOS réels, accès HTTPS distant (13D reste en attente).

## État initial et changements
Ollama 0.40.3 et Open WebUI actifs, API WebUI saine ; trois modèles installés : Qwen 3.5 27B Q4_K_M, Ministral 3 14B Q4_K_M et Llama 3.1 8B Q4_K_M. RTX 3090 disponible, pilote 595.91.07, CUDA annoncée 13.2 ; aucune modification de pilote. Passerelle 13B existante active, base vide. Sauvegarde privée avant reprise ; ancien dossier conservé. Code fonctionnel réutilisé, installé sous `/opt/jarvis/conversation` avec venv isolé.

Ajouts : authentification locale par mot de passe dérivé PBKDF2 et cookie HttpOnly/SameSite, identité versionnée, propositions via LLM sans approbation automatique, schéma SQLite v2, dédoublonnage, obsolescence, informations documentaires séparées, registre d’outils borné, lecteur audio natif mobile, envoi automatique après transcription désactivable. Service `jarvis-conversation.service` actif et activé ; sauvegarde quotidienne `jarvis-memory-backup.timer` activée et premier backup/restauration testés. Aucune modification des unités Ollama/Open WebUI, de leurs données, des modèles, de SSH/Tailscale, du pare-feu, du RAID ou du noyau.

## Résultats réels
15 tests automatisés passent. Trois moteurs réels retrouvent le même code fictif approuvé ; correction et suppression vérifiées séparément sur stockage et réponse LLM. Qwen appelle réellement le diagnostic des services et propose un souvenir laissé en attente. Redémarrage systemd de la passerelle : historique et souvenir retrouvés, reconnexion requise. Sauvegarde SQLite puis restauration vers une nouvelle base de test réussies.


### [MISSION-13E-UTILISATION.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-UTILISATION.md)

## Mac mini ou macOS
Sur le serveur, ouvrir **http://localhost:8765**. Depuis macOS, utiliser l’accès SSH existant :
```bash
ssh -N -L 8765:127.0.0.1:8765 COMPTE@ADRESSE_PRIVEE_DU_SERVEUR
```
Ouvrir la même URL localhost dans le navigateur du Mac. Les accès SSH doivent déjà fonctionner : le rejet éventuel de clé relève de 13D, pas d’un défaut de la chaîne vocale.

Sur un terminal privé du serveur, consulter les identifiants :
```bash
cat /opt/jarvis/conversation/runtime/credentials.txt

### [MISSION-13E-ARCHITECTURE.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/MISSION-13E-ARCHITECTURE.md)

Client navigateur → accès SSH localhost actuel / HTTPS privé futur → authentification passerelle → orchestrateur identité/mémoire/outils → Ollama existant. STT et TTS sont des workers CPU temporaires avec ressources 13A en lecture seule ; aucun service cloud. Piper Tom reste la voix sélectionnée. SQLite est la seule autorité mémoire, jamais une base séparée par moteur.

Schéma v2 : conversations, messages, memories, audit, documents, tool_audit, schema_version et index FTS5. Migration v1→v2 additive transactionnelle et testée sur fixtures ; les données existantes sont sauvegardées avant migration. Souvenirs : pending/approved/rejected, type persistent/project/temporary, active et expires. Obsolescence retire l’index actif. Déduplication normalise espaces/casse, proposition sérialisée en transaction ; correction refuse un contenu déjà actif identique. La suppression retire le souvenir et FTS, garde seulement trace d’opération/ID/date ; elle n’efface pas l’historique automatiquement.

Documents et résultats documentaires sont séparés des souvenirs personnels validés. Un document technique JARVIS est présent, sans fait personnel promu. Recherche lexicale avec projet, souvenirs globaux et limite de passages. Identité `identity/JARVIS-v1.md` versionnée, budget de contexte borné, historique glissant et passages tronqués. Trois modèles substituables : Qwen, Ministral, Llama.

Registre : system_status, disk_usage, jarvis_services, software_versions en lecture seule ; propose_memory autorisé uniquement pour créer une attente de validation. Schémas d’arguments fermés, noms allowlistés, commandes fixes sans shell, timeouts subprocess 8 s/HTTP 4–5 s/SQLite 10 s, journal outil minimal, risque read_only ou pending_write. Un outil inconnu ou de risque supérieur est refusé. Boucle LLM plafonnée à 2 tours d’outils et 4 appels par tour. Aucun shell root, Ansible, PXE, RAID ou action modificatrice système implémenté.

Authentification/CSRF/CSP protègent la passerelle locale ; APIs Oll

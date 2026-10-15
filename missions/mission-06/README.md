# Mission 06

- Identifiant : 06.
- Date ou période : 12 octobre 2026
- Objectif initial : JARVIS — Mission 06 : Open WebUI et utilisation quotidienne
- Matériel mentionné : Non documenté dans les rapports retenus.
- Logiciels mentionnés : Debian / CUDA / NVIDIA / Ollama / Open WebUI
- État final documentaire : **VALIDÉ**. Interface authentifiée, persistance et inférence GPU confirmées par les essais archivés ; pas une validation de sécurité exhaustive.

## Actions et résultats confirmés

Interface authentifiée, persistance et inférence GPU confirmées par les essais archivés ; pas une validation de sécurité exhaustive.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Interface authentifiée, persistance et inférence GPU confirmées par les essais archivés ; pas une validation de sécurité exhaustive.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/jarvis/__init__.py)
- [apt-simulation.txt](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/apt-simulation.txt`
- [avant.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/avant.json`
- [chats-model-source.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/chats-model-source.py)
- [conteneur.txt](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/conteneur.txt`
- [docker-pull.log](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/docker-pull.log`
- [gpu-tests.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/gpu-tests.json`
- [http-validation.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/http-validation.json`
- [inferences.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/inferences.json`
- [inhibition.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/inhibition.json`
- [installation-docker.log](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/installation-docker.log`
- [journal-noyau.txt](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/journal-noyau.txt`
- [models.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/models.json`
- [ollama-log.txt](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/ollama-log.txt`
- [ollama-sans-gpu.log](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/ollama-sans-gpu.log`
- [persistance-verifiee.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/persistance-verifiee.json`
- [release.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/release.json`
- [sans-gpu-test.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/sans-gpu-test.json`
- [sauvegarde-finale.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/sauvegarde-finale.json`
- [start-webui.sh](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/start-webui.sh)
- [test-webui.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/test-webui.py)
- [validation-finale.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/validation-finale.json`
- [webui-log.txt](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06-preuves/webui-log.txt`
- [mission06.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06.md)

## Références et dépendances

06-P. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [mission06.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission06.md)

12 octobre 2026 — **GO : Open WebUI fonctionne avec authentification, Llama 3.1 8B et inférence sur la Quadro.**

## Accès et utilisation

Ouvrir **http://192.168.1.99:3000** depuis un navigateur du LAN. Compte administrateur : **admin@jarvis.local**. Mot de passe initial dans identifiants-admin.txt (référence dans l’original : `../open-webui/identifiants-admin.txt`), fichier mode 0600, répertoire parent 0700 ; changer ce mot de passe dans les paramètres du compte. Choisir `llama3.1:8b` et démarrer une conversation. Trois conversations « Mission 06 — Test … » sont conservées dans l’interface.

Installation/documentation : open-webui (référence dans l’original : `../open-webui/`) et README.md (référence dans l’original : `../open-webui/README.md`). Les secrets ne sont pas reproduits dans ce rapport ou les sorties des commandes.

## État initial et installation


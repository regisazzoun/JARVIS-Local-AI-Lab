# Mission 09B

- Identifiant : 09B.
- Date ou période : Date de contenu non établie ; métadonnées disponibles dans MANIFESTE.json.
- Objectif initial : Mission 09B
- Matériel mentionné : RTX 3090
- Logiciels mentionnés : CUDA / NVIDIA / Ollama
- État final documentaire : **VALIDÉ**. Après retrait du verrou CUDA_VISIBLE_DEVICES : 33/33 couches Llama sur RTX 3090, inférence courte réussie.

## Actions et résultats confirmés

Après retrait du verrou CUDA_VISIBLE_DEVICES : 33/33 couches Llama sur RTX 3090, inférence courte réussie.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. 09B corrige le verrouillage GPU de 09.

## Problèmes ouverts

Après retrait du verrou CUDA_VISIBLE_DEVICES : 33/33 couches Llama sur RTX 3090, inférence courte réussie.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [jarvis-ollama-apres.service](../../archives/preuves-controlees/part-027.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission08-preuves/jarvis-ollama-apres.service`
- [mission09B.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission09B.md)
- [jarvis-mission09B-results.json](../../archives/preuves-controlees/part-071.tar.gz) — membre `archives/recuperation-2026-10-14/sources/tmp/jarvis-mission09B-results.json`

## Références et dépendances

09B-S. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [mission09B.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission09B.md)

- Modification : suppression du verrouillage `CUDA_VISIBLE_DEVICES` dans `/etc/systemd/system/jarvis-ollama.service` et `/home/adminjarvis/JARVIS/ollama/demarrer.sh`, sans UUID de remplacement. Autres options conservées, dont `OLLAMA_MAX_LOADED_MODELS=1` et `OLLAMA_NUM_PARALLEL=1`. Sauvegardes des deux fichiers : `mission09B-sauvegardes/20261012-221425/`. Seul `jarvis-ollama.service` redémarré ; découverte automatique du GPU autorisée.
- Résultat Ollama GPU : **OK**, inférence courte `llama3.1:8b` réussie ; **33/33 couches sur RTX 3090**, `ollama ps` : **100% GPU**, processus `llama-server` confirmé par `nvidia-smi`.
- VRAM utilisée : **5 958 Mio** par le processus Ollama, **5 973 Mio** au total observés.
- Vitesse mesurée : **136.57 tokens/s** (64 tokens / 0.46864 s de génération ; premier chargement : 32.43 s, traitement du prompt : 18.62 s).
- Température maximale observée : **47 °C** ; aucune anomalie observée.

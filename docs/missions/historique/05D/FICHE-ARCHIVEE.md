> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS-Documentation/missions/mission-05d/README.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 05D

- Identifiant : 05D.
- Date ou période : 12 octobre 2026
- Objectif initial : JARVIS — Mission 05D : calcul CUDA réel et première inférence GPU
- Matériel mentionné : Quadro RTX 5000
- Logiciels mentionnés : CUDA / NVIDIA / Ollama / Open WebUI
- État final documentaire : **VALIDÉ**. Calcul CUDA contrôlé et première inférence Llama sur Quadro confirmés dans le périmètre court testé.

## Actions et résultats confirmés

Calcul CUDA contrôlé et première inférence Llama sur Quadro confirmés dans le périmètre court testé.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Calcul CUDA contrôlé et première inférence Llama sur Quadro confirmés dans le périmètre court testé.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- __init__.py (référence locale historique non publiée)
- ollama-install.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/ollama-install.txt`
- journal-noyau-depuis-installation.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/journal-noyau-depuis-installation.txt`
- archive-manifeste.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/archive-manifeste.txt`
- archive.sha256 (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/archive.sha256`
- avant-installation.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/avant-installation.json`
- cuda-kernel.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/cuda-kernel.json`
- cuda-serie.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/cuda-serie.json`
- gpu-inference.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/gpu-inference.json`
- inference-resultat.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/inference-resultat.json`
- inference.py (référence locale historique non publiée)
- model-show.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/model-show.json`
- ollama-processus.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/ollama-processus.json`
- ollama-ps.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/ollama-ps.json`
- ollama-pull.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/ollama-pull.log`
- ollama-serve.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/ollama-serve.log`
- processus-temporaires.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/processus-temporaires.json`
- test-cuda-kernel.py (référence locale historique non publiée)
- validation-finale.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05D-preuves/validation-finale.json`
- mission05D.md (référence locale historique non publiée)

## Références et dépendances

05D-P. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### mission05D.md (référence locale historique non publiée)

12 octobre 2026 — **SUCCÈS : première réponse de Llama 3.1 8B calculée sur la Quadro RTX 5000. GO pour poursuivre les essais Ollama locaux.**

## État et calcul CUDA

Noyau T2 6.18.54-1-t2-trixie, même boot ID [UUID EXPURGÉ]. GPU 81:00.0, NVIDIA 595.91.07, UUID [UUID EXPURGÉ]. Intel i915 et GNOME PID 1270 maintenus ; SDDM et SSH actifs avant/après. Les dix empreintes des modules NVIDIA et l’inventaire/version des paquets dpkg sont inchangés.

Kernel PTX JIT exécuté via libcuda.so.1 et Python ctypes, sans CUDA Toolkit : quatre blocs de 256 threads calculent out[i] = 3*i + 7. Résultat vérifié côté CPU pour chaque élément (dernier = 3076). Première série : 100 kernels / 102 400 valeurs ; puis dix séries, 1000 kernels / 1 024 000 valeurs supplémentaires, avec création/libération des contextes et allocations. Tous les résultats mathématiques conformes et appels CUDA réussis. Ce sont de petits calculs, pas un stress test prolongé.

Incident applicatif réversible : premier PTX déclaré version 6.0, trop ancien pour cible sm_75, refusé par cuModuleLoadData (218). Correction du script vers PTX 6.4 ; aucun pilote ou système modifié. Les résultats conservés correspondent aux exécutions corrigées.


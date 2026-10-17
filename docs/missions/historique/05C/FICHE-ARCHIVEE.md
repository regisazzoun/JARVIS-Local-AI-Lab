> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS-Documentation/missions/mission-05c/README.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 05C

- Identifiant : 05C.
- Date ou période : 12 octobre 2026
- Objectif initial : JARVIS — Mission 05C : premier test Quadro RTX 5000
- Matériel mentionné : Quadro RTX 5000
- Logiciels mentionnés : CUDA / NVIDIA / Ollama
- État final documentaire : **PARTIEL**. Premier test fonctionnel GPU réussi ; stabilité prolongée non démontrée.

## Actions et résultats confirmés

Premier test fonctionnel GPU réussi ; stabilité prolongée non démontrée.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Premier test fonctionnel GPU réussi ; stabilité prolongée non démontrée.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- __init__.py (référence locale historique non publiée)
- capture-noyau.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/capture-noyau.log`
- capture-udev.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/capture-udev.log`
- cuda-driver-resultat.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/cuda-driver-resultat.json`
- etat-final.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/etat-final.json`
- etat-initial.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/etat-initial.json`
- nvidia-smi-detail.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/nvidia-smi-detail.txt`
- nvidia-smi.csv (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/nvidia-smi.csv`
- pci-gpu.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/pci-gpu.txt`
- preparation.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/preparation.json`
- test-cuda-driver.py (référence locale historique non publiée)
- mission05C.md (référence locale historique non publiée)

## Références et dépendances

05C-P. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### mission05C.md (référence locale historique non publiée)

12 octobre 2026 — **SUCCÈS du premier test fonctionnel ; GO pour préparer une validation CUDA de calcul, puis Ollama.** La stabilité prolongée et sous charge n’est pas démontrée.

## Préparation et chronologie

Noyau actif `6.18.54-1-t2-trixie`, boot ID `[UUID EXPURGÉ]` inchangé. Avant branchement : Core absent de PCIe, i915 actif, GNOME PID 1270, SDDM et SSH actifs ; dix empreintes de modules conformes à 05B-A. Captures noyau/udev démarrées et inhibition temporaire sleep:idle effectivement vérifiée. Signal PRÊT envoyé ; tests effectués uniquement après confirmation explicite « c’est branché ».

- 18:00:04 : énumération du Core/GPU, chargement automatique de NVIDIA 595.91.07 par les mécanismes système.
- 18:00:06 : nvidia-drm initialisé.
- Vers 18:01 : nvidia-smi réussit et relève le firmware GSP.
- 18:01:28 : test CUDA Driver API réussi.

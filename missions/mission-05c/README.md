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

- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/jarvis/__init__.py)
- [capture-noyau.log](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/capture-noyau.log`
- [capture-udev.log](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/capture-udev.log`
- [cuda-driver-resultat.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/cuda-driver-resultat.json`
- [etat-final.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/etat-final.json`
- [etat-initial.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/etat-initial.json`
- [nvidia-smi-detail.txt](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/nvidia-smi-detail.txt`
- [nvidia-smi.csv](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/nvidia-smi.csv`
- [pci-gpu.txt](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/pci-gpu.txt`
- [preparation.json](../../archives/preuves-controlees/part-021.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/preparation.json`
- [test-cuda-driver.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C-preuves/test-cuda-driver.py)
- [mission05C.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C.md)

## Références et dépendances

05C-P. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [mission05C.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05C.md)

12 octobre 2026 — **SUCCÈS du premier test fonctionnel ; GO pour préparer une validation CUDA de calcul, puis Ollama.** La stabilité prolongée et sous charge n’est pas démontrée.

## Préparation et chronologie

Noyau actif `6.18.54-1-t2-trixie`, boot ID `d8f67bde-f785-4365-99ed-1af19afe9620` inchangé. Avant branchement : Core absent de PCIe, i915 actif, GNOME PID 1270, SDDM et SSH actifs ; dix empreintes de modules conformes à 05B-A. Captures noyau/udev démarrées et inhibition temporaire sleep:idle effectivement vérifiée. Signal PRÊT envoyé ; tests effectués uniquement après confirmation explicite « c’est branché ».

- 18:00:04 : énumération du Core/GPU, chargement automatique de NVIDIA 595.91.07 par les mécanismes système.
- 18:00:06 : nvidia-drm initialisé.
- Vers 18:01 : nvidia-smi réussit et relève le firmware GSP.
- 18:01:28 : test CUDA Driver API réussi.

# Inventaire TTS-01 — consolidation Codex

L’inventaire initial a été exécuté par JARVIS, puis contrôlé indépendamment. Les états sont datés : la sortie monoGPU initiale précède l’extension doubleGPU, elle n’est pas une photographie actuelle.

| Élément | État constaté / provenance |
| --- | --- |
| Dell1 | Precision5820, Corei9-10980XE, Debian13, noyau6.12.113+deb13-amd64 lors de l’inventaire initial |
| RAM | Environ251Gio utilisables (256Go installés), DDR4 ; les anciens libellés «251Go» sont corrigés |
| GPU | Deux RTX3090 Dell de24Gio chacune, extension mission13 conservée ; pas de réinstallation |
| Pilote | NVIDIA550.163.01 ; CUDA12.4 affiché par nvidia-smi est la compatibilité du pilote |
| Python TTS |3.13.5 dans `/opt/jarvis-lab/tts-01/venv` |
| PyTorch / torchaudio |2.6.0+cu124 ; calcul CUDA réel validé |
| Moteur |qwen-tts0.1.1 ; Transformers4.57.3, Accelerate1.12.0, SoundFile0.14.0 |
| Administration |SSH réel via profil épinglé `dell-observe` et droits persistants11B ; ce constat ne prétend pas refaire un test Tailscale/Ansible complet |
| Ollama |Service historique11434 conservé ; service missions11435 avec80B ;27B conversation conservé sur Mac |
| Projet isolé |`/opt/jarvis-lab/tts-01/`, seul périmètre d’écriture distant accordé à cette expérimentation |

Les versions de reprise ont été lues indépendamment le24octobre, après installation historique par JARVIS. `nvidia-ml-py` a ensuite été installé par JARVIS pour mesurer la charge CUDA ; les preuves d’appel donnent sa version exacte.

Les deux lignes «active» du rapport initial concernent exactement SSH et jarvis-ollama ; elles ne prouvent pas nvidia-persistenced. Aucun processus absent d’un extrait n’est supposé inexistant. Les hypothèses d’occupation mémoire du rapport initial restent des hypothèses.

Voir [original JARVIS](jarvis/INVENTAIRE_MATERIEL.md), [contrôle et réserves](VERIFICATION-INVENTAIRE.json), [inventaire doubleGPU](../13-extension-gpu/INVENTAIRE-OBSERVE.json). Les températures/charges sont des observations ponctuelles, pas une qualification électrique à700W ni une nouvelle réception de mission13.

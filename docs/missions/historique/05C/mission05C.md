> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission05C.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 05C : premier test Quadro RTX 5000

12 octobre 2026 — **SUCCÈS du premier test fonctionnel ; GO pour préparer une validation CUDA de calcul, puis Ollama.** La stabilité prolongée et sous charge n’est pas démontrée.

## Préparation et chronologie

Noyau actif `6.18.54-1-t2-trixie`, boot ID `[UUID EXPURGÉ]` inchangé. Avant branchement : Core absent de PCIe, i915 actif, GNOME PID 1270, SDDM et SSH actifs ; dix empreintes de modules conformes à 05B-A. Captures noyau/udev démarrées et inhibition temporaire sleep:idle effectivement vérifiée. Signal PRÊT envoyé ; tests effectués uniquement après confirmation explicite « c’est branché ».

- 18:00:04 : énumération du Core/GPU, chargement automatique de NVIDIA 595.91.07 par les mécanismes système.
- 18:00:06 : nvidia-drm initialisé.
- Vers 18:01 : nvidia-smi réussit et relève le firmware GSP.
- 18:01:28 : test CUDA Driver API réussi.
- 18:01:52 : vérification finale Intel/GNOME/SDDM/SSH réussie ; captures arrêtées et inhibition temporaire libérée, sans changement de configuration permanente.

Observation d’environ 1 min 48 après l’apparition du GPU. **La fenêtre de dix minutes proposée en 05B-A n’a pas été accomplie** : ce résultat est un premier succès fonctionnel court, conformément à la priorité d’avancer sur le fonctionnement concret. Une qualification prolongée reste à faire ; aucun GO production n’en découle.

## Résultats matériels et pilote

| Élément | Résultat |
|---|---|
| GPU | Quadro RTX 5000, TU104GL, PCI 10de:1eb0 |
| BDF | 0000:81:00.0 |
| Pilote lié | nvidia, version 595.91.07 |
| VRAM | 16 384 MiB |
| UUID | [UUID EXPURGÉ] |
| GSP Firmware Version | 595.91.07, rapporté par nvidia-smi |
| BAR0 | 0x90000000, 16 MiB |
| BAR1 | 0x4000000000, 256 MiB |
| BAR3 | 0x4010000000, 32 MiB |
| BAR5 | I/O 0x8000, 128 octets |
| PCIe lors du relevé | 2.5 GT/s, x4 ; pas de mesure de débit sous charge |

GSP n’est pas attesté par un message explicite du journal de probe ; sa version rapportée et le contexte CUDA fonctionnel constituent les preuves positives d’initialisation utilisées ici. Modules nvidia, nvidia_modeset et nvidia_drm autochargés ; CUDA peut également déclencher nvidia_uvm, état final conservé dans les preuves. Aucun modprobe manuel ni changement du rôle graphique Intel.

Intel reste lié à i915 en 00:02.0, card0 ; connecteur card0-DP-3 toujours connecté. GNOME conserve PID 1270 ; SDDM et SSH actifs, commandes exécutées avec succès après le test. NVIDIA indique Display Active: Disabled. Ces indices attestent le maintien technique de l’affichage Intel ; aucune nouvelle confirmation visuelle de l’utilisateur n’a été recueillie.

## Test CUDA léger, sans Toolkit

Script Python ctypes utilisant la bibliothèque déjà installée `libcuda.so.1`. Tous les appels retournent CUDA_SUCCESS (0) : cuInit, cuDriverGetVersion, cuDeviceGetCount, cuDeviceGet/Name, cuCtxCreate_v2, cuMemAlloc_v2, cuMemcpyHtoD_v2, cuMemcpyDtoH_v2, cuCtxSynchronize, cuMemFree_v2, cuCtxDestroy_v2.

Un GPU détecté ; API pilote 13020 (13.2). Allocation de 4096 octets, données déterministes transférées hôte→GPU→hôte et comparaison exacte réussie. Mémoire libérée et contexte détruit. **Aucun kernel de calcul lancé** : le test valide le contexte, l’allocation et les transferts, pas un calcul CUDA, une inférence ou une charge prolongée. CUDA Version dans nvidia-smi désigne la capacité du pilote, pas un Toolkit installé. Références : [gestion des contextes NVIDIA](https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__CTX.html), [gestion mémoire NVIDIA](https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__MEM.html).

## Anomalies et limites

- `module verification failed: signature and/or required key missing - tainting kernel` : le chargeur ne reconnaît pas la signature/clé ; le module a effectivement été accepté dans l’état actuel sans signature forcée. Aucune tentative d’enrôlement ou correction. Ne pas interpréter cela comme une signature cryptographiquement acceptée.
- Module externe : taint signalé. Les limites RETHUNK de 05B-A restent applicables ; ce test ne les corrige ni ne les invalide.
- `Cannot find any crtc or sizes` sur NVIDIA : constat compatible avec l’absence d’affichage NVIDIA actif ; i915 et son connecteur restent présents. Pas de correction graphique tentée.
- Aucun Xid, BUG/Oops/panic, alerte de thunk non patché, timeout GSP/RPC, AER fatal ou faute IOMMU retrouvé dans la capture du test. Absence limitée à cette fenêtre.

## Preuves et suite

mission05C-preuves (référence locale historique non publiée) contient état-initial.json, preparation.json, capture-noyau.log, capture-udev.log, pci-gpu.txt, nvidia-smi.csv, nvidia-smi-detail.txt, test-cuda-driver.py, cuda-driver-resultat.json, etat-final.json et journal-noyau-final.txt.

Recommandation : valider un petit kernel CUDA avec résultat vérifiable, puis une courte charge et observation prolongée avant installation contrôlée d’Ollama. Pas besoin d’installer un Toolkit complet pour le test API réalisé. Ollama n’a pas été installé ni lancé. Veille, retrait à chaud et démarrage Core connecté restent non qualifiés. Le Core reste branché ; inhibition de test levée, politiques habituelles de veille restaurées sans modification permanente.

Aucun redémarrage, reset, débranchement, rescan, écriture PCIe, changement GRUB/EFI/initramfs/mitigations, réinstallation ou correction improvisée. Seuls fichiers utilisateur créés, capture et inhibition temporaires, lectures et appels GPU autorisés réalisés.

> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS-Documentation/missions/mission-05b/README.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 05B

- Identifiant : 05B.
- Date ou période : 12 octobre 2026
- Objectif initial : JARVIS — Mission 05B : installation contrôlée NVIDIA
- Matériel mentionné : Razer Core
- Logiciels mentionnés : Debian / CUDA / NVIDIA / Ollama
- État final documentaire : **PARTIEL**. Installation DKMS réussie ; avertissements objtool et chargement GPU encore non qualifiés.

## Actions et résultats confirmés

Installation DKMS réussie ; avertissements objtool et chargement GPU encore non qualifiés.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Installation DKMS réussie ; avertissements objtool et chargement GPU encore non qualifiés.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- __init__.py (référence locale historique non publiée)
- initrd.img-6.18.54-1-t2-trixie-contenu.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357/initrd.img-6.18.54-1-t2-trixie-contenu.txt`
- proc_cmdline.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-[UUID EXPURGÉ]-20261011-225304/proc_cmdline.txt`
- SHA256SUMS (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/SHA256SUMS`
- apt-update.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/apt-update.log`
- avertissements-dkms-synthese.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/avertissements-dkms-synthese.txt`
- boot-hashes-final.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/boot-hashes-final.txt`
- boot-id-final.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/boot-id-final.txt`
- bootstrap-apt.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/bootstrap-apt.log`
- cloture-etat.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/cloture-etat.txt`
- compiler-initial.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/compiler-initial.txt`
- compte-nvidia-cree.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/compte-nvidia-cree.txt`
- dkms-cles-metadonnees.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/dkms-cles-metadonnees.txt`
- dkms-final.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/dkms-final.txt`
- dkms-logs-analyse.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/dkms-logs-analyse.json`
- dkms-make-0.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/dkms-make-0.txt`
- dkms-make-1.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/dkms-make-1.txt`
- espace-final.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/espace-final.txt`
- fichiers-persistants.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/fichiers-persistants.json`
- firmware-verification.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/firmware-verification.json`
- gnome-affichage-etat.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/gnome-affichage-etat.txt`
- gnome-initial.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/gnome-initial.txt`
- headers-initial.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/headers-initial.txt`
- initramfs-apres-liste.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/initramfs-apres-liste.txt`
- initramfs-comparaison.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/initramfs-comparaison.json`
- installation-complete.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/installation-complete.log`
- installation-resultat.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/installation-resultat.json`
- journal-noyau-depuis-installation.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/journal-noyau-depuis-installation.txt`
- ldconfig-cache.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/ldconfig-cache.txt`
- lockdown-initial.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/lockdown-initial.txt`
- logs-dkms-inventaire.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/logs-dkms-inventaire.txt`
- lsmod-final.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/lsmod-final.txt`
- mitigations-lecture.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/mitigations-lecture.txt`
- modinfo-6.12.111+deb13-amd64-nvidia.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modinfo-6.12.111+deb13-amd64-nvidia.txt`
- modinfo-6.12.111+deb13-amd64-nvidia_drm.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modinfo-6.12.111+deb13-amd64-nvidia_drm.txt`
- modinfo-6.12.111+deb13-amd64-nvidia_modeset.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modinfo-6.12.111+deb13-amd64-nvidia_modeset.txt`
- modinfo-6.12.111+deb13-amd64-nvidia_peermem.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modinfo-6.12.111+deb13-amd64-nvidia_peermem.txt`
- modinfo-6.12.111+deb13-amd64-nvidia_uvm.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modinfo-6.12.111+deb13-amd64-nvidia_uvm.txt`
- modinfo-6.18.54-1-t2-trixie-nvidia.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modinfo-6.18.54-1-t2-trixie-nvidia.txt`
- modinfo-6.18.54-1-t2-trixie-nvidia_drm.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modinfo-6.18.54-1-t2-trixie-nvidia_drm.txt`
- modinfo-6.18.54-1-t2-trixie-nvidia_modeset.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modinfo-6.18.54-1-t2-trixie-nvidia_modeset.txt`
- modinfo-6.18.54-1-t2-trixie-nvidia_peermem.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modinfo-6.18.54-1-t2-trixie-nvidia_peermem.txt`
- modinfo-6.18.54-1-t2-trixie-nvidia_uvm.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modinfo-6.18.54-1-t2-trixie-nvidia_uvm.txt`
- modules-verification.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/modules-verification.json`
- paquets-difference.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/paquets-difference.json`
- paquets-finaux.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/paquets-finaux.txt`
- pci-final.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/pci-final.txt`
- persistance-avant-fin.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/persistance-avant-fin.txt`
- persistance-configuration-finale.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/persistance-configuration-finale.json`
- phase2-validation.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/phase2-validation.json`
- phase3-preparation.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/phase3-preparation.json`
- politique-apt-reelle.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/politique-apt-reelle.txt`
- preflight.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/preflight.json`
- preparation-apt.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/preparation-apt.json`
- protection-persistance.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/protection-persistance.log`
- rollback-paquets-reels.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/rollback-paquets-reels.txt`
- rollback-versions-reelles.tsv (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/rollback-versions-reelles.tsv`
- sauvegarde-archive-inventaire.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/sauvegarde-archive-inventaire.txt`
- sauvegarde-empreintes.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/sauvegarde-empreintes.txt`
- sauvegarde-execution.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/sauvegarde-execution.txt`
- sauvegarde-validation.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/sauvegarde-validation.json`
- secureboot-initial.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/secureboot-initial.txt`
- services-final.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/services-final.txt`
- services-pids.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/services-pids.txt`
- session-finale.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/session-finale.txt`
- simulation-archives-locales.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/simulation-archives-locales.log`
- simulation-reelle-apt.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/simulation-reelle-apt.log`
- t2-verification.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/t2-verification.json`
- validation-complete.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-preuves/validation-complete.json`
- valider-installation.py (référence locale historique non publiée)
- boot-sha256.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-sauvegarde-20261012-171120/boot-sha256.txt`
- configuration-paths.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-sauvegarde-20261012-171120/configuration-paths.txt`
- manuels.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-sauvegarde-20261012-171120/manuels.txt`
- paquets.tsv (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-sauvegarde-20261012-171120/paquets.tsv`
- services-critiques.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-sauvegarde-20261012-171120/services-critiques.txt`
- services.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05B-sauvegarde-20261012-171120/services.txt`
- mission05B.md (référence locale historique non publiée)

## Références et dépendances

05B-P, 05B-S, 05C. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### mission05B.md (référence locale historique non publiée)

12 octobre 2026, Europe/Paris. Installation autorisée par l’utilisateur, exécutée dans le périmètre de mission05B-P.md. **Core absent pendant toute la mission ; aucun redémarrage/arrêt, aucune connexion/déconnexion, aucun chargement volontaire NVIDIA, aucun nvidia-smi/CUDA/Ollama, aucun rescan/écriture PCI/DEVEN, aucune modification GRUB/EFI/NVRAM ou du rôle Intel.**

## 1. Résultat et recommandation

**Installation terminée avec succès : NVIDIA 595.91.07-1, modules ouverts DKMS, composants de calcul.** APT retourne **0** ; dpkg cohérent ; **29 ajouts exacts au total, aucun paquet préexistant modifié ou supprimé**. DKMS est **installed** pour **6.12.111+deb13-amd64** et **6.18.54-1-t2-trixie**. Les cinq modules de chaque noyau sont présents, de version et vermagic corrects. Firmware GSP cohérent.

**JARVIS reste démarré et accessible en SSH, avec Intel i915 et GNOME Wayland actifs.** Le processus gnome-shell conserve son PID **1270**. SDDM et SSH sont actifs. `nvidia-persistenced` est **disabled / inactive, MainPID=0**, masque runtime retiré. Aucun module NVIDIA ni nouveau chargé, Core toujours absent de l’inventaire.

**Recommandation : NO-GO immédiat pour connecter le Razer Core.** Les contrôles structurels d’installation réussissent, mais les builds émettent **14 060 lignes warning par noyau**, dont **13 782 diagnostics objtool sur des retours « naked » dans un build MITIGATION_RETHUNK**. Ces avertissements ne sont pas des erreurs de compilation, mais leur portée sur le binaire exact et ses mitigations n’est pas qualifiée. Je recommande un audit en lecture seule avant d’autoriser le chargement/hotplug en Mission 05C. Ce choix de prudence ne démontre ni un crash futur ni une vulnérabilité exploitable sur JARVIS.


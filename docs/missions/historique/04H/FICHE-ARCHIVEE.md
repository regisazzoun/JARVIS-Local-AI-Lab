> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS-Documentation/missions/mission-04h/README.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 04H

- Identifiant : 04H.
- Date ou période : 11 octobre 2026
- Objectif initial : JARVIS — Mission 04H : validation de la réallocation PCIe
- Matériel mentionné : Mac mini / Quadro RTX 5000 / Razer Core
- Logiciels mentionnés : CUDA / NVIDIA
- État final documentaire : **ÉCHEC**. Réallocation inefficace : BAR1/BAR3 non attribués.

## Actions et résultats confirmés

Réallocation inefficace : BAR1/BAR3 non attribués.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Réallocation inefficace : BAR1/BAR3 non attribués.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- pci-0000_7f_00.0.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04E-preparation/preuves-20261011-205427/pci-0000_7f_00.0.txt`
- pci-0000_80_01.0.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04E-preparation/preuves-20261011-205427/pci-0000_80_01.0.txt`
- pci-0000_81_00.0.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04E-preparation/preuves-20261011-205427/pci-0000_81_00.0.txt`
- pci-arbre.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04E-preparation/preuves-20261011-205427/pci-arbre.txt`
- routes.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04E-preparation/preuves-20261011-205427/routes.txt`
- SHA256SUMS.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/SHA256SUMS.json`
- bolt-domaines.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/bolt-domaines.txt`
- bolt.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/bolt.log`
- bolt.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/bolt.txt`
- boot.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/boot.txt`
- connexions.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/connexions.txt`
- ecoutes.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/ecoutes.txt`
- erreurs-et-contextes.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/erreurs-et-contextes.log`
- gpu-identification.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/gpu-identification.txt`
- iomem.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/iomem.txt`
- modules.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/modules.txt`
- noyau.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/noyau.log`
- pci-0000_00_01.2.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/pci-0000_00_01.2.txt`
- pci-0000_7b_00.0.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/pci-0000_7b_00.0.txt`
- pci-0000_7c_01.0.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/pci-0000_7c_01.0.txt`
- pci-complet.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/pci-complet.txt`
- pilotes-et-gnome.log (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/pilotes-et-gnome.log`
- reseau.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/reseau.txt`
- resource-0000_81_00.0.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/resource-0000_81_00.0.txt`
- sysfs.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/20261011-211801/sysfs.json`
- dernier-dossier.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H-preuves/dernier-dossier.txt`
- mission04H.md (référence locale historique non publiée)

## Références et dépendances

04E, 04E-P, 04G-P, 04H-P. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### mission04H.md (référence locale historique non publiée)

**11 octobre 2026, collecte à 21:18 CEST. C — Réallocation inefficace dans cet essai : BAR 1 et BAR 3 non attribués, fenêtres insuffisantes.** Core détecté et autorisé ; la détection ne constitue pas une allocation réussie. Bureau réactif et conservation de la main confirmés par l’utilisateur.

Contrôles exclusivement en lecture seule. Seuls rapports et preuves écrits dans le dossier utilisateur ; aucun pilote installé, module NVIDIA chargé, CUDA, configuration modifiée, écriture PCIe, débranchement ou redémarrage.

## Conditions et accès hôte

Accès privilégié désormais fonctionnel : sudo -n id, lspci, journalctl, Bolt, iomem, systemctl et ss réussissent. Aucune preuve nécessaire au classement n’est bloquée par les restrictions de 04G.

Noyau `6.18.54-1-t2-trixie`, boot ID `[UUID EXPURGÉ]`. Ligne active :


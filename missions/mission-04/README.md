# Mission 04

- Identifiant : 04.
- Date ou période : 11 octobre 2026
- Objectif initial : JARVIS — Mission 04 : préparation du premier GPU NVIDIA
- Matériel mentionné : Quadro RTX 5000 / Razer Core
- Logiciels mentionnés : Debian / CUDA / NVIDIA
- État final documentaire : **NON VÉRIFIÉ**. Documents retrouvés ; réception finale non établie dans cette première passe.

## Actions et résultats confirmés

Documents retrouvés ; réception finale non établie dans cette première passe.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Documents retrouvés ; réception finale non établie dans cette première passe.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/jarvis/__init__.py)
- [Xorg.0.log.old](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/Xorg.0.log.old`
- [bolt-incident-complet.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/bolt-incident-complet.log`
- [boots-systeme.txt](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/boots-systeme.txt`
- [boots.txt](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/boots.txt`
- [coredumps-systeme.txt](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/coredumps-systeme.txt`
- [noyau-incident-complet.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/noyau-incident-complet.log`
- [pci-actuel.txt](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/pci-actuel.txt`
- [razer-bolt.txt](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/razer-bolt.txt`
- [reboots.txt](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/reboots.txt`
- [session-evenement.json](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/session-evenement.json`
- [session-incident.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/session-incident.log`
- [thunderbolt-actuel.txt](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-incident-preuves/thunderbolt-actuel.txt`
- [bolt-domaines.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-initial-20261011/bolt-domaines.log`
- [bolt.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-initial-20261011/bolt.log`
- [noyau.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-initial-20261011/noyau.log`
- [pci.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04-initial-20261011/pci.log`
- [mission04.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04.md)

## Références et dépendances

03, 04-I. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [mission04.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04.md)

Date : 11 octobre 2026, diagnostic initial à 18:38–18:40 CEST. Statut : étape 1 réalisée ; attente du signal utilisateur avant connexion du premier Razer Core. Aucun boîtier externe ou GPU NVIDIA détecté, aucune installation ni modification système exécutée.

## Périmètre

Diagnostic en lecture seule et recherches documentaires uniquement. Rapport et preuves créés dans le répertoire utilisateur. Réseau/SSH, noyaux, GRUB et EFI inchangés. Aucune autorisation Thunderbolt accordée, aucun paquet téléchargé/installé, aucun dépôt ajouté, aucun reboot. Les validations Wi-Fi/Bluetooth précédentes figurent dans mission03.md ; l’utilisateur confirme leur disponibilité.

## Thunderbolt, Bolt et PCIe

- Deux contrôleurs Intel JHL7540 Thunderbolt 3 NHI Titan Ridge : 07:00.0 et 7d:00.0, PCI 8086:15eb rev06, pilote thunderbolt actif. Ponts Titan Ridge 8086:15ea et contrôleurs USB 8086:15ec liés à pcieport/xhci_hcd ; ponts amont DSL6540 8086:1578.
- bolt 0.9.8, service actif (unité static ; ce n’est pas une absence d’activation). auth-mode=enabled ; force-power non supporté. Deux domaines domain0/domain1, sécurité user, bootacl 0/0. boltctl list vide ; sysfs ne contient que hôtes 0-0/1-0 et domaines, aucun boîtier externe.

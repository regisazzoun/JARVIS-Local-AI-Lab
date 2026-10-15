# Mission 04N

- Identifiant : 04N.
- Date ou période : 2026-10-11T22:46:12
- Objectif initial : Complément Mission 04N — Installation autorisée
- Matériel mentionné : Non documenté dans les rapports retenus.
- Logiciels mentionnés : Debian / NVIDIA
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

- [SHA256SUMS](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/22580014ef7e/mission04N-preparation/SHA256SUMS`
- [grubenv](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/boot/grub/grubenv`
- [grub](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/default/grub`
- [00_header](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/00_header`
- [05_debian_theme](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/05_debian_theme`
- [10_linux](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/10_linux`
- [20_linux_xen](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/20_linux_xen`
- [25_bli](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/25_bli`
- [30_os-prober](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/30_os-prober`
- [30_uefi-firmware](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/30_uefi-firmware`
- [35_fwupd](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/35_fwupd`
- [40_custom](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/40_custom`
- [41_custom](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/41_custom`
- [README](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/README`
- [42_jarvis_t2](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-proposition/42_jarvis_t2`
- [99-jarvis-t2.cfg](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-proposition/99-jarvis-t2.cfg`
- [43_jarvis_t2_egpu_diagnostic](../../archives/preuves-controlees/part-004.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04C-preparation/43_jarvis_t2_egpu_diagnostic`
- [44_jarvis_t2_egpu_reallocation](../../archives/preuves-controlees/part-004.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04E-preparation/44_jarvis_t2_egpu_reallocation`
- [05_debian_theme](../../archives/preuves-controlees/part-004.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04E-preparation/grub.d-test/05_debian_theme`
- [45_jarvis_t2_egpu_reserve_512m](../../archives/preuves-controlees/part-004.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/45_jarvis_t2_egpu_reserve_512m`
- [generer-isole.sh](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/installation-20261011-213406/generer-isole.sh)
- [System.map](../../archives/preuves-controlees/part-005.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/sources/System.map`
- [pci.c](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/sources/pci.c`
- [setup-bus.c](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/sources/setup-bus.c`
- [arbre.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04J-preuves/a5d47772-9fed-4f51-8d99-ffe75be725b1/arbre.json`
- [bolt-domaines.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/bolt-domaines.json`
- [bolt.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/bolt.json`
- [config-6.18.54-1-t2-trixie](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/config-6.18.54-1-t2-trixie`
- [dmi.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/dmi.json`
- [identite.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/identite.json`
- [noyau.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/noyau.json`
- [routes.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/routes.json`
- [stockage.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/stockage.json`
- [sys_class_dmi_id_product_name.txt](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/sys_class_dmi_id_product_name.txt`
- [46_jarvis_t2_egpu_reallocation_ciblee](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/46_jarvis_t2_egpu_reallocation_ciblee`
- [grub.cfg-genere](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/grub.cfg-genere`
- [verifier-reserve.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/verifier-reserve.py)
- [audit-complementaire.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04M-preuves/audit-complementaire.py)
- [audit-final.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04M-preuves/audit-final.json`
- [pci-sysfs.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04M-preuves/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-222715/pci-sysfs.json`
- [proc_cmdline.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04M-preuves/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-222715/proc_cmdline.txt`
- [sys_bus_pci_resource_alignment.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04M-preuves/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-222715/sys_bus_pci_resource_alignment.txt`
- [mission04N-preparation-initiale.tar.gz.sha256](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation-initiale.tar.gz.sha256`
- [mission04N-preparation.tar.gz.sha256](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation.tar.gz.sha256`
- [SHA256SUMS](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/SHA256SUMS`
- [bloc-experimental-non-installe.cfg](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/bloc-experimental-non-installe.cfg`
- [collecte-hote.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/collecte-hote.py)
- [comparaison-avertissements.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/comparaison-avertissements.json`
- [comparaison-candidat.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/comparaison-candidat.json`
- [compteurs-aer.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/compteurs-aer.json`
- [derniere-installation.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/derniere-installation.txt`
- [empreintes-protegees-apres.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/empreintes-protegees-apres.json`
- [empreintes-protegees-code.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/empreintes-protegees-code.py)
- [execution-collecte.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/execution-collecte.txt`
- [extraction-empreinte.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/extraction-empreinte.json`
- [SHA256SUMS](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/SHA256SUMS`
- [collecte.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/collecte.json`
- [connexions.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/connexions.json`
- [ecoutes.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/ecoutes.json`
- [journal-bolt.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/journal-bolt.json`
- [journal-noyau.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/journal-noyau.json`
- [journal-systeme.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/journal-systeme.json`
- [lectures.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/lectures.json`
- [montages.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/montages.json`
- [nvme-sante.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/nvme-sante.json`
- [pci-sysfs.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/pci-sysfs.json`
- [pci.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/pci.json`
- [proc_cmdline.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/proc_cmdline.txt`
- [proc_iomem.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/proc_iomem.txt`
- [proc_modules.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/proc_modules.txt`
- [proc_self_status.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/proc_self_status.txt`
- [processus.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/processus.json`
- [reseau.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/reseau.json`
- [services.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/services.json`
- [sessions.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/sessions.json`
- [SHA256SUMS](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225815/SHA256SUMS`
- [collecte.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225815/collecte.json`
- [connexions.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225815/connexions.json`
- [journal-noyau.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225815/journal-noyau.json`
- [lectures.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225815/lectures.json`
- [nvme-sante.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225815/nvme-sante.json`
- [proc_self_status.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225815/proc_self_status.txt`
- [processus.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225815/processus.json`
- [reseau.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225815/reseau.json`
- [sessions.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225815/sessions.json`
- [SHA256SUMS](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/SHA256SUMS`
- [arbre.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/arbre.json`
- [bolt.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/bolt.json`
- [collecte.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/collecte.json`
- [connexions.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/connexions.json`
- [journal-bolt.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/journal-bolt.json`
- [journal-noyau.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/journal-noyau.json`
- [lectures.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/lectures.json`
- [nvme-sante.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/nvme-sante.json`
- [pci-sysfs.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/pci-sysfs.json`
- [pci.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/pci.json`
- [proc_iomem.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/proc_iomem.txt`
- [proc_modules.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/proc_modules.txt`
- [proc_self_status.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/proc_self_status.txt`
- [processus.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/processus.json`
- [reseau.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230324/reseau.json`
- [SHA256SUMS](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230401/SHA256SUMS`
- [collecte.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230401/collecte.json`
- [connexions.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230401/connexions.json`
- [journal-noyau.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230401/journal-noyau.json`
- [lectures.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230401/lectures.json`
- [nvme-sante.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230401/nvme-sante.json`
- [proc_self_status.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230401/proc_self_status.txt`
- [processus.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230401/processus.json`
- [reseau.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-230401/reseau.json`
- [SHA256SUMS](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/SHA256SUMS`
- [collecte.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/collecte.json`
- [connexions.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/connexions.json`
- [ecoutes.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/ecoutes.json`
- [journal-bolt.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/journal-bolt.json`
- [journal-noyau.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/journal-noyau.json`
- [journal-systeme.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/journal-systeme.json`
- [lectures.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/lectures.json`
- [montages.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/montages.json`
- [nvme-sante.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/nvme-sante.json`
- [pci.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/pci.json`
- [proc_iomem.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/proc_iomem.txt`
- [proc_modules.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/proc_modules.txt`
- [proc_self_status.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/proc_self_status.txt`
- [processus.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/processus.json`
- [reseau.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/reseau.json`
- [services.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/services.json`
- [sessions.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/sessions.json`
- [SHA256SUMS](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/SHA256SUMS`
- [collecte.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/collecte.json`
- [connexions.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/connexions.json`
- [journal-noyau.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/journal-noyau.json`
- [journal-systeme.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/journal-systeme.json`
- [lectures.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/lectures.json`
- [nvme-sante.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/nvme-sante.json`
- [proc_self_status.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/proc_self_status.txt`
- [processus.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/processus.json`
- [reseau.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/reseau.json`
- [services.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-224634/services.json`
- [47_jarvis_t2_egpu_np32_pref512](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/47_jarvis_t2_egpu_np32_pref512`
- [boot-id-avant.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/boot-id-avant.txt`
- [diff-grub.patch](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/diff-grub.patch`
- [diff-theme-isolation.patch](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/diff-theme-isolation.patch`
- [empreintes-avant.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/empreintes-avant.json`
- [entree-candidate.cfg](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/entree-candidate.cfg`
- [grub.cfg-genere](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/grub.cfg-genere`
- [installation-resultat.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/installation-resultat.json`
- [installer.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/installer.py)
- [rapport-04N-avant-installation.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/rapport-04N-avant-installation.md)
- [retour-arriere.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/retour-arriere.py)
- [validation-candidat.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/validation-candidat.json`
- [verification-apres.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/verification-apres.json`
- [inventaire-core-historique.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/inventaire-core-historique.txt`
- [journal-extraits.log](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/journal-extraits.log`
- [journal-noyau-complet.log](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/journal-noyau-complet.log`
- [ligne-experimentale-grub.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/ligne-experimentale-grub.txt`
- [parser-disassembly.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/parser-disassembly.txt`
- [rapport-mission04N.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/rapport-mission04N.md)
- [size-bridges-disassembly.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/size-bridges-disassembly.txt`
- [size-mem-disassembly.txt](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/size-mem-disassembly.txt`
- [provenance.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/sources/provenance.json`
- [validation-np-actuelle.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/validation-np-actuelle.json`
- [validation-reserve.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/validation-reserve.json`
- [validation-syntaxe.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/validation-syntaxe.json`
- [verification-finale.json](../../archives/preuves-controlees/part-009.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/verification-finale.json`
- [verifier-np-pref.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/verifier-np-pref.py)

## Références et dépendances

04N-P. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [rapport-mission04N.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/rapport-mission04N.md)

**Prêt pour le redémarrage manuel sans Core. Installation terminée à 2026-10-11T22:46:12.325315+02:00. Aucun redémarrage exécuté ; candidat non testé.** Autorisation utilisateur : « oui poursuit et dit moi quand tu es pet a redemarer ».

Entrée à sélectionner : **JARVIS — T2 eGPU NP 32M + PREF 512M**, ID `jarvis-t2-egpu-np32-pref512`. Source `/etc/grub.d/47_jarvis_t2_egpu_np32_pref512`, root:root 0755 ; GRUB conserve root:root 0600. Modification des paramètres par rapport à 04M : ajout unique `pci=hpmmiosize=32M`. Noyau et initramfs inchangés ; aucun hpmemsize ajouté.

GRUB généré dans un espace de montage privé avec racine, /boot et /run en lecture seule, sources GRUB copiées, cache thème comparé, verrous et temporaires locaux. Diff vérifié : seul le nouveau bloc 47 apparaît. Syntaxe candidat et GRUB installé validée. Installation atomique et vérification des empreintes préalables. **31 autres fichiers protégés inchangés**, notamment noyaux/initramfs, sources GRUB antérieures, défauts et grubenv. Entrée 04M, diagnostic sans Nouveau et Debian 6.12.111/6.12.107 conservés. Menu visible 15 secondes en fonctionnement normal, défaut Debian 6.12.111 maintenu. Grubenv vide, aucun next_entry ni redémarrage programmé.

SHA-256 GRUB installé : `9bc2c064607d7daa3438da38e9f7808e71060aa6430c32af3decb3adbf5d7726` ; source 47 : `4f6104dbc649381003eb4018b5ad9d0cf663ec0a7ec4e512f04675519b627a16`. Sauvegardes et retour arrière limité à l'ajout 47 dans `installation-20261011-224539/`. Script retour-arriere.py préparé, non exécuté ; exige les empreintes attendues et conserve l'entrée 04M. Aucun retour arrière 04L exécuté.

Contrôles après installation : même boot `b88dab5b-c58b-49fb-85a1-9fd50b9e9716`, cmdline actuelle toujours celle de 04M sans hpmmiosize (normal avant reboot), Intel i915 primaire, SSD nvme0 live, racine montée rw, Ethernet UP/1000 Mbit/s et carrier=1, services SSH et SDDM actifs, Core disconnected, aucune NVIDIA ni Nouveau. Collecte après : `hote-b88dab5b-c58b-49fb-8

### [rapport-04N-avant-installation.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/installation-20261011-224539/rapport-04N-avant-installation.md)

**Avis : corriger uniquement la demande NP avec `pci=hpmmiosize=32M` est un premier essai pertinent, sous réserve d'autorisation. `pci=hpmemsize=32M` seul est inadapté à l'objectif de préserver une demande PREF de 512 Mio : il règle les deux classes de mémoire. Aucun candidat installé ou démarré. Core débranché.**

Les preuves privilégiées confirment la réussite PREF de 04M et l'insuffisance NP. Le boot actuel demeure `b88dab5b-c58b-49fb-85a1-9fd50b9e9716`, noyau `6.18.54-1-t2-trixie`. Il n'existe pas encore de résultat matériel pour le nouveau paramètre. L'étude n'autorise ni installation, ni redémarrage, ni branchement.

## 1. Preuves hôte et état de référence

`sudo -n id` retourne uid=0 ; les limitations de 04M sont levées pour cette mission. Collecte complète à 22:38:05 CEST dans `hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-223805/` : journaux noyau/système/Bolt, iomem non masqué, PCI détaillé, configurations brutes des ponts, sysfs, services, réseau, montages, SMART et ACPI. Le collecteur 04L a été vérifié par SHA-256 avant copie ; adaptations limitées au dossier de sortie 04N et au chemin absolu smartctl. Aucun outil système installé.

Ligne actuelle, inchangée :


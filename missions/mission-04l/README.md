# Mission 04L

- Identifiant : 04L.
- Date ou période : 11 octobre 2026, 2026-10-11T22:16:56
- Objectif initial : JARVIS — Mission 04L : préparation de la réallocation PCIe ciblée
- Matériel mentionné : Razer Core
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
- [SHA256SUMS](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ea7f03a147cd/mission04L-preparation/SHA256SUMS`
- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/jarvis/__init__.py)
- [42_jarvis_t2](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-proposition/42_jarvis_t2`
- [99-jarvis-t2.cfg](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-proposition/99-jarvis-t2.cfg`
- [43_jarvis_t2_egpu_diagnostic](../../archives/preuves-controlees/part-004.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04C-preparation/43_jarvis_t2_egpu_diagnostic`
- [44_jarvis_t2_egpu_reallocation](../../archives/preuves-controlees/part-004.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04E-preparation/44_jarvis_t2_egpu_reallocation`
- [05_debian_theme](../../archives/preuves-controlees/part-004.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04E-preparation/grub.d-test/05_debian_theme`
- [45_jarvis_t2_egpu_reserve_512m](../../archives/preuves-controlees/part-004.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/45_jarvis_t2_egpu_reserve_512m`
- [grub.cfg-candidat](../../archives/preuves-controlees/part-004.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/grub.cfg-candidat`
- [generer-isole.sh](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/installation-20261011-213406/generer-isole.sh)
- [System.map](../../archives/preuves-controlees/part-005.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/sources/System.map`
- [pci.c](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/sources/pci.c`
- [setup-bus.c](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/sources/setup-bus.c`
- [arbre.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04J-preuves/a5d47772-9fed-4f51-8d99-ffe75be725b1/arbre.json`
- [boot-id-fin.txt](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04J-preuves/a5d47772-9fed-4f51-8d99-ffe75be725b1/boot-id-fin.txt`
- [bolt-domaines.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/bolt-domaines.json`
- [bolt.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/bolt.json`
- [config-6.18.54-1-t2-trixie](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/config-6.18.54-1-t2-trixie`
- [dmi.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/dmi.json`
- [ecoutes.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/ecoutes.json`
- [identite.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/identite.json`
- [journal-bolt.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/journal-bolt.json`
- [montages.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/montages.json`
- [noyau.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/noyau.json`
- [pci-sysfs.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/pci-sysfs.json`
- [pci.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/pci.json`
- [proc_cmdline.txt](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/proc_cmdline.txt`
- [proc_iomem.txt](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/proc_iomem.txt`
- [proc_modules.txt](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/proc_modules.txt`
- [routes.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/routes.json`
- [sessions.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/sessions.json`
- [stockage.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/stockage.json`
- [sys_class_dmi_id_product_name.txt](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/sys_class_dmi_id_product_name.txt`
- [mission04L-preparation-initiale.tar.gz.sha256](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation-initiale.tar.gz.sha256`
- [mission04L-preparation.tar.gz.sha256](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation.tar.gz.sha256`
- [SHA256SUMS](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/SHA256SUMS`
- [acpi-DSDT.dsl](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/acpi-DSDT.dsl`
- [desassemblage.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/desassemblage.json`
- [acpi-DSDT-desassemblage.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-DSDT-desassemblage.json`
- [acpi-DSDT.dsl](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-DSDT.dsl`
- [acpi-SSDT1-desassemblage.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT1-desassemblage.json`
- [acpi-SSDT1.dsl](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT1.dsl`
- [acpi-SSDT10-desassemblage.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT10-desassemblage.json`
- [acpi-SSDT10.dsl](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT10.dsl`
- [acpi-SSDT11-desassemblage.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT11-desassemblage.json`
- [acpi-SSDT11.dsl](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT11.dsl`
- [acpi-SSDT12-desassemblage.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT12-desassemblage.json`
- [acpi-SSDT12.dsl](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT12.dsl`
- [acpi-SSDT2-desassemblage.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT2-desassemblage.json`
- [acpi-SSDT2.dsl](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT2.dsl`
- [acpi-SSDT3-desassemblage.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT3-desassemblage.json`
- [acpi-SSDT3.dsl](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT3.dsl`
- [acpi-SSDT4-desassemblage.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT4-desassemblage.json`
- [acpi-SSDT4.dsl](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT4.dsl`
- [acpi-SSDT5-desassemblage.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT5-desassemblage.json`
- [acpi-SSDT5.dsl](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT5.dsl`
- [acpi-SSDT6-desassemblage.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT6-desassemblage.json`
- [acpi-SSDT6.dsl](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT6.dsl`
- [acpi-SSDT7-desassemblage.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT7-desassemblage.json`
- [acpi-SSDT7.dsl](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT7.dsl`
- [acpi-SSDT8-desassemblage.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT8-desassemblage.json`
- [acpi-SSDT8.dsl](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT8.dsl`
- [acpi-SSDT9-desassemblage.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT9-desassemblage.json`
- [acpi-SSDT9.dsl](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/acpi/individuel/acpi-SSDT9.dsl`
- [bloc-grub-verification.cfg](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/bloc-grub-verification.cfg`
- [boots-disponibles.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/boots-disponibles.txt`
- [collecte-hote.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/collecte-hote.py)
- [derniere-installation.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/derniere-installation.txt`
- [empreintes-systeme-avant.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/empreintes-systeme-avant.json`
- [SHA256SUMS](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-220256/SHA256SUMS`
- [collecte.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-220256/collecte.json`
- [connexions.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-220256/connexions.json`
- [journal-noyau.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-220256/journal-noyau.json`
- [lectures.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-220256/lectures.json`
- [nvme-sante.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-220256/nvme-sante.json`
- [proc_self_status.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-220256/proc_self_status.txt`
- [processus.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-220256/processus.json`
- [reseau.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-220256/reseau.json`
- [SHA256SUMS](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-221729/SHA256SUMS`
- [collecte.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-221729/collecte.json`
- [connexions.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-221729/connexions.json`
- [journal-noyau.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-221729/journal-noyau.json`
- [lectures.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-221729/lectures.json`
- [nvme-sante.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-221729/nvme-sante.json`
- [proc_self_status.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-221729/proc_self_status.txt`
- [processus.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-221729/processus.json`
- [reseau.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-221729/reseau.json`
- [46_jarvis_t2_egpu_reallocation_ciblee](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/46_jarvis_t2_egpu_reallocation_ciblee`
- [diff-grub.patch](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/diff-grub.patch`
- [empreintes-avant.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/empreintes-avant.json`
- [entree-candidate.cfg](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/entree-candidate.cfg`
- [generation-meta.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/generation-meta.json`
- [grub.cfg-genere](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/grub.cfg-genere`
- [installation-resultat.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/installation-resultat.json`
- [installer.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/installer.py)
- [rapport-04L-avant-installation.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/rapport-04L-avant-installation.md)
- [retour-arriere.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/retour-arriere.py)
- [System.map-6.12.107+deb13-amd64](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/sauvegarde/boot/System.map-6.12.107+deb13-amd64`
- [config-6.12.107+deb13-amd64](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/sauvegarde/boot/config-6.12.107+deb13-amd64`
- [config-6.12.111+deb13-amd64](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/sauvegarde/boot/config-6.12.111+deb13-amd64`
- [validation-apres.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/validation-apres.json`
- [validation-candidat.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/validation-candidat.json`
- [verification-finale.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/verification-finale.json`
- [integrite-fin.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/integrite-fin.json`
- [journal-allocation-extraits.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/journal-allocation-extraits.txt`
- [journal-erreurs-contexte.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/journal-erreurs-contexte.txt`
- [ligne-grub-temporaire.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/ligne-grub-temporaire.txt`
- [README](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/outils/extrait/usr/share/doc/acpica-tools/README`
- [README.Debian](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/outils/extrait/usr/share/doc/acpica-tools/README.Debian`
- [copyright](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/outils/extrait/usr/share/doc/acpica-tools/copyright`
- [rapport-mission04L.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/rapport-mission04L.md)
- [ressources-protegees.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/ressources-protegees.json`
- [secours-preuves.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/secours-preuves.json`
- [chaines-parser.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/chaines-parser.json`
- [extraction.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/extraction.json`
- [pci_dev_str_match-disassembly-annote.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_dev_str_match-disassembly-annote.txt`
- [pci_dev_str_match-disassembly.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_dev_str_match-disassembly.txt`
- [pci_device_add-disassembly-annote.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_device_add-disassembly-annote.txt`
- [pci_device_add-disassembly.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_device_add-disassembly.txt`
- [pci_disable_bridge_window-disassembly-annote.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_disable_bridge_window-disassembly-annote.txt`
- [pci_disable_bridge_window-disassembly.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_disable_bridge_window-disassembly.txt`
- [pci_reassigndev_resource_alignment-disassembly-annote.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_reassigndev_resource_alignment-disassembly-annote.txt`
- [pci_reassigndev_resource_alignment-disassembly.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_reassigndev_resource_alignment-disassembly.txt`
- [pci_reassigndev_resource_alignment.cold-disassembly-annote.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_reassigndev_resource_alignment.cold-disassembly-annote.txt`
- [pci_reassigndev_resource_alignment.cold-disassembly.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_reassigndev_resource_alignment.cold-disassembly.txt`
- [pci_setup-disassembly-annote.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_setup-disassembly-annote.txt`
- [pci_setup-disassembly.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_setup-disassembly.txt`
- [pci_setup_device-disassembly-annote.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_setup_device-disassembly-annote.txt`
- [pci_setup_device-disassembly.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pci_setup_device-disassembly.txt`
- [pcibios_default_alignment-disassembly-annote.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pcibios_default_alignment-disassembly-annote.txt`
- [pcibios_default_alignment-disassembly.txt](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/pcibios_default_alignment-disassembly.txt`
- [probe.c](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/sources/probe.c`
- [syntaxe-grub.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/syntaxe-grub.json`
- [validation-reserve-actuelle.json](../../archives/preuves-controlees/part-007.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/validation-reserve-actuelle.json`
- [verifier-reserve.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/verifier-reserve.py)

## Références et dépendances

04K, 04L-P. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [rapport-mission04L.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/rapport-mission04L.md)

## Complément — Installation autorisée avant redémarrage

**Installation terminée et vérifiée à 2026-10-11T22:16:56.454294+02:00. Autorisation reçue : « procede au modification du kernel et du grub et tt autre fichier avant redemarrage et test ». Aucun redémarrage ni test matériel effectué.** Ce complément décrit l’état actuel ; l’étude conservée plus bas décrit la préparation antérieure à l’installation.

### Modification installée

Nouvelle entrée : **JARVIS — T2 eGPU réallocation ciblée PCIe**, ID `jarvis-t2-egpu-reallocation-ciblee`. Source `/etc/grub.d/46_jarvis_t2_egpu_reallocation_ciblee`, root:root 0755. `/boot/grub/grub.cfg` mis à jour avec un ajout strictement limité au bloc 46, mode root:root 0600 conservé.

Le noyau déjà installé prend en charge le mécanisme : la modification porte sur les paramètres de son démarrage. Image `6.18.54-1-t2-trixie` et son initramfs inchangés ; aucun patch ou recompilation requis, aucun initramfs régénéré. La nouvelle entrée contient :


### [rapport-04L-avant-installation.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04L-preparation/installation-20261011-221528/rapport-04L-avant-installation.md)

**11 octobre 2026 — Préparation terminée, paramètre reconnu dans le noyau installé ; essai non appliqué et non autorisé.** La ligne temporaire est prête et sa syntaxe GRUB vérifiée sur une copie locale. La possibilité d’une allocation haute est réelle du point de vue des apertures et des types des trois ponts, mais son succès demeure incertain : les fenêtres des descendants non ciblés, notamment 7c:04.0, peuvent empêcher le déplacement des parents. Aucun branchement du Core n’est admissible sur les fenêtres actuelles.

## 1. Périmètre, accès et preuves

Mission 04K reprise, puis nouvelle collecte privilégiée à **22:02:56 CEST**. `sudo -n` réussit avec uid=0, sans contournement de l’environnement. Noyau actif `6.18.54-1-t2-trixie`, boot ID `a5d47772-9fed-4f51-8d99-ffe75be725b1`, inchangé. ACPI, journaux noyau/système/Bolt, iomem, sysfs PCI et configuration brute accessibles. Les limites d’accès qui affectaient la première étude 04K ne s’appliquent donc plus à cette collecte.

Dossier : mission04L-preparation (référence dans l’original : `mission04L-preparation/`). Capture hôte : `hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-220256/`. Commandes, sorties, erreurs et codes conservés. Une copie du collecteur et un analyseur hors ligne permettent la comparaison au futur boot.

Aucun changement GRUB, EFI, ACPI, VFIO, i915 ou réglage noyau ; aucun module chargé par la mission, aucune écriture de configuration PCI, aucun retrait/rescan, branchement ou redémarrage. Seuls les rapports, copies et outils d’analyse sont écrits dans le dossier utilisateur. `iasl` absent du système : paquet Debian téléchargé puis **extrait localement**, sans installation ni modification de la base des paquets. Son désassembleur travaille sur des copies de tables ; aucune méthode ACPI n’est invoquée à nouveau sur le matériel.


# Mission 04P

- Identifiant : 04P.
- Date ou période : 11 octobre 2026
- Objectif initial : JARVIS — Mission 04H : validation de la réallocation PCIe
- Matériel mentionné : Mac mini / Quadro RTX 5000 / Razer Core
- Logiciels mentionnés : T2Linux / CUDA / NVIDIA
- État final documentaire : **PARTIEL**. Allocation PCIe Quadro réussie ; pilote et calcul non validés à cette étape.

## Actions et résultats confirmés

Allocation PCIe Quadro réussie ; pilote et calcul non validés à cette étape.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Allocation PCIe Quadro réussie ; pilote et calcul non validés à cette étape.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [04E-extraits.txt](../../archives/preuves-controlees/part-004.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04G-preuves/collecte-restreinte-20261011/04E-extraits.txt`
- [mission04H.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H.md)
- [System.map](../../archives/preuves-controlees/part-005.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04I-preparation/sources/System.map`
- [bolt-domaines.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/bolt-domaines.json`
- [config-6.18.54-1-t2-trixie](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/config-6.18.54-1-t2-trixie`
- [dmi.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/dmi.json`
- [identite.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/identite.json`
- [noyau.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/noyau.json`
- [routes.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/routes.json`
- [stockage.json](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/stockage.json`
- [sys_class_dmi_id_product_name.txt](../../archives/preuves-controlees/part-006.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637/sys_class_dmi_id_product_name.txt`
- [sys_bus_pci_resource_alignment.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04M-preuves/hote-b88dab5b-c58b-49fb-85a1-9fd50b9e9716-20261011-222715/sys_bus_pci_resource_alignment.txt`
- [ecoutes.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/ecoutes.json`
- [montages.json](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/montages.json`
- [proc_cmdline.txt](../../archives/preuves-controlees/part-008.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04N-preparation/hote-b70d6ac9-b00b-4a16-b60f-ba2dcd09b376-20261011-225304/proc_cmdline.txt`
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
- [rapport-mission04O.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04O-preuves/rapport-mission04O.md)
- [mission04P-preuves.tar.gz.sha256](../../archives/preuves-controlees/part-010.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves.tar.gz.sha256`
- [SHA256SUMS](../../archives/preuves-controlees/part-010.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves/SHA256SUMS`
- [aer-initial.json](../../archives/preuves-controlees/part-010.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves/aer-initial.json`
- [audit-global.json](../../archives/preuves-controlees/part-010.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves/audit-global.json`
- [comparaison-04O.json](../../archives/preuves-controlees/part-010.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves/comparaison-04O.json`
- [gpu-config.json](../../archives/preuves-controlees/part-010.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves/gpu-config.json`
- [journal-delta-final.json](../../archives/preuves-controlees/part-010.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves/journal-delta-final.json`
- [journal-depuis-04O.txt](../../archives/preuves-controlees/part-010.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves/journal-depuis-04O.txt`
- [rapport-mission04P.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves/rapport-mission04P.md)
- [validation-BAR.json](../../archives/preuves-controlees/part-010.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves/validation-BAR.json`

## Références et dépendances

04E, 04E-P, 04G-P, 04H, 04H-P, 04O. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [mission04H.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04H.md)

**11 octobre 2026, collecte à 21:18 CEST. C — Réallocation inefficace dans cet essai : BAR 1 et BAR 3 non attribués, fenêtres insuffisantes.** Core détecté et autorisé ; la détection ne constitue pas une allocation réussie. Bureau réactif et conservation de la main confirmés par l’utilisateur.

Contrôles exclusivement en lecture seule. Seuls rapports et preuves écrits dans le dossier utilisateur ; aucun pilote installé, module NVIDIA chargé, CUDA, configuration modifiée, écriture PCIe, débranchement ou redémarrage.

## Conditions et accès hôte

Accès privilégié désormais fonctionnel : sudo -n id, lspci, journalctl, Bolt, iomem, systemctl et ss réussissent. Aucune preuve nécessaire au classement n’est bloquée par les restrictions de 04G.

Noyau `6.18.54-1-t2-trixie`, boot ID `565560bb-80ac-424b-8bc3-101e7441b335`. Ligne active :


### [rapport-mission04P.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04P-preuves/rapport-mission04P.md)

**Attribution PCIe réussie pour la Quadro RTX 5000 et ses fonctions associées. Aucun indice de régression critique dans les captures ; réserves hotplug internes partiellement refusées et indicateurs GPU à surveiller.** Le GPU n'est pas validé en fonctionnement : aucun pilote graphique lié, COMMAND=0, Mem−/I/O−/BusMaster−. Aucun paramètre modifié, pilote chargé par cette mission, rescan, écriture PCIe, redémarrage ou débranchement. Les pilotes génériques audio/USB ont été liés automatiquement par le système au hotplug.

## Identité et chaîne

Boot `b70d6ac9-b00b-4a16-b60f-ba2dcd09b376`, identique à 04O, noyau `6.18.54-1-t2-trixie`, cmdline complète inchangée :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```


### [rapport-mission04O.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04O-preuves/rapport-mission04O.md)

**Conclusion A — NP et PREF utilisables pour les besoins historiques connus ; essai eGPU envisageable uniquement après accord distinct.** Aucun branchement, pilote NVIDIA, modification GRUB, écriture PCIe ou redémarrage effectué. Les seules écritures sont les preuves et rapports utilisateur.

## Boot et méthode

Nouveau boot `b70d6ac9-b00b-4a16-b60f-ba2dcd09b376`, distinct de 04M/04N `b88dab5b-c58b-49fb-85a1-9fd50b9e9716`. Noyau T2Linux `6.18.54-1-t2-trixie`. Cmdline complète :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```


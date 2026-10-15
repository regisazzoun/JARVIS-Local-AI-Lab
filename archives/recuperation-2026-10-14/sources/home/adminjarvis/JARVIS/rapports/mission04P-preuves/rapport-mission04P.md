# JARVIS — Mission 04P

**Attribution PCIe réussie pour la Quadro RTX 5000 et ses fonctions associées. Aucun indice de régression critique dans les captures ; réserves hotplug internes partiellement refusées et indicateurs GPU à surveiller.** Le GPU n'est pas validé en fonctionnement : aucun pilote graphique lié, COMMAND=0, Mem−/I/O−/BusMaster−. Aucun paramètre modifié, pilote chargé par cette mission, rescan, écriture PCIe, redémarrage ou débranchement. Les pilotes génériques audio/USB ont été liés automatiquement par le système au hotplug.

## Identité et chaîne

Boot `b70d6ac9-b00b-4a16-b60f-ba2dcd09b376`, identique à 04O, noyau `6.18.54-1-t2-trixie`, cmdline complète inchangée :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```

Identification dynamique vendor/device **10de:1eb0**, résultat unique **0000:81:00.0**, TU104GL Quadro RTX 5000, boot_vga=0. Chaîne depuis sysfs :

`pci0000:00 → 0000:00:01.2 → 0000:7b:00.0 → 0000:7c:01.0 → 0000:7f:00.0 → 0000:80:01.0 → 0000:81:00.0`.

NHI hôte 7d:00.0 sous 7c:00.0, thunderbolt lié ; port cible 7c:01.0. Core : pont amont 7f:00.0 DSL6540, branche GPU 80:01.0 et branche USB sœur 80:04.0 → 82:00.0. Fonctions GPU 81:00.1 audio, .2 USB NVIDIA, .3 UCSI. Bolt Core authorized. Journal hôte date le branchement à 23:02:22 CEST ; boltctl affiche 21:02:22 pour le même événement (présentation horaire différente), ne pas interpréter comme second branchement. Thunderbolt RX/TX 20 Gb/s rapportés ; lien local GPU 8 GT/s ×4, pont Thunderbolt 2,5 GT/s ×4. Aucune mesure de débit réel.

## BAR et couverture

| BAR | Attribution inclusive | Taille et classe | Alignement / cinq parents |
|---|---|---|---|
| BAR0 | 90000000–90ffffff | 16 Mio NP 32 bits | correct / tous couverts |
| BAR1 | 4000000000–400fffffff | 256 Mio PREF64 | correct / tous couverts |
| BAR3 | 4010000000–4011ffffff | 32 Mio PREF64 | correct / tous couverts |

Les trois registres BAR lus sur 64 octets concordent avec sysfs ; tailles confirmées par Resizable BAR et journal. Attribution dans iomem. Validation exhaustive de chaque BAR contre les cinq fenêtres correspondantes dans validation-BAR.json. Apertures hôte basse 80000000–feafffff et haute 4000000000–7fffffffff couvrent ces ressources. Le décodage GPU désactivé sans pilote ne remet pas en cause l'attribution, mais interdit d'en déduire un accès GPU opérationnel.

BAR5 I/O 8000–807f, ROM attribuée 91000000–9107ffff, non activée par la mission. Audio 91080000–91083fff, snd_hda_intel lié ; UCSI 91084000–91084fff sans pilote lié ; USB NVIDIA BAR0 4012000000–401203ffff et BAR3 4012040000–401204ffff, xhci_hcd lié ; USB Core 91100000–9110ffff, xhci_hcd lié. Ces BAR connus sont attribués et couverts ; pas d'affirmation de fonctionnement UCSI. Tous les ponts liés à pcieport, décodage mémoire et I/O actifs.

## Fenêtres finales

| Pont | NP | PREF | I/O |
|---|---|---|---|
| 0000:00:01.2 | `8fa00000–93bfffff` (66 Mio) | `4000000000–403fffffff` (1024 Mio) | `8000–bfff` |
| 0000:7b:00.0 | `8fa00000–93bfffff` (66 Mio) | `4000000000–403fffffff` (1024 Mio) | `8000–bfff` |
| 0000:7c:01.0 | `8fb00000–91afffff` (32 Mio) | `4000000000–401fffffff` (512 Mio) | `8000–9fff` |
| 0000:7f:00.0 | `90000000–911fffff` (18 Mio) | `4000000000–40121fffff` (290 Mio) | `8000–9fff` |
| 0000:80:01.0 | `90000000–910fffff` (17 Mio) | `4000000000–40120fffff` (289 Mio) | `8000–8fff` |
| 0000:80:04.0 | `91100000–911fffff` (1 Mio) | `4012100000–40121fffff` (1 Mio) | `9000–9fff` |

Sysfs et configurations brutes des ponts archivés. Audit global : 129 inclusions mémoire vers tous les ancêtres, aucun échec ni collision entre allocations de même niveau. Fenêtres mémoire à granularité 1 Mio ; I/O à granularité 4 Kio. I/O GPU couvert par toute la chaîne.

## Allocation et erreurs

Le journal montre une première demande de 7f:00.0 : NP **49 Mio** (0x03100000), PREF **802 Mio** (0x32200000), refusée faute de place. Le noyau retombe sur les fenêtres **18 Mio NP / 290 Mio PREF**, puis attribue tous les BAR connus. Extensions optionnelles refusées : +31 Mio NP et +512 Mio PREF sur le pont amont Core, +31 Mio NP sur 80:04.0, dont la fenêtre finale reste 1 Mio. Les messages no space/failed to assign existent donc réellement ; ils concernent ces demandes de fenêtres élargies et ne sont pas des échecs finaux des BAR1/BAR3. Les attributions finales et l'ordre du journal constituent la preuve de résolution pour les ressources obligatoires. Les réserves optionnelles complètes ne sont pas disponibles.

Aucune erreur d'allocation finale des BAR GPU, faute IOMMU/DMAR, événement AER fatal/nonfatal rapporté, déclenchement DPC, timeout/reset NVMe ou GPU hang i915 relevé. Compteurs AER sysfs disponibles à zéro (aer-initial.json). **Réserve diagnostique : GPU DevSta CorrErr+ et UnsupReq+, CESta AdvNonFatalErr+ masqué ; UESta sans bit actif, LaneErrStat=0.** Bits de statut persistants, non horodatés : leur cause et leur instant ne peuvent être établis par cette lecture. Ils ne justifient pas un certificat d'absence absolue d'erreurs PCIe ; aucun effacement ou test supplémentaire effectué. Ponts Core : états corr/nonfatal/fatal/UnsupReq négatifs dans la capture.

Thunderbolt : DROM revision inconnue, CRC32 mismatch continuing, entrées supplémentaires ignorées, signatures déjà présentes en 04H. bridge configuration invalid bus 00-00 est suivi de reconfiguring et d'une numérotation finale valide. Avertissements ACPI/LPSS et eDP du boot sont ceux de 04O. tg3 VPD access failed est réémis lors des lectures lspci, signature historique, sans perte Ethernet constatée.

## Système et stabilité

Intel 00:02.0 i915 lié, boot_vga=1, DP-3 connected/enabled, SDDM actif. Le journal vgaarb modifie les décodages legacy à l'arrivée du GPU ; BAR Intel et sortie active restent conservés. Réactivité humaine après branchement non confirmée séparément dans cette mission ; utilisateur indique surveillance graphique et SSH depuis un Mac indépendant.

SSD nvme0 live, partitions EFI /boot et LVM présentes, racine ext4 rw. SMART PASSED, Critical Warning=0, erreurs média et compteur d'erreurs=0, température 34 °C ; code smartctl=4 dû à la limitation historique Invalid Log Page 0x109. Ethernet hôte enp4s0 UP, carrier=1, 1000 Mbit/s, IP 192.168.1.99/24, routes conservées ; services/socket SSH actifs et connexions depuis 192.168.1.63 présentes. Nouvelle interface Ethernet USB Core détectée, sans présumer liaison réseau opérationnelle.

Captures 2026-10-11T23:03:25.179983+02:00 et 2026-10-11T23:04:02.078525+02:00, intervalle **36.899 secondes**. PCI-sysfs complet identique entre captures : **True**. Même boot, ressources et pilotes stables. Aucun nouveau message noyau entre ces captures hormis tg3 VPD pendant la deuxième collecte. Observation ponctuelle au repos, sans test de charge GPU ni garantie de stabilité prolongée.

## Comparaison

| Contrôle | 04E / 04H | 04O sans Core | 04P Core connecté |
|---|---|---|---|
| BAR0 | attribué 16 Mio | placement prévu 90000000 | attribué à cette adresse |
| BAR1 / BAR3 | non attribués, no space | placements prévus PREF haute | attribués aux plages prévues |
| PREF parents / cible | 224 / 112 Mio | 1024 / 512 Mio | inchangée par hotplug |
| PREF Core amont / GPU | 100 Mio / absente en 04H | ponts absents | 290 / 289 Mio |
| NP parents / cible | 226 / 112 Mio en 04H | 66 / 32 Mio | inchangée par hotplug |
| Réserves internes | allocation graphique bloquée | limite anticipée ≈49 Mio NP et >512 PREF | extensions refusées, BAR obligatoires réussis |

Référence 04E archivée sous forme d'extraits du journal, complétée par le tableau historique du rapport 04H ; aucune prétention de collecte actuelle 04E. Les ressources et pilotes des périphériques préexistants de 04O sont conservés (voir comparaison-04O.json). La prédiction arithmétique 04O est confirmée pour les BAR, et sa limite concernant les réserves internes est observée réellement.

## Preuves et suite

Accès privilégié disponible, aucune commande de secours SSH nécessaire. Collecteur 04N relu et vérifié par SHA-256 c6b449d5cdbb424bbb6e3c952f9127a2663a7dffb49d983ab353c18e50a1f660 avant exécution, copie 04O utilisée sans changement. Dossiers originaux produits dans 04N-preparation puis copiés intégralement ici. Journaux complets système/noyau/Bolt, PCI complet, arbre, configs ponts/GPU, sysfs, iomem, ACPI, SMART, services/réseau et erreurs de commandes conservés. Rapport et manifeste SHA-256 inclus dans archive.

**Validation des ressources PCIe réussie ; fonctionnement Quadro avec pilote et stabilité en charge non testés. Réserves optionnelles partiellement refusées ; statuts GPU à surveiller lors d'une mission distincte. Attente de votre accord avant toute nouvelle intervention. Core laissé connecté.**

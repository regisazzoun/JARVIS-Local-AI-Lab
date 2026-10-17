> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission04O.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 04O

**Conclusion A — NP et PREF utilisables pour les besoins historiques connus ; essai eGPU envisageable uniquement après accord distinct.** Aucun branchement, pilote NVIDIA, modification GRUB, écriture PCIe ou redémarrage effectué. Les seules écritures sont les preuves et rapports utilisateur.

## Boot et méthode

Nouveau boot `[UUID EXPURGÉ]`, distinct de 04M/04N `[UUID EXPURGÉ]`. Noyau T2Linux `6.18.54-1-t2-trixie`. Cmdline complète :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```

Tous les paramètres attendus présents, y compris les trois BDF resource_alignment ; sysfs concordant. Accès hôte sudo non interactif uid=0 disponible. Les quatre outils 04N ont été lus et leurs empreintes vérifiées contre SHA256SUMS avant exécution ; copies exactes et manifeste dans outils/. Collecteur original exécuté sans modification : il produit ses dossiers dans 04N-preparation, recopiés intégralement ici sous initial/ et final/. Analyseurs hors ligne exécutés sur les deux collectes. Journaux complets, ressources de tous les périphériques PCI, configurations 64 octets des ponts, iomem non masqué, tables ACPI, stockage, SMART, réseau et services archivés avec codes et erreurs.

## Avant / après

| Pont | NP 04M/04N | NP 04O | PREF 04M/04N → 04O |
|---|---:|---|---|
| 0000:00:01.2 | 6 Mio | 8fa00000–93bfffff, 66 Mio | 4000000000–403fffffff, 1024 Mio inchangés |
| 0000:7b:00.0 | 6 Mio | 8fa00000–93bfffff, 66 Mio | 4000000000–403fffffff, 1024 Mio inchangés |
| 0000:7c:01.0 | 2 Mio | 8fb00000–91afffff, 32 Mio | 4000000000–401fffffff, 512 Mio inchangés |
| 0000:7c:04.0 | 2 Mio | 91c00000–93bfffff, 32 Mio | 4020000000–403fffffff, 512 Mio inchangés |

Les résultats 04N étaient une confirmation privilégiée du boot 04M, pas un démarrage NP32 antérieur. NP agrandie conformément à l'attente 66/32 Mio ; PREF conservée intégralement. Les 66 Mio couvrent NHI 1 Mio + port cible 32 Mio + USB local 1 Mio + sœur 32 Mio.

Les huit fenêtres concordent entre registres/sysfs ; COMMAND.MEM actif, PREF64 type 1/1, bornes alignées à 1 Mio. La sœur est également contrôlée par le complément quatre-ponts. 62 inclusions BAR/fenêtres vers ancêtres réussies ; aucune collision mémoire entre allocations de même niveau. NP entièrement sous 4 Gio dans aperture publiée ACPI/hôte `80000000–feafffff`. PREF dans aperture `4000000000–7fffffffff`. Les plages cible sont vides de descendants et sans réservation concurrente publiée dans iomem. Tables ACPI et annonces de ressources racine du noyau archivées ; pas de preuve du routage d'un GPU absent ni des réservations firmware invisibles.

## Capacité de placement

Adresses inclusives, Mio=1048576 octets. BAR0 16 Mio NP : `90000000–90ffffff`, base alignée 16 Mio, dans cible `8fb00000–91afffff`. Paquet GPU 17 Mio : `90000000–910fffff` ; branche USB séparée 1 Mio : `91100000–911fffff`. Le modèle absorbe ROM historique 512 Kio (conservatrice, sans activation), audio 16 Kio, UCSI 4 Kio et marge USB NVIDIA 320 Kio ; USB boîtier 64 Kio dans sa fenêtre distincte. La somme NP stricte connue est 16,58203125 Mio, arrondie en modèle de ponts à 18 Mio. Le décalage d'alignement BAR0 consomme 5 Mio au début du port ; le modèle de 18 Mio tient réellement, marge finale 9 Mio.

BAR1 256 Mio PREF : `4000000000–400fffffff`. BAR3 32 Mio PREF : `4010000000–4011ffffff`. Bases naturellement alignées ; 224 Mio restants, suffisants aussi pour les 256+64 Kio PREF64 de l'USB NVIDIA. Ces placements sont simultanés dans leurs classes respectives. BAR5 I/O 128 octets : fenêtre cible `8000–9fff`, parents `8000–bfff`, aperture hôte `0d00–ffff` ; placement aligné possible à 8000. Bus cible 7f–b7 (57 numéros), sœur b8–f0, parents 7b/7c–f0 ; capacité numérique pour la topologie historique, sans garantie du prochain hotplug.

Les fenêtres de transit internes du Core ne s'ajoutent pas aux BAR qu'elles couvrent. Toutefois le port USB interne HotPlug+ peut demander 32 Mio NP supplémentaires : paquet GPU 17 Mio + réserve USB 32 Mio ≈49 Mio, supérieur à la cible. Une extension PREF512 interne peut également dépasser la réserve cible avec les BAR graphiques. Le placement des besoins obligatoires est établi ; conservation de toutes les réserves optionnelles internes non démontrée. Aucune substitution automatique de paramètres.

## Santé et journaux

SSD Apple AP0512M nvme0 live ; p1 vfat EFI 976 Mio, p2 ext4 /boot 977 Mio, p3 LVM 464 Gio, racine LVM ext4 **rw**, swap présent. SMART PASSED, Critical Warning=0, erreurs média/intégrité=0, Error Information Log Entries=0, 35 °C. Code smartctl=4 lié à Invalid Log Page (0x109), limite historique ; 38 arrêts non sûrs historiques.

Intel i915 primaire boot_vga=1, DP-3 connected/enabled, SDDM actif ; NVIDIA absent et Nouveau non chargé. Ethernet enp4s0 UP/carrier=1, 1000 Mbit/s, [ADRESSE PRIVÉE EXPURGÉE]/24 ; routes et écoute SSH présentes, service/socket actifs. Thunderbolt et xhci liés, NHI attribué ; Bolt indique Core disconnected, aucun descendant cible. Confirmation utilisateur archivée : connexions SSH remontées et bureau réactif depuis le redémarrage.

Les six `can't claim; no compatible bridge window` initiaux sont suivis de la reconstruction et de l'attribution finale correcte. Aucun `no space`/`failed to assign` final, faute DMAR, erreur E/S ou reset/timeout NVMe, GPU hang i915, AER critique ou déclenchement DPC relevé. Toutes les signatures d'erreur/avertissement kernel filtrées sont déjà présentes dans le dernier relevé 04N après normalisation des adresses SSDT. ACPI AE_AML_BUFFER_LIMIT/AE_ALREADY_EXISTS, IOAPIC GSI34/LPSS, liens Thunderbolt natifs, eDP désactivé, pcspkr, Broadcom/BT et unchecked buffer NVMe sont historiques. Le seul nouveau message entre captures est tg3 VPD access failed lors du second lspci ; même signature historique et aucun lien perdu. Une lecture VPD diagnostique peut provoquer ce message.

## Observation et décision

Collectes 2026-10-11T22:53:05.325274+02:00 et 2026-10-11T22:58:15.758695+02:00 : **310.433 secondes**, plus de cinq minutes. 11 relevés intermédiaires : boot, ressources PCI, nvme live, affichage Intel, carrier/vitesse et compteurs AER disponibles inchangés ; compteurs AER à zéro. Les deux captures PCI-sysfs complètes sont strictement identiques, incluant pilotes et registres de ponts. Analyseurs initiaux et finaux réussis. Aucun indice de régression critique.

A retenu dans le périmètre sans Core, B/C non observés, preuves nécessaires accessibles et validations humaines reçues, E non identifié. A ne vaut pas preuve de fonctionnement GPU ni autorisation de branchement. **Attente de votre autorisation pour toute action supplémentaire.**

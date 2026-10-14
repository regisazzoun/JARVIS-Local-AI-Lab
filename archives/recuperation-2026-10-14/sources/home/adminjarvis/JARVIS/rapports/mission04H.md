# JARVIS — Mission 04H : validation de la réallocation PCIe

**11 octobre 2026, collecte à 21:18 CEST. C — Réallocation inefficace dans cet essai : BAR 1 et BAR 3 non attribués, fenêtres insuffisantes.** Core détecté et autorisé ; la détection ne constitue pas une allocation réussie. Bureau réactif et conservation de la main confirmés par l’utilisateur.

Contrôles exclusivement en lecture seule. Seuls rapports et preuves écrits dans le dossier utilisateur ; aucun pilote installé, module NVIDIA chargé, CUDA, configuration modifiée, écriture PCIe, débranchement ou redémarrage.

## Conditions et accès hôte

Accès privilégié désormais fonctionnel : sudo -n id, lspci, journalctl, Bolt, iomem, systemctl et ss réussissent. Aucune preuve nécessaire au classement n’est bloquée par les restrictions de 04G.

Noyau `6.18.54-1-t2-trixie`, boot ID `565560bb-80ac-424b-8bc3-101e7441b335`. Ligne active :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on
```

Bolt : Razer Core authorized, UUID `e0010000-00a2-8f08-a22d-f4d4b040b318`, politique auto, génération Thunderbolt 3 ; sysfs `1-1`, authorized=1. Débits annoncés rx/tx : 20 Gb/s, deux voies. Journal : connexion à **21:16:12 CEST**, énumération PCIe à **21:16:13**. Bolt affiche 19:16:12, cohérent avec UTC ; les heures du rapport suivent journalctl +02:00.

Identification dynamique par `lspci -Dnnk -d 10de:1eb0` : Quadro RTX 5000 actuellement **0000:81:00.0**. Cette adresse est constatée, pas supposée. Aucun pilote lié au GPU, lien local 8 GT/s ×4 ; ce lien n’est pas une mesure du débit de bout en bout.

## Chaîne et fenêtres comparées

Chemin sysfs constaté : Mac mini, racine pci0000:00 → **00:01.2 → 7b:00.0 → 7c:01.0 → 7f:00.0 → 80:01.0 → 81:00.0**. Les cinq premiers périphériques sont les ponts parents de la Quadro. Le NHI 7d:00.0 appartient à une autre branche et n’est pas ajouté à cette chaîne. Des lspci -nnvvk et ressources sysfs individuels sont archivés pour tous ces périphériques.

Adresses inclusives ; Mio = 1 048 576 octets. Fenêtres lspci corroborées par sysfs.

| Pont | 04E sans realloc : non préchargeable | 04H avec realloc : non préchargeable | 04E : préchargeable | 04H : préchargeable |
|---|---|---|---|---|
| 0000:00:01.2 | `0x8f900000–0x9dafffff` (226 Mio) | `0x8fa00000–0x9dbfffff` (226 Mio) | `0xbf400000–0xcd3fffff` (224 Mio) | `0xbf400000–0xcd3fffff` (224 Mio) |
| 0000:7b:00.0 | `0x8f900000–0x9dafffff` (226 Mio) | `0x8fa00000–0x9dbfffff` (226 Mio) | `0xbf400000–0xcd3fffff` (224 Mio) | `0xbf400000–0xcd3fffff` (224 Mio) |
| 0000:7c:01.0 | `0x8fb00000–0x96afffff` (112 Mio) | `0x8fc00000–0x96bfffff` (112 Mio) | `0xbf400000–0xc63fffff` (112 Mio) | `0xbf400000–0xc63fffff` (112 Mio) |
| 0000:7f:00.0 | `0x90000000–0x961fffff` (98 Mio) | `0x90000000–0x961fffff` (98 Mio) | `0xc0000000–0xc63fffff` (100 Mio) | `0xc0000000–0xc63fffff` (100 Mio) |
| 0000:80:01.0 | `0x90000000–0x910fffff` (17 Mio) | `0x90000000–0x910fffff` (17 Mio) | Absente | Absente |

Les trois fenêtres NP hôtes sont décalées de +1 Mio sans agrandissement. Toutes les fenêtres préchargeables restent identiques : 224 Mio en amont, 112 Mio sur la branche Thunderbolt, 100 Mio sur 7f:00.0, aucune sur le pont final 80:01.0. Une fenêtre de 224 Mio est inférieure au seul BAR 1 de 256 Mio.

## BAR : attribution et couverture

Tailles confirmées par les capacités Resizable BAR de lspci -vv et les besoins du journal d’énumération. Les lignes resource nulles ne permettent pas à elles seules de mesurer un BAR non attribué.

| BAR | Taille / type requis | Début–fin attribués | Attribution sysfs | Présence dans iomem | Couverture effective de tous les parents |
|---|---|---|---|---|---|
| 0 | 16 Mio ; 32 bits non préchargeable | `0x90000000–0x90ffffff` | Oui ; flags 0x40200 | Oui, même plage GPU | Oui, inclus dans chacune des cinq fenêtres NP |
| 1 | 256 Mio ; 64 bits préchargeable | Aucune | Non : début=0, fin=0, flags=0 | Aucune plage GPU correspondante | Non : allocation absente, fenêtres amont insuffisantes et fenêtre finale absente |
| 3 | 32 Mio ; 64 bits préchargeable | Aucune | Non : début=0, fin=0, flags=0 | Aucune plage GPU correspondante | Non : allocation absente et fenêtre finale absente |

BAR 0 est couvert individuellement par 00:01.2, 7b:00.0, 7c:01.0, 7f:00.0 et 80:01.0 (comparaison début/fin inclusifs). Pour BAR 1/3, aucune couverture effective ne peut exister sans allocation ; les fenêtres amont existantes ne prouvent aucune couverture de ces BAR absents. La fenêtre finale préchargeable est absente pour les deux.

Control GPU `Mem- BusMaster-` sans pilote : décodage désactivé, mais BAR 0 bien attribué selon journal/sysfs/iomem. L’autre entrée iomem GPU `0x91080000–0x910fffff` est la ROM, pas BAR 1 ou 3. Une ligne resource 0/0/0 signifie absence d’attribution, pas allocation à zéro. Les plages à zéro lors de l’énumération expriment des besoins de taille.

Les BAR 1/3 demandent ensemble 288 Mio ; alignement et autres fonctions sont aussi à considérer. Le pont final demande initialement 0x12100000 (289 Mio), puis 0x12000000 (288 Mio) : les deux fenêtres échouent.

## Erreurs du boot actuel et modules

Journaux noyau, système et Bolt complets accessibles et archivés jusqu’à la collecte. À 21:16:13, échecs répétés :

```text
pci 0000:81:00.0: BAR 1 [mem size 0x10000000 64bit pref]: can't assign; no space
pci 0000:81:00.0: BAR 1 [mem size 0x10000000 64bit pref]: failed to assign
pci 0000:81:00.0: BAR 3 [mem size 0x02000000 64bit pref]: can't assign; no space
pci 0000:81:00.0: BAR 3 [mem size 0x02000000 64bit pref]: failed to assign
```

80:01.0 échoue aussi à obtenir sa fenêtre préchargeable. BAR 0 est attribué, libéré lors d’une nouvelle tentative puis réattribué à la même plage ; l’état final est confirmé par sysfs et iomem.

Aucun événement d’erreur AER, DPC containment ou faute DMAR/IOMMU explicite repéré dans les journaux examinés. AER/DPC apparaît dans la prise de contrôle _OSC ; DMAR/IOMMU décrit l’initialisation, les groupes et le domaine Passthrough. Ces mentions ne sont pas des erreurs. Aucun timeout/reset/I/O error NVMe ciblé identifié. Cela ne signifie pas un journal exempt de tous avertissements.

Avertissements Thunderbolt : au boot, `device links to tunneled native ports are missing!` sur les deux NHI ; au branchement, `DROM device_rom_revision 0x0 unknown`, `DROM data CRC32 mismatch ... continuing` et `ignoring unnecessary extra entries in DROM`. Autorisation et énumération se poursuivent ; aucun lien causal avec les échecs BAR n’est établi.

Nouveau absent de lsmod/sysfs ; journal à 21:16:13 : **Module nouveau is blacklisted**. `Kernel modules: nouveau` dans lspci est un candidat, pas un module chargé. Modules nvidia/nvidia_drm/nvidia_modeset/nvidia_uvm absents ; aucune initialisation graphique NVIDIA/NVRM repérée dans les journaux examinés. Les lignes HDA NVidia sont celles de l’audio HDMI/DP, pas une preuve de chargement du pilote graphique NVIDIA. Aucune tentative de chargement provoquée par cette mission.

## Affichage Intel, Ethernet et SSH

Intel 00:02.0 lié à i915, boot_vga=1, i915 chargé. GNOME utilise card0 i915 en atomic mode setting, renderer GBM et GPU primaire Intel. DP-3 connected/enabled, modes 1920×1080 ; display-manager actif. L’utilisateur confirme le bureau réactif après branchement.

Ethernet enp4s0 UP, carrier=1, 1000 Mbit/s, tg3 ; 192.168.1.99/24, route par défaut via 192.168.1.254. SSH service/socket actifs, écoute sur 127.0.0.1:22 et 192.168.1.99:22. Trois authentifications publickey réussies depuis 192.168.1.63 à 21:15 avant branchement ; les trois connexions restent ESTAB au relevé de 21:18 après branchement. Services, écoute et connexions persistantes démontrés ; aucune nouvelle connexion externe provoquée par ces contrôles.

## Synthèse comparée

| Critère | Mission 04E sans pci=realloc=on | Mission 04H avec pci=realloc=on | Différence |
|---|---|---|---|
| Noyau / blacklist | Noyau T2 identique, Nouveau absent | Identique | Argument realloc actif |
| Chaîne GPU | Même chaîne | Retrouvée dynamiquement | Aucune |
| Fenêtres préchargeables | 224/224/112/100 Mio/absente | Identiques | Aucun espace supplémentaire |
| Fenêtres NP | 226/226/112/98/17 Mio | Mêmes tailles | Trois fenêtres hôtes décalées de +1 Mio |
| BAR 0 | 16 Mio, attribué à 0x90000000 et couvert | Identique | Aucune |
| BAR 1 | 256 Mio non attribués | Toujours non attribués | Aucune amélioration |
| BAR 3 | 32 Mio non attribués | Toujours non attribués | Aucune amélioration |
| Erreurs d’allocation | can't assign/no space/failed to assign | Mêmes erreurs GPU/pont final | Échec persistant |
| Stabilité | Bureau/SSH confirmés alors | Bureau confirmé, Intel/Ethernet/SSH établis | Stabilité actuelle, allocation défaillante |

Référence 04E : autre boot `cf644abb-f9ae-4308-ba1f-d97be3e7aa39`. Le boot 04H est celui de 04G. Les relevés restreints 04G vers 21:08–21:10 précèdent l’événement désormais daté par le journal à 21:16:12 ; les fenêtres hôtes alors accessibles sont identiques aux fenêtres hôtes après branchement. Ceci fournit une comparaison avant/après limitée aux données effectivement accessibles : l’ancienne absence dans une vue isolée n’est pas une preuve générale d’absence physique. Le bilan 04G reste historiquement non concluant ; ses limites d’accès sont levées ici.

Le déplacement NP entre boots n’établit pas une amélioration partielle utile au GPU : états des trois BAR identiques à 04E, goulet préchargeable identique. Classement C, pas B. Ce constat tranche cet essai et cette configuration, sans préjuger d’autres conditions non testées.

## Preuves conservées

Dossier : `mission04H-preuves/20261011-211801/`. Boot/cmdline, identification GPU, lspci GPU/ponts, resource GPU, sysfs.json, PCI complet et arbre, iomem non masqué, journaux et extraits, modules, GNOME, DRM, réseau/routes/SSH/connexions et SHA256SUMS.json. Commandes archivées avec stderr et code de sortie. Références : `mission04E-preparation/preuves-20261011-205427/` et `mission04G-preuves/collecte-restreinte-20261011/` (limitations conservées).

**C — Réallocation inefficace : BAR 1 et BAR 3 toujours non attribués, fenêtre préchargeable finale absente et fenêtres amont insuffisantes.**

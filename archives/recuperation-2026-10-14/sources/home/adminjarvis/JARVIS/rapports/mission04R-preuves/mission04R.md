# JARVIS — Mission 04R : disparition du GPU Intel avec Core présent au boot

**Diagnostic en lecture seule autorisé par l’utilisateur. Aucune correction ni expérience avec redémarrage effectuée.** Rapport du 12 octobre 2026 ; capture principale 13:07:24–13:07:25 CEST, compléments dans les minutes suivantes. Hôte Apple Macmini8,1, Debian 13, noyau `6.18.54-1-t2-trixie`.

## Résultat principal et limites causales

**Le GPU Intel est actuellement désactivé et masqué au niveau du pont hôte : `DEVEN = 0x0000000f`, donc `D2EN`, bit 4, vaut zéro.** Cette lecture matérielle explique son absence PCI ; le problème précède le lancement de SDDM et de la session GNOME.

Ce registre a été lu dans les 256 premiers octets de configuration de `0000:00:00.0` (`8086:3ec4`), à l’offset `0x54`. Les octets sont `0f 00 00 00`. Deux lectures concordent intégralement. Le tableau Intel de cette génération associe le bit 4 à la visibilité du périphérique 2 du bus 0. Référence : [Intel, datasheet 8e/9e génération, volume 2, §3.14, page 60](https://cdrdv2-public.intel.com/337345/8th-gen-core-family-datasheet-vol-2.pdf#page=60). La table de bits a été utilisée, et non une documentation d’une autre génération.

**Le mécanisme de masquage est établi ; l’auteur et l’instant de la désactivation restent inconnus.** Le firmware Apple est l’hypothèse principale, parce qu’Intel manque dès la première énumération du bus racine alors que les autres périphériques sont détectés. Une intervention du chargeur ou d’un chemin noyau très précoce n’est pas exclue par les seuls journaux. Les captures 04O/04P ne contiennent que 64 octets de configuration des ponts ; elles ne permettent pas une comparaison historique de DEVEN à `0x54`.

Il serait donc prématuré d’affirmer « Apple désactive systématiquement l’iGPU lorsqu’un Core est présent », ou « pci=realloc est définitivement innocent ». Une capture avant Linux et une répétition contrôlée doivent établir ces points.

## 1. Identité du démarrage et inventaire

Boot actuel : `89e71147-112d-4713-a92d-2d3f97d8ae38`, identique à 04Q. Boot 04O/04P : `b70d6ac9-b00b-4a16-b60f-ba2dcd09b376`. BIOS annoncé : `2020.80.5.0.1`, date `12/20/2023` ; le journal donne iBridge `21.16.3049.0.0,0`.

`uname -a` :

```text
Linux JARVIS-MacMIini 6.18.54-1-t2-trixie #1 SMP PREEMPT_DYNAMIC Fri Sep 25 21:03:59 UTC 2026 x86_64 GNU/Linux
```

Cmdline strictement identique aux preuves 04O, 04P et 04Q :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```

Inventaire complet : **44 fonctions PCI**, fourni dans `pci.txt`, `pci-arbre.txt` et `pci-sysfs.json`. Intel `0000:00:02.0` est absent de lspci et de sysfs ; aucun autre Intel graphique n’est présent sous une adresse différente. NVIDIA Quadro RTX 5000 `10de:1eb0` reste à `0000:81:00.0`, sans pilote graphique lié, `boot_vga=0`. Aucun i915, nouveau ou nvidia chargé ; `/dev/dri` absent.

Chaîne Core conservée :

```text
00:01.2 → 7b:00.0 → 7c:01.0 → 7f:00.0 → 80:01.0 → 81:00.0
                                                   └ fonctions .1/.2/.3
                                     → 80:04.0 → 82:00.0
```

## 2. Chronologie depuis les premières lignes

`dmesg.txt` commence à l’événement noyau `0.000000`, avec la version et la cmdline. Le journal noyau complet est également archivé. Attention : les anciens messages importés par journald apparaissent à partir d’environ 2,61 s ; pour l’ordre et les intervalles internes du boot actuel, les temps dmesg sont plus précis.

| Temps noyau actuel | Événement |
|---:|---|
| 0,137788 s | Linux utilise les fenêtres du pont hôte fournies par ACPI |
| 0,156930 s | Pont hôte PCI vers bus 0000:00 |
| 0,156958 s | Détection du host bridge 8086:3ec4 en 00:00.0 |
| 0,157296 s | Détection du port 00:01.2 ; pas de détection de 00:02.0 ensuite |
| 0,233594 s et suivantes | Refus de revendication de certaines fenêtres Thunderbolt initiales |
| 0,233889 s | Chargement de vgaarb, sans GPU Intel à enregistrer |
| 0,250781 s | Attribution de la fenêtre NP reconstruite de 00:01.2 |
| 0,268292 s | Initialisation du framebuffer EFI |
| 3,741558 s | Codec Intel HDMI/DP : aucune liaison i915 |
| 4,152756 s | Détection NVIDIA 81:00.0 dans la chaîne Core |
| 4,155046 s | Ajout NVIDIA à vgaarb, `owns=none` |
| 23:11:38 CEST | Service SDDM lancé ; pas de création de display |
| 23:11:45 CEST | graphical.target atteint |

La recherche exacte `0000:00:02.0` donne **zéro occurrence** dans dmesg et le journal noyau actuel. Aucun Intel détecté puis supprimé, aucun BAR Intel refusé, aucune tentative d’initialisation i915 ni de KMS Intel. La recherche ne confond pas le NVMe Apple `0000:02:00.0` avec l’iGPU `0000:00:02.0`.

La mention humaine « Core connecté avant le boot » est conservée comme observation. Linux détecte ses fonctions après quelques secondes ; ce délai ne démontre pas ce que le firmware voyait avant Linux.

## 3. Pont hôte, ACPI _CRS et tables firmware

Les annonces effectives de ressources racine sont **strictement identiques à celles du boot 04O/04P** :

| Classe | Aperture effective annoncée |
|---|---|
| I/O | `0000–0cf7`, `0d00–ffff` |
| Mémoire legacy | `000a0000–000fffff` |
| Mémoire basse | `80000000–feafffff` |
| Mémoire haute | `4000000000–7fffffffff` |
| Bus ACPI | `00–ff` |

MCFG publie un ECAM `e0000000–ef0fffff`, bus `00–f0`. L’avertissement de couverture partielle du pont ACPI est historique ; il ne concerne pas un manque de couverture du bus 00 où se situe Intel.

**Les 21 tables ACPI statiques actuelles sont identiques octet pour octet aux tables 04O et 04P**, dont DSDT, SSDT6/SaSsdt, SSDT11/Thunderbolt, DMAR et MCFG. Les empreintes et résultats de comparaison sont dans `comparaison.json`.

Désassemblage hors ligne de DSDT, SSDT6 et SSDT11 avec l’iasl déjà disponible dans les preuves 04L, sans installation et sans exécution de méthode ACPI :

- DSDT conserve `Device (IGPU)` et `_ADR = 0x00020000` ; son existence ne rend pas une fonction PCI masquée accessible.
- Le nœud sysfs ACPI `LNXVIDEO:00` a toujours le chemin `\_SB_.PCI0.IGPU`, avec des descendants. Pas de valeur `status` publiée pour ce nœud dans le relevé : aucun `_STA=0` de l’iGPU n’est démontré.
- Le `_STA` à zéro relevé pour `IGPU.IPUA` concerne un sous-périphérique ; il ne doit pas être attribué à l’iGPU lui-même.
- Le code `_CRS` construit les plages à partir de variables telles que TLUD, M64B et M64L. Des tables identiques ne garantissent donc pas des valeurs mémoire firmware identiques ; ici, les apertures effectives racine concordent.
- DMAR conserve une unité DRHD à `fed90000` avec scope bus 0/device 2/function 0, et un RMRR `79800000–7fffffff` pour ce même scope. Cette description statique d’Intel persiste malgré son absence PCI ; elle ne prouve pas son activation.

Le désassemblage global `iasl -da` échoue sur des doublons (`AE_ALREADY_EXISTS`). Cet échec est archivé. Les désassemblages individuels réussissent, avec avertissements de références externes ; les constats portent sur les constructions directement lisibles, sans prétendre avoir validé l’exécution complète de l’AML. Les messages iasl hors ligne ne sont pas des erreurs supplémentaires survenues dans le noyau.

## 4. Registres matériels du pont hôte

| Élément | Lecture actuelle | Interprétation / limite |
|---|---|---|
| Host bridge | 8086:3ec4, 00:00.0 | Périphérique présent |
| DEVEN, offset 54h | `0000000f` | D2EN, bit 4, à zéro : périphérique graphique masqué |
| Confirmation | 256 octets identiques sur deux lectures | État stable durant le relevé |
| GGC, offset 50h, 16 bits | `03c1` | Bit IVD=0, verrou GGC=1 |
| Référence DEVEN 04O/04P | indisponible | Les captures historiques s’arrêtent avant cet offset |

Le bit IVD de GGC règle les cycles VGA legacy, tandis que D2EN règle la visibilité du périphérique. La combinaison actuelle IVD=0 / D2EN=0 doit être consignée sans déduire que l’iGPU est actif ou que le framebuffer EFI est nécessairement balayé par Intel. Le tableau GGC décrit aussi le verrou au bit 0. Référence : [Intel, même datasheet, §3.13–3.14](https://cdrdv2-public.intel.com/337345/8th-gen-core-family-datasheet-vol-2.pdf#page=59).

Aucune écriture dans ces registres, aucune lecture forcée d’une fonction absente via `/dev/mem`, aucun essai de réactivation. La lecture post-boot de DEVEN prouve l’état actuel, pas son historique. Le fonctionnement antérieur d’Intel rend une incapacité matérielle permanente beaucoup moins plausible.

## 5. Ressources initiales, réallocation et portée des paramètres

Les paramètres `resource_alignment` visent `00:01.2`, `7b:00.0` et `7c:01.0`, confirmé par sysfs. Intel `00:02.0` est une fonction du bus racine, distincte de ces ponts et extérieure à leur descendance. `pci=realloc=on` reste un paramètre global : la liste d’alignement ne limite pas nécessairement tous ses effets à trois fonctions.

Une différence initiale réelle apparaît avant reconstruction :

| Fenêtre NP du port 7c:01.0 | Plage | Taille |
|---|---|---:|
| Initiale 04O/boot 04P | `8fc00000–96bfffff` | 112 Mio |
| Initiale actuelle | `8fc00000–96ffffff` | 116 Mio |
| Finale 04O/04P/actuelle | `8fb00000–91afffff` | 32 Mio |

La fenêtre initiale actuelle recouvre sur **4 Mio** (`96c00000–96ffffff`) le début de la fenêtre sœur 7c:04.0 (`96c00000–9dbfffff`). C’est une différence de l’état initial rapporté, corrigée par la reconstruction finale. Elle est dans la branche ciblée et ne recouvre aucun BAR Intel historique. Elle n’établit pas que ce chevauchement cause le masquage DEVEN.

La comparaison des BAR et fenêtres initiales publiés dans le journal, avant les premiers refus de revendication, ne trouve pas d’autre différence de ces champs pour les BDF communs à 04O. Les lectures ne constituent pas un dump de toutes les ressources du firmware avant Linux.

Les six refus initiaux « can't claim; no compatible bridge window » sont suivis de reconstruction et d’attribution. Les ressources finales de **tous les BDF communs à 04P sont identiques**, comme leurs pilotes. Aucun transfert de BAR Intel vers NVIDIA, aucune disparition d’un autre BDF, aucune nouvelle fonction depuis 04P. Par rapport à 04O, seuls les huit BDF Core sont ajoutés et Intel manque.

Ainsi, les paramètres modifient bien les fenêtres Thunderbolt pendant ce démarrage, comme lors du boot fonctionnel ; **aucun effet final collatéral sur les ressources des périphériques communs n’est observé**. L’absence Intel dans le scan initial précède les allocations visibles à 0,250 s. Cela affaiblit l’hypothèse d’un simple échec d’attribution de BAR Intel. Cela ne couvre pas un éventuel chemin noyau précoce non journalisé.

## 6. BAR Intel historiques et collisions

Recherche de chevauchements contre toutes les ressources PCI actuelles et contre les BAR/fenêtres PCI initialement annoncés :

| BAR Intel en 04O/04P | Classe / plage | Chevauchement PCI actuel ou initial |
|---|---|---|
| BAR0 | NP `80000000–80ffffff`, 16 Mio | aucun |
| BAR2 | PREF `a0000000–afffffff`, 256 Mio | aucun |
| BAR4 | I/O `3000–303f`, 64 octets | aucun |

La réservation efifb `a0000000–a07e8fff` est dans l’ancien BAR2 Intel. Ce framebuffer EFI avait la même base au boot fonctionnel, avant le relais i915 ; cette superposition historique ne démontre pas une nouvelle collision bloquante. Les enveloppes du pont hôte dans iomem couvrent normalement les ressources enfants : elles ne sont pas des propriétaires concurrents.

Ressources NVIDIA finales inchangées : BAR0 `90000000–90ffffff`, BAR1 `4000000000–400fffffff`, BAR3 `4010000000–4011ffffff`. Pas de conflit avec les plages Intel ci-dessus. Les refus de réserve Core NP 49 Mio/PREF 802 Mio retombent sur les fenêtres obligatoires, comme en 04P ; ils n’indiquent pas un BAR Intel non attribué.

Limite : cet audit couvre les ressources publiées ; il ne certifie pas l’absence de réservations firmware invisibles ni le routage électrique d’un GPU masqué.

## 7. ACPI, PCIe, IOMMU/DMAR et arbitrage VGA

Aucune nouvelle signature d’erreur ACPI/DMAR/IOMMU dans le journal actuel par rapport aux journaux complets des captures 04O et 04P, après normalisation des adresses de tables chargées. Restent les erreurs historiques AE_AML_BUFFER_LIMIT sur `_SB._OSC` et AE_ALREADY_EXISTS sur les tables CPU ; elles existaient avec Intel fonctionnel.

Pas de faute DMAR/IOMMU, de déclenchement DPC ou d’événement AER fatal/nonfatal identifié dans les journaux examinés. Les compteurs AER sysfs disponibles sont archivés ; leur absence éventuelle ne vaut pas un zéro. Aucun effacement de statut ni audit de charge. Les anciennes réserves 04P sur les statuts persistants de la NVIDIA ne sont pas annulées par ce relevé.

Arbitrage VGA actuel : vgaarb chargé sans ajout Intel, puis NVIDIA enregistrée avec `decodes=io+mem,owns=none,locks=none`, boot_vga=0. Aucun événement « Intel boot VGA » ni changement des décodages Intel. L’arbitrage Linux ne montre donc pas une reprise de l’affichage par NVIDIA ni le retrait d’un Intel auparavant présent.

Le message `No i915 binding for Intel HDMI/DP codec` est cohérent avec l’absence graphique ; ce symptôme audio n’en établit pas la cause.

## 8. Absence de greeter et fond GRUB

Le système atteint graphical.target ; SDDM PID 932 est actif. Pourtant seat0 indique `CanGraphical=no`, aucune session locale, aucun Xorg, greeter, GNOME Shell/Mutter ou KWin en exécution. Le journal SDDM s’arrête après « Logind interface found », avant toute création de display.

L’environnement réellement utilisé en 04O/04P était **GNOME Wayland**, avec greeter SDDM X11. GNOME et Plasma sont installés ; la dernière session mémorisée reste GNOME Wayland. Le diagnostic actuel n’est pas celui d’un compositeur Plasma défaillant.

**Dans cette configuration, perdre Intel suffit à expliquer l’absence du greeter :** c’était le seul GPU disposant d’un pilote graphique utilisable, la NVIDIA n’ayant aucun pilote graphique lié. L’absence de DRM et le refus de capacité graphique du seat concordent avec SDDM restant sans display. Cela ne signifie pas qu’un SDDM ne pourrait jamais utiliser un autre backend dans une autre configuration.

Seul framebuffer : EFI VGA, base `a0000000`, 1920×1080×32, stride 7680. Aucun relais i915drmfb, aucun connecteur DP-3 exposé. fbcon est lié au framebuffer ; on ne peut pas affirmer que Linux n’y a jamais écrit. L’écran conservant le fond GRUB est compatible avec l’absence de nouveau rendu graphique. Les pixels et le rafraîchissement physique n’ont pas été mesurés. **Aucun bureau fonctionnant invisiblement en arrière-plan n’est observé.**

## 9. Classement des causes

| Niveau de preuve | Proposition | Éléments / limites |
|---|---|---|
| Établi | Intel masqué par D2EN=0 | Registre documenté, deux lectures concordantes, absence PCI/sysfs |
| Établi | Chaîne graphique non lancée faute de GPU utilisable dans l’état actuel | Aucun DRM, CanGraphical=no, pas de greeter/session |
| Hypothèse prioritaire | Décision firmware Apple dépendant du Core présent au boot | Intel absent dès le scan ; différence entre boot sans Core et boot actuel ; acteur non tracé |
| Possible, non démontré | État hérité du boot précédent, distinction démarrage chaud/froid, ou intervention pré-Linux du chargeur | Une seule capture du boot problématique ; pas de relevé DEVEN avant Linux |
| Possible mais moins étayé | Chemin noyau très précoce dépendant de topologie, éventuellement lié aux paramètres PCI | Mêmes paramètres au boot fonctionnel ; pas de trace d’écriture DEVEN ; reste à tester indépendamment |
| Peu étayé comme cause directe | Collision de BAR / refus de fenêtres Thunderbolt | Aucun chevauchement Intel publié ; ressources finales identiques ; iGPU absent avant attribution visible |
| Non étayé | Modification des tables ACPI statiques supprimant IGPU | 21 tables identiques, nœud IGPU conservé |
| Non étayé | Faute IOMMU/DMAR ou crash i915/GNOME/SDDM causant la disparition PCI | Pas de faute pertinente ; i915 et session non lancés ; DEVEN explique l’absence en amont |
| Peu plausible sans nouvelle preuve | Défaillance permanente de l’iGPU | GPU opérationnel en 04O/04P ; état de masquage cohérent, mais aucune expérience de retour à l’état fonctionnel |

## 10. Protocole recommandé — à autoriser séparément

**Aucune des expériences ci-dessous n’a été exécutée.** Elles exigent des redémarrages, changements de branchement ou choix de démarrage actuellement interdits. Le système reste dans son état présent en attente de votre autorisation.

### A. Reproduction avec une seule variable : Core présent ou absent avant boot

Fixer d’abord les constantes : même noyau/cmdline/GRUB, même alimentation et port Thunderbolt, même écran/câble/sortie Intel, même procédure de démarrage (chaud OU froid pour toute la série), mêmes autres périphériques. Conserver un accès réseau indépendant.

| Essai | Seule variable | Prédiction de l’hypothèse firmware |
|---|---|---|
| A1 | Core absent avant démarrage | Intel visible, D2EN=1, i915/DRM et greeter fonctionnels |
| B1 | Core présent avant démarrage | Intel absent, D2EN=0, absence DRM/greeter |
| A2 | Retour Core absent, même procédure | Retour à l’état A1 |
| B2, si nécessaire | Répétition Core présent | Confirmation de reproductibilité |

Pour chaque boot, recueillir **avant toute autre intervention** boot ID, cmdline, dmesg complet, inventaire PCI, 256 octets host bridge dont DEVEN/GGC, tables ACPI, apertures racine, fenêtres initiales/finales, seat, services et observation écran. Une fois A1 capturé, un hotplug séparément autorisé peut mesurer DEVEN avant/après pour vérifier si le masquage nécessite le passage par un démarrage.

Critère : alternance reproductible de D2EN/Intel avec la seule présence pré-boot renforce la causalité de cette condition, mais ne désigne pas encore le composant logiciel responsable. Si A2 ne rétablit pas Intel, ne pas attribuer automatiquement le résultat au Core ; examiner l’état hérité avant de poursuivre.

### B. Départager firmware, chargeur et noyau

Sur les mêmes états A/B, prévoir une capture **en lecture seule** de DEVEN et de l’inventaire PCI avant le chargement de Linux, avec un outil UEFI/GRUB dont les opérations sont vérifiées à l’avance. Ne pas improviser de commande d’écriture de registre. Garder le même chemin de démarrage ; si l’outil impose un chemin distinct, le valider comme expérience séparée, car il ajoute une variable.

- D2EN=0 et Intel masqué déjà avant Linux : exclut la réallocation Linux comme initiateur ; privilégie firmware/chargeur selon le point de capture.
- D2EN=1 avant Linux, puis D2EN=0 après : rechercher un acteur entre ces points ; conserver un journal noyau précoce lors d’une mission dédiée.
- Capture avant GRUB avec Intel visible, après GRUB masqué : orienter l’enquête vers le chargeur ou son interaction avec le firmware.

Les captures actuelles ne peuvent pas reconstituer ces valeurs antérieures. Aucune méthode ACPI ni modification EFI n’est nécessaire pour une simple lecture du registre.

### C. Distinguer état chaud/froid

Seulement après la série A/B, maintenir le Core présent, les paramètres et le câblage constants ; comparer une procédure de démarrage chaud et une procédure froide définies précisément. Répéter avec retour au premier état. Cette série teste une autre variable et doit rester distincte de la série A/B.

### D. Paramètres PCI, si les séries précédentes ne tranchent pas

Avec Core présent et procédure de démarrage fixée, prévoir éventuellement un essai temporaire d’une seule option à la fois : d’abord `pci=realloc=on`, puis, dans une série distincte, `pci=resource_alignment`. Chaque série doit partir de la référence et y revenir ; conserver les deux réserves hotplug et les autres paramètres. Les trois BDF de la liste d’alignement peuvent ensuite être isolés un par un si un effet est reproductible.

Ces essais changeraient la cmdline et les allocations ; **aucune autorisation n’est présumée**. Ils viennent après la capture pré-Linux, plus discriminante. Avant exécution, préparer un retour à l’entrée de démarrage connue et une surveillance Ethernet/NVMe. Un changement de D2EN/visibilité est le critère principal ; un autre écran noir dû à des BAR NVIDIA non attribués ne prouve pas la même cause.

Ne pas mélanger ces essais avec installation NVIDIA, chargement forcé i915, rescan, écriture DEVEN, modification ACPI ou redémarrage de SDDM.

## 11. État préservé et preuves

NVMe `nvme0` : live ; racine LVM/ext4 montée rw. Ethernet `enp4s0` : carrier=1, 1000 Mbit/s ; routes, adresse et connexions TCP archivées. SSH service/socket actifs ; la connexion de travail reste opérationnelle. Core connecté et autorisé. Aucun test SMART supplémentaire, test de charge ou lecture VPD diagnostique demandé dans cette mission.

Preuves sous `mission04R-preuves/` :

- Collecteur et analyseur conservés, commandes/retours et dates dans `collecte.json`.
- Journaux noyau et système complets, dmesg depuis 0 s, journal précédent, SDDM et liste des boots.
- Inventaire complet PCI/arbre/sysfs, headers de ponts/GPU, host bridge 256 octets et confirmation.
- 21 tables ACPI, inventaire sysfs ACPI, code DSL et journaux de désassemblage.
- Comparaison 04O/04P/04Q, analyse des erreurs et de DMAR, collisions finales/initiales, différence de fenêtre initiale.
- État graphique, services, modules, stockage, montages, réseau et connexions.

Les PDF/texte complets de la documentation Intel ont été téléchargés uniquement comme référence locale, sans installation ; son URL et empreinte sont conservées. L’archive technique exclut ces deux copies complètes de documentation, accessibles par le lien Intel, et inclut les preuves locales et le décodage retenu. Les codes d’échec attendus (objets absents) et avertissements sont conservés. Les preuves et le rapport sont accompagnés d’empreintes SHA-256.

**Fin de mission : masquage matériel Intel identifié ; origine firmware probable mais non prouvée. Attente d’une autorisation distincte pour les expériences contrôlées.**

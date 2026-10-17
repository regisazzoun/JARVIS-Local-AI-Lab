> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission04U.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 04U : localiser le masquage Intel entre GRUB et Linux

Date : 12 octobre 2026. Mac mini 2018, Debian 13 T2Linux, noyau `6.18.54-1-t2-trixie`.

**Conclusion : la transition `DEVEN 0x3f → 0x0f` est établie entre les mesures communiquées dans GRUB et Linux. Son auteur n’est pas identifié. Les candidats prioritaires sont une intervention firmware pendant le transfert EFI, ou une interaction ACPI/firmware déclenchée par Linux. Une écriture directe du noyau reste à vérifier sur les sources exactes du binaire T2 installé.**

**Mise à jour après réception des fichiers : les deux captures complètes de 1 538 lignes ont été analysées. Le dmesg commence à 0.000000. Intel manque dès le scan initial du bus racine, vers 0,167 s, avant la réallocation publiée à 0,262 s et avant la détection NVIDIA à 3,965 s. Aucun résultat du boot 04R n’est attribué au boot 04U. Les journaux ne mesurent toutefois pas DEVEN à cet instant et ne tracent pas son écriture.**

Seules des lectures et la création de ce rapport ont été effectuées. Aucun redémarrage, débranchement, rescan, chargement de pilote, installation, écriture DEVEN ou modification GRUB/EFI/PCIe/ACPI/systemd. Tous les protocoles ci-dessous sont des propositions non exécutées, nécessitant une autorisation distincte.

## 1. Preuves et provenance

| Élément | Résultat | Provenance et portée |
|---|---|---|
| Boot actuel | `[UUID EXPURGÉ]` | `/proc/sys/kernel/random/boot_id`, confirmé au début et à la fin des lectures |
| Noyau | `6.18.54-1-t2-trixie`, compilation du 25 septembre 2026 | `uname -a` ; paquet installé `linux-image-6.18.54-1-t2-trixie`, version `6.18.54-1`, source déclarée `linux-upstream` |
| Core présent avant mise sous tension | Oui | Observation utilisateur |
| DEVEN dans GRUB | `0x0000003f`, deux lectures | Résultat expérimental communiqué ; photographies et identité PCI pré-Linux non examinées ici |
| DEVEN après Linux | `0x0000000f` | Résultat communiqué ; nouvelle lecture privilégiée impossible dans cet environnement |
| Pont hôte | `8086:3ec4`, `0000:00:00.0` | VID/DID sysfs et premiers octets de configuration concordants |
| Intel `0000:00:02.0` | Absent | Vérification actuelle du chemin sysfs ; `/dev/dri` absent également |
| Modules graphiques | Aucun i915/nouveau/nvidia/apple-gmux dans `/proc/modules` au relevé | Photographie actuelle, pas une histoire du chargement |
| Thunderbolt | Module chargé | `/proc/modules` ; ne prouve pas l’instant du tunnel PCIe |
| SSH | Opérationnel selon l’utilisateur | Pas de nouvelle validation de service ni de session distante effectuée ici |

Cmdline actuelle, identique à celle des rapports 04O/04P :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```

La lecture sysfs de configuration du pont hôte ne restitue que **64 octets** sans privilèges, malgré une taille affichée de 256 octets. Elle confirme VID/DID, mais n’atteint pas `0x54`. Aucune valeur DEVEN ne doit être inventée à partir de cette lecture tronquée.

Le [datasheet Intel Coffee Lake / Refresh, volume 2, registre DEVEN §3.14](https://cdrdv2-public.intel.com/337345/8th-gen-core-family-datasheet-vol-2.pdf) est également archivé en 04R. À B0:D0:F0 + `54h`, D2EN est le bit 4 et D3EN le bit 5. `0x3f XOR 0x0f = 0x30` : **les deux bits passent de 1 à 0 entre les observations**. D2EN=0 masque le périphérique 2 et explique l’absence Intel. D3EN concerne le périphérique 3 ; ce n’est pas un deuxième bit d’activation de l’iGPU. Ne pas déduire son rôle exact ici. Champs verrouillables : aucune connaissance actuelle du verrou DEVEN, ni autorisation de le tester par écriture.

Deux lectures GRUB concordantes établissent une stabilité durant leur intervalle. Elles n’excluent ni une transition ultérieure, ni plusieurs changements intermédiaires. La vérification sysfs seule ne prouve pas le passé ; les captures désormais reçues confirment indépendamment que ce boot ne journalise aucune détection Intel dès son scan initial.

## 2. Journal 04U : collecte reçue et chronologie depuis t=0

Commande réellement tentée :

```text
journalctl -b 41984ede628649dcbb6c2fbd189b6869 -k --no-pager -o short-monotonic
```

Résultat : avertissement d’accès limité, puis `-- No entries --`. `dmesg --time-format=raw` échoue avec `Operation not permitted`. `sudo -n id` échoue : configuration visible appartenant à UID 65534, puis flag `no new privileges`. Les fichiers `system.journal` sont présents sous `/var/log/journal/2201d5aba3834f0e997d0064b0ba7fa2/`, mais leurs permissions n’accordent pas la lecture à cette session. **Ce sont des restrictions de collecte, pas une preuve de journal vide ou de défaut SSH.** Aucune tentative de changement de permissions, de groupes ou de contournement.

### Collecte désormais disponible

L’utilisateur a généré les deux fichiers depuis sa session privilégiée puis autorisé leur consultation. L’échec d’accès ci-dessus décrit la première phase de la mission ; il n’empêche plus l’analyse des captures reçues.

| Fichier original | Lignes / octets | SHA-256 |
|---|---|---|
| `/home/adminjarvis/mission04U-dmesg.txt` | 1 538 / 118 852 | `98b6eb160dde7c428ba2eaed8925f46cd8f9fd8bad703cc31f7256b571fff059` |
| `/home/adminjarvis/mission04U-journal-noyau.txt` | 1 538 / 154 983 | `f7f92db904b67dfdac049fa1b3109eaa05510639078f05536e60be4c80db8484` |

Les fichiers ont été lus intégralement par l’analyse hors ligne. Après retrait des préfixes de présentation, horodatages et normalisation des espaces, **les 1 538 messages sont identiques et dans le même ordre**. Les captures ne sont donc pas deux observations matérielles indépendantes. Le dmesg commence à `0.000000` et se termine à `12.638010`. Journald présente les premiers messages importés vers `2.300383`, puis des temps légèrement différents : utiliser les temps **dmesg** dans la chronologie ci-dessous.

Le noyau et la cmdline concordent avec la référence. Le boot ID live reste `[UUID EXPURGÉ]`. Le fichier texte ne contient pas lui-même de champ `_BOOT_ID` : son rattachement repose sur la commande de génération fournie, la confirmation utilisateur et cette concordance avec le boot courant.

### Chronologie propre à 04U

| Temps dmesg | Événement observé |
|---:|---|
| 0.000000 | Version, cmdline, EFI Apple v2.4 et restriction runtime v1.10 |
| 0.028528 | Configuration `_OSI(Darwin)` via DMI Apple |
| 0.121396 | Ajout `_OSI(Darwin)` et désactivation des chaînes OS vendors par défaut |
| 0.135046 / 0.135895 | Darwin honoré via DMI ; Linux ignoré |
| 0.142776–0.144875 | Erreurs historiques `_OSC`/tables CPU ACPI |
| 0.146284 | Interpréteur ACPI activé |
| 0.146316 | Utilisation des fenêtres host bridge fournies par ACPI |
| 0.166406 / 0.166411 | Pont racine PCI0 et contrôle OS des fonctions PCIe annoncés |
| 0.166884 / 0.166913 | Pont hôte vers bus 00 ; détection `8086:3ec4` |
| 0.167254–0.167655 | Port `00:01.2`, puis périphérique `00:12.0` ; aucune détection `00:02.0` |
| 0.244450–0.244473 | Six refus initiaux de revendication de ressources Thunderbolt |
| 0.244745 | vgaarb chargé, sans GPU Intel enregistré |
| 0.245769 / 0.245823 | Deux erreurs de résolution de chemins dans les propriétés EFI Apple |
| 0.262146 et suivantes | Attribution des fenêtres NP/PREF reconstruites |
| 0.279639 | Framebuffer EFI à `0xa0000000`, 1920×1080×32 |
| 0.682009 et suivantes | Initialisation Thunderbolt ; avertissements de liens natifs |
| 1.115909 / 1.115917 | Découverte Thunderbolt du Razer Core |
| 3.495167 | `No i915 binding for Intel HDMI/DP codec` |
| 3.803785 | pciehp annonce Card present sur `7c:01.0` |
| 3.964707 | Première détection PCI de NVIDIA `81:00.0`, `10de:1eb0` |
| 3.973896–3.974245 | Réserves optionnelles refusées puis BAR NVIDIA obligatoires attribués |
| 4.142195 | Nouveau explicitement blacklisté |
| 12.637977 | Ethernet hôte enp4s0, lien 1000 Mbps full duplex |

Recherche sur l’intégralité des deux captures : **zéro occurrence de `0000:00:02.0`**, zéro DEVEN/D2EN/D3EN, aucun chargement/initialisation i915 ; la seule mention i915 est le symptôme audio à 3,495 s. Aucun Intel énuméré puis retiré, aucun BAR Intel refusé ou crash graphique Intel n’est journalisé. Il n’y a pas non plus de message de réservation « stolen » ; cette absence ne remplace pas une lecture précoce du registre.

**La non-détection est donc acquise au scan initial vers 0,167 s.** La combinaison avec les mesures DEVEN communiquées est cohérente avec un masquage survenu avant ce scan, mais **le journal ne prouve pas directement que DEVEN était déjà 0x0f à 0,167 s**. L’instant exact de son changement reste compris entre les deux observations du registre ; la chronologie fournit une borne du symptôme PCI, pas une mesure intermédiaire DEVEN.

### Comparaison ciblée des anomalies avec les captures 04O/P

Après normalisation des adresses de tables SSDT, les erreurs ACPI sélectionnées `AE_AML_BUFFER_LIMIT` et `AE_ALREADY_EXISTS` sont retrouvées dans les archives fonctionnelles. Darwin est déjà honoré dans les deux situations. Aucune faute DMAR, erreur AER fatal/nonfatal, déclenchement de containment DPC ou timeout/reset/erreur E/S NVMe n’a été identifié par les recherches dans ces captures ; cela ne garantit pas l’absence d’erreurs matérielles non journalisées.

Deux signatures nouvelles par rapport aux journaux 04O/P examinés sont présentes : `apple-properties: device path parse error -19 at 0x14` et `... at 0x26`. Le premier dump contient notamment des propriétés graphiques `AAPL,ig-platform-id` et `GraphicsDisplaySetup` ; le deuxième des propriétés Tunnel Endpoint. Elles méritent d’être conservées comme différences pertinentes du passage firmware/OS.

Le [code stable v6.18.54 apple-properties.c](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/firmware/efi/apple-properties.c) résout un chemin EFI vers un périphérique Linux ; sur erreur il journalise le bloc puis ignore ce périphérique. Il ne contient pas d’écriture DEVEN dans ce chemin. Ces erreurs arrivent **après le scan sans Intel** : elles peuvent être une conséquence de périphériques non encore ou plus visibles, et ne prouvent pas une désactivation graphique par ce parseur. Leur origine exacte demande le décodage complet des chemins et la comparaison des propriétés fournies au chargeur.

Les fenêtres racine publiées sont identiques aux archives fonctionnelles : mémoire basse `80000000–feafffff`, mémoire haute `4000000000–7fffffffff`. Les six refus initiaux sont suivis de reconstruction. Les refus vers 3,974 s portent sur les réserves optionnelles du Core : les BAR NVIDIA finaux sont attribués à `90000000`, `4000000000` et `4010000000`, comme en 04P. **Ces allocations tardives ne peuvent expliquer la non-détection antérieure d’Intel au scan.** Un effet noyau plus précoce ou une réaction firmware indirecte reste ouvert.

## 3. Comparaison avec 04O, 04P et 04S

Les journaux archivés `mission04O-preuves/initial/journal-noyau.json` et `mission04P-preuves/initial/journal-noyau.json` ont été lus et recherchés hors ligne : respectivement **1 303 et 1 539 lignes**. Ils commencent par la version du noyau et la cmdline. Leurs dates ISO sont des dates journald, pas une chronologie dmesg précise.

| Essai | Situation | Intel / DEVEN | Ce que cela permet de conclure |
|---|---|---|---|
| 04O | Démarrage sans Core | Intel `8086:3e9b` énuméré, i915 initialisé ; DEVEN non capturé à 54h | Cette configuration noyau/paramètres sait conserver Intel |
| 04P | Core branché à chaud, **même boot** `[UUID EXPURGÉ]` | Intel conservé ; DEVEN non capturé | La présence simultanée Linux du Core et d’Intel est possible ; ce n’est pas un second boot indépendant |
| 04S A1 | Core absent au démarrage | `3f`, Intel fonctionnel | Résultat transcrit en 04T, issu du contexte utilisateur |
| 04S B1 | Core présent au démarrage | `0f`, Intel absent | Même provenance ; dépendance reproductible à la condition de boot |
| 04S A2 | Core absent au démarrage | `3f`, Intel rétabli | Retour à la référence ; aucune nouvelle collecte de cet essai ici |
| 04U | Core présent avant mise sous tension | GRUB `3f` ×2 ; Linux `0f`, Intel absent | Localise la transition après la dernière lecture GRUB, sans désigner l’acteur |

Le rapport/fichiers bruts 04S n’ont pas été retrouvés. Ses résultats viennent de `mission04T.md` ; ils ne sont pas présentés comme une nouvelle vérification de traces 04S.

Éléments effectivement retrouvés dans les archives 04O/04P : détection host bridge `8086:3ec4`, dix lignes PCI de `00:02.0`, BAR0 Intel `80000000–80ffffff`, BAR2 `a0000000–afffffff`, enregistrement boot VGA et `[drm] Initialized i915`. Le hotplug Core est journalisé le 11 octobre à **23:02:22 CEST**, puis NVIDIA `81:00.0` et changements de décodage VGA Intel. Intel reste présent après ces changements : décodage VGA legacy et visibilité PCI sont distincts.

Les deux archives montrent également EFI Apple v2.4, limitation aux services runtime EFI v1.10, `_OSI(Darwin)` honoré via DMI et `_OSI(Linux)` ignoré. Les erreurs `_OSC` historiques existaient avec Intel fonctionnel. Leur seule réapparition éventuelle ne suffirait donc pas à expliquer 04U.

Référence supplémentaire **04R, autre boot** `[UUID EXPURGÉ]` : son rapport et ses preuves décrivent Intel absent dès le scan vers 0,157 s, avant les allocations à environ 0,251 s. Ils rendent une cause précoce plausible, mais ces bornes **ne sont pas transférables à 04U**. Les 21 tables ACPI identiques entre 04R et 04O/P, ainsi que l’absence de collision BAR Intel publiée, sont des constats historiques, non des contrôles actuels de toutes les tables 04U.

## 4. Chemins Linux susceptibles d’intervenir

### Écritures directes de configuration PCI

Linux peut écrire via `pci_write_config_*`, les opérations PCI brutes x86/CF8-CFC, ECAM/MMCONFIG, des quirks précoces, ou des restaurations de configuration. La recherche doit inclure les écritures octet à `54h` et les accès plus larges couvrant ce registre, les macros, les identifiants génériques et les adresses MMIO aliasées. Une recherche du seul mot DEVEN n’est pas exhaustive.

Dans [drivers/pci/quirks.c de Linux stable v6.18.54](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/pci/quirks.c), les recherches textuelles `DEVEN`, `3ec4`, `0x54` ne trouvent pas de correspondance. Aucun quirk explicite masquant ce pont hôte n’a été identifié. Cela ne certifie pas toutes les sources ni les patches du noyau installé. Les passes early/header peuvent intervenir pendant l’énumération ; les passes final et les sondes de pilotes interviennent plus tard. Le quirk générique des host bridges `quirk_mmio_always_on` évite de couper le décodage pendant le dimensionnement des BAR, sans être une écriture D2EN.

Le [scan PCI, drivers/pci/probe.c](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/pci/probe.c) est un point d’instrumentation pertinent : lectures d’identité, `pci_setup_device`, fixups puis ajout des périphériques. Si le scan ne voit jamais Intel, un quirk s’exécutant uniquement lors de la sonde i915 n’est pas une bonne explication du premier masquage.

Les sources locales `mission04N-preparation/sources/pci.c` et `setup-bus.c`, dont la provenance déclare v6.18.54, ne présentent aucune correspondance textuelle `DEVEN|0x54|3ec4` dans la recherche effectuée. Réallocation et alignement manipulent les ressources BAR/fenêtres ; aucune écriture DEVEN n’a été identifiée dans ce périmètre. Les trois BDF d’alignement sont distincts de `00:00.0` et `00:02.0`. `pci=realloc=on` demeure global : une influence indirecte n’est pas exclue sans chronologie et audit complets.

### Initialisation Intel, framebuffer et arbitrage

Le [code x86 early-quirks v6.18.54](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/arch/x86/kernel/early-quirks.c) comprend `intel_graphics_quirks` et la réservation de mémoire stolen. Ce chemin lit les données graphiques et réserve une plage e820 ; le chemin examiné ne désactive pas D2EN/D3EN. Il démontre néanmoins qu’une activité graphique existe avant i915.

La [sonde i915](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/gpu/drm/i915/i915_driver.c) requiert un périphérique PCI détecté. La configuration locale donne `CONFIG_DRM_I915=m` ; son absence actuelle n’établit pas son historique. Framebuffer EFI/GOP, simple framebuffer, transfert de console, sélection boot VGA et `vga_switcheroo` doivent être distingués d’une écriture du registre DEVEN. Un fond GRUB ou une adresse framebuffer conservée ne prouvent pas la visibilité PCI du GPU.

## 5. EFI/ACPI : auteur matériel et déclencheur logiciel peuvent différer

### Fin de GRUB et passage EFI

Le fragment local `/etc/grub.d/47_jarvis_t2_egpu_np32_pref512` contient `load_video`, modules de lecture disque, `linux` et `initrd` ; aucune commande `setpci`, `apple_set_os` ou `chainloader` dans ce fragment. Le fichier actif `/boot/grub/grub.cfg` est inaccessible ici. Le fichier généré archivé en 04N ne présente pas de correspondance pour ces commandes. Ces éléments n’auditent pas le binaire EFI effectivement lancé, ses patches Debian, sa configuration incorporée ni toute sa chaîne.

Après la console, GRUB charge le noyau/initrd et prépare la vidéo et le transfert. Le [chargeur EFI GRUB 2.12](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/loader/efi/linux.c) et le [stub EFI x86 Linux](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/firmware/efi/libstub/x86-stub.c) sont à distinguer du noyau principal. Le chemin exact exécuté localement doit être établi ; on ne suppose pas que tous les mécanismes présents dans les sources s’exécutent à chaque boot.

Dans le chemin stub examiné, préparation graphique et PCI précèdent `exit_boot()` puis l’entrée noyau. Le [helper EFI](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/firmware/efi/libstub/efi-stub-helper.c) appelle ExitBootServices ; son éventuelle protection DMA désactive le bus mastering de ponts PCI, ce qui est un autre registre et une autre fonction que DEVEN. Le [code PCI EFI correspondant](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/firmware/efi/libstub/pci.c) doit être contrôlé dans l’arbre exact avant toute conclusion sur le binaire.

La [spécification UEFI, ExitBootServices et groupes d’événements](https://uefi.org/specs/UEFI/2.10/07_Services_Boot_Services.html) prévoit des notifications firmware lors du transfert. Un callback Apple peut donc intervenir **après la lecture GRUB**, y compris lorsque l’appelant est du code Linux EFI. La fin des Boot Services ne supprime pas le SMM. Aucun callback Apple écrivant DEVEN n’a été observé : c’est une hypothèse mécanistique, pas une preuve.

### Initialisation ACPI et SMM

Dans la DSDT **archivée 04R**, `PCI0` expose `OperationRegion(HBUS, PCI_Config, Zero, 0x100)`. À `Offset(0x54)`, seul `D0EN`, **un bit**, est déclaré ; son nom apparaît une seule fois. Aucun champ D2EN/D3EN ni écriture correspondante n’a été identifié dans les trois désassemblages 04R consultés. Les autres offsets `54h` dans des régions différentes ne sont pas automatiquement DEVEN. Cela n’exclut ni AML dynamique/indirecte, ni les SSDT non examinées, ni du code SMM propriétaire.

La même DSDT déclare une région SystemIO `0xB2`, champs SSMP/SSMY, et des choix OSYS via `_OSI`. Le FADT **04R** contient `SMI_CMD=0xb2`, `ACPI_ENABLE=0xf0`, `ACPI_DISABLE=0xf1`. Ces valeurs ont été décodées hors ligne. La table FADT actuelle n’est pas lisible ici.

Le [code ACPICA acpi_hw_set_mode](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/acpi/acpica/hwacpi.c) peut écrire ACPI_ENABLE au port SMI_CMD lors d’un changement de mode. Ce chemin peut déclencher un traitement firmware opaque. **La présence de ces champs ne prouve pas que Linux a effectué cette transition dans 04U** : il faut vérifier notamment l’état SCI_EN préalable et le chemin exécuté. SMM peut également être déclenché autrement.

Linux sur Apple configure [la réponse `_OSI(Darwin)` via DMI](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/acpi/osi.c). C’est confirmé dans les journaux 04O/P ; proposer simplement « ajouter Darwin » sans preuve manquerait cette configuration existante. `_OSI` est une interrogation AML après lancement du noyau, tandis que le protocole EFI Apple Set OS est pré-Linux : deux mécanismes différents.

Le [programme apple_set_os original](https://github.com/0xbb/apple_set_os.efi/blob/master/apple_set_os.c) appelle un protocole firmware pour annoncer version et fournisseur OS. Son [cas documenté](https://github.com/0xbb/apple_set_os.efi/blob/master/README.md) est un MacBookPro11,3, pas ce Macmini8,1. Il démontre une possibilité historique de politique graphique Apple dépendant de l’identité OS, sans fournir une correction validée ici. Aucun appel, copie ou installation de ce programme proposé comme action immédiate.

## 6. Thunderbolt/eGPU et adaptations T2Linux

La comparaison 04O/P/04S suggère que **la présence avant le transfert de boot**, et non la simple coexistence PCI Linux, est la condition pertinente. Elle peut modifier l’état firmware, les tunnels, la sélection graphique, le calendrier des événements ou une branche ACPI. Détection du Core sous Linux après plusieurs secondes ne prouve pas qu’il était invisible à EFI auparavant. La disparition simultanée de D2EN et D3EN suggère éventuellement une politique de plateforme, mais ne permet pas d’identifier son code.

Les quirks Thunderbolt Apple examinés dans `drivers/pci/quirks.c` incluent un arrêt du contrôleur Cactus Ridge en **suspend_late**, avec conditions de contrôleur et méthodes ACPI. Ce chemin n’est pas une explication établie d’un démarrage normal ni un quirk DEVEN Coffee Lake. Le scan/tunnel Thunderbolt et les réserves NP/PREF peuvent influencer indirectement un firmware ; aucun effet direct sur DEVEN n’est identifié.

Adaptations pertinentes consultées dans le [dépôt T2Linux](https://github.com/t2linux/linux-t2-patches) :

| Patch public consulté | Portée | Pertinence pour ce masquage |
|---|---|---|
| [2008 i915 quatre voies MBP15,1](https://raw.githubusercontent.com/t2linux/linux-t2-patches/master/2008-i915-4-lane-quirk-for-mbp15-1.patch) | Quirk DDI A, entrée GPU/subsystem MacBookPro15,1 | Configuration de lien après détection GPU ; pas une écriture DEVEN identifiée |
| [2009 apple-gmux](https://raw.githubusercontent.com/t2linux/linux-t2-patches/master/2009-apple-gmux-allow-switching-to-igpu-at-probe.patch) | `force_igd`, gmux, vgaarb et report de sonde | Recherche d’un iGPU déjà présent ; option par défaut fausse. Aucun gmux chargé ici ; présence physique d’un gmux non établie |
| [9001 ACPI CPU T2](https://raw.githubusercontent.com/t2linux/linux-t2-patches/master/9001-ACPI-x86-Apple-T2-systems-need-early-CPU-offlining.patch) | Notifiers de suspension/reprise et CPUs secondaires | Pas un chemin démontré de boot initial masquant le pont hôte |

Le [script de construction Debian/Ubuntu T2](https://raw.githubusercontent.com/t2linux/T2-Debian-and-Ubuntu-Kernel/Mainline/build.sh) applique des patches au noyau stable. **Les branches publiques consultées sont mobiles et ne prouvent pas la liste utilisée le 25 septembre pour ce paquet.** Le changelog local dit seulement « Custom built Linux kernel ». Headers et configuration ne remplacent pas les sources complètes. Config locale : EFI_STUB, ACPI, PCI_QUIRKS, KPROBES, FUNCTION_TRACER activés ; APPLE_GMUX et I915 en modules.

Conclusion limitée : des adaptations graphiques/ACPI existent dans T2Linux, mais aucun chemin consulté ne justifie une désactivation volontaire D2EN/D3EN sur ce Mac mini. Pour l’exclure rigoureusement, récupérer en lecture seule l’arbre **et les commits de patches exacts** du paquet, identifier les fixups applicables à `8086:3ec4`, puis auditer les accès PCI/EFI/ACPI avec leur contexte. Aucune installation ni compilation effectuée.

## 7. Hypothèses classées et critères de discrimination

| Priorité | Hypothèse | Arguments | Preuve manquante |
|---|---|---|---|
| 1, plausible | Callback/politique firmware à la fin de GRUB ou dans le transfert EFI | GRUB encore à 3f ; condition Core pré-boot ; notifications EFI possibles | Mesures avant/après ExitBootServices dans le même transfert |
| 1, plausible | Linux déclenche une action firmware via ACPI/SMI/SMM | Interface SMI et chemins ACPI réels dans les archives | Première lecture Linux avant ACPI, lectures encadrant activation/méthodes et événement déclencheur |
| 2, ouverte | Écriture directe d’un chemin noyau/T2 très précoce | Capacité générale d’écrire PCI, arbre exact non audité | Accès à 54h ou alias avec pile d’appel et identité du pont hôte |
| 2, ouverte | Finalisation GRUB, vidéo ou protocole EFI spécifique | La mesure à la console précède chargement et lancement | Lecture après linux/initrd puis instrumentation du dernier transfert |
| 3, moins étayée | Événement firmware asynchrone / état hérité / délai | Deux lectures ne couvrent qu’un intervalle court | Réplication avec durées et type de mise sous tension contrôlés |
| 3, faible comme cause directe | Réallocation BAR/fenêtres Thunderbolt | Paramètres globaux ; état initial variable historiquement | Écriture DEVEN identifiée ou transition encadrée pendant cette phase |
| Faible | i915, vgaarb, pilote NVIDIA ou SDDM retire Intel | Aucun pilote graphique actuellement ; hotplug 04P conservait Intel | Preuve Intel énuméré puis écriture/retrait dans 04U |

L’ancien diagnostic « firmware avant Linux » doit être précisé : **avant la lecture GRUB, D2EN n’est pas masqué dans cet essai**. Firmware tardif reste possible. Inversement, « après GRUB » ne signifie pas automatiquement « Linux écrit DEVEN ». Un appel Linux peut déclencher un auteur firmware ; une simple lecture Linux tardive ne les départage pas.

## 8. Mesures plus précoces étudiées, sans exécution

| Méthode future | Information | Limites / retour arrière |
|---|---|---|
| Lecture GRUB dans une copie éditée en RAM de l’entrée, après `linux` et `initrd`, juste avant `boot` | Sépare chargement/préparation de la phase de lancement | Autorisation explicite de l’édition temporaire requise ; aucune sauvegarde. Reste avant finalisation vidéo/transfert réel ; ne permet pas une lecture après ExitBootServices |
| Arrêt initramfs prévu par l’initramfs installé, lecture DEVEN | Borne avant services utilisateurs, éventuellement avant certaines sondes modulaires | Noyau PCI/ACPI déjà initialisé ; option exacte et outil disponible à auditer ; réseau/initramfs non garanti. Pas une mesure t=0 |
| `initcall_debug`, journal plus verbeux, trace PCI au boot | Ordonne initcalls/fixups, peut identifier écritures noyau après activation de la trace | Changement cmdline autorisé séparément ; paramètres ne lisent pas DEVEN automatiquement et ne couvrent pas SMM/EFI ni forcément les accès très précoces |
| Noyau diagnostique avec lectures ciblées dans early x86/setup_arch, avant/après ACPI et scan PCI | Borne le premier changement dans Linux | Nouvelle construction/entrée nécessitant autorisation ; conserver noyau/initrd de référence. Aucun module tardif ne remplace cette instrumentation |
| Instrumentation EFI stub avant/après ExitBootServices, collecte en RAM | Sépare état avant sortie EFI et état à l’entrée noyau | Nouveau binaire à auditer. Après sortie, ne plus utiliser console/protocoles Boot Services ; publier le buffer une fois Linux prêt |
| Trace des écritures PCI avec valeur, largeur, BDF, offset et pile | Peut prouver un auteur noyau direct | Surveiller tous les chemins pertinents, y compris bruts/ECAM ; absence dans la trace n’exclut SMM, écritures MMIO aliasées ou période non instrumentée |

Mesure cible : identité `3ec48086` et DEVEN 32 bits au même BDF à chaque jalon. Utiliser des helpers de lecture adaptés au stade, sans sonde destructive de BAR, réactivation, rescan ou lecture improvisée `/dev/mem`. D2EN masqué ne gêne pas une lecture du pont hôte qui reste présent. Enregistrer statut d’accès et longueur ; une erreur ou `ffffffff` n’est pas un état DEVEN valide.

Jalons idéaux : G0 console GRUB ; G1 après chargement noyau/initrd ; E0 juste avant ExitBootServices ; E1 juste après ; K0 première phase x86 ; K1 avant/après ACPI ; K2 avant/après scan racine ; K3 avant pilotes ; L état SSH. Les jalons sont une **carte de mesure**, pas une chronologie du chemin local déjà prouvée. Conserver les résultats en mémoire réservée et les exporter plus tard avec boot ID ; éviter un printk/console susceptible de modifier le chemin EFI ou de disparaître avec l’affichage.

## 9. Prochaine expérience recommandée et correction progressive

**Étape documentaire effectuée : les deux captures 04U sont analysées au §2. Intel manque dès le scan initial.** La prochaine expérience doit donc privilégier les jalons de fin GRUB, transfert EFI et début Linux avant/après ACPI ; une collecte initramfs seule arriverait après le symptôme déjà observé.

**Premier nouvel essai proposé, uniquement après autorisation :** conserver Core connecté, mêmes paramètres et même procédure de mise sous tension ; mesurer VID/DID et DEVEN après chargement de `linux`/`initrd` dans l’entrée NP32/PREF512 éditée uniquement en RAM, immédiatement avant `boot`. Conserver les mesures console initiales et celles Linux, les délais et des photographies externes. Le texte temporaire doit être préparé et revu avant l’accord ; ne pas réécrire à la main une cmdline approximative. Aucun changement persistant de GRUB/EFI. Cet essai requiert un redémarrage et une édition temporaire actuellement interdits : **il n’est pas autorisé par ce rapport**.

- G1=`0f` : transition déjà pendant préparation/chargement ou événement asynchrone ; instrumenter GRUB/protocoles firmware et reproduire avec délais contrôlés.
- G1=`3f`, Linux=`0f` : concentrer l’instrumentation sur transfert EFI et début Linux ; ce résultat ne départage toujours pas firmware et noyau.
- Première lecture après ExitBootServices=`0f` : rechercher transfert EFI/firmware ; si elle vaut `3f` et K1 devient `0f`, encadrer ACPI/quirks.
- Trace montrant une écriture noyau couvrant 54h avec transition : examiner son appelant, son quirk et la provenance du patch avant de corriger.

Protocole de correction proposé, après localisation et accords séparés :

1. **Figer la référence** : noyau/initrd/GRUB existants, empreintes, cmdline, type de démarrage, port Core, écran et réseau indépendant. Définir réussite : D2EN conservé, Intel visible dès scan, i915/DRM/greeter fonctionnels, SSH et stockage conservés ; absence de régression d’allocation eGPU.
2. **Contournement opérationnel de référence** : le démarrage sans Core puis hotplug a fonctionné en 04O/P et le retour sans Core en 04S. Toute utilisation future nécessite l’autorisation d’arrêt/changement physique. Ce contournement ne corrige pas le boot Core présent.
3. **Si auteur noyau identifié** : préparer un correctif minimal de la condition fautive ou de son patch dans un noyau alternatif, sans remplacer la référence. Tester une seule variation ; retour par sélection manuelle du noyau initial. Une autre version déjà installée peut constituer un contrôle distinct, mais ajoute des différences T2 et ne valide pas seule un correctif.
4. **Si mécanisme ACPI identifié** : envisager seulement une variation ciblée et temporaire de l’interface concernée, avec contrôle mémoire/PCI/réseau. Pas de `acpi=off` général comme correction proposée ; `_OSI(Darwin)` est déjà honoré historiquement. Retour à la cmdline initiale au boot suivant.
5. **Si callback/protocole EFI identifié** : préparer un essai d’identification OS ou de chemin de transfert adapté à ce Macmini8,1, audité et réversible. Le précédent apple_set_os sur MacBook ne suffit pas à autoriser son usage. Conserver chargeur/entrée EFI existants ; ne pas changer NVRAM ni politiques Apple pour l’essai initial.
6. **Valider puis seulement envisager la persistance** : plusieurs essais contrôlés, aucune écriture DEVEN de secours, aucun rescan, aucun chargement forcé i915. Une réussite ponctuelle ne justifie pas une modification persistante immédiate.

Arrêter la série en cas de perte SSH indépendante, erreur stockage, état DEVEN inattendu ou impossibilité de revenir à la référence. Le retour arrière d’un essai de boot implique lui-même un arrêt/redémarrage autorisé et un opérateur local ; il n’existe pas de retour arrière instantané par SSH à GRUB. Avec les restrictions actuelles, le retour arrière est simplement de **ne lancer aucun essai** et de conserver le système présent.

**Journal 04U analysé et rapport complété. Attente d’autorisation avant toute instrumentation, expérimentation de boot ou correction. L’attribution exacte de l’écriture demeure non démontrée et nécessite les mesures supplémentaires proposées.**

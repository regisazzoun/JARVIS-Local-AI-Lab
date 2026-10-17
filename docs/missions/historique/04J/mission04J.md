> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission04J.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 04J : vérification avant branchement

**D — Test non concluant : données hôte manquantes. NE PAS brancher le Razer Core.** Les fenêtres PCIe effectivement accessibles restent insuffisantes et inchangées ; le constat local correspond à une réserve inefficace, mais la validation complète du nouveau démarrage est empêchée par l’isolation.

Collecte du 2026-10-11T21:44:01.884487+02:00. Boot ID : `[UUID EXPURGÉ]`. Contrôles système en lecture seule ; seules les preuves et ce rapport sont écrits dans le dossier utilisateur. Aucun paramètre modifié, module chargé, pilote installé, redémarrage ou action sur le Core.

## 1. Noyau et arguments

Noyau confirmé : `6.18.54-1-t2-trixie`. Les six arguments sont présents exactement : `intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M`.

Ligne active :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M
```

La présence du paramètre confirme sa transmission, pas une réserve effective.

## 2. Limites précises d’accès

`sudo -n id` échoue : `/etc/sudo.conf` vu avec uid 65534 et flag « no new privileges ». CapEff/CapBnd nuls, NoNewPrivs=1. Aucune élévation hôte possible par l’outil disponible ; pas de tentative de contourner l’isolation. `lspci -Dnnvvk` lit les fenêtres mais les capacités indiquent `<access denied>`. Les ressources sysfs sont accessibles et corroborent les plages ; `/proc/iomem` masque toutes les adresses à zéro, donc la couverture par les apertures racines et les conflits globaux ne sont pas vérifiables.

`dmesg` : Operation not permitted. `journalctl -b -k` : aucune entrée et avertissement de visibilité restreinte ; ce n’est pas un journal noyau vide démontré. `journalctl -b` fournit uniquement des journaux accessibles utilisateur, pas le journal système complet. Les premières tentatives avec UUID comportant des tirets ont donné Invalid argument ; les tentatives corrigées `-b` sont archivées et font foi.

`systemctl` et `loginctl` : bus système interdit. `boltctl` : D-Bus interdit. `ip address`/`ip route` et `ss` : netlink interdit ; les tableaux vides de ss, malgré son code 0, ne démontrent pas une absence de sockets. La vue `ps` ne permet pas de valider les processus hôte SSH/GDM.

## 3. Graphique, réseau et stockage

Nouveau absent de `/proc/modules` et aucun périphérique PCI visible lié à Nouveau. i915 chargé, Intel UHD 630 `0000:00:02.0` lié à i915, boot_vga=1. Les journaux GNOME accessibles confirment card0 i915 en atomic mode setting et sélection du Boot VGA GPU comme principal. DP-3 connected/enabled. GNOME Wayland atteint graphical-session.target à 21:40:31 ; réactivité du bureau et service display-manager non vérifiés directement.

Ethernet `enp4s0` : operstate up, carrier=1, 1000 Mbit/s ; contrôleur 04:00.0 lié à tg3. Adresse IP, routes, service SSH, écoute et connexions SSH **non vérifiables** dans cet environnement.

NVMe : contrôleur Apple ANS2 02:00.0 lié à nvme, `nvme0` state=live, APPLE SSD AP0512M. `nvme0n1` 465,9 Gio et partitions p1/p2/p3 visibles ; /boot/efi et /boot visibles dans lsblk. Santé SMART, absence de reset/timeout et état complet LVM/racine hôte non établis par cette collecte.

## 4. Core et GPU

Aucun 10de:1eb0 ni autre périphérique NVIDIA dans le PCI visible. Les ponts externes 7f:00.0 et 80:01.0 de 04H sont absents ; la branche 7c:01.0 est vide. Thunderbolt sysfs ne montre que domain0/domain1 et les routeurs hôtes 0-0/1-0 Macintosh, aucun Core 1-1. Ces constats sont cohérents avec le débranchement indiqué par l’utilisateur ; **ils ne constituent pas une confirmation physique indépendante depuis un accès hôte privilégié**. Bolt n’est pas consultable.

## 5. Fenêtres préchargeables actuelles

Adresses inclusives ; Mio = 1048576 octets. Type annoncé par lspci ; plages et tailles corroborées par sysfs. Les NHI sont des endpoints, pas des ponts : 07:00.0 et 7d:00.0 sont liés à thunderbolt et leurs BAR sont non préchargeables (256 Kio + 4 Kio), pas des réserves GPU.

| Pont | Type de fenêtre | Adresse | Mio | Couverture par parent immédiat |
|---|---|---|---:|---|
| 0000:00:01.1 | 32 bits | `0xb1400000–0xbf3fffff` | 224 | racine hôte : iomem masqué |
| 0000:00:01.2 | 32 bits | `0xbf400000–0xcd3fffff` | 224 | racine hôte : iomem masqué |
| 0000:05:00.0 | 32 bits | `0xb1400000–0xbf3fffff` | 224 | 0000:00:01.1 : oui |
| 0000:06:00.0 | 64 bits annoncés, désactivée | aucune | 0 | sans fenêtre active |
| 0000:06:01.0 | 32 bits | `0xb1400000–0xb83fffff` | 112 | 0000:05:00.0 : oui |
| 0000:06:02.0 | 64 bits annoncés, désactivée | aucune | 0 | sans fenêtre active |
| 0000:06:04.0 | 32 bits | `0xb8400000–0xbf3fffff` | 112 | 0000:05:00.0 : oui |
| 0000:7b:00.0 | 32 bits | `0xbf400000–0xcd3fffff` | 224 | 0000:00:01.2 : oui |
| 0000:7c:00.0 | 64 bits annoncés, désactivée | aucune | 0 | sans fenêtre active |
| 0000:7c:01.0 | 32 bits | `0xbf400000–0xc63fffff` | 112 | 0000:7b:00.0 : oui |
| 0000:7c:02.0 | 64 bits annoncés, désactivée | aucune | 0 | sans fenêtre active |
| 0000:7c:04.0 | 32 bits | `0xc6400000–0xcd3fffff` | 112 | 0000:7b:00.0 : oui |

Les inclusions immédiates démontrées remontent donc les branches actives jusqu’à 00:01.1/00:01.2. La couverture par l’aperture racine hôte reste inconnue, car iomem est masqué. Un type 64 bits affiché sur une fenêtre désactivée n’est pas une fenêtre 64 bits attribuée. Les fenêtres actives de la chaîne du Core restent 32 bits ; des BAR GPU 64 bits peuvent être placés sous 4 Gio, mais uniquement si la plage et l’alignement le permettent.

## 6. Tableau AVANT/APRÈS

Sources AVANT : rapports 04H et 04I, comparaison 04E archivée. Boot 04E `[UUID EXPURGÉ]` ; 04H `[UUID EXPURGÉ]`. AVANT avec Core connecté, APRÈS sans Core selon utilisateur et vue accessible : l’absence des ponts externes ne se compare pas à une fenêtre désactivée sur un pont présent.

| Critère | AVANT 04E | AVANT 04H | APRÈS 04J |
|---|---|---|---|
| realloc / réserve 512M | sans / sans | avec / sans | avec / avec dans cmdline |
| 00:01.2 préchargeable | bf400000–cd3fffff, 224 Mio | identique | identique, 32 bits |
| 7b:00.0 préchargeable | bf400000–cd3fffff, 224 Mio | identique | identique, 32 bits |
| 7c:01.0 préchargeable | bf400000–c63fffff, 112 Mio | identique | identique, 32 bits |
| 7f:00.0 préchargeable | c0000000–c63fffff, 100 Mio | identique | pont externe absent de la vue |
| 80:01.0 préchargeable | absente, pont présent | identique | pont externe absent de la vue |
| NP 00:01.2 et 7b:00.0 | 8f900000–9dafffff, 226 Mio | 8fa00000–9dbfffff, 226 Mio | identique à 04H |
| NP 7c:01.0 | 8fb00000–96afffff, 112 Mio | 8fc00000–96bfffff, 112 Mio | identique à 04H |
| BAR 1 / BAR 3 GPU | 256 / 32 Mio non attribués | identique | GPU absent, attribution non testée |
| Journaux allocation / stabilité | accessibles dans archives | accessibles dans archives | noyau/système/SSH incomplets |

## 7. Réserve utilisable et alignement

Aucune fenêtre préchargeable de 512 Mio n’est attribuée dans les ponts Thunderbolt relevés. Sur la chaîne cible visible `00:01.2 → 7b:00.0 → 7c:01.0`, aucun agrandissement n’est observé. Les 224 Mio amont et 112 Mio aval sont inférieurs au seul BAR 1 de 256 Mio. On ne peut pas additionner les deux fenêtres de 112 Mio de branches sœurs pour y placer un BAR contigu.

BAR 1 exige un début aligné sur `0x10000000`. Dans `0xbf400000–0xcd3fffff`, le premier est `0xc0000000` ; fin requise `0xcfffffff`, au-delà de `0xcd3fffff` (212 Mio disponibles depuis ce début). Sur 7c:01.0, même début, fin requise au-delà de `0xc63fffff` (100 Mio disponibles depuis ce début). BAR 1 ne tient donc dans aucun de ces parents, même avant de considérer BAR 3.

BAR 3 de 32 Mio, alignée sur `0x02000000`, pourrait isolément tenir par exemple à `0xc0000000–0xc1ffffff`, mais cela n’établit aucun placement simultané avec BAR 1. Besoin minimal combiné : 288 Mio, plus contraintes des autres fonctions. Exemple arithmétique de placement dans une hypothétique plage convenable : BAR 1 c0000000–cfffffff, BAR 3 d0000000–d1ffffff ; cette seconde plage est aussi hors des fenêtres relevées. Ce n’est pas une allocation effectuée ni une recommandation d’écriture.

La réserve effective n’est donc pas démontrée ; **les fenêtres présentes ne permettent pas le placement demandé**. Le mécanisme exact de non-agrandissement ne peut pas être diagnostiqué sans journal noyau et accès privilégié.

## 8. Erreurs du nouveau démarrage

Allocation PCIe, AER, DPC, ACPI, DMAR/IOMMU, Thunderbolt et NVMe : recherche noyau empêchée par dmesg interdit et journal noyau invisible. Aucune conclusion d’absence d’erreurs ou de régression n’est possible. Les journaux utilisateur montrent GNOME démarré et des avertissements de session, dont erreur d’enregistrement auprès de GDM ; ils ne permettent pas d’attribuer une régression au paramètre PCIe ni de valider le service GDM.

## 9. Preuves et décision

Dossier preuves (référence locale historique non publiée), commandes, stdout/stderr et codes conservés en JSON ; PCI complet, arbre, ressources sysfs, modules, périphériques, journaux restreints et échecs d’accès. Références 04H/04I et extraits 04E copiés dans ce dossier. Empreintes SHA256SUMS ; archive tar.gz et empreinte séparée à côté du dossier. Boot ID relu en fin de collecte.

**Conclusion obligatoire : D — Test non concluant : données manquantes pour la vérification hôte complète.** Constat des fenêtres accessibles : réserve inefficace, goulets 224/112 Mio inchangés ; aucun élément en faveur de A ou B. **NE PAS brancher le Razer Core**, les fenêtres relevées sont insuffisantes et l’absence de régression n’a pas pu être contrôlée. Rapport terminé dans les limites documentées ; attente de la décision utilisateur, aucune étape de branchement engagée.

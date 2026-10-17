> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission04L.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 04L : préparation de la réallocation PCIe ciblée

## Complément — Installation autorisée avant redémarrage

**Installation terminée et vérifiée à 2026-10-11T22:16:56.454294+02:00. Autorisation reçue : « procede au modification du kernel et du grub et tt autre fichier avant redemarrage et test ». Aucun redémarrage ni test matériel effectué.** Ce complément décrit l’état actuel ; l’étude conservée plus bas décrit la préparation antérieure à l’installation.

### Modification installée

Nouvelle entrée : **JARVIS — T2 eGPU réallocation ciblée PCIe**, ID `jarvis-t2-egpu-reallocation-ciblee`. Source `/etc/grub.d/46_jarvis_t2_egpu_reallocation_ciblee`, root:root 0755. `/boot/grub/grub.cfg` mis à jour avec un ajout strictement limité au bloc 46, mode root:root 0600 conservé.

Le noyau déjà installé prend en charge le mécanisme : la modification porte sur les paramètres de son démarrage. Image `6.18.54-1-t2-trixie` et son initramfs inchangés ; aucun patch ou recompilation requis, aucun initramfs régénéré. La nouvelle entrée contient :

```text
linux /vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M 'pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0'
initrd /initrd.img-6.18.54-1-t2-trixie
```

Les guillemets protègent les points-virgules dans GRUB. Au démarrage via cette entrée, Linux doit recevoir la liste entière. Aucun changement global de la ligne de commande, i915, VFIO, modules, ACPI ou EFI. Aucun service, règle udev, sélection automatique ou action de branchement ajouté.

### Contrôles de l’installation

Candidat généré dans un espace de montage privé : racine, /boot et /run en lecture seule ; copies locales des sources GRUB, comparaison du cache thème au lieu de sa réécriture, temporaires et verrous LVM locaux. La génération contrôlée retourne 0 ; `grub-script-check` réussit sur le candidat puis sur le GRUB installé. Le fichier installé est identique au candidat généré. Diff vérifié : **seul le nouveau bloc 46 apparaît**.

**31 autres fichiers protégés ont les mêmes empreintes**, notamment toutes les images noyau/initramfs des trois versions, grubenv, les sources existantes et la configuration du menu. SHA-256 GRUB avant : `81be6b6101d1916fb9c62de50444959ee19b8a3dbbf714c8eb9c368f2919054d` ; après : `f770d88776a678b6a23880afb63b3c515e80bfdd43aff2c7d26ce49d56f3b97e`. Source 46 : `f70a056431638a92cf3c18c37760a25a7db7b7efcbccaeb4a18869234b3c262d`.

Le menu reste visible 15 secondes et **Debian 6.12.111 demeure le choix par défaut**. Diagnostic T2 sans Nouveau, entrée realloc seule, réserve 512M, Debian 6.12.111 et 6.12.107 restent disponibles. Aucun next_entry programmé.

Boot ID après installation : `[UUID EXPURGÉ]`, identique. Le noyau en cours ne reçoit pas rétroactivement `resource_alignment` : **le candidat n’est pas actif et son efficacité n’a pas été testée**. Core toujours disconnected dans Bolt, aucune NVIDIA en PCI ; i915 lié à Intel primaire, display-manager et SSH/service/socket actifs, Ethernet UP, SSD présent. Collecte après dans `hote-[UUID EXPURGÉ]-20261011-221729/`. Cela confirme l’état avant redémarrage, pas celui du futur essai.

### Prochain essai, encore à autoriser

Pour un futur essai autorisé, sélectionner manuellement **JARVIS — T2 eGPU réallocation ciblée PCIe** dans le menu, sans édition supplémentaire. Cela remplace la saisie ponctuelle décrite dans la préparation initiale. **Laisser le Core déconnecté.** Disposer d’une console Intel et d’un clavier direct avant le redémarrage ; aucune activation par défaut.

Après boot, suivre les critères de la section 9 : nouveau boot ID, paramètre complet, collecte privilégiée, fenêtres et registres NP/PREF, couverture de chaque parent et de tous les descendants, réserve PREF libre contiguë de 512 Mio et placement aligné de 256 + 32 Mio, NP suffisant, i915/SSD/Ethernet et nouvelle connexion SSH, journaux complets et stabilité. La branche sœur basse demeure un risque de blocage. Toute insuffisance, incohérence ou régression implique **NE PAS brancher le Razer Core**. Une validation sans Core ne vaut pas autorisation de branchement.

### Retour arrière préparé

Premier retour : choisir manuellement **JARVIS — T2 eGPU diagnostic sans Nouveau**, sans le nouveau paramètre. Debian 6.12.111 puis 6.12.107 restent les secours détaillés plus bas. Le redémarrage et toute action physique restent à autoriser.

Pour retirer ensuite l’installation persistante si demandé, le script `installation-20261011-221528/retour-arriere.py` restaure le GRUB antérieur et retire uniquement la source 46. **Il est préparé mais non exécuté.** Il vérifie les empreintes du GRUB, de la source et des fichiers protégés avant d’agir ; si le système a évolué, il refuse et le retour doit être réexaminé. Il ne redémarre pas. Sauvegarde du GRUB antérieur et des configurations dans `installation-20261011-221528/sauvegarde/`, plus `grub.cfg-avant`.

Preuves : `installation-20261011-221528/` contient source candidate, GRUB généré, diff, validation syntaxique, empreintes avant, résultat d’installation et contrôles après. L’archive de la préparation initiale est conservée séparément ; l’archive courante inclut ce complément et les nouvelles preuves.

**Les modifications de démarrage autorisées sont installées. Aucun test exécuté ; attente de la décision utilisateur pour le redémarrage sans Core.**

---

## Étude initiale de préparation — état avant installation

**11 octobre 2026 — Préparation terminée, paramètre reconnu dans le noyau installé ; essai non appliqué et non autorisé.** La ligne temporaire est prête et sa syntaxe GRUB vérifiée sur une copie locale. La possibilité d’une allocation haute est réelle du point de vue des apertures et des types des trois ponts, mais son succès demeure incertain : les fenêtres des descendants non ciblés, notamment 7c:04.0, peuvent empêcher le déplacement des parents. Aucun branchement du Core n’est admissible sur les fenêtres actuelles.

## 1. Périmètre, accès et preuves

Mission 04K reprise, puis nouvelle collecte privilégiée à **22:02:56 CEST**. `sudo -n` réussit avec uid=0, sans contournement de l’environnement. Noyau actif `6.18.54-1-t2-trixie`, boot ID `[UUID EXPURGÉ]`, inchangé. ACPI, journaux noyau/système/Bolt, iomem, sysfs PCI et configuration brute accessibles. Les limites d’accès qui affectaient la première étude 04K ne s’appliquent donc plus à cette collecte.

Dossier : mission04L-preparation (référence locale historique non publiée). Capture hôte : `hote-[UUID EXPURGÉ]-20261011-220256/`. Commandes, sorties, erreurs et codes conservés. Une copie du collecteur et un analyseur hors ligne permettent la comparaison au futur boot.

Aucun changement GRUB, EFI, ACPI, VFIO, i915 ou réglage noyau ; aucun module chargé par la mission, aucune écriture de configuration PCI, aucun retrait/rescan, branchement ou redémarrage. Seuls les rapports, copies et outils d’analyse sont écrits dans le dossier utilisateur. `iasl` absent du système : paquet Debian téléchargé puis **extrait localement**, sans installation ni modification de la base des paquets. Son désassembleur travaille sur des copies de tables ; aucune méthode ACPI n’est invoquée à nouveau sur le matériel.

## 2. Vérification dans le binaire réellement installé

L’image `/boot/vmlinuz-6.18.54-1-t2-trixie` a été extraite avec le script fourni par ses headers. Analyse statique uniquement : aucune exécution du code noyau extrait.

| Élément | Preuve |
|---|---|
| SHA-256 image installée | `a41e1a7680c5d76761a744d4265b7901bbd7494e90340fda1eb59eec73d72d1b` |
| SHA-256 ELF extrait | `120964b4ad696997873e737756f0240d7c7e64cfa726fc34bb91f186c7c855e1` |
| Configuration | X86_64, PCI, PCI_DOMAINS, PCI_IOV, ACPI activés ; pages de 4 Kio |
| Entrée parser | `pci_setup` à `0xffffffff833b8cc0` |
| Chaîne effective | `resource_alignment=` à `0xffffffff825b32bf` |
| Variable recevant la valeur | `resource_alignment_param`, `0xffffffff838e7210` |
| Fonction effectrice | `pci_reassigndev_resource_alignment`, `0xffffffff81a47420` |

Le désassemblage de `pci_setup` compare **19 octets**, avance de 19 et stocke la valeur restante dans la variable. Dans la fonction effectrice, l’absence d’un ordre suivi de `@` sélectionne l’ordre **12**, donc 4096 octets. Le parser accepte le séparateur `;` (0x3b). `pci_dev_str_match` contient le format `%x:%x:%x.%x%c`, qui prend en charge les BDF avec domaine ; le format sans domaine est également présent. Les identités 0000:00:01.2, 0000:7b:00.0 et 0000:7c:01.0 existent et correspondent à la topologie actuelle. L’appel depuis `pci_device_add` est confirmé à `0xffffffff81a3bc24`, lors de l’énumération et avant la liaison normale des pilotes.

**Conclusion syntaxique :** la liste exacte demandée et les arguments `pci=` séparés sont pris en charge dans cette image. L’absence d’ordre explicite ne demande pas un alignement de 512 Mio ; elle sélectionne le mécanisme de réaffectation avec l’alignement par défaut. L’interface `/sys/bus/pci/resource_alignment` est actuellement vide, et le candidat n’apparaît pas dans cmdline. Cette preuve établit la disponibilité du chemin, pas son résultat d’allocation.

Désassemblages bruts et annotés, chaînes du parser et empreintes conservés dans `sources/`. Le code stable est une référence complémentaire, distincte de la preuve du binaire T2 : [pci.c Linux 6.18.54](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/pci/pci.c), [probe.c](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/pci/probe.c).

## 3. ACPI _CRS et apertures du boot actuel

21 tables ACPI copiées. DSDT et 13 SSDT désassemblées individuellement avec `iasl` 20250404, code 0. La tentative de désassemblage en namespace commun échoue sur des noms déjà existants ; son erreur est conservée. Les fichiers individuels peuvent conserver des références externes et ne constituent pas une réévaluation intégrale de l’AML.

Dans la DSDT, `\_SB.PCI0` porte PNP0A08/PNP0A03. Son `_CRS` sérialisé retourne BUF0 après ajustement :

- aperture basse : minimum `TLUD << 20`, maximum `0xfeafffff`, longueur recalculée ;
- aperture haute QWord : longueur M64L, minimum M64B, maximum minimum + longueur − 1 ; si M64L=0, longueur nulle.

Les champs M64B/M64L sont définis dans SSDT6, dans la région firmware. Leur valeur physique n’est pas sondée via /dev/mem. Le résultat effectivement publié à Linux est corroboré par le journal du boot courant et l’iomem non masqué :

| Ressource hôte mémoire | Taille | État |
|---|---:|---|
| `000a0000–000fffff` | 384 Kio | aperture basse historique |
| `80000000–feafffff` | 2027 Mio | aperture MMIO basse partagée |
| `4000000000–7fffffffff` | 256 Gio | aperture haute annoncée et présente dans iomem |

Il ne s’agit pas d’une « table _CRS » indépendante : _CRS est une méthode de la DSDT utilisant des données firmware. L’ACPI racine fournit déjà un espace haut ; aucun besoin de modifier _CRS ou d’ignorer ACPI n’est démontré.

Le journal confirme l’emploi des fenêtres ACPI et le contrôle OS de PCIeHotplug/AER/DPC. Les erreurs _OSC/AE_AML_BUFFER_LIMIT et SSDT/AE_ALREADY_EXISTS sont présentes au boot et comparables aux références antérieures ; elles ne prouvent pas que l’aperture haute soit inutilisable. La couverture ECAM partielle est aussi conservée : MCFG est l’accès configuration, pas la réserve GPU.

## 4. Fenêtres et registres des trois ponts

Adresses inclusives ; Mio=1048576 octets. Les champs bruts de configuration et les ressources Linux concordent sur les adresses et les tailles.

| Pont | Non préchargeable, 32 bits | Préchargeable, type brut 64 bits |
|---|---|---|
| 00:01.2, Intel 8086:1909 | `8fa00000–9dbfffff`, 226 Mio | `bf400000–cd3fffff`, 224 Mio |
| 7b:00.0, DSL6540 8086:1578 | `8fa00000–9dbfffff`, 226 Mio | `bf400000–cd3fffff`, 224 Mio |
| 7c:01.0, JHL7540 8086:15ea | `8fc00000–96bfffff`, 112 Mio | `bf400000–c63fffff`, 112 Mio |

| Pont | COMMAND | NP base/limite, 0x20/0x22 | PREF base/limite, 0x24/0x26 | PREF hauts, 0x28/0x2c |
|---|---|---|---|---|
| 00:01.2 | 0x0407 | 0x8fa0 / 0x9db0 | 0xbf41 / 0xcd31 | 0 / 0 |
| 7b:00.0 | 0x0007 | 0x8fa0 / 0x9db0 | 0xbf41 / 0xcd31 | 0 / 0 |
| 7c:01.0 | 0x0407 | 0x8fc0 / 0x96b0 | 0xbf41 / 0xc631 | 0 / 0 |

Les quatre bits de type PREF valent 1 dans chaque base/limite : décodage 64 bits annoncé, actuellement programmé sous 4 Gio. La présentation lspci « 32-bit » ne doit pas supplanter ces registres, leurs flags sysfs et le journal `64bit pref`. La correction d’interprétation de 04K est confirmée.

00:01.2 et 7b:00.0 couvrent aussi 7c:00.0 (NHI 7d:00.0), 7c:02.0 (USB 7e:00.0), 7c:04.0 (branche sœur vide). Celle-ci conserve NP `96c00000–9dbfffff`, 112 Mio, et PREF `c6400000–cd3fffff`, 112 Mio. 7c:01.0 n’a aucun descendant actuellement. L’autre domaine Thunderbolt sous 00:01.1 n’est pas ciblé.

Les parents contiennent les fenêtres actuelles, sans chevauchement entre branches sœurs. Aucune réserve contiguë utile de 512 Mio ; l’intersection PREF des trois ponts reste 112 Mio. Le premier emplacement BAR 1 aligné serait c0000000–cfffffff et dépasse chacune des fenêtres bloquantes. L’analyseur hors ligne retourne donc **ARRÊT** pour la configuration actuelle, exclusivement pour réserve insuffisante et placement impossible ; ce résultat ne teste pas le candidat.

## 5. Effets exacts du candidat et descendants

Le binaire installé permet de préciser le périmètre, au-delà du nom du paramètre :

1. Pour chacun des trois ponts reconnus, le bit mémoire de COMMAND est effacé, puis les ressources mémoire locales sont examinées. Les petites ressources locales peuvent être arrondies à 4 Kio ; les BAR des endpoints non ciblés ne sont pas directement soumis à cet arrondi.
2. Les fenêtres de pont portant IORESOURCE_MEM sont marquées IORESOURCE_UNSET ; leur début devient 0 et leur fin représente la taille précédente − 1. Cela concerne **NP et PREF**, pas seulement PREF. Cette étape ne les fixe pas à 512 Mio.
3. La fonction de désactivation des fenêtres écrit les registres NP/PREF pour rendre leurs plages invalides, avant que l’allocateur ne les reconstruise. Le désassemblage montre les offsets 0x20, 0x24, 0x28 et 0x2c. Ces écritures auraient lieu lors du futur boot, et ne sont pas exécutées ici.
4. La liste ne modifie pas directement les ressources des endpoints i915/NVMe/tg3 ni les numéros de bus. Elle ne réalise pas une réallocation récursive automatique de tous les descendants. NHI/USB et ponts enfants peuvent garder des allocations firmware que les parents doivent couvrir, ou qui devront être déplacées par les passes générales.

Les fenêtres I/O ne sont pas marquées mémoire par cette boucle ; les numéros de bus ne sont pas demandés à la réaffectation. Cela ne suffit pas à garantir l’identité des BDF après un prochain boot : elle devra être vérifiée.

**Point limitant important :** si la fenêtre PREF de 7c:04.0 reste à c6400000–cd3fffff, les parents ne peuvent pas être déplacés entièrement dans l’aperture haute tout en couvrant cette enfant basse. Une seule fenêtre PREF contiguë allant du bas à l’aperture haute traverserait l’intervalle absent des apertures racines et d’autres réservations : elle n’est pas une solution valide. Il faut donc que les descendants incompatibles soient déplacés/réévalués, ou que l’allocateur trouve une solution intégralement basse suffisante. Le candidat ne garantit ni l’un ni l’autre.

NHI et USB imposent aussi leurs fenêtres NP basses. Leur conservation doit être démontrée sur chaque parent. Ne pas ajouter spontanément 7c:04.0, cibler tous les ponts Intel ou augmenter l’ordre d’alignement si le premier essai échoue.

Le mécanisme de dimensionnement peut conserver les fenêtres déjà revendiquées et traiter les suppléments hotplug comme optionnels. Cela explique pourquoi une simple demande 512M n’a pas forcé l’agrandissement ; la liste ciblée ouvre une autre voie de reconstruction, sans garantir sa réussite. [Allocateur Linux 6.18.54](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/pci/setup-bus.c).

## 6. Ressources à protéger et allocation au-dessus de 4 Gio

| Périphérique actuel | Pilote et principales ressources mémoire | Relation au ciblage |
|---|---|---|
| Intel 00:02.0 | i915 ; BAR0 `80000000–80ffffff`, BAR2 `a0000000–afffffff` | branche sœur, hors cible |
| SSD Apple 02:00.0 | nvme ; `b0000000–b03fffff`, `b1000000–b107ffff`, `b1200000–b120ffff` | sous 00:1b.0, hors cible ; autres fonctions T2 partagent son parent |
| Ethernet 04:00.0 | tg3 ; `81610000–8161ffff` et `81600000–8160ffff` | sous 00:1c.1, hors cible |
| NHI 7d:00.0 | thunderbolt ; `8fb00000–8fb3ffff`, `8fb40000–8fb40fff` | sous les deux ponts amont ciblés |
| USB Thunderbolt 7e:00.0 | xhci_hcd ; `8fa00000–8fa0ffff` | sous les deux ponts amont ciblés |
| NHI 07:00.0 / USB 08:00.0 | thunderbolt / xhci ; `81900000–81940fff` et `81800000–8180ffff` | autre domaine, hors cible |
| Intel HDA 00:1f.3 | snd_hda_intel ; `81710000–81713fff` et `4000000000–40000fffff` | hors cible, occupe déjà 1 Mio de l’aperture haute |

Le fichier `ressources-protegees.json` conserve indices, flags et plages exactes, notamment les fonctions non graphiques. Sous 4 Gio, l’espace est partagé avec ces ressources et ECAM ; une réorganisation globale augmenterait le risque.

Une allocation PREF haute est théoriquement compatible avec les trois ponts et les BAR 64 bits de la Quadro. Exemple arithmétique, **aucune adresse imposée** : fenêtre `4010000000–402fffffff` de 512 Mio, BAR1 `4010000000–401fffffff` et BAR3 `4020000000–4021ffffff`. Elle évite HDA dans l’état relevé. Le noyau doit choisir sa propre allocation ; tous les parents et branches sœurs doivent ensuite être valides. L’aperture annoncée et l’absence d’occupant enregistré sur une plage ne prouvent pas seules l’absence de périphérique firmware caché ni le routage effectif futur. IOMMU ne corrige pas une collision MMIO.

## 7. État préalable et erreurs du boot

Bolt confirme Razer Core **disconnected** ; aucun 10de:1eb0 ni autre NVIDIA en PCI. Nouveau et les modules graphiques NVIDIA sont absents de la liste chargée ; Intel i915 reste primaire. GNOME utilise card0 i915 en atomic mode setting, DP-3 actif ; display-manager actif (SDDM, pas GDM). Les messages GNOME d’enregistrement auprès de GDM ne démontrent donc pas une panne du gestionnaire réellement utilisé.

Ethernet enp4s0 UP, carrier=1, 1000 Mbit/s, [ADRESSE PRIVÉE EXPURGÉE]/24 ; SSH service/socket actifs, écoute [ADRESSE PRIVÉE EXPURGÉE]:22 et connexion authentifiée existante depuis [ADRESSE PRIVÉE EXPURGÉE]. Cela ne remplace pas une nouvelle connexion de contrôle après le futur boot.

SSD nvme0 live ; racine dm-0 et partitions du SSD montées. SMART PASSED, Critical Warning=0, erreurs média/intégrité=0. smartctl retourne toutefois 4 parce que la lecture du journal d’erreurs est refusée par `Invalid Log Page (0x109)` : ce journal détaillé est indisponible, pas une preuve de défaillance du SSD. 38 arrêts non sûrs historiques relevés ; aucune attribution à la mission.

Aucun échec PCIe `can't assign/no space/failed to assign`, timeout/reset/I/O NVMe ou faute DMAR/AER/DPC explicite repéré dans la recherche ciblée du journal courant collecté. Aucune ligne `add_size` ne démontre une réserve demandée à nouveau sur ce boot. Les avertissements Thunderbolt sur les liens natifs manquants et les erreurs ACPI préexistantes restent à comparer par signature ; le journal n’est pas qualifié d’exempt de tout avertissement.

## 8. Ligne GRUB temporaire préparée, jamais appliquée

Sélection future : **JARVIS — T2 eGPU réserve PCIe 512M**. Conserver le bloc de recherche /boot et son initrd. Modifier seulement sa ligne linux lors d’une édition ponctuelle, avec le Core déconnecté, après autorisation :

```text
linux /vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M 'pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0'
```

Initrd conservé : `/initrd.img-6.18.54-1-t2-trixie`. Les guillemets simples protègent les points-virgules pour GRUB ; ils sont syntaxiques et ne font pas partie de la valeur attendue par Linux. Sans protection, les points-virgules seraient des séparateurs GRUB. Cette ligne est **destinée à l’éditeur GRUB, pas à un shell Linux**.

`ligne-grub-temporaire.txt` contient cette ligne ; `bloc-grub-verification.cfg` est une copie locale du bloc réel avec ce seul ajout. `grub-script-check` réussit, code 0. Cela valide la syntaxe du bloc, pas le routage PCIe ni le futur démarrage. Aucun update-grub, grub-reboot ou grub-set-default, aucune écriture grubenv. Le paramètre ne sera pas enregistré de façon persistante.

## 9. Tests après un futur démarrage sans Core

Ces étapes sont préparées ; aucun boot n’a lieu en 04L.

1. **Avant essai :** opérateur à la console physique, écran branché au Mac/Intel, clavier direct utilisable dans GRUB, poste SSH prêt. Identifier le menu et les secours ci-dessous ; laisser le Core déconnecté. Vérifier les empreintes et disposer du rapport hors de JARVIS. Une absence de console/GRUB exploitable reporte l’essai.
2. **Après boot :** confirmer nouveau boot ID, noyau T2 exact et sept arguments complets. Vérifier que `/sys/bus/pci/resource_alignment` reflète la liste entière et que les BDF/identités correspondent aux trois ponts attendus. Toute troncature, paramètre inconnu/ignoré ou pont inattendu entraîne arrêt.
3. Exécuter le collecteur préparé, puis analyser les preuves avec `verifier-reserve.py DOSSIER_PREUVES`. Il compare registres/sysfs, inclusions, décodage mémoire, type PREF64, branches sœurs, aperture racine, réserve contiguë et placement aligné. Il lit seulement les fichiers de preuves ; un résultat positif n’autorise pas seul un branchement.
4. Refaire une comparaison de toutes les ressources PCI, particulièrement NP, BAR NHI/USB et branches non ciblées ; vérifier pour chaque BAR l’inclusion par chaque pont parent et l’absence de chevauchement entre ressources de même niveau. Distinguer inclusions parent/enfant normales des collisions. Vérifier HDA, fonctions T2, autre domaine Thunderbolt et réservations iomem globales.
5. Confirmer Intel primaire/i915, DP-3 actif, bureau réactif et gestionnaire d’affichage ; vérifier SSD/racine, NVMe live et journaux I/O ; vérifier Ethernet, route et **nouvelle connexion SSH authentifiée depuis le poste distant**. Aucun benchmark écrivant sur le SSD, aucun chargement de pilote GPU, aucun rescan.
6. Observer au moins cinq minutes après la disponibilité du bureau, avec relevés initial et final, et réexaminer erreurs PCIe, AER/DPC, ACPI, IOMMU, Thunderbolt, NVMe et i915. Capturer à nouveau journaux et empreintes. Aucun succès déclaré sur un journal incomplet.

### Critères de décision avant tout branchement

| Décision | Critères précis |
|---|---|
| Réserve préparée, essai GPU seulement envisageable | au moins 512 Mio PREF libres et contigus dans la branche cible ; inclusion dans chaque parent et aperture ACPI ; registres/sysfs cohérents ; types appropriés ; placement mathématique simultané de 256/32 Mio avec alignements naturels ; NP suffisant pour BAR0 de 16 Mio aligné et marge ROM/audio/boîtier ; tous les autres BAR/branches valides ; tests bureau/SSD/Ethernet/SSH concluants ; aucune nouvelle erreur critique |
| Réserve partielle, arrêt | agrandissement de certains ponts seulement, parent manquant, réserve contiguë inférieure à 512 Mio, alignement impossible, ou descendants incompatibles |
| Réserve inefficace, arrêt | chaîne toujours 224/112 Mio, ou absence d’agrandissement utilisable |
| Non concluant, arrêt | journaux/ressources indispensables manquants, incohérence registres/sysfs, contrôle humain ou nouvelle connexion SSH non réalisés |
| Régression, arrêt immédiat | NVMe absent/reset/I/O, root non montable, perte Intel/bureau, Ethernet/SSH perdu, NHI/USB non couverts, collisions, nouvelle faute DMAR/AER/DPC ou allocation essentielle échouée |

Seuil NP conservateur proposé : un bloc libre d’au moins 32 Mio sur la branche, permettant BAR0 aligné et marge. Ce seuil est un contrôle préalable, pas une mesure des besoins exacts du futur boîtier. Une taille différente exige une analyse explicite des besoins historiques et de tous les alignements, pas une acceptation automatique. Même 512 Mio PREF ne prouve pas l’allocation GPU, absent par construction ; celle-ci et les ponts externes relèvent d’une mission distincte après accord.

**Dans tous les cas d’arrêt : NE PAS brancher le Razer Core. Un succès sans Core exige encore une autorisation explicite pour l’essai GPU.**

## 10. Retour arrière et risques

Le GRUB actif présente un menu visible **15 secondes** ; choix par défaut Debian **6.12.111**, déterminé par la configuration complémentaire, malgré les valeurs génériques de /etc/default/grub. Navigation proposée : interrompre le compte à rebours avec une touche ; en EFI, Esc répété peut aider si nécessaire. `e` ouvre l’édition, Esc l’annule, Ctrl-X/F10 démarrerait la ligne modifiée **seulement lors de l’essai autorisé**. La sélection manuelle de l’entrée 512M en 04J montre un accès menu déjà réalisé par l’utilisateur ; le clavier doit rester utilisable lors du prochain essai.

| Secours à sélectionner sans candidat | Vérification actuelle |
|---|---|
| **JARVIS — T2 eGPU diagnostic sans Nouveau**, ID `jarvis-t2-egpu-sans-nouveau` | noyau/initrd 6.18.54-1-t2-trixie présents ; arguments IOMMU/pt/pm_async et blacklist, sans realloc/réserve/candidat |
| **Advanced options for Debian GNU/Linux → Linux 6.12.111+deb13-amd64** | noyau/initrd présents ; modules i915, tg3, nvme/nvme-core dans initrd ; boots antérieurs observés à 15:24 et 18:48 avec NVMe/racine et Ethernet |
| **Advanced options for Debian GNU/Linux → Linux 6.12.107+deb13-amd64** | noyau/initrd et mêmes modules dans initrd ; disponibilité vérifiée, démarrage de secours non testé par cette mission |

Ne pas confondre l’entrée T2 « essai » sans blacklist avec le diagnostic antérieur. Le diagnostic est le premier retour arrière recommandé, Core toujours déconnecté. L’édition ponctuelle disparaît au prochain boot ; aucun fichier à restaurer pour ce candidat. Aucun paramètre global, règle ou sélection automatique n’est ajouté.

Si la machine reste réactive mais échoue : arrêter les contrôles actifs, conserver les preuves et revenir lors d’un redémarrage explicitement autorisé au diagnostic. Si l’affichage tombe mais SSH fonctionne : lire les preuves à distance, sans unbind/rescan ni modification i915. Si SSH tombe mais console fonctionne : collecter localement. Si blocage total : dernier recours physique préalablement accepté par l’opérateur, sans boucle de redémarrages ; une coupure forcée expose le SSD à un arrêt non sûr. Aucune de ces actions n’est exécutée ici.

Au retour, vérifier noyau/cmdline sans candidat, nvme0 live et racine/boot/EFI montés, absence de nouvelles erreurs I/O, Intel i915 primaire et bureau réactif, tg3/enp4s0 UP/1000 Mbit/s, route et nouvelle connexion SSH. Archiver un boot ID distinct et comparer aux preuves de référence.

| Risque | Évaluation argumentée |
|---|---|
| Démarrage | modéré, échec possible : allocation NP/PREF de deux parents d’un domaine Thunderbolt remise en jeu ; branche sœur conservée peut bloquer la solution. Aucun taux de réussite mesuré |
| Affichage Intel | inférieur à une réallocation globale, mais non nul : i915 hors cible ; collision/perturbation globale ou clavier sur hub Thunderbolt peuvent rendre la console inutilisable |
| SSD Apple/T2 | hors cible et secours 6.12.111 observé fonctionnel ; pas de garantie face à collision globale, firmware ou arrêt forcé. Préserver l’ensemble de ses fonctions |
| Connectivité | Ethernet hors cible, risque indirect non nul ; la connexion SSH existante avant boot ne garantit pas son retour |
| NHI/USB/branche sœur | exposition directe par parents ciblés ; ressource NP valide et reconstruction cohérente obligatoires |
| Retour arrière | fort avantage d’une édition ponctuelle, mais exige console physique et menu accessibles ; aucun mécanisme logiciel ne récupère seul une machine complètement figée |

**Recommandation : conserver exactement ce candidat pour un premier essai ponctuel sans Core, seulement après autorisation et confirmation des moyens de récupération.** Les preuves indispensables sont disponibles et la syntaxe est confirmée ; la reconstruction de la branche sœur reste la principale incertitude technique. Aucun élargissement automatique du ciblage n’est prévu.

## 11. Intégrité et clôture

Empreintes des sources GRUB, grubenv et des noyaux/initramfs/configurations comparées avant/après préparation ; résultats conservés dans `empreintes-systeme-avant.json` et `integrite-fin.json`. GRUB actif SHA-256 : `81be6b6101d1916fb9c62de50444959ee19b8a3dbbf714c8eb9c368f2919054d`. SHA256SUMS du dossier et archive séparée assurent la conservation des preuves. ELF temporaire retiré après archivage de son empreinte et des extraits statiques ; image système intacte.

**Mission 04L terminée. Aucun essai appliqué. Attente de l’autorisation utilisateur avant toute édition de démarrage, tout redémarrage ou essai matériel.**

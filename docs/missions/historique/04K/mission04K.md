> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission04K.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 04K : limitations PCIe du Mac mini 2018

**Étude terminée le 11 octobre 2026. Recommandation : valider puis envisager une réallocation Linux ciblée des ponts au démarrage, en conservant les apertures ACPI. Aucun essai exécuté. Le Core reste déconnecté ; attente de l’accord utilisateur.**

Le problème démontré est une chaîne de fenêtres trop petites, pas l’absence d’un espace hôte supérieur à 4 Gio. Une correction réellement utile doit attribuer une plage contiguë et alignée, la faire traverser tous les ponts et maintenir la cohérence entre registres PCI, ressources Linux et aperture hôte. La présence du GPU, son autorisation Thunderbolt ou le chargement d’un pilote ne satisfont pas ces conditions.

## 1. Périmètre et niveau de preuve

Machine de référence : Macmini8,1, Debian T2Linux, noyau 6.18.54-1-t2-trixie, Razer Core et Quadro RTX 5000 10de:1eb0. Références privilégiées : mission 04H, boot `[UUID EXPURGÉ]`. Mission 04J et lectures 04K : boot `[UUID EXPURGÉ]`, Core absent de la vue PCI/Thunderbolt accessible.

L’environnement reste isolé : sudo interdit par NoNewPrivs, journaux noyau actuels invisibles, iomem actuel masqué, D-Bus/netlink bloqués. Lecture DSDT, SSDT1, MCFG et DMAR refusée. Les apertures et capacités externes ci-dessous proviennent donc des preuves 04H, pas d’une nouvelle extraction ACPI complète. Le code public étudié est Linux stable 6.18.54 ; des différences propres au noyau T2 installé restent possibles. Aucun téléchargement/exécution de script, changement système, écriture PCI, retrait/rescan, chargement expérimental, changement GRUB/EFI/ACPI/VFIO, branchement ou redémarrage.

## 2. Correction importante : fenêtres 64 bits

Les rapports 04I/04J reprenaient « 32-bit » affiché par lspci pour les fenêtres actives. **Cette indication ne permettait pas de conclure à une limitation matérielle à 32 bits.** La lecture binaire de 64 octets de configuration, sans écriture, montre maintenant :

| Pont | PREF_BASE à 0x24 | PREF_LIMIT à 0x26 | Type bas/limite | Registres hauts 0x28/0x2c |
|---|---|---|---|---|
| 00:01.2 | 0xbf41 | 0xcd31 | 1 / 1 : 64 bits | 0 / 0 |
| 7b:00.0 | 0xbf41 | 0xcd31 | 1 / 1 : 64 bits | 0 / 0 |
| 7c:01.0 | 0xbf41 | 0xc631 | 1 / 1 : 64 bits | 0 / 0 |

Le masque du type vaut 0x0f ; 0 signifie 32 bits et 1 signifie 64 bits. Des registres hauts nuls signifient une plage actuellement sous 4 Gio, pas une impossibilité de décoder au-dessus. Décodage corroboré par les [définitions PCI Linux](https://raw.githubusercontent.com/torvalds/linux/v6.18/include/uapi/linux/pci_regs.h) et l’en-tête local archivé. lspci 3.13.0 utilisé ; la cause de sa présentation divergente n’est pas établie ici.

Le journal 04H qualifie déjà les fenêtres 00:01.2, 7b:00.0 et 7c:01.0 de `64bit pref`. Il qualifie également celles de 7f:00.0 et 80:01.0 ainsi lors de leur énumération. Les ressources sysfs 04H permettent de corroborer leurs attributs Linux ; 80:01.0 est désactivé à l’état final. **Toute la chaîne possède ainsi des indications de prise en charge 64 bits**, mais la vérification brute actuelle des deux ponts externes est impossible sans le Core. Ce dernier point devra être confirmé dans un futur essai autorisé, sans sonder les tailles BAR par des écritures.

Cette correction ne change ni les tailles insuffisantes ni la recommandation de 04J. Les rapports historiques restent conservés ; le présent rapport rectifie leur interprétation du type.

## 3. Pont racine et contraintes de la chaîne

Chaîne GPU 04H : `pci0000:00 → 00:01.2 → 7b:00.0 → 7c:01.0 → 7f:00.0 → 80:01.0 → 81:00.0`. 00:01.2 est un pont PCIe racine Intel, distinct du host bridge qui fournit les apertures du bus 00. Les BDF externes devront être retrouvés dynamiquement.

| Pont | Préchargeable 04E/04H | Préchargeable 04J/04K | Couverture constatée |
|---|---|---|---|
| 00:01.2 | bf400000–cd3fffff, 224 Mio | identique | inclus dans aperture ACPI basse historique |
| 7b:00.0 | bf400000–cd3fffff, 224 Mio | identique | égale à celle de 00:01.2 |
| 7c:01.0 | bf400000–c63fffff, 112 Mio | identique | incluse dans 7b:00.0 |
| 7f:00.0 | c0000000–c63fffff, 100 Mio | pont externe absent | incluse dans 7c:01.0 en 04H |
| 80:01.0 | aucune attribuée | pont externe absent | pas de couverture GPU préchargeable |

Adresses inclusives, Mio=1048576 octets. La branche sœur 7c:04.0 possède c6400000–cd3fffff, 112 Mio : on ne peut pas additionner deux plages de branches différentes pour placer un BAR contigu. Les NHI 7d:00.0/07:00.0 ne font pas partie de la chaîne GPU en série.

Les 224 Mio amont ne contiennent pas une BAR de 256 Mio. Son premier début naturellement aligné est c0000000 ; la fin cfffffff dépasse cd3fffff. La branche de 112 Mio échoue également. BAR 3 de 32 Mio peut isolément tenir, mais l’ensemble demande au moins 288 Mio. BAR 0 non préchargeable de 16 Mio était attribué et couvert : agrandir PREF ne dispense pas de préserver NP, la ROM et les autres fonctions.

## 4. ACPI et espace supérieur à 4 Gio

04H montre explicitement l’utilisation des fenêtres ACPI et ces ressources hôtes :

| Aperture mémoire | Taille inclusive | Interprétation |
|---|---:|---|
| 000a0000–000fffff | 384 Kio | espace bas historique |
| 80000000–feafffff | 2027 Mio | aperture MMIO basse, déjà partagée |
| 4000000000–7fffffffff | 256 Gio | aperture haute annoncée à Linux |

L’iomem privilégié 04H place Intel HDA 00:1f.3 à 4000000000–40000fffff. L’espace haut est donc une piste concrète mais **aucune adresse historique n’est une autorisation de réutilisation au prochain boot**. Il faut recalculer les collisions sur l’iomem complet courant, avec réservations firmware et tous les enfants.

Exemple purement arithmétique : BAR 1 à 4010000000–401fffffff, BAR 3 à 4020000000–4021ffffff ; une fenêtre de 512 Mio allant de 4010000000 à 402fffffff les contiendrait. Chaque parent devrait les couvrir et être réellement programmé en 64 bits. Aucun de ces placements n’est attribué ou proposé comme écriture manuelle.

Les erreurs ACPI _OSC de 04H (`AE_AML_BUFFER_LIMIT`, `AE_ALREADY_EXISTS`) et la couverture ECAM partielle sont archivées. Le même journal annonce que l’OS assume PCIeHotplug/AER/DPC ; ces erreurs ne prouvent donc ni absence de contrôle PCIe, ni lien causal avec les BAR. L’analyse AML exacte de _CRS, _OSC et des SSDT reste à faire depuis un accès hôte privilégié. MCFG décrit l’accès configuration, pas une réserve MMIO GPU ; DMAR décrit le remappage, pas une augmentation des fenêtres de ponts.

## 5. Pourquoi les paramètres précédents n’ont pas suffi

Dans Linux 6.18.54, `pbus_size_mem()` quitte si la fenêtre a déjà un parent. Les ressources firmware revendiquées peuvent donc rester intactes. Le supplément hotplug concerne `is_hotplug_bridge` et peut être optionnel ; l’allocation hotplug distribue l’espace disponible sous le port. 00:01.2 annonce HotPlug−, 7c:01.0 HotPlug+ ; ces bits ne suffisent pas à reconstituer tous les champs internes. `realloc=on` ne signifie pas remplacement inconditionnel de chaque fenêtre attribuée. [Dimensionnement Linux 6.18.54](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/pci/setup-bus.c).

**Inférence pour JARVIS :** les fenêtres conservées en 04J sont compatibles avec ces chemins. Le GPU absent au scan initial ne présente pas ses besoins de 288 Mio ; quand il apparaît en hotplug, la branche existante reste un goulet. Le journal 04H prouve les échecs aval, mais le journal 04J manquant empêche d’identifier exactement quelle passe a abandonné la réserve 512M. La syntaxe du paramètre était confirmée dans le binaire installé en 04I ; sa reconnaissance ne prouve pas son effet.

## 6. Mécanismes Linux et candidat ciblé

La documentation décrit `pci=resource_alignment=` avec une liste de périphériques et un ordre optionnel d’alignement ; un pont peut être ciblé pour réexaminer ses fenêtres. hpmmioprefsize demande une réserve hotplug ; hpbussize concerne les numéros de bus. `big_root_window` vise les CPU AMD, donc n’est pas adapté à ce Mac Intel. [Paramètres versionnés](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/Documentation/admin-guide/kernel-parameters.txt).

Dans `pci_reassigndev_resource_alignment()`, un pont ciblé voit ses fenêtres mémoire marquées non attribuées et désactivées pour réallocation. Le mécanisme touche NP et PREF, pas seulement la réserve GPU. Un ordre explicite peut gonfler les ressources BAR trop petites ; **29 signifie 2^29 octets, mais ne constitue pas une commande garantissant une fenêtre PREF de 512 Mio**. L’interface sysfs `resource_alignment` ne réalloue pas à elle seule immédiatement les périphériques déjà présents. [Implémentation pci.c](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/pci/pci.c).

Candidat d’étude, **à ne pas appliquer dans cette mission**, pour un essai ponctuel sans Core :

```text
pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```

Il conserverait les arguments T2, IOMMU, pm_async, blacklist et `pci=realloc=on pci=hpmmioprefsize=512M`. L’absence d’ordre explicite évite de demander un gonflement massif des petites BAR du GPU/NHI. Ce ciblage devra être validé dans le noyau T2 exact et sa topologie : désattribuer seulement le pont aval laisse le plafond de 224 Mio ; désattribuer toute la machine augmente inutilement le périmètre de risque.

**Limite :** la branche sœur 7c:04.0 peut conserver sa fenêtre, empêcher le déplacement souhaité de son parent ou augmenter le besoin global. Si deux branches réclament 512 Mio, leur parent peut avoir besoin d’au moins 1 Gio, plus autres ressources. Le premier essai n’inclut pas arbitrairement cette sœur ; si elle bloque, arrêt et étude d’un second candidat précisément borné, pas élargissement automatique. L’allocateur peut aussi choisir une plage basse : l’option ne force pas l’adresse haute.

Alternative de développement si le mécanisme natif échoue : quirk PCI spécifique à Macmini8,1 dans un noyau T2 de test, utilisant les APIs d’allocation et de réclamation de ressources pour toute la chaîne avant liaison des pilotes. Piste plausible, non correctif existant validé ; compatibilité Thunderbolt, verrouillage, collisions, descendants et échec atomique doivent être traités. Aucun noyau compilé ici.

## 7. Démarrage avec Core connecté

Un essai sans nouveau paramètre peut déterminer si le firmware présente le GPU assez tôt pour que ses BAR soient comptés au scan initial. C’est un contrôle utile, pas une garantie d’agrandissement.

Distinguer : présence électrique → routeur Thunderbolt détecté → tunnel PCIe autorisé → GPU énuméré → BAR attribués. Une politique Bolt « auto » enregistrée en 04H ne garantit pas que le firmware autorise le tunnel avant le noyau. Une autorisation seulement après démarrage de boltd peut reproduire un hotplug tardif, même avec le câble branché depuis le départ. Les niveaux de sécurité et l’attribut authorized gouvernent le tunnel ; l’IOMMU ne fournit pas de fenêtre supplémentaire. [Documentation Thunderbolt Linux](https://docs.kernel.org/admin-guide/thunderbolt.html).

Il faudra dater PCI scan, NHI, apparition du routeur/Core, authorized, événement Bolt et GPU. Si le GPU n’apparaît qu’après boltd, l’essai n’a pas testé un GPU présent au scan initial. Ne pas créer de règle udev/service, modifier boot ACL, politique d’autorisation ou sécurité pour obtenir artificiellement ce résultat. Écran conservé sur Intel, pas sur la Quadro.

## 8. Audit du projet public t2-egpu-linux

Le [projet de philmcneely](https://github.com/philmcneely/t2-egpu-linux) rapporte un cas Macmini8,1 avec RX 6800/boîtier différent et noyau Ubuntu T2 différent. C’est un témoignage pertinent pour l’utilisation de l’aperture haute, pas une validation Debian/Quadro. Branche main consultée via le navigateur ; SHA de commit non obtenu, donc revue non figée et nouvelle vérification requise avant tout usage.

Le [script egpu-init.sh](https://raw.githubusercontent.com/philmcneely/t2-egpu-linux/main/egpu-init.sh) découvre la chaîne puis réécrit ses fenêtres et le BAR 0 AMD à adresse fixe, charge module/pilote et peut écrire un réglage DRM. Les erreurs d’écriture des ponts sont masquées ; la présence de n’importe quelle card DRM suffit à annoncer un succès, critère ambigu avec i915 déjà présent. Aucune opération de ce script n’est exécutée ni transposée.

Le [module egpu_bar.c](https://raw.githubusercontent.com/philmcneely/t2-egpu-linux/main/egpu_bar.c) cible 1002:73bf et une seule BAR AMD de 256 Mio. Il libère la ressource PREF du parent immédiat, change ses champs et donne directement un pointeur parent au BAR. Il ne réinsère pas cette fenêtre via request_resource et ne reconstruit pas toutes les ressources des ancêtres. Le déchargement restaure des champs, mais pas la réclamation complète ni les registres matériels. Le retour arrière annoncé est donc incomplet pour cet usage. JARVIS demande deux BAR préchargeables, 256 + 32 Mio : une fenêtre de 256 Mio ne suffit pas. Remplacer l’identifiant AMD ou BAR 0 par BAR 1 serait une adaptation insuffisante et risquée.

## 9. Risques et classement

Les probabilités ci-dessous sont qualitatives : aucune série d’essais ne permet un pourcentage fiable.

| Stratégie | Risque | Complexité | Potentiel / décision |
|---|---|---|---|
| Compléter relevés hôte/ACPI/config | très faible | faible à moyenne | indispensable ; aucune correction par elle-même |
| Répéter seulement realloc + 512M | faible à modéré au boot | faible | faible : résultat négatif déjà observé |
| Boot connecté, configuration existante | modéré | faible | incertain ; contrôle chronologique utile après accord séparé |
| resource_alignment ciblé + realloc/réserve | modéré, panne de boot possible | moyenne | meilleur compromis mécanisme natif / ciblage ; candidat principal |
| Quirk noyau T2 spécifique correctement alloué | élevé | élevée | potentiel technique sérieux, non démontré ; seconde ligne |
| Noyau T2 plus récent seul | modéré | moyenne | inconnu sans correctif PCI identifié ; ne pas promettre une résolution |
| Ignorer _CRS par nocrs / réallocation globale | élevé | moyenne | mauvais ciblage : aperture haute existe déjà ; déconseillé |
| Changer EFI/ACPI / politique Thunderbolt | élevé à très élevé | élevée | besoin non établi ; pas de premier essai |
| Script setpci + module du projet | très élevé | élevée après adaptation | exemple AMD, invariants incomplets ; non recommandé |
| Redimensionner BAR/ReBAR ou installer NVIDIA | variable | moyenne | ne crée pas l’espace des parents ; ne traite pas ce goulet |

Intel i915 00:02.0 est une branche sœur : ses BAR historiques 80000000–80ffffff et a0000000–afffffff doivent être préservés. Une réallocation globale ou une collision peut perdre l’affichage même si l’on ne cible pas i915. Le SSD/T2 sous 00:1b.0 utilise l’espace bas b0000000–b12fffff ; sa perte peut empêcher le démarrage et corrompre des données si des transactions sont mal routées. Ethernet tg3 sous 00:1c.1 et ses BAR bas doivent rester disponibles pour SSH. HDA occupe déjà l’aperture haute. NHI, USB Thunderbolt et branche sœur partagent des parents avec la cible : une fenêtre NP supprimée ou mal replacée peut casser ces fonctions. Une modification MMIO n’est pas neutralisée par intel_iommu=on.

## 10. Protocole proposé, non exécuté

**Phase préalable obligatoire — lecture seule depuis l’hôte.** Vérifier sudo réel, journal noyau complet, iomem non masqué, accès bus système et réseau. Relever boot ID/cmdline, PCI/arbre, sysfs resource, configuration brute des ponts, DRM/GNOME, Ethernet/SSH, NVMe et SMART si outil déjà installé. Copier DSDT/SSDT/MCFG/DMAR et désassembler avec outil disponible sans installation implicite. Vérifier _CRS/_OSC, toutes les réservations, flags PREF64 et le comportement resource_alignment dans la version T2 exacte. Contrôler absence de pilote GPU et absence de nouveau/nvidia chargés ; ne provoquer aucun chargement. Si une preuve essentielle manque, aucun essai dépendant.

**Phase 1 — candidat principal, uniquement après accord explicite.** Préparer une fiche de ligne complète, BDF/identités/descendants et paramètres comparés. Tester par édition ponctuelle du menu GRUB lors d’un seul boot, sans enregistrer de configuration, sans Core. Cela nécessitera une autorisation distincte de la présente étude. La machine doit disposer d’une console physique Intel, d’un secours T2 connu et d’un poste SSH ; le choix Debian par défaut ne remplace pas la validation du secours T2 pour le SSD Apple.

Après boot, collecter avant tout branchement les mêmes preuves. Exiger une réserve PREF contiguë utile sur 7c:01.0, idéalement au moins 512 Mio, contenue dans 7b:00.0 puis 00:01.2 puis aperture hôte, types 64 bits compatibles. Vérifier mathématiquement un placement simultané aligné 256/32 Mio et l’espace des autres enfants. Une fenêtre parent peut être plus grande que 512 Mio ; le succès se juge à la chaîne, pas à une ligne du journal. Contrôler NP et les ressources de tous les descendants. Toute fenêtre insuffisante, collision, erreur allocation, régression i915/NVMe/réseau ou journal incomplet entraîne arrêt : **NE PAS brancher le Core**.

**Phase 2 — essai GPU seulement après validation de phase 1 et accord séparé.** Un hotplug surveillé permettrait de vérifier l’allocation réelle des BAR ; un boot connecté peut être retenu comme contrôle distinct de temporalité. Ne pas mélanger les deux scénarios ni ajouter plusieurs nouveaux paramètres. Aucun pilote NVIDIA requis pour vérifier l’allocation. Identifier le GPU par 10de:1eb0, retrouver tous ses parents et lire leurs registres/ressources. Si les ressources GPU restent nulles ou si les parents ne les couvrent pas, essai échoué. Autorisation Bolt et détection seule ne sont pas des succès.

**Preuves et critères.** Nouveau dossier par boot ID ; horodatages, commandes, stderr/codes, journaux noyau/système/Bolt complets, BAR/parents/config/iomem, SHA-256, tableau avant/après. BAR 1 = 256 Mio et BAR 3 = 32 Mio attribuées, naturellement alignées, non chevauchantes, couvertes par chaque parent ; BAR 0/ROM/audio et autres ressources valides. Nouveau toujours absent, i915 primaire, bureau réactif confirmé humainement, nouvelle connexion SSH authentifiée depuis le poste distant, Ethernet/route conservés, SSD live et aucune nouvelle erreur I/O/reset. Rechercher et contextualiser allocation, AER, DPC, ACPI, IOMMU et Thunderbolt ; comparer aux avertissements historiques.

**Retour arrière préparé.** L’édition ponctuelle disparaît au prochain boot. Si échec, arrêter l’essai, puis sur autorisation revenir à un démarrage sans Core avec l’entrée T2 connue sans le nouveau candidat ; aucune boucle d’essais automatique, rescan ou réparation setpci. Pour un boot bloqué, console physique et procédure d’arrêt/redémarrage préalablement convenue, puis entrée de secours. Conserver toutes les preuves disponibles avant de quitter un système encore réactif. Revalider Intel/SSD/Ethernet/SSH au retour. Les écritures de registres volatiles faites par l’allocateur au boot sont une intervention réelle même sans fichier modifié ; le candidat n’est donc pas présenté comme un test en lecture seule.

## 11. Décision recommandée

Le meilleur candidat pour augmenter réellement la chaîne est **la réallocation native ciblée des ponts existants**, associée à la réserve hotplug et à la validation de l’aperture haute déjà annoncée. Ce choix répond au blocage des ressources firmware conservées tout en limitant le périmètre par rapport à nocrs ou aux écritures manuelles. Son succès reste incertain, notamment à cause des branches sœurs et de l’implémentation T2.

La prochaine action recommandée est d’abord la collecte hôte privilégiée préalable. Ensuite seulement, envisager la phase 1 sans Core. Le boot connecté est un contrôle secondaire pertinent, pas une solution assurée ; les scripts du projet public ne sont pas recommandés. **Aucun accord de test, branchement, redémarrage ou changement de paramètre n’est présumé. Mission 04K terminée ; attente de l’accord utilisateur.**

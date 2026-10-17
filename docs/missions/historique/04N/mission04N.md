> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission04N.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Complément Mission 04N — Installation autorisée

**Prêt pour le redémarrage manuel sans Core. Installation terminée à 2026-10-11T22:46:12.325315+02:00. Aucun redémarrage exécuté ; candidat non testé.** Autorisation utilisateur : « oui poursuit et dit moi quand tu es pet a redemarer ».

Entrée à sélectionner : **JARVIS — T2 eGPU NP 32M + PREF 512M**, ID `jarvis-t2-egpu-np32-pref512`. Source `/etc/grub.d/47_jarvis_t2_egpu_np32_pref512`, root:root 0755 ; GRUB conserve root:root 0600. Modification des paramètres par rapport à 04M : ajout unique `pci=hpmmiosize=32M`. Noyau et initramfs inchangés ; aucun hpmemsize ajouté.

GRUB généré dans un espace de montage privé avec racine, /boot et /run en lecture seule, sources GRUB copiées, cache thème comparé, verrous et temporaires locaux. Diff vérifié : seul le nouveau bloc 47 apparaît. Syntaxe candidat et GRUB installé validée. Installation atomique et vérification des empreintes préalables. **31 autres fichiers protégés inchangés**, notamment noyaux/initramfs, sources GRUB antérieures, défauts et grubenv. Entrée 04M, diagnostic sans Nouveau et Debian 6.12.111/6.12.107 conservés. Menu visible 15 secondes en fonctionnement normal, défaut Debian 6.12.111 maintenu. Grubenv vide, aucun next_entry ni redémarrage programmé.

SHA-256 GRUB installé : `9bc2c064607d7daa3438da38e9f7808e71060aa6430c32af3decb3adbf5d7726` ; source 47 : `4f6104dbc649381003eb4018b5ad9d0cf663ec0a7ec4e512f04675519b627a16`. Sauvegardes et retour arrière limité à l'ajout 47 dans `installation-20261011-224539/`. Script retour-arriere.py préparé, non exécuté ; exige les empreintes attendues et conserve l'entrée 04M. Aucun retour arrière 04L exécuté.

Contrôles après installation : même boot `[UUID EXPURGÉ]`, cmdline actuelle toujours celle de 04M sans hpmmiosize (normal avant reboot), Intel i915 primaire, SSD nvme0 live, racine montée rw, Ethernet UP/1000 Mbit/s et carrier=1, services SSH et SDDM actifs, Core disconnected, aucune NVIDIA ni Nouveau. Collecte après : `hote-[UUID EXPURGÉ]-20261011-224634`.

Pour l'essai : conserver le Core physiquement débranché, écran Intel et clavier direct disponibles ; sélectionner manuellement la nouvelle entrée dans GRUB. Après démarrage, appliquer la validation sans Core décrite ci-dessous, avec nouvelle connexion SSH et bureau réactif confirmés par l'utilisateur. L'efficacité NP reste inconnue jusqu'à ce démarrage. Aucune autorisation de branchement eGPU n'est donnée par cette installation.

---

# JARVIS — Mission 04N : préparation de la correction NP

**Avis : corriger uniquement la demande NP avec `pci=hpmmiosize=32M` est un premier essai pertinent, sous réserve d'autorisation. `pci=hpmemsize=32M` seul est inadapté à l'objectif de préserver une demande PREF de 512 Mio : il règle les deux classes de mémoire. Aucun candidat installé ou démarré. Core débranché.**

Les preuves privilégiées confirment la réussite PREF de 04M et l'insuffisance NP. Le boot actuel demeure `[UUID EXPURGÉ]`, noyau `6.18.54-1-t2-trixie`. Il n'existe pas encore de résultat matériel pour le nouveau paramètre. L'étude n'autorise ni installation, ni redémarrage, ni branchement.

## 1. Preuves hôte et état de référence

`sudo -n id` retourne uid=0 ; les limitations de 04M sont levées pour cette mission. Collecte complète à 22:38:05 CEST dans `hote-[UUID EXPURGÉ]-20261011-223805/` : journaux noyau/système/Bolt, iomem non masqué, PCI détaillé, configurations brutes des ponts, sysfs, services, réseau, montages, SMART et ACPI. Le collecteur 04L a été vérifié par SHA-256 avant copie ; adaptations limitées au dossier de sortie 04N et au chemin absolu smartctl. Aucun outil système installé.

Ligne actuelle, inchangée :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```

La liste resource_alignment sysfs est intégrale et identique. Tous les ponts ci-dessous sont liés à pcieport. Adresses inclusives, Mio=1048576 octets.

| Pont | NP historique 04L | NP 04M confirmée hôte | PREF historique 04L | PREF 04M confirmée hôte |
|---|---|---|---|---|
| 0000:00:01.2, 8086:1909 | 8fa00000–9dbfffff / 226 Mio | 8fa00000–8fffffff / 6 Mio | bf400000–cd3fffff / 224 Mio | 4000000000–403fffffff / 1024 Mio |
| 0000:7b:00.0, 8086:1578 | idem / 226 Mio | idem / 6 Mio | idem / 224 Mio | idem / 1024 Mio |
| 0000:7c:01.0, 8086:15ea | 8fc00000–96bfffff / 112 Mio | 8fb00000–8fcfffff / 2 Mio | bf400000–c63fffff / 112 Mio | 4000000000–401fffffff / 512 Mio |
| 0000:7c:04.0, 8086:15ea | 96c00000–9dbfffff / 112 Mio | 8fe00000–8fffffff / 2 Mio | c6400000–cd3fffff / 112 Mio | 4020000000–403fffffff / 512 Mio |

Registres et sysfs concordent ; PREF base/limite type=1, donc décodage 64 bits. COMMAND.MEM actif. NP est une fenêtre de pont 32 bits et reste sous 4 Gio. L'analyseur 04L valide maintenant les apertures et retourne `CONTROLES_RESERVE_OK_VALIDATIONS_COMPLEMENTAIRES_REQUISES` : cet outil ne vérifie pas la suffisance NP, d'où le complément dédié.

Apertures hôte actuelles : `80000000–feafffff` (2027 Mio) et `4000000000–7fffffffff` (256 Gio), plus fenêtre legacy `000a0000–000fffff`. La PREF cible libre de descendants, `4000000000–401fffffff`, est réellement enregistrée sous l'aperture haute et les deux parents. Placement arithmétique : BAR1 `4000000000–400fffffff`, BAR3 `4010000000–4011ffffff`. Aucun routage vers un GPU absent n'est testé.

L'audit complémentaire trouve 62 inclusions mémoire BAR/fenêtres vers leurs ancêtres, toutes correctes, et aucune collision de mémoire entre allocations de même niveau. Les imbrications parent/enfant normales sont distinguées des collisions. La réserve PREF ne rencontre aucune autre réservation publiée dans iomem. Le matériel firmware caché et les effets du futur hotplug ne sont pas démontrables par cette inspection.

## 2. Journaux et recherche de régressions

Les six messages `can't claim; no compatible bridge window` concernent les anciennes fenêtres de 7c:00.0, 7c:02.0, 7c:04.0 NP/PREF et BAR0/BAR1 NHI 7d:00.0. Ils apparaissent à l'énumération avant reconstruction. Le journal confirme ensuite leur attribution, les plages finales sont couvertes et les pilotes sont liés. Ce sont des échecs transitoires de revendication firmware, pas des allocations finales manquantes. Ils doivent être interprétés avec leur issue ; un message semblable non résolu au prochain boot entraînerait arrêt.

Aucun échec final `no space`/`failed to assign`, erreur E/S NVMe, timeout/reset NVMe, faute de traduction DMAR, événement AER critique ou déclenchement DPC n'est repéré dans le journal complet collecté. Les compteurs AER disponibles sont archivés ; leur vérification finale est résumée dans les preuves complémentaires. Les lignes annonçant AER/DPC ou l'activation de VT-d ne sont pas des erreurs.

Les signatures suivantes existent déjà en 04L : ACPI AE_AML_BUFFER_LIMIT et AE_ALREADY_EXISTS ; IOAPIC GSI34 introuvable ; échec intel-lpss ACPI INT34BA:00 avec IRQ absente ; liens natifs Thunderbolt manquants ; i915 eDP désactivé faute d'information de lien ; pcspkr déjà enregistré ; tentatives de firmware Broadcom et échec P2P ; Bluetooth baudrate ; NVMe unchecked data buffer. Les adresses variables des tables SSDT sont normalisées pour comparer les signatures. Aucune nouvelle signature parmi ces avertissements. L'échec ACPI LPSS ne doit pas être confondu avec la fonction PCI 00:1e.0, dont le pilote reste lié.

Un avertissement tg3 « VPD access failed » apparaît pendant la collecte PCI détaillée ; même signature en 04L. La lecture diagnostique VPD peut provoquer cet avertissement ; aucun lien perdu n'est constaté. Il n'est pas assimilé à une régression Ethernet. Aucun registre PCI n'a été modifié par la mission.

SSD Apple AP0512M : nvme0 live, partitions p1 EFI /boot/efi, p2 ext4 /boot et p3 LVM ; racine LVM montée **rw** dans l'hôte. SMART PASSED, Critical Warning=0, erreurs média/intégrité=0, compteur d'erreurs=0, 35 °C ; 38 arrêts non sûrs historiques. Code smartctl=4 dû à `Invalid Log Page (0x109)` lors de la lecture du journal détaillé, limite du contrôleur déjà connue. L'état de santé lisible n'est pas un échec global SMART.

Intel i915 primaire, DP-3 connecté/activé, SDDM actif ; Nouveau et GPU NVIDIA absents. Ethernet enp4s0 UP, carrier=1, 1000 Mbit/s, `[ADRESSE PRIVÉE EXPURGÉE]/24`, route et écoute SSH présentes, service/socket SSH actifs. Aucune connexion SSH depuis le Mac n'est démontrée par la capture des connexions ; une nouvelle connexion et la réactivité humaine du bureau restent à confirmer avant tout essai futur.

**Aucune régression critique identifiée dans les preuves hôte actuelles.** Ce constat répare les limites documentaires de 04M, sans réécrire son rapport archivé. L'insuffisance NP reste certaine et interdit le branchement.

## 3. Fonctionnement exact des paramètres dans le T2 installé

Image installée SHA-256 `a41e1a7680c5d76761a744d4265b7901bbd7494e90340fda1eb59eec73d72d1b`. ELF extrait pour analyse statique : `120964b4ad696997873e737756f0240d7c7e64cfa726fc34bb91f186c7c855e1`, identique à 04L. Aucun code extrait exécuté. System.map fournit les symboles ; chaînes et désassemblages sont archivés.

Parser `pci_setup` :

| Paramètre | Effet établi dans le binaire |
|---|---|
| hpmmiosize=32M | memparse puis écriture de pci_hotplug_mmio_size, adresse 82dbcf58, seule |
| hpmmioprefsize=512M | memparse puis écriture de pci_hotplug_mmio_pref_size, adresse 82dbcf50, seule |
| hpmemsize=32M | memparse puis écriture du même résultat dans **les deux** variables |

La branche hpmemsize compare 10 octets, saute le nom, appelle memparse puis effectue les deux stores à `ffffffff833b8fb1` et `ffffffff833b8fb8`. M représente 2^20 : 32M=0x02000000 et 512M=0x20000000. La branche hpmmiosize (11 octets) n'effectue qu'un store à `ffffffff833b8f51`. Les octets rodata des trois noms sont vérifiés.

Le parser traite les options dans leur ordre ; une affectation ultérieure remplace la précédente. Conséquences :

| Ordre dans cmdline | NP demandée | PREF demandée | Avis |
|---|---:|---:|---|
| 04M actuelle : hpmmioprefsize=512M | 2 Mio par défaut | 512 Mio | NP insuffisante |
| 04M puis hpmemsize=32M | 32 Mio | **32 Mio** | ne préserve pas la demande PREF |
| hpmemsize=32M puis hpmmioprefsize=512M | 32 Mio | 512 Mio | équivalent fonctionnel, dépend de l'ordre |
| 04M + hpmmiosize=32M | 32 Mio | 512 Mio | recommandé pour isoler la variable NP |

Le candidat ordonné hpmemsize avant hpmmioprefsize serait techniquement cohérent. On privilégie hpmmiosize pour exprimer directement la demande NP et éviter l'écrasement PREF. Une demande PREF de 32 Mio ne permet pas de promettre une baisse exacte des fenêtres à 32 Mio si certaines restent revendiquées ; c'est la **demande globale** qui changerait, et le succès observé de 04M ne serait plus préservé par les paramètres.

La référence amont concorde avec les chemins vérifiés : [parser Linux 6.18.54](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/pci/pci.c). Sources téléchargées versionnées et SHA archivés, identiques aux copies 04L. La preuve du binaire T2 est distincte d'une hypothèse de correspondance totale au code amont.

## 4. Agrandissement NP des parents et allocation simultanée

Le désassemblage de `__pci_bus_size_bridges` confirme la récursion sur les enfants avant le calcul du parent. Le test du drapeau hotplug ouvre les lectures des deux variables de réserve à `ffffffff81a50518` et `ffffffff81a50524`. Le chemin appelle séparément `pbus_size_mem` pour PREF et NP. Le binaire de pbus_size_mem montre accumulation des ressources, maxima et arrondi ; les ressources déjà revendiquées sont préservées par le chemin d'exclusion.

Le dimensionnement distingue besoins obligatoires et extensions optionnelles hotplug. La demande n'est ni une adresse, ni un alignement naturel de BAR, ni une taille imposée à chaque parent. Les extensions peuvent échouer tout en laissant les ressources obligatoires attribuées. Le contrôle doit porter sur les fenêtres finales, pas uniquement sur cmdline.

SltCap : 00:01.2 HotPlug− ; 7b:00.0 Upstream Port ; 7c:01.0 et 7c:04.0 HotPlug+/Surprise+. La réserve est demandée directement aux ports hotplug, puis leurs fenêtres et suppléments sont additionnés dans les parents. Les 6 Mio NP actuels s'expliquent par 1 Mio NHI + 2 Mio cible + 1 Mio USB + 2 Mio sœur. La PREF 1024 Mio est l'addition de deux réserves de 512 Mio.

Avec une reconstruction comparable et les deux extensions réussies, l'attente sans Core est :

| Niveau | NP attendue avec candidat | PREF à préserver |
|---|---:|---:|
| 7c:01.0 vide | au moins 32 Mio | au moins 512 Mio |
| 7c:04.0 vide | au moins 32 Mio | au moins 512 Mio |
| 7c:00.0 NHI | 1 Mio dans l'état actuel | désactivée |
| 7c:02.0 USB | 1 Mio dans l'état actuel | désactivée |
| 7b:00.0 puis 00:01.2 | **au moins 66 Mio** pour couvrir l'ensemble | au moins 1024 Mio |

66 est une attente arithmétique pour cette topologie vide, pas une taille exacte promise par le noyau. Alignements, espaces nécessaires à des descendants ou échec de réserve peuvent modifier le résultat. Les deux fenêtres sœurs sont simultanées : on ne peut pas leur attribuer le même bloc NP sous prétexte qu'un seul boîtier sera branché. À l'inverse, on n'additionne pas le même BAR une nouvelle fois à chaque ancêtre ; chaque parent couvre le paquet de ses enfants.

La référence du calcul et du traitement optionnel est [allocateur Linux 6.18.54](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/pci/setup-bus.c). Le dimensionnement utilise une réserve comme minimum/maxima avec les besoins et cumule les suppléments enfants ; ce n'est pas « 32 Mio supplémentaires à chaque étage ».

`resource_alignment` reste identique : les trois ponts ciblés rendent **NP et PREF** réattribuables à l'énumération. L'ordre implicite demeure 12 (4 Kio) ; il ne demande pas des fenêtres de 32 ou 512 Mio. Les écritures de désactivation réalisées par le noyau lors d'un futur boot font partie du mécanisme étudié ; elles ne sont pas exécutées par cette mission. La sœur non ciblée a elle-même été reconstruite en 04M après échec de revendication sous les parents réinitialisés. Cette observation favorise la nouvelle hypothèse, sans garantir sa reproduction.

Changer uniquement la réserve NP laisse le mécanisme PREF et sa demande intacts. Cela ne fige pas ses adresses : l'allocateur peut redistribuer NP/PREF et d'autres BAR de la racine. hpmmiosize est **global pour les ponts hotplug**, pas limité aux trois BDF. Les ponts de l'autre domaine dont les fenêtres restent revendiquées peuvent être conservés ; toute libération/réaffectation doit néanmoins être contrôlée. Aucun ciblage plus large de resource_alignment n'est proposé.

## 5. Besoin NP du GPU et du Core

L'inventaire PCI historique 04E avec le Core branché, archivé ici sans nouvel accès au boîtier, distingue tailles BAR et réserves des ponts. Les BAR1/BAR3 graphiques manquaient alors d'allocation ; leurs besoins 256/32 Mio proviennent de l'objectif et des missions précédentes, pas d'une allocation réussie en 04E.

| Fonction historique | Besoin connu | Classe / traitement |
|---|---:|---|
| Quadro 81:00.0 BAR0 | 16 Mio | NP, alignement 16 Mio obligatoire |
| Quadro expansion ROM | 512 Kio | NP conservatrice ; ROM désactivée/virtuelle dans l'historique, ne pas l'activer |
| NVIDIA audio 81:00.1 BAR0 | 16 Kio | NP |
| NVIDIA UCSI 81:00.3 BAR0 | 4 Kio | NP |
| NVIDIA USB 81:00.2 BAR0/BAR3 | 256 + 64 Kio | PREF64, compte dans PREF ; marge NP prudente si repli |
| USB boîtier Intel 82:00.0 BAR0 | 64 Kio | NP, derrière une branche séparée |
| Quadro BAR5 | 128 octets | I/O, ne pas compter comme NP |
| Ponts externes 7f:00.0, 80:01.0, 80:04.0 | fenêtres de transit | ne pas compter leurs fenêtres en plus des BAR qu'elles contiennent |

Somme NP stricte connue incluant ROM : 17 387 520 octets, soit 16,58203125 Mio. Le paquet GPU/audio/UCSI/ROM se loge dans 17 Mio avec BAR0 aligné à 16 Mio ; le port USB séparé exige une fenêtre arrondie à 1 Mio. **Modèle minimal connu : 18 Mio NP** sur l'amont externe, avec choix d'adresse adéquat. Même en réservant les 320 Kio NVIDIA USB dans le paquet NP par prudence, celui-ci reste sous 17 Mio. Le classement réel PREF64 doit être conservé lorsque disponible.

Une simple taille de 18 Mio sans preuve de placement ne suffit pas : l'alignement de 16 Mio et les fenêtres internes imposent des contraintes. 32 Mio fournit une marge appréciable au-delà des fonctions connues et permet un modèle compact aligné. Le validateur hors ligne construit un BAR0 aligné, un paquet GPU de 17 Mio et une fenêtre USB de 1 Mio dans la NP cible ; il ne valide pas toute la politique de réserve des futurs ponts externes.

**Nuance essentielle : 32 Mio n'est pas une garantie de toutes les réserves hotplug du Core.** 80:01.0 (GPU) était HotPlug− ; 80:04.0 (USB) HotPlug+. Si le noyau conserve 32 Mio NP de réserve pour cette branche interne USB en plus des 17 Mio GPU, l'amont du Core demanderait environ **49 Mio**, éventuellement davantage selon alignement et chemins d'allocation. Les 98/81 Mio historiques des ponts externes étaient en grande partie des fenêtres/réserves, pas 98 Mio de BAR réellement consommés.

De même, la politique globale PREF512 pourrait demander une réserve PREF supplémentaire à la branche interne USB, en plus de 288 Mio graphiques et 320 Kio USB NVIDIA. Les besoins obligatoires connus restent compatibles avec 512 Mio ; la conservation intégrale de toutes les extensions optionnelles imbriquées pourrait dépasser cette taille. Le succès sans Core ne prouve pas l'allocation future de ces réserves externes.

L'essai 32 Mio doit donc répondre d'abord à « les fenêtres NP des ports et parents sont-elles reconstruisibles tout en gardant PREF512 ? ». Une autre valeur ne sera pas substituée automatiquement si le résultat est insuffisant. Un éventuel futur choix de 64 Mio exige une décision séparée : il augmenterait aussi la réserve sur les branches internes et ne garantit pas mécaniquement toutes les réserves imbriquées.

## 6. Ressources système modifiées et espace disponible

| Ressource | Comparaison 04L → état actuel |
|---|---|
| Intel i915 00:02.0 | BAR0 80000000–80ffffff, BAR2 a0000000–afffffff inchangés ; primaire |
| SSD Apple et fonctions T2 02:00.0–.3 | ensemble des BAR sous b0000000–b123ffff conservé ; pilotes nvme/t2bce conservés là où liés |
| Ethernet 04:00.0 | BAR 81610000–8161ffff et 81600000–8160ffff inchangés ; tg3 actif |
| NHI 7d:00.0 | ancien 8fb00000/8fb40000 → 8fa00000/8fa40000 ; couvert, thunderbolt lié |
| USB 7e:00.0 | ancien 8fa00000 → 8fd00000 ; couvert, xhci_hcd lié |
| HDA 00:1f.3 | BAR0 inchangé ; BAR4 4000000000–40000fffff → 4040000000–40400fffff ; snd_hda_intel conservé |
| LPSS PCI 00:1e.0 | 4000100000–4000100fff → 4040100000–4040100fff ; intel-lpss conservé |
| autre domaine TB sous 00:01.1 | fenêtres et BAR conservés |

Aucun changement de ressource/pilote entre le dernier relevé 04M et la collecte 04N ne sera présumé : comparaison exacte jointe aux preuves finales.

L'espace bas `90000000–9fffffff`, 256 Mio, n'a actuellement aucun enfant enregistré dans iomem. Il appartient à l'aperture basse et peut accueillir une construction NP de 66 Mio sans toucher Intel BAR2. Exemple **arithmétique seulement, aucune adresse imposée** : parents `90000000–941fffff`, cible `90000000–91ffffff` (32 Mio), sœur `92000000–93ffffff` (32 Mio), NHI `94000000–940fffff`, USB `94100000–941fffff`. Le mécanisme choisira ses propres adresses ; ce plan démontre une capacité publiée, pas le succès de l'allocateur ou l'absence d'occupants firmware invisibles.

## 7. Proposition expérimentale non installée

**Une seule option ajoutée à la ligne 04M : `pci=hpmmiosize=32M`.** Aucun changement de noyau, initramfs, liste BDF, reserve PREF, IOMMU, blacklist ou autre réglage.

```text
linux /vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M 'pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0'
initrd /initrd.img-6.18.54-1-t2-trixie
```

Bloc préparé dans `bloc-experimental-non-installe.cfg`, copie locale du bloc installé 46 avec ce seul ajout. `grub-script-check` retourne 0 ; syntaxe validée, aucune génération/installation GRUB. Nom et ID du bloc local gardés identiques pour comparaison ; ne pas installer ce bloc à côté de l'original avec un ID dupliqué.

Premier essai recommandé après accord : édition ponctuelle de la ligne de l'entrée actuelle dans GRUB, Core déconnecté, console Intel et clavier disponibles. Une installation persistante éventuelle relèverait d'une autorisation explicite supplémentaire ; elle devrait conserver l'entrée 04M comme référence et utiliser un ID distinct. Aucun changement n'a été fait maintenant.

## 8. Critères de validation sans Core

1. Nouveau boot ID, noyau exact, cmdline identique à 04M hormis hpmmiosize=32M ; PREF512 conservée, liste resource_alignment intégrale. Aucun GPU NVIDIA, Nouveau absent, Core disconnected.
2. Collecte privilégiée dès disponibilité du bureau puis après au moins cinq minutes. Conserver journaux complets, iomem non masqué, config des ponts et tous les BAR, pilotes, montages, SMART, réseau, services, compteurs AER, erreurs et codes de commandes. Vérifier boot ID constant pendant chaque capture et empreintes des preuves.
3. Port cible et sœur vides : chacun au moins 32 Mio NP, 512 Mio PREF libres et contigus. Parents couvrant les quatre branches : au moins 66 Mio NP et 1024 Mio PREF dans le modèle actuel, ou calcul explicite si la topologie diffère. Command.MEM, types PREF64 et concordance registres/sysfs obligatoires.
4. Vérifier chaque descendant sur tous ses ancêtres, disjonction des fenêtres sœurs, inclusion dans les apertures hôte et absence de collisions avec réservations iomem/ECAM/T2/i915/HDA. Un parent de seulement 32 Mio ne suffit pas à deux branches de 32 Mio.
5. Démontrer placement simultané BAR1 256 Mio, BAR3 32 Mio alignés ; BAR0 16 Mio aligné et paquet NP historique (ROM/audio/UCSI, marge USB, port USB séparé). Distinction explicite entre fonctions obligatoires et réserves internes futures. L'I/O BAR5 nécessite aussi couverture dédiée ; conserver I/O et bus disponibles, sans changement de hpbussize.
6. Intel primaire et bureau réactif, NVMe live/racine rw/boot/EFI montés, SMART sans nouveau signal critique, Ethernet [ADRESSE PRIVÉE EXPURGÉE]/SSH actifs. **Nouvelle connexion SSH depuis le Mac à confirmer par l'utilisateur**, avec validation physique du bureau.
7. Pas d'erreur finale d'attribution ou ressource essentielle manquante ; aucune nouvelle faute DMAR, AER/DPC critique, NVMe reset/E/S, i915 hang/perte d'affichage. Les anciens avertissements sont comparés par signature, pas effacés. Les messages transitoires can't claim ne sont acceptables que si toutes les ressources concernées sont réattribuées et fonctionnelles ensuite.

Outils préparés : `collecte-hote.py` (sudo, lectures et écritures de preuves uniquement), copie `verifier-reserve.py` de 04L, `verifier-np-pref.py` (hors ligne, complément NP), `audit-complementaire.py` (hors ligne, inclusions/collisions). Exemple après un futur boot autorisé :

```bash
sudo python3 /home/adminjarvis/JARVIS/rapports/mission04N-preparation/collecte-hote.py
# Utiliser le chemin exact « Preuves » affiché :
python3 /home/adminjarvis/JARVIS/rapports/mission04N-preparation/verifier-reserve.py /CHEMIN/PREUVES
python3 /home/adminjarvis/JARVIS/rapports/mission04N-preparation/verifier-np-pref.py /CHEMIN/PREUVES
python3 /home/adminjarvis/JARVIS/rapports/mission04N-preparation/audit-complementaire.py /CHEMIN/PREUVES
# Après au moins cinq minutes de bureau disponible, refaire le collecteur.
```

Un succès réserve sans Core permet seulement d'envisager une mission d'essai distincte avec autorisation ; il ne démontre ni allocation des ponts externes ni fonctionnement GPU. NP/PREF insuffisante → B et aucun branchement ; absence d'effet → C ; preuve indispensable/humaine manquante → D ; régression → E, arrêter les essais et conserver les preuves.

## 9. Retour arrière préparé, non exécuté

L'édition ponctuelle n'est pas persistante. Lors d'un redémarrage **ultérieurement autorisé**, reprendre l'entrée 04M « JARVIS — T2 eGPU réallocation ciblée PCIe » sans hpmmiosize ; elle restitue le scénario validé PREF et NP6/2, mais reste inapte au Core. En cas de régression de réallocation, choisir « JARVIS — T2 eGPU diagnostic sans Nouveau », puis Debian 6.12.111 ou 6.12.107 si nécessaire. Ces entrées sont conservées ; menu 15 s et défaut Debian à vérifier avant tout essai.

Console physique Intel et clavier direct requis pour l'essai. Si écran perdu mais SSH présent, collecter seulement ; aucun unbind/rescan/réglage i915. Si réseau perdu mais console présente, collecter localement. Aucun redémarrage automatique, aucune boucle d'essais, aucune coupure déclenchée par cette mission. Toute action de récupération matérielle reste décidée par l'opérateur.

Après retour : vérifier nouveau boot, cmdline de référence, Intel primaire, SSD/montages/SMART, réseau et nouvelle connexion SSH, journaux, fenêtres et empreintes. Aucun script de restauration n'est nécessaire pour le candidat ponctuel. Si une installation persistante était autorisée plus tard, préparer alors sa sauvegarde et son retrait précis ; ne pas exécuter le retour arrière 04L, qui retirerait l'entrée 04M existante.

## 10. Décision

**hpmemsize=32M est pris en charge et peut contribuer au dimensionnement NP, y compris indirectement des parents, mais il affecte aussi PREF.** Avec un ordre contrôlé avant hpmmioprefsize=512M, ses valeurs effectives seraient correctes ; ajouté à la fin, il contredirait l'objectif PREF. **Avis favorable conditionnel à un essai sans Core de hpmmiosize=32M**, formulation plus directe du changement NP unique.

L'espace bas publié paraît suffisant pour les 66 Mio attendus sans Core ; la reconstruction 04M constitue un indice favorable. La réserve n'est pas garantie, la portée du paramètre est globale, et les réserves hotplug internes du Core peuvent demander plus de 32 Mio. Préparation complète, configuration active intacte. **Attente de l'autorisation avant installation ou essai.**

## Vérification finale et conservation

Comparaison exacte au dernier relevé 04M : 0 changements de ressource/pilote, 0 nouveau périphérique. Compteurs AER disponibles sur 20 périphériques ; 0 compteur non nul relevé. Boot inchangé. 32 fichiers de démarrage protégés (noyaux, initramfs, configurations et sources GRUB, grub.cfg, grubenv) ont exactement les mêmes empreintes et métadonnées avant/après étude : True.

Sources, collecteur, analyseurs, journaux, inventaire historique, paramètres candidats et contrôles sont archivés avec SHA-256. Seuls les fichiers de préparation et preuves utilisateur ont été écrits ; aucune modification système.

## Registres finaux des quatre ponts concernés

| Pont | COMMAND | NP base/limite 20/22 | PREF base/limite 24/26 | PREF hauts 28/2c |
|---|---|---|---|---|
| 0000:00:01.2 | 0x407 | 0x8fa0 / 0x8ff0 | 0x1 / 0x3ff1 | 0x40 / 0x40 |
| 0000:7b:00.0 | 0x7 | 0x8fa0 / 0x8ff0 | 0x1 / 0x3ff1 | 0x40 / 0x40 |
| 0000:7c:01.0 | 0x407 | 0x8fb0 / 0x8fc0 | 0x1 / 0x1ff1 | 0x40 / 0x40 |
| 0000:7c:04.0 | 0x407 | 0x8fe0 / 0x8ff0 | 0x2001 / 0x3ff1 | 0x40 / 0x40 |

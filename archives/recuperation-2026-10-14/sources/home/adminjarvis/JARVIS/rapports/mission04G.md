# JARVIS — Mission 04G : vérification après branchement du Razer Core

11 octobre 2026, relevés vers 21:08–21:10 CEST. **Conclusion D : test non concluant, informations ou conditions de comparaison insuffisantes.** Le branchement est annoncé par l’utilisateur, mais la vue système accessible ne permet pas d’observer le Core ni la Quadro après cet événement. Ce bilan ne démontre ni réussite ni échec de la réallocation.

Toutes les vérifications sont en lecture seule. Seules les preuves et les rapports dans le dossier utilisateur sont écrits. Aucun CUDA, installation, chargement de module, autorisation Bolt, écriture PCIe, débranchement ou redémarrage exécuté.

## Conditions et accès

Boot ID accessible : `565560bb-80ac-424b-8bc3-101e7441b335`. Noyau confirmé par uname : `6.18.54-1-t2-trixie`. Ligne de commande :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on
```

Les deux arguments demandés sont présents. Le boot 04E était `cf644abb-f9ae-4308-ba1f-d97be3e7aa39`, sans pci=realloc=on, avec le même noyau et la même blacklist.

À la demande de réessai avec élévation, `sudo -n id` exécuté seul a confirmé uid=0 via une commande préapprouvée. Les commandes de collecte sudo ont néanmoins échoué dans le sandbox : `no new privileges`, avec avertissement de propriétaire `/etc/sudo.conf` uid 65534. Une demande d’exécution élevée de `sudo -n lspci -Dnn -d 10de:1eb0` a été rejetée par la politique automatique : `sandbox_approval: false`. Aucun contrôle privilégié PCIe/journal/Bolt réussi ne peut être déduit du succès isolé de id. Aucun changement des permissions ou contournement tenté.

## Détection et chaîne

Identification dynamique par `lspci -Dnnk -d 10de:1eb0` et parcours des attributs vendor/device de tous les périphériques sysfs : **aucune correspondance dans la vue accessible**. Aucune adresse actuelle du GPU n’est supposée. Le fichier resource du GPU et son lspci -nnk/-vv sont donc indisponibles pour 04G.

Thunderbolt : uniquement les hôtes Apple Macintosh `0-0` et `1-0`, authorized=1, et domain0/domain1, sécurité user, iommu_dma_protection=0. Aucun périphérique Razer externe visible. L’autorisation des hôtes ne prouve pas celle du Core. `boltctl list` et `boltctl domains` échouent sur D-Bus (Operation not permitted) ; l’autorisation actuelle du Razer Core n’est pas vérifiée.

Chaîne historique 04E, établie par les preuves : Mac mini → `0000:00:01.2 → 0000:7b:00.0 → 0000:7c:01.0 → 0000:7f:00.0 → 0000:80:01.0 → 0000:81:00.0` (Quadro).

La partie visible de cette branche en 04G est `00:01.2 → 7b:00.0 → 7c:01.0`, avec bus secondaire 7f, sans périphérique externe visible sur ce bus. Le NHI hôte est sur une autre branche : `00:01.2 → 7b:00.0 → 7c:00.0 → 7d:00.0`. Il ne faut pas l’ajouter comme pont parent du GPU. **La chaîne complète actuelle jusqu’à la Quadro ne peut pas être reconstituée.**

## Fenêtres comparées

Adresses inclusives ; Mio = 1 048 576 octets. Les lspci -vv et ressources sysfs des ponts visibles sont archivés ; leurs capacités étendues portent access denied.

| Pont | 04E sans realloc : non préchargeable | 04G avec realloc : non préchargeable | 04E : préchargeable | 04G : préchargeable | Différence observable |
|---|---|---|---|---|---|
| 00:01.2 | 0x8f900000–0x9dafffff, 226 Mio | 0x8fa00000–0x9dbfffff, 226 Mio | 0xbf400000–0xcd3fffff, 224 Mio | Identique, 224 Mio | NP décalée de +1 Mio ; tailles identiques |
| 7b:00.0 | 0x8f900000–0x9dafffff, 226 Mio | 0x8fa00000–0x9dbfffff, 226 Mio | 0xbf400000–0xcd3fffff, 224 Mio | Identique, 224 Mio | NP décalée de +1 Mio ; tailles identiques |
| 7c:01.0 | 0x8fb00000–0x96afffff, 112 Mio | 0x8fc00000–0x96bfffff, 112 Mio | 0xbf400000–0xc63fffff, 112 Mio | Identique, 112 Mio | NP décalée de +1 Mio ; tailles identiques |
| 7f:00.0 | 0x90000000–0x961fffff, 98 Mio | Non visible | 0xc0000000–0xc63fffff, 100 Mio | Non vérifiable | Pas de comparaison après branchement |
| 80:01.0 | 0x90000000–0x910fffff, 17 Mio | Non visible | Absente | Non vérifiable | Pas de comparaison après branchement |

Les fenêtres préchargeables visibles restent de 224/112 Mio. Aucune ne contient une plage de 256 Mio. Elles seraient insuffisantes pour BAR 1 si cette chaîne et ces fenêtres étaient celles de l’état réellement connecté. Mais l’absence du GPU et des ponts externes dans la collecte interdit de conclure C sur l’essai annoncé, ou B sur la seule translation des fenêtres NP entre deux boots.

## BAR : attribution et couverture

Les besoins 16/256/32 Mio et les types sont confirmés pour 04E par les journaux PCIe et les capacités Resizable BAR ; ils ne sont pas remesurables sur le GPU absent de la vue 04G. Les BAR 1 et 3 sont mémoire 64 bits préchargeable ; BAR 0 mémoire 32 bits non préchargeable.

| BAR | Taille/type requis | 04E : début–fin attribués | 04E : état et ressources noyau | 04E : couverture de tous les parents | 04G : début/fin, attribution, présence noyau, couverture |
|---|---|---|---|---|---|
| 0 | 16 Mio, non préchargeable | 0x90000000–0x90ffffff | Attribué dans sysfs resource et /proc/iomem ; décodage Mem- sans pilote | Oui : inclus dans chacune des cinq fenêtres NP de la chaîne ci-dessus | Tous non vérifiables ; GPU non visible |
| 1 | 256 Mio, préchargeable | Aucune ; resource 0/0/flags 0 | Non attribué ; aucune plage GPU correspondante dans iomem | Non : aucune plage attribuée ; amont 224/112/100 Mio insuffisant et fenêtre finale absente | Tous non vérifiables ; GPU non visible |
| 3 | 32 Mio, préchargeable | Aucune ; resource 0/0/flags 0 | Non attribué ; aucune plage GPU correspondante dans iomem | Non : aucune plage attribuée et fenêtre finale absente | Tous non vérifiables ; GPU non visible |

Pour 04E, 0/0 dans resource signifie absence d’attribution, pas une allocation à l’adresse zéro ; les plages à zéro dans les messages d’énumération expriment des besoins de taille. Les 288 Mio préchargeables cumulés nécessitent aussi l’alignement de BAR 1 et la prise en compte des autres périphériques. En 04G, /proc/iomem est conservé mais **toutes les adresses sont masquées à zéro** : il ne permet aucune validation de couverture ni d’adresse.

## Journaux et stabilité

| Vérification | 04E | 04G |
|---|---|---|
| can't assign / failed to assign / no space | Échecs BAR 1/3 et fenêtre de pont de 0x12000000 (288 Mio), documentés | Recherche impossible dans le journal noyau complet inaccessible |
| AER / DPC / DMAR | Preuves historiques conservées ; les capacités AER ne constituent pas seules une erreur journalisée | Absence d’erreur non démontrée ; journal inaccessible |
| NVMe errors / Thunderbolt errors | Journaux historiques conservés | Absence d’erreur non démontrée ; NVMe sysfs live seulement |
| Nouveau | Absent ; message Module nouveau is blacklisted | Absent de lsmod et /sys/module/nouveau ; blacklist active |
| NVIDIA | Aucun pilote lié au GPU | nvidia/nvidia_drm/nvidia_modeset/nvidia_uvm absents ; aucune tentative provoquée pendant cette mission. Absence de tentative antérieure au cours du boot non démontrable sans journal |
| i915 / affichage Intel | i915 primaire, GNOME et SSH confirmés par l’utilisateur à l’époque | i915 chargé et lié à 00:02.0, boot_vga=1 ; card0-DP-3 connected/enabled, modes 1920×1080. Réactivité GNOME non déduite de sysfs |
| Ethernet / SSH | enp4s0 UP, 192.168.1.99 ; services/écoutes établis | tg3 chargé, enp4s0 up, carrier=1, 1000 Mbit/s. IP/routes/écoutes/service SSH non vérifiables (netlink/D-Bus bloqués) |

`journalctl -b -k` indique restriction d’accès puis No entries ; ce résultat n’est **pas** un journal noyau vérifié vide. Les mêmes limites affectent les journaux système et Bolt. Aucun scan négatif ne peut démontrer l’absence des erreurs demandées. L’heure précise du branchement et les confirmations humaines GNOME/SSH ne sont pas encore reçues dans ce relevé.

## Comparaison avant/après du même démarrage et preuves

Aucune capture avant branchement identifiée pour le boot `565560bb-80ac-424b-8bc3-101e7441b335` dans les rapports disponibles. Aucune preuve hôte vérifiable du hotplug actuel ne permet de dater ou qualifier la capture restreinte comme état PCIe réellement après branchement. Les preuves 04E sont d’un autre démarrage : elles constituent une référence historique, pas l’état avant branchement du boot 04G. Les décalages NP observés ne sont pas attribués causalement à pci=realloc=on.

Preuves 04G : `mission04G-preuves/collecte-restreinte-20261011/` : boot/cmdline, PCI complet et arbre, lspci des ponts visibles, ressources sysfs, identification GPU, modules, Thunderbolt/DRM/Ethernet/NVMe, iomem masqué, tentatives journaux/Bolt/réseau/SSH et leurs erreurs, tentatives sudo, extraits 04E et SHA256SUMS.json. Référence 04E : `mission04E-preparation/preuves-20261011-205427/`, notamment pci-0000_81_00.0.txt, ressources-sysfs.json, iomem.txt et noyau-complet.log.

À compléter pour trancher : collecte hôte réellement privilégiée des mêmes données après branchement, identification dynamique et chaîne issue du chemin sysfs du GPU, fenêtres et resource, iomem non masqué, journal complet de ce boot et capture avant branchement du même boot si disponible. Ne pas rebrancher ni redémarrer pour obtenir ces preuves sans autorisation. Le collecteur existant `mission04E-preparation/collecte-lecture-seule.py` peut servir depuis un terminal hôte autorisé, vers un nouveau dossier de preuves.

**D. Test non concluant : informations ou conditions de comparaison insuffisantes.** BAR 1 et BAR 3 attribués et couverts par tous les ponts ne sont pas démontrés ; aucune réussite n’est revendiquée.

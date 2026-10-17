> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission04-incident-egpu.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 04I — Entrée réserve PCIe 512M installée

**Installation explicitement autorisée par « oui install », terminée et vérifiée le 2026-10-11T21:36:23.538987+02:00. Aucun redémarrage ni débranchement exécuté.** Cette section remplace le statut de préparation non installée conservé dans l’étude ci-dessous.

Entrée **JARVIS — T2 eGPU réserve PCIe 512M**, ID `jarvis-t2-egpu-reserve-512m`, installée via `/etc/grub.d/45_jarvis_t2_egpu_reserve_512m` (root:root 0755). GRUB actif (root:root 0600, mode conservé) identique au candidat préparé et à la génération contrôlée ; syntaxe vérifiée. Diff strictement limité au nouveau bloc 45.

Arguments propres à cette entrée : `intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M`, image/initramfs exacts `6.18.54-1-t2-trixie`, root/ro/quiet existants conservés. Debian 6.12.111 demeure le choix par défaut, menu 15 s ; secours Debian 6.12.107/6.12.111 et toutes les entrées T2 précédentes conservés. grubenv inchangé, aucune next_entry.

SHA-256 de `/boot/grub/grub.cfg` : `81be6b6101d1916fb9c62de50444959ee19b8a3dbbf714c8eb9c368f2919054d`. Autres empreintes protégées identiques avant/après : configuration globale/sources JARVIS existantes, grubenv et les trois paires noyau/initramfs. Sauvegarde juste avant installation et contrôles dans `mission04I-preparation/installation-20261011-213406/`.

Génération effectuée vers un fichier de contrôle dans un espace de montage privé avec racine, /boot et /run en lecture seule, copies des sources superposées, thème copié comparant le cache au lieu de le réécrire, verrous LVM et temporaires locaux. Génération retenue code 0, identique octet pour octet au candidat. Première tentative d’isolation non retenue conservée ; ses différences n’ont pas été installées. Aucun fichier thème système modifié.

Relecture après installation : boot ID `[UUID EXPURGÉ]` inchangé, Quadro encore présente, SSH/service/socket et display-manager actifs. `pci=hpmmioprefsize=512M` **n’est pas encore actif** dans le noyau lancé : son effet reste à tester lors d’un futur démarrage autorisé. La conclusion C de 04H n’est pas corrigée par cette installation seule.

**Installation terminée. Le retrait du Core, le redémarrage sans Core et le branchement surveillé ne sont pas autorisés par l’accord d’installation et n’ont pas été exécutés.** Le plan et les critères de validation avant branchement restent ceux de l’étude ; aucune configuration pilote, i915, VFIO, EFI, réseau, service ou initramfs modifiée.

---

# Mission 04I — Réserve PCIe hotplug 512M étudiée, non installée

**11 octobre 2026. Préparation achevée ; attente de l’accord explicite pour l’installation.** Test 04H clos, conclusion C confirmée par l’utilisateur depuis SSH : BAR 1/3 absents malgré realloc. Les 27 empreintes des preuves 04H ont été vérifiées ; archive tar.gz du dossier et du rapport, avec SHA-256, conservée dans mission04I-preparation.

Comparaison 04E/04H : fenêtres préchargeables inchangées (224/224/112/100 Mio, absente au pont final), BAR identiques ; seules trois fenêtres NP hôtes translatées de +1 Mio à taille constante. pci=hpmmioprefsize=512M pris en charge par le parser du binaire T2 installé, confirmé par désassemblage et System.map. Demande globale hotplug de réserve préchargeable, sans garantie d’extension des parents attribués ; 224 Mio restent insuffisants pour BAR 1 de 256 Mio. Essai utile uniquement si une réserve effective et couverte apparaît dès le boot sans Core.

Entrée distincte « JARVIS — T2 eGPU réserve PCIe 512M », source 45, ID jarvis-t2-egpu-reserve-512m, préparée uniquement dans le dossier utilisateur. Lanceur et candidat syntaxiquement vérifiés ; diff limité au bloc ajouté. Empreintes système avant/après identiques. Aucun GRUB modifié, génération système, pilote, module, PCIe, rescan, i915/VFIO/EFI, débranchement ou redémarrage.

Analyse, risques et plan détaillé : [mission04I.md](../04I/mission04I.md). Installation, préparation d’un boot sans Core, reboot et unique branchement surveillé sont des étapes soumises à leurs accords explicites. Debian reste le défaut et les secours/T2/Intel/SSH sont conservés par le plan. Ce suivi ne valide pas encore le paramètre 512M en fonctionnement.

---

# Mission 04H — Réallocation PCIe vérifiée sur l’hôte

**11 octobre 2026, 21:18 CEST. C — Réallocation inefficace dans cet essai.** Accès privilégié hôte fonctionnel ; boot `[UUID EXPURGÉ]`, noyau 6.18.54-1-t2-trixie, blacklist Nouveau et pci=realloc=on confirmés. Core autorisé, branchement journalisé à 21:16:12. Quadro identifiée dynamiquement par 10de:1eb0 à 0000:81:00.0.

BAR 0 attribué à 0x90000000–0x90ffffff (16 Mio), présent dans iomem et couvert par tous les parents. BAR 1 (256 Mio) et BAR 3 (32 Mio) restent non attribués, resource 0/0/0 ; échecs répétés can't assign/no space/failed to assign. Chaîne 00:01.2 → 7b:00.0 → 7c:01.0 → 7f:00.0 → 80:01.0 → 81:00.0. Fenêtres préchargeables identiques à 04E : 224/224/112/100 Mio, absente au pont final. Le décalage de +1 Mio de trois fenêtres NP n’améliore pas l’allocation GPU.

Nouveau absent et explicitement bloqué au hotplug ; aucun module graphique NVIDIA chargé. Pas d’erreur AER/DPC ou faute DMAR explicite repérée ; avertissements DROM Thunderbolt consignés. i915/DP-3 et Ethernet 1 Gbit/s établis ; SSH actif et trois connexions distantes restent ESTAB après branchement. Bureau réactif confirmé par l’utilisateur.

Rapport : [mission04H.md](../04H/mission04H.md), preuves dans mission04H-preuves/20261011-211801/. Ce résultat lève les réserves d’accès du bilan 04G et remplace le statut courant du test. Aucune modification système, pilote, module NVIDIA, écriture PCIe, CUDA, débranchement ou redémarrage. Seuls rapports et preuves écrits.

---

# Mission 04G — Vérification avec pci=realloc=on, accès incomplet

**11 octobre 2026, vers 21:10 CEST. Statut actuel : D — test non concluant.** Noyau `6.18.54-1-t2-trixie`, `pci=realloc=on` et `module_blacklist=nouveau` confirmés sur le boot accessible `[UUID EXPURGÉ]`. Branchement du Core annoncé par l’utilisateur, mais aucun `10de:1eb0` ni Core externe visible dans la collecte restreinte. Chaîne complète, BAR et couverture après branchement non vérifiables. Les fenêtres préchargeables hôtes visibles restent 224/112 Mio ; fenêtres NP décalées de +1 Mio à taille constante par rapport à 04E, sans causalité établie.

Réessai d’élévation demandé : sudo -n id réussit seul par une commande préapprouvée ; les collectes sudo restent bloquées par no new privileges. Exécution PCIe hors sandbox rejetée par la politique d’approbation automatique (sandbox_approval=false). Journaux noyau/Bolt, SSH et iomem non masqué indisponibles ; aucune absence d’erreur ou de tentative NVIDIA au cours du boot n’est affirmée. Nouveau et modules NVIDIA absents ; i915/Intel DP-3 actif, Ethernet lien 1 Gbit/s. Confirmation interactive GNOME/SSH et heure de branchement encore attendues.

Rapport détaillé : [mission04G.md](../04G/mission04G.md). Preuves : `mission04G-preuves/collecte-restreinte-20261011/`, avec erreurs d’accès et empreintes. Aucun avant-branchement de ce même boot retrouvé. Les preuves 04E restent une référence d’un autre démarrage, où BAR 1/3 échouaient. Une collecte hôte privilégiée après branchement est nécessaire pour conclure A/B/C. Aucun module chargé, pilote installé, CUDA, écriture PCIe, redémarrage, débranchement ou modification de configuration. Seuls rapports et preuves écrits.

Cette section remplace le statut courant de l’essai des sections historiques ci-dessous ; elle ne démontre pas une correction de l’incident eGPU.

---

# Mission 04E — Preuves archivées et entrée réallocation installée

**11 octobre 2026. Préparation puis génération et installation explicitement autorisées pendant cette mission. Aucun redémarrage ni débranchement exécuté.** Ce bilan remplace les restrictions et états historiques précédents. Le test du Core avec Nouveau désactivé a été effectué par l’utilisateur ; il confirme GNOME réactif et accès SSH fonctionnel.

Boot actuel : [UUID EXPURGÉ] ; noyau 6.18.54-1-t2-trixie ; ligne diagnostic sans pci=realloc=on. Core autorisé et connecté, Quadro RTX 5000 0000:81:00.0, 10de:1eb0. GPU : lien 8 GT/s ×4 ; ceci décrit son lien local, pas le débit de bout en bout (certains ponts/tunnels annoncent d’autres vitesses). Nouveau absent de lsmod, aucun pilote lié au GPU, journal à 20:49:49 : Module nouveau is blacklisted. Intel 00:02.0 reste lié à i915, boot_vga=1. Ethernet enp4s0 UP à [ADRESSE PRIVÉE EXPURGÉE]/24 ; service/socket SSH actifs, écoute conservée. Confirmation SSH et réactivité fournie par l’utilisateur.

Branchement daté par journaux autour de 20:49:48–20:49:49 CEST. Journaux complets noyau/système/Bolt conservés ainsi que les extraits depuis le branchement (heure journalctl short-iso-precise ; les heures boltctl peuvent être affichées en UTC). Ressources sysfs, PCI complet/arbre, chaque pont de la chaîne, BAR, modules, réseau et SSH archivés dans `mission04E-preparation/preuves-20261011-205427/`, et archive tar.gz avec empreinte SHA-256.

Chaîne menant au GPU : `00:01.2 → 7b:00.0 → 7c:01.0 → 7f:00.0 → 80:01.0 → 81:00.0`.

| PCI | Mémoire non préchargeable | Mémoire préchargeable |
|---|---|---|
| 0000:00:01.2 | `0x8f900000–0x9dafffff` (226 Mio) | `0xbf400000–0xcd3fffff` (224 Mio) |
| 0000:7b:00.0 | `0x8f900000–0x9dafffff` (226 Mio) | `0xbf400000–0xcd3fffff` (224 Mio) |
| 0000:7c:01.0 | `0x8fb00000–0x96afffff` (112 Mio) | `0xbf400000–0xc63fffff` (112 Mio) |
| 0000:7f:00.0 | `0x90000000–0x961fffff` (98 Mio) | `0xc0000000–0xc63fffff` (100 Mio) |
| 0000:80:01.0 | `0x90000000–0x910fffff` (17 Mio) | Absente |

BAR 0 attribué : 0x90000000–0x90ffffff (16 Mio), décodage mémoire actuellement désactivé sans pilote. BAR 1 (256 Mio) et BAR 3 (32 Mio) : ressources sysfs nulles, échecs répétés can't assign; no space et failed to assign dans le journal. Le pont 80:01.0 n’a pas de fenêtre préchargeable ; demande de fenêtre 0x12000000 (288 Mio), également refusée. Les fenêtres amont 224/112/100 Mio ne peuvent couvrir simultanément les 288 Mio demandés ; l’alignement et les autres périphériques restent à considérer. La suppression du gel par blacklist ne résout pas l’allocation.

Entrée **JARVIS — T2 eGPU réallocation PCIe**, ID `jarvis-t2-egpu-reallocation`, installée via `/etc/grub.d/44_jarvis_t2_egpu_reallocation` et remplacement contrôlé du GRUB actif par le candidat généré. Arguments : `quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on`. Noyau et initramfs T2 exacts. Diagnostic précédent inchangé, Debian 6.12.111 par défaut, menu 15 s, secours Debian 6.12.111/6.12.107 et recovery conservés. Aucun changement global, i915, VFIO, initramfs, service ou réseau.

Sauvegarde configuration complète et empreintes avant conservées. `grub-mkconfig` exécuté après accord vers un fichier de test dans une isolation avec système en lecture seule, sources copiées superposées, thème copié adapté pour comparer le cache existant au lieu de le réécrire, verrous LVM locaux. Dernière génération code 0, identique octet pour octet au candidat. Essais d’isolation antérieurs non retenus conservés, jamais installés. Diff final **strictement limité à l’ajout du bloc 44**. Installation ensuite explicitement autorisée : source root:root 0755 et grub.cfg root:root 0600. Syntaxe active code 0, SHA-256 actif `5682492e9f0f28f894a7f43cdde5eb3913c73f66c4052d7acd1381ee8a27e75c`. Toutes les autres empreintes système protégées inchangées ; grubenv inchangé, aucun next_entry. GPU encore présent et boot ID inchangé après installation.

Fichiers : `44_jarvis_t2_egpu_reallocation`, `entree-grub-prevue.cfg`, `grub.cfg-candidat`, `grub.cfg-genere-test`, `grub-diff-exact.patch`, `grub-diff-genere.patch`, `validation-preparation.txt`, `validation-installation.txt`, `empreintes-avant.json`, `sauvegarde/`, `fenetres-ponts.md`, `collecte-lecture-seule.py`, `plan-essai-et-retour-arriere.md` dans mission04E-preparation.

Le plan prévoit comparaison des fenêtres au démarrage puis après branchement, identification dynamique par ID GPU, archives distinctes, flux SSH système/GNOME et accès indépendant, critères BAR 1/3 attribués et absence d’erreurs, récupération seulement après accord, retour arrière ciblé et conservation des secours. **Installation terminée. Autorisation distincte de redémarrage attendue. Aucun débranchement/rebranchement préautorisé.** Le paramètre n’est pas actif sur le boot actuel et son effet n’est pas encore testé.

---

# Suivi — SSH et désactivation de la veille, 11 octobre 2026 20:43 CEST

SSH et ssh.socket actifs ; Ethernet [ADRESSE PRIVÉE EXPURGÉE]/24, route via [ADRESSE PRIVÉE EXPURGÉE]. Bannières OpenSSH obtenues localement sur [ADRESSE PRIVÉE EXPURGÉE]:22 et [ADRESSE PRIVÉE EXPURGÉE]:22 ; ce test ne valide pas le chemin depuis un autre poste. Règles nftables vides. Configuration effective : clés autorisées, mots de passe interdits, root interdit, utilisateur adminjarvis autorisé depuis localhost ou [ADRESSE PRIVÉE EXPURGÉE]/24. Connexion distante réussie à 20:00:02 depuis [ADRESSE PRIVÉE EXPURGÉE] ; tentative depuis cette même adresse fermée avant authentification à 20:17:50, sans cause précise établie. Erreur client demandée pour poursuivre le diagnostic ; aucune configuration SSH modifiée.

Suspension constatée de 20:18:58 à 20:19:39. À la demande explicite de désactivation de veille, réglages GNOME sleep-inactive-ac-type et sleep-inactive-battery-type passés à nothing, puis cibles sleep/suspend/hibernate/hybrid-sleep/suspend-then-hibernate masquées avec systemctl mask. Relecture : deux valeurs nothing et cinq cibles masked. Changement persistant, sans reboot. Cette action autorisée constitue une exception au périmètre de lecture seule des validations antérieures. Core toujours non autorisé.

---

# Mission 04C — Recontrôle avec droits élevés

**11 octobre 2026, 19:59–20:00 CEST. Cette section remplace les réserves d’accès du bilan précédent.** À la demande de l’utilisateur, reprise des contrôles avec élévation : `sudo -n id` confirme uid=0. Même boot ID `[UUID EXPURGÉ]`, aucun redémarrage.

| Contrôle | Résultat actuel |
|---|---|
| Script de vérification | Réexécuté : code 0, sept contrôles OK. |
| Noyau / blacklist / Nouveau | `6.18.54-1-t2-trixie` ; `module_blacklist=nouveau` présent et unique ; Nouveau absent, i915 chargé et Intel lié à i915, boot_vga=1. |
| Affichage principal | Display-manager actif, session locale seat0/tty1 non idle. Journal GNOME à 19:56:18 : card0 (i915) ajouté en atomic mode setting, renderer GBM créé, GPU boot VGA choisi comme primaire. DP-3 connecté/activé confirmé précédemment. La réactivité interactive reste une observation à confirmer par l’utilisateur. |
| Ethernet et IP | enp4s0 UP, `[ADRESSE PRIVÉE EXPURGÉE]/24`, route par défaut via `[ADRESSE PRIVÉE EXPURGÉE]`, source `[ADRESSE PRIVÉE EXPURGÉE]`. Lien 1 Gbit/s confirmé précédemment. |
| SSH | Service actif depuis 19:55:57, configuration précontrôlée avec succès par sshd -t ; écoute effective sur `[ADRESSE PRIVÉE EXPURGÉE]:22` et `[ADRESSE PRIVÉE EXPURGÉE]:22`. Journal : authentification publickey réussie d’adminjarvis depuis `[ADRESSE PRIVÉE EXPURGÉE]` à 20:00:02, session ouverte. L’accès distant depuis cette adresse est donc démontré sur ce boot ; l’identité de ce client comme Mac de travail n’est pas déduite de l’adresse seule. |
| PCIe / NVMe / Thunderbolt | Journal noyau désormais accessible. Aucun message critique ciblé AER/fatal, DPC containment, échec d’allocation BAR, timeout/reset/I/O error NVMe, échec/timeout Thunderbolt, panic, BUG, tâche bloquée ou faute DMAR repéré jusqu’au contrôle à 20:00. |
| Avertissements matériels | Deux messages Thunderbolt `device links to tunneled native ports are missing!` et NVMe `using unchecked data buffer` présents au démarrage ; mêmes messages retrouvés dans le boot T2 de l’incident `47896394d801461483a770ad6f5faecc`. Ils ne sont donc pas nouveaux et ne prouvent pas une correction du futur hotplug. |
| GRUB actif | `grub-script-check /boot/grub/grub.cfg` : code 0. SHA-256 `10434b2acdcf83cbab77e1d20fa5eb4981cc724c150b434c62bc841126a39080`, exactement identique après installation. Entrée diagnostic et ses arguments/initramfs présents. Debian 6.12.111 reste le choix par défaut ; menu normal 15 s ; grubenv sans next_entry. |
| Secours Debian | Entrées normales et recovery 6.12.111 et 6.12.107 conservées dans le GRUB actif. Images/initramfs présents et empreintes identiques, comme vérifié au contrôle précédent. Aucun démarrage de secours retesté. |

Le journal n’est pas exempt de tous avertissements : erreurs ACPI AE_AML_BUFFER_LIMIT/AE_ALREADY_EXISTS et IOAPIC, échec intel-lpss IRQ, avertissements CPU/SMT, firmwares et interfaces Wi-Fi/Bluetooth, modules T2 staging. Les messages ACPI et IOAPIC cités sont également retrouvés dans le boot T2 antérieur. i915 initialise le framebuffer primaire ; un message de désactivation eDP faute d’informations de lien est présent, tandis que la sortie DP-3 et le renderer GNOME sont établis. Aucune conclusion d’innocuité globale n’est tirée de ces avertissements.

**Bilan : contrôles techniques locaux du démarrage diagnostic conformes, réseau et accès SSH distant démontrés, aucun nouvel incident critique ciblé repéré.** Reste à confirmer humainement la réactivité du bureau et, pour la suite, l’identité du client SSH et le fonctionnement de la collecte distante. **Le branchement du Razer Core reste non autorisé ; aucun redémarrage.** La validation de ce boot ne démontre pas que l’allocation PCIe au branchement sera corrigée.

Contrôles exclusivement en lecture seule. Seul ce rapport est mis à jour ; aucun changement de service, module, GRUB, réseau, EFI ou paramètre PCIe.

---

# Mission 04C — Validation après démarrage diagnostic

**11 octobre 2026, 19:58–20:00 CEST. Validation partielle ; aucun branchement du Razer Core autorisé.** Cette section constitue le bilan actuel ; les sections suivantes sont conservées comme historique. Le démarrage a été effectué par l’utilisateur. Aucun redémarrage exécuté ici.

Boot ID : `[UUID EXPURGÉ]`.

## Contrôles réalisés en lecture seule

Le script `mission04C-preparation/verification-apres-demarrage.sh` a été lu puis exécuté avec `sh` : **code de sortie 0, sept contrôles OK**.

Ligne de commande active :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau
```

| Contrôle | Résultat et preuve |
|---|---|
| Noyau actif | Conforme : `6.18.54-1-t2-trixie`, confirmé par le script et `uname -r`. |
| Blacklist | `module_blacklist=nouveau` présent, une seule occurrence de l’argument blacklist ; arguments IOMMU et pm_async attendus présents. |
| Nouveau | Absent de `/sys/module/nouveau` et de `lsmod`. Aucune tentative de charge provoquée. |
| Intel | PCI `0000:00:02.0` UHD 630 lié à i915, i915 chargé, `boot_vga=1`, framebuffer `i915drmfb`. |
| Affichage principal | `card0-DP-3` connecté et activé, modes dont 1920×1080 ; autres sorties désactivées. Journal utilisateur : GNOME Wayland atteint à 19:56:19, GNOME Shell démarré, applications ouvertes ensuite. Fonctionnement graphique étayé ; réactivité visuelle et interactive actuelle à confirmer par l’utilisateur. |
| Ethernet | `enp4s0` : operstate `up`, carrier `1`, vitesse `1000` Mbit/s ; pilote PCI `tg3`. |
| IP [ADRESSE PRIVÉE EXPURGÉE] et SSH | **Non vérifiés sur l’hôte** : `ip` et `ss` refusent netlink ; `systemctl` refuse le bus système. `/proc/net` ne montre que le réseau isolé du sandbox, et les processus visibles sont ceux du sandbox : cela ne prouve pas une absence de réseau/sshd sur l’hôte. Connexion SSH depuis le Mac non testée. |
| PCIe, NVMe, Thunderbolt : erreurs critiques | **Absence non démontrée** : journal noyau inaccessible. `journalctl -b -k` affiche un avertissement d’accès limité puis « No entries », qui ne constitue pas un journal vide vérifié. `sudo -n journalctl` refusé par `no new privileges`. NVMe en état sysfs `live`, pilote `nvme` présent ; deux domaines Thunderbolt et leurs contrôleurs présents, aucun périphérique externe Thunderbolt ni GPU NVIDIA dans l’inventaire accessible. Ces états ne remplacent pas les journaux. |
| Noyaux Debian de secours | Images et initramfs `6.12.111+deb13-amd64` et `6.12.107+deb13-amd64` présents ; SHA-256 identiques aux empreintes après installation. Images/initramfs T2 également identiques. Leur capacité à démarrer n’a pas été retestée. |
| Configuration GRUB | `/etc/default/grub`, `99-jarvis-t2.cfg`, source T2 précédente et source diagnostic : empreintes identiques après installation. Surcharge conservée : Debian 6.12.111 par défaut, menu 15 s. Source diagnostic correcte, grubenv lisible sans variable ni next_entry. **grub.cfg actif inaccessible (Permission denied)** : contenu, empreinte et syntaxe actuels non revérifiables ; la validation d’installation conservée reste une preuve historique. |

Le journal utilisateur contient notamment un avertissement d’enregistrement GNOME auprès de GDM, des avertissements clavier/xkbcomp et de réglages XSettings. Ils sont consignés sans les assimiler à des erreurs PCIe/NVMe/Thunderbolt ni conclure à leur innocuité globale.

## Bilan avant poursuite

**Le boot diagnostic et l’isolation actuelle de Nouveau sont conformes. La validation complète avant essai matériel reste inachevée**, faute d’accès aux contrôles système ci-dessus et de confirmation interactive de l’écran. Ne pas brancher le Razer Core. Aucun redémarrage ni changement de configuration demandé ou exécuté.

Pour compléter les preuves depuis un terminal hôte disposant déjà des droits nécessaires (commandes non exécutées ici) :

```sh
ip -br address show enp4s0
ip route
systemctl is-active ssh
systemctl status ssh --no-pager
ss -ltn
sudo journalctl -b -k -o short-iso-precise --no-pager
sudo grub-script-check /boot/grub/grub.cfg
sudo sha256sum /boot/grub/grub.cfg
sudo cat /boot/grub/grub.cfg
```

Comparer l’empreinte GRUB à `10434b2acdcf83cbab77e1d20fa5eb4981cc724c150b434c62bc841126a39080`, vérifier les entrées Debian normales/recovery et diagnostic, puis examiner le journal complet pour AER/DPC, échecs BAR, timeouts/reset NVMe, erreurs Thunderbolt, panic et blocages. Depuis le Mac : `ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'uname -r; cat /proc/sys/kernel/random/boot_id'` ; contrôler le même boot ID. Confirmer aussi la réactivité du bureau. Ces vérifications ne constituent pas une autorisation de branchement.

Seule écriture de cette mission : mise à jour de ce rapport, conformément à la demande. Tous les contrôles système sont en lecture seule ; aucun pilote chargé/déchargé, service modifié, paramètre PCIe écrit, changement GRUB ou intervention EFI.

---

# Mission 04C — Entrée GRUB installée et vérifiée

**11 octobre 2026, 19:47 CEST. Accord utilisateur « oui » pour l’installation uniquement.** Cette mise à jour remplace le statut « non installée » des sections de préparation conservées plus bas.

Entrée **JARVIS — T2 eGPU diagnostic sans Nouveau**, ID `jarvis-t2-egpu-sans-nouveau`, installée par ajout de `/etc/grub.d/43_jarvis_t2_egpu_diagnostic` (root:root, 0755) puis génération d’un candidat et installation contrôlée de `/boot/grub/grub.cfg` (root:root, 0600, mode d’origine).

Arguments propres à cette entrée : `quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau`, noyau et initramfs `6.18.54-1-t2-trixie`. Aucun argument i915/VFIO ni correction PCIe ajouté.

Vérifications réalisées avant et après installation :

- État initial identique aux empreintes de préparation ; copies grub.cfg et grubenv actualisées avant le lot.
- `grub-mkconfig` exécuté vers `mission04C-preparation/grub.cfg-candidat`, pas directement vers le fichier actif. os-prober désactivé par le défaut existant, aucun changement de configuration pour cela.
- Syntaxe GRUB du candidat puis du fichier actif validée par `grub-script-check`.
- Diff **strictement limité** au bloc de la nouvelle source et son entrée ; le retrait de ce bloc restitue exactement l’ancien grub.cfg. Toutes les anciennes entrées et le choix par défaut restent identiques.
- **Debian 6.12.111 reste le défaut**, menu 15 s, aucune modification grubenv/next_entry. Les deux secours Debian sont conservés.
- Empreintes des trois images noyau, trois initramfs, paramètres GRUB globaux et source T2 précédente identiques avant/après. Contenu grubenv inchangé. Source installée identique au fichier préparé.

Seuls le nouveau script grub.d et grub.cfg ont été modifiés côté configuration système. Aucun grub-install, intervention EFI, modification de service/réseau, initramfs, charge/décharge de pilote ou écriture PCI. Aucun redémarrage ou rebranchement ; le noyau actif reste Debian `6.12.111+deb13-amd64`.

**Le blocage effectif de Nouveau au boot diagnostic reste à vérifier après un redémarrage explicitement autorisé.** La vérification en lecture seule, les commandes SSH depuis le Mac et la récupération restent celles du plan `mission04C-preparation/plan-installation-et-essai.md`. Une entrée installée et syntaxiquement valide ne prouve pas un démarrage réussi. Ne pas brancher le Core avant validation du boot diagnostic, de l’accès SSH depuis le Mac, d’i915 et de la collecte distante.

Preuves : `mission04C-preparation/grub.cfg-avant-installation`, `grubenv-avant-installation`, `installation-diff.patch`, `empreintes-apres-installation.txt`, `validation-installation.txt` et candidat. Aucun retour arrière nécessaire ; sauvegarde ciblée disponible si un lot de retrait/restauration est autorisé ultérieurement.

**Statut : installation terminée ; redémarrage et essai matériel non autorisés.**

---

# Mission 04C — Préparation de l’entrée T2 eGPU sans Nouveau

Préparation du 11 octobre 2026. **Cette section remplace la préparation transitoire proposée en Mission 04B. L’utilisateur valide le principe d’isolation, mais pas le reboot ni le branchement. L’installation de l’entrée reste soumise à son prochain accord.**

État vérifié : Debian 6.12.111 actif et choix par défaut conservé via 99-jarvis-t2.cfg, menu 15 s, grubenv vide. Noyaux/images/initramfs Debian 6.12.107 et 6.12.111 conservés. i915 chargé, Intel lié à i915 et boot_vga=1 ; aucune proposition ne blacklist i915 ni ne lie Intel à VFIO. Nouveau et i915 sont présents dans l’initramfs T2 ; aucune modification de cette image prévue.

Fichiers préparés sous `mission04C-preparation/` : source exacte `43_jarvis_t2_egpu_diagnostic`, aperçu `entree-grub-prevue.cfg`, vérificateur en lecture seule `verification-apres-demarrage.sh`, plan détaillé `plan-installation-et-essai.md`, copie `grub.cfg-avant`, liste initramfs et empreintes. Nouvelle source absente de /etc/grub.d et ID absent du GRUB actif : **entrée non installée**.

Validation de préparation : syntaxe du lanceur shell et du texte GRUB vérifiée séparément ; vérificateur shell/Python syntaxiquement valide ; grub.cfg actuel valide. Empreintes avant/après identiques pour les trois noyaux, trois initramfs, grub.cfg, paramètres globaux et entrée T2 précédente. Aucun grub-mkconfig, update-grub, reboot, branchement, écriture PCI ou charge de module exécuté.

Le plan exact suit ; les scripts et commandes d’installation/essai qui y figurent sont des propositions, non des actions réalisées.

# Mission 04C — Plan exact, non exécuté

## Fichiers et modification proposée

Source préparée : `/home/adminjarvis/JARVIS/rapports/mission04C-preparation/43_jarvis_t2_egpu_diagnostic`.
Destination nouvelle : `/etc/grub.d/43_jarvis_t2_egpu_diagnostic`, propriétaire root:root, mode 0755.
Titre : **JARVIS — T2 eGPU diagnostic sans Nouveau**.
ID : `jarvis-t2-egpu-sans-nouveau`.

Le fichier reprend les chemins, UUID du /boot et racine LVM de l’entrée T2 déjà installée. Il ajoute une entrée distincte, sans modifier la précédente. Contenu exact :

```sh
#!/bin/sh
exec tail -n +3 "$0"
menuentry 'JARVIS — T2 eGPU diagnostic sans Nouveau' --class debian --class gnu-linux --class gnu --class os --id jarvis-t2-egpu-sans-nouveau {
    load_video
    insmod gzio
    if [ x$grub_platform = xxen ]; then insmod xzio; insmod lzopio; fi
    insmod part_gpt
    insmod ext2
    search --no-floppy --fs-uuid --set=root [UUID EXPURGÉ]
    linux /vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau
    initrd /initrd.img-6.18.54-1-t2-trixie
}
```

Les `insmod` ci-dessus sont des commandes du chargeur GRUB pour lire/comprimer le noyau, pas des commandes de charge de pilotes Linux. Aucun argument ne bloque i915 ni ne lie Intel à VFIO.

Deux modifications système prévues après accord : création de ce fichier, puis remplacement contrôlé de `/boot/grub/grub.cfg` par sa version régénérée contenant la nouvelle entrée. Aucun autre fichier système à modifier. Les paramètres globaux, le choix par défaut, grubenv, EFI, noyaux, initramfs, modprobe.d et services restent identiques.

Défaut déjà effectif, conservé tel quel :

```text
gnulinux-advanced-[UUID EXPURGÉ]>gnulinux-6.12.111+deb13-amd64-advanced-[UUID EXPURGÉ]
```

Menu 15 s ; aucune sélection automatique du diagnostic, aucun grub-reboot/set-default, aucune modification grubenv. À la lecture actuelle, grubenv est vide, donc aucun next_entry ne supplante le défaut. Les images/initramfs Debian 6.12.111 et 6.12.107 sont présentes, avec leurs entrées normales et recovery. La nouvelle entrée est persistante au menu, mais sa blacklist ne s’applique que lorsqu’elle est choisie ; cela remplace la proposition précédente d’une édition manuelle transitoire de la ligne GRUB.

## Installation proposée après autorisation — pas un script exécuté

1. Relire les états et vérifier qu’aucune configuration n’a changé depuis la préparation. Confirmer que la destination n’existe toujours pas. Actualiser les sauvegardes et empreintes ; ne pas écraser un fichier créé entre-temps.
2. Installer la seule nouvelle source :

```sh
sudo -n install -o root -g root -m 0755 /home/adminjarvis/JARVIS/rapports/mission04C-preparation/43_jarvis_t2_egpu_diagnostic /etc/grub.d/43_jarvis_t2_egpu_diagnostic
```

3. Générer d’abord un fichier candidat dans les rapports, sans toucher au grub.cfg actif :

```sh
sudo -n grub-mkconfig -o /home/adminjarvis/JARVIS/rapports/mission04C-preparation/grub.cfg-candidat
sudo -n grub-script-check /home/adminjarvis/JARVIS/rapports/mission04C-preparation/grub.cfg-candidat
sudo -n diff -u /boot/grub/grub.cfg /home/adminjarvis/JARVIS/rapports/mission04C-preparation/grub.cfg-candidat
```

La génération exécute les scripts existants de grub.d : les relire avant exécution, notamment l’état os-prober et les scripts locaux. Aucun grub-mkconfig/update-grub exécuté pendant cette préparation. Si une génération demande une modification de montage/EFI inattendue, arrêter et présenter l’écart.

4. Exiger un diff limité au bloc `43_jarvis_t2_egpu_diagnostic` et son entrée ; vérifier Debian par défaut, anciennes entrées, paramètres globaux et paths inchangés. En cas d’autre écart, arrêter avant remplacement actif et examiner la cause. Ne pas accepter automatiquement une régénération plus large.
5. Après ces contrôles, installer le candidat en reprenant exactement propriétaire/mode du grub.cfg d’origine (mesurés au moment du lot), puis vérifier à nouveau la syntaxe et les empreintes des images, initramfs et configurations conservées. Aucune commande `grub-install`, `efibootmgr`, mise à jour initramfs ou redémarrage.

La préparation actuelle a déjà vérifié le lanceur shell (deux premières lignes) avec `sh -n`, le vérificateur shell/Python par contrôle syntaxique, et `grub-script-check` sur le bloc GRUB extrait et sur le grub.cfg d’origine : succès. Le script grub.d mélange un lanceur shell et du texte GRUB : `sh -n` sur le fichier entier refuse le bloc GRUB, comme pour l’entrée T2 existante ; chaque langage est donc contrôlé séparément. Cela valide la syntaxe, pas un démarrage réel ni le fonctionnement du GPU.

## Vérification de Nouveau avant tout branchement

Nouveau et i915 sont tous deux présents dans l’initramfs T2. **Le fichier Nouveau ne sera pas supprimé de l’initramfs.** `module_blacklist=nouveau` est un paramètre du noyau, qui interdit la charge du module, y compris si la tentative vient de l’initramfs. CONFIG_DRM_NOUVEAU=m : ce n’est pas un pilote compilé en dur. [Documentation Linux 6.18](https://raw.githubusercontent.com/torvalds/linux/v6.18/Documentation/admin-guide/kernel-parameters.txt).

Après un démarrage explicitement autorisé et sélection manuelle de la nouvelle entrée :

```sh
sh /home/adminjarvis/JARVIS/rapports/mission04C-preparation/verification-apres-demarrage.sh
sudo -n journalctl -b -k -o short-iso-precise --no-pager
/usr/sbin/lsmod
readlink /sys/bus/pci/devices/0000:00:02.0/driver
cat /sys/bus/pci/devices/0000:00:02.0/boot_vga
```

Le script préparé est en lecture seule. Il exige noyau T2 exact, les quatre arguments demandés, une seule blacklist, absence de `/sys/module/nouveau`, présence d’i915, Intel lié à i915 et boot_vga=1. Tout échec interdit de poursuivre l’essai. Il n’est pas exécuté sur le boot Debian actuel, qui ne correspond pas à la cible.

Ne pas utiliser `modprobe nouveau` comme test : cela demanderait une charge de module. Ne pas confondre le dry-run modprobe, l’absence actuelle de module avec Core absent, ou la présence du fichier dans l’initramfs avec une preuve de blocage effectif. Après le futur hotplug autorisé, vérifier de nouveau l’absence du module et d’un lien `driver` Nouveau sur le GPU PCI identifié par 10de:1eb0. Des messages de refus/blacklist dans le journal apporteraient une preuve positive supplémentaire ; leur absence ne suffit pas à invalider le paramètre si aucune tentative de charge n’a eu lieu.

L’écran reste branché directement au Mac mini, pas au Core. Vérifier GNOME/i915 comme GPU primaire dans le journal et la réactivité du bureau. `boot_vga=1` est un indice firmware, pas à lui seul une preuve du GPU de rendu du compositeur.

## Surveillance depuis le Mac de travail — commandes préparées

L’hôte Linux écoute actuellement sur [ADRESSE PRIVÉE EXPURGÉE]:22, Ethernet intégré enp4s0 UP. **Une connexion depuis le Mac reste à effectuer par l’utilisateur et à confirmer.** Un login historique ne valide pas l’accès sur le prochain boot. Adresse DHCP à recontrôler si elle change ; ne pas changer SSH ou réseau dans ce lot.

Avant chaque essai, ouvrir deux connexions indépendantes, exécuter la vérification en lecture seule et vérifier le login publickey côté Linux. Les commandes ci-dessous s’exécutent sur le Mac ; la création de fichiers est locale au Mac. Elles ne sont pas lancées ici.

```sh
mkdir -p ~/JARVIS-mission04C
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'uname -r; cat /proc/cmdline; ip -brief address; cat /proc/sys/kernel/random/boot_id'
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'sh /home/adminjarvis/JARVIS/rapports/mission04C-preparation/verification-apres-demarrage.sh'

# Export complet avant l’essai, car le suivi ne remplace pas l’historique.
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'sudo -n journalctl -b -o short-iso-precise --no-pager' > ~/JARVIS-mission04C/avant-systeme.log 2>&1
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'lspci -nnk; lspci -t; boltctl list; boltctl domains' > ~/JARVIS-mission04C/avant-materiel.log 2>&1

# Terminal distinct A : conserver le flux système en temps réel.
ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=3 adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'sudo -n journalctl -b -f -o short-iso-precise --no-pager' > ~/JARVIS-mission04C/suivi-systeme.log 2>&1

# Terminal distinct B : flux de la session utilisateur, incluant GNOME.
ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=3 adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'journalctl --user -b -f -o short-iso-precise --no-pager' > ~/JARVIS-mission04C/suivi-session.log 2>&1

# Terminal distinct C : deuxième accès indépendant pour les contrôles.
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE]
```

Avant branchement, regarder depuis une autre fenêtre Mac `tail` des fichiers et vérifier l’absence d’erreur SSH/sudo/journalctl. Les redirections masquent la sortie à l’écran : un fichier créé n’est pas une preuve de collecte valide. Arrêter si le flux ne fonctionne pas ; ne pas élargir automatiquement les droits. Les timestamps journal suivent l’heure configurée sur Linux ; conserver le boot ID.

Les fichiers portent des noms fixes : les archiver dans un nouveau dossier avant un autre essai pour ne pas écraser les preuves. Arrêter les clients de suivi avec Ctrl-C après collecte ; cela ne touche pas les services Linux. Capturer aussi après l’essai `sudo journalctl -b`, `sudo lspci -nnvv`, `/proc/iomem`, ressources sysfs du GPU/ponts et `lsmod`, sans écritures PCI.

## Récupération si le graphique se fige

1. Ne pas charger/décharger de pilote ni redémarrer GNOME Wayland. Garder les flux Mac et utiliser la connexion indépendante.
2. Si SSH répond, capturer immédiatement :

```sh
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'date -Is; cat /proc/sys/kernel/random/boot_id; ps -eo pid,comm,stat,wchan:32; /usr/sbin/lsmod' > ~/JARVIS-mission04C/gel-processus.log 2>&1
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'sudo -n journalctl -b -o short-iso-precise --no-pager' > ~/JARVIS-mission04C/gel-systeme.log 2>&1
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'sudo -n lspci -nnvv; sudo -n cat /proc/iomem' > ~/JARVIS-mission04C/gel-ressources.log 2>&1
```

3. Arrêter l’essai et convenir de la récupération : un reboot propre par SSH nécessite un accord explicite, ou une autorisation de récupération donnée avant le futur essai. Aucune commande reboot n’est exécutée/préautorisée maintenant.
4. Si SSH ne répond pas, attendre les délais clients puis constater si la panne est graphique ou globale à partir des preuves disponibles. Une courte pression du bouton a déclenché une suspension lors de l’incident : ne pas la traiter comme un redémarrage. Un arrêt matériel est un dernier recours à convenir avant le test, avec risque de perte de données ; aucun arrêt matériel demandé ici.
5. Après arrêt/redémarrage autorisé, prévoir un retour Core absent sur Debian 6.12.111, ou 6.12.107 dans les options avancées. La nouvelle entrée n’étant pas le défaut, elle ne sera pas choisie automatiquement. Aucun effacement du noyau T2 ou des secours.

La politique Bolt du Core reste auto : tout futur rebranchement peut déclencher rapidement l’autorisation et l’énumération. Ne le faire qu’après nouvelle validation de l’essai, après vérification SSH/blocage/collecte. L’installation de l’entrée seule n’autorise ni boot ni connexion du Core.

## Retour arrière de l’installation, si nécessaire

Avant installation, les copies et empreintes sont dans ce dossier. Après installation, si la régénération ou ses contrôles échouent, enlever uniquement le nouveau fichier créé par le lot, puis remettre le grub.cfg sauvegardé avec ses propriétaire/mode d’origine si le fichier actif a été remplacé. Ne toucher à aucun autre script. Vérifier la syntaxe, le défaut Debian et les empreintes ; aucune intervention EFI. Procédure à exécuter dans le périmètre du lot approuvé, pas maintenant.

Pour retirer ultérieurement une entrée validée, supprimer uniquement cette source et régénérer/contrôler GRUB dans un lot autorisé. Aucun retour arrière n’efface des images/initramfs.

## Statut et périmètre d’accord demandé

**Préparation terminée ; entrée non installée.** L’accord attendu porte uniquement sur l’installation de `/etc/grub.d/43_jarvis_t2_egpu_diagnostic`, la génération/validation d’un candidat, puis son installation dans `/boot/grub/grub.cfg`, avec retour arrière ciblé si nécessaire. Il exclut reboot, branchement, PCIe, chargement de pilotes, initramfs, paramètres globaux, sélection du boot, EFI et réseau.


---

# Mission 04B — Ressources PCIe et plan de correction proposé

Diagnostic du 11 octobre 2026, 19:06–19:12 CEST. **Cette section est la synthèse la plus récente.** Lecture des rapports Mission 04 et incident, inventaires locaux, comparaison des journaux Debian/T2 et recherche documentaire. Seuls le rapport et ses preuves utilisateur sont écrits. Aucun système, pilote, module, service, GRUB, EFI ou paramètre PCIe modifié ; aucun reboot, rebranchement ou compilation exécuté.

## Résultat principal

**Le domaine Thunderbolt de l’incident offre 224 Mio de mémoire préchargeable, et son port utilisé seulement 112 Mio. La Quadro demande 256 Mio + 32 Mio pour BAR 1/3 : les fenêtres existantes ne peuvent pas les accueillir.** Ces limites préchargeables sont identiques sous Debian 6.12.111 et T2 6.18.54. Ce n’est pas un déficit de RAM système ni de numéros de bus.

**Nouveau peut se charger automatiquement sur les deux noyaux.** Le module T2 déclare 30 chemins de firmwares TU104, tous absents du système. L’initialisation graphique a échoué au branchement. Cela confirme deux obstacles, mais ne prouve pas lequel a bloqué GNOME. Le premier essai proposé isole Nouveau ; les essais suivants traitent l’allocation, séparément.

## Phase 1 — Ressources, contraintes et comparaison

Chaîne lors de l’incident :

```text
00:01.2 -> 7b:00.0 -> 7c:04.0 -> b8:00.0 -> b9:01.0 -> ba:00.0 Quadro
                                          -> b9:04.0 -> bb:00.0 USB du Core
```

Les adresses après le port Thunderbolt pourront changer lors d’un prochain boot ; l’identification de la carte devra utiliser `10de:1eb0` et son chemin sysfs, sans supposer `ba:00.0` permanent. NVIDIA répertorie **1EB0 comme Quadro RTX 5000** : l’identification annoncée est désormais corroborée par les journaux PCI. [NVIDIA, produits pris en charge](https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/supportedchips.html).

| Pont / ressource | T2, avant branchement | Debian actuel | Taille / conséquence |
|---|---|---|---|
| 00:01.2, fenêtre préchargeable | bf400000–cd3fffff | identique | 224 Mio pour le domaine1 |
| 7b:00.0, fenêtre préchargeable | bf400000–cd3fffff | identique | Même limite amont, fenêtres imbriquées, non additives |
| 7c:01.0, autre branche | bf400000–c63fffff | identique | 112 Mio |
| 7c:04.0, branche du Core | c6400000–cd3fffff | identique | 112 Mio, insuffisant même pour BAR 1 seul |
| 00:01.2 et 7b:00.0, mémoire non préchargeable | 8f900000–9dafffff | 8fa00000–9dbfffff | 226 Mio, décalage de 1 Mio, pas un agrandissement |
| 7c:04.0, non préchargeable | 96b00000–9dafffff | 96c00000–9dbfffff | 112 Mio dans les deux cas |
| Bus sous 7c:04.0 | b8–f0 | b8–f0 | 57 numéros de bus ; pas d’épuisement de bus enregistré |
| Racine PCI, grande fenêtre | 4000000000–7fffffffff | identique | Fenêtre hôte de 256 Gio ; son existence ne garantit pas son routage derrière tous les ponts |

L’autre contrôleur Thunderbolt présente une répartition comparable de 224 Mio en deux branches de 112 Mio. Changer de port sans autre correction ne constitue donc pas une solution démontrée.

Le BAR de 256 Mio exige aussi un placement aligné ; la somme 288 Mio n’est qu’un minimum de capacité, pas la taille suffisante de toute fenêtre dans n’importe quel placement. Le journal demande jusqu’à `0x12300000` (291 Mio) pour la branche et échoue. Une réservation de 512 Mio serait une valeur expérimentale avec marge, jamais une garantie, et pourrait être demandée pour plusieurs ports simultanément.

**Ponts où l’échec est explicitement enregistré :** `7c:04.0`, `b8:00.0`, `b9:01.0` et `b9:04.0`. **Contraintes amont :** `00:01.2` et `7b:00.0` n’offrent que 224 Mio. Leur fenêtre commune est inférieure aux besoins totaux du GPU : élargir seulement le dernier pont ne suffit pas. Les journaux montrent des libérations/réessais dans le sous-arbre, sans succès final pour BAR 1/3.

La lecture actuelle `lspci -vv` affiche `[32-bit]` pour les fenêtres situées sous 4 Gio. Une vérification supplémentaire, **sans écriture**, par `setpci` retourne `bf41/cd31` pour les registres base/limite de `00:01.2` et `7b:00.0`, `c641/cd31` pour `7c:04.0`, avec les parties hautes à zéro. Le type bas vaut 1, indiquant une fenêtre préchargeable de type 64 bits dans les registres. On ne conclut donc pas à une impossibilité matérielle de dépasser 4 Gio sur ces ponts à partir du seul affichage lspci. Le routage complet, y compris les ponts externes absents actuellement, reste à valider.

Le code PCI amont 6.18 prévoit une réallocation de sous-arbre et des réessais, et ne peut pas libérer indistinctement les fenêtres contenant des ressources déjà affectées. Il ne garantit pas le déplacement à chaud de toute la hiérarchie active. Cette lecture du code explique pourquoi les réessais visibles ne prouvent pas qu’un espace hôte pourtant disponible a pu être rendu accessible au GPU. [Linux 6.18, setup-bus.c](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/pci/setup-bus.c). Le noyau T2 peut comporter des correctifs : analyse amont, pas preuve d’identité de tout son code.

### Paramètres actuellement présents

| Point | Boot Debian actuel | Boot T2 de l’incident |
|---|---|---|
| Noyau | 6.12.111+deb13-amd64 | 6.18.54-1-t2-trixie |
| Arguments supplémentaires | `quiet` | `quiet intel_iommu=on iommu=pt pm_async=off` |
| Type IOMMU observé | Translated, invalidation lazy | Passthrough |
| Réallocation PCI compilée | CONFIG_PCI_REALLOC_ENABLE_AUTO=y | identique |
| Nouveau compilé | module | module |
| Protection DMA Thunderbolt | attributs = 0 | attributs = 0 dans capture initiale |

L’IOMMU et le remapping IRQ sont initialisés sous Debian selon le journal, même sans option `intel_iommu=on` explicite. Aucune faute DMAR n’a été enregistrée lors de l’incident. IOMMU ne crée pas d’espace d’adressage BAR : modifier ce réglage n’est pas la correction prioritaire.

Aucun `pci=realloc`, réserve hotplug personnalisée ou `pcie_ports=native` dans les deux lignes de commande. Le port hotplug a pourtant détecté la carte et le retrait. ASPM est déjà affiché désactivé sur le lien examiné. Pas d’indice justifiant d’ajouter des paramètres d’énergie en bloc.

GRUB conserve une entrée dédiée `jarvis-t2-6.18.54-test` avec les trois arguments T2 de l’incident. Les entrées T2 génériques n’ont que `quiet` : pour un essai comparable, sélectionner l’entrée dédiée. Le défaut configuré reste Debian 6.12.111, menu visible 15 s. Images et initramfs Debian 6.12.107, 6.12.111 et T2 présents ; empreintes conservées dans `boot-hashes-avant.txt`. Aucune modification.

### Pourquoi Nouveau se charge, et firmwares manquants

- La configuration effective `modprobe --showconfig` ne contient aucun blocage ni option Nouveau. Aucune règle spécifique trouvée dans modprobe.d, modules-load.d ou initramfs-tools.
- Les aliases PCI du module correspondent à la carte. La simulation `modprobe -n -v -b` sur l’alias NVIDIA aboutit à `nouveau.ko.xz`, pour Debian comme pour T2. **L’option -n garantit ici la simulation : aucun module chargé.**
- Le module Nouveau est inclus dans l’initramfs T2. CONFIG_DRM_NOUVEAU=m ; actuellement aucun module Nouveau/NVIDIA chargé, i915 actif. La carte absente ne déclenche pas sa charge.
- `firmware-nvidia-graphics` n’est pas installé ; candidat local 20250410-2. Le paquet déjà installé `firmware-misc-nonfree` ne fournit pas les chemins TU104 requis observés.
- Audit de tous les chemins `nvidia/tu104/` déclarés par modinfo T2 : **30 absents**, y compris variantes compressées .xz/.zst. Liste intégrale dans `firmwares-tu104.txt`.

Chemins importants absents : `tu104/nvdec/scrubber.bin`, les cinq fichiers ACR, les treize fichiers GR, les trois SEC2, et les quatre fichiers GSP pour chacune des versions 535.113.01 et 570.144. Le journal mentionne GR/SEC2 indisponibles et l’absence de scrubber ; modinfo ne permet pas de dire que chaque fichier déclaré a été demandé dans cette tentative. Le message PMU ne donne pas un nom de fichier exact : ne pas inventer un fichier PMU manquant.

La liste officielle du paquet Debian contient TU104 ACR/GR/SEC2/scrubber et un lien de dossier GSP vers les fichiers 535.113.01 ; elle ne liste pas 570.144. Le module T2 déclare aussi 535, mais le chemin réellement choisi et son fonctionnement devront être testés. Installer ce paquet ne résoudrait pas les BAR et n’est pas proposé dans le premier essai. [Debian, fichiers de firmware-nvidia-graphics](https://packages.debian.org/trixie/all/firmware-nvidia-graphics/filelist).

### Recommandations documentées et limites

T2Linux déclare Thunderbolt fonctionnel et propose `pcie_ports=native` si nécessaire. Ce conseil ne certifie pas un eGPU donné ; ici l’autorisation et l’énumération réussissent déjà. [État des fonctions T2Linux](https://wiki.t2linux.org/state/).

Un auteur décrit le même plafond de 224 Mio sur **Macmini8,1**, pour un RX 6800 sous Ubuntu/T2 7.0.9. Son contournement utilise écritures PCI et module de réparation des ressources. Il désactive aussi l’affichage Intel par VFIO. Ce retour d’expérience concorde avec notre mesure, mais cible AMD et un autre noyau : **ne pas transposer son script, ses adresses ni sa configuration**, qui contreviendraient à la préservation d’Intel. [Retour d’expérience et code de l’auteur](https://github.com/philmcneely/t2-egpu-linux/blob/main/README.md).

La documentation NVIDIA 580 prend en charge les eGPU mais ne garantit pas la stabilité d’un retrait en cours d’utilisation. Ses règles d’écrans Xorg ne constituent pas une garantie pour GNOME Wayland. [NVIDIA, GPU externes](https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/egpu.html).

Pour la Quadro Turing, NVIDIA 580.119.02 documente les modules ouverts et propriétaires, mutuellement exclusifs ; les ouverts nécessitent GSP. Ce sont des candidats matériels, pas une certification du couple exact T2 6.18.54/Razer. [Variantes NVIDIA](https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/kernel_open.html). Les sources de cette version annoncent les noyaux 4.15 et suivants et une interface à construire pour le noyau cible ; cette plage générale ne prouve pas que la compilation et le chargement réussiront sur notre build T2. [Sources NVIDIA 580.119.02](https://raw.githubusercontent.com/NVIDIA/open-gpu-kernel-modules/580.119.02/README.md).

Aucune source primaire consultée ne valide exactement Macmini8,1 + Quadro RTX 5000 + ce noyau T2. La branche 580 reste une piste, **version de référence, pas sélection définitive du paquet actuel**. Les en-têtes T2 existent et DKMS est vide. APT actuel ne propose pas nvidia-driver/nvidia-kernel-dkms. Il faudra examiner un dépôt officiel, les versions disponibles et une simulation sans suppression avant tout changement. Une compilation isolée pourra vérifier l’API après accord ; installation, chargement et test restent des validations distinctes. [Guide NVIDIA Debian](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/debian.html).

## Phase 2 — Solutions séparées et risques

Les paramètres ci-dessous sont **évalués, non appliqués**. La documentation Linux décrit `pci=realloc=on` pour redimensionner des allocations de ponts insuffisantes et `pci=hpmmioprefsize=512M` pour réserver de la mémoire préchargeable hotplug. `pci=resource_alignment=...` peut cibler un pont. `module_blacklist=nouveau` interdit la charge du module. `pci=nocrs` ignore les fenêtres ACPI et `assign-busses` renumérote les bus. [Paramètres Linux 6.18](https://raw.githubusercontent.com/torvalds/linux/v6.18/Documentation/admin-guide/kernel-parameters.txt).

| Solution | Intérêt / ordre proposé | Risques et effet Intel | Retour arrière prévu |
|---|---|---|---|
| Interdiction Nouveau pour **un seul boot** | Premier test : isoler l’initialisation graphique, sans réparer les BAR | Risque faible à modéré, reboot et hotplug toujours susceptibles de gel. Intel i915 reste chargé ; aucune accélération NVIDIA attendue | Éditer seulement la ligne GRUB en mémoire avec `module_blacklist=nouveau`. Au boot suivant sans cet ajout, effet disparu ; pas de fichier ni initramfs modifié |
| `pci=realloc=on`, un seul boot | Après isolation, première tentative standard d’agrandissement amont | Modéré : peut déplacer des ressources d’autres périphériques. Réallocation automatique déjà compilée ; effet non garanti. Intel peut subir un problème d’allocation/affichage | Supprimer l’ajout à l’essai suivant ; démarrer Debian de secours, Core absent |
| Réservation `pci=hpmmioprefsize=512M` | Essai suivant si réallocation seule insuffisante, Nouveau toujours bloqué | Modéré : demande appliquée à plusieurs ports ; peut dépasser les fenêtres amont et augmenter les échecs. Ne crée pas à elle seule la fenêtre hôte/routage | Paramètre d’un boot uniquement ; l’omettre au prochain boot. Conserver les autres réglages testés identiques |
| Core connecté **avant démarrage** | Tester l’allocation lorsque toute la topologie est visible tôt ; après essai hotplug isolé | Modéré : peut bloquer boot ou affichage avant SSH. Sans BootACL (0/0), l’autorisation OS peut arriver après l’allocation initiale, donc bénéfice non garanti | Arrêt propre si possible, retour Core absent puis boot Debian. Ne pas modifier EFI ni inscrire une BootACL pour cet essai |
| Alignement/réaffectation ciblée par paramètre | Si échec des options standard, étudier un pont précis et la chaîne complète | Élevé : adresses peuvent changer ; redimensionnement peut affecter autres périphériques. Paramètre exact à préparer à partir des résultats, pas un wildcard global | Omettre au boot suivant et revenir au secours ; aucune écriture sysfs d’alignement proposée |
| Installer firmware-nvidia-graphics | Si décision séparée de poursuivre Nouveau après résolution PCIe | Modéré : nouvelle voie d’initialisation graphique, risque de nouveau gel, pas de réparation des fenêtres | Inventaire/backup des fichiers, retrait du seul lot ajouté après revue, initramfs restauré/régénéré si modifié par le paquet. Pas de purge globale |
| NVIDIA ouvert, paquet DKMS | Candidat Turing ultérieur pour calcul, après BAR corrects | Modéré à élevé : GSP, DKMS/API 6.18, conflits Nouveau, hooks initramfs, bibliothèques et intégration graphique. Garder i915 et écran sur Mac | Sauvegarde avant lot, revenir Debian/Core absent, désactiver uniquement le chargement NVIDIA selon plan, retirer les paquets ajoutés et restaurer configurations/initramfs approuvés |
| NVIDIA propriétaire, paquet DKMS | Alternative séparée si le choix ouvert est inadapté | Même risques d’installation ; firmware/GSP dépend du mode et version. Aucun avantage certain pour l’allocation BAR | Même procédure ciblée ; ne jamais mélanger les deux variantes/modules/bibliothèques de versions différentes |
| Écritures `setpci`, rescan/retrait sysfs, module correcteur privé | Dernier recours de développement si solutions standard échouent | Très élevé : incohérence ressources noyau/matériel, corruption, panne NVMe/Intel/réseau, gel. Non retenu dans le plan initial | Reboot sans correcteur et restauration des fichiers ajoutés ne garantissent pas récupération des données en cas de corruption ; ne pas improviser ce lot |

Ni `pcie_ports=native`, ni ASPM/PM, ni IOMMU ne seront ajoutés dans le premier test. Si une trace ultérieure justifie chacun, l’évaluer séparément. `pci=nocrs`, `pci=assign-busses`, `acpi=off`, `iommu=off` ne sont pas proposés : pas de preuve que les fenêtres hôtes, numéros de bus ou DMA sont le défaut à corriger. `pci=big_root_window` vise AMD, donc inadapté à ce Mac Intel.

**Affichage Intel à préserver dans tous les lots :** écran branché directement au Mac, i915 non blacklisté, aucune liaison VFIO de `8086:3e9b`, aucun nvidia-xconfig, aucune règle faisant de NVIDIA le GPU principal, aucun écran sur le Core pendant l’isolation. La préservation physique/configuration ne garantit pas l’absence de gel du compositeur lors de l’énumération ; le suivi SSH reste nécessaire.

## Phase 3 — Premier test concret, non autorisé à ce stade

**Hypothèse unique : la tentative d’initialisation Nouveau contribue au gel du bureau.** Comparaison avec le boot incident T2, mêmes trois arguments IOMMU/PM, même port et câble si identifiables, même hotplug ; seule variable de pilote : interdiction Nouveau. Les erreurs BAR resteront probablement présentes. Aucun `pci=realloc`, firmware ou pilote NVIDIA ajouté. Le but n’est pas d’obtenir un GPU fonctionnel.

### Préalables obligatoires

1. **Tester SSH depuis le Mac administrateur**, sur Ethernet intégré `enp4s0`, IP actuelle `[ADRESSE PRIVÉE EXPURGÉE]`. Les services et écoutes sont actifs, mais aucun login depuis le Mac n’est enregistré sur le boot actuel ; le succès historique à 18:26 sur le boot précédent ne suffit pas. Nous ne pouvons pas initier un test depuis le Mac à sa place. Vérifier une nouvelle connexion et une seconde session indépendante, puis confirmer dans journalctl `Accepted publickey` avec la bonne source. Éviter Ethernet du Core, Wi-Fi, mot de passe transmis ou changement de configuration SSH.
2. Sauvegarder le travail du bureau. Confirmer l’écran Intel et le Core actuellement déconnecté. Vérifier menu de secours visible, les trois images/initramfs et clavier utilisable au menu.
3. **Après accord explicite de reboot**, démarrer l’entrée dédiée T2 avec ajout transitoire `module_blacklist=nouveau` à sa ligne `linux` via la touche e de GRUB. Ne pas enregistrer cette édition. Ligne attendue :

```text
/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau
```

4. **Avant toute connexion du Core**, contrôler `uname -r`, `/proc/cmdline`, i915 actif, Nouveau absent, nouveau login SSH du Mac sur ce boot T2 et bureau réactif. Tout écart arrête l’essai. Le retour à T2 est nécessaire pour comparer à l’incident ; un essai Debian sans Nouveau changerait aussi le noyau et l’IOMMU, et ne permettrait pas la même conclusion.
5. Démarrer deux collectes distantes sur le Mac ; vérifier que les sorties arrivent réellement. Commandes proposées uniquement, non exécutées :

```sh
# Sur le Mac, vérifier l’accès et le noyau, dans une première session.
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'uname -r; cat /proc/cmdline; ip -brief address'

# Deuxième session : journal complet du boot, puis suivi (fichier sur le Mac).
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'sudo -n journalctl -b -f -o short-iso-precise --no-pager' > mission04B-suivi-systeme.log 2>&1

# Troisième session : conserver le journal utilisateur GNOME et son suivi.
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] 'journalctl --user -b -f -o short-iso-precise --no-pager' > mission04B-suivi-session.log 2>&1
```

Les fenêtres dédiées à la collecte restent ouvertes ; une quatrième connexion sert au diagnostic. Si sudo non interactif échoue, arrêter et choisir une lecture autorisée après validation, pas modifier les droits. Les commandes de suivi peuvent manquer des événements anciens sans export préalable complet : capturer également `sudo journalctl -b` et les inventaires avant connexion.

Captures avant/après : `lspci -nnvv`, `lspci -t`, `boltctl list/domains`, `/proc/iomem`, ressources sysfs du GPU et de tous ses ponts, modules chargés, unités GNOME et processus. Toujours retrouver le GPU par `10de:1eb0`. Conserver début/fin, boot ID et heure du branchement annoncée par l’utilisateur.

### Déroulement après validation du test et signal de préparation

Une seule connexion du premier Core, sur le port de l’incident identifié par domain1/7d:00.0 ; aucun second boîtier. Observer au moins 60 s si système stable. Si BAR échoués, arrêt du diagnostic fonctionnel : aucun chargement manuel de pilote, aucune correction à chaud, aucun second branchement automatique. Collecter les ressources et tester depuis le Mac la réponse SSH pendant l’observation.

| Résultat | Interprétation et décision |
|---|---|
| Nouveau absent, BAR échoués, bureau réactif | Compatible avec une contribution de Nouveau au gel. PCIe reste défectueux ; préparer l’essai séparé de réallocation. Une seule répétition ne prouve pas la causalité |
| Nouveau absent, bureau encore figé | Nouveau n’est pas nécessaire au gel ; examiner PCIe/vgaarb/i915/GNOME avec les preuves distantes |
| BAR attribués malgré réglages PCIe inchangés | Allocation dépendante de l’état/énumération possible ; relever toutes les fenêtres, pas déclarer Nouveau réparateur PCIe |
| Nouveau présent | Isolation invalide : arrêter et analyser avant autre tentative |
| SSH perdu, panic/lockup ou erreurs stockage | Arrêt immédiat du plan d’essai ; récupération et collecte avant toute reprise |

### Récupération prévue

Si le bureau fige mais SSH répond : garder la collecte, capturer `ps -eo pid,comm,stat,wchan:32`, `journalctl -b`, l’état GNOME et les ressources PCI. Ne pas redémarrer GNOME Wayland ni décharger i915/Nouveau. Un redémarrage propre par SSH est une action de récupération **à autoriser explicitement**, pas automatiquement exécutée. L’état de montage/stockage sera contrôlé avant cette action.

Si SSH ne répond plus : ne pas utiliser une courte pression du bouton comme si elle demandait un reboot ; elle a déclenché une suspension lors de l’incident. La procédure de dernier recours par arrêt matériel doit être convenue avant l’essai, avec risque de perte des écritures. Ce cas n’autorise aucun arrêt/reboot automatique ici.

Retour de secours : après arrêt autorisé, Core absent, démarrer Debian 6.12.111 (ou 6.12.107 si nécessaire) depuis le menu existant, sans l’argument transitoire. Une édition GRUB non enregistrée disparaît au prochain boot. Ne supprimer aucun noyau ni fichier d’origine.

### Essais suivants, chacun soumis à un nouvel accord

Une fois Nouveau maintenu bloqué comme contrôle : tester `pci=realloc=on` seul comme nouvelle variable, d’abord vérifier les fenêtres au boot sans Core puis une connexion surveillée. Si insuffisant, évaluer la réserve hotplug ou le démarrage Core connecté, **dans des essais différents**. Un essai Core déjà connecté doit documenter l’heure d’autorisation Bolt par rapport au scan PCI pour savoir s’il a réellement testé une topologie visible au démarrage. Ne jamais cumuler d’emblée réallocation, réserve, changement IOMMU, changement de pilote et cold-plug.

**Statut final : Phase 1 terminée sur les preuves accessibles, phases 2 et 3 préparées. SSH Mac sur le prochain boot, corrections, reboot et rebranchement restent en attente de validation utilisateur.** Le risque classé « faible à modéré » décrit la portée des changements ; il ne garantit pas la stabilité du test.

Contrôle final à 19:12 : empreintes avant/après identiques pour les trois images, les trois initramfs et grub.cfg ; i915 toujours chargé, Nouveau/NVIDIA absents, Bolt indique Core déconnecté.

Preuves locales : `mission04B-preuves/` (PCI Debian complet, arbre, iomem, noyau Debian, modinfo des deux noyaux, configuration modprobe effective, simulations d’alias, liste des 30 firmwares absents, registres des ponts, paramètres GRUB, liste initramfs T2, état SSH et empreintes boot). Journaux T2 complets conservés dans `mission04-incident-preuves/`. Les essais dry-run et lectures de registres ont été utilisés sans charge de module ni écriture PCI.

---

# JARVIS — Mission 04 : diagnostic complété du gel eGPU

Mise à jour : 11 octobre 2026, 18:59 CEST. Lecture système désormais accessible avec `sudo -n`. **Cette synthèse remplace les conclusions provisoires de la première lecture, conservées plus bas comme historique.** Aucun changement système, reboot ou rebranchement effectué.

## Conclusion actualisée

Le branchement a déclenché **un échec confirmé d’allocation des ressources PCIe**, suivi d’un **échec confirmé du pilote Nouveau**. Ce sont les anomalies principales à traiter avant un nouvel essai. Le lien exact avec le blocage GNOME reste une hypothèse : aucune pile bloquée du compositeur ni GPU HANG i915 n’est enregistrée.

Le système n’était pas entièrement arrêté à 18:43:21 : noyau, Bolt et services continuent à produire des événements, notamment lors de la déconnexion du Core à 18:45:19 et d’une demande de suspension à 18:46:59. Aucun kernel panic ou redémarrage automatique par watchdog n’est démontré. Un nouveau boot sous Debian débute ensuite à 18:48.

## Chronologie système confirmée

Boot incident : `47896394d801461483a770ad6f5faecc`, noyau `6.18.54-1-t2-trixie`. Bornes du journal système conservé : **18:11:00–18:47:00**, au lieu de la dernière trace utilisateur à 18:43:21. Le journal privilégié révèle aussi le boot `d2c66e2757ad4a4f8fbfd727b3fd4640`, 18:08:36–18:09:14, absent de la première liste limitée aux droits utilisateur.

| Heure CEST | Événement |
|---|---|
| 18:42:19 | Retrait d’un périphérique USB contenant le support Debian ; erreur de synchronisation du cache après retrait. Événement distinct, antérieur d’une minute au Core. |
| 18:43:20.492–.505 | Lecture DROM avec avertissements puis découverte `thunderbolt 1-3: Razer Core` sur le NHI `7d:00.0`, domain1. |
| 18:43:20.521558 | Bolt : `authorize: finished: ok (status: authorized, flags: 0)`. |
| 18:43:20.678680 | GPU PCI `ba:00.0`, identifiant `10de:1eb0`, découvert. |
| 18:43:20.688–.711 | Échecs répétés des fenêtres mémoire de ponts et des BAR 1/3 du GPU. |
| 18:43:21.032–.273 | Chargement automatique de Nouveau, GPU TU104, 16 Gio GDDR6, firmwares indisponibles et initialisation échouée. |
| 18:43:22–.27 | Énumération des hubs USB et Ethernet ASIX du Core ; services toujours actifs. |
| 18:45:19.020–.709 | Perte du lien PCIe et déconnexion Thunderbolt ; retrait des périphériques, erreurs xHCI/audio ; restauration des décodages VGA i915. |
| 18:46:59.651539 | `systemd-logind: Power key pressed short.` |
| 18:46:59.661254 | `The system will suspend now!` |
| 18:47:00.246929 | `systemd-sleep: Performing sleep operation 'suspend'...` ; fin des traces. |
| 18:48:06 | Boot actuel selon uptime, sous `6.12.111+deb13-amd64`. Première entrée système conservée : 18:48:13. |

La demande de suspension suit l’incident : les mentions `user.slice: Unit now frozen` à 18:47 relèvent de cette suspension, pas du gel initial. Aucune trace de reprise ni séquence d’arrêt normal n’est conservée après elle. Le passage de la suspension au nouveau boot n’est pas expliqué par ces seules traces.

## Erreurs PCIe : preuve principale

```text
18:43:20.688939 pci 0000:b8:00.0: bridge window [mem size 0x0d400000 64bit pref]: can't assign; no space
18:43:20.691028 pci 0000:b9:01.0: bridge window [mem size 0x12100000 64bit pref]: can't assign; no space
18:43:20.706649 pcieport 0000:7c:04.0: bridge window [mem size 0x12300000 64bit pref]: can't assign; no space
18:43:20.710802 pci 0000:ba:00.0: BAR 1 [mem size 0x10000000 64bit pref]: can't assign; no space
18:43:20.710961 pci 0000:ba:00.0: BAR 1 [mem size 0x10000000 64bit pref]: failed to assign
18:43:20.711123 pci 0000:ba:00.0: BAR 3 [mem size 0x02000000 64bit pref]: can't assign; no space
18:43:20.711459 pci 0000:ba:00.0: BAR 3 [mem size 0x02000000 64bit pref]: failed to assign
```

BAR 1 demande 256 Mio et BAR 3 32 Mio d’espace d’adressage PCIe préchargeable. Le noyau essaie plusieurs allocations sans succès enregistré pour ces deux BAR. D’autres ressources, dont BAR 0 et les fonctions audio/USB, sont assignées : cela explique la détection partielle sans GPU opérationnel. Ces messages ne décrivent pas un manque de RAM système.

Les messages `bridge configuration invalid ([bus 00-00]), reconfiguring` sont suivis d’une reconfiguration et d’une découverte de périphériques ; ils ne suffisent pas seuls à diagnostiquer un pont défectueux. Les échecs finaux de ressources, eux, sont explicites.

## Nouveau : tentative automatique et échec

```text
18:43:21.032953 nouveau 0000:ba:00.0: NVIDIA TU104 (164000a1)
18:43:21.268684 nouveau 0000:ba:00.0: pmu: firmware unavailable
18:43:21.268893 nouveau 0000:ba:00.0: gr: firmware unavailable
18:43:21.269079 nouveau 0000:ba:00.0: sec2: firmware unavailable
18:43:21.269261 nouveau 0000:ba:00.0: fb: 16384 MiB GDDR6
18:43:21.272684 nouveau 0000:ba:00.0: fb: VPR locked, but no scrubber binary!
18:43:21.272888 nouveau 0000:ba:00.0: bar: one-time init failed, -12
18:43:21.273449 nouveau 0000:ba:00.0: probe with driver nouveau failed with error -12
```

L’absence de pilote NVIDIA propriétaire ne signifie donc pas l’absence de tentative de pilote graphique : **Nouveau a été chargé automatiquement**. TU104, l’identifiant PCI et les 16 Gio constituent désormais des preuves matérielles supplémentaires cohérentes avec la carte annoncée. L’échec BAR PCIe et l’échec d’initialisation Nouveau se suivent ; les journaux ne départagent pas leurs contributions exactes, ni celles des firmwares absents, au gel du bureau.

## Thunderbolt, i915 et retrait

```text
18:43:20.494070 thunderbolt 0000:7d:00.0: 3: DROM data CRC32 mismatch (expected: 0xd7bf6269, got: 0xd7bf62e9), continuing
18:43:20.681625 i915 0000:00:02.0: vgaarb: VGA decodes changed: olddecodes=io+mem,decodes=none:owns=io+mem
18:45:19.022277 thunderbolt 1-3: device disconnected
18:45:19.708687 i915 0000:00:02.0: vgaarb: VGA decodes changed: olddecodes=none,decodes=io+mem:owns=io+mem
```

Avertissement DROM confirmé, mais le noyau poursuit et Bolt autorise correctement le périphérique. Il ne démontre pas à lui seul un câble défectueux. Le changement des décodages VGA i915 est observé au branchement et inversé au retrait ; son rôle dans le gel n’est pas prouvé.

Les erreurs xHCI `Controller not ready at resume -19`, `HC died`, `Host not accessible` et `Runtime PM usage count underflow`, ainsi que les erreurs HDMI ELD, arrivent **après la perte du lien à 18:45:19**. Elles ne doivent pas être présentées comme le déclencheur du gel de 18:43. La déconnexion est confirmée ; sa cause physique n’est pas déduite.

## Crash, GNOME et signatures recherchées

La recherche sur le journal noyau complet ne révèle aucun `GPU HANG`, soft lockup, hung task, Oops, kernel panic, erreur AER/DPC ou faute DMAR/IOMMU explicite. Aucun OOM enregistré. L’avertissement workqueue/Wi-Fi du boot reste antérieur au branchement. Aucun crash GNOME/Wayland/Xorg enregistré autour de l’événement ; le blocage du compositeur reste plausible sans preuve directe.

`sudo coredumpctl list` sur 18:42–18:48 : **No coredumps found**, sans restriction d’accès cette fois. `/var/lib/systemd/coredump` et `/sys/fs/pstore` sont vides. Au boot actuel, systemd-pstore a été ignoré parce que pstore était vide. Aucun rapport de crash conservé trouvé ; cela n’exclut pas un blocage sans crash ou une trace non persistée.

État Bolt actuel vérifié par D-Bus : **Razer Core disconnected**, UUID `[UUID EXPURGÉ]`, politique persistante `auto`, deux domaines en sécurité `user`, bootacl 0/0. Les heures 16:43:20 affichées par boltctl correspondent ici à 18:43:20 CEST dans journalctl.

## Recommandations actualisées

**Ne pas répéter maintenant le même branchement à chaud sans préparation.** L’étape suivante est une analyse en lecture seule des fenêtres de ponts PCIe et de la configuration actuelle, puis un plan concret pour gérer l’allocation et la tentative automatique de Nouveau. Une installation de pilote seule ne peut pas être considérée comme une solution démontrée aux échecs PCIe.

Toute proposition de changement de pilote, blacklist, ressources PCIe ou paramètres de démarrage devra être documentée et validée séparément ; aucune n’est appliquée ni prescrite à l’aveugle ici. Le passage au noyau Debian actuel constitue une différence à prendre en compte, pas une preuve de correction. Pour un futur essai validé : SSH Ethernet testé au préalable, collecte distante continue noyau/Bolt/GNOME et comparaison des BAR avant/après ; arrêt de l’essai si les erreurs d’allocation réapparaissent.

Les preuves nouvelles sont conservées dans `mission04-incident-preuves/` : `systeme-incident-complet.log`, `noyau-incident-complet.log`, `bolt-incident-complet.log`, `boots-systeme.txt`, `coredumps-systeme.txt`. Les neuf axes demandés ont désormais été examinés avec accès système ; la cause directe du gel GNOME et celle du redémarrage final restent non démontrées.

---

# Historique — Première lecture à accès restreint

Les restrictions et conclusions ci-dessous décrivent uniquement le premier passage. Elles sont remplacées par la synthèse actualisée ci-dessus.

# JARVIS — Mission 04 : incident au branchement du Razer Core

Diagnostic du 11 octobre 2026, commencé à 18:53 CEST (Europe/Paris, UTC+02:00).

## Conclusion et limites

**Redémarrage confirmé après l’incident. Détection du Razer Core et de sa fonction audio NVIDIA confirmée vers 18:43:20–18:43:21. Cause du gel non établie.** Le démarrage concerné est `47896394d801461483a770ad6f5faecc` (index -1 au moment du diagnostic), sous `6.18.54-1-t2-trixie`. La machine fonctionne maintenant sous le noyau Debian `6.12.111+deb13-amd64`.

Les journaux utilisateur, les traces Xorg et les métadonnées Bolt sont lisibles. Les journaux système/noyau de la fenêtre de l’incident ne sont pas accessibles depuis cette session restreinte. Une capture noyau antérieure, conservée par la préparation de Mission 04, a été examinée ; elle s’arrête avant le branchement. Il serait incorrect de conclure à l’absence d’erreur noyau pendant le gel.

Seules les écritures de ce rapport et de ses preuves dans le dossier utilisateur ont été effectuées. Aucun pilote, service, autorisation Thunderbolt, GRUB, EFI ou paramètre n’a été modifié ; aucun redémarrage ou branchement demandé/exécuté.

## 1. Démarrages et chronologie

`uptime -s` et `who -b` situent le démarrage actuel à **18:48:06**. `last -x` confirme le passage du noyau T2 au noyau Debian :

```text
reboot system boot 6.18.54-1-t2-tri Sun Oct 11 18:10 - crash
reboot system boot 6.12.111+deb13-a Sun Oct 11 18:48 - still running
```

La mention `crash` dans cet historique signifie qu’aucun arrêt normal correspondant n’est enregistré ; elle ne démontre ni kernel panic ni redémarrage automatique. L’origine du reboot (manuel, arrêt électrique, watchdog…) reste inconnue.

Extrait de `journalctl --list-boots`, bornes des seules entrées accessibles :

| Index | Identifiant | Première entrée | Dernière entrée |
|---|---|---|---|
| -3 | b79e816092ef4f14880cbd87c5b5fa36 | 15:25:36 | 17:51:40 |
| -2 | 2d7e0cbb167e42c0a628afaefd9ae832 | 17:52:52 | 18:07:44 |
| -1 | 47896394d801461483a770ad6f5faecc | 18:11:30 | 18:43:21 |
| 0 | 1496f370c89a4c39ad862be607eb7ec5 | 18:49:20 | démarrage actuel |

Ces bornes ne donnent pas les heures exactes du boot ou de l’arrêt. La capture noyau antérieure commence à 18:11:00 ; l’historique `last` arrondit à la minute.

Chronologie pertinente :

- 18:11:00–18:11:01 : initialisation T2, erreurs ACPI et avertissement Wi-Fi préexistants.
- 18:11:31 : GNOME Shell/Mutter 48.7 démarre comme serveur Wayland, GPU primaire Intel i915.
- 18:13:33 : erreur JavaScript GNOME, trente minutes avant l’incident.
- 18:38–18:40 : préparation Mission 04 ; aucune carte NVIDIA ni boîtier externe détecté dans les captures antérieures.
- **18:43:20.513935** : message GNOME d’auto-inscription du Core.
- **18:43:20** : heures de connexion et d’autorisation enregistrées par Bolt ; inscription persistante du Razer Core.
- **18:43:21.310124** : cible audio atteinte dans la session utilisateur.
- Vers 18:43:21 : quatre entrées audio NVIDIA apparaissent dans Xorg.
- Après 18:43:21 : aucune autre entrée accessible dans le journal utilisateur de ce boot. Cela ne date pas précisément le gel ni ne prouve un arrêt de tout le système.
- 18:48:06 : nouveau démarrage, noyau Debian.

## 2. Thunderbolt et événements juste avant le gel

Fenêtre examinée : 18:40 à la fin du journal accessible, puis recherche sur l’ensemble du boot identifié.

```text
2026-10-11T18:43:20+02:00 gnome-shell[1227]: thunderbolt: [Core] auto enrollment: yes (allowed: yes)
2026-10-11T18:43:21+02:00 systemd[1049]: Reached target sound.target - Sound Card.
```

La base `/var/lib/boltd/devices/[UUID EXPURGÉ]` contient :

```ini
[device]
name=Core
vendor=Razer
generation=3
type=peripheral
[user]
policy=auto
label=Razer Core
storetime=1791737000
```

`storetime` correspond à 18:43:20 CEST. Les fichiers `.conntime` et `.authtime` du même UUID ont également une date de modification à 18:43:20. **Une inscription persistante avec politique auto existe déjà**, issue de l’événement passé ; ce diagnostic ne l’a pas créée. Cela ne garantit pas que tout le tunnel PCIe a fonctionné correctement.

`/var/log/Xorg.0.log.old` identifie le noyau T2 et comporte :

```text
[ 1946.131] (II) config/udev: Adding input device HDA NVidia HDMI/DP,pcm=3 (/dev/input/event17)
[ 1946.131] (II) config/udev: Adding input device HDA NVidia HDMI/DP,pcm=9 (/dev/input/event20)
[ 1946.132] (II) config/udev: Adding input device HDA NVidia HDMI/DP,pcm=7 (/dev/input/event18)
[ 1946.132] (II) config/udev: Adding input device HDA NVidia HDMI/DP,pcm=8 (/dev/input/event19)
```

Les temps Xorg sont relatifs au boot. Le message GNOME a le temps monotone 1945.277262 s : les ajouts audio suivent d’environ **0,854 s**, cohérent avec la cible audio à 18:43:21. Les messages suivants « No input driver specified, ignoring this device » ne constituent pas une erreur du pilote GPU : ils concernent les entrées audio présentées au gestionnaire d’entrées Xorg.

Cela démontre une énumération au moins partielle d’une fonction NVIDIA. Cela ne vérifie pas le modèle Quadro RTX 5000, ses BAR, ni le pilote graphique chargé lors du branchement. Aucun journal PCIe de cette fenêtre n’est actuellement lisible.

## 3. GNOME, Wayland et Xorg

```text
18:11:31 gnome-shell[1227]: Running GNOME Shell (using mutter 48.7) as a Wayland display server
18:11:31 gnome-shell[1227]: Added device '/dev/dri/card0' (i915) using atomic mode setting.
18:11:31 gnome-shell[1227]: Boot VGA GPU /dev/dri/card0 selected as primary
18:13:33 gnome-shell[1227]: JS ERROR: TypeError: this.actor is null
  _syncEnabled@resource:///org/gnome/shell/ui/windowManager.js:144:25
  _destroyWindowDone@resource:///org/gnome/shell/ui/windowManager.js:1612:21
```

Erreur JavaScript confirmée, mais nettement antérieure : aucun lien causal établi. Les avertissements xkbcomp sont explicitement déclarés non fatals. Le journal montre aussi une erreur de permission geolocation et d’enregistrement GDM au démarrage, sans preuve qu’elles provoquent l’incident.

Aucun crash, arrêt ou délai d’attente de GNOME Shell n’est enregistré dans les entrées accessibles autour de 18:43. Aucun marqueur d’erreur `(EE)` réel, Fatal ou Backtrace n’a été retrouvé dans Xorg.0.log.old. Ce Xorg appartient à la session du gestionnaire SDDM, initialisée avant GNOME Wayland : il ne constitue pas le journal du compositeur Wayland ni une preuve que celui-ci répondait encore.

Le pointeur mobile avec fenêtres et menus inaccessibles est compatible avec un blocage du compositeur ou de la chaîne graphique. Ce symptôme ne permet pas d’exclure un blocage noyau partiel ; aucune pile du processus au moment du gel n’est disponible.

## 4. Noyau, ACPI et ressources PCIe

Source antérieure : `mission04-initial-20261011/noyau.log`, capturée avant branchement. Extraits :

```text
18:11:00 ACPI BIOS Error (bug): AE_AML_BUFFER_LIMIT, Field [CDW3] at bit offset/length 64/32 exceeds size of target Buffer (64 bits)
18:11:00 ACPI Error: Aborting method \_SB._OSC due to previous error (AE_AML_BUFFER_LIMIT)
18:11:00 ACPI Error: AE_ALREADY_EXISTS ... Table is already loaded
18:11:00 thunderbolt 0000:07:00.0: device links to tunneled native ports are missing!
18:11:00 thunderbolt 0000:7d:00.0: device links to tunneled native ports are missing!
18:11:00 i915 ... [ENCODER:105:DDI A/PHY A] failed to retrieve link info, disabling eDP
18:11:01 brcmfmac ... brcmf_pcie_setup: Dongle setup failed
18:11:01 ieee80211 phy0: brcmf_fw_crashed: Firmware has halted or crashed
18:11:01 WARNING: CPU: 9 PID: 73 at kernel/workqueue.c:4287 __flush_work+0x377/0x3a0
```

La pile de cet avertissement contient `cancel_work_sync`, `brcmf_bus_cancel_reset_work`, `brcmf_pcie_remove`, `brcmf_fw_request_done` et `request_firmware_work_func`. Elle correspond au problème Wi-Fi au démarrage, avant l’installation des firmwares de Mission 03. **Ce WARNING n’est pas une preuve de panic eGPU.**

La capture montre des fenêtres de ponts PCIe et des BAR assignés, notamment pour les contrôleurs hôtes ; aucun message explicite `failed to assign`, `no space`, `cannot assign` ou collision de ressources n’a été retrouvé. Ces allocations précèdent l’eGPU : ses ressources ne sont pas validées.

IOMMU activé sur le boot incident selon la capture et sa ligne de commande (`intel_iommu=on iommu=pt pm_async=off`), domaine par défaut Passthrough. Les attributs Thunderbolt de protection DMA valaient déjà 0 dans le diagnostic initial. Aucun lien causal établi avec le gel.

Recherche effectuée : thunderbolt, bolt, PCIe, AER, DPC, DMAR, IOMMU, i915, DRM, GPU HANG, watchdog, hung task/blocked for more, soft lockup, kernel panic, Oops et BUG/WARNING. Aucune signature de GPU HANG, panic, Oops, lockup, erreur AER/DPC ou faute DMAR n’a été identifiée **dans la capture antérieure et les entrées utilisateur lisibles**. Des mentions de watchdog sont de l’initialisation ou une liste de modules, pas un déclenchement. La fenêtre noyau de l’incident reste non examinable.

## 5. État actuel

- Noyau Debian `6.12.111+deb13-amd64`, ligne de commande `BOOT_IMAGE=/vmlinuz-6.12.111+deb13-amd64 root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet`. Elle diffère du boot incident ; l’état actuel ne valide pas le comportement du noyau T2.
- Deux NHI Intel JHL7540 `8086:15eb`, adresses `07:00.0` et `7d:00.0`, liés à `thunderbolt` ; ponts PCIe et USB hôtes présents.
- Sysfs Thunderbolt : seulement `0-0`, `1-0`, `domain0`, `domain1`, hôtes Apple Macintosh autorisés. Sécurité `user` ; `iommu_dma_protection=0` sur les deux domaines.
- Aucun Razer Core externe dans sysfs, aucune carte NVIDIA dans `lspci -nnk`. Seul GPU détecté : Intel UHD630 `8086:3e9b`, pilote i915. Cela indique l’absence actuelle de détection, sans prouver si le câble est physiquement retiré.
- `boltctl list` et `boltctl domains` échouent sur l’accès D-Bus : statut du service Bolt non vérifiable directement ici. L’inscription persistante du Core reste lisible.

## 6. Rapports de crash et restrictions d’accès

`/var/lib/systemd/coredump` et `~/.cache/kcrash-metadata` sont vides ; `/var/crash` n’existe pas. `coredumpctl list` indique « No coredumps found », mais signale aussi un échec d’accès au bus et la restriction du journal : aucune garantie exhaustive. `/sys/fs/pstore` refuse la lecture. Aucun rapport de crash de l’incident n’a donc été trouvé dans les sources accessibles.

`journalctl -k -b -1` et `journalctl -b -1 -u bolt` renvoient « No entries » avec l’avertissement d’accès limité. La lecture directe des fichiers système journal échoue avec `Permission denied` ; `dmesg` avec `Operation not permitted`. `sudo -n journalctl --list-boots` échoue parce que le contexte impose `no new privileges`. Aucun droit n’a été changé et aucun mécanisme de contournement utilisé.

Le fichier `system@…journal~`, daté de 18:47, est présent. Son suffixe et sa date seuls ne permettent pas de diagnostiquer une corruption ou la cause de l’arrêt ; son contenu est inaccessible.

## 7. Hypothèses et prochaines étapes

| Piste | Éléments disponibles | Statut |
|---|---|---|
| Blocage GNOME/Mutter ou chaîne i915/DRM au hotplug | Bureau figé avec pointeur mobile, proximité temporelle du hotplug | Plausible, non prouvé |
| Blocage noyau/PCIe/Thunderbolt lors de l’autorisation ou de l’énumération | Auto-inscription et apparition audio NVIDIA juste avant la fin des traces | Plausible, non prouvé |
| Échec d’allocation BAR, AER/DPC ou faute IOMMU | Aucune preuve accessible dans la fenêtre critique | À vérifier, non confirmé |
| Problème lié à un pilote graphique NVIDIA/nouveau | Aucun relevé du pilote de la carte pendant l’événement | Indéterminé |
| Erreurs ACPI ou avertissement Wi-Fi comme cause directe | Présents plus de 30 min avant, session utilisable ensuite | Lien causal non établi |
| Panic/watchdog provoquant le reboot | Redémarrage et absence d’arrêt normal dans last | Non confirmé |

**Diagnostic non validé pour un nouvel essai.** La priorité est de récupérer, dans un contexte hôte disposant déjà des droits nécessaires, les journaux système du boot exact, sans changer de configuration :

```sh
sudo journalctl -b 47896394d801461483a770ad6f5faecc --since '2026-10-11 18:42:00' --until '2026-10-11 18:48:00' -o short-iso-precise --no-pager
sudo journalctl -b 47896394d801461483a770ad6f5faecc -k -o short-iso-precise --no-pager
sudo journalctl -b 47896394d801461483a770ad6f5faecc -u bolt --no-pager
sudo coredumpctl list --since '2026-10-11 18:42:00' --until '2026-10-11 18:48:00' --no-pager
sudo ls -la /sys/fs/pstore
```

Examiner les pilotes réellement chargés, identifiants PCI, affectations BAR, erreurs AER/DPC/DMAR et piles bloquées ; comparer la fin du journal à un arrêt normal. Si aucune trace n’a été conservée, la cause restera indéterminée rétrospectivement.

Pour un essai ultérieur **uniquement après validation séparée du diagnostic**, prévoir une session SSH Ethernet préalablement testée et une collecte distante en continu des journaux noyau, Bolt et GNOME, avec horodatage. Relever PCI/sysfs avant et après et noter port, câble, alimentation et état de l’écran. Tenir compte de la politique Bolt `auto` déjà enregistrée. Aucun changement automatique de cette politique, de pilote ou de paramètre noyau n’est recommandé sans preuves complémentaires. Aucun rebranchement n’est demandé maintenant.

## Sources conservées

Dossier `mission04-incident-preuves/` : liste des boots, historique `last`, journal utilisateur du boot complet, événement JSON avec temps monotones, copie Xorg antérieure, métadonnées Razer Bolt, état sysfs actuel et inventaire PCI actuel. Capture noyau antérieure conservée dans `mission04-initial-20261011/noyau.log`. Les extraits ci-dessus restent distingués selon leur provenance et leur période.

---

## Suite proposée — en attente du prochain prompt utilisateur

À la demande de l’utilisateur, la suite est consignée ici sans être exécutée. Aucun nouvel essai de branchement n’est engagé.

Prochain diagnostic proposé, **entièrement en lecture seule et sans rebrancher le Razer Core** :

1. Lire les fenêtres mémoire réservées aux ponts PCIe/Thunderbolt actuellement détectés et les comparer aux besoins non satisfaits du GPU lors de l’incident : BAR 1 de 256 Mio et BAR 3 de 32 Mio, en tenant compte des fenêtres et contraintes d’alignement des ponts intermédiaires. Objectif : préciser où l’espace d’adressage disponible était insuffisant, sans confondre cet espace avec la RAM système.
2. Comparer les paramètres PCIe et la ligne de commande du noyau Debian actuel avec ceux du boot T2 de l’incident. Objectif : identifier les différences pertinentes pour l’allocation au branchement à chaud ; aucune différence ne sera considérée comme une correction sans validation.
3. Examiner les règles de chargement automatique de Nouveau, les éventuelles configurations modprobe et les firmwares disponibles. Objectif : expliquer la tentative automatique et les messages de firmware indisponible, sans charger/décharger de module ni installer de fichier.

À partir de ces lectures, préparer un plan d’essai qui vérifie une hypothèse précise, avec SSH Ethernet préalablement testé et surveillance distante des journaux. Un rebranchement immédiat dans des conditions non préparées pourrait reproduire le gel sans apporter suffisamment de preuves supplémentaires.

**Statut : diagnostic complémentaire proposé, non exécuté. Attente du prochain prompt utilisateur.** Aucun changement de pilote, service, politique Thunderbolt, GRUB, EFI ou paramètre noyau ; aucun redémarrage et aucune demande de rebranchement.

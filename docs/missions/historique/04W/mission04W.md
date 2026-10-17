> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission04W.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 04W : analyse du démarrage interrompu

Investigation du 12 octobre 2026, Europe/Paris. Lectures uniquement ; création du rapport et de ses preuves dans le répertoire utilisateur. Aucun démarrage, arrêt, branchement, changement de service/pilote, rescan, écriture PCI/DEVEN ou modification de GRUB/EFI/NVRAM/initramfs effectué pendant cette mission.

## 1. Résultat et identification

**Classe F : traces insuffisantes pour déterminer si Linux a commencé à exécuter cet essai.** Aucun boot ID conservé n’est attribuable au démarrage manuel interrompu 04V. La dernière étape attestée pour cet essai est G1 dans GRUB, après chargements linux/initrd déclarés réussis, avec DEVEN=0x3F à deux reprises. L’exécution humaine de `boot` et les clignotements sont des observations utilisateur ; ils ne prouvent ni l’entrée dans le noyau, ni ExitBootServices réussi, ni une boucle de redémarrage.

Le boot `41984ede628649dcbb6c2fbd189b6869` (index -1 au relevé système) appartient à **04U et à la préparation 04V**, pas au nouvel essai. Cette attribution est corroborée par mission04U.md et mission04V.md, qui donnent explicitement ce boot ID, et par ses sessions SSH pendant leur rédaction. Sa fin est un arrêt propre. Ses messages PCI/Thunderbolt/EFI ne sont donc pas les messages de l’incident.

Le boot courant `d8f67bdef785436599ed1af19afe9620` est compatible avec la **récupération sans Core** décrite par l’utilisateur : Intel présent, i915 initialisé, réseau et SSH fonctionnels, aucune détection Razer Core dans son journal noyau. Son rattachement à la récupération repose aussi sur le récit utilisateur ; les journaux seuls n’attestent pas le débranchement physique. Noyau courant : `6.18.54-1-t2-trixie`.

### Horloges : correction indispensable

Les heures FIRST/LAST de journald sont les heures des premières/dernières entrées conservées, pas nécessairement les heures réelles de mise sous tension/extinction. Le boot courant indique un RTC initial à **2020-01-08**, puis systemd avance l’heure au timestamp sauvegardé **2026-10-12 15:08:20 CEST**. À **t=36,459665 s**, timesyncd synchronise à **16:09:47,428062 CEST**. La reconstruction par soustraction donne une origine monotone vers **16:09:10,968 CEST**, sous réserve de la précision de la synchronisation et des horloges. Le décalage observé est d’environ **+1 h 00 min 55 s**.

Ainsi, les entrées initiales à 15:08 du boot actuel ne signifient pas que l’arrêt précédent, l’essai GRUB, l’arrêt physique et la récupération se sont déroulés en quelques secondes. L’authentification SSH initiale du boot actuel à t=25,225491 s correspond approximativement à **16:09:36 CEST**, même si son timestamp avant correction affiche 15:08:41. Preuve : `horloge.json`, avec boot ID, timestamps réels et monotones. Les durées aberrantes de `last -x` et ses mentions « crash » ne sont pas des diagnostics de crash noyau ; elles ne doivent pas servir à dater précisément l’essai.

Paramètres courants, issus de /proc/cmdline :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```

## 2. Inventaire des traces

Dossier : `/home/adminjarvis/JARVIS/rapports/mission04W-preuves/`.

| Preuve | Contenu et limite |
|---|---|
| boots.txt | Liste système complète via sudo, **18 boots** conservés ; liste utilisateur initiale incomplète (17) |
| journal-precedent.txt, kernel-precedent.txt | Boot ID 41984… explicitement sélectionné ; 04U, pas l’incident |
| journal-actuel.txt, kernel-actuel.txt | Boot ID d8f67… explicitement sélectionné ; récupération |
| dmesg.txt | Buffer du boot courant, première ligne Linux version à **0.000000** ; aucune récupération du buffer du boot interrompu |
| horloge.json | Messages choisis avec _BOOT_ID et temps monotones/réels |
| last.txt | Historique wtmpdb, débute le 11 octobre à 22:51 ; heures affectées par l’horloge |
| logs.txt | Inventaire des fichiers /var/log, dont journaux persistants système et utilisateur |
| boot.log, sddm.log, Xorg.0.log, Xorg.0.log.old | Copies en lecture seule des journaux texte existants ; pas de boot ID propre à 04V ni preuve indépendante de son exécution Linux identifiée |
| pstore.txt | **/sys/fs/pstore vide et /var/lib/systemd/pstore vide**, lecture privilégiée réussie |
| grub.cfg.txt, fragment.txt | Configuration active et générateur de l’entrée ; concordance du corps |
| collecte.json, fichiers .stderr | Commandes exactes et codes retour des collectes |
| grub-*.c, manuel-extraits.txt | Sources amont GRUB 2.12 et extraits du manuel installé pour étude statique |
| candidat-editeur-RAM.txt, verification-syntaxe.txt | Proposition non exécutée, contrôle syntaxique uniquement |

Contrôle complémentaire des logs texte : `boot.log` contient 18 sections, dont les deux dernières à 14:23:25 et 15:08:22 (horloge non corrigée), cohérentes avec les 18 boots journald ; aucune section supplémentaire entre elles. `sddm.log` est vide. `Xorg.0.log` annonce 15:08:28 avec la cmdline complète de référence et Intel ; `Xorg.0.log.old` annonce 14:11:30, donc concerne un démarrage encore antérieur. Aucune de ces cmdlines ne valide la saisie 04V.

Les journaux système sont persistants dans `/var/log/journal/2201d5aba3834f0e997d0064b0ba7fa2/`. Le boot de récupération atteste leur flush sur disque à t≈5,48 s. **Cela ne prouve pas une écriture sur disque pour l’essai interrompu.** Aucun fichier pstore exploitable ; ne pas supposer ramoops configuré ou capable de capturer tous les blocages. Aucun journal syslog/kern.log autonome n’apparaît dans l’inventaire courant (l’installer/syslog concerne l’installation).

Les refus initiaux sans sudo (grub.cfg, pstore, journal système) ont été levés par `sudo -n` pour ces lectures. Aucun blocage administrateur restant pour les collectes réalisées ; aucune demande de mot de passe, installation ou modification de groupes.

### Liste complète système au relevé

```text
IDX BOOT ID                          FIRST ENTRY                  LAST ENTRY
-17 b79e816092ef4f14880cbd87c5b5fa36 Sun 2026-10-11 15:24:13 CEST Sun 2026-10-11 17:51:45 CEST
-16 2d7e0cbb167e42c0a628afaefd9ae832 Sun 2026-10-11 17:52:30 CEST Sun 2026-10-11 18:07:45 CEST
-15 d2c66e2757ad4a4f8fbfd727b3fd4640 Sun 2026-10-11 18:08:36 CEST Sun 2026-10-11 18:09:14 CEST
-14 47896394d801461483a770ad6f5faecc Sun 2026-10-11 18:11:00 CEST Sun 2026-10-11 18:47:00 CEST
-13 1496f370c89a4c39ad862be607eb7ec5 Sun 2026-10-11 18:48:13 CEST Sun 2026-10-11 19:55:09 CEST
-12 cf644abbf9ae4308ba1fd97be3e7aa39 Sun 2026-10-11 19:55:50 CEST Sun 2026-10-11 21:03:53 CEST
-11 565560bb80ac424b8bc3101e7441b335 Sun 2026-10-11 21:05:03 CEST Sun 2026-10-11 21:39:02 CEST
-10 a5d477729fed4f518d99ffe75be725b1 Sun 2026-10-11 21:39:59 CEST Sun 2026-10-11 22:24:36 CEST
 -9 b88dab5bc58b49fb85a19fd50b9e9716 Sun 2026-10-11 22:25:21 CEST Sun 2026-10-11 22:50:13 CEST
 -8 b70d6ac9b00b4a16b60fba2dcd09b376 Sun 2026-10-11 22:51:02 CEST Sun 2026-10-11 23:11:31 CEST
 -7 89e71147112d4713a92d2d3f97d8ae38 Sun 2026-10-11 23:11:31 CEST Mon 2026-10-12 13:30:09 CEST
 -6 eb95a45319ee450da29473d73665195a Mon 2026-10-12 13:30:09 CEST Mon 2026-10-12 13:34:01 CEST
 -5 964e3637112741e695e62b20c08f8a65 Mon 2026-10-12 13:34:01 CEST Mon 2026-10-12 13:37:29 CEST
 -4 0f40aa84fb0d4fb59e35af2c799097fa Mon 2026-10-12 13:37:29 CEST Mon 2026-10-12 13:53:34 CEST
 -3 4b050a84587b4d1db739c0eff9fb3626 Mon 2026-10-12 13:53:34 CEST Mon 2026-10-12 14:11:23 CEST
 -2 722c5f56099948d49272cfd54e518ef4 Mon 2026-10-12 14:11:23 CEST Mon 2026-10-12 14:23:24 CEST
 -1 41984ede628649dcbb6c2fbd189b6869 Mon 2026-10-12 14:23:24 CEST Mon 2026-10-12 15:08:21 CEST
  0 d8f67bdef785436599ed1af19afe9620 Mon 2026-10-12 15:08:21 CEST Mon 2026-10-12 16:21:17 CEST

```

## 3. Chronologie attribuable à l’incident

| Étape | Temps | Preuve / portée |
|---|---|---|
| Préparation 04V sur 41984… | Jusqu’à 15:03–15:08, heure du journal précédent | Lectures grub.cfg à 15:03:38 ; SSH accepté à 15:07:59 |
| Arrêt du boot de préparation | 15:08:19–15:08:21 CEST, journal précédent | Commande historique systemctl poweroff à 15:08:19 ; cibles poweroff, sync et arrêt journald à 15:08:21. **Commande passée, non exécutée en 04W** |
| G0 puis linux/initrd puis G1 | Heure externe non fournie | Données utilisateur : G0=3F ×2, codes linux/initrd=0, G1=3F ×2 |
| boot manuel, clignotements, ping/SSH indisponibles | Non horodaté | Récit utilisateur ; aucune trace noyau attribuable |
| Arrêt physique, déconnexion Core éteint | Non horodaté | Récit utilisateur |
| Récupération d8f67… | Origine reconstruite ≈16:09:11 CEST | Journal actuel + synchronisation NTP ; boot Linux complet |

L’essai est situé **dans l’intervalle entre le boot de préparation et celui de récupération**, sans heure précise de G0/G1/boot ni durée du blocage. La borne 15:08 du boot précédent est son heure enregistrée, à ne pas élever en mesure externe exacte sans contrôle de son horloge. Aucun boot conservé intermédiaire ne fournit un ID pour l’essai. La photographie de l’incident n’est pas présente comme fichier local identifié : les mesures et la limite de cadrage sont prises comme données acquises du demandeur, sans prétendre à une inspection visuelle supplémentaire.

## 4. Linux a-t-il démarré ? Dernière étape attestée

Pour **04V interrompu**, aucun des jalons suivants n’est attesté dans les preuves disponibles : Linux version, dmesg t=0, exécution initramfs, EFI/ACPI noyau, énumération PCIe, Intel 00:02.0, i915, contrôleurs Thunderbolt, Quadro, montage racine, systemd, Ethernet, SSH.

Le chargement GRUB de l’initrd **ne signifie pas son exécution**. G1 demeure avant le lancement du chargeur : les hooks vidéo et le transfert EFI peuvent encore intervenir après cette mesure. Aucun DEVEN sous Linux n’a été relevé pour cet essai ; **ne pas lui affecter 0x0F** à partir de 04U.

| Classe | Conclusion pour 04V |
|---|---|
| A — avant entrée noyau | Possible, non prouvé |
| B — initialisation noyau | Possible, non prouvé |
| C — initramfs | Possible, non prouvé |
| D — systemd | Possible, non prouvé |
| E — Linux actif sans réseau | Possible ; ping/SSH seuls ne l’excluent pas |
| F — traces insuffisantes | **Conclusion retenue** |

L’absence de boot dans journald ne prouve pas que le noyau n’a jamais commencé. Un noyau bloqué avant journald/flush, un initramfs incapable de monter la racine, ou des journaux volatils perdus au poweroff peuvent laisser ce même résultat.

## 5. Commande GRUB : référence et risques

L’entrée active **JARVIS — T2 eGPU NP 32M + PREF 512M**, ID `jarvis-t2-egpu-np32-pref512`, concorde avec `/etc/grub.d/47_jarvis_t2_egpu_np32_pref512` pour son corps. Le /boot séparé est recherché par UUID `[UUID EXPURGÉ]`. Chemins GRUB relatifs à ce volume :

```text
linux /vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M 'pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0'
initrd /initrd.img-6.18.54-1-t2-trixie
```

Ces lignes sont la **référence installée**, pas une reconstruction de la saisie 04V. La cmdline réelle de l’essai interrompu n’est pas récupérable. Les cmdlines de 41984… et d8f67… contiennent la référence complète, mais concernent deux autres exécutions.

| Élément | Conséquence possible d’une erreur ou omission |
|---|---|
| vmlinuz/initrd exacts | Mauvais fichier inexistant : erreur de chargement attendue ; fichier existant différent : succès possible sans être la référence ; initrd incompatible : modules/racine possiblement indisponibles |
| root=/dev/mapper/JARVIS--MacMIini--vg-root | Une faute peut empêcher de trouver/monter la racine et laisser une attente/shell initramfs sans réseau |
| intel_iommu=on, iommu=pt | Change l’activation IOMMU ou le domaine par défaut ; omission ne prouve pas une panne mais invalide la comparaison contrôlée |
| pm_async=off | Change la politique asynchrone PM ; effet au boot non établi ici |
| module_blacklist=nouveau | Omission/typo peut permettre la sonde nouveau et changer vidéo/allocation si présent dans l’initramfs ; ne pas affirmer qu’il a été chargé |
| pci=realloc=on | Modifie la politique de réallocation, importante pour la topologie eGPU |
| pci=hpmmioprefsize=512M, pci=hpmmiosize=32M | Mauvaise valeur/unité/orthographe : réserves différentes ou paramètre ignoré ; pas de causalité démontrée avec cet incident |
| pci=resource_alignment avec les trois BDF | Une BDF tronquée/modifiée cible une autre fonction ou supprime un ciblage ; conserver exactement 0000:00:01.2, 0000:7b:00.0, 0000:7c:01.0 |

**Points-virgules :** dans GRUB, non protégés, ils séparent des commandes. Sans apostrophes ASCII (ou protection équivalente), `linux` peut charger avec un seul BDF, puis GRUB tenter d’exécuter `0000:7b:00.0` et `0000:7c:01.0` comme commandes. Le chargement réussi ne valide pas la cmdline. Selon les commandes qui suivent, `echo $?` peut aussi porter sur la dernière commande du groupe plutôt que sur linux. Une faute dans une option noyau ne doit pas nécessairement empêcher GRUB de charger l’image. Les répétitions `pci=` présentes dans la référence ne sont pas, à elles seules, une faute.

La fin de la ligne n’est pas entièrement visible sur la photo décrite : aucune validation visuelle des derniers paramètres ou de leur quoting n’est possible ici. Différences possibles avec une entrée normale : préparation load_video/modules/search, root GRUB, ligne saisie, délais et état RAM ; le `boot` explicite réutilise l’état chargé, tandis que le lancement depuis le menu exécute de nouveau le corps et son boot implicite.

## 6. Comparaison et anomalies EFI/graphiques

| Jalons | 41984… (04U) | d8f67… (récupération) | 04V interrompu |
|---|---|---|---|
| Linux version / cmdline | Oui, référence complète | Oui, référence complète | Non récupérés |
| EFI Apple, ACPI, DMAR/IOMMU | Oui | Oui | Non attestés |
| Racine / systemd | Oui | Oui | Non attestés |
| Intel 00:02.0 / i915 | Aucune détection Intel ; pas de liaison i915 | Intel 8086:3e9b, i915 initialisé, fbcon i915drmfb | Inconnus |
| Thunderbolt / Razer / Quadro | Contrôleurs, Core, Quadro 81:00.0 et BAR | Contrôleurs ; pas de Core/Quadro détectés | Inconnus |
| Ethernet / SSH | Oui, sessions jusqu’avant arrêt | Lien 1 Gbit/s, NetworkManager, authentification à t=25,225 s | Indisponibles selon utilisateur |

Les premières lignes noyau importées dans journald sont à ~2,300 s (04U) et ~5,349 s (récupération) ; **ce ne sont pas les temps d’exécution originaux t=0**. Le dmesg courant commence bien à 0.000000. Les captures 04U depuis t=0 étaient déjà conservées dans `/home/adminjarvis/mission04U-dmesg.txt` et analysées dans mission04U.md ; leurs bornes ne sont pas transférées à 04V.

Récupération : efifb à 0xa0000000 en 1920×1080, puis i915 et fbcon ; message i915 « failed to retrieve link info, disabling eDP » malgré fonctionnement graphique. 04U : efifb à la même base, mais sans i915 ; avertissements Thunderbolt DROM CRC « continuing », erreurs d’expansion/allocation de fenêtres optionnelles, puis poursuite de Linux et SSH. Ces anomalies appartiennent aux boots identifiés et ne démontrent pas la cause 04V.

Aucune trace d’EFI stub/ExitBootServices pour l’essai interrompu. Le fait que la récupération atteigne Linux atteste son propre transfert, pas celui de 04V. Aucune preuve de reset graphique ou GPU hang propre à 04V. Les archives 04O/P documentent Intel/i915 fonctionnels et coexistence avec Core après hotplug ; 04R/S/T/U documentent le masquage dans d’autres conditions. Ce contexte ne transforme pas le clignotement actuel en mesure de DEVEN. Une persistance intermittente du framebuffer GRUB ou un changement de mode reste compatible avec l’observation.

## 7. Hypothèses classées par preuve

1. **Établi :** une divergence s’est produite après G1 et la tentative humaine de boot ; son stade exact est inconnu. G1=3F ×2 ; aucun résultat Linux pour cet essai.
2. **À vérifier en priorité : erreur de saisie ou divergence avec l’entrée normale.** Longue cmdline partiellement photographiée et quoting sensible ; hypothèse concrète, mais aucun paramètre fautif identifié.
3. **Ouvertes, sans trace positive propre à 04V :** échec finalisation vidéo/EFI stub/ExitBootServices/transfert ; blocage précoce noyau PCIe/ACPI/Thunderbolt/IOMMU ; attente initramfs/racine ; Linux partiellement ou complètement démarré sans réseau.
4. **Non démontrées :** cause DEVEN ou firmware Apple, crash Linux, reboot en boucle, panne GPU. Aucun auteur ni transition DEVEN après G1 n’est observé. L’incident peut être indépendant du masquage habituel.

La priorité documentaire n’est pas une probabilité chiffrée. Aucun classement causal plus fin n’est justifié par les journaux absents.

## 8. Méthode plus sûre étudiée — sans exécution

**Écarter la retranscription de linux/initrd et la pause ajoutée simplement après initrd dans une entrée lancée par Ctrl+x.** Une fin de script avec un chargeur enregistré provoque un boot implicite ; interrompre sleep ne constitue pas un veto. Ouvrir seulement une console depuis l’éditeur ne copie pas/exécute pas automatiquement ses lignes.

### Proposition : définir une fonction en RAM, puis l’appeler depuis la console

Cette proposition conserve les lignes longues de l’entrée dans le buffer de l’éditeur. Elle sépare **définition**, **chargement** et **boot humain**. Elle est étudiée statiquement pour GRUB 2.12 installé (`2.12-9+deb13u2`), **pas validée par une exécution pré-Linux locale**.

**Précondition essentielle : menu GRUB fraîchement atteint, aucun chargeur linux/chainloader chargé auparavant.** Une simple définition de fonction n’enregistre pas de chargeur. Toutefois le boot implicite de l’éditeur pourrait lancer un chargeur hérité d’une tentative précédente ! Ne pas utiliser ce protocole après un chargement/échec antérieur ; un retour au menu ne garantit pas l’effacement du chargeur. Sans cette précondition, la proposition n’est pas sûre et doit être abandonnée avant Ctrl+x.

Après autorisation distincte, opérateur local et capture externe :

1. Depuis ce premier menu, interrompre le décompte par une flèche, sélectionner l’entrée validée, `e`. Ne pas modifier les lignes linux/initrd ni leurs quotes. Photographier le buffer et vérifier leur intégrité.
2. Ajouter **avant tout le corps existant** `function jarvis04w_load {` puis `set jarvis04w_ready=0`. Ajouter après chaque commande du corps une garde `if [ "$?" != "0" ]; then return 1; fi` (ne pas scinder la ligne linux). Après la garde d’initrd ajouter `set jarvis04w_ready=1`, puis `}` ; hors fonction ajouter seulement `echo JARVIS04W_FUNCTION_DEFINED_NO_LOAD`. Le candidat complet est dans `candidat-editeur-RAM.txt`. **Ne pas ajouter d’appel de fonction ni boot dans l’éditeur.** Toute modification reste en RAM.
3. Avant exécution, Échap abandonne les éditions et retourne au menu. Une erreur de syntaxe doit faire abandonner, sans la contourner.
4. Ctrl+x exécute uniquement la définition et echo. Avec aucun chargeur préalable, le test interne de boot implicite est faux : aucun noyau n’est chargé/lancé. La fonction reste enregistrée en RAM. Après retour de l’interface au menu, ouvrir `c`. Si le comportement diverge ou une erreur apparaît, arrêter ; ne pas appeler boot.
5. En console, relever plateforme/version et lire VID/DID puis G0 deux fois avec les commandes GRUB déjà documentées en 04V. **Lectures seulement**, argument registre sans `=` : `setpci -s 00:00.0 0.L` puis `setpci -s 00:00.0 -d 8086:3ec4 54.L`. Vérifier identité `3ec48086`, sortie non vide et stable.
6. Saisir seulement `jarvis04w_load`. La fonction exécute la préparation, la ligne linux exacte puis initrd exact. Les gardes arrêtent la fonction sur statut non nul ; aucune commande boot dans la fonction. Immédiatement relever `echo $?`, puis `echo $jarvis04w_ready`. Exiger 0, ready=1 et aucune erreur affichée. Sinon **aucun boot**, même si linux a laissé un chargeur partiel enregistré.
7. Relever G1 deux fois, photographier et attendre à l’invite. La console n’ajoute pas de boot implicite. Retour au menu par Échap en cas d’erreur/annulation ; ne pas réutiliser un boot isolé après erreur, ni relancer Ctrl+x sur le corps initial. Le retour est un retour d’interface, pas une remise à zéro de RAM.
8. Seulement après validation humaine et autorisation couvrant ce lancement, saisir séparément `boot` à l’invite. Aucun boot par délai ou fin de fonction. Après ce transfert, aucun retour GRUB garanti.

Le contrôle `/usr/bin/grub-script-check candidat-editeur-RAM.txt` retourne **0** pour le candidat final ; il parse le texte sans charger de noyau. Un premier candidat limité à une définition de fonction a retourné 1 avec « contains no commands and will do nothing » ; l’echo extérieur rend le contrôle final explicite. **La syntaxe valide ne prouve ni le comportement du binaire EFI effectif, ni l’absence de chargeur hérité, ni l’exactitude des edits futurs.** Les gardes vérifient des codes retour, pas la sémantique des paramètres noyau.

Les sources [éditeur GRUB 2.12](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/normal/menu_entry.c) confirment l’exécution du buffer et le boot implicite conditionné par un chargeur chargé. Les [fonctions](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/script/function.c) sont enregistrées dans une liste globale, et leur [exécution](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/script/execute.c) prend en charge return et les statuts. Copies sources conservées ; le manuel local a aussi été consulté. Les adaptations Debian et le chemin EFI réellement actif limitent la portée de cette validation amont. Une vérification du binaire/paquet exact et une revue du buffer sont recommandées avant d’autoriser l’essai, sans promettre une sécurité absolue.

Comparaison : console 04V = pause fiable mais retranscription risquée ; éditeur avec sleep = réutilisation fiable mais boot implicite dangereux ; fonction RAM appelée en console = réutilisation et contrôle humain, **sous précondition stricte d’absence de chargeur préalable**. Aucun save_env, update-grub, écriture fichier GRUB, EFI ou NVRAM. Cette étude ne constitue aucune autorisation d’éditer réellement le boot suivant.

## 9. Limites et recommandation

Aucune cmdline réelle, aucun boot ID, aucun dernier printk, aucune mesure DEVEN après boot pour l’essai interrompu. Aucun événement ExitBootServices ou panic attribuable. Les photos complètes/horodatages externes ne sont pas disponibles localement ; aucune affirmation sur la partie invisible. Des événements perdus avant persistance ne sont pas récupérables par journalctl. Les logs texte ne compensent pas cette absence d’attribution.

**Arrêter les essais de démarrage à ce stade et conserver l’état stable.** Le travail documentaire peut poursuivre la revue de la méthode RAM et du paquet GRUB exact. Ne pas reproduire la longue saisie manuelle. Un futur essai ne serait raisonnable qu’après autorisation explicite, revue de la procédure, opérateur local, captures externes horodatées et possibilité de récupération convenue. En cas d’incident nouveau ou d’impossibilité de garantir la précondition du protocole, abandonner avant boot.

**Aucune expérience supplémentaire exécutée ; attente de l’autorisation explicite de l’utilisateur.**

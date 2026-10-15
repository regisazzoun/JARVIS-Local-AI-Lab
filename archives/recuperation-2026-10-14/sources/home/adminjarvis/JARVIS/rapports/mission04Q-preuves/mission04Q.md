# JARVIS — Mission 04Q : écran conservant le fond GRUB

Rapport établi le 12 octobre 2026, relevés vers 12:54–12:55 CEST, sur l’hôte JARVIS-MacMIini. Diagnostic en lecture seule ; seules les preuves et ce rapport sont écrits. Aucun redémarrage, redémarrage de gestionnaire graphique, changement de pilote, modification GRUB, rescan, écriture PCIe, branchement ou débranchement. SSH et Razer Core conservés dans leur état actuel.

## Conclusion prioritaire

**Debian a démarré, mais la chaîne graphique locale n’a pas démarré. Le GPU Intel 0000:00:02.0, présent en 04O et 04P, est absent de l’énumération PCI du boot actuel dès les premiers journaux. i915 n’est pas chargé ; aucun GPU DRM ni connecteur, notamment DP-3, n’est publié.**

SDDM est actif comme processus, mais aucun serveur Xorg, greeter ou compositeur n’est lancé. Logind indique `CanGraphical=no` sur seat0. L’état systemd « actif » ne constitue donc pas une preuve de fonctionnement du greeter ou du bureau. Le blocage se situe en amont de la session GNOME, au niveau de la disponibilité du matériel graphique pour Linux.

Le scénario prioritaire est une différence d’exposition de l’iGPU au démarrage avec le Core déjà connecté, éventuellement liée au firmware. C’est une hypothèse causale : l’absence PCI est prouvée ; une désactivation par le firmware et son mécanisme exact ne le sont pas. Il n’y a pas de preuve d’un crash de GNOME/Mutter/KWin ni d’une bascule graphique Linux vers la NVIDIA.

## 1. Identité et périmètre de comparaison

Boot actuel : `89e71147-112d-4713-a92d-2d3f97d8ae38`, journal démarrant le 11 octobre à 23:11:31 CEST. Boot 04O/04P : `b70d6ac9-b00b-4a16-b60f-ba2dcd09b376`, démarré à 22:51:02 CEST. Noyau identique : `6.18.54-1-t2-trixie`. Cmdline strictement identique aux fichiers de preuves 04O et 04P :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```

Observation humaine fournie : écran physique sur le fond GRUB, Debian/SSH/Codex accessibles, Core présent avant le boot. L’image physique n’a pas été observée directement par le collecteur. Les journaux voient le GPU NVIDIA vers 23:11:33, soit environ quatre secondes après le début du noyau en temps monotone ; cela confirme sa détection très tôt, sans constituer une capture de la phase firmware.

## 2. Environnements installés, sélection et session réelle

Les deux environnements sont installés : GNOME 48 (gnome, gnome-core, gnome-session, gnome-shell 48.7, Mutter 48.7), ainsi que KDE Plasma 6.3 (kde-plasma-desktop, plasma-desktop, plasma-workspace, kwin-wayland et kwin-x11). La présence de KDE et d’applications KDE ne prouve pas une session Plasma.

Sessions proposées :

| Protocole | Fichiers disponibles |
|---|---|
| X11 | gnome-xorg.desktop, gnome.desktop, plasmax11.desktop |
| Wayland | gnome-wayland.desktop, gnome.desktop, plasma.desktop |

`/var/lib/sddm/state.conf` mémorise `User=adminjarvis` et `Session=/usr/share/wayland-sessions/gnome-wayland.desktop`. Il s’agit de la dernière sélection, pas d’une session en cours ni d’une configuration d’autologin. Aucun fichier de surcharge SDDM n’a été trouvé aux emplacements de configuration usuels ; les valeurs par défaut indiquent un autologin vide et `DisplayServer=x11`.

**Session actuelle : aucune session graphique locale.** Les sessions loginctl n’ont pas de seat ni de TTY local ; seat0 n’a aucune session active. Aucun processus gnome-session, gnome-shell, Xorg, Xwayland, kwin ou plasmashell en fonctionnement n’a été relevé.

**Session réelle en 04O et 04P : GNOME Wayland**, démontrée par les processus archivés et le journal du boot précédent : `Running GNOME Shell (using mutter 48.7) as a Wayland display server`. Ce même journal montre l’ajout de card0/i915 en modesetting atomic et sa sélection comme GPU primaire. Aucun fondement pour attribuer ces captures à Plasma.

## 3. Gestionnaire de connexion, target et greeter

`/etc/X11/default-display-manager` contient `/usr/bin/sddm` ; le lien `display-manager.service` pointe sur `sddm.service`. GDM3 48 est installé, mais n’est pas le gestionnaire actif. Le processus actif est `/usr/bin/sddm`, PID 932.

- Target par défaut : graphical.target.
- graphical.target : active depuis le 11 octobre à 23:11:45 CEST.
- display-manager/SDDM : active (running) depuis 23:11:38 CEST.
- Journal SDDM actuel : seulement « Initializing », « Starting », « Logind interface found » après le démarrage du service.
- Aucun « Adding new display », « Display server starting », « Greeter starting » ni succès de greeter dans ce boot.
- seat0 : `CanGraphical=no`, `ActiveSession=` et `Sessions=` vides.

Le greeter est configuré pour **X11** par défaut, indépendamment de la session utilisateur GNOME Wayland mémorisée. **Aucune tentative effective de lancement X11 ou Wayland du greeter n’apparaît dans le boot actuel.** SDDM semble attendre un seat graphique utilisable ; le lien causal avec `CanGraphical=no` est très fortement étayé, sans trace détaillée interne SDDM.

Au boot 04O/04P, SDDM lançait explicitement `/usr/bin/X ... -seat seat0 vt2`, annonçait le succès du greeter X11, puis lançait la session GNOME Wayland après authentification. Les deux protocoles remplissaient des fonctions différentes.

## 4. Composants graphiques et erreurs de session

GNOME Shell/Mutter et KWin sont installés mais ne tournent pas dans le boot actuel. Aucune trace de lancement ou d’échec de ces compositeurs ne figure dans les journaux collectés. Il ne faut pas interpréter leur absence d’erreurs comme un démarrage réussi : ils ne sont pas lancés.

Xorg est installé mais aucun processus Xorg n’est présent. `/var/log/Xorg.0.log` est **historique** : création le 11 octobre à 22:51:09, dernière modification à 23:09:59, avant le boot actuel. Il décrit DP-3 connecté et un mode initial 1920×1080 sur le pilote modesetting/iris du boot précédent ; il n’atteste pas d’un serveur X actuel.

**Classification : chaîne graphique arrêtée avant le greeter, et non bureau actif invisible.** Il ne s’agit pas non plus d’une session utilisateur qui aurait été lancée puis aurait échoué : aucune session locale n’a été créée dans ce boot.

## 5. Intel, i915, DRM et sorties physiques

L’Intel UHD Coffee Lake `8086:3e9b`, BDF `0000:00:02.0`, est absent de lspci et de `/sys/bus/pci/devices`. Aucun événement d’énumération de ce BDF ni initialisation i915 dans le journal noyau actuel. Le module i915 n’est pas chargé et son répertoire de pilote PCI est absent. Les modules DRM génériques présents ne constituent pas un pilote de GPU actif.

`/sys/class/drm` ne contient que `version`. `/dev/dri` est absent ; aucun card0, renderD128 ni connecteur DP/HDMI. Debugfs DRI ne présente aucun état de GPU/CRTC consultable.

**DP-3 est absent, et non simplement « disconnected » ou « disabled ».** Son état physique, son EDID et son éventuel scanout matériel ne sont pas accessibles via DRM dans ce boot. Aucun mode KMS Linux ne peut être attesté. Les sorties Intel physiques n’ont donc aucun contrôle DRM publié ; leur fonctionnement électrique reste indéterminé. Le port physique sur lequel l’utilisateur observe le fond GRUB doit être consigné pour lever cette limite, sans déplacer le câble.

En 04O/04P : Intel lié à i915, boot_vga=1, DP-3 connected/enabled. Journal précédent : création i915drmfb, framebuffer primaire fbcon, initialisation DRM réussie et liaison audio Intel/i915.

## 6. Framebuffer EFI et persistance du fond GRUB

Le boot actuel conserve `fb0 = EFI VGA`, associé à `/devices/platform/efi-framebuffer.0`. Journal efifb : adresse `0xa0000000`, taille 8100 Kio, géométrie 1920×1080×32, stride 7680. `/proc/iomem` réserve `a0000000–a07e8fff` à efifb. Le mode sysfs `U:1920x1080p-77` est une description fbdev ; il ne prouve ni modeset KMS ni fréquence physique mesurée.

Le boot précédent annonçait le même framebuffer EFI, puis i915 prenait le relais. Ce relais est absent aujourd’hui. fbcon est présent et le vtconsole framebuffer est lié (`bind=1`) ; il serait donc excessif d’affirmer que Linux n’a absolument jamais écrit dans le framebuffer.

**L’image héritée firmware/GRUB sans remplacement visible par un greeter est l’explication la mieux compatible avec les faits.** La conservation des pixels, la lecture effective de cette zone par le matériel et l’absence totale de rafraîchissement ne sont pas démontrées. Un écran affichant une image identique peut continuer à rafraîchir cette image normalement. Aucune écriture dans `/dev/fb0`, bascule de VT ou tentative de dessin n’a été effectuée.

## 7. NVIDIA, arbitrage VGA et ordre d’initialisation

Quadro RTX 5000 `10de:1eb0` présente à `0000:81:00.0`, sans pilote graphique lié, boot_vga=0. Nouveau et NVIDIA ne sont pas chargés ; aucun paquet de pilote NVIDIA propriétaire installé dans le relevé. Le module Xorg nouveau installé et libdrm-nouveau ne signifient pas qu’un pilote noyau Nouveau fonctionne.

Le journal vgaarb actuel ajoute la NVIDIA avec `decodes=io+mem,owns=none,locks=none` et « bridge control possible ». Il ne comporte pas de sélection Intel comme boot VGA, contrairement au précédent. En 04P, l’arrivée à chaud du Core provoquait un changement des décodages legacy Intel, mais Intel restait présent et lié à i915.

**Aucune bascule d’affichage Linux vers NVIDIA :** aucun driver NVIDIA/nouveau, aucun objet DRM NVIDIA, aucun serveur graphique. Une décision d’affichage prise par le firmware ne peut pas être exclue à partir de ces seuls indicateurs ; boot_vga=0 sur la NVIDIA et l’absence Intel empêchent de reconstituer le GPU firmware primaire avec certitude.

La disparition Intel existe dans l’énumération initiale, avant l’attribution tardive des BAR du Core. Elle est plus compatible avec une différence d’exposition matérielle/firmware qu’avec un échec de session ou une simple mauvaise sélection de connecteur. Les journaux ne montrent pas de BAR Intel refusé ni de suppression ultérieure d’un Intel initialement détecté.

## 8. Comparaison exacte 04O / 04P / 04Q

Comparaison automatisée des fichiers PCI-sysfs initiaux 04O et 04P avec la capture actuelle ; résultat intégral dans `mission04Q-preuves/comparaison.json`.

| Contrôle | 04O | 04P | 04Q actuel |
|---|---|---|---|
| Boot | b70d6ac9… | identique à 04O | 89e71147… |
| Core | absent | ajouté à chaud à 23:02:22 | présent avant boot selon utilisateur, détecté tôt |
| Intel 00:02.0 | présent, i915 | présent, i915 | absent dès l’énumération |
| GPU primaire Linux | Intel boot_vga=1 | Intel boot_vga=1 | aucun GPU DRM |
| NVIDIA | absente | présente sans pilote graphique | présente sans pilote graphique, boot_vga=0 |
| DP-3 | connected/enabled | connected/enabled | connecteur inexistant dans DRM |
| SDDM | actif, greeter lancé | actif, session GNOME en cours | actif, aucun display/greeter lancé |
| Session | GNOME Wayland | GNOME Wayland | aucune session graphique |
| Framebuffer | relais EFI → i915drmfb | i915 conservé | EFI VGA uniquement |
| Cmdline / noyau | référence | identiques | identiques |

Par rapport à 04P : **seul BDF manquant = 0000:00:02.0 ; aucun BDF nouveau ; aucune différence de ressources ni de pilote des BDF communs**. Par rapport à 04O : Intel manque et les huit BDF du Core sont ajoutés ; ressources et pilotes des autres BDF communs identiques. L’absence de différences concerne ces champs, pas une comparaison exhaustive de registres PCI ou de réservations firmware.

BAR GPU inchangés depuis 04P : BAR0 `90000000–90ffffff`, BAR1 `4000000000–400fffffff`, BAR3 `4010000000–4011ffffff`. Fenêtres parents/cible et Core identiques. La disparition Intel signifie que ses BAR historiques `80000000–80ffffff`, `a0000000–afffffff` et I/O `3000–303f` n’ont plus de propriétaire PCI Intel publié ; seule la sous-plage efifb reste réservée. Aucun transfert de ces BAR vers NVIDIA n’est observé.

## 9. Signatures d’erreur recherchées

Recherche dans le journal noyau complet : drm, i915, modeset, atomic, framebuffer, simpledrm, fbcon et vgaarb. Aucun échec atomic/modeset ou GPU hang i915 identifié ; surtout, aucun lancement i915 ni pipeline KMS. Les mentions « atomic » de pools DMA et ext4 concernent d’autres sous-systèmes. Pas d’initialisation simpledrm ni de relais i915drmfb actuel.

Message graphique notable actuel : `snd_hda_codec_intelhdmi ... No i915 binding for Intel HDMI/DP codec`, cohérent avec l’absence de liaison i915. Ce message audio est un témoin secondaire, pas la cause établie.

Les refus de fenêtres Core 49 Mio NP / 802 Mio PREF et d’extensions optionnelles sont suivis de l’allocation obligatoire réussie, comme en 04P. Tous les BAR et ressources comparés restent identiques. Ces refus ne démontrent pas une privation de ressources d’Intel, qui n’a jamais été énuméré dans ce boot. Les avertissements LPSS, ACPI, Broadcom/BT et pcspkr ne fournissent pas d’explication graphique directe. Aucun test de charge GPU ni nouvel audit électrique PCIe n’a été effectué.

## 10. Diagnostic hiérarchisé

1. **Établi : iGPU Intel non exposé à Linux dans ce boot.** Explique i915 absent, DRM absent, DP-3 absent et impossibilité d’établir le GPU primaire Intel.
2. **Établi : SDDM actif sans greeter, sans session graphique.** `CanGraphical=no` et arrêt du journal SDDM avant création du display étayent l’attente d’un seat graphique. graphical.target est atteint malgré cette absence.
3. **Très probable : image héritée conservée faute de relais graphique Linux.** efifb seul, observation humaine du fond GRUB ; contenu et refresh matériel non mesurés.
4. **Hypothèse causale prioritaire : exposition/initialisation firmware différente avec Core connecté avant boot.** Corrélation nette avec 04O/04P et absence Intel dès le départ ; pas de preuve de la règle firmware exacte ni de reproductibilité sur plusieurs boots contrôlés.
5. **Moins étayé : compétition de ressources ou arbitrage VGA Linux faisant disparaître Intel.** Aucun Intel détecté puis retiré, aucune allocation Intel échouée ; ressources des périphériques communs conservées. Une décision antérieure au noyau demeure possible.
6. **Non étayé dans le boot actuel : crash GNOME/Mutter/KWin/Xorg, problème Wayland spécifique ou rendu sur NVIDIA.** Aucun de ces composants graphiques n’est lancé.

## 11. Tests non destructifs proposés, sans correction

Les premiers contrôles en lecture seule ont été exécutés et archivés. Leur répétition permet de vérifier si la situation reste identique, sans modifier les ressources :

```bash
cat /proc/sys/kernel/random/boot_id
ls -la /sys/class/drm /sys/bus/pci/devices/0000:00:02.0
lspci -nnk -s 00:02.0
lsmod | rg 'i915|nouveau|nvidia'
loginctl show-seat seat0 -p CanGraphical -p ActiveSession -p Sessions
systemctl show display-manager.service -p ActiveState -p SubState -p MainPID
sudo journalctl -b -u sddm --no-pager
sudo journalctl -b -k --no-pager | rg -i '00:02\.0|i915|drm|vgaarb|efifb|framebuffer|modeset|atomic|simpledrm|fbcon'
```

Résultat discriminant attendu : Intel toujours absent et CanGraphical=no renforcent le diagnostic matériel en amont. Si Intel/DRM réapparaissaient spontanément, relever immédiatement les nouveaux journaux et le boot ID avant toute autre action. Ne pas demander de rescan ou de chargement de module.

Tests complémentaires proposés, non exécutés :

- Consigner le port exact de l’écran (sortie Mac mini ou Core), l’entrée sélectionnée dans l’OSD et le signal/résolution rapporté par l’écran, sans changer d’entrée ni déplacer de câble. Distingue chemin physique et contrôle Linux.
- Lire deux fois les pixels de `/dev/fb0` en mode strictement lecture seule, comparer les empreintes et éventuellement exporter une image pour comparaison avec le fond GRUB. Des pixels identiques confortent une image stable, mais ne prouvent pas l’absence de rafraîchissement ; des pixels différents avec écran inchangé suggèrent un problème de scanout/chemin physique. Aucune écriture fbdev.
- Examiner hors ligne les tables ACPI du boot actuel et celles archivées en 04O/04P, en particulier IGPU/GFX0 et `_STA`, sans exécuter de méthode ACPI ni écrire de registre. Peut mettre en évidence une différence d’exposition, sans garantir que les tables décrivent l’état matériel effectif.
- Lire la politique des règles udev/logind et les propriétés du framebuffer EFI pour expliquer plus précisément pourquoi seat0 n’est pas graphique. La propriété udev du framebuffer a déjà été archivée ; aucun rechargement de règles ni déclenchement udev.

Une comparaison contrôlée de démarrages avec/sans Core permettrait ultérieurement de tester la causalité firmware. **Elle est hors périmètre : aucun redémarrage ni débranchement n’est proposé pour exécution maintenant.** Ne pas tester `modprobe`, `startx`, `Xorg`, `sddm --test-mode`, un modeset, `chvt`, un redémarrage de service ou une modification GRUB/PCIe dans cette mission.

## 12. Preuves, limites et conservation

Preuves sous `mission04Q-preuves/` : journaux système/noyau complets actuels, journaux SDDM actuel/précédent, journal GNOME Shell précédent, PCI sysfs et comparaison JSON, paquets, processus, sessions/seat, modules, paramètres, état framebuffer, propriétés udev, Xorg historique, réseau et connexions. `collecte.json` consigne commandes, codes retour et date. Les erreurs d’accès ou l’absence de fichiers sont conservées ; elles ne sont pas remplacées par des suppositions.

La session SSH de travail reste opérationnelle, le service SSH est actif et le Core reste connecté. Ce rapport ne constitue ni une validation du pilote NVIDIA ni une demande de correction. Aucun rapport mission04Q.md préexistant n’a été trouvé au début de cette collecte ; ce fichier rassemble le diagnostic 04Q et le complément demandé, sans inventer de résultats antérieurs 04Q.

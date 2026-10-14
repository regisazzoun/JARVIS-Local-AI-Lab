# Mission 04E — Plan d’essai et récupération

## État et périmètre

Nouvelle entrée installée après accord explicite : JARVIS — T2 eGPU réallocation PCIe, ID jarvis-t2-egpu-reallocation. Noyau/initramfs 6.18.54-1-t2-trixie. Arguments : quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on. Seule variation diagnostique : pci=realloc=on. Ancienne entrée inchangée, Debian 6.12.111 par défaut, menu normal 15 s, deux secours et recovery conservés. Pas de modification i915, VFIO, initramfs ou paramètres globaux.

Génération autorisée puis installation autorisée séparément par l’utilisateur. Le redémarrage n’est pas autorisé. Le Core reste connecté à cet instant. Le futur protocole nécessitant Core absent au démarrage et un nouveau branchement exige une autorisation explicite de ces manipulations ; aucune n’est exécutée ici. Si le Core reste présent au démarrage, le résultat sera un essai de détection au boot et devra être distingué du hotplug : ne pas mélanger les deux scénarios.

## Préparation et installation effectuées

Sauvegarde des configurations GRUB, grubenv et scripts dans sauvegarde/ ; empreintes des configurations, images et initramfs dans empreintes-avant.json. Métadonnées originales conservées avec les preuves. Un candidat assemblé a été contrôlé. Puis grub-mkconfig réel exécuté avec les copies de grub.d superposées dans un namespace de montages : système en lecture seule, écritures dans ce dossier uniquement. La copie du thème remplace cp par cmp pour réutiliser le cache déjà identique au fond d’écran ; les verrous LVM sont isolés. Les copies système ne sont pas modifiées. La sortie finale est strictement identique au candidat ; les premiers essais d’isolation non retenus sont conservés et ne sont pas installés.

Diff exact : grub-diff-genere.patch et grub-diff-exact.patch ; seul ajout du bloc 44. Après accord, installation de la source /etc/grub.d/44_jarvis_t2_egpu_reallocation en root:root 0755 et du candidat généré dans /boot/grub/grub.cfg en root:root 0600, mode d’origine. Syntaxe active valide, contenu actif identique au candidat, autres empreintes inchangées. Aucun update-grub/grub-install/EFI ni sélection next_entry. Preuve : validation-installation.txt.

## Futur essai, uniquement après accord distinct

1. Convenir explicitement du redémarrage et de l’état physique du Core. Pour comparer le hotplug au test précédent : obtenir l’accord de déconnexion/reconnexion, Core absent avant démarrage, écran directement sur Intel. Ne rien manipuler maintenant.
2. Sélectionner manuellement la nouvelle entrée. Vérifier noyau exact, boot ID nouveau, présence des cinq paramètres, absence de Nouveau, Intel lié à i915 et bureau réactif. Vérifier Ethernet 192.168.1.99 et ouvrir deux connexions SSH indépendantes depuis le Mac. La veille est actuellement désactivée ; confirmer cet état.
3. Avant tout branchement autorisé, exécuter la collecte ci-dessous vers un nouveau dossier avant-branchement. Comparer toutes les fenêtres des ponts hôtes disponibles avec fenetres-ponts.md. Les ponts externes n’existeront qu’après branchement. Ne pas supposer que pci=realloc=on a eu un effet sans changement observé.
4. Démarrer les deux flux distants ci-dessous et vérifier qu’ils produisent des données sans erreur. Faire une copie complète des journaux avant l’essai. Brancher uniquement après accord matériel distinct et validation de l’accès/collecte.
5. Après branchement, retrouver le GPU par vendor=0x10de et device=0x1eb0, car l’adresse 81:00.0 peut changer. Relever sa chaîne sysfs, toutes les fenêtres et ressources des ponts, BAR 0/1/3 et le lien. Exiger BAR 1 attribué sur 256 Mio, BAR 3 sur 32 Mio, fenêtres couvrant ces plages et BAR 0 valide. Contrôler l’absence de can't assign/no space, erreurs AER/DPC/DMAR, reset NVMe, nouveau gel graphique ou perte SSH. Nouveau doit rester absent et i915 primaire. L’absence d’erreurs seule ne suffit pas : les plages doivent être attribuées.
6. Archiver après-branchement dans un dossier distinct. Aucun pilote à charger pour ce test. Succès éventuel limité à l’allocation PCIe et la stabilité observée ; fonctionnement accéléré de la Quadro non démontré.

Collecte locale via SSH depuis le Mac (écrit uniquement l’archive demandée sur JARVIS, lectures système) :

```sh
ssh adminjarvis@192.168.1.99 'sudo -n python3 /home/adminjarvis/JARVIS/rapports/mission04E-preparation/collecte-lecture-seule.py /home/adminjarvis/JARVIS/rapports/mission04E-preparation/essai-avant-NOUVEAU_IDENTIFIANT'
```

Remplacer NOUVEAU_IDENTIFIANT par un horodatage inédit, puis utiliser un autre dossier essai-apres-NOUVEAU_IDENTIFIANT après branchement. Le script refuse un dossier déjà existant et conserve les codes de sortie de chaque commande.

Sur le Mac, utiliser un dossier inédit pour éviter tout écrasement :

```sh
mkdir -p ~/JARVIS-mission04E-NOUVEAU_IDENTIFIANT
ssh adminjarvis@192.168.1.99 'sudo -n journalctl -b -o short-iso-precise --no-pager' > ~/JARVIS-mission04E-NOUVEAU_IDENTIFIANT/avant.log 2>&1
# Terminal A :
ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=3 adminjarvis@192.168.1.99 'sudo -n journalctl -b -f -o short-iso-precise --no-pager' > ~/JARVIS-mission04E-NOUVEAU_IDENTIFIANT/systeme-suivi.log 2>&1
# Terminal B :
ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=3 adminjarvis@192.168.1.99 'journalctl --user -b -f -o short-iso-precise --no-pager' > ~/JARVIS-mission04E-NOUVEAU_IDENTIFIANT/gnome-suivi.log 2>&1
# Terminal C : garder une connexion indépendante.
ssh adminjarvis@192.168.1.99
```

Vérifier avec tail les fichiers sur le Mac et l’absence de refus sudo/journalctl ; ne pas considérer un fichier créé comme preuve de flux valide.

## Arrêt d’essai et récupération

Si erreurs d’allocation persistantes : constater l’échec de l’hypothèse, capturer immédiatement et ne pas ajouter d’autres paramètres. Si GNOME se fige mais SSH répond : collecte complète immédiate via le terminal indépendant et relevé `ps -eo pid,comm,stat,wchan:32` ; ne pas redémarrer le compositeur, charger/décharger de module ni écrire les BAR. Stopper toute nouvelle manipulation. Redémarrage propre uniquement après accord explicite de récupération. Si SSH est perdu, conserver les derniers journaux Mac, constater délais/état écran et convenir d’une récupération ; aucun arrêt forcé préautorisé.

Après récupération autorisée : sélectionner Debian 6.12.111 (défaut) ou 6.12.107 dans les options avancées, Core absent seulement si sa déconnexion a été autorisée. Les images de secours sont conservées. L’entrée diagnostic précédente reste sélectionnable pour comparaison.

## Retour arrière GRUB proposé, non exécuté

Avant retrait, sauvegarder et contrôler l’état actuel pour ne pas écraser des changements ultérieurs. Si les seules modifications depuis les empreintes avant sont celles de cette mission : après accord de retrait, enlever uniquement /etc/grub.d/44_jarvis_t2_egpu_reallocation, puis restaurer sauvegarde/boot/grub/grub.cfg en root:root 0600. Vérifier grub-script-check et empreinte d’origine 10434b2acdcf83cbab77e1d20fa5eb4981cc724c150b434c62bc841126a39080, défaut/menu/anciennes entrées et grubenv inchangé. Aucun autre script, noyau, initramfs, EFI ou paramètre à supprimer. Si d’autres changements existent, arrêter et préparer un retrait ciblé régénéré au lieu de restaurer aveuglément.

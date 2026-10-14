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
    search --no-floppy --fs-uuid --set=root 8027cbc0-b9fc-4988-99a0-54dc00f7f5c7
    linux /vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau
    initrd /initrd.img-6.18.54-1-t2-trixie
}
```

Les `insmod` ci-dessus sont des commandes du chargeur GRUB pour lire/comprimer le noyau, pas des commandes de charge de pilotes Linux. Aucun argument ne bloque i915 ni ne lie Intel à VFIO.

Deux modifications système prévues après accord : création de ce fichier, puis remplacement contrôlé de `/boot/grub/grub.cfg` par sa version régénérée contenant la nouvelle entrée. Aucun autre fichier système à modifier. Les paramètres globaux, le choix par défaut, grubenv, EFI, noyaux, initramfs, modprobe.d et services restent identiques.

Défaut déjà effectif, conservé tel quel :

```text
gnulinux-advanced-e9a6022b-4986-4652-9929-0693fe71d174>gnulinux-6.12.111+deb13-amd64-advanced-e9a6022b-4986-4652-9929-0693fe71d174
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

L’hôte Linux écoute actuellement sur 192.168.1.99:22, Ethernet intégré enp4s0 UP. **Une connexion depuis le Mac reste à effectuer par l’utilisateur et à confirmer.** Un login historique ne valide pas l’accès sur le prochain boot. Adresse DHCP à recontrôler si elle change ; ne pas changer SSH ou réseau dans ce lot.

Avant chaque essai, ouvrir deux connexions indépendantes, exécuter la vérification en lecture seule et vérifier le login publickey côté Linux. Les commandes ci-dessous s’exécutent sur le Mac ; la création de fichiers est locale au Mac. Elles ne sont pas lancées ici.

```sh
mkdir -p ~/JARVIS-mission04C
ssh adminjarvis@192.168.1.99 'uname -r; cat /proc/cmdline; ip -brief address; cat /proc/sys/kernel/random/boot_id'
ssh adminjarvis@192.168.1.99 'sh /home/adminjarvis/JARVIS/rapports/mission04C-preparation/verification-apres-demarrage.sh'

# Export complet avant l’essai, car le suivi ne remplace pas l’historique.
ssh adminjarvis@192.168.1.99 'sudo -n journalctl -b -o short-iso-precise --no-pager' > ~/JARVIS-mission04C/avant-systeme.log 2>&1
ssh adminjarvis@192.168.1.99 'lspci -nnk; lspci -t; boltctl list; boltctl domains' > ~/JARVIS-mission04C/avant-materiel.log 2>&1

# Terminal distinct A : conserver le flux système en temps réel.
ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=3 adminjarvis@192.168.1.99 'sudo -n journalctl -b -f -o short-iso-precise --no-pager' > ~/JARVIS-mission04C/suivi-systeme.log 2>&1

# Terminal distinct B : flux de la session utilisateur, incluant GNOME.
ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=3 adminjarvis@192.168.1.99 'journalctl --user -b -f -o short-iso-precise --no-pager' > ~/JARVIS-mission04C/suivi-session.log 2>&1

# Terminal distinct C : deuxième accès indépendant pour les contrôles.
ssh adminjarvis@192.168.1.99
```

Avant branchement, regarder depuis une autre fenêtre Mac `tail` des fichiers et vérifier l’absence d’erreur SSH/sudo/journalctl. Les redirections masquent la sortie à l’écran : un fichier créé n’est pas une preuve de collecte valide. Arrêter si le flux ne fonctionne pas ; ne pas élargir automatiquement les droits. Les timestamps journal suivent l’heure configurée sur Linux ; conserver le boot ID.

Les fichiers portent des noms fixes : les archiver dans un nouveau dossier avant un autre essai pour ne pas écraser les preuves. Arrêter les clients de suivi avec Ctrl-C après collecte ; cela ne touche pas les services Linux. Capturer aussi après l’essai `sudo journalctl -b`, `sudo lspci -nnvv`, `/proc/iomem`, ressources sysfs du GPU/ponts et `lsmod`, sans écritures PCI.

## Récupération si le graphique se fige

1. Ne pas charger/décharger de pilote ni redémarrer GNOME Wayland. Garder les flux Mac et utiliser la connexion indépendante.
2. Si SSH répond, capturer immédiatement :

```sh
ssh adminjarvis@192.168.1.99 'date -Is; cat /proc/sys/kernel/random/boot_id; ps -eo pid,comm,stat,wchan:32; /usr/sbin/lsmod' > ~/JARVIS-mission04C/gel-processus.log 2>&1
ssh adminjarvis@192.168.1.99 'sudo -n journalctl -b -o short-iso-precise --no-pager' > ~/JARVIS-mission04C/gel-systeme.log 2>&1
ssh adminjarvis@192.168.1.99 'sudo -n lspci -nnvv; sudo -n cat /proc/iomem' > ~/JARVIS-mission04C/gel-ressources.log 2>&1
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

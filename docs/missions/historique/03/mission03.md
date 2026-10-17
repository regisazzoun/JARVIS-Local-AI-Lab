> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission03.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 03

Date : 11 octobre 2026. Statut actualisé : premier démarrage T2 réussi ; contrôles hôte réalisés après modification des droits (voir dernière section). Anomalies SSH LAN, Wi-Fi/Bluetooth, ACPI/Thunderbolt et profil de capture audio identifiées. Les statuts ci-dessous constituent l’historique. Firmwares Wi-Fi C2 installés ; scan Wi-Fi et Bluetooth validés, association/appairage en attente. Phase D non appliquée. Tailscale non installé, accès Tailscale non testé.

## Autorisations et méthode

Diagnostics en lecture seule autorisés par la mission ; exécutés hors sandbox via le mécanisme d’approbation Codex. `sudo -n id` retourne `uid=0(root) gid=0(root) groups=0(root)`. Création de ce rapport et de ses répertoires autorisée explicitement. Chaque lot administratif reste soumis à un accord ; GRUB et redémarrage demandent une validation distincte. Aucun contournement de protection.

## Commandes réellement exécutées

`sudo -n id`, `cat /etc/os-release`, `uname -a`, `uptime`, `df -h / /boot /boot/efi`, `lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS`, `dpkg --audit`, `apt-mark showhold`, `apt-mark showmanual`, inventaire `dpkg-query` des noyaux/en-têtes/GRUB/DKMS/NVMe/SSH/Bolt/réseau/sudo, `ls -l /boot`, lecture des sources APT et `apt-cache policy`, `sudo -n apt-get -s upgrade --no-remove`, `systemctl --failed --no-pager`, état des services réseau/Bolt, `ip -brief address`, `ip route`, `lspci -nnk`, `lsusb`, `sudo -n journalctl -b -p err --no-pager -n 60`, `sudo -n grub-script-check /boot/grub/grub.cfg`, `sudo -n dpkg --verify` (contrôle long, résultat à compléter), recherche des outils et domaines Thunderbolt.

Compléments : simulation `sudo -n apt-get -s install --no-remove openssh-server dkms linux-headers-amd64 linux-headers-6.12.111+deb13-amd64 nvme-cli`, lecture `/etc/default/grub`, `sudo -n nft list ruleset`, `boltctl domains`, `getent ahostsv4 deb.debian.org`, `nmcli general status`, recherche et lecture des rapports Mission 02 et 02B. Recherche initiale de JARVIS : répertoire absent, créé ensuite à la demande de l’utilisateur.

## Résultats

- Debian 13.7 trixie, noyau actif 6.12.111+deb13-amd64 ; noyau 6.12.107+deb13-amd64 conservé, images et initramfs présents. Aucun test de démarrage du secours réalisé.
- Espace disponible : racine 402 Gio, /boot 709 Mio, EFI 965 Mio. Aucune partition modifiée.
- `dpkg --audit` et liste des paquets gelés : aucun signalement. Aucun service système en échec. Vérification syntaxique de grub.cfg sans message d’erreur ; ceci ne valide pas toute la chaîne de démarrage EFI.
- Sources Debian trixie, trixie-security et trixie-updates, composants main/non-free-firmware. Index non actualisés : simulation upgrade = 0 mise à jour, 0 suppression ; résultat provisoire.
- Simulation installation : 11 nouveaux paquets, 0 suppression. Paquets demandés et dépendances : openssh-server, openssh-sftp-server, dkms, linux-headers-amd64, linux-headers-6.12.111+deb13-amd64, linux-headers-6.12.111+deb13-common, linux-kbuild-6.12.111+deb13, nvme-cli, pahole, runit-helper, uuid-runtime.
- NetworkManager, networking et Bolt actifs ; systemd-networkd inactif. Ethernet enp4s0 UP, [ADRESSE PRIVÉE EXPURGÉE]/24, route via [ADRESSE PRIVÉE EXPURGÉE]. DNS deb.debian.org résolu ; NetworkManager rapporte une connectivité complète. Accès APT frais non testé.
- Aucun filtrage nftables affiché. Adresse IPv6 globale présente : éviter l’écoute SSH générale lors de l’installation. Routeur, redirections et filtrage amont non contrôlés.
- Deux contrôleurs Thunderbolt JHL7540, pilote thunderbolt et deux domaines Bolt en sécurité user. Aucun GPU NVIDIA détecté.
- T2 Bridge et audio Apple sans pilote actif dans l’inventaire ; NVMe Apple fonctionne. BCM4364 détecté, erreurs brcmfmac et firmware Bluetooth absent ; Wi-Fi non disponible dans NetworkManager. Erreurs ACPI, intel-lpss et applesmc enregistrées ; aucun correctif appliqué. Des erreurs de session GNOME apparaissent aussi, sans service système actuellement en échec. Ne pas conclure à une panne critique sans analyse ciblée.

Contrôle long terminé : `dpkg --verify` n’a produit aucun signalement. Cette vérification repose sur les métadonnées disponibles des paquets ; elle ne prouve pas une intégrité exhaustive ni cryptographique du système. La séquence de diagnostics est terminée.

## Lot Phase A approuvé et appliqué

1. Sauvegarder les configurations pertinentes et l’inventaire/hashes des noyaux dans le dossier de rapports ; marquer manuels les deux paquets de noyaux versionnés pour prévenir leur suppression automatique.
2. `sudo -n apt-get update` ; arrêt si un dépôt ou une signature échoue. Refaire les simulations upgrade/install avec les index frais. Toute suppression, mise à jour noyau/GRUB ou changement substantiel du lot demande une validation complémentaire avant application. Aucun autoremove, full-upgrade, grub-install ou redémarrage.
3. `sudo -n apt-get --no-remove upgrade` uniquement après revue de la simulation et hors changements de GRUB/noyau non validés.
4. Empêcher le démarrage automatique de SSH avant installation par masquage ciblé de ssh.service et ssh.socket. Installer avec `sudo -n apt-get --no-remove install openssh-server dkms linux-headers-amd64 linux-headers-6.12.111+deb13-amd64 nvme-cli`. Dépendances réellement nécessaires seulement.
5. Préparer un fragment SSH : PermitRootLogin no, AllowUsers adminjarvis, PubkeyAuthentication yes et écoute initiale [ADRESSE PRIVÉE EXPURGÉE] seulement. Ne pas désactiver les mots de passe avant une connexion par clé réussie depuis le poste administrateur. Validation `sshd -t` et `sshd -T` avant activation du service local ; aucun port routeur ni règle réseau ajouté. L’accès LAN/Tailscale constitue la Phase B et nécessite une configuration approuvée.
6. Vérifier `apt-get check`, `dpkg --audit`, intégrité des paquets et GRUB, conservation des noyaux, lien build du noyau actif, `dkms status`, `nvme list` et santé NVMe, services réseau et état/écoute SSH. Arrêt sur erreur critique, sans réparation automatique non autorisée.

APT peut recharger des services et installer partiellement des paquets avant une erreur ; ce lot n’est pas transactionnel. Les noyaux et GRUB ne seront pas modifiés sans validation spécifique si les simulations les impliquent.

## Phases suivantes et retour arrière

Mission 02 et 02B retrouvées dans /home/adminjarvis. Leurs limitations de sudo/réseau dans le sandbox sont levées par ces diagnostics hôte ; leurs propositions n’autorisent aucune installation.

Phase B : demander la clé publique du poste administrateur (jamais sa clé privée), préparer une écoute LAN ou Tailscale ciblée, puis faire tester une connexion distante par clé avant de désactiver les mots de passe.

Phase C : documentation officielle T2Linux, compatibilité trixie, provenance/empreinte de clé et signatures des dépôts à vérifier à nouveau avant sélection d’un noyau et de ses en-têtes. Firmware BCM4364 et composants audio à examiner. Aucun dépôt T2 ajouté, aucun noyau choisi ou installé, aucun paramètre GRUB modifié.

Retour arrière prévu : conserver les deux noyaux Debian, leurs initramfs et entrées GRUB ; démarrage manuel d’un noyau Debian depuis les options avancées en cas de problème T2. Procédure non testée ; sauvegardes avant intervention à réaliser après accord.

Phase D : attendre la stabilisation puis le branchement du premier Razer Core Quadro RTX 5000. Ne pas installer NVIDIA, CUDA ou Container Toolkit avant détection et validation du plan correspondant. Aucune configuration simultanée des GPU.

## Exécution Phase A — 11 octobre 2026

Accord utilisateur : « oui applique la phase A ». Toutes les commandes administratives ont été exécutées sur l’hôte hors sandbox via les demandes d’approbation Codex.

Sauvegardes et journaux : `~/JARVIS/rapports/phaseA-20261011-1619/`. Archive configuration-avant.tgz contenant /etc/apt, /etc/default/grub, /boot/grub/grub.cfg et /etc/ssh avant installation ; inventaire dpkg et marques manuelles ; empreintes SHA256 des deux images noyau, deux initramfs et grub.cfg ; journaux APT et simulations ; copie du sshd_config du paquet et configuration effective SSH. L’archive contient les configurations de la machine : la conserver localement. Aucun fichier de clé privée n’a été lu ou affiché.

Commandes de modification réellement exécutées : `apt-mark manual linux-image-6.12.107+deb13-amd64 linux-image-6.12.111+deb13-amd64`, `apt-get -o APT::Update::Error-Mode=any update`, simulations upgrade/install, `apt-get -y --no-remove upgrade`, `systemctl mask ssh.service ssh.socket`, puis `apt-get -y --no-remove install openssh-server dkms linux-headers-amd64 linux-headers-6.12.111+deb13-amd64 nvme-cli`. Actualisation réussie, aucune erreur de signature signalée ; 0 mise à jour, 11 installations, 0 suppression.

Versions installées : OpenSSH Server/SFTP 1:10.0p1-7+deb13u4 ; DKMS 3.2.2-1~deb13u1 ; en-têtes amd64/communs, métapaquet et linux-kbuild 6.12.111-1 ; nvme-cli 2.13-2 ; pahole 1.30-1 ; runit-helper 2.16.4 ; uuid-runtime 2.41.5-0+deb13u1. Aucun utilitaire supplémentaire ajouté.

Le paquet OpenSSH a créé les clés hôte, le compte système sshd et ses dépendances systemd. Masquage préalable : messages de preset impossible attendus, sans échec d’APT ; aucun serveur n’a démarré avant configuration. Message dpkg-preconfigure « unable to re-open stdin » sans échec d’installation ; les paquets se sont configurés normalement. Les paquets uuid-runtime/nvme-cli ont aussi enregistré leurs unités habituelles (uuidd.socket, unités NVMe Fabrics).

Configuration créée : `/etc/ssh/sshd_config.d/00-jarvis.conf`, droits 644, contenant AddressFamily inet, ListenAddress [ADRESSE PRIVÉE EXPURGÉE], PermitRootLogin no, AllowUsers adminjarvis, PubkeyAuthentication yes, PasswordAuthentication yes. Répertoire temporaire /run/sshd créé si absent. Aucun authorized_keys modifié ; aucun mot de passe désactivé. `sshd -t` réussi ; `sshd -T` contrôlé automatiquement pour ces six valeurs et pour l’absence d’autre ListenAddress. Puis `systemctl unmask ssh.service ssh.socket`, `systemctl disable ssh.socket`, `systemctl enable --now ssh.service`.

SSH actif et activé au démarrage, socket systemd désactivé ; `ss -ltnp` confirme uniquement [ADRESSE PRIVÉE EXPURGÉE]:22. `ssh-keyscan -T 5 -t ed25519 [ADRESSE PRIVÉE EXPURGÉE]` confirme un échange protocolaire local ; ce test ne valide pas une connexion authentifiée. Empreinte ED25519 générée par le paquet : SHA256:QYVmHZNn7JLacJbfmEcIlUxkgmZht7gZzcS+2Gdczy4. L’accès distant LAN/Tailscale et la connexion par clé depuis le poste administrateur restent à préparer en Phase B.

Contrôles après installation : `apt-get check` et `dpkg --audit` sans erreur ; `grub-script-check` réussi ; les cinq empreintes des noyaux/initramfs/grub.cfg sont identiques à avant intervention. Les deux noyaux sont marqués manuels. Lien build du noyau actif valide vers /usr/src/linux-headers-6.12.111+deb13-amd64. `dkms status` vide : infrastructure installée, aucun module DKMS enregistré, donc aucune compatibilité NVIDIA/T2 testée.

`nvme list` identifie APPLE SSD AP0512M ; `nvme smart-log /dev/nvme0` : avertissement critique 0, température 34 °C, réserve 100 %, usure déclarée 0 %, erreurs média 0, journal erreurs 0. Compteur historique de 37 arrêts non sûrs observé ; aucune correction automatique et aucune preuve de défaut actuel.

NetworkManager, networking, Bolt et SSH actifs ; aucun service système en échec ; adresse Ethernet et route inchangées. Wi-Fi toujours indisponible (Phase C). Aucun changement de partition, noyau, GRUB, pare-feu ou routeur ; aucun redémarrage, pilote NVIDIA, CUDA ou dépôt T2 ajouté.

Retour arrière : configuration SSH du paquet sauvegardée, fragment JARVIS identifié ; toute restauration et arrêt du service devront faire l’objet d’un lot approuvé. Aucune désinstallation automatique proposée. Les noyaux Debian et leurs entrées existantes sont conservés ; démarrage du secours non testé.

Vérification finale terminée : `dpkg --verify` sans signalement, y compris après installation ; simulation finale upgrade : 0 mise à jour, 0 installation, 0 suppression, 0 paquet différé. Phase A validée, aucune erreur critique rencontrée. Les contrôles d’intégrité ne constituent pas un test exhaustif du système ou de la chaîne EFI.

## Accès SSH LAN — 11 octobre 2026

Autorisation utilisateur : « Modifie les droits pour que mes autres machines du reseau puisse se connecter en ssh ». Lot présenté puis exécuté hors sandbox via approbation Codex. Adresse contrôlée : [ADRESSE PRIVÉE EXPURGÉE]/24 ; aucun filtrage nftables affiché.

Sauvegarde : `~/JARVIS/rapports/ssh-lan-20261011-162408/00-jarvis.conf-avant`. Fragment /etc/ssh/sshd_config.d/00-jarvis.conf mis à jour : écoute IPv4 sur [ADRESSE PRIVÉE EXPURGÉE] et [ADRESSE PRIVÉE EXPURGÉE] ; AllowUsers adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] adminjarvis@[ADRESSE PRIVÉE EXPURGÉE]/24 ; root interdit ; clés et mots de passe autorisés jusqu’au test distant par clé. Aucun droit sudo ou droit de fichier utilisateur modifié.

Premier contrôle automatique arrêté avant rechargement : assertion supposant une seule ligne AllowUsers dans sshd -T. OpenSSH affiche une ligne par règle ; correction du contrôle après lecture des valeurs effectives, sans changement supplémentaire de configuration. `sshd -t` réussi ; contrôle corrigé des deux écoutes et des deux règles AllowUsers réussi ; `systemctl reload ssh.service` exécuté, service actif, `ss -ltnp` confirme les deux écoutes IPv4. `ssh-keyscan` sur [ADRESSE PRIVÉE EXPURGÉE] confirme l’échange SSH depuis l’hôte.

Connexion depuis une autre machine et authentification non encore testées. Adresse attribuée par DHCP : sa stabilité future n’est pas garantie ; aucune réservation ou configuration réseau modifiée. Aucune écoute IPv6, aucun port routeur ouvert, aucun redémarrage. Configuration du routeur non inspectée. Retour arrière : restaurer le fragment sauvegardé puis valider et recharger SSH, après accord.

## Phase B — préparation et attente de clé publique

Autorisation utilisateur : passer à la Phase B et exécuter ses scripts de déploiement après double vérification. Cette autorisation ne supprime pas l’exigence de test depuis le poste administrateur avant désactivation des mots de passe et ne couvre pas les phases T2/eGPU ou un redémarrage.

Première vérification hôte : sudo root confirmé, sshd -t valide, paramètres effectifs root interdit/clé autorisée/mot de passe conservé/StrictModes yes, service actif et écoutes limitées à localhost et [ADRESSE PRIVÉE EXPURGÉE]. Dossier ~/.ssh et authorized_keys absents : aucune clé publique utilisateur déjà installée. Dossier personnel adminjarvis:adminjarvis, mode 700. Tailscale absent du PATH ; aucune installation ou connexion Tailscale effectuée.

Seconde vérification : configuration effective évaluée pour adminjarvis et une adresse cliente LAN d’exemple [ADRESSE PRIVÉE EXPURGÉE] ; état du service relu ; empreinte ED25519 du serveur contrôlée depuis le fichier public. Cette vérification ne constitue pas une connexion distante authentifiée.

Suite prévue après réception de la clé publique : vérifier son format puis son empreinte avec ssh-keygen ; installer sans écraser d’autres clés dans ~/.ssh/authorized_keys, droits .ssh 700 et authorized_keys 600, propriétaire adminjarvis ; relire et contrôler indépendamment empreinte, droits et configuration effective. Demander ensuite un test depuis le poste administrateur avec PasswordAuthentication=no et PreferredAuthentications=publickey, puis contrôler le journal Accepted publickey. Seulement après ce succès, sauvegarder et passer PasswordAuthentication à no, valider syntaxe et configuration effective avant rechargement, puis vérifier service et nouvelle connexion. Maintenir l’accès local KDE/Konsole. Une adaptation Tailscale nécessitera les adresses réelles et la configuration du réseau concerné ; aucune écoute générale anticipée.

Clé publique demandée à l’utilisateur. Aucune clé privée demandée, lue ou transférée. Aucun changement système effectué lors de cette préparation ; Phase B en attente de la clé et du test distant.

## Phase C — diagnostics, signatures et plan précis

L’utilisateur demande de passer à la Phase C. Diagnostics et préparation exécutés ; aucune installation de noyau ou modification GRUB effectuée. La demande initiale impose un plan avant ces opérations et un accord distinct pour redémarrer. L’autorisation de scripts donnée en Phase B ne vaut pas validation spécifique de ce nouveau plan de démarrage.

### Diagnostics hôte

Macmini8,1 confirmé ; sudo root confirmé ; noyau Debian 6.12.111 actif. /boot libre 709 Mio, ESP libre 965 Mio. Commande de démarrage actuelle sans paramètres T2. SecureBoot rapporté désactivé par mokutil ; aucun réglage de sécurité changé. PipeWire et WirePlumber actifs. /proc/asound/cards n’expose que HDA Intel PCH, aucune carte AppleT2. Pile t2bce absente du noyau chargé. NVMe et Thunderbolt restent pris en charge par Debian.

Wi-Fi : demande précise `brcm/brcmfmac4364b2-pcie.apple,lanai-HRPN-u-7.5-X3.bin`, puis variantes moins spécifiques jusqu’à brcmfmac4364b2-pcie.bin, toutes manquantes ; crash de firmware brcmfmac. Bluetooth : brcm/BCM.hcd absent. applesmc : initialisation échouée -5. Ne pas installer broadcom-wl. Aucun besoin de Touch ID, Touch Bar, trackpad ou APFS sur cette machine.

### Documentation et vérifications

Sources consultées : [installation Debian T2Linux](https://wiki.t2linux.org/distributions/debian/installation/), [dépôt du mainteneur](https://github.com/AdityaGarg8/t2-ubuntu-repo), [configuration de base](https://wiki.t2linux.org/guides/postinstall/), [audio](https://wiki.t2linux.org/guides/audio-config/), [Wi-Fi/Bluetooth](https://wiki.t2linux.org/guides/wifi-bluetooth/). Le README annonce Debian 13 trixie et fournit linux-t2-lts. Compatibilité annoncée et dépendances cohérentes, pas encore de test de démarrage local.

Fichiers téléchargés et extraits uniquement dans `~/JARVIS/rapports/phaseC-preparation/`. Aucune source ajoutée à /etc/apt et aucune clé ajoutée au trousseau système. Clé publique obtenue par HTTPS depuis GitHub Pages puis comparée octet par octet au fichier du dépôt GitHub : identiques. Empreinte : `9F9873A566A73E27CFF0294FE2E496114ACDBFD4` (RSA 4096, Aditya Garg). Cette comparaison est une cohérence entre deux publications du même mainteneur, pas une authentification indépendante de son identité.

`gpgv` valide les signatures InRelease commun (19 septembre 2026) et trixie (5 octobre 2026) ; index Packages conformes en taille et SHA256 aux Release signés. Pas de champ Valid-Until dans ces métadonnées ; dates examinées manuellement, pas de garantie automatique contre un rejeu ancien. APT en utilisateur, avec listes/cache et sources dédiés au dossier de préparation et Signed-By explicite, a également accepté les signatures. Simulation : 4 nouveaux paquets, 0 suppression, 0 mise à jour. Les dépôts Debian n’étaient pas ajoutés à cette simulation isolée ; toutes les dépendances demandées sont toutefois satisfaites par l’état dpkg courant et les paquets T2 sélectionnés.

Paquets téléchargés, SHA256 vérifié deux fois contre les index signés, extraits sans exécuter leurs scripts :

| Paquet | Version | Taille téléchargée |
|---|---|---:|
| linux-t2-lts | 6.18.54-1-trixie | 1326 octets |
| linux-image-6.18.54-1-t2-trixie | 6.18.54-1 | 161070956 octets |
| linux-headers-6.18.54-1-t2-trixie | 6.18.54-1 | 10478944 octets |
| apple-t2-audio-config | 0.5.3-trixie | 1512 octets |

Empreintes sauvegardées dans paquets-sha256.json ; simulation dans simulation-install.log. Noyau contient t2bce_dma/core/vhci/audio/ave et applesmc ; firmware Wi-Fi non inclus. En-têtes : build -> /usr/src/linux-headers-6.18.54-1-t2-trixie. Compilateur noyau GCC Debian 14.2.0-19 identique au compilateur installé. Aucun module NVIDIA compilé : compatibilité NVIDIA/DKMS non validée. Le métapaquet LTS contient un Conflicts sur lui-même dans les métadonnées ; APT accepte cette sélection, les autres variantes T2 sont absentes.

Scripts noyau preinst/postinst/prerm/postrm lus et syntaxe sh validée. Ils appellent les hooks /etc/kernel et /usr/share/kernel. Hooks locaux lus : DKMS, génération initramfs et zz-update-grub. L’installation modifiera donc /boot/grub/grub.cfg et créera un initramfs même sans exécution manuelle préalable d’update-grub. Config audio : profils ALSA UCM AppleT2x2/x4/x6 ; fonctionnement réel à valider après démarrage du pilote t2bce_audio.

Erreurs de préparation sans modification système : sudo ne trouve pas rg dans son PATH, corrigé par lecture sudo puis filtrage rg utilisateur ; deux anciennes URL wiki remplacées par les liens actuels ; téléchargement Python sans délai interrompu puis repris avec curl et délais explicites ; parseur de métadonnées arrêté sur une stanza vide après téléchargement des quatre paquets, contrôles repris séparément. Aucun incident interprété comme une panne Debian, aucun script distant exécuté.

### Lot C1 proposé : noyau/en-têtes/audio et GRUB

1. Revalider état APT, hashes et espace, sauvegarder /etc/default/grub, /etc/default/grub.d et grub.cfg, inventaire des paquets et noyaux. Conserver les noyaux Debian 6.12.111 et 6.12.107 marqués manuels.
2. Installer les quatre .deb déjà vérifiés avec `sudo -n apt-get --no-remove install` et leurs chemins locaux, après une nouvelle simulation. Aucune activation de dépôt tiers pour ce premier essai ; les futures mises à jour T2 demanderont un lot de maintenance dédié. Ne pas installer les paquets autonomes apple-bce/applesmc-t2 ni d’autres variantes de noyau.
3. Avant installation, créer un fragment GRUB dédié /etc/default/grub.d/99-jarvis-t2.cfg fixant GRUB_DEFAULT à l’entrée Debian actuelle dans son sous-menu (identifiants gnulinux-advanced-[UUID EXPURGÉ] > gnulinux-6.12.111+deb13-amd64-advanced-[UUID EXPURGÉ]), afficher le menu avec délai 10 secondes. Ne pas ajouter globalement de paramètres T2 à ce stade : ils seront saisis pour le premier essai sur l’entrée T2 uniquement, afin que le démarrage Debian de secours garde sa ligne actuelle. La validation du lot doit explicitement couvrir ce fragment et la régénération du menu par les hooks d’installation, puis `update-grub` si nécessaire ; aucun grub-install, changement EFI ou partition.
4. Vérifier initramfs T2, modules t2bce, en-têtes/build, DKMS, audit paquets et syntaxe/menu GRUB, présence des deux entrées Debian et choix par défaut Debian. Estimation /boot : noyau/config environ 18 Mio plus initramfs (taille exacte après génération), compatible avec 709 Mio libres ; arrêter si la marge devient insuffisante. Ne pas régénérer les initramfs Debian inutilement.
5. Préparer le test : sélectionner manuellement le noyau T2 dans les options avancées GRUB, touche e et ajouter `intel_iommu=on iommu=pt pm_async=off` à sa ligne linux pour ce démarrage uniquement. Ces paramètres sont recommandés par le wiki. Après un essai réussi, proposer leur persistance pour T2 et un éventuel changement du noyau par défaut dans un lot distinct. Aucun redémarrage sans accord séparé et présence locale pour sélectionner l’entrée.

Retour arrière : noyau par défaut Debian 6.12.111, ancien 6.12.107 disponible ; en cas d’échec de l’essai T2, sélectionner Debian au menu (paramètres T2 non globaux). Tous les paquets Debian sont conservés ; suppression/restauration éventuelle uniquement après accord. Test réel du secours non réalisé.

### Lot C2 proposé séparément : firmwares Broadcom

macOS supprimé : méthode 5 T2Linux (image de récupération Apple Monterey/Ventura/Sonoma), téléchargement pour extraction de firmware uniquement, aucune installation macOS. Script firmware.sh téléchargé et syntaxe Bash vérifiée, branche méthode 5 inspectée. Le script upstream télécharge un autre script depuis une branche mouvante, monte une image via loop, écrit les firmwares et recharge des modules ; il ne sera pas exécuté aveuglément.

Avant déploiement C2 : récupérer et figer le helper de téléchargement, l’inspecter et vérifier la provenance de l’image Apple ; télécharger l’image dans l’espace utilisateur, convertir avec dmg2img, monter l’image en lecture seule via un loop (sans toucher aux partitions réelles), extraire/renommer les seuls firmwares BCM4364 adaptés et Bluetooth, sauvegarder /usr/lib/firmware/brcm avant copie. dmg2img manque : simulation Debian = 1 installation, 0 suppression. curl et python3 sont présents. Contrôler les fichiers et hashes avant copie, vérifier absence de chemins dangereux dans les archives ; paramètres exacts et commandes seront présentés avant accord C2. Reload des modules seulement après vérification de la pile du noyau effectivement actif, jamais force-unload t2bce.

Phase C reste préparatoire : noyau, firmwares, audio et démarrage T2 pas encore installés/testés. Réseau Ethernet, SSH et KDE restent utilisables. Aucun pilote NVIDIA ajouté.

## Phase B — finalisation SSH, contrôles avant accord

11 octobre 2026, 17:34 CEST. L’utilisateur confirme une connexion par clé ED25519 depuis son Mac de travail et demande de présenter les modifications avant leur validation. Contrôles effectués hors sandbox avec approbation Codex ; aucune modification de configuration appliquée à cette étape.

- ~/.ssh : propriétaire adminjarvis:adminjarvis, mode 700 ; authorized_keys : adminjarvis:adminjarvis, fichier régulier mode 600. Dossier personnel mode 700. Aucun ajustement de permissions nécessaire. Aucun fichier privé lu.
- ssh-keygen -lf authorized_keys : clé ED25519, commentaire mac-travail-jarvis, empreinte SHA256:5VkwEPPaD1KGQNEM3XZ/JiK0ivMm3AwIrhFDzN3PGuM affichée deux fois (deux entrées de la même clé). Aucun nettoyage des doublons demandé ou effectué.
- Journal ssh.service : Accepted publickey pour adminjarvis depuis [ADRESSE PRIVÉE EXPURGÉE] le 11 octobre à 17:33:00, ED25519 avec cette même empreinte. Connexion par clé confirmée indépendamment du retour utilisateur.
- sshd -t valide. Configuration effective : PasswordAuthentication yes ; KbdInteractiveAuthentication no ; PubkeyAuthentication yes ; PermitRootLogin no ; StrictModes yes. Écoutes [ADRESSE PRIVÉE EXPURGÉE]:22 et [ADRESSE PRIVÉE EXPURGÉE]:22 ; AllowUsers adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] et adminjarvis@[ADRESSE PRIVÉE EXPURGÉE]/24.
- Sauvegarde créée : ~/JARVIS/rapports/phaseB-finalisation-20261011-173446/ssh-configuration-avant.tgz (sshd_config et sshd_config.d), paramètres effectifs dans sshd-effective-avant.txt. Répertoire utilisateur mode 700. Les messages tar de suppression du slash initial sont normaux.

Modification proposée, en attente d’accord : dans /etc/ssh/sshd_config.d/00-jarvis.conf, remplacer PasswordAuthentication yes par PasswordAuthentication no et ajouter explicitement KbdInteractiveAuthentication no. Maintenir les clés, l’interdiction root, les écoutes et AllowUsers exactement comme actuellement. Avant rechargement : sshd -t puis contrôle sshd -T (y compris contexte adminjarvis/client [ADRESSE PRIVÉE EXPURGÉE]). Recharger avec systemctl reload ssh.service, vérifier service et écoute. Aucune modification réseau, GRUB ou noyau ; aucun redémarrage Debian. La phase ne sera déclarée terminée qu’après une nouvelle connexion par clé depuis le Mac de travail et vérification du journal après rechargement.

### Application approuvée de la sécurisation

Accord : « oui modifie ». Application sur l’hôte hors sandbox avec approbation Codex, le 11 octobre 2026 à 17:35:53 CEST. Copie supplémentaire du fragment immédiatement avant modification : phaseB-finalisation-20261011-173446/00-jarvis.conf-immediat-avant ; paramètres effectifs immédiats sauvegardés également.

Seul fichier système modifié : /etc/ssh/sshd_config.d/00-jarvis.conf. PasswordAuthentication passé à no ; KbdInteractiveAuthentication no ajouté explicitement (déjà no dans la configuration effective précédente). Aucun changement de clé, de droits de ~/.ssh, d’AllowUsers, d’adresses d’écoute, de réseau, de GRUB ou de noyau.

Contrôles : sshd -t avant et après modification réussis. sshd -T global et contextualisé pour adminjarvis depuis [ADRESSE PRIVÉE EXPURGÉE] contrôlés par assertions indépendantes. Différence de configuration effective globale limitée à passwordauthentication yes -> no ; pubkeyauthentication yes, permitrootlogin no, kbdinteractiveauthentication no et restrictions d’accès conservés. Résultats sauvegardés dans sshd-effective-apres.txt et sshd-effective-mac-apres.txt.

systemctl reload ssh.service réussi ; service actif. ss -ltnp confirme uniquement [ADRESSE PRIVÉE EXPURGÉE]:22 et [ADRESSE PRIVÉE EXPURGÉE]:22. Journal confirme rechargement et réouverture des deux écoutes à 17:35:53 CEST. Aucun redémarrage Debian effectué ; aucune erreur rencontrée.

Statut Phase B : sécurisation appliquée, validation finale EN ATTENTE d’une nouvelle connexion par clé depuis le Mac de travail après 17:35:53. Test demandé avec ssh -o ControlMaster=no -o ControlPath=none -o PreferredAuthentications=publickey -o PasswordAuthentication=no adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] (nouvelle connexion TCP, sans réutilisation d’une session multiplexée). La phase ne sera déclarée terminée qu’après confirmation utilisateur et contrôle du nouveau Accepted publickey dans le journal.

### Validation finale Phase B

Confirmation utilisateur : « oui c bon ». Contrôle hôte du journal après rechargement : Accepted publickey pour adminjarvis depuis [ADRESSE PRIVÉE EXPURGÉE] à 17:36:58 CEST, port client 49727, clé ED25519 SHA256:5VkwEPPaD1KGQNEM3XZ/JiK0ivMm3AwIrhFDzN3PGuM. Cette nouvelle connexion est postérieure au rechargement de 17:35:53. Service actif, sshd -t valide, paramètres effectifs confirmés une nouvelle fois : mots de passe et authentification interactive désactivés ; clé autorisée ; root interdit ; écoutes et restrictions LAN conservées.

Phase B SSH LAN terminée et validée. Aucun changement système pendant cette dernière vérification. Tailscale reste une future adaptation : non installé et non testé ; l’accès SSH actuel conserve sa restriction au LAN et localhost. Phases C et D inchangées.

## Phase C1 — contrôles renouvelés et plan final avant accord

11 octobre 2026, 17:40 CEST. Demande utilisateur : préparer l’installation T2, sauvegarder et présenter un plan ; autorisation explicite requise avant installation/modification GRUB, puis accord distinct pour redémarrer. Diagnostics hôte et sauvegardes effectués via approbation Codex. Aucune installation ou modification du démarrage exécutée.

### Résultats et traces

- sudo -n id confirme root ; uname -r confirme 6.12.111+deb13-amd64 ; ligne noyau actuelle conservée (ro quiet).
- dpkg --audit sans signalement, apt-get check réussi. Deux images Debian 6.12.111/6.12.107 installées et marquées manuelles, DKMS 3.2.2 installé, dkms status vide.
- df -h : /boot libre 709 Mio, EFI libre 965 Mio. Espace pour le noyau (environ 18 Mio dans /boot) et son futur initramfs ; taille finale à vérifier après génération.
- gpgv valide à nouveau l’InRelease trixie du 5 octobre avec la clé documentée. Taille/SHA256 de Packages contrôlés contre ce Release signé ; taille/SHA256 des quatre .deb contrôlés contre Packages, puis comparés au manifeste préparatoire. Identité/version/architecture des paquets relues avec dpkg-deb -f. Tous les contrôles réussissent.
- Nouvelle simulation **avec les chemins des quatre .deb locaux**, apt-get -s --no-remove sur l’hôte : 4 nouveaux paquets, 0 mise à jour, 0 suppression, aucun paquet différé. Les dépendances exactes du métapaquet sont satisfaites par les deux .deb image/en-têtes ; pas de dépendance supplémentaire requise.
- grub-script-check actuel réussi ; sous-menu et identifiant de l’entrée Debian 6.12.111 relus. grubenv ne contient aucune variable next_entry. EFI : BootCurrent 0000, Debian shimx64.efi ; BootOrder 0000,0080. Anciennes entrées Apple non modifiées.
- SSH et NetworkManager actifs. Aucune erreur de diagnostic.

Sauvegardes : `~/JARVIS/rapports/phaseC1-20261011-1740/`. grub-avant.tgz contient /etc/default/grub, /etc/default/grub.d, /etc/grub.d, grub.cfg et grubenv. efi-avant.txt, grubenv-avant.txt, grub.cfg-avant, cmdline-avant.txt, disques-avant.txt, inventaire dpkg, marques manuelles, hashes des deux images/initramfs Debian et hashes des fichiers EFI sauvegardés. Simulation locale et manifeste revérifié enregistrés. Messages tar sur les slashs initiaux normaux, archive créée avec succès. Informations de démarrage sauvegardées, pas d’image complète du disque.

### Plan final proposé — NON APPLIQUÉ

Paquets : linux-t2-lts 6.18.54-1-trixie ; linux-image-6.18.54-1-t2-trixie 6.18.54-1 ; linux-headers-6.18.54-1-t2-trixie 6.18.54-1 ; apple-t2-audio-config 0.5.3-trixie. Installation locale seulement ; aucun nouveau dépôt APT, aucun firmware ou pilote NVIDIA dans C1.

Avant installation : recontrôler les empreintes et sauvegardes ; installer le fragment proposé sous /etc/default/grub.d/99-jarvis-t2.cfg, propriétaire root:root, mode 644, avec :

```sh
GRUB_DEFAULT='gnulinux-advanced-[UUID EXPURGÉ]>gnulinux-6.12.111+deb13-amd64-advanced-[UUID EXPURGÉ]'
GRUB_TIMEOUT_STYLE=menu
GRUB_TIMEOUT=10
```

Proposition écrite uniquement dans le dossier utilisateur (99-jarvis-t2.cfg.proposition), syntaxe sh contrôlée et identifiants vérifiés contre grub.cfg actuel. Aucun fragment système créé à cette étape.

Commande d’installation proposée : `sudo -n apt-get --no-remove install` suivie des quatre chemins absolus .deb dans phaseC-preparation. Les hooks image noyau génèrent l’initramfs, passent par DKMS et régénèrent GRUB ; cet effet est explicitement inclus dans le lot soumis à accord. Exécuter update-grub après installation pour garantir que le fragment est pris en compte. Ne pas lancer grub-install ni modifier l’ESP, les entrées EFI ou les partitions. Conserver les noyaux et le métapaquet Debian ; aucun autoremove ou retrait de paquet.

Vérifications après installation : dpkg-query des quatre paquets, apt-get check, dpkg --audit, présence/vérification des fichiers noyau/initramfs T2 (lsinitramfs), modinfo sur les modules T2 et lien build/en-têtes, dkms status, fichiers UCM audio ; grub-script-check, entrée T2 et deux entrées Debian, GRUB_DEFAULT ciblant effectivement Debian 6.12.111 et menu visible 10 secondes ; hashes Debian/EFI comparés aux sauvegardes ; SSH/réseau et espace restants. Aucun chargement forcé de modules T2 sous le noyau Debian. Arrêt sur erreur critique ; aucune réparation non validée. Aucun redémarrage.

Les paramètres intel_iommu=on iommu=pt pm_async=off ne seront pas ajoutés globalement dans C1. Pour le premier essai, sélectionner l’entrée T2 dans GRUB et les ajouter temporairement à sa ligne linux. Cela préserve le démarrage Debian de secours. L’audio ne peut être testé avant démarrage T2 ; Wi-Fi/Bluetooth restent en attente du lot firmware C2. Compatibilité future NVIDIA/DKMS non testée.

Retour arrière : laisser le délai expirer pour démarrer Debian 6.12.111 ; en cas d’échec de l’essai T2, sélectionner cette entrée ou 6.12.107 dans les options avancées. Fragment dédié et archive permettent une restauration de configuration après accord ; aucune désinstallation automatique ou réinstallation EFI. Ne pas restaurer grub.cfg ancien seul comme solution durable : régénérer après restauration des réglages, avec validation. Les noyaux de secours sont conservés mais leur démarrage n’a pas été testé dans cette mission.

Statut C1 : diagnostics/simulation/sauvegardes terminés ; attente de l’accord explicite pour les quatre installations et les modifications GRUB décrites, puis vérification avant toute demande de redémarrage distincte.

## Phase C1 — installation approuvée et vérifications

Accord utilisateur : « oui install ». Lot exécuté sur l’hôte via approbation Codex, le 11 octobre 2026 vers 17:44 CEST. Aucune autorisation de redémarrage reçue ou utilisée.

Avant application : empreintes des quatre paquets revérifiées contre le manifeste déjà validé cryptographiquement ; sauvegarde GRUB présente ; hashes des images et initramfs Debian et de tous les fichiers EFI conformes aux sauvegardes. Simulation locale renouvelée : 4 installations, 0 suppression/mise à jour. Espace inchangé.

Modifications exécutées : installation root:root 644 du fragment /etc/default/grub.d/99-jarvis-t2.cfg à partir de la proposition validée, syntaxe sh vérifiée. `sudo -n apt-get -y --no-remove install` avec les quatre chemins absolus .deb préparés ; hooks noyau exécutés par dpkg, initramfs T2 généré et GRUB régénéré. Puis `sudo -n update-grub` et `sudo -n grub-script-check /boot/grub/grub.cfg`. Journaux installation.log et update-grub.log dans phaseC1-20261011-1740.

Les quatre paquets sont configurés (état ii) aux versions prévues. apt-get check et dpkg --audit sans erreur, dpkg --verify des quatre paquets sans signalement. Message dpkg-preconfigure stdin absent non bloquant ; avertissement os-prober non exécuté attendu (pas de dual boot recherché) ; message audio « Restart » informatif seulement, aucun redémarrage lancé.

Contrôles du démarrage : grub.cfg syntaxiquement valide. Analyse automatisée confirme GRUB_DEFAULT pointant le sous-menu Debian puis l’entrée 6.12.111, menu visible et délai 10 s ; entrées normales des trois noyaux et références à leurs initramfs présentes ; grubenv ne contient aucun next_entry. Les quatre fichiers image/initramfs Debian sont byte-identiques aux sauvegardes ; tous les fichiers EFI sont identiques et efibootmgr -v identique au relevé préalable. Aucun EFI réinstallé, aucune partition modifiée.

Initramfs T2 lisible avec lsinitramfs, contenu enregistré dans initramfs-t2-contenu.txt : modules NVMe, LVM (dm-mod) et ext4 présents. Image T2 environ 10 Mio, initramfs environ 87 Mio. Modules t2bce_dma/core/vhci/audio présents sous /lib/modules/6.18.54-1-t2-trixie ; modinfo confirme vermagic correspondant. Ils ne sont pas dans l’initramfs généré automatiquement : pas de chargement T2 précoce forcé, clavier USB externe et racine LVM non chiffrée utilisés sur ce Mac mini ; la pile T2 devra être vérifiée après démarrage. Aucun module chargé sous le noyau Debian actif.

Lien build valide vers /usr/src/linux-headers-6.18.54-1-t2-trixie et Makefile présent. dkms status vide : aucun module externe installé, compatibilité NVIDIA non testée. Profils UCM AppleT2x2/x4/x6 installés ; audio réel non testé tant que T2 n’est pas démarré. Firmwares Broadcom non installés dans ce lot.

Système après installation : uname -r toujours 6.12.111+deb13-amd64 ; SSH et NetworkManager actifs, sshd -t valide, aucun service système en échec. /boot libre 604 Mio ; /boot/efi libre 965 Mio. Aucun problème critique rencontré.

Statut : installation C1 terminée et vérifiée avant démarrage. Premier essai T2 en attente d’accord distinct et de présence locale : sélectionner manuellement 6.18.54-1-t2-trixie dans les options avancées GRUB, éditer sa ligne linux et ajouter temporairement intel_iommu=on iommu=pt pm_async=off. Sans sélection manuelle, le démarrage reste Debian 6.12.111. En cas d’échec, revenir au noyau Debian conservé ; aucun changement permanent de paramètres ou du choix par défaut pendant cet essai. Aucun redémarrage effectué.

## Premier essai de démarrage T2 — autorisation de redémarrage

L’utilisateur confirme sa présence devant JARVIS avec écran et clavier USB et autorise explicitement un redémarrage normal pour tester 6.18.54-1-t2-trixie. Commande prévue : `sudo -n systemctl reboot`, hors sandbox via approbation Codex. Aucun changement GRUB, partition ou ordre de démarrage. L’utilisateur sélectionnera manuellement le noyau et ajoutera temporairement `intel_iommu=on iommu=pt pm_async=off`.

Autorisation consignée avant lancement ; résultat de la commande et démarrage effectif à confirmer au retour utilisateur. Après lancement, attente du retour, sans autre modification ni diagnostic automatique post-redémarrage. Contrôles prévus ensuite : noyau/paramètres actifs, périphériques T2, Ethernet, SSH et journaux. Validation du premier démarrage non encore obtenue.


## Mission 03 — simplification de l’essai T2 (11 octobre 2026)

Demande utilisateur : préparer les changements exacts, obtenir son accord avant modification de GRUB, puis appliquer et contrôler sans redémarrage. Le premier essai manuel n’a pas démarré T2, selon son retour. Lecture actuelle de uname et /proc/cmdline : Debian 6.12.111+deb13-amd64, ro quiet, aucun des trois paramètres T2.

### Analyse et limites de la session actuelle

/etc/default/grub indique GRUB_DEFAULT=0 et délai 5 s, mais /etc/default/grub.d/99-jarvis-t2.cfg les surcharge : choix explicite du sous-menu puis Debian 6.12.111, style menu, délai 10 s. Aucun paramètre T2 global présent. Les six fichiers image/initramfs des trois noyaux sont présents et non vides dans /boot.

Le grub.cfg actif est illisible (Permission denied). sudo -n id échoue : sudo.conf appartient à uid 65534 dans cette vue et no_new_privileges empêche l’élévation. L’accès administratif hors sandbox est désactivé par la politique de cette session. Aucune tentative de contournement. Les contrôles du menu se fondent donc sur phaseC1-20261011-1740/grub.cfg-apres, sauvegarde historique, et ne certifient pas le menu actif actuel.

Cette sauvegarde contient : entrée principale « Debian GNU/Linux » pointant en réalité vers T2 6.18.54 ; sous-menu « Advanced options for Debian GNU/Linux » avec T2 6.18.54, Debian 6.12.111 et Debian 6.12.107, chacun en mode normal et recovery. Le fragment actuel sélectionne Debian 6.12.111 par identifiants, malgré la première entrée T2. Debian 6.12.107 reste un secours manuel, pas un basculement automatique en cas d’échec.

### Changements exacts proposés — NON APPLIQUÉS

Fichiers préparés dans mission03-grub-proposition/ uniquement, sans modification système :

1. Remplacer /etc/default/grub.d/99-jarvis-t2.cfg par la proposition homonyme : commentaire actualisé, GRUB_TIMEOUT passe de 10 à 15 ; GRUB_DEFAULT et GRUB_TIMEOUT_STYLE=menu conservés.
2. Créer /etc/grub.d/42_jarvis_t2 (root:root, 755 après accord), dont le contenu exact figure dans la proposition. Entrée au premier niveau « JARVIS — Apple T2 6.18.54-1-t2-trixie (essai) », identifiant jarvis-t2-6.18.54-test. Recherche de /boot par UUID [UUID EXPURGÉ], cohérent avec fstab et le menu sauvegardé. Ligne noyau :

```
linux /vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off
initrd /initrd.img-6.18.54-1-t2-trixie
```

Les chemins GRUB sont relatifs à la partition /boot sélectionnée ; ils correspondent aux fichiers /boot/vmlinuz-* et /boot/initrd.img-* vérifiés. Les lignes Debian et les paramètres globaux ne changent pas. Aucun paquet/noyau supprimé.

### Contrôles réalisés et suite après accord

Syntaxe sh du fragment de réglages valide. Pour 42_jarvis_t2, seules les deux premières lignes sont du shell ; le reste est du GRUB transmis par tail. Un sh -n sur tout le fichier a donc signalé une accolade inattendue : contrôle inadapté, pas une erreur GRUB. Contrôle correct : en-tête shell valide, exécution du script via sh produit exactement entree-t2.cfg, grub-script-check de cette sortie réussi. grub-script-check sur menu-simulation.cfg réussi également. Cette simulation ajoute l’entrée et porte le délai à 15 s dans la sauvegarde ; ce n’est pas une génération réelle par grub-mkconfig. Lecture approfondie des initramfs et contrôle du menu actif restent à refaire avec accès hôte.

Après accord ET rétablissement de l’accès administratif : relire grub.cfg et grubenv actifs, vérifier absence de next_entry et correspondance des UUID/identifiants, sauvegarder les fichiers actuels, installer les deux propositions avec propriétaires/modes prévus, générer un menu temporaire via grub-mkconfig, vérifier syntaxe, choix Debian, délai 15 s, entrée T2 et paramètres isolés, entrées/initramfs Debian et absence de changements de leurs lignes linux/initrd. Publier le menu par update-grub seulement si ces contrôles réussissent, puis contrôler grub.cfg actif et consigner résultats. Ne pas annoncer ces vérifications comme effectuées avant exécution. Aucun grub-install, changement EFI ou redémarrage prévu.

Statut : préparation terminée ; accord utilisateur requis pour les changements GRUB décrits. Application et génération réelle également bloquées par l’accès administratif de cette session.


### Accord reçu — application bloquée par l’environnement

L’utilisateur a répondu « oui » à la proposition des deux modifications GRUB. Cet accord autorise leur application, la génération et les contrôles, sans redémarrage ; aucune nouvelle confirmation de ce même lot n’est nécessaire.

Nouvelle tentative de diagnostic : sudo -n id échoue toujours, avec /etc/sudo.conf vu comme appartenant à uid 65534 et le drapeau no_new_privileges empêchant l’élévation. La politique de session interdit les exécutions hors sandbox ; aucun contournement tenté. grub.cfg actif reste en mode 600 et inaccessible. Le fragment système reste à GRUB_TIMEOUT=10 et /etc/grub.d/42_jarvis_t2 est absent. Aucun changement système appliqué, aucune génération réelle effectuée, aucun redémarrage lancé.

Suite : reprendre le lot déjà autorisé dans une session disposant de l’accès administratif à l’hôte. Recontrôler la configuration active avant installation et réaliser les vérifications prévues ci-dessus. Les propositions restent disponibles dans mission03-grub-proposition/.


### Simplification GRUB appliquée et contrôlée

Après modification des permissions par l’utilisateur, sudo -n id confirme uid=0. Accord antérieur utilisé, aucun nouvel accord demandé. Menu actif relu : correspond aux entrées identifiées précédemment. UUID de /boot confirmé par grub-probe ; grubenv sans next_entry.

Sauvegardes et journaux : /home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357 . Archive des réglages et scripts GRUB, grub.cfg et grubenv ; copies avant/après et empreintes des six fichiers noyau/initramfs.

Modifications : /etc/default/grub.d/99-jarvis-t2.cfg installé root:root 644, délai normal 15 s ; /etc/grub.d/42_jarvis_t2 installé root:root 755, entrée dédiée JARVIS — Apple T2 6.18.54-1-t2-trixie (essai) avec les trois paramètres autorisés. Choix Debian 6.12.111 conservé. Debian 6.12.107 conservé comme secours manuel.

Génération réelle de test via grub-mkconfig réussie et contrôlée avant update-grub ; update-grub réussi puis contrôle du menu actif réussi. grub-script-check valide les deux menus. Contrôles automatisés : identifiant de défaut exact, menu visible, délai normal 15 s, entrée dédiée unique, chaque paramètre T2 présent une seule fois dans cette entrée, lignes linux/initrd Debian normales et recovery identiques à avant. Les trois initramfs sont lisibles via lsinitramfs, contenus enregistrés. Les six images/initramfs ont des empreintes identiques avant/après ; grubenv inchangé.

La branche préexistante recordfail conserve son délai de 30 s, tandis que le démarrage normal affiche le menu 15 s. Cela ne change pas le choix Debian par défaut. Aucun grub-install, modification EFI, suppression de noyau ou redémarrage exécuté. Validation syntaxique effectuée ; démarrage effectif T2 encore à tester par l’utilisateur.


### Redémarrage autorisé après simplification GRUB

Le 2026-10-11T18:06:14, l’utilisateur demande « ok redemarre ». Autorisation explicite de lancer sudo -n systemctl reboot. Entrée T2 dédiée à sélectionner manuellement pendant le menu de 15 secondes ; Debian 6.12.111 reste le défaut. Autorisation consignée avant lancement ; résultat du redémarrage et noyau effectivement démarré à confirmer après retour.


## Validation du premier démarrage T2 — 11 octobre 2026, 18:16 CEST

### Périmètre et limites

Demande actuelle : diagnostic en lecture seule, sans modification système ni redémarrage. Seul ce rapport a été complété. Aucun chargement manuel de module, installation, changement SSH/GRUB, test sonore, réparation ou redémarrage exécuté. KDE accessible selon la confirmation utilisateur.

La session dispose d’une vue sandbox : sudo -n id échoue (sudo.conf vu comme appartenant à uid 65534 et no_new_privileges actif). La politique interdit l’exécution hors sandbox ; aucun contournement tenté. Netlink, D-Bus et PipeWire sont interdits ; les nœuds matériels /dev/nvme* et /dev/snd ne sont pas exposés. Le journal système et /boot/grub/grub.cfg ne sont pas lisibles. Les résultats « No entries », « no soundcards », route vide et DNS échoué ne prouvent donc pas des pannes de l’hôte. Les montages ro observés par findmnt sont ceux de cette vue sandbox, pas une preuve de remount-ro dû à une erreur disque.

### Résultats actuels

| Composant | Preuve observée | Évaluation |
|---|---|---|
| Noyau | uname : 6.18.54-1-t2-trixie, SMP PREEMPT_DYNAMIC | Confirmé actif |
| Démarrage | /proc/cmdline : BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off | Trois paramètres confirmés |
| T2 Bridge | PCI 02:00.1 106b:1801, pilote t2bce_core ; modules t2bce_core, t2bce_dma, t2bce_vhci chargés | Pilotes liés et bus USB virtuel présent |
| Audio T2 | PCI 02:00.3 106b:1803, pilote t2bce_audio chargé | Carte ALSA enregistrée ; son réel non testé |
| SMC | applesmc chargé, mais noms hwmon visibles : nvme, pch_cannonlake, coretemp uniquement | Chargement confirmé ; exposition des capteurs SMC non confirmée |
| PCIe / Thunderbolt | Deux NHI JHL7540 (07:00.0 et 7d:00.0) liés à thunderbolt ; contrôleurs USB liés à xhci_hcd | Contrôleurs reconnus ; erreurs et périphériques externes non validés |
| Secure Enclave | PCI 02:00.2 106b:1802 sans pilote affiché | Inventorié ; aucune conclusion de panne |
| USB | lsusb échoue libusb -99 ; lsusb -t montre xHCI, hub, HID, stockage UAS 10 Gbit/s, bus T2 avec cdc_ncm et HID | Topologie et pilotes visibles ; inventaire libusb limité |
| SSD | ANS2 02:00.0 lié à nvme ; APPLE SSD AP0512M 465,9 Gio / 500,28 Go, firmware 1306 | Détecté et utilisé ; SMART non accessible |
| LVM | nvme0n1p3 LVM2_member 464 Gio ; sysfs dm-0 = JARVIS--MacMIini--vg-root, dm-1 = JARVIS--MacMIini--vg-swap_1 ; swap actif 24 637 436 Kio, utilisé 0 | Volumes présents ; métadonnées PV/VG/LV non validées par outils administratifs |
| Espace disque | Racine 433 Gio, disponible 401 Gio ; /boot disponible 604 Mio ; EFI disponible 965 Mio | Espace suffisant |
| Ethernet | BCM57766 04:00.0 lié à tg3 ; enp4s0 operstate up, carrier 1, speed 1000 ; rx_errors=0, tx_errors=0 | Lien physique actif à 1 Gbit/s ; IP et accès distant non confirmés |
| NetworkManager / Internet | nmcli, systemctl et ss bloqués ; /proc/net ne montre que loopback de la session ; getent sans réponse et curl erreur DNS | Non vérifiables dans cet espace réseau isolé |
| Wi-Fi | BCM4364 03:00.0 détecté, module brcmfmac disponible/chargé mais aucun pilote lié affiché | Anomalie probable à investiguer ; cause firmware non confirmée aujourd’hui |
| SSH | Fragment 00-jarvis.conf lisible : écoute [ADRESSE PRIVÉE EXPURGÉE] et [ADRESSE PRIVÉE EXPURGÉE], PermitRootLogin no, AllowUsers limité à adminjarvis local/LAN, PubkeyAuthentication yes, PasswordAuthentication no, KbdInteractiveAuthentication no | Configuration par clé conservée ; service, écoute et connexion réelle non validés |
| Clés SSH | authorized_keys mode 600 ; ssh-keygen -lf reconnaît deux lignes ED25519 de même empreinte | Clé présente ; doublon à examiner ultérieurement, non modifié |
| Secours Debian | 6.12.107+deb13-amd64 et 6.12.111+deb13-amd64 : vmlinuz, initrd, config et répertoires /lib/modules présents | Deux noyaux conservés ; démarrage effectif non testé |

### Audio disponible

/proc/asound/cards : carte 0 « Apple T2 Audio », carte 1 « HDA Intel PCH ». /proc/asound/pcm : Speaker (00-00, lecture), Codec Output (00-02, lecture), Codec Input (00-03, capture), HDMI 0/1/2 (01-03, 01-07, 01-08, lecture). L’entrée « Apple Headset » est également visible dans /proc/bus/input/devices sur le bus t2bce_vhci.

aplay -l et arecord -l retournent « no soundcards found » dans la vue /dev restreinte ; wpctl ne peut pas joindre PipeWire. Ces échecs ne contredisent pas l’enregistrement des cartes par le noyau. Profils KDE/PipeWire, volumes, routage, haut-parleur, jack et capture restent à valider sur l’hôte.

### Journaux noyau, ACPI, T2 et Thunderbolt

journalctl -b -k -p warning et journalctl -b -u ssh ne voient aucune entrée avec avertissement de permissions ; dmesg --level=err,warn retourne Operation not permitted. system.journal existe mais n’est pas lisible par cette session. Aucune affirmation d’absence d’erreurs n’est possible. Les erreurs ACPI, intel-lpss, applesmc, Wi-Fi et Bluetooth consignées plus haut proviennent de contrôles antérieurs sous Debian et ne constituent pas des erreurs confirmées de ce démarrage T2.

### Reconnaissance des claviers Apple dans GRUB

Linux reconnaît actuellement un clavier Apple USB 05ac:0250 (« Apple Inc. Apple Keyboard »), deux interfaces HID et gestionnaires kbd, derrière le hub USB 1-8, port 1-8.2, sur le contrôleur Intel 00:14.0. Un Logitech USB Keyboard 046d:c31c est également connecté directement sur 1-14. hid_apple et usbhid sont chargés. Ce clavier Apple observé ne passe pas par le bus USB virtuel T2.

La reconnaissance sous Linux ne valide pas la reconnaissance avant chargement du noyau. Le chemin via hub est une piste de test, pas une cause établie. Le modèle/chemin d’un éventuel autre clavier Apple ou Bluetooth n’a pas été confirmé.

Réglages système lisibles : fragment 99-jarvis-t2.cfg conserve Debian 6.12.111 par défaut, menu visible 15 secondes ; entrée 42_jarvis_t2 conserve les paramètres T2 isolés. grub.cfg actif reste inaccessible. La sauvegarde mission03-grub-20261011-180357/grub.cfg-apres contient terminal_output gfxterm, les entrées Debian normales/recovery et aucun chargement explicite USB/HID/keyboard trouvé par la recherche. Cette absence ne prouve pas que la saisie firmware est indisponible. La sauvegarde est une preuve historique, pas une lecture du menu actif aujourd’hui.

Recommandation : lors d’un futur démarrage explicitement autorisé, comparer le clavier Apple branché directement à un port USB du Mac, puis via le hub, en conservant le Logitech disponible pour sélectionner le secours. Consigner si le clavier répond au sélecteur firmware et dans GRUB. Ne proposer une modification GRUB qu’après cette comparaison et inspection du menu actif ; aucune configuration modifiée maintenant.

### Prochaines actions recommandées

1. Terminer les contrôles en lecture seule depuis une session hôte disposant des permissions nécessaires : journalctl -b -k (ACPI, T2/t2bce, applesmc, Thunderbolt, NVMe et I/O), journalctl -b -u ssh, état NetworkManager/SSH, ip address/route, ss -lnt, nvme smart-log, pvs/vgs/lvs --readonly et lecture du grub.cfg actif. Ne pas affaiblir les protections pour cela.
2. Depuis le poste administrateur, tester une nouvelle connexion SSH à [ADRESSE PRIVÉE EXPURGÉE] avec la clé existante, BatchMode=yes et PreferredAuthentications=publickey ; vérifier le succès publickey dans les journaux hôte. Ne pas désactiver la vérification de clé d’hôte. Aucun test distant par clé effectué pendant cette session.
3. Valider les profils et périphériques audio dans KDE/PipeWire puis, avec accord pour le test, vérifier lecture et capture. Examiner applesmc/capteurs et BCM4364 à partir des journaux avant toute correction ou installation firmware.
4. Comparer les chemins USB du clavier lors d’un redémarrage futur autorisé ; conserver les deux secours Debian. Aucun redémarrage nécessaire pour les contrôles réseau, SSH, SMART et journaux.

Conclusion : démarrage T2, paramètres, liaison des pilotes T2/audio, inventaire SSD/LVM, lien Ethernet et conservation des deux noyaux Debian confirmés. Anomalies/pistes : BCM4364 sans pilote lié affiché, capteurs SMC non confirmés malgré module chargé, problème clavier GRUB rapporté, doublon de clé autorisée. La validation complète reste ouverte pour les journaux, SMART, services/connectivité réseau, SSH réel et fonctionnement sonore ; ces limites sont explicitement documentées et ne sont pas déclarées comme des pannes.


## Reprise avec droits hôte — 11 octobre 2026, 18:19 CEST

Cette section actualise et remplace les limites du premier diagnostic pour les contrôles désormais accessibles. sudo -n id confirme uid=0 ; commandes toujours en lecture seule. Aucun paramètre, service, firmware, profil audio ou menu modifié, aucun redémarrage. Preuves brutes : mission03-validation-hote-20261011-1819/ (journal noyau complet, journal SSH, SMART, menu GRUB actif et profils audio).

### Composants confirmés fonctionnels

- Noyau 6.18.54-1-t2-trixie et paramètres intel_iommu=on iommu=pt pm_async=off reconfirmés. Journaux : t2bce_dma/core/vhci/audio initialisés ; bus T2 enregistré et périphériques iBridge/Headset détectés. Les avertissements staging signalent le statut des pilotes, pas un échec de leur initialisation.
- Apple SMC : 608 clés, 1 ventilateur, 31 sondes annoncés ; fichiers présents sous /sys/bus/acpi/devices/APP0001:00. Lecture fan1_input = 1682 tr/min, temp1_label = TA0V, temp1_input = 20250 (20,25 °C). L’absence de nom applesmc dans /sys/class/hwmon/*/name ne constituait donc pas une absence de capteurs. Avertissement API hwmon obsolète présent.
- NVMe : SMART critical_warning=0, température 34 °C, réserve 100 %, usure déclarée 0 %, media_errors=0, num_err_log_entries=0. Compteur historique unsafe_shutdowns=37 à surveiller ; il ne prouve pas 37 incidents durant cette mission. Racine montée rw sur l’hôte ; aucune occurrence panic, oops, I/O error ou EXT4-fs error trouvée dans le journal de ce démarrage. Message « nvme0: using unchecked data buffer » présent, sans erreur média SMART associée.
- LVM : PV /dev/nvme0n1p3, VG JARVIS-MacMIini-vg <464,01 Gio, 1 PV/2 LV, libre 28 Mio ; root 440,48 Gio et swap_1 <23,50 Gio. dmsetup confirme les deux mappings actifs en écriture. Les attributs XX de lvs --readonly sont une information d’état indisponible dans ce mode, pas une panne déduite. Le faible espace libre du VG diffère des 401 Gio libres dans le système de fichiers racine : une extension de LV aurait peu de réserve, mais la racine dispose de beaucoup d’espace.
- Ethernet/NetworkManager : enp4s0 UP, [ADRESSE PRIVÉE EXPURGÉE]/24, route par [ADRESSE PRIVÉE EXPURGÉE] ; NetworkManager actif, état connected/full. DNS deb.debian.org résolu et HTTPS retourne HTTP/2 200. Interface Ethernet virtuelle T2 enxacde48001122 DOWN/unavailable, distincte de l’interface LAN fonctionnelle.
- USB : lsusb fonctionne désormais, clavier Apple Aluminium ISO 05ac:0250, hub intégré Apple 05ac:1006, Logitech K120, souris Dell, adaptateur NVMe Realtek RTL9210 et périphériques T2 détectés.
- Secours : images/initramfs et modules Debian 6.12.107 et 6.12.111 toujours présents ; menu GRUB actif contient les deux versions en normal/recovery. grub-script-check réussi ; grubenv vide. Défaut Debian 6.12.111, délai normal 15 s (recordfail 30 s), entrée dédiée T2 avec les trois paramètres. Les autres entrées T2 générées n’ont pas ces paramètres : conserver l’entrée dédiée pour les essais. Aucun test de démarrage des secours effectué.
- Aucun service système en échec selon systemctl --failed.

### Anomalies confirmées

**SSH LAN indisponible malgré service actif.** À 18:11:16, sshd enregistre « Bind to port 22 on [ADRESSE PRIVÉE EXPURGÉE] failed: Cannot assign requested address », puis écoute seulement sur [ADRESSE PRIVÉE EXPURGÉE]:22. ss -lnt confirme aujourd’hui cette écoute locale exclusive, alors que l’adresse LAN est maintenant présente. sshd -t réussi ; configuration effective vérifiée pour adminjarvis depuis une adresse LAN : PubkeyAuthentication yes, PasswordAuthentication no, KbdInteractiveAuthentication no, PermitRootLogin no, utilisateurs limités au local/LAN. Les clés autorisées restent présentes. L’ordre observé de ssh.service dépend de network.target ; une course avec l’acquisition de l’adresse est probable, sans cause définitive établie. Aucun succès publickey enregistré dans le journal SSH du démarrage actuel. Pas de clé privée locale et agent SSH sans identité : authentification réelle non testée. Le service n’a pas été relancé.

**Wi-Fi/Bluetooth.** Firmware brcmfmac4364b2-pcie absent (-2), échec Dongle setup, Firmware halted/crashed ; avertissement workqueue __flush_work avec trace dans brcmfmac lors du retrait après échec. NetworkManager indique WIFI-HW missing. Bluetooth : échec réglage baudrate (-16), firmware brcm/BCM.hcd introuvable. Aucune installation ou extraction de firmware faite.

**ACPI/IRQ.** AE_AML_BUFFER_LIMIT dans _SB._OSC ; AE_ALREADY_EXISTS et méthodes CPU GCAP/_OSC/_PDC/APPT interrompues ; IOAPIC GSI 34 introuvable, intel-lpss INT34BA:00 échec -22 (IRQ index 0 absent), routage PCI INT A du contrôleur thermique absent. Le système démarre, mais l’impact des fonctions concernées n’est pas établi par ce diagnostic.

**Thunderbolt/USB.** Deux contrôleurs thunderbolt liés, deux domaines Bolt en sécurité user, aucun périphérique externe listé par boltctl. Avertissement sur les deux NHI : « device links to tunneled native ports are missing! ». USB : gestion d’alimentation des ports potentiellement peu fiable et négociation U1 échouée sur 6-2 (adaptateur Realtek). Pas de conclusion de panne Thunderbolt ni de validation eGPU : aucun périphérique externe testé.

**Audio.** aplay/arecord confirment Speaker, Codec Output, Codec Input et HDMI (LG TV détectée). PipeWire/WirePlumber accessibles : sortie Apple mono par défaut à 40 %, HDMI à 40 %. Profil Apple actif output:mono-fallback, aucune source physique exposée ; seules les sources monitor des sorties apparaissent. Profil pro-audio disponible avec 2 sorties/1 entrée, sans activation. Capture ALSA présente mais capture PipeWire indisponible dans le profil courant. Lecture/capture réelles non testées.

**Autres avertissements relevés.** Pilote pcspkr déjà enregistré, limitations UEFI Secure Boot sur T2, avertissements CPU/SMT MDS, MMIO Stale Data et VMSCAPE. Ils sont consignés comme avertissements du noyau ; aucune politique de mitigation modifiée.

### Clavier GRUB et interface graphique : précisions

Le hub 1-8 n’est pas identifié comme un hub externe : lsusb le nomme « Hub in Aluminum Keyboard ». Le clavier Apple est relié à travers son propre hub intégré sur le contrôleur Intel, pas à travers T2. Le test futur consiste donc à comparer les ports physiques du Mac et, uniquement si un autre hub/adaptateur externe est utilisé, son retrait. Maintenir le Logitech K120 disponible lors d’un futur démarrage autorisé.

Lecture directe du menu actif : terminal_output gfxterm ; aucun terminal_input ni chargement explicite usb/hid/keyboard trouvé. Cela ne permet pas d’affirmer une défaillance de saisie firmware ; reconnaissance pré-noyau à tester physiquement. Aucun réglage GRUB changé.

La session graphique observée exécute gnome-shell ; aucun plasmashell trouvé. L’accès graphique fonctionne, mais l’environnement observé est GNOME, contrairement à la confirmation initiale KDE. Aucune session modifiée.

### Actions recommandées, non appliquées

1. Priorité SSH : après accord pour une action sur le service, rétablir l’écoute LAN lorsque [ADRESSE PRIVÉE EXPURGÉE] est disponible, contrôler ss et faire tester une connexion par clé depuis le poste administrateur. Préparer ensuite une solution persistante à la course de démarrage, en conservant le périmètre LAN actuel ; ne pas élargir l’écoute sans revue. Pas de reboot nécessaire pour ce rétablissement.
2. Préparer un lot séparé de firmwares Wi-Fi/Bluetooth adaptés au Macmini8,1, avec provenance et procédure vérifiées avant installation. Recontrôler la trace brcmfmac après correction.
3. Examiner le profil audio adapté à T2 et la capture avant toute modification ; faire les tests sonores avec l’utilisateur.
4. Analyser les avertissements ACPI/IRQ/Thunderbolt et la gestion d’alimentation USB selon leur impact observé. Valider un périphérique Thunderbolt avant la phase eGPU. Ne pas ajouter de paramètres noyau au hasard.
5. Tester le clavier Apple aux différents ports et la saisie firmware/GRUB lors d’un futur redémarrage explicitement autorisé. Conserver les deux secours Debian.

Statut final : diagnostic hôte effectué ; noyau/T2/SMC, stockage, LVM, Ethernet/Internet, inventaire USB et secours confirmés. SSH par clé correctement configuré mais accès LAN actuellement indisponible ; validation réelle par clé encore à faire après rétablissement. Son réel, clavier avant noyau et périphériques Thunderbolt externes nécessitent des tests fonctionnels complémentaires. Aucun changement système ni redémarrage réalisé.


## Correction durable SSH — diagnostic et proposition en attente d’accord

Diagnostic effectué le 11 octobre 2026. Sauvegarde et propositions : `/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437`. Archive configuration-avant.tgz (mode 600), empreinte SHA256, unités et état systemd, paramètres sshd effectifs et journaux. Aucun override local ssh.service.d/ssh.socket.d n’existait. Aucune clé privée copiée. Aucun réglage système ni service modifié.

Cause confirmée par journal monotone : sshd tente la liaison LAN à +20,976 s ; le lien Ethernet arrive à +24,656 s, DHCP attribue [ADRESSE PRIVÉE EXPURGÉE] à +24,840 s, NetworkManager-wait-online finit à +26,942 s. ssh.service dépend de network.target, pas de network-online.target, et démarre en parallèle de wait-online. Comme la liaison localhost réussit, sshd reste actif et Restart=on-failure ne déclenche aucune nouvelle tentative. Aujourd’hui enp4s0 = [ADRESSE PRIVÉE EXPURGÉE]/24, DHCP auto ; SSH actif mais seulement [ADRESSE PRIVÉE EXPURGÉE]:22. ssh.socket est désactivé/inactif et son unité fournisseur prévoit ListenStream=22 (écoute générale), à ne pas activer sans override.

Options étudiées : Wants/After=network-online.target réduirait la course actuelle mais ne garantit pas l’adresse exacte ni sa disponibilité après expiration de wait-online ou branchement tardif. Restart=on-failure seul est inefficace pour cet échec partiel. Une écoute [ADRESSE PRIVÉE EXPURGÉE] ou :: élargirait inutilement l’exposition. Une boucle de surveillance/reload est possible mais ajoute un mécanisme périodique. Solution proposée : sockets systemd limités aux deux adresses actuelles, FreeBind=yes, transmis à sshd Debian via son support de socket activation (LISTEN_FDS/LISTEN_PID présents dans le binaire installé).

Fichier proposé /etc/systemd/system/ssh.socket.d/10-jarvis-lan.conf :

```ini
[Socket]
ListenStream=
ListenStream=[ADRESSE PRIVÉE EXPURGÉE]:22
ListenStream=[ADRESSE PRIVÉE EXPURGÉE]:22
FreeBind=yes
```

La ligne vide remplace l’écoute générale du fournisseur. FreeBind permet de créer la socket avant l’attribution de l’adresse ; elle devient joignable à l’arrivée de [ADRESSE PRIVÉE EXPURGÉE], sans attente arbitraire ni redémarrage de sshd. Aucun changement global ip_nonlocal_bind.

Fichier proposé /etc/systemd/system/ssh.service.d/10-jarvis-socket.conf :

```ini
[Unit]
Requires=ssh.socket
After=ssh.socket
```

Conserver ssh.service activé ; activer ssh.socket après installation et validation de son override. Requires/After imposent la création des sockets avant tout démarrage du service. Le service reprend les sockets systemd. Une courte interruption du listener sera nécessaire pour transférer le port ; KillMode=process est configuré, mais le test depuis le Mac devra être une nouvelle connexion.

Conserver /etc/ssh/sshd_config.d/00-jarvis.conf intégralement : IPv4 uniquement, clés uniquement, root interdit, adminjarvis limité à localhost et [ADRESSE PRIVÉE EXPURGÉE]/24. Aucun port IPv6/global, règle routeur/NAT/pare-feu ou ouverture Internet ajouté. nft list ruleset est vide ; règles/redirections du routeur non auditées. On peut garantir l’absence d’ouverture supplémentaire par ce lot, pas certifier une configuration externe non inspectée. L’adresse [ADRESSE PRIVÉE EXPURGÉE] doit rester attribuée à ce Mac (réservation DHCP à confirmer) ; FreeBind ne compense pas un changement d’adresse ou une panne physique du réseau.

Après accord : vérifier archive et configuration inchangée, installer les deux overrides root:root 644 ; sshd -t, validation systemd des unités fusionnées ; arrêt ciblé du listener, daemon-reload, activation de ssh.socket, redémarrage ssh.service ; vérifier écoute strictement sur les deux adresses IPv4, service/socket, paramètres effectifs et journaux. En cas d’échec, restaurer les états initiaux et retirer uniquement les nouveaux overrides. Aucun reboot. Demander ensuite une nouvelle connexion depuis le Mac avec la clé existante et vérifier Accepted publickey dans les journaux. Le démarrage réel restera à valider lors d’un redémarrage distinctement autorisé.

Référence : manuel systemd.socket installé et documentation primaire https://github.com/systemd/systemd/blob/main/man/systemd.socket.xml (ListenStream et FreeBind). Statut : sauvegarde/diagnostic terminés, deux fichiers préparés dans le dossier de proposition uniquement ; application en attente de l’accord utilisateur.


### Correction SSH approuvée et appliquée — 11 octobre 2026, 18:25 CEST

Accord utilisateur : « oui ». Archive préalable vérifiée, SHA256 569f2d9b4e5d2b87eb1ba2ea5817355b853e8626108866f353f534a3563a696a ; configuration SSH inchangée au contrôle avant application.

Installés root:root 644 : /etc/systemd/system/ssh.socket.d/10-jarvis-lan.conf et /etc/systemd/system/ssh.service.d/10-jarvis-socket.conf, exactement selon la proposition. systemd-analyze verify ssh.service ssh.socket et sshd -t réussis. Listener SSH arrêté, daemon-reload exécuté, ssh.socket activé et démarré, ssh.service démarré. L’avertissement de rechargement d’unité lors de l’arrêt précédait daemon-reload et a été résolu par cette commande.

ssh.service et ssh.socket sont actifs et activés pour le démarrage. Configuration fusionnée : FreeBind=yes, sockets [ADRESSE PRIVÉE EXPURGÉE]:22 et [ADRESSE PRIVÉE EXPURGÉE]:22 ; Requires/After=ssh.socket confirmés pour ssh.service. ss montre les deux sockets partagés par systemd PID 1 et sshd PID 4353, sans écoute [ADRESSE PRIVÉE EXPURGÉE] ou IPv6. Journal à 18:25:18 : Server listening sur les deux adresses, aucun nouvel échec de liaison. Une connexion TCP depuis l’hôte obtient la bannière SSH sur chacune des deux adresses ; ceci ne valide pas une connexion distante authentifiée.

sshd -T reconfirme AddressFamily inet, PubkeyAuthentication yes, PasswordAuthentication no, KbdInteractiveAuthentication no, PermitRootLogin no, AllowUsers adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] et adminjarvis@[ADRESSE PRIVÉE EXPURGÉE]/24. Aucun changement de clé, configuration sshd, réseau, pare-feu, routeur, noyau ou GRUB. Aucun redémarrage Debian. Preuves après application dans le dossier de proposition : état, écoutes, journal, configuration effective et unités fusionnées.

Résultat : écoute SSH LAN rétablie et mécanisme persistant installé. Test demandé à l’utilisateur : ouvrir une nouvelle connexion depuis le Mac, par exemple ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no adminjarvis@[ADRESSE PRIVÉE EXPURGÉE] avec la clé habituelle. Ne pas transmettre la clé privée ; ne pas désactiver le contrôle de clé d’hôte. Confirmation utilisateur et entrée Accepted publickey à vérifier ensuite. Démarrage réel après reboot non testé ; attend une autorisation distincte. La garantie d’arrivée tardive concerne l’adresse [ADRESSE PRIVÉE EXPURGÉE] configurée : sa réservation DHCP et les règles du routeur restent à confirmer hors de ce lot.


## Phase C2 — préparation Wi-Fi/Bluetooth — 11 octobre 2026

Succès SSH confirmé par l’utilisateur et journal : Accepted publickey pour adminjarvis depuis [ADRESSE PRIVÉE EXPURGÉE] à 18:26:16, clé ED25519 attendue. Ethernet enp4s0 [ADRESSE PRIVÉE EXPURGÉE]/24 connecté ; sockets SSH localhost/LAN toujours présentes.

Matériel : Macmini8,1 ; Wi-Fi PCI 03:00.0 14e4:4464 rev03 / sous-système Apple 106b:07bf, BCM4364/3 avec firmware brcmfmac4364b2-pcie variante lanai-HRPN-u-7.5-X3. Bluetooth UART serial0-0, ACPI BCM2E7C:APPLE-UART-BLTH, BCM4364B0 Maui Olympic GEN (MFG), chip id123, via hci_uart_bcm et contrôleur PCI UART 00:1e.0. Aucun contrôleur Bluetooth USB séparé recensé ; iBridge 05ac:8233 et Headset 05ac:8103 sont des périphériques T2 distincts. Wi-Fi absent de NetworkManager ; aucun firmware 4364 ni BCM.hcd présent dans brcm. Journaux missing -2, Dongle setup/crash, Bluetooth baudrate -16 et patch BCM.hcd absent. BlueZ actif et contrôleur Bluetooth déjà détecté/alimenté : fonctionnement radio/appairage non validé.

Méthode 5 T2Linux reprise et vérifiée. Scripts lus, copies figées, récupération Apple Sonoma 14.6.1/build23G93 téléchargée dans le répertoire utilisateur, blocs SHA256 et signature RSA chunklist validés. Extraction des quatre fichiers Wi-Fi adaptés, empreintes identiques aux sources Apple. dmg2img utilisé depuis un paquet Debian extrait localement sans installation. Montage loop et HFS+ strictement en lecture seule puis démontage/détachement. Firmwares existants sauvegardés. Noyaux/initramfs et grub.cfg : empreintes avant/après identiques.

L’image et la méthode T2Linux ne fournissent pas de patch UART BCM4364B0 identifiable ; aucun BCM.hcd arbitraire ni fichier PCIe Bluetooth proposé. Objectif Bluetooth reste ouvert ; le lot prévoit des tests de découverte du contrôleur existant, pas une installation Bluetooth non justifiée.

Plan détaillé, fichiers/destinations/empreintes/commandes/validation/retour arrière : `/home/adminjarvis/JARVIS/rapports/phaseC2-preparation/plan-installation.md`. Manifestes et sources dans le même répertoire, script installation-proposee.sh préparé mais NON EXÉCUTÉ. Ce lot propose quatre ajouts /usr/lib/firmware/brcm root:root644, rechargement brcmfmac uniquement, scan Wi-Fi et Bluetooth borné ; aucune connexion Wi-Fi/appairage automatique, aucune interruption volontaire Ethernet/SSH, aucun noyau/GRUB/initramfs modifié. Aucune installation de firmware, aucun redémarrage, aucune phase NVIDIA. Installation et activation attendent l’autorisation demandée par l’utilisateur ; bilan matériel final à produire après ces tests.


### Phase C2 appliquée après accord — 11 octobre 2026, 18:34–18:35 CEST

Accord utilisateur « oui » pour les quatre fichiers Wi-Fi, le rechargement ciblé et les scans Wi-Fi/Bluetooth. Script installation-proposee.sh revu et exécuté : hashes source vérifiés, destinations préalablement absentes, copie des quatre fichiers listés dans manifest-installation.json, puis modprobe -r brcmfmac / modprobe brcmfmac. Aucune autre décharge de module ni relance de service. Les quatre destinations /usr/lib/firmware/brcm sont root:root 644 et leurs SHA256 correspondent au manifeste. Sauvegarde firmware-brcm-avant.tgz conservée. Aucun fichier Bluetooth installé.

**Wi-Fi : détection et réception radio validées.** Pilote PCI brcmfmac lié à 03:00.0 ; firmware BCM4364/3 version [ADRESSE PRIVÉE EXPURGÉE].32.5.92, FWID 01-88a8883 chargé ; TxCap blob trouvé. Interface wlp3s0 présente dans NetworkManager, état disconnected, scan réussi avec de nombreux réseaux (dont le réseau Bbox à signal 99). Aucune connexion Wi-Fi créée, aucun mot de passe demandé ni route Wi-Fi ajoutée. Association WPA2, DHCP Wi-Fi et trafic de données Wi-Fi restent non testés. RFKill sysfs : phy0 soft=0/hard=0.

Les demandes initiales de noms plus spécifiques .bin retournent encore -2 avant le succès de fallback sur lanai.bin ; ces messages ne sont plus un échec global du firmware. Aucun nouveau Dongle setup failed ou firmware crashed dans le journal de l’application. Anomalies restantes : cfg80211 « regulatory.db is malformed or signature is missing/invalid » (liens actuels vers regulatory.db-debian et signature -debian) ; erreurs de création P2P -52 (mise à jour adresse et p2p_disc), malgré une interface P2P listée dans NetworkManager. Scan Wi-Fi normal réussi ; P2P non validé. Aucune correction réglementaire, changement de pays, de backend ou paramètre noyau appliqué.

**Bluetooth : détection et découverte radio validées.** BlueZ hci0 Powered=yes ; scan borné à 15 secondes réussi et plusieurs appareils détectés. Aucun appairage, connexion de périphérique ou test de bonding. Au terme du client de scan, une commande séparée scan off retourne org.bluez.Error.Failed car la session de découverte est déjà terminée ; état final Discovering=no vérifié. Discoverable=no et Pairable=no conservés. RFKill hci0 soft=0/hard=0. Les erreurs historiques au boot (baudrate -16, BCM.hcd absent, absence reset) subsistent dans le journal historique ; aucun nouveau message bluetoothd pendant ce test. Le scan montre qu’elles n’empêchent pas la découverte, mais ne valide pas la fiabilité d’appairage/reconnexion. Aucun patch UART arbitraire ajouté.

**Ethernet/SSH préservés.** enp4s0 toujours connecté, adresse [ADRESSE PRIVÉE EXPURGÉE]/24, route par [ADRESSE PRIVÉE EXPURGÉE] métrique100. HTTPS deb.debian.org retourne HTTP/2 200 après rechargement. SSH PID4353 inchangé, sockets LAN et localhost conservées ; NetworkManager/ssh/ssh.socket actifs. Connexion Mac par clé validée avant cette phase, aucune nouvelle connexion Mac réalisée automatiquement après le lot.

**Périmètre et retour arrière.** Aucun noyau, initramfs ou grub.cfg modifié : sha256sum -c boot-sha256-avant.txt retourne OK pour les sept fichiers contrôlés. Aucun reboot, installation paquet système, modification Ethernet/SSH ou travail NVIDIA. Retour arrière prévu : retirer uniquement les quatre ajouts du manifeste après vérification de leurs hashes puis recharger uniquement brcmfmac si sûr ; archive antérieure disponible. Aucun rollback exécuté car détection/scan fonctionnent.

Preuves : phaseC2-preparation/installation.log, noyau-apres.log, wifi-scan-apres.log, bluetooth-scan.log, bluetooth-apres.log, reseau-apres.log, routes-apres.log, ssh-ecoutes-apres.log. Prochaines validations : association Wi-Fi au réseau choisi sans remplacement de la route Ethernet, puis appairage/connexion d’un périphérique Bluetooth identifié avec accord utilisateur. Pas de promesse de fonctionnement complet ou après reboot avant ces tests. Examiner ensuite regulatory.db et P2P dans un lot séparé si nécessaire ; aucun reboot requis pour commencer ces diagnostics.

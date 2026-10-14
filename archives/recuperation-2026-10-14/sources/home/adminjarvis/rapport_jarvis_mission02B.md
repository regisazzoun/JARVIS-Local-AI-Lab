# JARVIS — Mission 02B : Administration et préparation système

Date : 11 octobre 2026. Base : `rapport_jarvis_mission02.md`, relu pendant cette mission.

## Résultat

La préparation est terminée, mais aucune administration système n’a été exécutée. Aucun moyen autorisé d’exécution hors du bac à sable n’est disponible dans les outils de cette session. Le script `~/jarvis_mission02B.sh` est préparé pour une exécution manuelle depuis Konsole, avec les droits habituels de l’utilisateur.

SSH n’est pas actuellement opérationnel dans l’installation visible : client présent, serveur absent. Le système n’est pas encore déclaré prêt à installer T2Linux : sudo et réseau réels restent à valider, DKMS et en-têtes sont absents, les signatures du dépôt T2 et ses dépendances doivent être contrôlées.

## 1. Contrôles réellement exécutés

- Lecture complète du rapport Mission 02.
- Inventaire des outils exposés : seul exec_command fournit un shell général ; aucun connecteur d’administration de l’hôte ou accès SSH configuré n’est disponible.
- `id`, `sudo -n -l`, lecture des capacités et de NoNewPrivs.
- Recherche non intrusive de commandes et chemins : ssh présent, nsenter présent, pas de chemin /run/host observé. La présence de nsenter ne constitue pas une autorisation ; aucune tentative de changement d’espace de noms ou d’évasion n’a été faite. /run/sshd existe, ce qui ne prouve pas qu’un serveur tourne.
- `uname -r`, interrogation dpkg des quatre paquets, relevé Ethernet sysfs, df et simulation APT.
- `ip -br address` et résolution de deb.debian.org : échec dans la session restreinte.
- Consultation des documentations OpenSSH et T2Linux.
- Création du script Bash et de ce rapport dans le répertoire utilisateur, conformément au livrable demandé.
- Validation syntaxique du script avec bash -n ; exécution de --help ; test de --diagnostic dans le bac à sable, qui s’arrête correctement avant sudo et toute écriture avec le message « Session restreinte ».

Aucune utilisation d’exécution non sandboxée, de su, de nsenter, d’une interface graphique d’administration ou d’un accès distant pour contourner les protections. Aucun paquet installé, index APT actualisé, fichier système modifié ou service activé. Aucune partition ou entrée EFI modifiée, aucun noyau supprimé, aucun redémarrage. Aucune clé d’accès à un agent créée.

## 2. État des lieux actualisé

| Contrôle | Résultat | Limite |
|---|---|---|
| Compte | adminjarvis, UID 1000 | Groupes présentés par le bac à sable, pas validation des groupes hôte |
| Sudo | Installé mais refus de sudo -n -l | NoNewPrivs=1, capacités nulles et propriétaires remappés ; droits réels non validés |
| Debian / noyau | Debian 13.7 trixie ; 6.12.111+deb13-amd64 | Noyau T2 non installé |
| Ethernet | enp4s0 up, 1000 Mbit/s | IP/routes de l’hôte non accessibles |
| DNS / dépôts | Résolution interdite/échouée dans cette session | Aucun diagnostic de panne DNS hôte justifié |
| openssh-server | Non installé | Client seul ne fournit pas de serveur |
| dkms / linux-headers-amd64 | Absents | Compilation de modules non prête |
| nvme-cli | Absent | smartmontools était déjà installé |
| Racine | 402 Gio libres | Aucun changement de partition nécessaire sur cette base |
| /boot | 709 Mio libres | Estimer l’espace avant chaque nouveau noyau |
| ESP | 965 Mio libres | Intégrité des fichiers à contrôler depuis l’hôte |

La Mission 02 a identifié les noyaux Debian 6.12.111 et 6.12.107, et les sources trixie, trixie-security et trixie-updates avec main non-free-firmware. Aucune suppression ni modification de ces sources effectuée.

Simulations répétées sur le cache actuel : upgrade ne propose aucun changement ; installation des quatre paquets propose 11 nouveaux paquets et aucune suppression. Les sept dépendances sont linux-headers-6.12.111+deb13-amd64, linux-headers-6.12.111+deb13-common, linux-kbuild-6.12.111+deb13, openssh-sftp-server, pahole, runit-helper et uuid-runtime. Le cache n’ayant pas été rafraîchi, ce n’est pas une certification que Debian est à jour.

## 3. Script contrôlable pour Konsole

Fichier : `~/jarvis_mission02B.sh`. Il n’est pas nécessaire de le rendre exécutable ; le lancer avec bash. Ne pas utiliser sudo bash : le script conserve l’utilisateur habituel et appelle sudo seulement pour les commandes qui en ont besoin.

### Diagnostic sans changement de configuration

```bash
bash ~/jarvis_mission02B.sh --diagnostic
```

Le mode diagnostic vérifie Debian 13 amd64, absence de NoNewPrivs, outils préalables, sudo réel, bus systemd, Ethernet, IP/routes, DNS, accès HTTPS aux InRelease Debian, montages, espace, fichiers EFI, syntaxe GRUB et cohérence dpkg. Il inventorie les noyaux et simule les opérations APT. Il crée seulement un répertoire utilisateur privé `~/jarvis-02B-XXXXXXXX` avec journal, copie de grub.cfg et hashes des images noyau. Les commandes sudo peuvent produire leurs journaux d’authentification usuels. Les journaux du script peuvent contenir des adresses réseau ; ne pas les publier sans relecture.

Tout échec arrête le script. Des avertissements dans journalctl ou systemctl --failed doivent être examinés même si les commandes elles-mêmes réussissent. Le diagnostic ne décide pas automatiquement que tous les avertissements sont bénins.

### Application après accord explicite

```bash
# À lancer seulement après validation du diagnostic et accord sur les opérations.
bash ~/jarvis_mission02B.sh --appliquer /chemin/cle_du_poste_administrateur.pub
```

La clé doit être une seule clé publique simple, sans options authorized_keys. Son empreinte sera affichée et demandée à l’approbation. La clé privée doit rester sur le poste administrateur ; le script ne la génère pas et ne la copie pas.

Le mode application refuse une session restreinte, un lancement root, un autre compte qu’adminjarvis, une configuration SSH déjà présente, un serveur déjà installé, des liens symboliques SSH ou des surcharges des unités systemd ciblées. Il ne prétend pas réparer un système déjà partiellement modifié. Après un échec d’installation, une reprise doit être analysée et préparée ; ne pas supprimer ces garde-fous.

Deux confirmations sont nécessaires : le plan général avant écritures système, puis les listes de paquets actualisées avant installation. APT reste interactif, sans -y, sans full-upgrade et sans autoremove. La confirmation dans le script ne remplace pas l’accord demandé dans cette conversation si l’agent devait effectuer l’opération.

## 4. Liste précise des opérations proposées à validation

1. Actualiser les index avec `apt-get -o APT::Update::Error-Mode=any update`, sans désactivation des signatures ; arrêter si un dépôt échoue. Afficher les nouvelles simulations et obtenir leur approbation.
2. Marquer manuels les paquets de noyaux versionnés déjà installés pour les préserver. Conserver le métapaquet Debian. Sauvegarder le menu GRUB et les hashes des images avant intervention.
3. Masquer de manière persistante ssh.service et ssh.socket avant installation pour empêcher leur activation automatique par les scripts des paquets. Ce blocage ciblé n’altère pas sudo ou les protections du bac à sable. Aucun serveur SSH préexistant n’est pris en charge par ce scénario.
4. Exécuter `apt-get --no-remove upgrade`, puis installer openssh-server, dkms, linux-headers-amd64 et nvme-cli avec leurs dépendances. Les mises à jour peuvent installer un nouveau noyau Debian et recharger d’autres services ; elles ne redémarrent pas la machine sur initiative du script. Arrêter sur erreur ou proposition incompatible avec --no-remove.
5. Sauvegarder la configuration SSH du paquet nouvellement installé, puis la remplacer par une configuration minimale vérifiable : écoute IPv4 sur 127.0.0.1:22 uniquement, PermitRootLogin no, utilisateur adminjarvis uniquement, authentification publickey obligatoire, mots de passe et authentification interactive désactivés. Le choix de clés uniquement est possible ici car une clé valide est requise et SSH reste local ; l’accès Konsole reste disponible.
6. Créer ou compléter ~/.ssh/authorized_keys avec la seule clé publique approuvée, droits 700 pour .ssh et 600 pour authorized_keys. Sauvegarder le fichier existant, s’il y en a un ; aucun droit sudo supplémentaire.
7. Valider sshd -t et la configuration effective, les noyaux conservés, grub-script-check, apt-get check, dpkg --audit, le lien build du noyau actif et dkms status.
8. Seulement après ces contrôles, démasquer les deux unités, désactiver ssh.socket et activer ssh.service. Contrôler le service et son écoute locale. Aucun port du routeur ou règle réseau modifié.

Les écritures SSH prévues sont /etc/ssh/sshd_config et ~/.ssh/authorized_keys, plus les états systemd et APT listés ci-dessus. Le script remplace uniquement la configuration d’une première installation SSH, sans inclure automatiquement d’autres fragments de configuration. Il n’est pas destiné à migrer un serveur existant.

### Limite volontaire d’accès SSH

SSH préparé sur 127.0.0.1 est accessible depuis JARVIS seulement : **ce lot ne fournit pas encore l’administration SSH depuis un autre poste du LAN**. Cela permet de préparer et tester le service sans écoute sur une adresse exposée à Internet, notamment IPv6. L’ouverture LAN nécessite de relever l’adresse et le sous-réseau réels, vérifier le filtrage et l’absence de redirection du routeur, puis approuver une configuration ciblée. Ne pas remplacer simplement ListenAddress par 0.0.0.0.

Une connexion authentifiée reste à tester après application avec la clé privée correspondante, depuis JARVIS pour la configuration locale. Si la clé privée se trouve uniquement sur le poste distant, ce test attendra la préparation de l’accès LAN ou un moyen local de signature déjà autorisé ; ne pas copier la clé privée sur le serveur pour faciliter le test.

Source : [configuration OpenSSH](https://man.openbsd.org/sshd_config).

### Gestion des erreurs et retour arrière

Le script utilise set -Eeuo pipefail et s’arrête dès une erreur, en indiquant le journal et la ligne. Il n’est pas transactionnel : APT peut avoir installé une partie des paquets avant un échec. Il ne lance pas automatiquement dpkg --configure -a ou une réparation.

Tant que le lot SSH n’a pas été validé, les unités restent masquées, y compris après un redémarrage manuel. Examiner les sauvegardes et la configuration avant de proposer une correction puis de réactiver le service. Aucune restauration ou suppression automatique ne suit un échec. Une erreur après l’activation finale peut laisser le service local actif ; vérifier son état dans ce cas. Les confirmations sont interactives et le script doit rester dans Konsole, sans exécution unattended.

Les contrôles de présence et de hashes vérifient la conservation des images noyau ; les initramfs peuvent légitimement être régénérés par les paquets. Les en-têtes du noyau actif peuvent manquer si le métapaquet vise déjà une version plus récente : le script s’arrêtera et proposera une installation séparée des en-têtes versionnés, après accord. Aucun redémarrage automatique pour résoudre cette situation.

## 5. Préparation T2Linux

Le dépôt communautaire documente Debian trixie, linux-t2 et linux-t2-lts. Pour la base serveur, examiner d’abord la variante LTS et ses en-têtes exacts. Aucun dépôt T2 ajouté et aucun paquet T2 installé par le script 02B.

Conditions restant à valider :

- Diagnostic hôte réussi et alertes réseau/journaux examinées.
- Base Debian cohérente, noyaux de secours conservés, fichiers EFI et menu GRUB contrôlés, espace /boot estimé pour le noyau retenu.
- Provenance de la clé du mainteneur, empreinte, signatures InRelease du dépôt commun et du dépôt trixie, fraîcheur des métadonnées et hashes des index/paquets vérifiés.
- Clé dédiée avec Signed-By ; pas de trusted=yes, AllowUnauthenticated ou trousseau global ajouté pour faciliter l’installation.
- Architecture, versions, dépendances et scripts de maintenance examinés, simulation T2 sans suppression de Debian.
- En-têtes du noyau T2 disponibles ; compatibilité NVIDIA/DKMS vérifiée pour la branche retenue. DKMS installé seul ne garantit pas cette compatibilité.
- Paramètres noyau et stratégie de démarrage présentés avant modification. Accord séparé pour l’installation T2 et pour tout redémarrage.

Le mainteneur indique que les pilotes T2 sont intégrés à ses noyaux : ne pas empiler les paquets autonomes apple-bce/applesmc-t2 déjà inclus. Aucun besoin de Touch Bar, trackpad, Touch ID ou APFS pour cette mission Mac mini. Le SSD et Thunderbolt sont déjà reconnus par Debian ; Wi-Fi BCM4364 et audio T2 demandent encore validation. Aucune restauration macOS ou modification de partition prévue.

La consultation du README établit une provenance documentaire et une compatibilité annoncée avec trixie ; elle ne constitue pas une validation cryptographique des signatures ni un test binaire. Ces contrôles restent à effectuer avant installation.

Source : [dépôt T2 du mainteneur](https://github.com/AdityaGarg8/t2-ubuntu-repo).

## 6. Validation du livrable et statut final

Tests réalisés sur le script : syntaxe Bash valide, aide fonctionnelle, arrêt explicite dans le bac à sable sans administration système. Le chemin d’application n’a pas été exécuté ; pas de test d’installation ou de SSH authentifié, et pas de validation dynamique complète sur Debian hôte. ShellCheck n’est pas disponible dans le PATH interrogé ; aucun outil ajouté pour cela.

**Réellement exécuté :** diagnostics accessibles, simulations sur cache APT, recherches documentaires, création du script et du rapport, tests de syntaxe/aide/refus d’environnement restreint.

**En attente :** exécution du diagnostic dans Konsole et revue de ses résultats ; clé publique et empreinte du poste administrateur ; accord sur les huit opérations précises ; exécution manuelle de l’application et revue des résultats ; préparation séparée de l’accès LAN et du dépôt T2.

**SSH opérationnel : non.** OpenSSH Server reste absent ; son installation et activation ne sont pas exécutées. Le script préparera un service local uniquement, à valider après exécution.

**Prêt pour installation du noyau Apple T2 : non, préparation partielle.** Sudo/réseau hôte, cohérence après mises à jour, en-têtes/DKMS, signatures et paquets T2 doivent encore être validés. Aucun changement de noyau ni redémarrage autorisé ou effectué.

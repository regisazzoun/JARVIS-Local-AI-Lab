# JARVIS — Mission 02 : Configuration Apple T2 et administration Debian

Date : 11 octobre 2026. Statut : diagnostics et préparation réalisés ; phase 1 partiellement vérifiable ; installations et configuration en attente d’accord et d’un accès hôte approprié.

## 1. Cadre et autorisations

Machine : Mac mini 2018 Macmini8,1, Core i7-8700B, 6 cœurs / 12 threads, 32 Go RAM, Debian 13.7 trixie avec KDE Plasma annoncé par l’utilisateur, SSD Apple AP0512M dédié à Debian. Deux Razer Core sont prévus : Quadro RTX 5000 16 Go et RTX 2080 Ti 11 Go ; aucun GPU NVIDIA n’est actuellement énuméré par PCI.

Autorisations reçues : diagnostics en lecture seule, préparation des commandes et création de ce rapport. Aucune autorisation d’installation, de modification système, de changement de noyau ou de redémarrage n’a été donnée pour cette mission.

Opérations exécutées : lectures système, inventaire PCI, lecture des dépôts et de la base dpkg, simulations APT, tests DNS/HTTPS limités, consultation des sources techniques et création de ce fichier. Aucun paquet installé, aucune configuration modifiée, aucun redémarrage. Aucun accès administrateur permanent accordé, aucune protection désactivée.

Le dual boot est abandonné : aucune restauration macOS, modification de partition, suppression de noyau ou nettoyage des entrées EFI Apple n’est proposé.

## 2. Phase 1 — Contrôles et résultats

### Sudo réel sur l’hôte

`sudo -n -l` échoue : `/etc/sudo.conf` est présenté comme appartenant à l’UID 65534, et le drapeau « no new privileges » empêche l’élévation. `/proc/self/status` confirme `NoNewPrivs: 1`, capacités effectives nulles et UID 1000. Les propriétaires sont remappés dans l’environnement isolé.

Conclusion : sudo est installé, version `1.9.16p2-3+deb13u2`, mais son fonctionnement réel sur l’hôte n’est pas validé. Ne pas modifier les permissions de sudo.conf, sudoers ou les protections pour corriger un effet du bac à sable. Il faut réaliser les contrôles depuis Konsole sur l’hôte, avec l’authentification habituelle de l’utilisateur.

### Ethernet, Internet et DNS

`enp4s0` : état `up`, porteuse présente, liaison négociée à 1000 Mbit/s. Pilote `tg3`, carte Broadcom BCM57766. Les deux domaines Thunderbolt restent en sécurité `user`.

`/etc/resolv.conf`, généré par NetworkManager, contient le domaine de recherche `lan`, DNS IPv4 `192.168.1.254` et IPv6 `2001:861:3895:b000:56c4:5bff:fed7:e52c`.

`ip -br address` et `ip route` échouent : ouverture de socket netlink interdite. Les résolutions de `deb.debian.org` et `security.debian.org` via Python échouent avec « Temporary failure in name resolution ». L’essai HTTPS vers Debian échoue au même stade.

Conclusion : lien Ethernet confirmé, mais IP, routes, DNS effectif et accès Internet de l’hôte non validés. L’échec dans le réseau isolé ne prouve pas une panne DNS du serveur. Aucune modification réseau proposée sans diagnostic hôte.

### Debian, APT et cohérence des paquets

Debian GNU/Linux 13, version complète 13.7, trixie, amd64. Sources visibles :

```text
deb http://deb.debian.org/debian/ trixie main non-free-firmware
deb http://security.debian.org/debian-security trixie-security main non-free-firmware
deb http://deb.debian.org/debian/ trixie-updates main non-free-firmware
```

Ces sources correspondent à Debian trixie et ses mises à jour. L’utilisation d’HTTP n’implique pas l’absence d’authentification APT : celle-ci repose sur les métadonnées signées. Aucune mise à jour des index ni vérification cryptographique fraîche n’a été effectuée pendant cette mission.

`dpkg --audit` ne produit aucun signalement. Cela ne constitue pas une vérification exhaustive de tous les fichiers de paquets.

`apt-get -s -o Debug::NoLocking=1 upgrade` : 0 mise à jour, 0 installation, 0 suppression selon le cache existant. Ce résultat ne permet pas d’affirmer que le système est à jour auprès des dépôts actuels.

Simulation `install openssh-server dkms linux-headers-amd64 nvme-cli` : 11 nouveaux paquets, aucune suppression, aucune mise à jour. Dépendances : openssh-sftp-server, runit-helper, uuid-runtime, les en-têtes 6.12.111 communs et amd64, linux-kbuild et pahole. Simulation seulement, aucun paquet installé.

| Outil / paquet | État |
|---|---|
| sudo, openssh-client | Installés |
| openssh-server | Absent ; candidat en cache `1:10.0p1-7+deb13u4` |
| dkms | Absent ; candidat en cache `3.2.2-1~deb13u1` |
| linux-headers-amd64 | Absent ; candidat `6.12.111-1` |
| build-essential | Installé `12.12` |
| curl, wget, ca-certificates, gnupg | Installés |
| pciutils, usbutils, bolt | Installés |
| smartmontools | Installé `7.4-3` ; binaire `/usr/sbin/smartctl` confirmé |
| nvme-cli | Absent ; candidat `2.13-2` |
| nvidia-driver | Non installé ; aucun candidat dans les index configurés |

Correction du rapport Mission 01 : smartctl était absent du PATH interrogé, mais smartmontools est bien installé et son binaire existe dans `/usr/sbin`. Aucun remplacement ou réinstallation nécessaire à ce titre.

Les composants APT `contrib` et `non-free` ne sont pas activés. Le choix éventuel d’un dépôt pour NVIDIA sera une opération distincte à approuver ; aucune source modifiée.

### Noyau et journaux

Noyau actif : `6.12.111+deb13-amd64`, paquet `6.12.111-1`, Debian standard, PREEMPT_DYNAMIC. Le noyau `6.12.107+deb13-amd64` est également présent. Métapaquet linux-image-amd64 installé.

`/lib/modules/6.12.111+deb13-amd64/build` est absent : la base de compilation des modules pour le noyau courant n’est pas prête. DKMS absent.

`journalctl -b -k -p warning` ne donne aucune entrée accessible et signale des droits insuffisants. `systemctl` ne peut pas joindre le bus système. Aucun bilan réel des erreurs du démarrage ou des services n’est donc possible ici.

### EFI, GRUB et espace

| Zone | Partition / système de fichiers | Espace disponible |
|---|---|---:|
| EFI | nvme0n1p1, 976 Mio, FAT32 | 965 Mio |
| /boot | nvme0n1p2, 977 Mio, ext4 | 709 Mio |
| Racine | LVM sur nvme0n1p3, ext4, 433 Gio utilisables | 402 Gio |

Les images et initramfs des deux noyaux Debian existent. Leur présence ne vaut pas validation cryptographique ou test de démarrage du noyau de secours.

EFI : BootCurrent 0000, Debian via `\EFI\debian\shimx64.efi`. BootOrder 0000,0080. Anciennes entrées Apple conservées sans intervention. `mokutil --sb-state` indique Secure Boot désactivé ; le réglage Apple T2 dans la récupération n’a pas été contrôlé.

GRUB : entrée par défaut 0, délai 5 secondes, paramètres `quiet`. grub.cfg n’est pas lisible dans cette session ; le contenu de l’ESP et la validité complète de la chaîne EFI/GRUB restent à contrôler depuis l’hôte. Ne pas lancer grub-install par précaution : aucune panne de démarrage n’est démontrée.

Un disque USB contient une image ISO Debian 13.7. Aucun repartitionnement prévu. Les montages en lecture seule observés sont affectés par le bac à sable et ne prouvent pas un défaut du système de fichiers hôte.

### Composants Apple T2

| Composant | Observation | Besoin à examiner |
|---|---|---|
| ANS2 NVMe `106b:2005` | Pilote nvme actif | Stockage déjà accessible ; surveiller après changement de noyau |
| T2 Bridge `106b:1801` | Pas de pilote actif indiqué | Support apple-bce intégré au noyau T2 |
| Secure Enclave `106b:1802` | Pas de pilote actif indiqué | Aucun service Touch ID nécessaire à ce Mac mini |
| Audio Apple `106b:1803` | Pas de pilote actif indiqué | Support noyau T2 et configuration audio adaptée si nécessaire |
| Broadcom BCM4364 `14e4:4464` | Pas de pilote actif associé | Firmwares Apple et diagnostic brcmfmac |
| Contrôleurs JHL7540 Thunderbolt | Pilote thunderbolt actif | Autorisation et essais physiques des eGPU |

Aucun fichier contenant `4364` dans `/usr/lib/firmware/brcm`, aucune interface Wi-Fi visible. Firmwares BCM4364 probablement manquants ; noms exacts à confirmer dans les journaux hôte. Aucun module apple-bce chargé dans le relevé précédent, noyau toujours identique. Les paquets génériques firmware-brcm80211, firmware-intel-graphics, firmware-misc-nonfree, firmware-sof-signed et intel-microcode étaient confirmés lors de Mission 01.

Pas d’installation de pilotes Touch Bar, trackpad ou Touch ID pour ce Mac mini. Pas d’APFS ni de restauration macOS. Un éventuel téléchargement d’une image Apple destiné uniquement à extraire des firmwares serait une proposition séparée, sans installation macOS et avec accord préalable.

### SSH

Client disponible ; `ssh -V` affiche OpenSSH_10.0p2 Debian-7+deb13u4. Version du paquet openssh-client : `1:10.0p1-7+deb13u4`, différence conservée telle qu’observée.

Serveur absent : openssh-server non installé, `/usr/sbin/sshd`, `/etc/ssh/sshd_config` et unité ssh.service absents. Aucun test d’accès distant effectué. Aucun serveur entrant standard OpenSSH n’est disponible dans l’installation visible.

## 3. Commandes de diagnostic à exécuter depuis Konsole sur l’hôte

Commandes préparées, non exécutées sur un terminal hôte par l’agent. Elles ne modifient pas les configurations ; sudo peut demander le mot de passe habituel et les outils peuvent produire leurs journaux usuels.

```bash
sudo -l
sudo id
ip -br address
ip route
ip -6 route
nmcli device status
getent ahosts deb.debian.org
getent ahosts security.debian.org
curl -I --connect-timeout 10 --max-time 20 https://deb.debian.org/debian/
systemctl --failed --no-pager
systemctl status NetworkManager --no-pager
sudo journalctl -b -k -p warning --no-pager
sudo journalctl -b -k --grep='brcmfmac|firmware|thunderbolt|nvme' --no-pager
sudo ss -lntup
sudo nft list ruleset
findmnt / /boot /boot/efi
df -hT / /boot /boot/efi
sudo pvs
sudo vgs
sudo lvs
sudo smartctl -a /dev/nvme0
sudo ls -l /boot/efi/EFI/debian
sudo grub-script-check /boot/grub/grub.cfg
sudo rg 'menuentry|submenu' /boot/grub/grub.cfg
```

Si un outil est absent ou une commande échoue, relever l’erreur et analyser avant d’envisager une installation ou une correction. Ne pas interpréter un refus d’authentification comme une invitation à modifier sudoers.

## 4. Modifications proposées et justification — accord nécessaire

### Lot A : mises à jour Debian et outils

Prérequis : phase 1 validée sur l’hôte, accès sudo fonctionnel, DNS/HTTPS vérifiés. Opérations proposées : rafraîchir les index APT signés, examiner une nouvelle simulation, puis installer les mises à jour et les outils manquants approuvés.

```bash
# Ne pas exécuter avant accord explicite.
sudo apt-get update
apt-get -s upgrade
apt-get -s install openssh-server dkms linux-headers-amd64 nvme-cli
# Après revue de la nouvelle liste de paquets :
sudo apt-get upgrade
sudo apt-get install openssh-server dkms linux-headers-amd64 nvme-cli
```

Justification : administration distante, compilation des modules, diagnostic NVMe. build-essential, smartmontools et les outils de téléchargement sont déjà présents. Une nouvelle version du noyau pourrait être installée par les mises à jour ; sa liste devra être présentée avant exécution. Aucun full-upgrade automatique, autoremove ou suppression de noyau. L’installation de paquets peut démarrer ou recharger des services via leurs scripts : ces effets font partie du lot à approuver. L’installation d’OpenSSH peut démarrer immédiatement le service ; prévoir l’accès LAN et le durcissement avant le début de ce lot.

Conserver explicitement les images Debian 6.12.111 et 6.12.107 et leurs fichiers de démarrage. Si elles sont marquées automatiques, proposer leur marquage manuel par apt-mark dans le lot autorisé ; ne pas désinstaller le métapaquet Debian. Aucun redémarrage inclus dans ce lot.

### Lot B : SSH administrable et sûr

Obtenir la clé publique du poste administrateur et son empreinte ; ne jamais demander la clé privée. Préparer authorized_keys pour adminjarvis avec droits appropriés, sans droit sudo supplémentaire. Une clé peut être générée sur le poste client si nécessaire, avec phrase secrète.

Configuration proposée dans un fichier inclus par sshd, après inspection des règles existantes :

```text
PermitRootLogin no
PubkeyAuthentication yes
```

Valider `sshd -t` puis la configuration effective avec `sshd -T -C user=adminjarvis,host=JARVIS-MacMIini,addr=ADRESSE_CLIENT` en remplaçant l’adresse. Activer le service avec `systemctl enable --now ssh` si nécessaire. Tester une connexion par clé depuis un second terminal client en conservant l’accès local.

La désactivation de PasswordAuthentication et KbdInteractiveAuthentication n’est proposée qu’après réussite de la connexion par clé et vérification des méthodes d’accès nécessaires. Aucun port SSH arbitraire, ouverture WAN, privilège permanent ou changement réseau prévu. Contrôler l’exposition IPv4/IPv6 et le pare-feu avant de déclarer le service validé.

La clé publique client n’a pas été fournie ; l’authentification par clé n’est donc pas prête à être appliquée.

### Lot C : provenance et signatures T2Linux

Le wiki T2Linux pointe vers le dépôt communautaire AdityaGarg8/t2-ubuntu-repo. Son README décrit un dépôt commun et un dépôt de noyaux spécifique `trixie`, avec linux-t2 et linux-t2-lts. Proposition pour la stabilité : examiner d’abord linux-t2-lts et les en-têtes associés, sans figer une version avant lecture des métadonnées.

Éléments réellement vérifiés via consultation web : origine documentaire, existence annoncée de KEY.gpg, InRelease et Release.gpg, prise en charge de trixie décrite. **Non vérifiés cryptographiquement : empreinte de clé, signature InRelease, fraîcheur et hashes des paquets. La compatibilité binaire effective n’est pas encore validée.** La simple présence de ces fichiers ne suffit pas.

Procédure proposée avant toute installation T2 :

1. Télécharger dans un répertoire de travail la clé et les métadonnées du dépôt commun et du dépôt trixie, sans exécuter de script distant.
2. Afficher l’empreinte avec `gpg --show-keys --with-fingerprint KEY.gpg` et la confronter à une publication authentifiée du mainteneur. Si aucune corroboration satisfaisante n’est disponible, signaler la limite et arrêter avant ajout du dépôt.
3. Vérifier la signature de chaque InRelease avec gpgv et une clé dédiée ; examiner les dates et les sommes SHA256 des index et paquets. Vérifier les hashes des paquets téléchargés contre les index authentifiés.
4. Après accord pour l’ajout du dépôt, placer la clé dans `/etc/apt/keyrings` et utiliser Signed-By pour les deux sources. Ne pas importer la clé dans le trousseau global, ne pas utiliser trusted=yes ou AllowUnauthenticated.
5. Examiner architecture amd64, dépendances, versions des noyaux et en-têtes, provenance APT et scripts de maintenance ; simuler l’installation et vérifier l’absence de suppression ou migration d’autres paquets Debian.
6. Présenter les paquets exacts, l’espace dans /boot et les effets GRUB/initramfs avant de demander l’accord d’installation du noyau.

Le dépôt prévient de ne pas ajouter les paquets de pilotes autonomes apple-bce/applesmc-t2 et autres pilotes déjà intégrés lorsqu’on utilise ses noyaux T2. Ne pas empiler ces modules. Aucun APFS nécessaire. Aucun ajout de dépôt réalisé.

Sources : [README du mainteneur](https://github.com/AdityaGarg8/t2-ubuntu-repo), [guide T2Linux Debian](https://wiki.t2linux.org/distributions/debian/installation/). Les informations résumées ici ne constituent pas un audit du code ou une certification du dépôt.

### Lot D : noyau T2 et préparation DKMS/NVIDIA

Installer seulement après validation du lot C et accord spécifique : noyau T2 retenu, en-têtes exacts, configuration audio éventuellement utile. Vérifier l’initramfs, le menu GRUB et l’entrée Debian de secours. Un nouveau noyau peut modifier l’entrée sélectionnée par GRUB_DEFAULT=0 : présenter le choix de démarrage prévu avant application.

Les paramètres recommandés par le wiki, notamment intel_iommu=on iommu=pt pm_async=off, sont à examiner et à approuver séparément. Aucun paramètre de sécurité, Secure Boot, IOMMU ou Thunderbolt désactivé pour contourner une erreur.

Préparation NVIDIA : les deux GPU annoncés sont de génération Turing. Choisir une même branche de pilote prenant en charge les deux identifiants PCI une fois relevés ; examiner modules ouverts/propriétaires selon la branche et les paquets réellement disponibles. Ne pas mélanger installation .run et paquets APT.

Critères DKMS : en-têtes et lien build correspondant à chaque noyau cible, compilateur compatible, source du module adaptée à l’API du noyau, compilation sans erreur et journal de construction examiné. Une simulation APT ne prouve pas la compatibilité DKMS. Aucun module NVIDIA n’est actuellement installé ou compilé : cette compatibilité reste à tester après accord, avant de basculer le démarrage sur le noyau T2.

La documentation NVIDIA décrit l’installation Debian 13 et les modules DKMS ouverts. Le noyau communautaire T2 doit être validé séparément ; son support ne se déduit pas du support de Debian 13.

Sources : [NVIDIA pour Debian](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/debian.html), [modules noyau NVIDIA](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/kernel-modules.html).

## 5. Phase 3 — Tests de validation prévus

| Contrôle | Résultat actuel | Validation à effectuer après opérations autorisées |
|---|---|---|
| Cohérence dpkg | Aucun signalement de dpkg --audit | dpkg --audit et apt-get check après installation |
| Mise à jour | Simulation sans changement sur cache existant | Actualiser les index signés puis réexaminer les candidats |
| Réseau | Ethernet 1 Gbit/s | IP/routes, DNS, HTTPS et état NetworkManager depuis l’hôte |
| SSH | Client présent, serveur absent | sshd -t, configuration effective, service actif, clé fonctionnelle, root interdit |
| EFI/GRUB | Entrée Debian EFI présente | Fichiers EFI lisibles, grub-script-check, images/initramfs et secours présents |
| T2 | Plusieurs fonctions sans pilote actif | Modules, journaux, stockage, audio et Wi-Fi après démarrage autorisé |
| DKMS | Absent, en-têtes absents | dkms status, compilation et journaux NVIDIA pour noyau cible |
| Thunderbolt | Deux domaines en sécurité user | Détection et autorisation du boîtier, sans désactivation globale de sécurité |

Aucun test de nouveau noyau possible sans installation et redémarrage autorisés. Aucun test ne sera présenté comme réussi avant observation de son résultat.

## 6. Erreurs et suites

| Erreur observée | Analyse | Suite proposée |
|---|---|---|
| Sudo bloqué par NoNewPrivs et UID remappés | Restriction de session | Contrôle local hôte ; aucune modification sudoers |
| Netlink / bus système refusés | Isolation réseau et services | Exécuter les lectures depuis Konsole |
| DNS et HTTPS échouent | Réseau de session restreint | Vérifier DNS de l’hôte avant correction |
| Journaux inaccessibles | Droits insuffisants | Lecture via sudo sur l’hôte |
| grub.cfg illisible | Permissions dans le bac à sable | Lecture et vérification depuis l’hôte |
| sshd/configuration absents | OpenSSH Server non installé | Installation après accord |
| lien build absent | En-têtes noyau absents | Installation d’en-têtes après accord |
| candidat nvidia-driver absent | Index actuels sans offre NVIDIA | Choix et validation du dépôt lors de Mission 03 |

Pas de tentative de correction système à la suite de ces erreurs. Les limitations ont été analysées avant toute proposition de suite.

## 7. Opérations restantes et accord demandé

Priorité : compléter et valider la phase 1 depuis l’hôte. Ensuite proposer l’exécution du lot A et du lot B : actualisation APT, revue des nouvelles simulations, mises à jour Debian, installation des quatre paquets manquants et de leurs dépendances, conservation des anciens noyaux, activation SSH, installation de la clé publique client et interdiction du root distant. Aucun redémarrage, dépôt T2/NVIDIA ni changement de réseau inclus dans cet accord initial.

La demande d’accord découle explicitement de la règle de Mission 02 : « Avant toute installation de paquets, modification de configuration, changement de noyau ou redémarrage, présente les opérations prévues et demande mon accord. » Même avec cet accord, la session actuelle ne peut pas effectuer l’administration de l’hôte ; aucune protection ne sera contournée. Un terminal hôte et la clé publique client restent nécessaires.

Les lots C et D feront l’objet de présentations et d’accords distincts après vérification de provenance, signatures, dépendances et stratégie de secours. Le redémarrage fera l’objet d’un accord explicite séparé.

## 8. Proposition de Mission 03 — Installation et validation du Razer Core avec la Quadro RTX 5000

Objectif : valider d’abord un seul boîtier et la Quadro RTX 5000 16 Go, puis préparer l’arrivée de la RTX 2080 Ti sans modifier le partitionnement.

1. Identifier le modèle exact du Razer Core, son alimentation, le câble Thunderbolt et la carte ; vérifier leur compatibilité physique et électrique dans les documentations constructeur.
2. Relever le fonctionnement de la base Debian, SSH et des noyaux avant branchement ; garder l’affichage KDE sur l’Intel lorsque cela convient à l’usage calcul.
3. Brancher le boîtier et relever les événements Thunderbolt/PCIe ; autoriser uniquement le périphérique identifié après accord, sans désactiver la sécurité globale.
4. Relever l’identifiant PCI NVIDIA puis présenter la branche de pilote, sa provenance, la signature du dépôt, les dépendances et la compatibilité DKMS avec les noyaux Debian/T2.
5. Installer le pilote après accord et valider nvidia-smi, les 16 Go de VRAM, température, consommation et un calcul CUDA simple. Tout redémarrage nécessite une autorisation séparée.
6. Tester stabilité et journaux sous charge ; tester les branchements uniquement selon les capacités validées. Ne pas débrancher un GPU utilisé par une charge de calcul.
7. Établir un bilan de performance et la procédure de retour arrière avant d’ajouter le second Razer Core avec la RTX 2080 Ti.

Livrable proposé : rapport Mission 03 avec identification du matériel, commandes autorisées, tests, erreurs, performances et configuration retenue. Docker/Ollama/Open WebUI pourront ensuite être installés et validés dans une mission distincte.

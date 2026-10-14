# Mission 01 — Audit de JARVIS

Date de l’audit : 11 octobre 2026. Machine : `JARVIS-MacMIini`.

## Périmètre et méthode

Audit en lecture seule du matériel, des périphériques, du réseau, du partitionnement, du démarrage EFI/GRUB, du noyau, des firmwares et de Thunderbolt. Vérification de sudo et SSH sans modification de leur configuration.

Aucun paquet installé, aucun service reconfiguré et aucun redémarrage effectué. Ce rapport est enregistré à la demande explicite de l’utilisateur ; sa création constitue la seule écriture effectuée pour cette demande.

Les relevés proviennent d’un environnement d’exécution isolé : restrictions réseau, `NoNewPrivs: 1`, propriétaires remappés et montages en lecture seule. Les refus observés dans cet environnement ne doivent pas être interprétés comme des pannes de l’hôte. Les caractéristiques issues de PCI, sysfs et des fichiers système sont distinguées des vérifications impossibles.

## Synthèse

- Mac mini Intel 2018 confirmé : Apple `Macmini8,1`, Core i7, 32 Go de RAM.
- SSD interne, GPU Intel, Ethernet et deux contrôleurs Thunderbolt reconnus par le noyau Debian.
- Noyau Debian standard actif ; support T2 incomplet constaté dans l’inventaire des pilotes.
- Wi-Fi BCM4364 sans pilote actif associé ni interface Wi-Fi visible ; aucun fichier de firmware BCM4364 identifié.
- Aucune carte NVIDIA ni aucun eGPU détecté.
- Client SSH installé ; serveur OpenSSH absent de l’installation visible.
- Sudo installé, mais son fonctionnement sur l’hôte reste non vérifié à cause du bac à sable.
- Espace disque disponible suffisant pour envisager la pile Docker/Ollama/Open WebUI.

## 1. Caractéristiques matérielles

| Élément | Relevé |
|---|---|
| Fabricant et modèle | Apple Inc., `Macmini8,1` |
| Processeur | Intel Core i7-8700B à 3,20 GHz |
| Cœurs / threads | 6 cœurs physiques, 12 threads, un socket |
| Fréquences exposées | 800 MHz à 4,6 GHz |
| Architecture | x86_64 ; AVX2 et virtualisation VT-x disponibles |
| Cache L3 | 12 Mio |
| Mémoire | 31 Gio visibles, cohérents avec 32 Go physiques |
| Mémoire au relevé | Environ 3,7 Gio utilisés, 27 Gio disponibles |
| Swap | Environ 23,5 Gio, inutilisée au relevé |
| GPU | Intel UHD Graphics 630 / CoffeeLake-H GT2, PCI `8086:3e9b`, pilote `i915` |
| SSD | Apple SSD AP0512M, 465,9 Gio environ, firmware `1306` |
| BIOS / iBridge | `2020.80.5.0.1 (iBridge: 21.16.3049.0.0,0)` |

Températures ponctuelles : CPU package 53 °C ; cœurs entre 41 et 53 °C ; SSD 34,85 °C ; PCH 50 °C. Pas d’alerte thermique évidente à cet instant. Aucun test sous charge, de ventilation ou de stabilité n’a été effectué. Santé SMART et endurance du SSD non vérifiées ; `smartctl` et l’outil `nvme` n’ont pas été trouvés dans le PATH.

Le relevé `lscpu` indique des mitigations des vulnérabilités processeur ; certaines lignes signalent une vulnérabilité résiduelle liée au SMT. Cela n’a pas fait l’objet d’une évaluation de sécurité dédiée.

## 2. Périphériques et pilotes

| Périphérique | Identifiant / modèle | État observé |
|---|---|---|
| Contrôleur SSD Apple | ANS2 NVMe, `106b:2005` | Pilote `nvme` actif |
| T2 Bridge | `106b:1801` | Détecté ; aucun pilote actif indiqué |
| T2 Secure Enclave | `106b:1802` | Détecté ; aucun pilote actif indiqué |
| Audio Apple T2 | `106b:1803` | Détecté ; aucun pilote actif indiqué |
| Audio Intel | Cannon Lake PCH cAVS, `8086:a348` | `snd_hda_intel` actif |
| Wi-Fi | Broadcom BCM4364, `14e4:4464` | Module possible `brcmfmac`, aucun pilote actif associé |
| Ethernet | Broadcom BCM57766, `14e4:1686` | Pilote `tg3` actif |
| Thunderbolt NHI | Deux Intel JHL7540, `8086:15eb` | Pilote `thunderbolt` actif |
| USB Thunderbolt | Deux Intel JHL7540, `8086:15ec` | Pilote `xhci_hcd` actif |
| Ponts PCIe Thunderbolt | DSL6540 Alpine Ridge et JHL7540 Titan Ridge | Pilote `pcieport` |
| USB principal | Intel Cannon Lake PCH xHCI | Pilote `xhci_hcd` |

Les modules `i915`, `nvme`, `tg3`, `thunderbolt`, `brcmfmac`, `hci_uart` et `bluetooth` sont chargés. Aucun module `apple-bce` ni pilote NVIDIA n’apparaît dans le relevé.

`/proc/asound/cards` expose une seule carte « HDA Intel PCH ». Cela ne confirme pas le fonctionnement des haut-parleurs internes ou de l’audio T2. La présence des modules Bluetooth ne suffit pas à valider le fonctionnement du Bluetooth.

L’inventaire USB direct échoue avec `unable to initialize libusb: -99`. L’arbre `lsusb -t` reste accessible et montre : un hub USB avec périphériques HID, plusieurs hubs racines USB 2/3, et un stockage USB utilisant `uas` sur une liaison annoncée à 10 000 Mbit/s. Cette valeur est la vitesse de liaison, pas un débit mesuré.

## 3. Stockage et partitionnement

| Disque / partition | Taille relevée | Type et usage |
|---|---:|---|
| `nvme0n1` | 465,9 Gio | SSD interne |
| `nvme0n1p1` | 976 Mio | Partition EFI, FAT32, `/boot/efi` |
| `nvme0n1p2` | 977 Mio | ext4, `/boot` |
| `nvme0n1p3` | 464 Gio | Membre LVM |
| `sda` | 465,8 Gio | Disque USB portant une image d’installation |
| `sda1` | 3,7 Gio | ISO9660 Debian 13.7, montée en lecture seule |
| `sda2` | 3,6 Mio | FAT12, partition de démarrage de l’image |

La racine utilise `/dev/mapper/JARVIS--MacMIini--vg-root`, en ext4. `fstab` référence également le volume de swap `/dev/mapper/JARVIS--MacMIini--vg-swap_1` ; `/proc/swaps` confirme une swap active sur `/dev/dm-1`, inutilisée au relevé.

| Montage | Taille du système de fichiers | Utilisé | Disponible |
|---|---:|---:|---:|
| `/` | 433 Gio | 9,1 Gio | 402 Gio |
| `/boot` | 944 Mio | 170 Mio | 709 Mio |
| `/boot/efi` | 974 Mio | 9,1 Mio | 965 Mio |

Aucune partition macOS/APFS n’apparaît dans l’inventaire des disques visibles. La topologie complète des volumes logiques et l’espace libre du groupe LVM n’ont pas été interrogés. Aucun volume LUKS n’apparaît dans le relevé, sans constituer une vérification exhaustive du chiffrement.

Les montages observés comportent les restrictions du bac à sable (`ro`, `nosuid`, `nodev`, propriétaires remappés). Ils ne permettent pas de conclure que le système de fichiers racine de l’hôte est en lecture seule à cause d’une panne. `fstab` contient pour la racine l’option habituelle `errors=remount-ro`.

## 4. Système, noyau et démarrage EFI/GRUB

- Distribution : Debian GNU/Linux 13, trixie ; version complète `13.7`.
- Noyau actif : `6.12.111+deb13-amd64`, paquet `6.12.111-1`, compilation du 28 septembre 2026, `PREEMPT_DYNAMIC`.
- Noyau précédent présent : `6.12.107+deb13-amd64`, paquet `6.12.107-1`.
- Métapaquet installé : `linux-image-amd64`, version `6.12.111-1`.
- Ligne de démarrage : `BOOT_IMAGE=/vmlinuz-6.12.111+deb13-amd64 root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet`.

Le démarrage EFI est confirmé. `efibootmgr -v` rapporte :

- Entrée courante `0000` : `debian`, via `\EFI\debian\shimx64.efi` sur la partition EFI.
- Ordre de démarrage : `0000,0080`.
- Anciennes entrées Apple : `0080` Mac OS X, `0081` programme de mise à jour Apple et `FFFF` chemin Apple. Leur présence ne prouve pas que les systèmes ou partitions correspondants existent encore.

`mokutil --sb-state` rapporte **SecureBoot disabled**. La variable EFI lue confirme cette valeur. Le réglage de sécurité du démarrage propre à la puce T2 dans la récupération Apple n’a pas été vérifié.

Paramètres accessibles dans `/etc/default/grub` : `GRUB_DEFAULT=0`, `GRUB_TIMEOUT=5`, `GRUB_CMDLINE_LINUX_DEFAULT="quiet"`, `GRUB_CMDLINE_LINUX=""`.

Deux images de noyau et leurs initramfs sont présentes dans `/boot`. Le fichier généré `/boot/grub/grub.cfg` et le contenu de l’ESP sont inaccessibles ; les entrées GRUB exactes et les fichiers EFI n’ont donc pas pu être contrôlés.

Le noyau courant est un noyau Debian standard. L’absence de module `apple-bce` chargé et de pilotes actifs pour plusieurs fonctions T2 indique un support incomplet. Aucun changement des paramètres de démarrage n’a été effectué.

## 5. Réseau

- Interface Ethernet physique visible : `enp4s0`.
- État sysfs : `up`, porteuse `1`, vitesse négociée `1000` Mbit/s.
- Carte Broadcom BCM57766 avec pilote `tg3`.
- Interfaces sysfs visibles : Ethernet et boucle locale ; aucune interface Wi-Fi.
- Résolution configurée par NetworkManager : domaine de recherche `lan`, DNS IPv4 `192.168.1.254`, DNS IPv6 `2001:861:3895:b000:56c4:5bff:fed7:e52c`.

Les commandes `ip` et `ss` échouent à ouvrir leurs sockets netlink avec `Operation not permitted`. Le bus système est inaccessible. Les tables `/proc/net` visibles ne montrent que le réseau isolé du bac à sable.

**Non vérifiés :** IP de l’hôte, routes, passerelle, attribution DHCP, connectivité Internet de l’hôte, résolution DNS effective, ports en écoute, exposition IPv6 et règles du pare-feu. Les tables vides du bac à sable ne prouvent pas l’absence de réseau ou de services sur JARVIS.

## 6. Firmwares et fonctions manquantes

Paquets confirmés installés :

| Paquet | Version |
|---|---|
| `firmware-brcm80211` | `20250410-2` |
| `firmware-intel-graphics` | `20250410-2` |
| `firmware-misc-nonfree` | `20250410-2` |
| `firmware-sof-signed` | `2025.01-1` |
| `intel-microcode` | `3.20251111.1~deb13u1` |

Les sources APT visibles utilisent `trixie`, `trixie-security` et `trixie-updates`, avec les composants `main non-free-firmware`. Aucun dépôt T2Linux ou Docker n’a été identifié dans les lignes de sources relevées.

La carte BCM4364 est détectée mais sans pilote actif associé. `brcmfmac` est chargé ; aucune interface Wi-Fi n’est exposée. Une inspection du répertoire `/usr/lib/firmware/brcm` ne trouve aucun fichier contenant `4364`.

**Diagnostic probable : firmwares Apple adaptés à la BCM4364 manquants.** Les journaux noyau ne sont pas accessibles, ce qui empêche de préciser les fichiers effectivement demandés et d’exclure une autre cause. Les autres firmwares manquants ne peuvent pas être inventoriés exhaustivement.

`journalctl -b -k` ne présente aucune entrée accessible et signale des droits insuffisants. `dmesg` est interdit. Ce résultat ne signifie pas que les journaux système sont vides ou qu’aucune erreur noyau ne s’est produite.

T2Linux recommande le pilote noyau `brcmfmac` et propose l’extraction des firmwares depuis macOS ou une image de récupération Apple. Aucun script d’extraction n’a été exécuté.

Source : [Guide T2Linux Wi-Fi et Bluetooth](https://wiki.t2linux.org/guides/wifi-bluetooth/).

## 7. Thunderbolt

Deux contrôleurs Intel JHL7540 Titan Ridge Thunderbolt 3 NHI sont détectés : `07:00.0` et `7d:00.0`. Le pilote `thunderbolt` est actif.

Dans `/sys/bus/thunderbolt/devices`, les domaines `domain0` et `domain1` et les routeurs hôtes `0-0` et `1-0` sont visibles. Les deux routeurs hôtes portent le nom « Macintosh », affichent la génération `3` et `authorized=1`. Les deux domaines ont le niveau de sécurité `user`.

Aucun périphérique Thunderbolt externe ni eGPU n’est énuméré. `boltctl` est installé, mais les opérations via le bus système n’ont pas pu être vérifiées.

La reconnaissance des contrôleurs ne valide pas chacune des quatre prises physiques. Recommandation : tester chaque prise avec un périphérique et un câble Thunderbolt connus, relever son apparition, son autorisation et sa liaison PCIe. Ne pas désactiver globalement la sécurité Thunderbolt pour contourner un problème d’autorisation.

## 8. Sudo et SSH

### Sudo

Paquet installé : `sudo 1.9.16p2-3+deb13u2`. Le test non interactif `sudo -n -l` échoue avec deux messages : propriétaire de `/etc/sudo.conf` présenté comme UID 65534 et drapeau « no new privileges » actif.

`/proc/self/status` confirme `NoNewPrivs: 1`. Les UID sont remappés dans cette session. Ces observations ne permettent pas de conclure à une mauvaise propriété réelle de `/etc/sudo.conf` ou à une panne de sudo sur l’hôte. Aucune correction de droits, de groupes ou de sudoers n’est justifiée à partir de ce résultat.

Le fonctionnement de sudo et les droits réels d’`adminjarvis` doivent être vérifiés depuis un terminal hôte avec `sudo -l` et une commande de lecture telle que `sudo id`, sans éditer la configuration.

### SSH

- Client installé : paquet `openssh-client 1:10.0p1-7+deb13u4`.
- `ssh -V` fonctionne et affiche `OpenSSH_10.0p2 Debian-7+deb13u4`, OpenSSL `3.5.7` ; la différence avec la version du paquet est conservée telle qu’observée.
- `openssh-server` n’est pas installé dans la base de paquets visible.
- `/usr/sbin/sshd`, `/usr/lib/systemd/system/ssh.service` et `/etc/ssh/sshd_config` sont absents.
- L’état systemd n’est pas accessible depuis le bac à sable.

Aucune connexion SSH authentifiée ni accessibilité depuis une autre machine n’a été testée. L’absence du serveur OpenSSH indique que l’installation visible ne fournit pas de serveur SSH standard ; les ports de l’hôte n’ont pas pu être inspectés pour exclure un autre serveur.

## 9. Problèmes et limites à traiter

| Priorité | Constat | Suite recommandée |
|---|---|---|
| Haute avant intervention distante | Sudo hôte non validé et serveur OpenSSH absent | Vérifier sudo localement ; prévoir l’accès local et, si demandé, l’installation/configuration SSH dans une mission autorisée |
| Haute avant changement du noyau | Contenu EFI et GRUB généré non vérifié | Contrôler et sauvegarder le démarrage ; conserver un noyau Debian de secours |
| Moyenne | Support T2 incomplet | Préparer un noyau T2Linux compatible avec Debian 13 |
| Moyenne | Wi-Fi BCM4364 non opérationnel dans le relevé | Lire les journaux hôte puis installer les firmwares Apple adaptés |
| Conditionnelle | Aucun GPU NVIDIA visible | Identifier et tester un éventuel eGPU avant de choisir les pilotes |
| À compléter | Ports physiques Thunderbolt non testés | Essai par prise avec matériel connu |
| À compléter | Réseau, pare-feu, SMART et journaux non accessibles | Terminer les contrôles depuis l’hôte |

## 10. Plan d’installation proposé — non exécuté

Toute installation, modification de configuration ou tout redémarrage nécessite l’accord explicite de l’utilisateur. Les versions exactes seront vérifiées au moment de l’intervention.

### Étape 1 — Compléter l’audit sur l’hôte

Contrôler sudo, journaux noyau, adresses et routes, ports en écoute et pare-feu. Vérifier la topologie LVM, la santé du SSD, l’ESP et les entrées GRUB. Relever les noms exacts des firmwares réclamés par `brcmfmac`. Tester les prises Thunderbolt si le matériel de test est disponible.

### Étape 2 — Préparer le retour arrière

Après autorisation, sauvegarder les données et les fichiers de démarrage pertinents, conserver les noyaux Debian existants et disposer d’un support de secours ainsi que d’un accès local. Vérifier l’espace nécessaire dans `/boot` avant d’ajouter le noyau T2 et son initramfs. Aucun repartitionnement n’est proposé sur la base de cet audit.

### Étape 3 — Noyau T2Linux et firmwares Apple

Le guide T2Linux pour Debian oriente vers le dépôt communautaire `t2-ubuntu-repo` et le paquet `linux-t2`. Vérifier sa provenance, la clé de signature, la compatibilité trixie et les dépendances proposées avant installation. Prévoir les en-têtes correspondant exactement au noyau retenu pour les modules DKMS.

Installer les firmwares Apple requis et, selon les besoins, la configuration audio T2. Touch ID et Touch Bar ne concernent pas ce Mac mini. Examiner les paramètres recommandés par le guide : `intel_iommu=on iommu=pt pm_async=off`, puis préparer initramfs et GRUB en conservant un démarrage Debian de secours.

Un redémarrage avec accord explicite sera nécessaire pour valider le nouveau noyau. Critères : stockage et Ethernet opérationnels, accès administratif conservé, pilotes T2 chargés, Wi-Fi et audio contrôlés, Thunderbolt testé et journaux examinés. En cas de régression, revenir au noyau Debian conservé.

Sources : [Installation T2Linux pour Debian](https://wiki.t2linux.org/distributions/debian/installation/), [dépôt APT recommandé](https://github.com/AdityaGarg8/t2-ubuntu-repo), [sources du noyau T2 Debian/Ubuntu](https://github.com/t2linux/T2-Debian-and-Ubuntu-Kernel), [firmwares Wi-Fi/Bluetooth](https://wiki.t2linux.org/guides/wifi-bluetooth/).

### Étape 4 — NVIDIA, uniquement si un eGPU est présent

Aucune carte NVIDIA n’est actuellement visible. Identifier le boîtier, le câble et le modèle du GPU ; vérifier l’autorisation Thunderbolt et l’apparition PCIe avant de choisir la branche de pilote.

Choisir les paquets et la variante de module compatibles avec le GPU et Debian 13, puis vérifier la compilation DKMS avec les en-têtes du noyau T2. Ne pas mélanger plusieurs méthodes d’installation du pilote. Valider `nvidia-smi` et un calcul GPU après chargement du pilote. Tout redémarrage nécessaire fera l’objet d’un accord explicite.

La documentation Ollama consultée indique une capacité de calcul NVIDIA 5.0 minimum et des exigences de version du pilote dépendant de la génération : 550 minimum, ou 570 minimum pour les capacités 5.0 à 6.2. Ces exigences devront être revalidées pour la version d’Ollama choisie.

Pour l’accès GPU depuis Docker, prévoir NVIDIA Container Toolkit et la configuration du runtime Docker, puis un test de visibilité GPU dans un conteneur. Cette configuration et l’éventuel redémarrage de Docker seront soumis à autorisation.

Sources : [Pilotes NVIDIA pour Debian](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/debian.html), [matériel pris en charge par Ollama](https://docs.ollama.com/gpu), [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

### Étape 5 — Docker Engine et Compose

Installer Docker Engine depuis le dépôt officiel compatible Debian 13, avec clé dédiée et paquets Docker Engine, CLI, containerd, Buildx et Compose. Vérifier les éventuels conflits de paquets avant installation. Docker Desktop n’est pas nécessaire au projet serveur.

Valider le service, un conteneur de test, la persistance et les règles réseau effectives. Définir explicitement qui peut administrer Docker, l’accès au démon donnant des privilèges élevés. Contrôler les publications de ports IPv4 et IPv6.

Source : [Installation officielle Docker sur Debian](https://docs.docker.com/engine/install/debian/).

### Étape 6 — Ollama

Déployer Ollama en conteneur avec une version figée et un volume persistant pour les modèles. Démarrer sur CPU tant qu’aucun GPU compatible n’a été validé ; activer l’accès NVIDIA seulement après les tests du pilote et du runtime.

Proposition initiale : modèle quantifié de 3 à 8 milliards de paramètres, puis mesure du débit, de la latence et de la mémoire selon la longueur de contexte. Ce dimensionnement est une recommandation, pas une performance mesurée sur JARVIS. Conserver une marge mémoire pour le système et les autres services.

Placer Ollama sur un réseau Docker privé partagé avec Open WebUI, sans publication initiale du port 11434 sur le réseau local. Valider le chargement d’un modèle, la génération et la persistance après redémarrage du conteneur.

Source : [Ollama dans Docker, CPU et GPU](https://docs.ollama.com/docker).

### Étape 7 — Open WebUI

Déployer une version figée d’Open WebUI avec volume persistant et connexion à Ollama via le réseau Docker privé. Prévoir une clé secrète persistante et la création du compte administrateur.

Publier initialement l’interface sur `127.0.0.1:3000`. Définir ensuite l’accès distant souhaité : tunnel SSH lorsque SSH sera disponible, ou publication LAN/HTTPS après validation de la politique d’accès. Vérifier authentification, connexion au modèle, persistance et sauvegarde des volumes.

Source : [Démarrage officiel Open WebUI](https://docs.openwebui.com/getting-started/quick-start/).

## Conclusion

JARVIS dispose d’une base matérielle adaptée à une première installation Ollama sur CPU, avec mémoire et stockage disponibles. Le support Wi-Fi/T2 demande une intervention préparée et un retour arrière de démarrage. L’accélération NVIDIA dépend d’un eGPU qui n’est pas actuellement détecté.

L’audit ne valide pas encore sudo sur l’hôte, les services réseau, le pare-feu, la santé SMART ou chacune des prises Thunderbolt. Ces contrôles restent nécessaires avant de déclarer la machine entièrement prête. Aucun changement système n’a été exécuté.

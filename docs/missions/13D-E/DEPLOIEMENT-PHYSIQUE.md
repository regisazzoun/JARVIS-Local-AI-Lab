# Reprise physique 13D-E — procédure contrôlée, 15 octobre 2026

La priorité est désormais le Dell. Un laboratoire virtuel complet et 14A ne sont pas des prérequis de cette préparation. Aucun démarrage réseau réel, installation Dell, accès SSH Dell ou partitionnement n'a été effectué. Les fichiers `candidate` ne constituent pas une recette réceptionnée.

## Réseau Bbox et services

La Bbox reste l'unique serveur DHCP attribuant les adresses, la passerelle et le DNS. Le Mac mini répond uniquement aux requêtes PXE du MAC Dell validé, sur l'Ethernet et le sous-réseau validés. L'interface et les adresses observées sont consignées dans `deployment/13de/private/network-observed.json` local, exclu de Git. Adresse JARVIS observée dynamique : vérifier sa stabilité avant séance ; ne pas modifier la Bbox dans cette mission.

Flux prévus : DHCP Bbox UDP 67/68 ; ProxyDHCP UDP 67/4011 ; TFTP UDP 69 et ports de transfert ; HTTP TCP 8088 ; après installation SSH TCP 22 vers Dell. Le port DNS 53 n'est pas ouvert par cette configuration (`port=0`). Pas de plage d'allocation, DHCP autoritaire, RA, DHCPv6 ou option routeur. Aucune modification de pare-feu/routage. L'audit local n'a pas trouvé d'écoute 67/69/4011/8088 ; cela ne prouve pas leur traversée par le pare-feu ni l'absence d'un serveur distant.

Les templates sont dans `deployment/13de/pxe/templates/`. Remplacer chaque `@...@` dans une copie privée, à partir du plan validé : interface Ethernet, IP JARVIS, réseau, masque, MAC Dell, répertoires absolus. `proxy.conf` ignore tous les clients sans tag Dell et sélectionne les architectures UEFI x86-64 7/9 ; le tag iPXE évite de recharger le même binaire. Qualifier le comportement réel du firmware (notamment les échanges 4011) pendant une fenêtre contrôlée. Les autres clients doivent continuer à obtenir une adresse de la Bbox sans proposition de boot JARVIS.

Préparation sans activation :

```sh
# Depuis la racine du checkout ; nouveau répertoire uniquement.
./deployment/13de/pxe/fetch-debian.sh "$PWD/deployment/13de/private/debian-session"
# Copier les fichiers linux/initrd.gz vérifiés dans le HTTP_ROOT dédié.
# Copier /usr/lib/ipxe/snponly.efi dans le TFTP_ROOT, lisible par dnsmasq.
# Conserver Release, Release.gpg, SHA256SUMS et empreintes dans les preuves privées.
/usr/sbin/dnsmasq --test --conf-file=/CHEMIN/PRIVE/proxy.conf
# Aucun @...@ ne doit rester dans les copies rendues.
```

La signature du Release Debian authentifie SHA256SUMS puis linux/initrd.gz. Les binaires iPXE et OVMF proviennent des paquets Debian déjà installés. Ne pas remplacer silencieusement ces binaires par un téléchargement non vérifié. Le serveur HTTP ne sert qu'un répertoire dédié, jamais le dépôt, les journaux, les identités ou les clés. Les unités fournies sont des candidats sans installation ni activation effectuée.

**Validation réseau requise avant lancement :** faire approuver la copie exacte de `proxy.conf`, l'interface/IP/masque, le MAC Dell, les flux et les effets possibles sur les autres clients. Puis seulement, dans deux terminaux supervisés :

```sh
# CES COMMANDES ACTIVENT DES SERVICES LAN : validation humaine préalable.
python3 -m http.server 8088 --bind IP_JARVIS_VALIDEE --directory /HTTP_ROOT_DEDIE
sudo /usr/sbin/dnsmasq --keep-in-foreground --conf-file=/CHEMIN/PRIVE/proxy.conf
```

Arrêter ces processus par Ctrl-C à la fin de la séance ; pas d'activation persistante automatique. Capturer uniquement les échanges du MAC Dell si un diagnostic est nécessaire, en gardant les captures privées. Si un autre client reçoit une offre d'adresse du Mac mini ou une proposition de boot inattendue : arrêter immédiatement dnsmasq et conserver les traces. Ne pas toucher à la Bbox pour masquer le problème.

**Repli :** démarrer un support USB iPXE UEFI préparé sur une clé explicitement identifiée et autorisée à l'effacement, ou charger `snponly.efi` depuis une partition FAT existante dédiée sans écraser les autres fichiers. L'ISO iPXE installé est disponible, mais sa compatibilité USB/UEFI doit être vérifiée ; ne pas supposer qu'un simple `dd` suffit. Dans le shell iPXE : `dhcp`, puis `chain http://IP_JARVIS_VALIDEE:8088/discovery.ipxe`. Le DHCP reste celui de la Bbox ; ProxyDHCP peut être arrêté. Secure Boot et signatures iPXE doivent être inspectés sur le Dell ; toute modification UEFI demande accord séparé.

## Découverte matérielle et décision RAID

Démarrer un Debian live UEFI en mode découverte, sans lancer l'installation. Après accord pour ce démarrage, collecter localement :

```sh
sudo python3 deployment/13de/physical/discover.py > dell-discovery.json
sudo dmidecode -t system
lscpu
lspci -nnk
sudo nvme list -o json
lsblk -b -o PATH,MODEL,SERIAL,SIZE,TYPE,FSTYPE,MOUNTPOINTS
cat /proc/mdstat
sudo mdadm --examine --scan
```

Ces commandes lisent les informations ; garder UUID, séries et MAC privés. Ne pas monter automatiquement des partitions inconnues. Confirmer CPU, mémoire, GPU réellement présents, contrôleur, mode VMD/VROC actuel, référence et capacité exacte de chaque NVMe. La désignation commerciale annoncée ne remplace pas la découverte. Si le DMI diffère du nom strict attendu, arrêter et faire réviser le profil après inspection ; ne pas assouplir le contrôle globalement.

VROC est une option conditionnelle : support précis du chipset/CPU/BIOS et des SSD, licence éventuelle, visibilité et démarrage Linux du volume, récupération depuis un seul disque à démontrer. Rien de cela n'est présumé acquis. Ne pas changer de mode contrôleur sur des données existantes.

**Choix préparatoire recommandé : mdadm RAID1**, si les deux NVMe sont exposés indépendamment et le démarrage UEFI est compatible. GPT sur chaque disque ; une ESP FAT32 indépendante de 1 Gio sur chacun ; partitions restantes membres d'un RAID1, métadonnées mdadm 1.2, système ext4 sur le miroir. Les ESP ne sont pas dans mdadm. Pas de chiffrement ou de swap partitionné ajouté implicitement ; dimensionner éventuellement un fichier swap après installation.

La recette partman `preseed-dell.candidate.cfg` est préparée mais non qualifiée : vérifier les deux ESP, la sélection des partitions membres, les tailles et le chargeur avant de la promouvoir. Les confirmations destructrices automatiques sont volontairement absentes. Le prérequis restant est une validation ciblée de cette recette, sur deux disques jetables ou pendant une séance physique explicitement autorisée, pas la reconstruction d'un laboratoire complet.

Après installation autorisée : vérifier `/proc/mdstat`, `mdadm --detail /dev/md0`, les UUID et `findmnt`; conserver `mdadm.conf` dans l'initramfs Dell. Installer le chargeur Debian sur ESP1 et ESP2, créer/vérifier les entrées UEFI et la voie de secours `EFI/BOOT/BOOTX64.EFI` sur chacune selon Secure Boot. Ne pas copier des fichiers EFI d'une version différente. Tester un démarrage complet avec chacun des NVMe seul, machine arrêtée avant déconnexion et seulement après accord physique. Conserver console locale et média de secours.

Panne d'un disque : relever le membre manquant, l'état dégradé et le disque survivant ; démarrer sur son ESP. Faire approuver l'identité du remplaçant avant toute table GPT/formatage ; ne jamais inverser source et destination. Recréer ESP et partition membre compatibles, ajouter le membre au bon md, attendre la resynchronisation, réinstaller le chargeur et refaire les deux essais. Aucune commande générique d'effacement ou de clonage de table n'est exécutée par cette préparation.

## Bootstrap et frontières d'autorisation

1. Faire approuver le manifeste exact à partir de la découverte et la liste des données effacées. Copier `approved.example.json` dans `private/approved.json`, renseigner UUID, chemins, modèles, séries et tailles en octets. Débrancher les disques supplémentaires avant installation ; une clé USB de découverte doit être retirée après chargement si elle apparaît comme disque.
2. Sur le Dell live : `sudo python3 deployment/13de/physical/validate.py /CHEMIN/approved.json`. Un résultat positif valide seulement l'identité, aucune écriture. Toute différence arrête la procédure.
3. Choisir une **clé publique existante autorisée**, dont JARVIS contrôle le signataire ; vérifier son empreinte avec l'administrateur. Ne pas lire/copier une clé privée dans les assets. Aucun compte ni clé hôte modifié.
4. Construire le candidat avec `python3 deployment/13de/physical/build-initrd.py MANIFEST CLE_PUBLIQUE ASSETS_VERIFIES SORTIE_NOUVELLE.gz`. Le builder vérifie les sources et incorpore preseed, clé, manifeste TSV et garde shell dans l'initrd. Il n'incorpore **jamais** `approved-erase.sha256` : le candidat s'arrête avant partman. Un essai avec identités synthétiques ne doit pas être utilisé sur le matériel.
5. Avant toute version installable, qualifier la recette RAID et faire approuver explicitement l'effacement des deux séries. L'artefact d'autorisation attendu est le SHA256 exact de `/approved.tsv`, placé à la racine de l'initrd sous `approved-erase.sha256` dans une nouvelle construction privée revue. Ce mécanisme n'est pas une authentification cryptographique d'un humain : l'approbation humaine est externe, liée aux empreintes du manifeste, du preseed et de l'initrd final. Aucun outil de cette mission ne crée cet artefact.
6. Faire approuver séparément le lancement de l'installation physique ; ne pas confondre l'approbation réseau avec l'effacement. Conserver le console/journal d'installation et les rapports de partitionnement dans un dossier privé. La garde est répétée avant l'injection SSH ; le script refuse Apple, UUID erroné, disques inattendus, mode BIOS et autorisation absente. Le preseed bloque indéfiniment avant partman après un refus, pour empêcher une poursuite automatique.

TFTP/HTTP ne garantissent pas l'intégrité du transport contre un acteur malveillant du LAN. Servir le candidat uniquement pendant une fenêtre contrôlée ; si le LAN n'est pas de confiance, transporter l'initrd vérifié sur le média local et vérifier son empreinte sur la console. Ne jamais charger le manifeste ou l'autorisation par HTTP non authentifié. Les paquets Debian restent vérifiés par APT.

## Premier SSH puis Ansible

`install-ssh.sh` réutilisé configure uniquement la cible installateur : jarvisadmin, clé publique embarquée, SSH activé, compte sans mot de passe utilisable et sudo NOPASSWD pour le bootstrap. Ce sudo est un privilège administrateur complet, à approuver comme tel et à retirer ou réduire après définition d'une méthode become durable. Aucun changement au SSH du Mac mini.

Après premier boot Dell, relever les empreintes SSH **à sa console** avec `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`. Comparer à la connexion depuis JARVIS ; `ssh-keyscan` seul ne valide pas l'identité. Utiliser un fichier known_hosts dédié et un inventaire privé. Vérifier `id`, `sudo -n true`, Debian 13, `test -d /sys/firmware/efi`, réseau, RAID, journaux et redondance de boot avant les rôles.

```sh
ssh -o UserKnownHostsFile=/CHEMIN/PRIVE/known_hosts -o StrictHostKeyChecking=yes jarvisadmin@IP_DELL_VALIDEE
cd deployment/13de/ansible
ansible-playbook --syntax-check site.yml
ansible-playbook -i inventory/dell.yml --syntax-check dell.yml
# Après installation, réception stockage et autorisation de configuration :
ansible-playbook -i /INVENTAIRE_PRIVE dell.yml --check --diff
ansible-playbook -i /INVENTAIRE_PRIVE dell.yml
ansible-playbook -i /INVENTAIRE_PRIVE dell.yml
```

L'inventaire privé doit fournir `deployment_scope: dell-approved`, `dell_configuration_authorized: true`, `approved_uuid`, `approved_addresses` (liste exacte d'IP Dell), `storage_acceptance_complete: true`, le fichier known_hosts et le compte. `dell.yml` refuse l'inventaire livré avant tout contact distant ; les rôles ne commencent qu'après contrôle DMI/OS. Ne jamais inclure l'IP Mac mini. Le deuxième passage doit présenter zéro modification ; cette idempotence n'est pas encore prouvée faute de cible installée.

NVIDIA/CUDA/Ollama restent différés dans les rôles existants et exclus du playbook physique livré. Leur installation n'est pas validée par le syntax-check. Après réception Debian et nouvelle autorisation : vérifier les deux GPU, alimentation/refroidissement, Secure Boot et versions de pilotes compatibles ; sélectionner une provenance/version figée, tester DKMS puis `nvidia-smi`, CUDA et chaque GPU ; installer Ollama depuis une source authentifiée, faire une inférence témoin et contrôler mémoire/températures. Aucun modèle hôte n'est déplacé. Réserve explicite : les rôles IA exécutables restent à compléter à partir des versions choisies et du matériel constaté.

Intégration JARVIS : définir une adresse Dell stable, un accès de service limité et authentifié, puis un endpoint d'inférence de test. Ollama écoute localement par défaut ; pas d'exposition LAN implicite. Vérifier timeout, indisponibilité Dell et retour au moteur local. Ne pas partager la SQLite active par un système de fichiers réseau : conserver JARVIS comme propriétaire de la mémoire et passer par son API. Le rôle `jarvis` actuel crée seulement un répertoire ; aucun worker ni raccordement agent n'est réceptionné.

## Reprise et retour sûr

Échec PXE : arrêter le ProxyDHCP, conserver le DHCP Bbox, essayer iPXE USB avec la même image vérifiée. Échec avant effacement : arrêter, corriger le profil à partir de la découverte, nouvelle validation. Échec après effacement autorisé : conserver logs `/var/log/installer`, état md/GPT/EFI et ne pas réinitialiser le miroir sain ; média Debian rescue UEFI, assemblage md et réparation depuis console après diagnostic. Perte SSH : utiliser la console Dell, vérifier DHCP/SSH/clé et empreinte ; aucune réparation des accès Mac mini n'est justifiée. Arrêter les seuls services temporaires créés pendant la séance, sans redémarrer JARVIS.

## Références officielles consultées

- [Debian Installer trixie : preseed, comptes et RAID](https://www.debian.org/releases/trixie/amd64/apbs04.en.html).
- [Index officiel des images Debian amd64](https://deb.debian.org/debian/dists/trixie/main/installer-amd64/current/images/).
- [Manuel dnsmasq : ProxyDHCP, tags et services PXE](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html).

Ces références guident les candidats ; elles ne remplacent pas la recette matérielle.


## Reprise bootstrap A/B — 16 octobre 2026

Le premier PXE UEFI physique a désormais atteint Debian Installer. Ne pas refaire sa conception/validation. Pour la prochaine séance, suivre [BOOTSTRAP-AUTOMATISE.md](BOOTSTRAP-AUTOMATISE.md) : découverte automatique embarquée et bloquante, réception du manifeste, puis autorisations distinctes. L'ancien preseed et install-ssh.sh restent historiques ; le nouveau candidat bootstrap ne devient installable qu'après approbation liée aux séries réelles et qualification RAID/ESP. Aucun compte temporaire n'est révoqué avant preuve indépendante de l'accès permanent.

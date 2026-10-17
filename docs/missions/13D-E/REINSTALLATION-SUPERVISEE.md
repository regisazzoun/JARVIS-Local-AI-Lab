# Mission continue 13D-E / 14 — nouvelle tentative, 17 octobre 2026

La mission complète a été relancée par le propriétaire : installation Debian neuve, conservation prioritaire du RAID/GPT/ESP, comptes jarvis-bootstrap et adminjarvis avec le même mot de passe utilisateur privé, maintien SSH par mot de passe et clé, clavier français, puis Ansible/NVIDIA/CUDA/Ollama/modèles/intégration/réception. Les anciennes clôtures, reports IA et révocations automatiques ne régissent plus cette tentative. Aucun résultat physique nouveau n'est déclaré réussi à ce stade.

## Chaîne préparée et exécutants

`deployment/13de/reinstall/` contient le constructeur d'overlay du netboot existant, le démarrage SSH en RAM, l'installation de la racine sur miroir préexistant, le contrôleur PXE/SSH, le suivi, le playbook serveur IA, les tests d'intégration avec restauration des paramètres précédents en cas d'échec et la publication des seuls résultats expurgés. Les scripts de poursuite attendent la preuve d'accès indépendant par mot de passe/clé/sudo avant la phase IA. Les comptes de secours ne sont pas révoqués automatiquement.

La reconstruction de l'overlay est nécessaire pour ajouter la supervision SSH, le clavier français effectif et la réutilisation du RAID, que l'ancienne recette partman recréait. Le noyau Debian authentifié existant est conservé. Le démarrage supervisé ne retourne jamais au partitionneur et n'écrit aucun disque ; le contrôleur vérifie ensuite l'identité avant de lancer le script d'installation. Celui-ci exige un miroir RAID1 sain, deux membres exacts et deux ESP FAT/GPT ; il n'appelle ni mdadm --create, ni wipefs, ni un outil de repartitionnement. Le formatage ext4 vise uniquement le volume RAID racine contrôlé.

Une clé hôte de supervision et une clé hôte du système cible sont préparées dans le stockage privé et épinglées localement. Le SSH en mémoire utilise le port 2222 et une clé, limité à JARVIS. Le système installé utilise adminjarvis et jarvis-bootstrap, avec mot de passe utilisateur et clé publique. Le rapport de premier boot n'est plus l'unique voie de reprise.

## Vérifications préparatoires réellement effectuées

- Signature Release Debian, empreintes du noyau/initrd et des udebs ajoutés vérifiées ; secrets et identifiants restent privés.
- Test ciblé sans disque : chargement NVMe/RAID1/ext4, debootstrap disponible, sshd démarré. Carte française chargée et relue : keycode16=a, keycode17=z.
- Test ciblé en RAM sur réseau QEMU utilisateur avec redirection localhost : authentification SSH indépendante par clé, vérification stricte de la clé hôte et `uid=0` obtenus. Aucun disque ni installation complète VM.
- Syntaxe Python/shell et playbook Ansible vérifiée. Ces vérifications ne remplacent pas la réception physique à venir.
- ProxyDHCP/TFTP et HTTP actifs dans le périmètre Dell, ressources de boot HTTP vérifiées. Bbox demeure serveur DHCP d'allocation. Mail envoyé au propriétaire pour F12 → UEFI IPv4.

## IA et intégration à valider sur le Dell

Réutilisation de l'Ollama 0.40.3 et des modèles présents sur le Mac, sans modifier les sources : qwen3.5:27b-q4_K_M, ministral-3:14b-instruct-2512-q4_K_M et llama3.1:8b. Une seule RTX 3090 utilisable est exigée, l'UUID effectif est fixé dans CUDA_VISIBLE_DEVICES. Pilote et toolkit proviennent des paquets Debian compatibles ; nvidia-smi, VRAM Ollama et inférences réelles doivent valider l'accélération. Un échec de chargement du pilote reste un échec, jamais un succès supposé.

Whisper Small/Piper Tom, outils et mémoire SQLite restent sur le Mac mini. L'intégration change uniquement le backend d'inférence de la passerelle existante et d'Open WebUI, avec sauvegarde de configuration, sauvegarde SQLite en ligne et restauration des paramètres précédents si les tests échouent. Les tests doivent inclure authentification, réponse modèle, souvenir fictif temporaire dans la mémoire canonique, appel réel d'un outil autorisé, chaîne vocale sur WAV synthétique et requête Open WebUI. Aucune extension silencieuse des droits agentiques.

## Supervision et reprise

Vue locale : `python3 deployment/13de/reinstall/progress.py deployment/13de/private/reinstall-02/progress.json` (répéter avec watch si souhaité). Barres globale/par tâche, états, durée et dernière activité ; aucune coche sans validation réelle. Les phases sans mesure continue restent explicitement indéterminées. Le relais affiche cette vue sur tty1 de l'installateur et la conserve dans `/run/jarvis/progress.txt`, lisible depuis les consoles et SSH. Logs détaillés et transferts modèles restent privés.

Sur échec, consulter les fichiers privés controller.log, installer-tail.log, ai-phase.log et les marqueurs d'erreur. Ne pas relancer aveuglément le script de formatage : le marqueur RAM empêche un second lancement pendant la même session. Après reboot, l'existence de preuves privées doit guider la reprise ; ne pas repartir en PXE destructif pour un simple échec d'intégration.

La réception finale reste à établir : démarrage physique, stockage préservé, authentifications, Ansible idempotent, pilote/CUDA/inférence, intégration et redémarrage final. La publication automatique résume les seules étapes réellement validées, sur la branche existante, sans fusion.

Sources techniques : [preseed Debian trixie](https://www.debian.org/releases/trixie/amd64/apbs04.en.html), [pilotes NVIDIA pour Debian](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/debian.html), [installation Linux Ollama](https://docs.ollama.com/linux). Versions effectivement observées et preuves locales priment sur une supposition de compatibilité.


## Correctif après arrêt « JARVIS STOP : identité »

Le premier démarrage de cette tentative s'est arrêté avant l'activation réseau et avant toute écriture disque. Erreur de préparation identifiée : le constructeur prenait inventory.observed.json, inventaire brut comprenant le lecteur SD sans média comme troisième disque, au lieu du manifest.install-target.json déjà qualifié avec deux NVMe et une exception précise pour ce lecteur. Le contrôle restait actif et cette entrée rendait le manifeste incompatible avec lui.

La référence a été corrigée dans le constructeur, le contrôleur et la phase IA. Le constructeur applique désormais une validation de cohérence hors ligne entre les identités du manifeste et l'inventaire historique ; cette vérification de construction ne constitue pas une nouvelle mesure UEFI, qui reste impérativement vérifiée sur la machine par le guard. Les cas inventaire brut utilisé comme plan, média inséré et UUID différent sont rejetés. L'image servie a été reconstruite et son empreinte HTTP comparée au fichier local. Le clavier français précède désormais le contrôle, et le motif précis de refus est affiché en console. Aucune vérification d'identité n'a été supprimée. Un nouveau boot PXE est nécessaire puisque le premier s'est arrêté sans réseau ni SSH.


## Reprise distante après défauts d'outillage de l'installateur

PXE, identité physique et authentification SSH indépendante ont été validés. L'installation s'est arrêtée avant formatage sur tee absent ; l'outil a été ajouté en RAM via le paquet Debian busybox-static, sans nouveau PXE. Le miroir préexistant a ensuite été assemblé sain [UU], la seule racine reformatée et Debian de base installé. Un deuxième arrêt a révélé l'absence des modules FAT de l'environnement netboot : udebs du noyau exact vérifiés, pilotes ajoutés par SSH et deux ESP montées. La reprise après installation de base saute explicitement formatage/debootstrap ; un défaut de conservation de l'option de reprise a été corrigé, et la tentative de formatage du miroir déjà monté a été refusée par mke2fs sans modification. Le script vérifie désormais explicitement les outils et refuse le formatage d'un miroir monté.

Un mode de rattachement du contrôleur à l'installateur SSH existant permet de surveiller cette reprise sans relancer le PXE ni le script destructif. La fenêtre d'exécution est renouvelée à partir du démarrage authentifié. Le constructeur intègre maintenant tee/gzip et les modules FAT pour les prochains boots. La réception finale reste subordonnée aux contrôles effectifs, pas à ces correctifs.


## Installation neuve finalisée, premier redémarrage en vérification

La reprise distante a installé le noyau Debian 6.12.113+deb13-amd64, configuré les deux comptes, généré l'initramfs et vérifié les copies EFI. Une installation GRUB signée standard a également été exécutée avec succès. Le Dell a redémarré automatiquement ; le retour réseau et les authentifications ne sont pas encore validés à cette observation. Un avertissement fsck.ext4 absent a été relevé avant reboot : e2fsprogs est ajouté explicitement aux dépendances de la recette et du playbook ; l'affichage physique et le diagnostic doivent déterminer la cause réelle du défaut de retour réseau avant réception. Ne pas affirmer qu'une connexion adminjarvis est validée. La nouvelle image de supervision inclut les outils et modules FAT manquants et passe les contrôles ciblés en RAM ; aucun nouveau formatage n'est nécessaire pour une réparation du démarrage.


## Défaut constaté par le propriétaire — clavier installé QWERTY

Le 17 octobre 2026, après le redémarrage de Debian neuf, le propriétaire confirme l'invite de connexion et constate que le clavier physique reste en QWERTY. Le chargement AZERTY vérifié dans l'installateur ne s'est donc pas traduit par une disposition française effective sur la console du système installé. Les fichiers de configuration et setupcon --save-only ne constituent pas une validation de la disposition active.

Correction à exécuter dès accès : charger le clavier français sur la console, vérifier keyboard-setup.service et console-setup.service ainsi que leurs journaux et cartes enregistrées, corriger la configuration persistante et les éventuels fichiers générés/initramfs, puis vérifier après redémarrage sur la console réelle (notamment keycode16=a, keycode17=z). Maintenir cette exigence pour secours/installateur/système. Le défaut est ouvert ; aucune correction installée ni vérification après reboot n'est revendiquée à ce stade.

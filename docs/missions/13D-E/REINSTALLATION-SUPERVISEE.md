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


## Dépendance réseau manquante constatée en console

Le propriétaire signale `ip : commande introuvable` après connexion locale. iproute2 était absent de la sélection de paquets du système minimal : il est désormais explicitement ajouté à la recette et au playbook. Son installation effective sur le Dell reste à vérifier. networkctl, fourni par systemd, est le moyen de diagnostic alternatif proposé. Le retour réseau et les authentifications SSH restent à réceptionner.


## Réseau, authentifications, clavier et RAID — résultats confirmés après reprise

Le propriétaire a observé State off / Network File n/a. Le fichier réseau créé sous umask 077 n'était pas lisible par systemd-networkd. La remise des droits du répertoire à 0755 et du fichier à 0644, suivie d'un redémarrage du service, a rétabli routable/online. Le contrôleur a ensuite validé réellement adminjarvis par mot de passe, sudo et une connexion indépendante par clé. Le secours par mot de passe reste préservé. Ces droits sont maintenant explicites dans la recette et Ansible.

Cause du QWERTY identifiée par SSH : /etc/vconsole.conf est un lien vers /etc/default/keyboard sur ce Debian. L'écriture de KEYMAP=fr avait tronqué le fichier XKB complet. La configuration combinée a été restaurée sans tronquer ce lien, les cartes régénérées et chargées : dumpkeys sur tty1 confirme keycode16=+a et keycode17=+z. La persistance après le prochain reboot reste à vérifier.

Le miroir conservé est [UU], mais une resynchronisation complète a repris après le reboot forcé de l'installateur ; une observation a montré 15,2 %, environ 141 minutes restantes. La préservation des métadonnées n'a donc pas évité cette synchronisation. Le reboot forcé constitue une cause probable de l'état sale et doit être remplacé par une séquence de démontage/arrêt propre pour les prochaines installations. Ne pas arrêter ni faussement déclarer terminée cette resynchronisation. La phase IA peut avancer avec deux membres sains, mais la réception finale exige le retour idle, puis un redémarrage normal et la relecture de l'état.

mdmonitor échouait faute de destinataire ou de programme d'alerte. Un programme local de journalisation a été configuré, puis le service relancé et constaté actif ; aucun email d'alerte non demandé n'a été envoyé. iproute2/e2fsprogs sont explicitement requis par la recette corrigée. NVIDIA, CUDA, Ollama et l'intégration restent à vérifier selon les preuves de la phase IA.


## Affichage de progression rétabli après le premier reboot

Le suivi existait en fichier mais n'était plus visible en console après reboot : cette limitation ne satisfaisait pas la demande. Une console dédiée tty8 a été créée et activée, sans fermer la session tty1. Alt+F8 affiche le suivi ; Alt+F1 revient à la connexion. La commande jarvis-progress fournit la même vue actualisée depuis SSH. Le service est activé pour les démarrages suivants et le constructeur/recette embarquent désormais les mêmes assets. Le service actif et tty8 comme console courante ont été vérifiés à distance.

La vue compacte conserve toutes les tâches, les barres, états, durées et heures de dernière activité ; les détails sont disponibles via progress.py --details et les journaux privés. La resynchronisation est mesurée depuis /proc/mdstat, car sync_completed dans sysfs reflétait un point de progression plus ancien. Les coches sont réservées aux contrôles réellement réussis. Les phases sans pourcentage mesurable affichent une barre d'activité, sans pourcentage inventé.


## Progression IA et correction d'un suivi périmé

Pilote NVIDIA 550.163.01 chargé : une RTX 3090 reconnue, 24576 MiB. La première passe Ansible a réussi. Le transfert des modèles a ensuite échoué parce que le répertoire parent /var/lib/ollama était privé à l'utilisateur de service, empêchant adminjarvis d'atteindre models. Le transfert utilise désormais sudo rsync sur la cible ; les clés et mots de passe restent privés. Les binaires avaient été copiés, mais le moteur Ollama et les inférences n'étaient pas encore validés à cet arrêt.

Le tableau affichait à tort un état ancien et 99 % provenant d'un transfert précédent : les événements de transfert sont maintenant délimités, la phase en échec doit être signalée explicitement et la télémétrie RAID continue même après un échec IA. Lecture réelle lors de la reprise : RAID sain [UU], environ 51 % de resynchronisation. Nouvelle passe Ansible sans échec, transfert relancé ; aucune réussite des modèles ou d'Ollama n'est déduite de ces seules opérations.


## Intégration JARVIS — refus d'authentification corrigé et tests réussis

L'échec d'intégration provenait d'un HTTP 403 à la connexion de test à la passerelle du Mac : le mot de passe enregistré dans credentials.txt ne correspondait plus au hash actif. Le mot de passe déjà imposé par le propriétaire correspondait à l'authentification courante. Le test sélectionne désormais un identifiant local déjà disponible et vérifié contre le hash actif, sans modifier les comptes, les mots de passe ou les règles d'authentification. Les secrets restent privés. Le mécanisme de restauration avait conservé les paramètres précédents après le premier échec.

La reprise a réellement validé : passerelle authentifiée avec inférence Qwen sur le Dell, rappel d'un souvenir fictif temporaire depuis la mémoire SQLite canonique (fixture ensuite supprimée), appel réel de jarvis_services, Whisper Small sur WAV synthétique puis Qwen Dell et Piper Tom, et requête authentifiée Open WebUI avec Llama. Aucun microphone physique testé, aucune base parallèle créée. Ansible deuxième passe : changed=0, failed=0, unreachable=0. NVIDIA/CUDA et les trois modèles ont déjà des preuves d'inférence GPU réelles.

La réception finale reste en cours : attendre la fin de resynchronisation RAID, vérifier le stockage, effectuer un reboot normal, puis retester les accès/services/GPU et les requêtes authentifiées JARVIS/Open WebUI. Le contrôleur dispose d'un mode de reprise depuis ces preuves d'intégration pour éviter de réinstaller ou retransférer des composants déjà validés. Le relais d'affichage reste désormais actif en cas d'échec, au lieu de figer la console.

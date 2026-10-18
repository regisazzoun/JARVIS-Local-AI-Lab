# Dernière réception 13D-E / 14

RÉCEPTION COMPLÈTE VALIDÉE. Référence : [réception de la nouvelle tentative](RECEPTION-MISSION14.md). Les sections suivantes sont historiques.

## Bilan explicite des erreurs et des scripts corrigés — 17 octobre 2026

Cette section décrit les erreurs de la chaîne livrée et de son exécution. Elle distingue les corrections vérifiées des défauts encore présents dans le code. Les anciens états « incomplet », « en cours » et « à vérifier après reboot » ci-dessous sont des traces historiques, remplacées pour la réception courante par les résultats du [rapport de réception](RECEPTION-MISSION14.md).

Les scripts cités se trouvent dans `deployment/13de/reinstall/`.

| Erreur / conséquence observée | Correction et scripts concernés | Résultat et limite |
| --- | --- | --- |
| Utilisation de l’inventaire brut comme manifeste : lecteur SD sans média interprété comme stockage supplémentaire ; arrêt du garde d’identité. | Chaîne `build-supervised.py` / `serve-supervised.py` alimentée par le manifeste qualifié, avec exclusion précise du lecteur vide. Les contrôles DMI et identité des NVMe restent obligatoires. | Installation réalisée sur la cible qualifiée ; cet arrêt initial n’a pas écrit sur les disques. |
| Image minimale sans `tee`, puis modules FAT manquants : interruption du script et impossibilité de monter les ESP. | `build-supervised.py` : applets statiques et modules authentifiés nécessaires ; dépannage de l’environnement en RAM puis reprise. | Montage et vérification des deux ESP réussis ; pas de reconstruction systématique du noyau. |
| Argument `--resume-base` perdu après `set --` : tentative de formatage lors d’une reprise. | `install-preserve.sh` : conservation de l’argument dans `resume_base` et refus explicite de formater une racine montée. | `mke2fs` avait refusé l’opération sur la racine montée ; aucune perte supplémentaire constatée. Reprise sans refaire le formatage. |
| Configuration réseau créée sous `umask 077`, illisible par networkd : interfaces off, Network File n/a. | `install-preserve.sh`, `server.yml` : droits explicites 0755 sur le répertoire et 0644 sur le fichier réseau. | Réseau routable/online et accès SSH rétablis ; disponibilité confirmée après reboot. |
| Écriture de `KEYMAP` via un lien `/etc/vconsole.conf` : configuration XKB tronquée, clavier QWERTY. | `install-preserve.sh`, `server.yml` : configuration française combinée, respect du lien, régénération et chargement de la carte. `finish-ai.py` contrôle la carte après reboot. | `dumpkeys` confirme keycode16=a et keycode17=z après reboot. La mention VC Keymap unset de localectl ne remplace pas cette mesure réelle. |
| Commande `ip` et outils ext4 absents du système minimal. | `install-preserve.sh`, `server.yml` : dépendances `iproute2` et `e2fsprogs` explicites. | Outils disponibles dans le système installé. |
| `mdmonitor` en échec faute de destination d’alerte. | `server.yml` : programme local d’alerte vers le journal. | Service rétabli ; aucun mécanisme d’email d’alerte n’est revendiqué. |
| Redémarrage forcé de l’installateur, suivi d’une resynchronisation RAID intégrale malgré la conservation des métadonnées. | `finish-ai.py` attend désormais la fin du RAID et utilise `systemctl reboot` pour la réception finale. **`serve-supervised.py` contient encore `sync; reboot -f` : correction du passage installateur → Debian restant à faire.** | RAID terminé et sain [UU], puis reboot final normal validé. Le lien entre reboot forcé et resynchronisation est une cause probable, pas une preuve exclusive. Ne pas promettre que le prochain déploiement évitera la resynchronisation avec le contrôleur actuel. |
| Transfert des modèles refusé : parent du répertoire privé à l’utilisateur Ollama. | `finish-ai.py` : rsync distant via sudo, sans ouvrir globalement les permissions. | Transfert achevé ; inférences GPU réelles Qwen, Ministral et Llama réussies. |
| Progression figée / ancien 99 % après échec ; suivi non visible en console après reboot. | `finish-ai.py`, `telemetry.py`, `dashboard.py`, `progress.py` : erreurs explicites, transferts délimités, télémétrie maintenue, mesure RAID par /proc/mdstat. `progress-viewer.sh`, `progress-console.service`, `install-preserve.sh` : vue SSH et tty8 persistante. | Suivi rétabli et tâches clôturées sur preuves. Pourcentage global par tâches, pas estimation fiable du temps restant. |
| Test d’intégration HTTP 403 : fichier de credentials périmé. | `integrate.py` : sélection d’un secret local existant correspondant au hash actif, sans changement de compte ou mot de passe. | Passerelle, Open WebUI, mémoire canonique, outil et chaîne vocale synthétique validés. Secrets exclus de Git. |
| Risque de reboot pendant l’installation KDE ajoutée en cours de mission. | `install-plasma.sh`, `plasma-worker.py`, `await-plasma.py`, `finish-ai.py`, `progress.py` : tâche distincte et attente de son installation avant reboot ; contrôle SDDM/Xorg ensuite. | Gestionnaire graphique actif après reboot ; session utilisateur interactive non testée. |
| `nvidia-persistenced` et `polkit` observés en échec pendant le déploiement. | Contrôle à nouveau après reboot ; aucune correction spécifique de ces deux causes n’est démontrée par les changements de scripts vérifiés ici. | À 17 h 18, les deux services sont actifs et systemctl --failed est vide. Ne pas présenter ce rétablissement comme une correction de code identifiée. |

### État confirmé et travail restant

Réception automatique terminée à 15 h 09 ; contrôle supplémentaire en direct à 17 h 18 : RAID [UU] sans resynchronisation, SSH/Ollama/SDDM/polkit/nvidia-persistenced actifs, aucun service en échec. GPU au repos : 29 °C, environ 30 W, ventilateurs 30 %, contre 57–60 °C et environ 117 W avec Qwen chargé lors du diagnostic précédent. Ces mesures ne constituent pas un relevé des ventilateurs du châssis.

Pour le prochain déploiement, corriger et qualifier l’arrêt propre de l’installateur dans `serve-supervised.py` reste nécessaire. Les essais physiques de session KDE, microphone réel, retrait d’un SSD et seconde RTX ne sont pas revendiqués. La seconde RTX demeure inutilisée faute d’alimentation complète. Les preuves détaillées restent privées ; aucun secret ni identifiant matériel unique n’est publié.

---

# Dernière réception 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Référence : [réception de la nouvelle tentative](RECEPTION-MISSION14.md). Les sections suivantes sont historiques.

# Dernière réception 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Référence : [réception de la nouvelle tentative](RECEPTION-MISSION14.md). Les sections suivantes sont historiques.

# Dernière réception 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Référence : [réception de la nouvelle tentative](RECEPTION-MISSION14.md). Les sections suivantes sont historiques.

# Dernière réception 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Référence : [réception de la nouvelle tentative](RECEPTION-MISSION14.md). Les sections suivantes sont historiques.

# Dernière réception 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Référence : [réception de la nouvelle tentative](RECEPTION-MISSION14.md). Les sections suivantes sont historiques.

# Dernière réception 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Référence : [réception de la nouvelle tentative](RECEPTION-MISSION14.md). Les sections suivantes sont historiques.

# État courant — installation autonome prête pour lancement PXE

PXE et découverte physiques acquis. Le propriétaire autorise l’installation complète sur les deux NVMe identifiés, le reboot et l’administration SSH/Ansible, sans nouvelle validation humaine. La seule intervention attendue est le lancement PXE lorsque les services sont annoncés prêts. Qualification ciblée RAID1/deux ESP et deux démarrages UEFI sur disque virtuel seul réussis ; 25 tests + récepteur passent. **Aucune installation Dell encore effectuée.**

Directive prioritaire : [prompt d’installation autonome](PROMPT-INSTALLATION-AUTONOME.md). Les états ci-dessous sont conservés avec leur contexte ; leurs anciennes demandes de validation humaine ne remplacent pas cette directive.

---

# Reprise 13D-E — GO AVEC RÉSERVES pour la préparation physique

La préparation progresse vers le Dell sans imposer un laboratoire virtuel complet. Aucun Dell installé et aucune autorisation de lancement physique déduite de ce verdict. Le NO-GO historique reste conservé ci-dessous avec son contexte.

Livré et contrôlé : audit hôte accessible, sources Debian authentifiées, templates ProxyDHCP limité au MAC Dell/TFTP/HTTP, iPXE de découverte, manifeste matériel et garde pré-partitionnement, builder d'initrd sans autorisation d'effacement, preseed RAID candidat, playbook physique verrouillé, procédures réseau/RAID/SSH/reprise/intégration. 16 tests passent, deux playbooks passent le syntax-check, HTTP loopback et démarrage Debian Installer TCG ciblé réalisés. Aucun service LAN PXE activé, accès hôte conservés.

**Réserves empêchant le lancement immédiat de l'installation :**

- Plan réseau exact, interface d'écoute, MAC Dell et effets LAN à approuver humainement avant activation.
- Identités Dell/CPU/GPU/contrôleur/SSD et mode VROC inconnus ; manifeste réel à valider avant toute écriture.
- Recette partman RAID candidate non qualifiée, double ESP et démarrage depuis chacun des NVMe à tester ; aucun effacement autorisé.
- Clé publique de déploiement réelle à sélectionner et vérifier ; premiers SSH et idempotence Ansible non testés faute de Debian cible.
- Rôles NVIDIA/CUDA/Ollama encore différés ; worker et intégration JARVIS non réceptionnés. Ces étapes ne doivent pas être présentées comme opérationnelles.
- Accès utilisateur KVM refusé, sans impact sur la préparation physique ; TCG testé.

La prochaine étape est une séance de découverte et la qualification ciblée du stockage, suivies des autorisations distinctes réseau et installation. Les commandes et conditions exactes sont dans [la procédure physique](DEPLOIEMENT-PHYSIQUE.md), les preuves dans [les tests](TESTS.md). Ce GO AVEC RÉSERVES porte sur l'avancement préparatoire ; il ne vaut pas GO de mise en service ni clôture des réserves de recette.

**ROADMAP ↔ SUIVI synchronisés, format SUIVI conservé.** Publication sur `codex/mission-13de-preparation`, sans fusion dans main.

---

## Addendum matériel et décision de déploiement — 16 octobre 2026

Informations confirmées par le propriétaire (non mesurées à distance lors de cette mise à jour) : Dell Precision 5820 X-Series, BIOS 2.24.0, processeur Intel Core i9 X-Series Extreme (référence exacte restant à relever), **8 × 32 Go = 256 Go RAM détectés dans le BIOS**, deux NVIDIA RTX 3090 présentes dans les logements PCIe. Le système atteint le BIOS avec les deux cartes en place ; **une seule RTX 3090 est actuellement alimentée complètement**, les cordons de la seconde étant attendus. L'accès BIOS n'est pas une preuve de reconnaissance CUDA des deux cartes. La seconde carte ne doit être raccordée qu'après extinction complète et déconnexion secteur, avec câblage/adéquation PSU validés ; éviter de solliciter une carte sans alimentation auxiliaire. Risque spécifique de dépassement de l'enveloppe graphique constructeur avec deux RTX 3090 de 350 W : vérifier PSU, câbles d'origine compatibles, rails/connecteurs et limites de puissance avant usage conjoint ; aucune validation de double-GPU à pleine puissance n'est revendiquée.

Stockage identifié via BIOS/VROC : NVMe **KIOXIA KXG70PNV2T04** et **Samsung PM9A1** (~2 To chacun), Intel VROC 7.0.3.1006 en **pass-through**, aucun volume RAID VROC. **Décision confirmée : RAID 1 logiciel Linux `mdadm` sous Debian 13**, pas de RAID VROC ni achat de clé d'activation. Le `deployment/13de/debian/preseed-dell.candidate.cfg` existant configure déjà `partman-auto/method=raid` et `mdadm` ; il demeure **candidat**, sans garantie de partitionnement UEFI correct ni d'amorçage autonome sur chacun des deux disques. Qualifier ESP sur chaque disque, copie/synchronisation chargeurs EFI, démarrage dégradé, surveillance mdadm/SMART et reconstruction en VM avant toute installation physique.

**Exclusion utilisateur : ne pas réaliser de benchmarks de débit ou de tests intensifs d'écriture NVMe** (`fio`, `dd` de performance, mesure comparative CPU/RAID). Seules les vérifications fonctionnelles nécessaires à la sécurité et à la résilience restent dans le périmètre.

**Suite 13D-E :** conserver infrastructure PXE préparée, proxyDHCP Bbox et garde d'effacement ; préparer installation sur une seule RTX 3090 alimentée, puis reconnaissance contrôlée de la seconde après ajout de ses câbles, **sans réinstallation Debian**. Aucune activation des services LAN, aucun effacement et aucune installation physique ne sont autorisés par cet addendum. Les réserves historiques ci-dessous sont conservées comme traces d'état à leur date.

---

## Installation autonome autorisée et préparée — 16 octobre 2026

Le propriétaire autorise explicitement l'effacement des deux NVMe identifiés, l'installation, le reboot et l'administration sans validations humaines intermédiaires ; sa seule intervention sera le lancement PXE. Directive enregistrée dans AGENTS.md et [le prompt de référence](PROMPT-INSTALLATION-AUTONOME.md), prioritaire sur les anciens prompts de mission contradictoires.

Qualification ciblée acquise : deux NVMe virtuels, RAID1 [UU], deux ESP FAT distinctes et finalisation EFI ; puis deux démarrages **natifs UEFI**, A seul et B seul, racine md0 en état dégradé attendu. 25 tests + récepteur passent. Les défauts identifiés pendant la qualification ont été corrigés avant construction de l'image réelle. Les preuves brutes et autorisations liées aux séries restent privées. Aucun test physique de retrait NVMe, aucune installation Dell encore effectuée.

Profil adapté au DMI réel, sans abandon du contrôle UUID/séries/modèles/tailles. Le lecteur SD n'est exclu que sans média et au modèle exact ; tout autre stockage bloque. Image d'installation complète et superviseur de bootstrap/Ansible préparés. Secret et identité dédiés privés, SSH/Tailscale/services Mac et DHCP Bbox préservés. GPU/IA restent une phase ultérieure indépendante.

---

## Adaptation bootstrap A/B — 16 octobre 2026

**PXE UEFI physique acquis ; GO pour la prochaine découverte automatique seulement, avant autorisation réseau.** Initrd privé de découverte préparé, envoi du rapport et génération de manifeste non approuvé sans saisie des résultats. Blocage indéfini avant partitionnement, aucun service activé.

Bootstrap temporaire par mot de passe fort local, hash seul dans le futur initrd, SSH limité à JARVIS et root interdit. Transition par connexions indépendantes à clé avec sudo, révocation seulement après preuve positive, reprise et nettoyage des secrets implémentés. Candidat installation minimal/RAID1, finalisation des deux ESP, synchronisation EFI et orchestration Ansible protégée livrés comme code **non réceptionné sur le Dell**.

Validations : 22 tests contrôleur/manifeste/bootstrap et un test agrégé récepteur réussis ; politique SSH évaluée hors daemon ; deux playbooks syntax-check ; archives découverte et candidat synthétique inspectées ; dnsmasq/nft vérifiés sans activation. Aucune campagne VM ou écriture Dell. Le candidat synthétique a été supprimé.

Réserves bloquant l'installation : découverte exacte UUID/séries/capacités, qualification partman RAID/double ESP, approbation explicite d'effacement et de reboot, revue de l'exposition du futur initrd sur LAN maîtrisé, identité SSH permanente autorisée à sélectionner. La réception de clé hôte par capacité HTTP/MAC n'est pas une attestation indépendante sur LAN hostile. Ansible réel, double boot disque, idempotence cible et GPU/IA restent non réceptionnés. Les trois autorisations réseau/installation/administration sont distinctes.

Premier essai automatique : noyau/initrd chargés, mais rapport absent et écran noir. Défaut détecté dans le wrapper (pilote NVMe absent du netboot) ; image corrigée avec pilotes Debian authentifiés, DHCP BusyBox et console explicite. Chargement des trois pilotes confirmé par un test TCG ciblé sans disque ni réseau. Nouvelle réception physique encore en attente.

Détails et commandes : [bootstrap automatisé](BOOTSTRAP-AUTOMATISE.md). Aucun changement aux accès/services JARVIS, DHCP Bbox, BIOS/VROC, SQLite ou GPU. Branche et PR existantes, sans fusion.

---

## Demande du propriétaire — suivi complet des prochains déploiements

Instruction consolidée le 16 octobre 2026 : mettre en place un suivi automatique de l'ensemble des tâches du déploiement, depuis le démarrage PXE jusqu'à la réception finale. Présenter sur une page JARVIS une barre de progression globale et une liste chronologique des tâches, chacune avec sa propre barre de progression et son état : à venir, en cours, réussie, en échec ou bloquée. Afficher une coche de validation uniquement après une vérification effective de la réussite de la tâche ; ne pas confondre lancement, fin d'exécution et validation du résultat.

Le suivi doit couvrir le téléchargement des images, le démarrage de l'installateur, la vérification du matériel et des disques, le partitionnement, la création et la synchronisation RAID, l'installation du système et des paquets, la configuration réseau et SSH, la préparation et la vérification des deux ESP et chargeurs, le redémarrage sur disque, la réception du rapport de premier boot, la création et la validation de l'accès permanent, la révocation du bootstrap, les deux passes Ansible, les contrôles finaux et le nettoyage. Toute tâche supplémentaire exécutée par le déploiement doit également apparaître dans ce suivi.

Actualiser automatiquement les états et afficher pour chaque tâche son heure de début, sa durée, sa dernière activité et, en cas d'échec ou de blocage, le message et les journaux utiles au diagnostic. Utiliser les mesures réelles lorsqu'elles sont disponibles ; identifier clairement les pourcentages estimés et afficher une activité en cours lorsque la progression n'est pas mesurable. Ne jamais afficher 100 % ni une coche de réussite sur la seule base du temps écoulé. Prévoir aussi un affichage synthétique de l'avancement sur la console du Dell pour éviter qu'un écran inchangé donne l'impression d'un plantage.

Prévoir un accès SSH temporaire dans l'installateur, accessible par clé depuis JARVIS uniquement, dès que le réseau est disponible et avant le partitionnement, puis pendant toute l'installation et la finalisation. Ce canal doit permettre à JARVIS de surveiller l'ensemble des tâches : journaux de l'installateur, processus, installation des paquets, stockage et RAID, configuration et contrôles de démarrage. Il complète les événements automatiques qui alimentent les barres de progression et les validations ; sa fonction ne se limite pas au RAID. Vérifier l'identité de la cible et la clé hôte avant connexion, conserver les clés privées sur JARVIS, ne pas exposer de secrets dans le suivi et retirer l'accès temporaire à la fin de l'installation. L'ensemble doit fonctionner sans nouvelle intervention manuelle ni validation intermédiaire du propriétaire.

Cette amélioration consolidée remplace les formulations précédentes relatives aux barres de progression et à la surveillance SSH. Elle est à réaliser pour les prochains déploiements ; elle n'est pas déclarée implémentée ni validée dans la mission actuelle.

## Rapport historique de la première exécution (conservé)

# Réception 13D-E — NO-GO pour réception complète

La préparation documentaire et une première base de code sont livrées. Les critères de réception ne sont pas tous atteints : aucun essai PXE/UEFI réel, aucune installation VM et aucune exécution Ansible ne sont possibles dans les capacités actuellement exposées à cette session. La mission n'est donc **pas déclarée achevée techniquement**. NO-GO pour lancer 14A avec cette chaîne, et pour tout déploiement Dell. Ce verdict n'annule pas le GO historique des accès 13D ou les preuves 13F.

| Domaine | Preuve acquise | Réserve / verdict |
| --- | --- | --- |
| Infrastructure JARVIS | Aucun changement système, modèle, base, disque physique ou service | Santé courante inaccessible ; absence de dégradation non certifiable |
| SSH | sshd_config identique avant/après ; aucun accès ni clé modifié | Procédure et script invités seulement ; aucune connexion Dell attendue |
| Tailscale | Aucun fichier/commande de configuration modifié | Service non inspectable dans cette session |
| Ansible | Inventaires lab/Dell, playbook et neuf rôles distincts | Absent ; syntax-check et idempotence non testés ; trois rôles IA explicitement différés |
| PXE/Debian | Script iPXE, template preseed, injection SSH préparés | Pas d'essai réel ; HTTP/mirror isolé et recette RAID1 exécutables non livrés |
| Laboratoire | Contrôleur TCG préparé ; six tests de garde-fous passent | QEMU/OVMF absents ; KVM non accessible ; boucle complète non fonctionnelle |
| Agent JARVIS | Contrat d'outils bornés et recette 14A documentés | Aucun raccordement à 13F ni service de tâches durable ; aucune autonomie simulée |
| Dell | Aucune intervention | Contrôleur, SSD, RAID et firmware toujours à identifier avant décision destructive |
| Documentation | Audit, architecture, SSH, laboratoire, agent, tests, incidents ; roadmap/suivi synchronisés | Publication sur branche dédiée, sans fusion automatique |

## Suite nécessaire

1. Rendre disponibles les outils utilisateur et firmware authentifiés dans un environnement permettant QEMU TCG ; un diagnostic/une validation ciblée reste requis avant toute installation système à risque.
2. Fournir une source de paquets hors ligne isolée, un transport SSH invité et un profil de second boot disque ; compléter HTTP si retenu.
3. Sélectionner une clé publique existante dont JARVIS contrôle le signataire ; produire l'initrd privé et vérifier le compte SSH.
4. Exécuter installation VM, Ansible deux fois, collecte complète des journaux ; développer et éprouver le RAID1 en VM.
5. Raccorder le worker à une copie de la passerelle avec superviseur durable et quotas, puis faire réaliser la recette 14A par le modèle local.

Les essais VM jetables restent autorisés sans confirmation par essai. Les obstacles actuels sont l'absence d'outils et les capacités de la session, pas une demande d'approbation des essais virtuels. Aucun service sensible n'a été modifié pour les contourner.


## Découverte automatique physique reçue — 16 octobre 2026, 19:24

Le Dell affiche « rapport envoyé, attente de revue humaine ». Rapport complet reçu et empreinte vérifiée ; réception et inventaire brut conservés uniquement sous private, permissions 0600. Services ProxyDHCP/TFTP/HTTP/récepteur automatiquement arrêtés et filtre temporaire retiré ; SSH/Tailscale/NetworkManager restent actifs. Aucune installation/écriture NVMe.

Données mesurées : Precision 5820 Tower X-Series, Core i9-10980XE, 36 processeurs logiques, MemTotal 263631232 kB ; deux NVMe KIOXIA KXG70PNV2T04 et Samsung PM9A1, chacun 2048408248320 octets. Les deux disques ont déjà des partitions. Un seul contrôleur graphique NVIDIA est exposé par le rapport PCI ; aucune opération sur la seconde carte et aucune validation CUDA. /proc/mdstat absent : absence de RAID non démontrée.

**NO-GO installation maintenu.** Le manifeste d'installation a été refusé : périphérique supplémentaire /dev/sda, SD/MMC CRW, taille nulle, et produit DMI « Precision 5820 Tower X-Series » différent du profil strict historique « Precision 5820 Tower ». Les séries et UUID sont conservés dans l'inventaire privé ; aucun identifiant matériel unique publié. Ne pas ignorer globalement les disques supplémentaires : identifier/qualifier le lecteur sans média avant révision précise de la politique. Autre écart à revoir : BIOS DMI 2.8.0 daté du 15 janvier 2021, alors que 2.24.0 avait été annoncé ; aucune modification firmware autorisée ou effectuée.

Découverte automatique réalisée et reçue ; qualification RAID/deux ESP, approbation d'effacement portant sur les séries réelles, identité SSH permanente et autorisation administrative restent à obtenir.


## Clôture de la tentative — 17 octobre 2026

Installation Debian finalisée et démarrage confirmé par console/SSH ouvert, mais rapport de premier boot absent et accès authentifié/Ansible non réceptionnés. Tentative arrêtée à la demande du propriétaire. Le [rapport transitoire de reprise](RAPPORT-TRANSITOIRE-REPRISE.md) porte les directives prioritaires pour terminer la mission : adminjarvis, mot de passe utilisateur privé, maintien du secours SSH, clavier français et conservation du RAID existant si possible.


## Défaut constaté par le propriétaire — clavier installé QWERTY

Le 17 octobre 2026, après le redémarrage de Debian neuf, le propriétaire confirme l'invite de connexion et constate que le clavier physique reste en QWERTY. Le chargement AZERTY vérifié dans l'installateur ne s'est donc pas traduit par une disposition française effective sur la console du système installé. Les fichiers de configuration et setupcon --save-only ne constituent pas une validation de la disposition active.

Correction à exécuter dès accès : charger le clavier français sur la console, vérifier keyboard-setup.service et console-setup.service ainsi que leurs journaux et cartes enregistrées, corriger la configuration persistante et les éventuels fichiers générés/initramfs, puis vérifier après redémarrage sur la console réelle (notamment keycode16=a, keycode17=z). Maintenir cette exigence pour secours/installateur/système. Le défaut est ouvert ; aucune correction installée ni vérification après reboot n'est revendiquée à ce stade.


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


## Ajout demandé par le propriétaire — KDE Plasma avant le reboot final

Le propriétaire demande KDE Plasma sur le Dell avant le redémarrage final. Une dix-huitième tâche KDE Plasma est ajoutée au tableau, en cours jusqu'à validation effective. Installation de kde-plasma-desktop, SDDM, Xorg/KWin X11 et outils de base, avec configuration française ; le réseau existant reste piloté par systemd-networkd. Le gestionnaire de connexion est préparé pour le prochain boot, sans autologin.

La réception finale est retenue jusqu'à la fin de cette installation, en plus de la synchronisation RAID. La reprise automatique reprend ensuite les contrôles finaux, avec vérification de SDDM et Xorg après reboot. L'ouverture interactive d'une session Plasma n'est pas déclarée testée tant qu'elle n'a pas été observée. SSH, sudo, le secours par mot de passe et les services IA restent à préserver.


## Loupé du déploiement 13D-E — client Tailscale absent (18 octobre 2026)

Le propriétaire signale et classe explicitement cette omission parmi les loupés de la mission 13 de déploiement du Dell n°1. Le client Tailscale n’a pas été installé sur le Dell : le contrôle de reprise constate l’absence du binaire et un service `tailscaled` inactif. L’accès direct au Dell par le tailnet n’est donc pas opérationnel et ne doit pas être présenté comme réceptionné.

Les accès LAN et les accès relayés par le Mac mini sont distincts d’un client Tailscale installé sur le Dell ; ils ne corrigent pas cette omission du déploiement initial. Les résultats Debian, RAID, SSH et IA déjà vérifiés restent conservés, avec cette réserve réseau supplémentaire.

Correctif restant : installer et configurer un client Tailscale propre au Dell, puis vérifier son identité réseau, une connexion SSH depuis un autre client du tailnet et la persistance après redémarrage. Cette entrée documentaire ne constitue ni une installation ni une validation de ce correctif.

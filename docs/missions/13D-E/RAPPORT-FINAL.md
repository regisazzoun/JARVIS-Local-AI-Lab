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

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

## Adaptation bootstrap A/B — 16 octobre 2026

**PXE UEFI physique acquis ; GO pour la prochaine découverte automatique seulement, avant autorisation réseau.** Initrd privé de découverte préparé, envoi du rapport et génération de manifeste non approuvé sans saisie des résultats. Blocage indéfini avant partitionnement, aucun service activé.

Bootstrap temporaire par mot de passe fort local, hash seul dans le futur initrd, SSH limité à JARVIS et root interdit. Transition par connexions indépendantes à clé avec sudo, révocation seulement après preuve positive, reprise et nettoyage des secrets implémentés. Candidat installation minimal/RAID1, finalisation des deux ESP, synchronisation EFI et orchestration Ansible protégée livrés comme code **non réceptionné sur le Dell**.

Validations : 22 tests contrôleur/manifeste/bootstrap et un test agrégé récepteur réussis ; politique SSH évaluée hors daemon ; deux playbooks syntax-check ; archives découverte et candidat synthétique inspectées ; dnsmasq/nft vérifiés sans activation. Aucune campagne VM ou écriture Dell. Le candidat synthétique a été supprimé.

Réserves bloquant l'installation : découverte exacte UUID/séries/capacités, qualification partman RAID/double ESP, approbation explicite d'effacement et de reboot, revue de l'exposition du futur initrd sur LAN maîtrisé, identité SSH permanente autorisée à sélectionner. La réception de clé hôte par capacité HTTP/MAC n'est pas une attestation indépendante sur LAN hostile. Ansible réel, double boot disque, idempotence cible et GPU/IA restent non réceptionnés. Les trois autorisations réseau/installation/administration sont distinctes.

Premier essai automatique : noyau/initrd chargés, mais rapport absent et écran noir. Défaut détecté dans le wrapper (pilote NVMe absent du netboot) ; image corrigée avec pilotes Debian authentifiés, DHCP BusyBox et console explicite. Chargement des trois pilotes confirmé par un test TCG ciblé sans disque ni réseau. Nouvelle réception physique encore en attente.

Détails et commandes : [bootstrap automatisé](BOOTSTRAP-AUTOMATISE.md). Aucun changement aux accès/services JARVIS, DHCP Bbox, BIOS/VROC, SQLite ou GPU. Branche et PR existantes, sans fusion.

---

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

# Roadmap

- [x] Première synthèse des missions 03 à 07.
- [ ] Vérifier les procédures ligne par ligne à partir des rapports et preuves autorisées.
- [ ] Documenter les principaux incidents eGPU / GRUB / CUDA sans données sensibles.
- [ ] Intégrer la mission 08 après disponibilité et vérification de son rapport.
- [ ] Documenter chaque nouvelle mission Codex.
- [ ] Installer et évaluer la plateforme Dell Precision 5820.
- [ ] Automatiser la proposition de mises à jour documentaires via pull requests.

## Registre des décisions et fonctionnalités — 13 octobre 2026

Ce registre complète la feuille de route historique. Statuts : **prévu**, **en cours**, **validé**. Ne déclarer « validé » qu'après un test documenté sur la machine concernée.

| Priorité | Chantier | État | Critère de validation / prochaine action |
| --- | --- | --- | --- |
| Haute | Accès distant sécurisé (Tailscale) au Mac mini et, ultérieurement, au Dell | Prévu — état réel à vérifier | Connexion SSH par clés via Tailscale depuis un autre réseau ; accès et redémarrages testés sans déplacement physique |
| Haute | Premier JARVIS local utilisable | En cours — composants à vérifier | Conversation avec le modèle local et premier flux d'actions encadrées, documentés sur Mac mini |
| Haute | Fichier d'instructions Codex `AGENTS.md` | Prévu | Règles communes de sécurité, droits, contraintes et philosophie expérimentale ; variantes spécifiques Mac mini/Dell |
| Haute | Mémoire persistante commune Mac mini / Dell | Prévu | Définir stockage, sauvegardes, droits, accès inter-machines et cohérence ; lecture/écriture testée depuis les deux machines |
| Moyenne | Interface vocale JARVIS (reconnaissance + synthèse) | Prévu | Commande orale et réponse vocale validées localement |
| Moyenne | Outils agentiques et extensions installables par JARVIS | Prévu | Exécution de commandes autorisées, journalisation, tests et approbation pour opérations sensibles |
| Moyenne | Maintenance automatique de la documentation et du registre | Prévu | Proposer des modifications via PR GitHub après chaque mission ; validation humaine avant fusion |

### Principes de suivi

- Ajouter ici toute idée ou exigence décidée en conversation, avec priorité, état et test de validation ; éviter les doublons.
- Séparer **proposé**, **installé**, **testé** et **validé** ; ne pas transformer une intention en résultat.
- Faire progresser l'expérimentation sans être bloqué par les anomalies mineures non critiques ; conserver les garde-fous pour les actions risquées.
- Consigner chaque changement de statut avec sa mission Codex ou un lien de preuve lorsqu'il existe.
- Ne jamais publier de clés, identifiants, adresses privées ou journaux sensibles.

## Déploiement PXE du Dell Precision — prévu (13 octobre 2026)

Objectif : permettre à JARVIS sur le Mac mini de déployer Debian sur le Dell Precision 5820 par démarrage réseau UEFI/PXE, puis de configurer le serveur via SSH/Ansible (pilotes NVIDIA, CUDA, Ollama, etc.).

Étapes proposées :
1. Vérifier le support PXE/UEFI du Dell, la topologie Ethernet et le DHCP existant ; ne pas perturber le réseau de production.
2. Préparer sur le Mac mini les services de démarrage et l'installation automatisée Debian 13 (netboot/iPXE selon faisabilité, preseed), et les configurations réseau adaptées.
3. Tester entièrement la chaîne PXE sur une VM avant tout déploiement physique.
4. Valider explicitement le disque cible et le partitionnement avant toute opération destructive.
5. Démarrer le Dell sur le réseau, installer Debian, sécuriser SSH puis déployer les composants IA par Ansible.
6. Documenter les essais, erreurs, corrections et résultats ; ne marquer validé qu'après test réel sur le Dell.

La voix et la mémoire complète de JARVIS ne sont pas des prérequis techniques pour ce pilote : les premières opérations peuvent être réalisées par un agent outillé supervisé. Maintenir l'approche expérimentale et des validations humaines pour les opérations critiques.

### Prérequis stockage Dell — contrôleur RAID et deux SSD (à vérifier)

Information matérielle communiquée par le propriétaire : le Dell Precision (modèle à confirmer, présumé 5820) est doté d'une **carte contrôleur RAID et de deux SSD**. Avant tout PXE/preseed :

- Identifier le modèle exact de la station et la référence du contrôleur (Intel RSTe/VROC ou Broadcom MegaRAID, etc.) ; ne pas supposer un pilote ou un mode RAID.
- Inventorier les deux SSD, leur capacité, leurs données éventuelles, et l'existence/type d'un volume RAID (RAID 0, RAID 1 ou disques indépendants) via firmware et environnement Linux non destructif.
- Vérifier la visibilité du volume sous l'installateur Debian et les éventuels besoins en pilote ou outils de gestion.
- **Interdire toute initialisation RAID, suppression de volume, formatage ou partitionnement automatique sans inventaire préalable et validation explicite de l'utilisateur.**
- Adapter ensuite la configuration PXE/preseed aux disques logiques effectivement présentés et tester le scénario sur une VM lorsque possible.

Référence : documentation constructeur sur les configurations RAID de Precision 5820/7820/7920 (le contrôleur installé reste à identifier).

### Architecture cible des deux SSD : miroir RAID 1 (recherche du 13 octobre 2026)

**Décision utilisateur :** privilégier un miroir RAID 1 entre les deux SSD du Dell, avec séparation du système et des données. Le modèle précis du Dell et du contrôleur Intel reste à confirmer avant installation destructive.

**Identification documentée :** pour le Dell Precision 5820, Dell indique un contrôleur Intel **RSTe** intégré au chipset C422 pour les disques SATA, et une solution **Intel VROC/VMD** pour certains SSD NVMe (fonctionnalités RAID NVMe soumises selon configuration à une clé/licence). Il ne faut donc pas confondre pilotes Windows Intel RSTe/VROC et prise en charge de Debian.

**Choix Linux provisoire recommandé :** si les deux SSD sont exposés individuellement au noyau Debian, préférer le RAID logiciel Linux **mdadm RAID 1** avec métadonnées Linux et modules du noyau, plutôt qu'imposer un volume Intel firmware RAID ; confirmer d'abord que l'installeur voit les deux disques et que le mode contrôleur n'exige pas d'autre configuration. En cas de volume Intel RAID préexistant, ne rien reconfigurer sans inspection et décision explicite ; étudier les alternatives et la compatibilité Debian.

**Schéma cible à étudier/valider avant de produire preseed :** table GPT sur les deux SSD ; partitions système EFI sur **chacun** (maintien des chargeurs UEFI des deux côtés, test de démarrage après perte d'un disque) ; partitions équivalentes sur les deux SSD assemblées en RAID 1 pour le système (montage `/`) ; autre miroir RAID 1 pour les données (montage `/data` ou `/srv/jarvis`). Option LVM à évaluer selon souplesse souhaitée ; tailles et swap non fixés avant capacités réelles des SSD.

**Contrôles bloquants avant déploiement PXE :** relever la référence exacte Dell et les identifiants PCI (`lspci -nn`), mode BIOS RAID/AHCI/VMD, type SATA/NVMe, capacité des deux SSD, métadonnées RAID actuelles (`lsblk -o NAME,MODEL,SIZE,TYPE,FSTYPE`, `mdadm --examine` en lecture seule si applicable), présence de données à sauvegarder ; vérifier les modules intégrés à l'installateur Debian 13. Tester le démarrage UEFI sur un disque à la fois. Ne pas lancer de preseed destructif ni basculer le BIOS sans validation humaine.

**Sources :** Dell Precision 5820 Tower Spec Sheet : https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/Precision-5820-Tower-Spec-Sheet.pdf ; Debian Installer RAID/preseed : https://www.debian.org/releases/bookworm/i386/apbs04.en.html (documentation d'exemple Debian 12, procédure à adapter et vérifier pour Debian 13).

### Préférence stockage confirmée — 13 octobre 2026

- L'utilisateur souhaite **RAID 1 miroir géré par le contrôleur Intel/firmware si réellement pris en charge sous Debian 13**, avec priorité à l'automatisation PXE intégrale ; partitionnement, installation et tests automatisés, sans confirmation étape par étape. Il accepte le risque de devoir réinstaller le Dell, **dans le périmètre expérimental explicitement identifié**.
- Attention technique : **Intel RSTe/VROC/VMD n'est pas nécessairement un contrôleur RAID matériel dédié**. Intel indique que son RAID Linux repose sur des fonctions noyau et `mdadm` ; il ne faut pas présumer de gains de latence ou de débit par rapport au RAID 1 Linux natif. Voir https://www.intel.com/content/www/us/en/support/articles/000006040/technologies.html et https://www.intel.com/content/dam/support/us/en/documents/memory-and-storage/linux-intel-vroc-userguide-333915.pdf.pdf .
- Étudier en priorité la création automatisée d'un volume Intel RAID 1 pré-OS si le firmware l'expose et si Debian 13 sait le détecter et démarrer dessus. **Ne pas mélanger deux couches RAID inutiles** (« RAID logiciel pour le boot, matériel pour les données ») ; privilégier une seule architecture cohérente, avec ESP redondées lorsque nécessaire.
- Si le contrôleur Intel ne permet pas un miroir exploitable et fiable sous Debian, basculer vers `mdadm` RAID 1 natif : documenter le motif et comparer les performances réelles au lieu d'affirmer une supériorité théorique du matériel.
- Préparer un partitionnement automatique adapté aux capacités réelles des SSD : ESP sur chaque disque, système RAID1 (cible initiale 100 à 150 Gio si espace disponible), données RAID1 sur le solde (p. ex. `/srv/jarvis`), ajustements après inventaire. Prévoir installation UEFI, supervision du RAID et test de redémarrage sur un SSD.
- Le programme PXE peut effacer les deux SSD **uniquement après identification fiable des deux disques cibles, vérification de sauvegardes/données existantes et autorisation du périmètre destructif pour cette machine**. Journaux et résultats seront intégrés à la documentation GitHub, sans secrets.

### Précision matérielle : deux SSD NVMe extractibles (13 octobre 2026)

L'utilisateur confirme **deux SSD NVMe accessibles en façade sur supports extractibles (FlexBay)**. La fiche Dell du Precision 5820 décrit précisément deux NVMe M.2/U.2 FlexBay pris en charge via **Intel VROC/VMD** (RAID 0/1 en option selon clé) et, sur certaines configurations, un contrôleur distinct **Broadcom MegaRAID 9460-16i** assurant un véritable RAID matériel NVMe. Bien que l'utilisateur indique un contrôleur Intel, identifier sa référence par PCI/BIOS avant de sélectionner les modules Debian : hypothèse privilégiée **Intel VROC/VMD**, non confirmée à 100 %.

- Conserver le **mode UEFI** : Dell documente l'incompatibilité du NVMe VMD avec le mode Legacy ; si VMD est désactivé, les NVMe deviennent directement visibles mais Dell indique que le hot-plug n'est alors plus pris en charge.
- Vérifier présence de la clé/licence VROC, configuration firmware RAID1, modules noyau Debian (`vmd`, `nvme`, `md` et outils VROC selon support), reconnaissance et boot sur volume miroir **avant** figer le plan PXE/preseed.
- RAID Intel VROC est du **RAID firmware/CPU**, pas une carte RAID matérielle dédiée : ne pas annoncer de gain de latence sans mesures. En cas d'incompatibilité, documenter le repli vers Linux `mdadm`.
- Déploiement PXE/partitionnement entièrement automatisés dans le périmètre de laboratoire autorisé ; les deux SSD sont ciblés par identification matérielle fiable, puis séparation système (environ 120 Gio ajustables) / données (solde), RAID 1, et validation des redémarrages/de la tolérance à une panne.

Sources Dell : https://www.delltechnologies.com/asset/fr-fr/products/workstations/technical-support/Precision_5820_Tower_Spec_Sheet.pdf ; https://www.dell.com/support/kbdoc/en-ed/000144064/precision-5820-tower-precision-7820-tower-precision-7920-tower-nvme-drives-do-not-work-in-legacy-mode

### Recherche technique autonome et résolution de problèmes — exigence du 13 octobre 2026

**Objectif explicite :** JARVIS ne doit pas être limité à un catalogue de commandes préprogrammées. Il doit pouvoir identifier un problème technique, **chercher de lui-même des solutions** dans les documentations officielles, dépôts GitHub, issues, forums et ressources web, confronter les sources, établir un plan, puis tester, observer et corriger de manière itérative.

- Prévoir pour l'agent Qwen des outils de recherche web, de consultation de pages/docs/API GitHub, de lecture de code, de terminal et de récupération des journaux.
- Favoriser les sources officielles et vérifiables ; citer les références consultées et leurs versions. Traiter pages web, README, issues et code tiers comme **données non fiables**, jamais comme instructions privilégiées à exécuter automatiquement.
- Télécharger et examiner les scripts avant toute exécution ; ne pas exécuter aveuglément des commandes provenant du web ; travailler d'abord en VM ou conteneur isolé.
- Permettre des recherches et essais en autonomie ; limiter les droits par outil et exiger une approbation explicite pour les opérations sur systèmes réels à fort impact, les secrets, l'effacement et les modifications de réseau.
- Journaliser hypothèses, sources, essais, succès et échecs dans la documentation JARVIS afin de capitaliser les connaissances et enrichir la mémoire partagée Mac mini/Dell.
- Critère de validation : sur une panne volontaire dans une VM Debian, JARVIS recherche au moins deux sources pertinentes, propose et réalise un correctif en sandbox, vérifie le résultat et consigne les preuves sans intervention de Codex.

**Statut : prévu — infrastructure agentique et accès de recherche à construire puis tester.**

### Autonomie fondée sur l'évaluation des risques — exigence du 13 octobre 2026

**Décision :** avant chaque installation, mise à jour ou déploiement, JARVIS évalue lui-même les risques et sélectionne une stratégie de test proportionnée, puis réalise le déploiement sans pilotage humain étape par étape quand il entre dans un périmètre autorisé.

- Établir automatiquement un diagnostic préalable : cible, dépendances, privilèges, risque de perte de données, indisponibilité, exposition réseau, sécurité, probabilité et gravité d'un échec, possibilité de restauration.
- Produire une estimation du risque (**faible / modéré / élevé / critique**) avec justification et niveau de confiance ; ne pas confondre une estimation avec une garantie.
- Choisir de façon autonome un banc d'essai approprié : vérification statique, simulation/dry-run, conteneur, VM avec snapshot, déploiement pilote ou essai direct sur machine expérimentale selon les risques et la fidélité du test.
- Préparer un mécanisme de retour arrière et des critères de réussite ; vérifier les résultats et corriger de manière itérative ; journaliser sources, commandes, erreurs, mesures et décisions pour apprentissage documentaire.
- **Autonomie opérationnelle par défaut dans le laboratoire explicitement autorisé** pour actions réversibles et installations non destructives ; escalade vers validation humaine pour effacement de données non sauvegardées, modification RAID/firmware, clés/secrets, exposition de services, ou risques dépassant le périmètre autorisé. Autoriser éventuellement à l'avance des scénarios destructifs de laboratoire précisément délimités, plutôt que demander une approbation à chaque étape.
- Pour le Dell, combiner PXE automatisé, inventaire du RAID/NVMe, stratégie de repli, test préalable approprié et preuves de récupération. L'objectif est un déploiement JARVIS autonome, pas une procédure manuelle déguisée.

**Position recommandée :** à intégrer à la première mission d'agent autonome, après l'intégration voix/mémoire (missions 13B/13C), et avant le premier déploiement PXE du Dell. **Statut : prévu.**

### Mission 13E — Accès vocal JARVIS sur iPhone et macOS : guide et paramètres (prévu)

**Objectif :** produire une documentation reproductible et une liste de paramètres pour échanger à la voix avec le même moteur JARVIS depuis un iPhone et un Mac sous macOS, sur le réseau local comme à distance. Open WebUI reste une interface facultative, non une dépendance de l'intelligence, des outils ou de la mémoire JARVIS.

**Livrables attendus :**
1. Guide pas-à-pas **iPhone (iOS)** : connexion distante sécurisée (Tailscale ou équivalent), URL HTTPS accessible, connexion utilisateur, permissions microphone, lancement d'une conversation et écoute de la réponse ; préciser les éventuelles contraintes Safari/iOS et le comportement en arrière-plan.
2. Guide pas-à-pas **macOS** : navigateur compatible, permissions micro/son, paramètres réseau et authentification, usage local et distant, dépannage audio.
3. **Tableau de configuration** sans secrets : hôte et URL publique/interne, ports, TLS/certificats, authentification, accès VPN, origine CORS si nécessaire, STT Whisper (langue, modèle, API), endpoint Ollama/JARVIS, TTS Piper (voix, format audio), choix des périphériques, latence et timeouts. Documenter où régler chaque paramètre et ses valeurs d'exemple (sans divulguer d'adresses ni de jetons réels).
4. Comparatif et procédure de test pour **deux clients** : mode vocal Open WebUI intégré (si l'intégration Whisper/Piper locale est effectivement opérationnelle) et interface vocale JARVIS indépendante. Les deux doivent utiliser une API JARVIS centrale et une mémoire cohérente (mission 13C), pas deux assistants divergents.
5. Checklist de validation : conversation audio complète depuis iPhone en Wi-Fi puis en réseau mobile distant, et depuis macOS ; contrôle des permissions, sécurité, latence, qualité de transcription/réponse et persistance de conversation ; guide de dépannage.

**Dépendances :** mission 13A (Whisper/Piper installés), 13B (chaîne vocale fonctionnelle), 13C (mémoire persistante). Le client distant et sa documentation peuvent être préparés en parallèle ; valider l'intégration réelle avant de déclarer 13E terminée.

**Sécurité :** ne pas exposer directement les API d'administration, Ollama, Whisper ou Piper sur Internet ; privilégier VPN privé et HTTPS, authentification et droits limités. Les commandes à effet sur les serveurs suivent la politique d'autonomie et d'évaluation des risques définie dans cette roadmap.

**Statut : prévu ; aucune validation iPhone/macOS encore constatée.**


> **RAPPEL PRIORITAIRE — décision du 14 octobre 2026 :** à la prochaine reprise des travaux de sécurisation JARVIS, proposer d'attaquer **13D en premier** : inventaire des clés SSH publiques et des accès existants, diagnostic du rejet `Permission denied (publickey)`, vérification des comptes/permissions, Tailscale MacBook ↔ Mac mini, tests de reconnexion/tmux et plan de secours. **Statut : en attente de lancement explicite** ; ne pas modifier les authentifications déjà en place ni lancer d'opérations sensibles sans validation. Faire le lien avec les prérequis de JL-02 et les clients 15A/15B.

## Mission 13D — Accès distant sécurisé SSH / Tailscale (EN ATTENTE)

**Statut au 14 octobre 2026 : EN ATTENTE, non exécutée dans cette séquence.** Cette mission est indépendante de 13E et doit rester visible comme jalon à part entière.

**Objectif :** sécuriser et fiabiliser l'administration distante du Mac mini Debian depuis le MacBook, en préservant les accès existants et en préparant l'administration future du Dell.

**Périmètre prévu :** diagnostiquer l'authentification SSH par clé du compte dédié `adminjarvis`, contrôler les permissions et les clés publiques autorisées sans exposer de clé privée ; vérifier Tailscale sur les deux machines ; employer des clés distinctes par poste ; prévoir `tmux`, reconnexion, tests d'accès et procédure de retour arrière. Ne pas modifier le pare-feu, la configuration SSH ou les accès actifs sans inventaire, sauvegarde et validation adaptée au risque de verrouillage.

**Constat disponible :** le journal de diagnostic précédent montre une connexion TCP au port 22 et une négociation SSH réussies, suivies d'un rejet de la clé publique présentée (`Permission denied (publickey)`). La cause exacte n'est pas encore établie ; l'accès distant opérationnel n'est donc pas validé.

**Critères de réception futurs :** connexion par clé depuis le MacBook via Tailscale ; reprise d'une session `tmux` après déconnexion ; maintien d'un accès de secours ; vérification des permissions, journaux et absence de régression. Conserver des preuves expurgées de secrets.

**Décision :** ne pas intégrer ces changements à la mission 13E. Reprendre 13D par une intervention distincte lorsque l'utilisateur le décide.

## À REPRENDRE SUR INSTRUCTION — Audit et redocumentation des anciennes missions

**Décision du 14 octobre 2026 : tâche différée, non autorisée à l'exécution pour l'instant.** Lors d'un prochain échange, rappeler à l'utilisateur de donner explicitement le feu vert avant de commencer.

**Travail à réaliser après validation :** reprendre toutes les missions historiques de cette roadmap, comparer leurs objectifs, décisions, états, livrables, blocages et preuves avec les discussions JARVIS et les rapports disponibles ; corriger les omissions, donner à chaque mission un titre clairement repérable, distinguer prévu / exécuté / simulé / vérifié, et conserver une chronologie lisible. Ne pas inventer de résultats, signaler les pièces ou échanges manquants et ne pas écraser l'historique sans traçabilité. Documenter dans `ROADMAP.md` et, si nécessaire, dans des rapports de mission dédiés. Exclure secrets et informations sensibles.

**Déclencheur :** instruction explicite de l'utilisateur. **Rappel à programmer séparément** selon la date ou le délai choisi par l'utilisateur.

## Point de synchronisation — 14 octobre 2026 (missions 12 à 13E)

**Convention :** « roadmap » et « feuille de route » désignent ce fichier `ROADMAP.md`, source de référence du suivi. Toute nouvelle mission doit y ajouter son état, ses décisions, ses preuves, ses blocages et sa prochaine étape. Les états historiques ci-dessus restent des instantanés datés et ne doivent pas être lus comme l'état courant.

### État consolidé (selon rapports reçus, sans nouvelle vérification machine)

| Mission | État | Résultat acquis / reste à faire |
| --- | --- | --- |
| 12 — étude voix et mémoire | Terminée : GO sous conditions | faster-whisper small CPU/int8, Piper Tom provisoire, SQLite/FTS5 avec validation explicite ; essais de fichiers et mémoire fictive, pas de microphone réel ni d'intégration complète. |
| 13A — socle vocal durable | Réussie dans son périmètre | Whisper Small et Piper Tom installés dans `/opt/jarvis/voice`, tests synthèse/transcription sur fichiers réussis, isolation CPU et préservation des installations vérifiées ; pas de service résident ni de test micro. |
| 13B — interface vocale | GO PARTIEL (bilan communiqué) | Interface Push-to-Talk, backend vocal et accès Ollama livrés ; microphone physique, navigateur, lecture et interruption audio, HTTP et génération Ollama réels restent à confirmer. |
| 13C — mémoire partagée | GO PARTIEL (bilan communiqué) | SQLite/FTS5, validations explicites, sauvegarde/restauration et scripts livrés ; partage entre trois moteurs testé avec simulations, non prouvé avec trois moteurs réels. |
| **13D — accès distant sécurisé** | **EN ATTENTE — ne pas démarrer avec 13E** | Finaliser SSH par clés, Tailscale Mac mini/MacBook, clés par machine, tmux, reconnexion et retour arrière. Un log SSH antérieur indique connexion TCP et négociation réussies mais rejet de la clé publique : `Permission denied (publickey)`. À diagnostiquer sans modifier l'accès existant à l'aveugle. |
| **13E — intégration vocale réelle** | **À PRÉPARER, NON EXÉCUTÉE** | Tests réels micro/navigateur, STT → Ollama → TTS, lecture/interruption, HTTP local, mémoire validée, persistance et démarrage contrôlé ; tests et critères d'acceptation à définir avant exécution. |

### Ordre et limites décidés

1. Maintenir **13D en attente** ; ne pas y glisser de changements SSH/Tailscale lors de 13E.
2. Préparer **13E comme mission Codex autonome et bornée**, pouvant tourner la nuit, mais sans présumer que les validations nécessitant une personne (micro physique, écoute, approbations) peuvent être obtenues en son absence.
3. Préserver Ollama, Open WebUI, modèles, configurations, conversations et données existantes ; sauvegarde avant modification autorisée, vérification après, aucun effacement ou mise à niveau globale implicite.
4. Distinguer systématiquement **livré**, **testé avec simulation**, **testé réellement** et **validé par l'utilisateur** ; pas de GO complet sans preuves.
5. Conserver une seule autorité de mémoire JARVIS : SQLite/FTS5 via passerelle, avec validation humaine des nouveaux souvenirs ; ne pas activer une seconde mémoire concurrente dans Open WebUI.
6. Dell Precision : chantier distinct, futur serveur d'inférence ; pas de déploiement PXE, RAID ou modification destructive dans 13E. Les règles et décisions Dell détaillées plus haut restent applicables.
7. En fin de mission, produire rapport, résultats, incidents, tests, points en attente et proposition de mise à jour de cette roadmap. Ne publier aucun secret, clé privée, sauvegarde sensible ou journal contenant des données personnelles.

### Prochain jalon

**13E :** rédiger le cahier d'exécution détaillé à remettre à Codex, en commençant par l'inventaire en lecture seule des livrables 13B/13C et la vérification de l'environnement. Autoriser les essais non destructifs automatiques ; laisser en attente les validations humaines et les opérations sensibles. Revenir à 13D séparément.

## Plan opérationnel — 14 octobre 2026

### Mission 13F — Finalisation du Mac mini JARVIS (EN COURS)

**État : EN COURS — mission définie et priorisée, exécution technique non attestée par cette mise à jour.**

**Objectif :** consolider l'assistant JARVIS existant avant de lui confier le déploiement autonome du Dell.

1. Fiabiliser la chaîne vocale réelle (microphone, Whisper, Ollama, Piper Tom), la qualité de transcription et la restitution audio ; mesurer les latences.
2. Améliorer les conversations : réponses orales brèves avec détails écrits, détection de fin de parole, réduction des manipulations Push-to-Talk dans les limites de l'interface actuelle, interruption de la synthèse si faisable.
3. Ajouter une mémoire contextuelle automatique pour consignes et préférences durables non sensibles ; conserver la validation explicite pour les informations sensibles, avec traçabilité, correction et suppression possibles. Vérifier la persistance et le rappel réel.
4. Vérifier la mémoire SQLite/FTS5 commune aux moteurs et éviter les doublons ou statuts contradictoires ; tester sauvegarde et restauration.
5. Préparer et tester les outils agentiques nécessaires à la mission Dell : diagnostic, documentation/recherche, terminal, journalisation, planification, essais isolés et correction itérative. Ne pas confondre capacité annoncée et capacité testée.
6. Vérifier le redémarrage des services et l'absence de régression ; livrer rapport Codex avec preuves et limites.

**Hors périmètre :** mission 13D SSH/Tailscale reportée ; applications natives Apple reportées ; aucune installation ni effacement du Dell pendant 13F.

### Mission 14 — Baptême du feu : déploiement autonome du Dell Precision (PRÉVUE)

**Objectif :** faire réaliser à JARVIS lui-même, et non à Codex, l'installation du Dell Precision 5820 en environnement laboratoire. ChatGPT prépare les consignes, objectifs et critères de réception ; JARVIS diagnostique, planifie, exécute, vérifie et documente ; l'utilisateur supervise.

- Reprendre l'inventaire matériel déjà effectué ; intégrer seulement les dernières informations communiquées par l'utilisateur, sans refaire inutilement l'étude.
- Préparer les prompts d'exécution et le cadre de droits de JARVIS, ainsi que les tests PXE en VM et le plan de récupération.
- Autoriser une autonomie étendue **sur le Dell identifié uniquement** : installation Debian, RAID 1 selon compatibilité vérifiée, pilotes NVIDIA, Ollama et services, avec journalisation et tests.
- Les actions irréversibles (notamment effacement des deux SSD, modification RAID/firmware) nécessitent une autorisation préalable explicite, spécifique à la cible et au périmètre ; une fois cette autorisation accordée, ne pas redemander une confirmation pour chaque commande incluse. Aucun droit implicite sur le Mac mini, les autres machines ou le réseau de production.
- Tester installation, redémarrage, RAID, GPU, services, inférence et capacité de reprise ; documenter les erreurs et corrections autonomes. Ne déclarer la mission validée qu'avec preuves.

**État : PRÉVUE — ne pas lancer avant la réception de 13F et la validation du périmètre destructif.**

### Mission 15 (provisoire) — Applications natives macOS / iPhone (REPORTÉE)

**Objectif :** clients SwiftUI macOS et iOS pour JARVIS, connexion privée via Tailscale, conversation vocale naturelle, interruption vocale et mémoire centrale partagée. macOS : activation vocale envisageable ; iOS : intégration Siri/Raccourcis/bouton Action selon les limitations réelles d'Apple, sans promettre d'écoute permanente en arrière-plan. Conserver l'interface web en secours.

**État : REPORTÉE — à replanifier après stabilisation du Mac mini et déploiement du Dell. Estimation exploratoire : prototype en 3 à 7 jours de développement, à réévaluer.**

**Ordre retenu :** 13F → 14 → 15. La 13D reste en attente indépendante. Les autorisations destructives font partie de la mission 14 et ne constituent pas une mission séparée.


## Décision de pilotage — 14 octobre 2026 : séparation de la mission 15

**État communiqué :** mission **13F finalisée — GO AVEC RÉSERVES**. Les réserves restent à inventorier et à vérifier avant de déclarer validées les fonctions concernées.

La mission 15 est divisée en **deux chantiers indépendants, réalisables en parallèle** :

| Mission | Périmètre | Sous-missions | Dépendances |
| --- | --- | --- | --- |
| **15A — Application macOS** | Application native Mac mini / MacBook | 15A.1 Architecture/UI ; 15A.2 Connexion sécurisée ; 15A.3 Texte, voix et mémoire ; 15A.4 Pilotage agents/missions ; 15A.5 Packaging et validation | API JARVIS et vérification des réserves 13F pertinentes |
| **15B — Application iOS** | Application native iPhone, évolutive iPad | 15B.1 Architecture/UI ; 15B.2 Accès distant sécurisé ; 15B.3 Voix et conversation ; 15B.4 Mémoire, notifications et approbations ; 15B.5 Déploiement/tests/validation | API JARVIS et vérification des réserves 13F pertinentes |
| **14 — Dell Precision** | Second nœud IA et déploiement automatisé | Phases techniques à suivre séparément | **Non bloquante** pour 15A et 15B |

### Architecture cible commune 15A / 15B

- Privilégier **Swift / SwiftUI** avec composants partagés lorsque possible, tout en conservant des expériences adaptées à macOS et iOS.
- Passer par une **API JARVIS versionnée**, indépendante de l'interface et du serveur physique ; ne pas coder en dur le Mac mini.
- Rendre configurable le serveur cible : Mac mini initialement, puis Dell quand la mission 14 sera réellement validée.
- Authentification, transport chiffré, séparation des permissions et approbations explicites pour actions sensibles.
- Définir des contrats communs pour conversation, voix, mémoire, opérations agentiques et statuts, sans présumer que toutes les capacités 13F sont déjà validées.
- Les missions 15A et 15B peuvent progresser **en parallèle** ; elles n'attendent pas le déploiement du Dell. Vérifier les API, la voix et la mémoire concernées par les réserves 13F avant tests d'intégration.

**Statut au 14 octobre 2026 :** cadrage acté, développement et validation de 15A/15B non encore documentés ici. Les anciennes mentions génériques de « mission 15 » désignent désormais le programme commun 15A + 15B.


### Mission 15B — stratégie d'installation iOS (étude du 14 octobre 2026)

Objectif : application native SwiftUI utilisée sur l'iPhone du propriétaire, sans obligation de publication publique sur l'App Store.

| Voie | Conditions | Limites |
| --- | --- | --- |
| Xcode / Personal Team gratuite | Compiler et installer sur son propre iPhone depuis un Mac | Provisioning et installation à renouveler après 7 jours ; limites sur les capacités disponibles |
| Ad Hoc | Apple Developer Program (99 USD/an, prix local variable), appareil enregistré, profil/signature | Nombre d'appareils limité ; renouvellement des profils/certificats selon échéance |
| TestFlight | Apple Developer Program, App Store Connect, installation via TestFlight | Chaque build expire au bout de 90 jours, nouvelle build nécessaire |
| PWA depuis Safari | Application Web hébergée en HTTPS, ajout à l'écran d'accueil | Certaines intégrations iOS natives limitées ; dépend du comportement du navigateur et des permissions |
| Web Distribution UE | Compte développeur, autorisation Apple, notarisation et critères d'éligibilité | Ne pas présumer qu'un développeur particulier est éligible |

**Décision validée — 14 octobre 2026 : solution gratuite pour l'instant.** Développer l'application native SwiftUI et l'installer sur l'iPhone personnel depuis Xcode avec un compte Apple gratuit (Personal Team). Prévoir le renouvellement périodique de la signature/provisioning (généralement 7 jours), sans abonnement Apple Developer à ce stade. Conserver une PWA comme accès de secours si la réinstallation devient contraignante. Ad Hoc et TestFlight restent des pistes ultérieures, non retenues pour la phase actuelle. La compilation/signature est distincte du serveur JARVIS, qui reste accessible via API chiffrée et authentifiée.

Sources Apple : https://developer.apple.com/help/account/basics/about-your-developer-account ; https://help.apple.com/xcode/mac/current/en.lproj/dev7ccaf4d3c.html ; https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/ ; https://developer.apple.com/fr/support/web-distribution-eu/ .


### Exécution Codex — missions 15A et 15B (préparées le 14 octobre 2026)

- [Mission 15A — Cahier Codex macOS](docs/missions/MISSION-15A-MACOS-CODEX.md) : **prêt, non lancé**.
- [Mission 15B — Cahier Codex iOS](docs/missions/MISSION-15B-IOS-CODEX.md) : **prêt, non lancé** ; installation gratuite Xcode / Personal Team.
- Les deux branches peuvent avancer en parallèle, après définition du contrat API partagé et inventaire des réserves 13F. Ne pas modifier les services Mac mini pour lancer ces prototypes.
- **Cette décision remplace** la section historique « Mission 15 (provisoire) — REPORTÉE » et l'ancien ordre « 13F → 14 → 15 ». La mission 14 est indépendante et non bloquante.


### Projet parallèle JL — JARVIS Launcher (14 octobre 2026)

**JL — JARVIS Launcher** est un projet annexe autonome, non bloquant pour les missions JARVIS 13F, 14, 15A et 15B. **JL-01** (lanceur web/macOS de terminaux SSH, Codex et tmux) a été lancé dans Codex par l'utilisateur ; résultat à vérifier. **JL-02** (Qwen/Ollama texte et voix, ChatGPT restant dans sa fenêtre séparée) est une phase ultérieure, non lancée. Toutes les spécifications, étapes et décisions JL sont suivies exclusivement dans la [roadmap dédiée JARVIS Launcher](docs/parallel-projects/JARVIS-Launcher/ROADMAP.md), à transférer au dépôt autonome lorsqu'il sera disponible.


## Priorité impérative de pilotage — décision du 14 octobre 2026 (état courant)

**Décision utilisateur : priorité validée, exécution technique non présumée.** Ce bloc fait autorité pour les prochains arbitrages et remplace les priorités contradictoires des instantanés historiques ci-dessus, sans effacer leur traçabilité.

1. **Mission 13D — sécurité d'abord (jalon bloquant)** : diagnostiquer et valider les accès SSH par clés et Tailscale entre MacBook et Mac mini, le compte dédié et ses permissions, l'accès de secours, les reprises de session et la journalisation. Vérifier les accès sans risquer un verrouillage. **État : à exécuter / à valider**, ne pas confondre la décision de priorité avec un GO technique.
2. **Mission 14A — aptitude agentique de JARVIS (après 13D)** : tester sur un périmètre isolé l'inventaire, la planification, l'exécution par outils autorisés, la recherche documentaire, la détection et correction d'erreurs, la vérification des résultats et la restitution de preuves. Décider GO / GO avec réserves / NO GO sur des essais réels documentés.
3. **Mission 14 — déploiement du Dell Precision par JARVIS (après les validations requises de 13D et 14A)** : JARVIS, et non Codex opérant à sa place, prépare et conduit sous supervision le déploiement Debian / PXE, RAID, NVIDIA / CUDA, Ollama et intégration. Maintenir les garde-fous existants : inventaire matériel et données, sauvegardes et secours, simulation préalable, droits minimaux, autorisation explicite et ciblée pour effacement SSD, RAID/firmware ou modification réseau sensible. Une autorisation couvrant précisément le périmètre expérimental permet l'automatisation des étapes prévues, sans demander confirmation à chaque commande.

**Missions 15A (macOS) et 15B (iOS)** : cahiers déjà préparés, développement indépendant et techniquement parallèle possible, **mais priorité d'exécution inférieure** à 13D → 14A → 14. Ne pas laisser les applications ou les améliorations de l'interface retarder les jalons de sécurité et d'autonomie. **JARVIS Launcher / JL-02** : chantier parallèle ; toute mise en service impliquant des accès ou des commandes distantes doit respecter les validations de sécurité 13D.

**Règle permanente de rappel :** si une prochaine instruction semble inverser cet ordre, rappeler d'abord la séquence **13D → 14A → 14**, ses motifs (sécurité, aptitude démontrée, supervision humaine et protection des données), puis demander seulement si le changement de priorité est bien volontaire lorsqu'il est nécessaire à l'arbitrage. Une modification explicite de la stratégie par l'utilisateur reste possible ; ne jamais présenter la présente décision comme une interdiction absolue.

**Critères de passage :** pas de déploiement distant autorisé sans preuve de l'accès sécurisé et du retour arrière ; pas de GO agentique sans tests ; pas d'opération destructive sur le Dell sans accord ciblé et vérification préalable. Consigner preuves, réserves et décision à chaque jalon.


## Règle permanente obligatoire — synchronisation du suivi des missions (15 octobre 2026)

Le fichier **[SUIVI.md](SUIVI.md)** constitue le **tableau de bord opérationnel unique** des missions : terminées, en cours, préparées, en attente, avec réserves ou non documentées. `ROADMAP.md` garde les décisions, dépendances et intentions détaillées ; `SUIVI.md` est la vue synthétique et actualisée de leur exécution.

**Consigne impérative pour ChatGPT, Codex et toute mise à jour documentaire :**

1. **À chaque modification** d'une mission, d'un état, d'une réserve, d'une preuve, d'un ordre de priorité ou d'une prochaine action dans `ROADMAP.md`, dans une roadmap de sous-projet ou dans un rapport de réception, **mettre à jour `SUIVI.md` dans la même intervention/PR/commit logique**. Réciproquement, toute modification de `SUIVI.md` impliquant une décision nouvelle doit être répercutée dans la roadmap pertinente.
2. **Conserver strictement la présentation** de `SUIVI.md` : titres, sections, tableaux Markdown, ordre et noms des colonnes, ligne de séparation, légende et conventions d'emoji. Ne pas reformater ni remplacer le fichier par une simple liste, un autre modèle de tableau ou un résumé libre.
3. **Conserver les entrées historiques**, y compris les échecs, réserves et GO partiels. Mettre à jour la cellule concernée plutôt que supprimer une ligne ; ajouter de nouvelles lignes pour les étapes ou missions nouvelles. Respecter les identifiants existants.
4. **Ajouter une entrée datée au journal des mises à jour** de `SUIVI.md` pour chaque changement significatif, avec preuve (rapport, PR, commande testée ou confirmation de l'utilisateur). Ne jamais indiquer « validé » sans preuve ni confondre réalisé, simulé, testé et réceptionné.
5. À la fin de chaque mission Codex, inclure expressément la vérification **« ROADMAP ↔ SUIVI synchronisés, format SUIVI conservé »** dans le rapport final. Si la mise à jour ne peut pas être réalisée, déclarer ce point comme réserve explicite, avec correctif proposé.
6. Ne jamais publier des secrets, clés privées, mots de passe, tokens, journaux ou adresses d'infrastructure sensibles dans le suivi.

**Rappel sécurité 13D :** le volet MacBook a été vérifié le 15 octobre (Tailscale, SSH clé et mot de passe, alias, tmux). Cela ne clôt pas encore la mission globale. **Les deux modes SSH restent activés jusqu'à validation explicite d'une stratégie différente et d'un accès de secours fiable.**


### Réévaluation des réserves historiques par les missions ultérieures — 15 octobre 2026

**Décision de consolidation :** une mission ultérieure peut **lever une réserve fonctionnelle** d'une mission précédente seulement si elle apporte une preuve réelle couvrant **le même critère de validation**. Cette règle n'efface jamais le verdict historique (GO PARTIEL, GO sous conditions, etc.) et ne convertit pas automatiquement toute la mission en GO complet.

- Dans [SUIVI.md](SUIVI.md), faire apparaître **le verdict historique** et **l'état technique actuel consolidé**, avec mission probante, portée exacte du test et réserves non levées. Conserver **strictement la mise en page Markdown**, les colonnes, la légende et le journal daté existants.
- La mission **13F** consolide les fonctionnalités des missions **12, 13A, 13B, 13C et partiellement 13E**, ainsi que des vérifications limitées pour **05D, 06, 07**. Voir la section « Consolidations transversales » de `SUIVI.md` et le [débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md).
- Les **tests backend, API et Chromium** de 13F ne prouvent **pas** une validation acoustique physique, Safari/iPhone, un reboot de la machine, l'interopérabilité mémoire Dell ou le déploiement PXE/RAID. Le rapport de réception propre à 13E et les missions 08–11 restent à vérifier, sans verdict inventé.
- À chaque nouvelle mission, vérifier systématiquement si ses preuves lèvent une réserve plus ancienne, mettre à jour les lignes correspondantes de `SUIVI.md` et consigner une entrée datée au journal, sans effacer le constat initial.


### Actualisation 13D — 15 octobre 2026 : GO AVEC RÉSERVES sur les accès

**Décision de suivi actuelle, prévalant sur les mentions historiques « en attente » :** le Mac mini macOS a été confirmé fonctionnel par l'utilisateur sur la base des essais du 14 octobre ; le MacBook a été validé le 15 octobre (Tailscale, SSH clé ED25519 et mot de passe, alias `ssh jarvis`, détachement et reprise tmux). Aucun nouveau test Mac mini n'a été demandé ni réalisé lors de cette actualisation. Selon l'utilisateur, **la configuration SSH du serveur n'a pas été modifiée, hormis l'ajout de la clé publique du MacBook aux clés autorisées**.

**Verdict : 13D — GO AVEC RÉSERVES pour poursuivre vers 14A**, sans modification supplémentaire du serveur. Réserves différées : vérification de la résilience après redémarrage complet, audit ciblé des journaux et validation du secours local avant toute opération à risque. Ces réserves ne doivent pas être présentées comme des validations déjà réalisées.

**Garde-fou impératif :** conserver **les deux modes d'authentification SSH, clé ET mot de passe**, jusqu'à décision expresse après tests sûrs ; pas de désactivation de mot de passe, de changement `sshd_config`, de politique Tailscale ni de reboot à distance tant qu'un accès de récupération local n'est pas garanti. Le suivi détaillé et le journal sont dans [SUIVI.md](SUIVI.md).


### Décision laboratoire — 15 octobre 2026 : tests PXE autonomes en VM

**Correction de l'étape 3 du plan de déploiement :** « Tester l'installation automatisée en VM » est réalisé par **JARVIS sans supervision humaine pendant l'exécution**. En laboratoire isolé et dans un périmètre préautorisé, JARVIS peut créer/recréer les VM et disques virtuels dédiés, lancer les essais UEFI/PXE, observer les erreurs, chercher des solutions, corriger, relancer autant que nécessaire et produire son propre rapport avec preuves. Aucune approbation au cas par cas n'est demandée pour ces opérations réversibles et confinées au laboratoire.

**Ordre cible :** préparer environnement PXE et automatisation/Ansible sur JARVIS → essais VM autonomes non supervisés → démarrage physique du Dell en PXE → installation Debian/RAID dans le périmètre matériel explicitement autorisé → configuration automatique SSH et clé publique JARVIS par l'installateur → premier SSH JARVIS vers Dell → configuration NVIDIA/CUDA/Ollama via Ansible → tests GPU et intégration.

**13D-E n'exige pas de liaison SSH au Dell avant son installation :** la clé publique et la configuration SSH sont injectées par l'installation PXE ; la connexion SSH réelle n'est vérifiable qu'après le premier démarrage Debian. Cette préparation reste à réaliser/tester et ne doit pas être marquée validée à ce stade.

**Frontière de sécurité :** pas de toucher au réseau de production ou aux disques réels du Dell sous couvert de « test VM ». Toute opération destructive sur les deux SSD, RAID/firmware ou réseau réel doit rester bornée par une autorisation préalable spécifique et un plan de récupération ; après autorisation du périmètre, JARVIS exécute les étapes convenues sans supervision commande par commande. Conserver les accès SSH clés **et** mot de passe existants du Mac mini Debian.



## Mission 13D-E — préparation Dell, état au 15 octobre 2026

**Préparation partielle ; NO-GO pour réception complète et lancement de 14A avec cette chaîne.** Audit non destructif réalisé avant toute installation ; aucune installation système effectuée. Inventaires et neuf rôles Ansible, bootstrap SSH invité, templates Debian/iPXE et contrôleur VM TCG borné livrés. Six tests du contrôleur passent ; cela ne valide pas UEFI/PXE, Debian, RAID1 ou l'autonomie du modèle local.

Blocages : QEMU/OVMF/Ansible absents ; KVM inaccessible dans cette session ; réseau/systemd/Docker restreints et DNS shell indisponible. Miroir de paquets isolé, transport SSH invité, second boot disque et superviseur agent durable restent à compléter. NVIDIA/CUDA/Ollama : rôles différés, pas de changement des installations actuelles. Variantes VROC/VMD et mdadm documentées sans décision de partitionnement physique.

Prochaine étape : fournir les prérequis sans altérer l'hôte, compléter la chaîne isolée, réaliser la recette VM et Ansible puis raccorder un worker durable à une copie de 13F. Les essais VM réversibles sont autorisés sans supervision ; les modifications de services sensibles demandent diagnostic et validation ciblée. La démonstration 14A doit provenir du modèle local JARVIS. Aucune intervention Dell, modification SSH/Tailscale/noyau/GRUB, clé, modèle ou SQLite.

Dossier : [réception](docs/missions/13D-E/RAPPORT-FINAL.md), [audit](docs/missions/13D-E/AUDIT.md), [architecture](docs/missions/13D-E/ARCHITECTURE.md), [laboratoire](docs/missions/13D-E/LABORATOIRE.md), [tests](docs/missions/13D-E/TESTS.md). Publication en branche dédiée, aucune fusion automatique.


## Reprise 13D-E — priorité physique, 15 octobre 2026

Cette décision remplace l'obligation préparatoire de reconstruire une chaîne VM complète : progression directe vers la préparation du Dell avec validations ciblées. GO AVEC RÉSERVES pour la préparation, aucun lancement physique autorisé. Outillage réaudité, 16 tests de garde-fous, deux syntax-check Ansible, sources Debian authentifiées, boot TCG et HTTP loopback ciblés. ProxyDHCP/TFTP/HTTP et initrd candidat prêts à être adaptés au plan validé ; aucune activation LAN.

Restent : découverte Dell/SSD/contrôleur et clé publique autorisée, validation humaine réseau, qualification de la recette mdadm et double ESP, autorisation explicite d'effacement/installation, puis premier SSH et idempotence. Les rôles IA et l'intégration agent sont encore différés. Le refus KVM utilisateur n'empêche pas cette préparation physique. 14A reste une preuve d'autonomie distincte, non acquise par ces tests.

Voir [procédure physique](docs/missions/13D-E/DEPLOIEMENT-PHYSIQUE.md), [tests](docs/missions/13D-E/TESTS.md) et [réception](docs/missions/13D-E/RAPPORT-FINAL.md). ROADMAP ↔ SUIVI synchronisés, format SUIVI conservé. Historique NO-GO maintenu sans le présenter comme l'état courant de l'outillage.


## Reprise 13D-E — bootstrap A/B, 16 octobre 2026

PXE UEFI physique jusqu'à Debian Installer confirmé et conservé. Prochaine étape : découverte automatique bloquante, après nouvelle autorisation réseau. Bootstrap temporaire, transition indépendante par clé et orchestration Ansible préparés ; 22 tests + récepteur passent, aucune installation/connexion SSH Dell exécutée. Qualification RAID/double ESP, séries réelles, clé autorisée et approbations d'effacement puis administration restent nécessaires. Aucun composant GPU/IA déclaré opérationnel. Voir [bootstrap automatisé](docs/missions/13D-E/BOOTSTRAP-AUTOMATISE.md), [rapport](docs/missions/13D-E/RAPPORT-FINAL.md) et SUIVI, synchronisés sans modifier les lignes historiques.


### 13D-E — découverte physique reçue, 16 octobre 2026

Rapport transmis automatiquement depuis le Dell et conservé privé ; découverte CPU/RAM/NVMe acquise. Services temporaires arrêtés automatiquement. Installation toujours NO-GO : lecteur SD sans média à qualifier, libellé DMI et écart BIOS à revoir, recette RAID/EFI et autorisations restantes. Aucun effacement ni prise de contrôle SSH effectués.


### 13D-E — installation autonome autorisée, 16 octobre 2026

Le propriétaire autorise réseau nécessaire, effacement des deux NVMe identifiés, installation/reboot et administration ; seule intervention humaine : lancement PXE. Directive prioritaire enregistrée dans AGENTS.md et le prompt de déploiement. Qualification RAID/deux ESP et deux boots UEFI sur disque seul acquise sur images jetables ; 25 tests + récepteur passent. Image réelle et orchestration automatique préparées, aucune installation Dell effectuée à ce stade.


## Jalon du 17 octobre 2026 — clôture de tentative Dell

Debian démarre ; SSH répond, mais authentification, rapport de premier boot et Ansible non réceptionnés. Tentative clôturée sur demande ; mission complémentaire à lancer pour finir, avec conservation du RAID si possible. Référence prioritaire : [rapport transitoire](docs/missions/13D-E/RAPPORT-TRANSITOIRE-REPRISE.md).


## Mission 13D-E / 14 relancée — 17 octobre 2026

Nouvelle chaîne supervisée préparée, services PXE actifs et email de lancement envoyé. Installation physique de cette tentative non encore validée. Voir [réinstallation supervisée](docs/missions/13D-E/REINSTALLATION-SUPERVISEE.md). Objectif continu incluant NVIDIA/CUDA/Ollama/modèles et intégration JARVIS ; aucun nouveau GO intermédiaire.


## Réception nouvelle tentative Dell 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

RÉCEPTION COMPLÈTE VALIDÉE. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.

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


## Réception Mission 13F — 14 octobre 2026

**Statut : GO AVEC RÉSERVES.** Cette réception remplace l'état « EN COURS » du plan ci-dessus sans supprimer les décisions historiques. Installation et tests réellement exécutés sur le Mac mini ; aucune installation Dell.

- Voix : AudioWorklet/VAD léger, fin sur silence, deux échanges successifs et interruption vocale testés avec microphone WAV artificiel. Push-to-Talk conservé. Acoustique humaine/écho/bruit et Safari/iPhone/macOS physiques restent à valider.
- Réponse écrite détaillée et synthèse orale séparée, longueur persistante, détails supplémentaires pour un seul tour.
- SQLite/FTS5 canonique v3 : préférences et habitudes non sensibles du catalogue enregistrées automatiquement, remplacements/suppressions/audit transactionnels. Validation conservée hors périmètre automatique. Rappel réel par Qwen, Ministral et Llama ; sauvegarde/restauration/restart vérifiés.
- Outils et laboratoire : diagnostics réels, journaux propres, recherche et lecture HTTPS, terminal Bubblewrap sans données personnelles, réseau hôte ou droits administrateur. Qwen sélectionne ses commandes, corrige des services HTTP isolés, reprend après échec et vérifie HTTP 200. Dernier essai : 17 appels, 125,51 secondes, deux documents officiels distincts effectivement lus.
- 27 tests backend passent ; 8 contrôles API réels, 8 contrôles navigateur (dont silence simulé et viewport mobile émulé), 6 contrôles finaux. Données initiales identiques : 2 conversations, 14 messages, 1 souvenir. Ollama/WebUI préservés.
- Réserves : VAD acoustique physique, catalogue mémoire limité, interprétations parfois approximatives du modèle, journaux Unix restreints, aucune validation VM UEFI/PXE/RAID/Dell ni reprise de mission longue après reboot.

Rapports : [réception](rapports/MISSION-13F-RAPPORT.md), [tests](rapports/MISSION-13F-TESTS.md), [installation](rapports/MISSION-13F-INSTALLATION.md), [architecture](rapports/MISSION-13F-ARCHITECTURE.md), [incidents](rapports/MISSION-13F-INCIDENTS.md), [utilisation](rapports/MISSION-13F-UTILISATION.md), [reprise](rapports/MISSION-13F-REPRISE.md). Code et templates sans configuration privée sous conversation/. Preuves publiques limitées à un résumé expurgé ; bases, journaux détaillés, identifiants, poids et sauvegardes exclus.

**Préparation de 14 : aptitude démontrée à raisonner et agir dans un laboratoire borné, pas encore à installer le Dell avec les droits actuels.** Prévoir transport/exécution ciblés, outils PXE/Ansible, VM UEFI et snapshots, contrôleur de mission persistant et autorisation du périmètre destructif sur les deux NVMe FlexBay précisément identifiés. Reprendre l'étude déjà effectuée : RAID 1 Intel VROC/VMD en priorité si compatible et fiable sous Debian 13, repli mdadm après vérification. La mission 14 sera réalisée par JARVIS, pas par Codex. Aucun PXE, RAID, firmware ni disque Dell modifié.

13D reste **EN ATTENTE** ; 14 **NON DÉMARRÉE** ; 15 **REPORTÉE**. Publication via branche et PR dédiée, validation humaine avant fusion selon le workflow existant.


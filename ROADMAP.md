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

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

# Incidents et blocages

| ID | Observation | Traitement | État |
| --- | --- | --- | --- |
| E01 | netlink, systemd, socket Docker refusés | Audit limité aux fichiers/paquets ; aucun contournement des permissions | Diagnostic hôte complet différé |
| E02 | /dev/kvm et QEMU/OVMF absents | TCG proposé sans toucher au noyau ; aucun lancement possible ici | Bloquant VM |
| E03 | Ansible, pip, ensurepip et PyYAML absents | Rôles/templates produits ; contrôle syntaxique Ansible impossible | Bloquant exécution Ansible |
| E04 | DNS shell : deb.debian.org non résolu | Documentation lue via outil web ; aucun téléchargement binaire ni installation système | Bloquant acquisition des outils |
| E05 | .git racine vide et protégée ; authentification gh locale indisponible | Pas de modification de .git ; connecteur GitHub et branche dédiée | Publication séparée |
| E06 | Laboratoire 13F 25 s / 128 Mio, réseau interdit | Contrôleur séparé proposé ; aucune modification du service actif | Intégration agent différée |
| E07 | SLIRP restreint bloque miroir et SSH entrant | Maintien de l'isolation ; miroir hors ligne et transport contrôlé à implémenter | Bloquant installation complète |
| E08 | Aucune clé de déploiement publique accessible | Ne pas générer ni lire de clé privée ; sélection future d'un signataire existant | Bloquant bootstrap réel |
| E09 | Pas de recette RAID1 UEFI validée | Variantes comparées ; pas de partitionnement Dell généré à l'aveugle | Validation matérielle future |

Aucun incident de service provoqué observé ; l'état de santé hôte n'est pas accessible dans cette session et ne peut être certifié.

## Actualisation reprise physique — 15 octobre 2026

E01 : visibilité réseau/systemd rétablie pour cet audit. E02 : QEMU/OVMF disponibles et TCG démarré ; accès KVM encore refusé mais non bloquant. E03 : Ansible disponible, deux syntax-check réussis ; idempotence sur cible toujours non démontrée. E04 : DNS/HTTPS fonctionnent, fichiers Debian récupérés et authentifiés. E05 : dépôt retrouvé dans JARVIS-Documentation, worktree dédié créé sur la branche demandée ; modifications et archives tierces conservées. E07 : transport HTTP loopback testé ; aucune boucle d'installation distante prétendue validée. E08 : clé réelle de déploiement non sélectionnée. E09 : recette mdadm candidate fournie, qualification double ESP/boot/panne encore nécessaire. E06 et démonstration agent 14A restent hors du périmètre physique préparatoire actuel.

Nouveau constat : le garde-fou physique refuse l'hôte Apple et l'inventaire Ansible Dell livré échoue localement avant connexion. Les refus sont attendus, pas des incidents de production. Aucun ProxyDHCP ni TFTP n'a été démarré. Le seul HTTP d'essai était sur loopback et a été arrêté automatiquement.

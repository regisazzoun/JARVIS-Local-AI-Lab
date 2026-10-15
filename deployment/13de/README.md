# 13D-E — préparation, non opérationnelle

Voir [rapport de réception](../../docs/missions/13D-E/RAPPORT-FINAL.md) et [laboratoire](../../docs/missions/13D-E/LABORATOIRE.md) avant utilisation.

`python3 -m unittest discover -s deployment/13de/tests -v` depuis la racine du dépôt.

Le worker refuse les actifs absents ; aucune installation ni activation automatique. Inventaire Dell désactivé. Ne pas appliquer les templates laboratoire au matériel physique. Les rôles NVIDIA/CUDA/Ollama signalent des étapes différées.

## Reprise physique

Consulter [la procédure complète](../../docs/missions/13D-E/DEPLOIEMENT-PHYSIQUE.md). Les nouveaux templates sont inactifs. `physical/` découvre et compare les identités, construit un initrd candidat sans approbation d'effacement. `ansible/dell.yml` refuse l'inventaire livré avant connexion. `debian/preseed-dell.candidate.cfg` doit être qualifié avant toute utilisation autorisée. Aucun lancement physique ni service LAN implicitement autorisé.

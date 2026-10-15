# 13D-E — préparation, non opérationnelle

Voir [rapport de réception](../../docs/missions/13D-E/RAPPORT-FINAL.md) et [laboratoire](../../docs/missions/13D-E/LABORATOIRE.md) avant utilisation.

`python3 -m unittest discover -s deployment/13de/tests -v` depuis la racine du dépôt.

Le worker refuse les actifs absents ; aucune installation ni activation automatique. Inventaire Dell désactivé. Ne pas appliquer les templates laboratoire au matériel physique. Les rôles NVIDIA/CUDA/Ollama signalent des étapes différées.

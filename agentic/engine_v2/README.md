# JARVIS Agentic Engine V2 — mission22

Copie versionnée du backend canonique avec améliorations ciblées. Le moteur réutilise Core, Registry, Ollama, le broker privilégié et la mémoire SQLite/FTS5 existants.

Tests : `PYTHONPATH=agentic/engine_v2 python3 -m unittest discover -s agentic/engine_v2/tests -v` depuis la racine du dépôt. Les tests simulés ne réceptionnent pas l'autonomie. Voir docs/missions/22 pour les essais réels et réserves.

Déploiement opérateur : `sudo python3 agentic/engine_v2/install.py`. Sauvegardes privées cohérentes de SQLite et des modules sous /var/backups/jarvis/mission22. Configuration, secrets, modèles et politique de droits ne sont pas remplacés. Le broker livré est installé séparément après compilation et contrôles de frontières.

API : /api/missions soumet une mission persistante ; /api/chat agent_mode=true renvoie202 et mission_id ; une mutation décidée en chat ordinaire est transférée avant exécution au worker. Les appels JSON et l'authentification existants restent requis. Le Launcher sélectionne mission_id et lit le journal SQLite.

Migration additive : anciennes missions et états interrompus conservés. Les baux expirés V2 sont repris automatiquement ; ne pas rejouer aveuglément une intention sans résultat. Une panne entre l'effet externe et son résultat enregistré reste une fenêtre d'incertitude : le modèle doit réobserver la cible. Il n'y a pas de garantie universelle exactly-once sur une commande shell arbitraire.

## Prérequis permanent avant une extension du moteur ou des connecteurs

Lire [AGENTS](../../AGENTS.md), la [charte](../../docs/CHARTE_DIRECTIVES_JARVIS.md), les états pertinents et les [prérequis de réutilisation](../../docs/PREREQUIS-REUTILISATION.md). Inventorier le moteur, le broker, le registre, les Skills, MCP et le code JARVIS déjà développé ; rechercher et comparer les bibliothèques/API/connecteurs/solutions open source existants. Réutiliser, configurer, raccorder et tester avant de coder. Tout complément doit être limité à un manque démontré et documenté avec sources, comparatif et preuves dans la mission et la PR, sans nouvelle validation humaine intermédiaire.

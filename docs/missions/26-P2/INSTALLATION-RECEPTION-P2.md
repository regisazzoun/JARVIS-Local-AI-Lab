# Installation et utilisation — réception ciblée P2

Branche `codex/mission-26-phase2-boucles-contexte-code-reel`, base Phase1/PR28, PR29. Références exactes des sept fichiers dans [VERIFICATION-SOURCES.json](reception/VERIFICATION-SOURCES.json) ; les versions intermédiaires ne sont pas la dernière installation.

Modules sous `/opt/jarvis/conversation/jarvis`, venv existant. Workers `jarvis-mission-worker.service` et `jarvis-mission-worker@2.service` rechargés ; serveur conversation et JL03 conservés. Copies de sources et nouveaux tests sous `/opt/jarvis-lab/mission26-phase2/engine/jarvis` et `reception` sur chacun des Dell.

Les outils P2 sont opt-in, dans la mission native existante `3aa717f3887e49daa7daf7e883ee52e4`. `control.py` transmet un seul scénario propriétaire ; JARVIS décide commandes et exécuteur. `receive.py` est le contrôleur indépendant Codex. **Ne pas rejouer les scénarios déjà reçus** : leurs problèmes, compteurs et fichiers sont persistants. Pour une nouvelle campagne autorisée, préparer une identité de problème propre sans réutiliser artificiellement un problème escaladé.

Les faux négatifs de transport sont des canaux Unix temporaires qui transmettent une vraie requête au broker existant, puis ferment leur écoute ou perdent réellement sa réponse. Aucun résultat de broker n’est simulé. Les fichiers privés et marqueurs distants ne sont pas supprimés.

Retour arrière : sauvegardes originales dans `/home/adminjarvis/JARVIS/mission26-phase2-private/before-reception-install/`. Suspendre cette mission, désactiver son opt-in, restaurer les quatre modules originaux modifiés (`mission_store`, `host_client`, `tools`, `durable_cycle`) avant de recharger les deux workers. Les trois nouveaux modules peuvent rester inactifs. Ne pas supprimer SQLite, les deux tables additives, les reçus ou les données existantes. Un retour arrière n’est pas une réception de P4.

La réception termine uniquement la supervision des dix cas : entréeP2 déplacée vers `received_tasks` dans le registre runtime, liste `tasks` vide. Timer maintenu, aucune ancienne mission JL03 relancée. La mission native reste en revue d’intégration, sans clôture artificielle des anciennes tâches. P3/P4 non transmises.

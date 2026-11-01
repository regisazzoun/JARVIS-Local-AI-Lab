# Socle standard WebUI / Qwen Code

Configuration native uniquement : Open WebUI0.12.0, MCPO0.0.20 avec versions du verrou amont v0.0.20, Open Terminal0.14.7, Qwen Code0.26.4 extrait de son archive npm officielle vérifiée, sans modification de ses sources.

Les exemples ne contiennent pas de jeton. `QWEN_HOME` désigne un répertoire dédié ; le provider local utilise une clé factice `ollama` via `JARVIS_LOCAL_OLLAMA_KEY`. Le profil Ollama standard32k est un alias de paramètres partageant les poids Coder existants. Aucun téléchargement de modèle.

`mcp-config.example.json` réutilise le connecteur JARVIS existant pour Google personnel/Éducation, GitHub, SSH, Ansible et Skills ; son outil de création de missions maison est exclu de ce parcours. Ce connecteur reste du code spécifique JARVIS, contrairement au pilotage de l’agent. Le seul changement de source ici aligne `jarvis_call.arguments` sur un objet structuré ; les anciennes chaînes JSON restent acceptées.

MCPO transforme ce serveur stdio en serveur OpenAPI déclaré dans les intégrations natives WebUI. Open Terminal se déclare dans la section Terminal dédiée. Dans le chat, sélectionner ce terminal avec le bouton nuage. `qwen-standard` lance le CLI amont avec le provider local, la configuration MCP et l’autorisation propriétaire déjà accordée. Aucun prompt d’identité, résumé ou moteur de rapports ajouté. Les processus longs se suivent par les outils natifs Open Terminal.

Les clés des deux services restent dans des fichiers privés. Ne jamais copier les unités runtime contenant une clé dans le dépôt. Préserver toutes les autres intégrations et restaurer les réglages sauvegardés pour revenir en arrière ; aucune base historique à restaurer ou effacer.

Voir `docs/missions/WEBUI-SOCLE-STANDARD/` pour la réception et ses réserves.

## Persistance après redémarrage

Le déploiement historique utilisait `ENABLE_PERSISTENT_CONFIG=false`, ce qui perdait les réglages API au redémarrage. La source Compose active utilise désormais `true`. Le fichier `compose.override.example.yaml` montre la surcharge native sans clé ; conserver le volume de données et tous les autres paramètres de la base Compose. Les connexions natives et profils ont été réappliqués par leurs API standard, puis un redémarrage du seul conteneur a confirmé leur conservation. Aucun script de réapplication au démarrage ajouté.

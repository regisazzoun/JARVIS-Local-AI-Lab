# Inventaire avant installation

Le composant PR35 `jarvis/google_workspace.py` est un client REST local, pas un serveur tiers fourni avec son OAuth applicatif. Il utilise google-auth2.62.0 et google-auth-oauthlib1.5.0 et attend un client OAuth dans `google-connect --client-file`. Le stockage prévu est ~/.config/jarvis/google/<profil>/token.json, renouvellement verrouillé par profil. Aucun de ces profils n’était présent lors de l’inventaire ; aucune réutilisation de jeton n’est revendiquée.

Le MCP canonique historique expose huit outils ; le transport client de PR35 expose six interfaces de catalogue/appel/mission/reçu, avec façade vers34capacités. Open WebUI et Qwen Code y sont réellement raccordés selon PR35, sans nouvelle mémoire. Le nouvel outil doit s’y ajouter, pas les reconstruire.

Aucun rclone, gcloud, gws ou gog n’a été trouvé sur le PATH contrôlé. Les emplacements usuels de configuration n’ont pas fourni d’identifiant applicatif Google utilisable pour cette mission. Les accès Google éventuellement liés à Codex ne sont pas exportés vers JARVIS.

Le lanceur Code utilise son Node22 dédié ; /usr/bin/node20.19.2, déjà installé, suffit au serveur Workspace ciblé. Le runtime canonique, ses bases et ses services sont conservés. Les sauvegardes avant modification sont privées sous google-mcp-oauth-private/runtime-before/ ; les ajouts historiques du tools.py installé ont été préservés par édition ciblée.

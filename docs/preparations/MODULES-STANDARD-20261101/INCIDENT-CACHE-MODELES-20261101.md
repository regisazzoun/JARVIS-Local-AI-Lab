# Incident observé — cache modèles vidé pendant un appel d’outil

Date : 1 novembre 2026. Chat concerné : https://jarvis-macmini.tail805e83.ts.net/c/3fe169c8-1505-4d34-a89b-6886aea96d00 ; tour assistant 74e2d26a-3489-4e75-92d3-8e3fd73d7093. Demande propriétaire : regarder les Skills disponibles, via parcours vocal LiveKit délégué à WebUI. Analyse des preuves existantes uniquement, aucun nouvel essai fonctionnel.

## Preuves ciblées

Horaires des journaux en UTC (heure de Paris : ajouter une heure).

- 16:09:42.995 : POST /api/chat/completions accepté, profil jarvis-qwen-code-lab.
- 16:09:43.683 : POST /ollama/config/update accepté, pendant cette génération.
- Le code installé /app/backend/open_webui/routers/ollama.py, clear_models_cache, vide BASE_MODELS, OLLAMA_MODELS et MODELS lors de la mise à jour.
- Le tour enregistré contient exactement un list_files sur /home/adminjarvis/JARVIS/qwen-code-projects/.agents/skills, status completed, suivi d’un function_call_output réussi contenant les 18 dossiers attendus. Aucun refus d’autorisation ni erreur de transport terminal dans ce résultat.
- 16:09:55.506 : open_webui.utils.middleware.response_handler signale « Tool-call continuation failed: Model not found ».
- La trace situe l’échec dans utils/chat.py:193, après models.get(model_id), quand l’entrée n’est pas trouvée dans request.app.state.MODELS. Cette voie ne recharge pas le catalogue avant de lever cette exception.
- 16:09:55.570 : main.process_chat restitue « Model '' was not found » au chat.

Le nom vide dans ce message est un libellé générique ; il ne démontre pas un identifiant vide. La première interprétation « modèle perdu/vide » est donc rectifiée. Les faits établissent une invalidation concurrente du cache et une continuation sans résolution de modèle ; aucun acteur humain ou agent précis n’est attribué à la sauvegarde d’après les seuls chemins HTTP.

## État et récupération

Les configurations persistées restent correctes : jarvis-qwen-code-lab est actif et pointe vers qwen3-coder-next:jarvis-standard-32k ; appels native et contexte32768 conservés. Le profil Conversation reste présent.

Le catalogue a été rechargé par GET /api/models, voie native qui reconstruit MODELS. La réponse contient le profil expérimental, son modèle de base et le profil Conversation. Aucun changement de profil, réinstallation, code runtime, redémarrage ou reprise de mission n’a été effectué. Le chat d’erreur et ses preuves restent inchangés.

**Limite : pas de nouvelle génération, aucun appel d’outil de test, aucun retest vocal.** Le cache est reconstitué mais la poursuite après outil n’est pas déclarée reçue après récupération.

## À suivre

- Éviter les modifications de connexions modèles pendant un échange comportant des outils ; une page de réglages peut invalider le cache utilisé par une requête en cours.
- Avant production, vérifier dans un environnement dédié la gestion d’une invalidation concurrente et le rechargement du catalogue à la continuation ; préférer une correction amont standard si nécessaire.
- Lors d’un futur essai autorisé, vérifier la découverte native des Skills et la réponse finale. Cette observation prouve uniquement la lecture effective des 18 répertoires, pas la lecture de chaque SKILL.md ni l’exécution des scripts.

Suivi : issue42, PR43. Les raccordements des machines du lycée restent distincts. Aucune modification des missions/services et aucun test supplémentaire effectué par ce diagnostic.

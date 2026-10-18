# Mission 22 — moteur durable V2

Développement Codex, exécution des essais par Qwen via le broker réel. La mémoire personnelle demeure SQLite/FTS5 canonique ; la base missions existante porte exclusivement l'état technique.

Une mission possède un identifiant, un objectif, un modèle, une conversation et un graphe de tâches. Le worker prend un bail transactionnel, renouvelle son signal de vie et conserve un quantum d'inférence. Chaque outil reçoit une intention persistante avant exécution et un résultat immédiatement après. Le journal conserve les arguments, la durée, l'exécutant et la référence de preuve ; un état started sans résultat ne vaut jamais réussite.

Les échanges assistant/outils et les notes de travail survivent aux cycles. À saturation du contexte, les observations intégrales restent consultables par identifiant et pagination. Une limite de génération rend la main au planificateur ; elle ne clôture pas la mission. Les tâches déjà validées ne sont pas replanifiées.

Une tâche dépend de ses prédécesseurs. Sa réception exige un rapport local relu indépendamment par le broker et une preuve issue de cette tâche. Les contrats peuvent exiger des outils précis. La validation documentaire n'est pas une preuve universelle de qualité sémantique : les scénarios de réception doivent aussi préciser leurs assertions fonctionnelles.

La publication utilise une outbox persistante : lecture locale, empreinte SHA256, checkpoint, push, relecture GitHub et comparaison du contenu. Une panne GitHub conserve le livrable et reporte la livraison. Les publications sont attribuées à l'automatisation du moteur, pas à un appel du modèle si celui-ci ne les a pas lui-même déclenchées.

Le Launcher lit le journal SQLite et conserve le lecteur historique pour les anciennes missions. Les événements Codex restent séparés. Aucune seconde mémoire, aucun accès du modèle aux clés privées, aucune réinstallation du Dell.


## Dépendances externes et provenance des sources

L’état `waiting_external` conserve le plan et les rapports sans relancer des générations identiques face à un enrôlement absent. `mission_block` exige une observation effective de la tâche et une relecture indépendante du rapport, publie ce rapport par l’outbox et ne crée aucune validation fonctionnelle. Une reprise remet la même mission en file et réutilise les tâches déjà reçues. Les erreurs de transport et les fins de quantum conservent leurs reprises automatiques.

Les contrats peuvent vérifier des champs du résultat réel, notamment `github_path`, pour distinguer le document demandé du document réellement obtenu. Les téléchargements sont des mutations locales autorisées, exécutées sous l’identité technique et relues intégralement. Aucun jeton GitHub ou Tailscale n’est transmis au modèle.

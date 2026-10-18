# Intégration JL-02 — mission 22

La branche Launcher2 codex/mission22-agentic-engine-v2 conserve la mise en page et ses défilements internes. Elle raccorde conversation et identifiant durable, remet le curseur d'événements à zéro lors d'un changement et transmet le contexte conversationnel aux missions.

Le backend expose les événements SQLite : intention, résultat, tâches vérifiées, checkpoints, erreurs de cycle et publications. Les acteurs JARVIS, JARVIS-engine et Codex restent distincts. Les journaux historiques restent accessibles par leur ancien mécanisme.

La migration des sessions ajoute seulement des empreintes et dates d'expiration à la base canonique. Les anciens cookies stockés uniquement dans la RAM de l'ancien processus ne peuvent être récupérés par l'API existante : une reconnexion peut être nécessaire au premier redémarrage. Les sessions créées ensuite doivent survivre aux redémarrages et rester révocables.

Déploiement et contrôle connecté : en cours ; aucun affichage navigateur réel n'est encore déclaré reçu pour V2.

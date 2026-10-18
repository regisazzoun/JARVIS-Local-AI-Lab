# Intégration JL-02 — mission 22

La branche Launcher2 codex/mission22-agentic-engine-v2 conserve la mise en page et ses défilements internes. Elle raccorde conversation et identifiant durable, remet le curseur d'événements à zéro lors d'un changement et transmet le contexte conversationnel aux missions.

Le backend expose les événements SQLite : intention, résultat, tâches vérifiées, checkpoints, erreurs de cycle et publications. Les acteurs JARVIS, JARVIS-engine et Codex restent distincts. Les journaux historiques restent accessibles par leur ancien mécanisme.

La migration des sessions ajoute seulement des empreintes et dates d'expiration à la base canonique. Les anciens cookies stockés uniquement dans la RAM de l'ancien processus ne peuvent être récupérés par l'API existante : une reconnexion peut être nécessaire au premier redémarrage. Les sessions créées ensuite doivent survivre aux redémarrages et rester révocables.

Déploiement et contrôle connecté : en cours ; aucun affichage navigateur réel n'est encore déclaré reçu pour V2.


## Déploiement et observation

Passerelle V2 réellement déployée avec sauvegardes privées SQLite cohérentes.14 contrôles Chromium connectés ont réussi ; les événements provenaient du journal de la mission réelle310306c2…, pas de réponses simulées. Les débuts d'outils et événements de moteur sont neutres, pas affichés comme échecs.

La conversation finale est conservée dans les messages/FTS canoniques avec identifiant de mission et dédoublonnage. Le Launcher recharge cette conversation après achèvement lorsqu'elle est déjà ouverte. Les opérations de coordination Codex restent identifiées dans les événements, y compris les corrections d'infrastructure.


### Contrôle de finalisation

Le navigateur Chromium connecté à la passerelle canonique a effectivement affiché la mission21, sept tâches et six coches de réception.17 assertions passent, dont la présence réelle d’événements neutres, l’attribution JARVIS et les ascenseurs internes sur trois dimensions. La progression compte des tâches reçues ; elle ne mesure pas un pourcentage de durée restante. L’attente externe, la reprise et la publication sont explicitement distinguées dans l’interface. Les échecs de commande restent visibles et ne deviennent pas des coches.

Les rapports JSON de réception sont disponibles dans ce dossier ; aucune capture privée contenant des données du laboratoire n’est publiée. Les tests physiques de microphone/MacBook et le client VNC externe restent hors des preuves disponibles.

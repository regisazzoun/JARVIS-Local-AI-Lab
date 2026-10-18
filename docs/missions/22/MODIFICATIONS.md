# Modifications — mission 22

État de travail : développement et réception en cours ; ne pas assimiler ce document à une réception finale.

- `mission_store.py` : migration additive, transactions, graphe, journal d'intentions/résultats, baux, événements et outbox.
- `missions.py` : worker durable, reprise sans plafond de cinq tentatives, publication asynchrone et interruption coopérative.
- `durable_cycle.py` : modèle local réel, contexte de travail persistant, réutilisation des preuves, détection des mêmes échecs, rapport final après validation des tâches.
- `durable_tools.py` : plan typé, lecture paginée des preuves, notes, vérification des rapports et réception des tâches, livraison GitHub.
- `server.py`, `core.py`, `tools.py` : demandes agentiques asynchrones ; promotion d'une opération conversationnelle vers une mission avant son effet ; préservation du chat et de la voix.
- `launcher_api.py` : événements durables et attribution explicite.
- `auth.py` : empreintes des sessions persistantes ; aucune conservation des jetons en clair dans la base. Les sessions de l'ancien processus, uniquement en RAM, ne peuvent pas être migrées par l'API existante.
- `memory.py` : éviter la réindexation d'un document inchangé dans la mémoire canonique.
- Broker : lecture GitHub distinguant fichiers/dossiers, lecture locale sans ajout artificiel de saut de ligne, copie Ansible idempotente, retrait des ulimit CPU/processus historiques du terminal hôte. Les masques de secrets, chemins autorisés et contrôles d'identité restent actifs.

Les premières itérations de réception ont révélé la perte de l'échange courant entre cycles, puis un contexte insuffisant. Ces défauts sont consignés ; les premiers essais ne seront pas comptés comme réussis.

## Corrections issues des essais réels

La réception de production a terminé trois tâches (30 appels,27 retours réussis,7 cycles), avec livraison et relecture distante des rapports. Codex est intervenu sur l'infrastructure de publication ; ce scénario n'est pas présenté comme une exécution sans correction de l'infrastructure.

Le broker créait les nouveaux parents de fichiers sous son umask privé : Git exécuté comme identité technique ne pouvait pas les traverser. La propriété et les modes des seuls dossiers du clone temporaire sont corrigés. Les rapports locaux ont été conservés et livrés par l'outbox.

Un rapport modèle contenait une adresse privée non secrète malgré la consigne. Codex a expurgé sa version courante, puis un filtre automatique a été ajouté pour les nouvelles livraisons ; les anciens commits de la branche de preuve conservent l'historique. Aucune clé ou mot de passe n'a été retrouvé dans ces rapports.

Mission21 a révélé un contrat trop lié à un nom d'outil : host_logs avait fourni les journaux, tandis que service_logs était exigé. Les deux sources équivalentes sont acceptées ; les suffixes .service sont normalisés. Les résultats satisfaisant chaque condition sont désormais épinglés dans le contexte avec leurs identifiants, au lieu de disparaître derrière les dernières lectures répétées. Ce défaut et les nombreuses relectures initiales ne sont pas masqués par un taux de retours réussis.

Le shell hôte est confiné et ne possède pas le bus systemd ni les périphériques réels. Des diagnostics structurés root en lecture seule permettent de consulter unités en échec et journaux système sans passer par ce shell. Les descriptions expliquent cette différence.

Le worker possède maintenant son propre Core/Registry/verrou et partage uniquement la mémoire canonique : chat et STT/TTS restent utilisables pendant une mission. Routage logique : échanges interactifs sur GPU Mac mini, missions sur GPU Dell1, repli entre les deux nœuds en cas d'erreur de transport. Les URL restent privées.

Après acquisition du verrou de processus canonique, le serveur peut reprendre immédiatement ses anciennes lignes running V2 ; la récupération par bail demeure utile pour les workers sans cette preuve d'exclusivité. Les états interrompus et missions historiques ne sont pas relancés.


## Finalisation du 18 octobre — corrections supplémentaires

- Codex a corrigé `host_github file` : l’argument `file` n’est plus ignoré au profit implicite de README ; des arguments path/file contradictoires sont rejetés. Les résultats identifient le chemin réellement lu. Les contrats peuvent contrôler ces métadonnées.
- `host_github download` conserve un fichier complet jusqu’à 1Mo dans un chemin autorisé, par fragments exécutés sous l’identité technique puis relecture intégrale et empreinte. La première version limitée à60Ko a refusé ROADMAP ; la limite a été corrigée sans tronquer la source. Les téléchargements restent exclus des lots de lectures, car ils écrivent un fichier.
- Les événements historiques aux champs JSON nuls sont désormais lisibles. Une intervention Codex avait ajouté un événement sans arguments, déclenchant une erreur de cycle ; la compatibilité est corrigée et testée, sans supprimer les événements.
- Deux opérations fixes `tailscale_configure` et `tailscale_status` ont été raccordées au profil Dell gardé. Le modèle a effectivement appelé l’installation : client installé et service activé, mais `NeedsLogin`. Aucun état Tailscale Mac copié. Les données d’enrôlement restent privées sur Dell.
- `mission_block` permet au modèle de conserver un rapport vérifié et publié sur une dépendance externe réelle, sans clôturer la tâche. L’état `waiting_external` n’est pas repris en boucle ; les tâches reçues restent intactes et la reprise conserve le plan. Les erreurs récupérables gardent leur reprise automatique existante.
- Le Launcher distingue attente externe, reprise, publication et interruption ; son bouton de reprise conserve les checkpoints. Le script Launcher installe uniquement les actifs et ne rétablit plus l’ancien backend.

Les installations et modifications de tâches21 ne sont pas attribuées à Codex : les commandes de développement, de déploiement du broker et de vérification indépendante sont Codex ; les appels au broker et rapports modèle sont JARVIS. Les interventions pendant cette réception empêchent de présenter cette exécution comme entièrement sans correction d’infrastructure.


### Contexte volumineux et progression de fin de tâche

La trace réelle montrait une réponse d’outil de101479 caractères (lot de lectures) avec un contexte durable16384 : le tour suivant compactait immédiatement les échanges. Cette perte des détails immédiats contribue probablement aux relectures ; elle ne prouve pas à elle seule la cause de toutes les répétitions. Le moteur conserve désormais le reçu intégral dans SQLite et n’envoie au modèle qu’une vue explicitement tronquée, avec début/fin, taille intégrale et identifiant de preuve. `mission_evidence` permet la lecture paginée. Aucun résultat d’outil stocké n’est remplacé par cet extrait.

Le contexte durable est porté à32768, sans plafond de tokens de génération, en vérifiant le chargement GPU réel. Les instructions actives sont relues à chaque génération, plutôt que figées pendant un quantum entier. L’objectif07 accumulé a été consolidé par Codex en actions restantes, sans toucher aux six tâches reçues ; l’ancien texte est sauvegardé et son empreinte journalisée.

Les téléchargements identiques sont maintenant réellement idempotents : relecture exacte, `changed=false`, aucune réécriture. Ils ne réinitialisent plus la détection de répétition comme s’ils avaient changé l’état du système.29 tests V2 passent après ces corrections ; la réception de mission longue conserve ses réserves tant que le modèle n’a pas clôturé ses résultats.


### Préservation documentaire et erreurs de publication

Après amélioration du contexte, JARVIS a bien rédigé ses bilans mais a remplacé localement les deux documents racine par des résumés propres à21, malgré la consigne de conserver les autres missions. Codex a identifié cette non-conformité. Le broker refuse désormais cette publication sur la branche21 si le document existant n’est pas conservé ; l’expurgation d’identifiants privés reste permise. Les documents GitHub originaux ont été vérifiés intacts après les refus. Cette protection matérialise la consigne du propriétaire, sans nouvelle validation humaine.

Un rejet nécessitant une révision locale devient `needs_revision`, sans boucle de push identiques ; les erreurs réseau conservent leur reprise. Une nouvelle version remplace l’intention rejetée. Les problèmes de livraison sont injectés dans le contexte actif du modèle. `mission_block` refuse de masquer une publication corrigeable derrière une dépendance d’authentification externe.

Autre erreur corrigée après essai réel : `mission_block` et `mission_evidence` acceptaient seulement l’identifiant d’invocation interne, alors que le modèle utilisait l’identifiant du reçu broker. Les deux références réelles sont maintenant résolues dans la même mission/tâche, comme pour la réception de tâche.35 tests V2 passent après ces corrections. Les travaux de correction sont Codex ; toute correction des fichiers ou publication de tâche reste exécutée par JARVIS.


Les sauvegardes temporaires choisies par le modèle dans `/tmp` ne persistent pas entre appels Bubblewrap. Codex a signalé cette erreur de stratégie et précisé la description de `host_exec` : utiliser les racines persistantes pour la reprise. Une commande de copie réussie dans un tmpfs ne prouve pas un fichier durable. Ce guidage est conservé comme intervention Codex, sans l’attribuer à une découverte autonome du modèle.


### Réception finale de l’interface et de l’attente

L’adaptateur JL-02 traitait encore les champs JSON nuls sans valeur par défaut : le premier écran passait mais une page tardive échouait. Le correctif s’applique au journal entier ;36 tests V2 passent, dont une pagination au-delà de150 événements. Les connexions SQLite de l’adaptateur sont fermées explicitement. Les rapports de tâches ont désormais des liens authentifiés, y compris le rapport partiel07 sans coche de réception.22 assertions navigateur et14 pages API réelles ont été vérifiées.

JARVIS a corrigé lui-même SUIVI/ROADMAP avec conservation du contenu antérieur, publié tous les bilans puis enregistré le blocage d’enrôlement. Le redémarrage du service conserve son état, ses empreintes et sa session. Le paquet Tailscale installé ne constitue toujours pas un accès direct validé.

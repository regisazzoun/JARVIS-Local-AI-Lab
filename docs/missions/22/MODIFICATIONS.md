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

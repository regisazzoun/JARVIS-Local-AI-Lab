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

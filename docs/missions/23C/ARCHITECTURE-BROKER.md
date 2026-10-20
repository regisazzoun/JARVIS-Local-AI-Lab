# 23C — architecture observée

Statut : 🟡 En cours / partiel. Observation du code et de l'unité accessibles le 20 octobre 2026 ; processus vivant et politique privée non inspectables depuis cette session.

Le registre conversationnel enregistre les outils de `jarvis/host_client.py`. Leur transport est le socket fixe `/run/jarvis-host/bridge.sock`. Le service `jarvis-host-bridge.service` lance `/usr/local/lib/jarvis-host/host_bridge.py`, annoncé historiquement « mission 11 ». `policy()` lit `/etc/jarvis/host-policy.json` à **chaque requête**, vérifie propriétaire root et absence d'écriture groupe/autres. Le client ne transmet aucun profil de mission. `execute()` applique directement ce dictionnaire : services/actions, racines, dépôts et profils distants.

Il n'existe pas, dans ce chemin de code, de sélection dynamique mission11/mission23. Le champ mission des anciennes lignes capabilities est fixé à `11` par `grant()` ; ce champ n'est pas consulté pour autoriser une opération. La description systemd ne sélectionne pas non plus un profil. Les noms historiques ne prouvent donc pas une révocation.

SO_PEERCRED contrôle l'UID technique ; le cgroup distingue JARVIS-runtime et local-operator pour l'attribution, sans créer de droits. Projet, mission durable et conversation sont des objets du moteur, distincts de cette identité Unix. La politique persistante propriétaire reste l'autorité ; les demandes du modèle dans requests ne l'étendent pas.

host_exec conserve Bubblewrap, les seuls montages accordés, sans bus systemd ni identifiants. systemd, GitHub, SSH et Ansible utilisent les opérations structurées du broker. Les preuves broker sont dans sa base privée ; les checkpoints et la mémoire personnelle restent dans leurs bases canoniques distinctes.

Le candidat 23C ajoute une empreinte de politique et sa méthode de relecture aux réponses. Aucun nouveau système de profils, aucune sélection par conversation, aucune union automatique de droits n'est introduit sans besoin démontré.

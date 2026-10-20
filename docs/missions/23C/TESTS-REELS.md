# Tests et attribution

| Acteur | Opération exécutée | Résultat testé | Portée |
| --- | --- | --- | --- |
| Codex | Client installé → host_policy et host_service LiveKit | PermissionError errno1 avant réponse | Accès session indisponible ; aucune conclusion sur politique |
| Codex | Socket Unix et socket TCP locale | Operation not permitted | Limitation transport locale |
| Codex | systemctl show | Bus inaccessible | État des services non connu |
| Codex | Lecture code/unité et référentiel | Réalisée | Architecture statique seulement |
| Codex | Prévol23C | JSON transport_denied, identité politique et preuve absentes | Nouvelle qualité du diagnostic client testée localement |
| Codex | Cinq tests23C | 5/5 réussis | Tests unitaires, pas réception système |
| Codex | Suite complète | 75 réussis sur76 ; test HTTP en erreur lors de socket() | Suite non intégralement passante dans cet environnement |
| Codex | Lecture PR11/12/13 et patches par connecteur existant | Réalisée | GitHub Codex, pas GitHub JARVIS |
| JARVIS | Nouvelles opérations23C | Aucune exécutée | API inaccessible depuis le coordinateur |
| Broker | Nouvelles opérations23C | Aucune réponse reçue | Aucun reçu de réussite inventé |

Les dix essais mission23 demandés restent à exécuter par JARVIS : services LiveKit, journaux, serveur, agent, fichiers, contrôle applicatif, Ollama, liaison Mac/Dell1, preuves persistantes et GitHub. Même exigence pour commit/push/vérification des blobs/mise à jour PR par JARVIS.

Les résultats antérieurs de mission23 restent historiques : PR12/13 confirment un tour automatisé WAV/WebRTC réussi, des tests d'interruption échoués et l'absence de réception physique. Ils ne sont pas comptés comme de nouveaux essais23C.

# Répartition observée

| Opération | Décideur | Exécution réelle | Preuve |
|---|---|---|---|
| Identifier les fichiers responsables | Qwen80B, inférence Dell1 | Lectures Dell1 | 39645/39650 |
| Choisir correctif et fichier Q1 | Qwen80B | Dell1 | 39839/39844 |
| Choisir correctif et fichier Q2 | Qwen80B | Dell1 | 40287/40292 |
| Choisir les commandes de test | Qwen80B | Dell1 et Dell2 selon ses appels | 40305,40117,40357 |
| Déterminer fichiers/sens de copie | Qwen80B | Broker Mac, SSH et extraction Dell2 | 39883/39897,40321/40335 |
| Refuser une version ou machine incorrecte | Préconditions déterministes du moteur | Mac, observations distantes | 40127,40315 |
| Interpréter les résultats, demander correction/acceptation | Qwen80B | Décisions inférées Dell1 | 39866,40112,40163,40379 |
| Écrire rapports et checkpoints | Texte demandé par Qwen ; persistance du moteur | Mac | 40211,40393,40428 |
| Développer et corriger l’adaptateur | Codex | Mac | Événements codex_interface_escalation |
| Fournir fixture et oracle indépendant | Codex | Préparation Mac, contrôles applicatifs Dell1/Dell2 | 39792,40151,40387 |
| Réception technique et publication GitHub | Codex | Mac /GitHub | Rapport de réception et PR28 |

Qwen décide effectivement sur Dell1 ; son processus d’inférence n’est pas déplacé vers Mac ou Dell2. Dell2 agit ici comme exécuteur de validation et reçoit les sources réelles par transfert vérifié. Aucun moteur d’inférence Dell2 n’est installé.

Les 17 commandes instrumentées authority_work comprennent13 exécutions Dell1 et4 Dell2. Ce ne sont pas tous les appels SSH : ressources, transferts, enveloppes et contrôles Codex ont leurs reçus distincts. Deux commandes modifient réellement des fichiers applicatifs ; une commande déclarée correct n’est qu’une assertion échouée sans changement. Aucune publication GitHub de cette phase n’est attribuée à JARVIS.

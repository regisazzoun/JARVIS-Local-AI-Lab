# Composants réutilisés et modifications

| Composant existant | Réutilisation / modification mission 11 |
| --- | --- |
| Core.chat, transport Ollama et boucle 13F | Conservés ; contexte hôte, observations compactes, checkpoints et reprises ; résultat incomplet sans récit final non prouvé |
| Registry.specs / execute / schemas | Conservés ; nouveaux outils, même validation/audit et mêmes résultats structurés ; inventaire API complet, schémas conversationnels adaptés à la cible |
| lab_terminal / agent.lab_command | Conservés pour le laboratoire facultatif ; aucun remplacement de la démonstration 13F |
| API /api/chat et interface existante | Conservées pour texte et transcription ; ajout d'un panneau et API de missions durables |
| Authentification existante | Réutilisée, aucun changement de compte ou mot de passe ; tests choisissent localement un secret correspondant au hash actif sans l'afficher |
| SQLite/FTS5 de mémoire | Base canonique, souvenirs, préférences et sauvegardes conservés ; données de missions techniques dans une base séparée |
| Whisper Small et Piper Tom | Réutilisés par les mêmes API ; essai vocal sur WAV synthétique, pas de microphone physique |
| adminjarvis et sudo existants | Identité réutilisée ; pas de nouvel utilisateur ni de sudoers global ajouté |
| systemd existant | Confinement conversation conservé ; nouvelle unité broker activée et unité de preuve inoffensive |
| Git, GitHub CLI et authentification | Réutilisés côté broker ; pas de jeton transmis au modèle ; copies Git propres pour publication |
| SSH et Tailscale existants | Préservés ; profil SSH loopback avec clé technique restreinte ajoutée, sans retrait des clés ou du mot de passe |
| Ansible existant | Réutilisé via profils épinglés et opérations autorisées, sans modification des playbooks ou services Dell |
| Services Dell 13D-E/14 et Launcher V1 | Aucune modification de déploiement ni de code Launcher V1 par cette mission |

## Nouveaux fichiers

Les modules et assets déployables sont dans `agentic/mission11/` : broker et politique, client d'outils, contrôleur de missions, graphe/procédures, modules Core/Registry/Server issus de l'installation 13F modifiés, unités systemd, identité actualisée, interface additive, installateur et réception. Les modifications reprennent l'installation constatée ; elles ne constituent pas un deuxième backend conversationnel.

## Emplacements effectifs

- Modules conversation : `/opt/jarvis/conversation/jarvis/`.
- Broker installé : `/usr/local/lib/jarvis-host/host_bridge.py`.
- Autorisation : `/etc/jarvis/host-policy.json` root:root.
- État privé capacités/preuves : `/var/lib/jarvis-agent/state.sqlite`.
- Missions, tâches et procédures : `/opt/jarvis/conversation/runtime/missions.sqlite`.
- Code avant mission et preuves brutes de réception : `/home/adminjarvis/JARVIS/mission11-private/`, non versionnés.
- Configurations gérées : `/etc/jarvis/managed/` ; projets réels : `/var/lib/jarvis/projects/` et `/home/adminjarvis/JARVIS/agent-workspaces/`.

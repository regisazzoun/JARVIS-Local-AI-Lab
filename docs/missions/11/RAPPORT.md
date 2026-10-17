# Rapport de réception — Mission 11 Agentic

**Date :** 17 octobre 2026
**Branche :** `codex/mission-11-agentic-enablement`
**Verdict : GO AVEC RÉSERVES**

JARVIS/Qwen utilise désormais les capacités Debian hôte par le même backend de conversation que le texte et la transcription vocale. Les actions décrites comme validées ci-dessous ont été réalisées par Qwen et vérifiées à partir des traces privées, des fichiers, des unités et des registres. La réception expurgée a passé **42 contrôles sur 42**. Les tests logiciels ont passé 27 tests du backend existant, 9 tests des frontières du broker et 3 tests du planificateur.

## Architecture effectivement installée

La mission reprend le backend, le registre d’outils, l’API de conversation, le transport Ollama, l’identité `adminjarvis`, l’authentification, la mémoire SQLite/FTS5 et le traitement voix Whisper/Piper déjà présents. `lab_terminal` et Bubblewrap restent disponibles pour les missions isolées 13F. Le nouvel outil hôte est raccordé au même `Registry.execute` et à la boucle Qwen ; aucun second backend conversationnel n’a été installé.

`jarvis-host-bridge.service`, exécuté en root, expose un socket Unix privé et vérifie l’identité Unix de l’appelant. Il applique la politique root `/etc/jarvis/host-policy.json`. Les opérations privilégiées sont structurées pour apt, les services explicitement accordés, les journaux, GitHub et les profils SSH/Ansible. `host_exec` exécute comme `adminjarvis`, avec les vrais répertoires hôte accordés montés en écriture et la racine en lecture seule ; il ne donne pas un shell root général. Les secrets GitHub, clés SSH et données d’authentification ne sont pas montés dans l’environnement de commande du modèle.

Les capacités et demandes persistantes résident dans `/var/lib/jarvis-agent/state.sqlite`, détenu par root. Missions, checkpoints, dépendances et procédures techniques utilisent `runtime/missions.sqlite`. La mémoire personnelle préexistante n’a pas changé : les 5 souvenirs, 4 préférences, 10 conversations et 34 messages sauvegardés avant l’installation sont toujours présents à l’identique. Les registres JSON publiés ici sont des instantanés expurgés ; la politique root et les bases locales restent les références.

## Installé et réellement validé

| Capacité | Résultat de réception |
| --- | --- |
| Debian réel | Qwen a créé, relu et modifié un fichier hôte persistant ; il a écrit et supprimé des fichiers et vérifié leur absence. Il a aussi modifié `/etc/jarvis/managed/`, seul répertoire de configuration accordé. |
| Commandes et systemd | Commandes système réelles, état et journaux du backend consultés. Le service de preuve a été démarré, redémarré puis vérifié actif par Qwen. |
| Paquets | `hello`, `tree`, `nodejs` et `npm` installés/configurés ; versions et commandes réellement exécutées par Qwen. `dpkg --audit` est propre. L’installation de `npm` a repris après un timeout et une configuration dpkg incomplète. |
| GitHub privé | Qwen a consulté le dépôt privé, publié une preuve de test sur `jarvis/mission11-proof-20261017`, vérifié le SHA et relu le contenu sur cette branche. La mise à jour répétée du même contenu est un succès idempotent. `main` n’a pas été modifiée. |
| Attribution durable | Qwen a détecté `tree` absent, créé une demande persistante, puis a installé le paquet, exécuté `tree --version` et lancé son propre `capability_test`. Les demandes `tree`, accès au dépôt Launcher2 et réparation npm sont reliées à leurs preuves de test et marquées `VALIDÉ`. |
| Mission complète et reprise | Qwen a créé un projet Python réel, observé une `ValueError`, corrigé la configuration, vérifié `PORT_OK=8091`, enregistré la procédure et validé un graphe de trois tâches dépendantes. Le backend a été redémarré après checkpoint ; Qwen a relu l’état hôte et terminé la mission au troisième passage. |
| SSH, Ansible et Tailscale | Le profil `local-ssh` a réussi identité, ressources et services ; Ansible a réussi ping, déploiement d’un fichier et installation apt autorisée. L’accès distant Dell `dell-observe`, créé à partir des éléments 13D-E déjà validés, a été utilisé par Qwen pour identité, ressources et services en lecture seule. |
| Texte et voix | Les actions hôte fonctionnent depuis `/api/chat` en mode agent décoché ; Qwen a écrit, relu et conservé le rapport d’intervention. Le même parcours a été exécuté depuis Whisper/Piper avec un WAV synthétique. |
| JL-02 | Qwen a créé puis inspecté `regisazzoun/JARVIS-Launcher2` et a enregistré l’objectif de développement futur. Le dépôt est vide ; le code V2 n’a pas été réalisé ici. Launcher V1 est intact. |

Le détail des composants réutilisés se trouve dans [COMPOSANTS.md](COMPOSANTS.md), l’audit avant modification dans [AUDIT.md](AUDIT.md), et le schéma d’autorité dans [ARCHITECTURE.md](ARCHITECTURE.md).

## Portée exacte des habilitations

Les autorisations résistent au redémarrage des services ; Qwen a réutilisé `tree`, npm, l’accès GitHub et le transport SSH après redémarrage de `jarvis-conversation`. Le test n’a pas redémarré tout le Mac. Les commandes `host_exec` peuvent écrire dans `/var/lib/jarvis/projects`, `/etc/jarvis/managed` et `/home/adminjarvis/JARVIS/agent-workspaces`; les installations et services sont limités à la politique root. Une nouvelle ressource hors de ces chemins ou services exige une modification de politique par Codex dans le périmètre propriétaire déjà accordé, puis un test réel par Qwen.

Le profil Dell observé est strictement en lecture seule pendant le déploiement 13D-E/14. Les modifications à distance sur le Dell ne sont donc pas testées et restent exclues jusqu’à la fin de ce déploiement. Le profil SSH/Ansible ayant fait l’objet d’opérations de mutation pendant cette mission est la cible locale loopback. Aucune configuration DHCP de la Bbox, unité de déploiement Dell, clé existante ou méthode SSH de secours n’a été modifiée.

## Demandes à Codex et limites restantes

La file SQLite est persistante et exploitable, mais elle n’envoie pas automatiquement de notification à une session Codex. Codex a traité les demandes de son périmètre et Qwen a effectué les sondes après correction. Un transport automatique nécessitera un consommateur Codex autorisé distinct ; une demande de Qwen ne pourra jamais modifier elle-même la politique.

L’activation GitHub Pages est conservée comme demande `DEMANDÉE` pour JL-02 : Launcher2 existe, mais n’a encore aucun contenu ni branche `gh-pages` à publier. Qwen devra créer et tester la publication lors du développement Launcher V2. Les demandes et états expurgés figurent dans [DEMANDES.json](DEMANDES.json) et [CAPACITES.json](CAPACITES.json).

Un scénario final trop large en chat normal a montré des répétitions de mutations par Qwen. L’envoi GitHub identique est maintenant idempotent, et un essai ciblé en chat normal confirme le cycle réussi écriture, relecture, rapport. Le graphe durable reste le chemin validé pour les missions longues. Ce comportement de répétition reste une limite à surveiller.

## Contrôles non réalisés

- Redémarrage complet de l’hôte et réutilisation après reboot.
- Administration mutative d’une machine distincte pendant le déploiement Dell actif.
- Entrée microphone et sortie haut-parleur physiques ; la voix a été testée avec un fichier WAV synthétique.
- Publication effective de GitHub Pages, reportée à JL-02.
- Livraison automatique d’une demande vers Codex.

Les preuves brutes demeurent dans le répertoire privé de réception et ne sont pas versionnées. [PREUVES-EXPURGEES.json](PREUVES-EXPURGEES.json) donne les assertions et les compteurs sans exporter les identifiants, secrets ou souvenirs personnels. Les incidents de réception sont détaillés dans [INCIDENTS.md](INCIDENTS.md) ; les opérations de maintenance et de retour arrière dans [MAINTENANCE.md](MAINTENANCE.md).

## JL-02 transmis à JARVIS

JARVIS doit prendre en charge le développement et la publication de Launcher V2 dans `regisazzoun/JARVIS-Launcher2` : interface responsive, chat texte et vocal, supervision matérielle et GitHub Pages. Il doit préserver intégralement Launcher V1 et exécuter son propre cycle de tests et de rapport. Aucun code JL-02 n’a été écrit par Codex.

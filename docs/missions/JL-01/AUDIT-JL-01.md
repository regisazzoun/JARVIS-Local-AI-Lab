> **Copie documentaire Codex — mission 00.** Source réelle : `/home/adminjarvis/JARVIS-Launcher/docs/AUDIT-JL-01.md`. Réception et preuves selon leur date, sans réexécution par cet audit. Le dépôt source et ses services restent inchangés. Données privées expurgées.

# JL-01 — Audit court des éléments accessibles

14 octobre 2026. Hôte d’exécution Linux ; aucun accès macOS distant fourni. Lectures ciblées uniquement. Aucun ancien script exécuté, remplacé ou supprimé.

| Élément | Constat | Limite |
|---|---|---|
| Série macOS V2, notamment 05_Retrouver_Session_Codex.command | Aucun fichier `.command` retrouvé dans les arbres accessibles /home/adminjarvis, /tmp et /opt/jarvis, hors environnements/outils | Leur absence sur les Macs n’est pas démontrée ; les fichiers ne sont pas inventés |
| Serveur Tailscale | `tailscale ip -4` retourne `[ADRESSE EXPURGÉE]` sur cet hôte | Accès depuis les deux Macs non testé |
| LAN `[ADRESSE EXPURGÉE]` | Valeur fournie, également documentée dans les missions JARVIS | Connectivité depuis les deux Macs non testée |
| Utilisateur/répertoire | `adminjarvis`, `/home/adminjarvis/JARVIS` accessible | Authentification SSH macOS non testée |
| Clé `~/.ssh/id_ed25519_jarvis` | Pas de clé homonyme retrouvée sur l’hôte Linux ; aucune clé privée lue | Doit être vérifiée localement sur chaque Mac |
| Alias SSH `jarvis` | `ssh -G jarvis` conserve hostname=jarvis sur l’hôte Linux | Aucun alias effectif des deux Macs vérifié ; le MVP ne dépend pas d’un alias |
| Codex | `/home/adminjarvis/.local/bin/codex`, version 0.162.1 | Aucun Codex interactif lancé pendant cette mission |
| tmux | `/usr/bin/tmux`, version 3.5a | Sessions du vrai serveur laissées intactes |
| Sessions au relevé | `jarvis-codex`, `jarvis-13f`, toutes deux détachées au relevé | `jarvis-13bc` non observée ; elle reste un choix historique configurable, pas une session déclarée existante |
| Port web 8765 | Écoute sur `[ADRESSE EXPURGÉE]:8765`; service conversation actif au relevé | Cela ne valide ni l’authentification web, ni le tunnel macOS, ni la chaîne vocale |
| GitHub dédié | `regisazzoun/JARVIS-Launcher` retourne 404 via le connecteur | Non accessible ou inexistant ; aucune capacité de création de dépôt exposée, aucun token Git CLI fourni |
| GitHub principal | Accessible mais exclu de tout changement JL-01 | Aucun fichier, branche ou PR du dépôt principal modifié par JL-01 |

Les valeurs connues sont des défauts explicites de configuration. Les deux profils désignent les clients MacBook Pro / Mac mini, avec le même serveur. Des paramètres différents sont possibles, notamment le port local du tunnel, sans inventer des différences de configuration non observées.

Sources de méthode : [Apple, appel des outils en ligne de commande et Terminal](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/CallCommandLineUtilities.html), [Apple, déclaration de protocoles URL](https://developer.apple.com/documentation/appkit/nsapplicationdelegate/application(_:open:)), [OpenSSH, SSH et redirection locale](https://man.openbsd.org/ssh), [GitHub, Pages et gratuité pour les dépôts publics](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

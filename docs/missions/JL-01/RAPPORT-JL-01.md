> **Copie documentaire Codex — mission 00.** Source réelle : `/home/adminjarvis/JARVIS-Launcher/docs/RAPPORT-JL-01.md`. Réception et preuves selon leur date, sans réexécution par cet audit. Le dépôt source et ses services restent inchangés. Données privées expurgées.

# Mission JL-01 — rapport de livraison

14 octobre 2026. **GO AVEC RÉSERVES pour livrer et prétester le MVP.** La réception complète sur les deux Macs, le protocole natif et GitHub Pages réels n’est pas acquise.

## Réalisé

Projet autonome dans `/home/adminjarvis/JARVIS-Launcher`, sans changement du dépôt principal ni de son installation. Audit des scripts réellement accessibles, frontend HTML/CSS/JS sans bibliothèque, deux profils clients persistants, favoris/sections/labels JSON et copie de secours.

Trois actions principales (SSH, Codex, Codex tmux), tmux avancé exact sans suppression/fusion, tunnel localhost, lecture des services, LAN explicite et trois terminaux avec confirmation. Application macOS AppleScript/JXA avec code source, installateur natif gratuit, protocole personnalisé, configuration locale conservée et désinstallation par Corbeille.

Protection : IDs fermés, arguments de session validés localement, matériel/profil contrôlés, aucun shell libre venant d’une URL, confirmation locale obligatoire, SSH avec pseudo-terminal et quoting, clés privées et secrets absents du dépôt/URL. Aucun serveur HTTP permanent ni script JARVIS à dupliquer sur les clients.

## Preuves

Neuf tests automatisés passent, dont 67 cas de politique. Captures bureau/mobile, résultats JSON et simulation du protocole depuis un chemin Pages dans docs/evidence. Test réel d’échec OpenSSH sur loopback ; tests tmux/Codex avec binaires factices isolés. Contrôles bash -n. Aucun appel de génération Codex ni création/attachement à une session JARVIS pendant JL-01.

Sur le vrai hôte, Codex et tmux sont disponibles, Tailscale indique [ADRESSE EXPURGÉE] et le service web écoute sur [ADRESSE EXPURGÉE]:8765. Les sessions jarvis-codex et jarvis-13f étaient présentes au relevé ; jarvis-13bc n’a pas été observée. Aucun script macOS .command V2 trouvé ; aucune présence/absence sur les Macs revendiquée.

## Livrables

- Sources structurées, README français, audit, architecture, dépannage, publication, PR préparée et matrice de réception.
- Fichiers Pages générés dans `dist/pages/`, ZIP de sources, bundle Git contenant l’historique local et manifestes SHA-256.
- Branche locale `codex/jl-01-jarvis-launcher`; main contient uniquement le README d’initialisation. Aucun merge automatique.

Installation MacBook Pro : `bash macos/install.sh macbook-pro`. Installation Mac mini client : `bash macos/install.sh mac-mini`. Après réception native, ouvrir le site et choisir le profil de ce poste.

## Blocage GitHub

Le dépôt dédié retourne 404 avec l’accès connecté. Le connecteur n’expose pas de création de dépôt, Git CLI n’est pas authentifié et gh n’est pas installé. La permission de création du compte n’est donc pas affirmée ou refusée : l’opération n’est pas réalisable avec ces capacités. Aucun second dépôt du projet principal n’a été créé, aucun fichier de ce dépôt n’a été modifié.

**Pas d’URL de branche distante, de PR ou de site actif à annoncer.** Les fichiers à publier et le résumé de PR sont prêts. [La procédure exacte](https://github.com/regisazzoun/JARVIS-Launcher/blob/main/docs/PUBLICATION.md) crée le dépôt dédié public, pousse la branche de travail et la branche statique gh-pages, prépare la PR, puis explique l’activation gratuite de Pages sans fusionner main.

## Réserves et suite

La syntaxe AppleScript et les appels Foundation/JXA, l’installation réelle, les permissions macOS et l’ouverture de Terminal doivent être vérifiés sur les deux Macs. Le protocole depuis la vraie origine GitHub Pages, SSH Tailscale/LAN, Codex interactif et l’accès web authentifié doivent être reçus. La copie web et l’autorité locale peuvent diverger si une seule configuration est éditée ; la mise à jour est explicitement séparée.

La disponibilité native ne peut pas être mesurée sûrement par une page sans canal de retour ; elle reste « non vérifiable », avec un diagnostic local. Une configuration locale corrompue, un matériel inconnu ou un profil différent bloque l’action. L’application n’est pas notariée et son installation locale doit être assumée par l’utilisateur après revue des sources.

Prochaines étapes : publier avec l’accès de création adéquat, activer/vérifier Pages, effectuer la matrice macOS sur les deux clients et compléter les résultats sans secrets. Ne fusionner la PR qu’après accord explicite.

Compte rendu envoyé le 14 octobre 2026 au compte Gmail connecté de l’utilisateur. Le service a confirmé l’envoi avec les statuts SENT et INBOX. Le mail précise les tests et réserves, le blocage de publication, les commandes de récupération des livrables, l’installation des deux profils et la procédure GitHub. Aucun secret envoyé ; les identifiants internes du message restent hors sources publiques.

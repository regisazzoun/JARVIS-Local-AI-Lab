# Installation et utilisation

## Accès immédiat

Le service est déjà installé sur le Mac mini Debian, port8766. Depuis un Mac avec les accès existants, télécharger cette branche du dépôt puis double-cliquer `macos/Ouvrir-JL03.command` ; si nécessaire, `chmod +x macos/Ouvrir-JL03.command` une fois. Le script lit le profil du compagnonJL-02 dans `~/Library/Application Support/JARVIS Launcher/config.json` sans le modifier. Il utilise le même hôte, utilisateur, port et chemin de clé. En l'absence de configuration, il utilise l'aliasSSH `jarvis` ; `JL03_SSH_TARGET` permet de choisir un alias déjà configuré.

Le tunnelV3 ne transporte que8766. Il n'arrête aucun ancien tunnel. La fenêtre reste ouverte tant que son SSHenfant doit être maintenu ; reconnexion après rupture, arrêt après trois échecs consécutifs. Une connexion déjà saine est simplement ouverte dans le navigateur. Le modeLiveKit nécessite aussi les tunnels existants7880/7881. Le script macOS a été contrôlé syntaxiquement et par fixtures de processus ; son exécution sur le MacBook du propriétaire reste à recevoir.

Ouvrir http://localhost:8766/. Si le cookie canonique existe surlocalhost, il est réutilisé ; sinon une connexion JARVIS. Une cléSSH déjà fonctionnelle évite une identificationSSH supplémentaire ; cette condition ne peut pas être garantie sans essai natif.

## Utilisation

Écrire dans le fil ou activer le microphone. La lecture automatique des réponses se règle dans Paramètres et reste désactivée par défaut. Bleu = disponible/écoute ; rouge = demande ou mission sélectionnée en traitement ; vert = sortie vocale active. Couper le micro arrête sa capture, pas la demande en cours. Arrêter la voix coupe la lecture sans annuler la mission. Une parole détectée pendant la lecture du mode canonique l'interrompt puis est transcrite.

Projets, nouvelle discussion, renommage et recherche utilisent la mémoire canonique. Les fichiers accessibles ont des liens privés ; la bibliothèque propose des lecteursWAV. Paramètres regroupe les liens vers administrationJL-02, état, outils, GitHub, prototype et optionLiveKit23D. Cette option est marquée comme session prototype non persistée dans la mémoire canonique.

Le panneau inférieur conserve son flux en étant réduit. Il est redimensionnable, agrandissable, possède son propre défilement et un bouton Revenir au direct. Recharger la page relit le journal depuis le serveur. Les missions continuent dans leurs workers existants quand la page est fermée.

## Reproduction sur le laboratoire existant

Placer le dépôt dans `/var/lib/jarvis/projects/jl03`. Python3stdlib suffit au backend. Les dépendances front sont déjà vendues ; `npm ci` puis copie des distributions officielles est réservé à une mise à jour contrôlée. `bash backend/install.sh` ajoute uniquement l'action de lecturetélémétrie manquante et le serviceV3, avec sauvegarde privée de la politique. Aucun broker ou JL-02 n'est réinstallé. Ce script est une procédure de reproduction ; le déploiement de réception a été installé directement par Codex.

Contrôles : `npm test`, `npm run check`, `curl --fail http://localhost:8766/api/health`. Le smokePlaywright peut être exécuté avec `JL03_COOKIE` fourni dans l'environnement privé et `JL03_CHROMIUM` si nécessaire ; ne jamais commiter cette valeur.

Retour arrière : `sudo systemctl disable --now jarvis-launcher3.service`. Cela ne désinstalle niJL-01/JL-02 ni les bases canoniques. L'action fixe `telemetry_v3` est additive et peut rester ; son retrait exige une édition ciblée de la politique, jamais une restauration aveugle qui perdrait des modifications ultérieures.

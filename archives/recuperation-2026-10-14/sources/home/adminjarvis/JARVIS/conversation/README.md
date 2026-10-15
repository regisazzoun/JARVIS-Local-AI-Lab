# JARVIS conversationnel — 13B + 13C
Application locale indépendante d’Open WebUI. Dépendances backend : bibliothèque standard Python 3.13. Moteurs vocaux : environnement 13A existant, uniquement en lecture, workers CPU séparés. Aucun service systemd ajouté.

## Lancement manuel sur le serveur (hors environnement restreint Codex)
```bash
cd /home/adminjarvis/JARVIS/conversation
scripts/start
```
Au besoin, recréer l’environnement isolé sans installation globale :
```bash
python3 -m venv --without-pip /home/adminjarvis/JARVIS/conversation/.venv
```
Le port proposé est 8765. Sa disponibilité n’a pas pu être vérifiée dans l’environnement restreint. Le bind sur 127.0.0.1 est la vérification définitive : un conflit termine l’application sans toucher au processus existant. Pour choisir un autre port, copier `config/example.json` dans un fichier local, modifier `port`, puis `scripts/start --config /chemin/absolu/config.json`. Utiliser le même port local et distant pour respecter les contrôles Host/Origin.

Depuis le poste client :
```bash
ssh -N -L 8765:127.0.0.1:8765 adminjarvis@192.168.1.99
```
Puis ouvrir **http://localhost:8765** dans Chrome ou Firefox récent et autoriser le microphone. L’adresse Tailscale connue peut remplacer l’adresse LAN, sans aucune modification réseau. Ce tunnel n’a pas été exécuté pendant la mission.

Maintenir « Maintenir pour parler » (ou Espace/Entrée lorsque le bouton a le focus), puis relâcher. Vérifier et corriger la transcription ; cliquer sur Envoyer. Cette étape évite d’envoyer une transcription incorrecte automatiquement. Une limite de durée stoppe l’enregistrement. Arrêter l’audio invalide aussi une synthèse encore en attente. Les longues réponses sont découpées en fragments de 600 caractères, lus successivement.

`Ctrl-C` arrête le lancement au premier plan. Une opération en cours termine ou atteint son timeout avant la sortie complète ; les workers ne sont pas volontairement abandonnés. Depuis un autre terminal, `scripts/stop` vérifie le PID, l’utilisateur, le répertoire et le module avant de signaler uniquement ce processus. `scripts/status` interroge l’état applicatif ; il ne certifie pas la disponibilité d’Ollama.

## Mémoire
Cocher/décocher la conservation avant une nouvelle conversation. Décocher commence une session éphémère en RAM ; cela ne supprime pas les conversations déjà enregistrées. Sessions éphémères : maximum 32, contexte glissant de 24 messages. Conservation SQLite : 30 jours par défaut, purge au lancement. Les souvenirs temporaires sont limités à leur identifiant de session ; les souvenirs permanents et de projet exigent une validation explicite. Aucun extrait personnel n’est proposé automatiquement par le modèle : le bouton Proposer crée la proposition, le bouton Approuver la valide. Une proposition en attente n’est jamais injectée dans le prompt. Le changement de modèle conserve le même ID de conversation et utilise le même dépôt SQLite.

Recherche FTS5 avec mots littéraux, filtre de projet et inclusion des souvenirs globaux. La suppression retire le souvenir et son index ; elle n’efface pas les anciennes conversations qui ont éventuellement cité son contenu. Audit minimal : opération, identifiant et date, sans contenu du souvenir supprimé.

## Sauvegarde, restauration et export privés
```bash
scripts/memory backup runtime/memory.sqlite /chemin/prive/sauvegarde.sqlite
scripts/memory restore-test /chemin/prive/sauvegarde.sqlite /tmp/jarvis-restauration-test.sqlite
scripts/memory export runtime/memory.sqlite /chemin/prive/export.json
```
Le répertoire destination doit exister. Aucune destination existante n’est écrasée. La restauration refuse un fichier existant et valide `integrity_check`. La sauvegarde utilise SQLite Online Backup ; conserver les sauvegardes dans un emplacement privé (permissions 0600), idéalement avant toute évolution. Le bouton Exporter fournit des données privées : ne pas les joindre aux archives de partage. Une restauration test peut être ouverte avec `scripts/start --db /tmp/jarvis-restauration-test.sqlite`, application principale arrêtée.

## Vérification
```bash
scripts/test
scripts/test-voice
scripts/audit > /tmp/jarvis-audit-local.json
```
`scripts/test-ollama` est un essai réel facultatif d’un seul modèle, à lancer uniquement pendant une fenêtre sans conversation Open WebUI. Il refuse un moteur absent ou un modèle déjà chargé ; cela ne garantit pas l’absence d’une requête externe concurrente. Aucun test automatique ne charge les trois modèles réels.

Aucun jeton d’authentification ajouté : application réservée à la boucle locale et au tunnel SSH authentifié. Contrôles Host/Origin, en-tête requis pour les mutations, absence de CORS, CSP et absence de journalisation des messages. Toute exposition hors boucle locale ou utilisation multiutilisateur doit faire l’objet d’une mission dédiée.

Voir `reports/` et `evidence/` pour les résultats et réserves. Aucun GO complet navigateur/Ollama n’est déclaré.

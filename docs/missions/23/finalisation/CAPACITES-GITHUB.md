# Connecteur GitHub persistant — finalisation23

Codex étend le broker ; JARVIS doit démontrer les opérations. L'identité gh existante reste dans le système, jamais dans le modèle. Politique : deux dépôts propriétaire déjà autorisés, branches jarvis/ ou codex/, aucune fusion main. Les lectures officielles tierces restent limitées à la politique de lecture.

## Contrat

`host_github(repository, action, ...)` :

- `repositories`, `inspect`, `branches`, `file`, `download`, `clone` : découverte/lecture et récupération existantes.
- `branch_create` : branche dédiée depuis main ; répéter retourne l'existante.
- `push` : un fichier ; `path` est le **dossier racine local**, `file` le chemin relatif. Les erreurs expliquent désormais le chemin calculé.
- `push_tree` : `path` dossier racine, `files` chaîne JSON d'une liste explicite de fichiers relatifs, `branch` dédiée, `message` facultatif. Exporte les sources sous l'identité confinée, puis crée un commit et pousse depuis un clone propre authentifié. N'exécute ni hooks ni configuration Git du projet. Ignore aucun fichier silencieusement : chemin privé, secret détecté, binaire ou fichier >=1Mo provoque un refus. `.env`, `.git`, venv, node_modules et private sont exclus. L'historique local reste conservé ; le commit distant de sources nettoyées a son propre SHA.
- `verify_tree` : mêmes paramètres path/files/branch ; compare les SHA Git de tous les fichiers locaux avec l'arbre distant. Retourne les fichiers absents ou différents ; aucune publication implicite.
- `commits`, `verify_commit` : branch obligatoire ; commit SHA facultatif. Vérifie présence et accessibilité du commit depuis la branche, retourne SHA/URL/verified.
- `diff` : changements de branche par rapport à main.
- `prs`, `pr_status` : PR et état.
- `pull_request` : crée une PR brouillon ou met à jour le corps de celle déjà ouverte ; body transmis par fichier, jamais par interpolation shell.

Les commits locaux peuvent être créés avec host_exec ; ils ne donnent pas accès aux credentials. Un commit contenant .env doit rester local ; préparer une livraison nettoyée, sans réécrire l'historique pour masquer l'incident.

## Reprise

Même snapshot déjà présent : aucun nouveau commit. Échec réseau/authentification/conflit : retour code/stderr/diagnostic, aucune réception supposée, aucun force push. Réobserver branche et fichiers avant nouvelle publication ; le clone propre récupère la branche distante courante à chaque essai. La publication ne supprime pas implicitement des fichiers distants.

## Défaut constaté

Les appels t12 passaient un fichier dans path alors que le broker ajoutait file. L'authentification gh était disponible ; le git push natif confiné n'avait pas ces credentials, volontairement. Un premier push et une relecture ont effectivement réussi par JARVIS après correction des arguments ; la publication complète doit être reçue séparément.

## Vérification

Tests automatisés : questions/exécution, restrictions de branches/chemins/secrets, snapshot inchangé sans doublon et conflit sans force push ; suite complète à58 tests réussis au premier déploiement. Les reçus réels JARVIS sont conservés dans la mission originale, distincts des vérifications Codex.

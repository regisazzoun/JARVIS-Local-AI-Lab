# Contrôle avant publication

**Ne jamais publier automatiquement les rapports bruts ni les dossiers de preuves.**

Retirer les mots de passe, jetons, clés SSH privées, fichiers `.env`, données personnelles, journaux d'authentification, bases utilisateurs et adresses privées inutiles.

La mission 07 signale explicitement plusieurs preuves privées, dont `db-avant-prive.json`, `db-apres-prive.json`, `rejeu-prive.json` et `transmissions-privees.jsonl`. Elles restent hors dépôt.

Pour les changements importants, préparer une pull request et faire valider la publication. Un dépôt privé n'est pas une raison pour y placer des secrets.

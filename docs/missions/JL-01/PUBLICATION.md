> **Copie documentaire Codex — mission 00.** Source réelle : `/home/adminjarvis/JARVIS-Launcher/docs/PUBLICATION.md`. Réception et preuves selon leur date, sans réexécution par cet audit. Le dépôt source et ses services restent inchangés. Données privées expurgées.

# Publication gratuite sur GitHub et Pages

État JL-01 : code et commits préparés localement. Le connecteur GitHub sait accéder au projet principal, mais n’expose aucune création de dépôt. `regisazzoun/JARVIS-Launcher` retourne 404 ; Git CLI n’est pas authentifié. Aucun dépôt, aucune PR et aucun site public JL-01 n’ont donc été créés durant cette passe. Il ne s’agit pas d’un refus de permission observé, mais d’une capacité indisponible.

## Publication avec les commits préparés

Depuis le dossier Git local livré `/home/adminjarvis/JARVIS-Launcher` ou un clone de son bundle Git :

```bash
gh auth login --git-protocol https --web
gh auth setup-git
git switch codex/jl-01-jarvis-launcher
bash scripts/publish.sh
```

GitHub CLI est gratuit. `gh auth setup-git` configure l’accès Git HTTPS sur la machine qui publie ; aucun jeton n’est ajouté au dépôt. Le script crée seulement `regisazzoun/JARVIS-Launcher` public, ou utilise ce dépôt s’il est vide. S’il contient déjà des données, il s’arrête pour les préserver. Il initialise main avec le seul README de départ, pousse la branche de travail, crée la PR depuis `docs/PR.md`, génère le site statique et pousse la branche séparée gh-pages. **Aucune fusion de code vers main.**

Le script ne doit pas être utilisé pour publier le projet principal. Les chemins distants et le nom du dépôt sont fixes.

Si vous partez du bundle :

```bash
git clone JARVIS-Launcher-JL-01.bundle JARVIS-Launcher
cd JARVIS-Launcher
git switch codex/jl-01-jarvis-launcher
bash scripts/publish.sh
```

Le ZIP contient les sources sans `.git`. Il sert à l’installation macOS et à la revue ; le bundle conserve main et la branche de travail pour publication.

## Activer Pages sans fusionner la PR

Dans le nouveau dépôt : Settings → Pages → Build and deployment → Deploy from a branch → `gh-pages` → `/ (root)` → Save. Ne sélectionnez pas `/site` : Pages accepte seulement la racine ou `/docs` pour cette méthode.

Ou, avec l’autorisation Pages/Administration adéquate :

```bash
gh api --method POST repos/regisazzoun/JARVIS-Launcher/pages \
  -f build_type=legacy -f 'source[branch]=gh-pages' -f 'source[path]=/'
gh api repos/regisazzoun/JARVIS-Launcher/pages --jq '{status,html_url,source}'
```

Adresse attendue **après activation et build réussi**, pas encore vérifiée : `https://regisazzoun.github.io/JARVIS-Launcher/`. La branche gh-pages publie la livraison en revue ; cela ne fusionne pas la branche applicative vers main. Après publication, ouvrir la véritable URL, vérifier les deux profils, puis tester chaque protocole sur chaque Mac avec la checklist de réception.

## Si le dépôt a été initialisé entretemps

Ne poussez pas la branche main préparée par-dessus main distante. Clonez le dépôt existant dans un autre dossier, partez de sa branche principale et créez la branche JL-01. Copiez les seuls fichiers du ZIP dans cette branche après inspection des collisions ; conservez les versions concurrentes en cas de doute. Faites un commit, poussez la branche et créez la PR avec le fichier `docs/PR.md`. Générer puis publier le site sur une nouvelle branche Pages si gh-pages contient déjà des données à préserver. Aucun force-push, reset destructif ou fusion automatique.

Références officielles : [GitHub CLI, création d’un dépôt](https://cli.github.com/manual/gh_repo_create), [Pages depuis une branche](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [API Pages et permissions](https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site).

# Rapport technique - Tâche T3 : Calcul empreinte SHA256 et création de manifest.json

## Résultat technique vérifié

Le fichier `/var/lib/jarvis/projects/mission26b/A/manifest.json` a été créé avec succès, contenant l'empreinte SHA256 réelle du fichier summary.json.

## Données techniques observées

### Empreinte calculée
Commande `sha256sum /var/lib/jarvis/projects/mission26b/A/summary.json` exécutée via `host_exec` (evidence `d65c0e4e21d746c9ae4e372bc8ed0b2d`, invocation `a63f735cc745432682abf17d59955bb8`) produisant :
```
5f82760437cc19f056462ab75b163745c090aa4e2dd61da3ba314d3b853eb1df  /var/lib/jarvis/projects/mission26b/A/summary.json
```

### Contenu de manifest.json
Écriture via `host_write_file` (evidence `52d8a85872ac4e23aa7de92768e1eaaa`, invocation `47445c026bb84e148620466dff4a4f69`) produisant :
```json
{
"file": "summary.json",
"sha256": "5f82760437cc19f056462ab75b163745c090aa4e2dd61da3ba314d3b853eb1df"
}
```

### Vérification sémantique
Appel `mission_verify` (evidence `5c89284313994b45ad99de58b0204b86`) confirmant le statut **PASS** :
- `/file`: valeur "summary.json", type string conforme
- `/sha256`: chaîne de 64 caractères hexadécimaux, type string conforme

## Provenance des données

L'empreinte SHA256 provient du fichier summary.json créé lors de la tâche T2 (rapport validé evidence `41c73c6d91f84837b1b56b1ed612a058`), contenant :
```json
{
"lines_articles": 3,
"somme_quantites": 12
}
```

## Limites techniques

Le fichier manifest.json est créé exclusivement dans `/var/lib/jarvis/projects/mission26b/A` via `host_write_file`. Aucune opération externe n'est effectuée. Les permissions Debian par défaut sont conservées sans modification explicite.

## État final

La tâche T3 est techniquement achevée avec succès. Le fichier manifest.json contient l'empreinte SHA256 exacte et vérifiée du fichier summary.json, prête pour la tâche T4 (vérification de cohérence entre les deux fichiers).

L'exécution de la commande `sha256sum /var/lib/jarvis/projects/mission26b/A/summary.json` via host_exec (invocation `a63f735cc745432682abf17d59955bb8`, evidence `d65c0e4e21d746c9ae4e372bc8ed0b2d`) a produit l'empreinte hexadécimale : 5f82760437cc19f056462ab75b163745c090aa4e2dd61da3ba314d3b853eb1df.

Le fichier `/var/lib/jarvis/projects/mission26b/A/manifest.json` a été écrit via host_write_file (invocation `47445c026bb84e148620466dff4a4f69`, evidence `52d8a85872ac4e23aa7de92768e1eaaa`) avec le contenu JSON suivant :
```json
{
"file": "summary.json",
"sha256": "5f82760437cc19f056462ab75b163745c090aa4e2dd61da3ba314d3b853eb1df"
}
```

La lecture de ce fichier via host_read_file (invocation `92f595e939f94378918b245048f4b549`, evidence `ce20402bb3234292b47fcf0249bb6e2c`) confirme le contenu exact ci-dessus.

La vérification sémantique mission_verify (invocation `5c89284313994b45ad99de58b0204b86`, evidence correspondante) a confirmé le statut PASS :
- Champ `/file` : valeur "summary.json", type string conforme
- Champ `/sha256` : chaîne de 64 caractères hexadécimaux, type string conforme

L'empreinte SHA256 provient du fichier summary.json créé lors de la tâche T2 (rapport validé, evidence `41c73c6d91f84837b1b56b1ed612a058`). La lecture de summary.json via host_read_file (invocation `653d08b9121348aca63044a944da72b4`, evidence `ff67fad2ad984cf0b42c8de8056b26da`) confirme son contenu :
```json
{
"lines_articles": 3,
"somme_quantites": 12
}
```

Le fichier manifest.json est créé exclusivement dans `/var/lib/jarvis/projects/mission26b/A` via host_write_file. Aucune opération externe n'est effectuée. La documentation technique des permissions Debian fera l'objet de la tâche T8 avec preuve par ls -la.

**Échecs historiques conservés :**
- Tentative de rapport T3 initiale (event:13747) : FAIL - Le rapport rejeté car titres de section non vérifiables ("Titre descriptif sans assertion factuelle", "Titre de section sans contenu factuel ou technique"). Ce rejet a conduit à la reformulation du rapport actuel avec uniquement des assertions techniques prouvées par les invocations d'outils.
- Le plan v1 initiale manquait la tâche T7 pour le rapport final (FAIL audit coverage).
- Les collisions de report_path entre tâches ont été corrigées dans les versions v2b-v4 du plan.
- La dernière tentative de mission_task_complete pour T3 a échoué car l'affirmation "Les permissions Debian par défaut sont conservées sans modification explicite" manquait de preuve technique (commande ls -la). Cette affirmation est maintenant retirée et reportée vers la tâche T8 dédiée.

La tâche T3 est techniquement achevée avec succès. Le fichier manifest.json contient l'empreinte SHA256 exacte et vérifiée du fichier summary.json, prête pour la tâche T4 (vérification de cohérence entre les deux fichiers).

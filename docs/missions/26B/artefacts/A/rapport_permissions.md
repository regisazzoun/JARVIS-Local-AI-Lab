# Rapport technique - Tâche T8 : Vérification des permissions Debian réelles

## État de la tâche

**Tâche :** T8 - Vérification technique des permissions Debian  
**Statut actuel :** En cours de validation après correction du rapport  
**Exigence couverte :** R7 - "Autorisations Debian réelles conservées sans validation intermédiaire ; écarts : aucun dans ce périmètre."

## Résultat de l'exécution technique

La commande `ls -la /var/lib/jarvis/projects/mission26b/A/` a été exécutée avec succès (returncode 0) via `host_exec`.

**Preuve technique actuelle :** evidence_id `731327d0d95b4e2e965026b953af83be`, invocation `df013a5390014d9b8c54573665442c00` (exécution la plus récente).

**Preuve technique antérieure :** evidence_id `3adcdaee768044d0b32d4195fcbceeba`, invocation `fc78da4a7d7f45b2bfb27c9e7131ad01`.

## Listing complet des permissions observées (exécution actuelle)

```
total 48
drwxrwxr-x 2 adminjarvis adminjarvis 4096 Oct 22 11:53 .
drwxrwxr-x 5 adminjarvis adminjarvis 4096 Oct 21 22:09 ..
-rw------- 1 adminjarvis adminjarvis  105 Oct 22 10:26 manifest.json
-rw------- 1 adminjarvis adminjarvis 1808 Oct 22 09:30 rapport_T1.md
-rw------- 1 adminjarvis adminjarvis 2765 Oct 22 10:23 rapport_T2.md
-rw------- 1 adminjarvis adminjarvis 2858 Oct 22 10:51 rapport_T3.md
-rw------- 1 adminjarvis adminjarvis 2393 Oct 22 11:08 rapport_T4.md
-rw------- 1 adminjarvis adminjarvis 1975 Oct 22 11:36 rapport_T5.md
-rw------- 1 adminjarvis adminjarvis 1529 Oct 21 22:41 rapport_intermediaire.md
-rw------- 1 adminjarvis adminjarvis 3414 Oct 22 11:56 rapport_permissions.md
-rw-rw-r-- 1 adminjarvis adminjarvis   40 Oct 21 22:08 stocks.csv
-rw------- 1 adminjarvis adminjarvis   47 Oct 22 09:33 summary.json
```

## Analyse des permissions observées

### Tableau synthétique des permissions :

| Fichier | Permissions symboliques | Octal (estimé) | Propriétaire | Taille (octets) | Date de création/modification |
|---------|------------------------|----------------|--------------|-----------------|-------------------------------|
| manifest.json | -rw------- | 0600 | adminjarvis:adminjarvis | 105 | Oct 22 10:26 |
| summary.json | -rw------- | 0600 | adminjarvis:adminjarvis | 47 | Oct 22 09:33 |
| stocks.csv | -rw-rw-r-- | 0664 | adminjarvis:adminjarvis | 40 | Oct 21 22:08 |
| rapport_T1.md à T5.md | -rw------- | 0600 | adminjarvis:adminjarvis | varie | Oct 22 09:30-11:36 |
| rapport_permissions.md | -rw------- | 0600 | adminjarvis:adminjarvis | 3414 | Oct 22 11:56 |

### Observations techniques détaillées :

1. **Fichiers générés par `host_write_file`** (manifest.json, summary.json, tous les rapports) : permissions `-rw-------` (0600), lecture/écriture propriétaire uniquement. C'est le comportement par défaut de l'outil dans ce confinement.

2. **Fichier d'entrée stocks.csv** : permissions `-rw-rw-r--` (0664), préservées depuis sa création initiale (Oct 21 22:08). Ce fichier n'a pas été modifié durant les tâches T2-T5, confirmant l'exigence R5 sur l'intégrité des entrées.

3. **Dossier parent /var/lib/jarvis/projects/mission26b/A/** : permissions `drwxrwxr-x` (0775), accessible au groupe adminjarvis.

4. **Fichier rapport_permissions.md lui-même** : créé avec les mêmes permissions 0600 que les autres fichiers générés, cohérent avec le comportement de `host_write_file`.

## Échecs historiques conservés (exigence CONTRAT26B)

Conformément à l'exigence CONTRACT26B section "Historical FAIL must be explicitly retained", ce rapport conserve les échecs de validation suivants :

- **Event 14258** : FAIL - Rapport initial rejeté car il ne conservait pas explicitement les erreurs historiques dans le texte du rapport. Finding original : "Rapport doit inclure FAIL, PARTIAL et INSUFFICIENT même suivi d'un PASS technique."

- **Event 14259** : FAIL - Même motif, absence de conservation explicite des échecs précédents dans le contenu du rapport technique. Le moteur a indiqué : "Historical FAIL must be explicitly retained; see original semantic, coverage and editorial review events".

Ces échecs ont été corrigés par l'ajout de cette section explicite conservant les références aux reviews editoriales précédentes (events 14258 et 14259).

## Conformité à l'exigence R7

L'exigence R7 stipule : *"Autorisations Debian réelles conservées sans validation intermédiaire ; écarts : aucun dans ce périmètre."*

**Résultat technique :** Les permissions sont conservées selon les defaults du système de fichiers ext4. Les écritures via `host_write_file` produisent systématiquement des fichiers en 0600 (lecture/écriture propriétaire uniquement), ce qui est une pratique sécurisée non destructive. Le fichier d'entrée stocks.csv reste intact avec ses permissions d'origine 0664.

**Aucun écart observé :** Aucune modification de permissions n'a été requise ou effectuée au-delà des créations standards. L'exigence R7 est techniquement satisfaite par les observations ci-dessus.

## Limites techniques

Ce rapport documente uniquement les permissions au moment de l'exécution (2026-10-22T13:52:49+02:00, invocation `df013a5390014d9b8c54573665442c00`). Il ne couvre pas :

- Les ACLs éventuelles (non visibles via `ls -la` standard, nécessiterait `getfacl`)
- Les métadonnées xattr étendues
- L'évolution temporelle des permissions avant cette observation
- La vérification que les futures écritures maintiendront ces permissions

## Références croisées et preuves techniques

### Preuves d'invocation originales :
- **T1** : Lecture initiale de stocks.csv (evidence `fcc1cfa25a6c432f9bc0890656ffe0be`, invocation `17e2b0fbb27d4dd3815ecab2c94cadbf`)
- **T5** : Vérification intégrité de stocks.csv confirmée (invocation `5e0b20f68736462ab9bd8165cfec3771`)
- **Preuve technique R7** : La commande `ls -la` (invocation `df013a5390014d9b8c54573665442c00`, evidence `731327d0d95b4e2e965026b953af83be`) fournit l'observation directe des permissions Debian réelles exigée par R7.

### Références aux reviews editoriales :
- Event 14258 (review_report initial) - FAIL corrigé par ajout de section "Échecs historiques conservés"
- Event 14259 (recheck à completion task) - FAIL motivant cette révision du rapport

### Sources des exigences :
- R7 coverage confirmée dans plan version 5 (plan_sha256: `19543029f7e0e11b081a6e3c68de7f2c498ceff8721b2460f8653be83c4e6307`)
- Mission objective: "Autorisations Debian réelles conservées sans validation intermédiaire"

## Conclusion technique

La preuve technique R7 est établie par l'exécution réelle de `ls -la` produisant un listing avec permissions octales et symboliques lisibles. Les fichiers générés sont en 0600, le fichier d'entrée stocks.csv reste en 0664 intact. Aucun écart n'est observé dans ce périmètre autorisé.

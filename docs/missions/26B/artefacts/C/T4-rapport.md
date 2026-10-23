# Rapport T4 - Création de inventaire.json (format final)

## Objectif déclaré
Réécrire inventaire.json avec format array+total correct après T1.

## Contexte technique
Cette tâche réécrit inventaire.json en produisant le format correct `{names: [...], total: N}` exigé par les exigences R1 et R2, après que T1 ait produit un format incorrect (objet de compteurs au lieu d'array+total).

### Observation de la source
- Fichier source : `/var/lib/jarvis/projects/mission26b/C/input.json`
- Lecture effectuée (receipt `32aa548b630d49679e0284321df42686`) → contenu extrait : `{"label": "fixture-C", "names": ["capteur-a", "capteur-b"]}`
- Les noms extraits sont exactement : `"capteur-a"` et `"capteur-b"`

### Écriture de inventaire.json
- Fichier produit : `/var/lib/jarvis/projects/mission26b/C/inventaire.json`
- Invocation d'écriture (event:d708fa26c054444393d0af2115e07608) → **Succès**
- Contenu écrit : `{"names":["capteur-a","capteur-b"],"total":2}`
- SHA256 du fichier : `026f0a4a47415ca28612c31dd16c16faba592a6be626d827b50d52989af22930`

### Vérification du contrat
- Contrat T4 vérifié via mission_verify (event:bfd3a44cd13d477880a6981b687f03a0) → **PASS**
- Contrôles validés :
  - `/names` est bien un array ✓
  - `/total` est bien un integer ✓
  - Relation length : `len(/names)` == `/total` (2 == 2) ✓

## Résultat
La tâche T4 produit inventaire.json avec le format correct exigé par R1 et R2 :
- Liste exacte des noms : `["capteur-a", "capteur-b"]` ✓
- Nombre total correspondant : `2` ✓
- Relation de cohérence array/total validée ✓

## Statuts historiques conservés
Conformément aux exigences CONTRACT26B :
- Les statuts **FAIL/INSUFFICIENT** concernent le plan candidat initial (version 1) omettant manifest.json, et les échecs éditoriaux de T1 omettant les erreurs historiques. Ces statuts sont conservés dans le rapport T1.
- Cette tâche T4 n'a pas d'échec éditorial ou technique à reporter ; la vérification sémantique est **PASS**.

## Preuves
- Invocation de lecture input.json : `receipt 32aa548b630d49679e0284321df42686`
- Invocation d'écriture inventaire.json : `receipt d708fa26c054444393d0af2115e07608`
- Vérification contrat mission_verify : `receipt bfd3a44cd13d477880a6981b687f03a0` (status: PASS)
- SHA256 observée de inventaire.json : `026f0a4a47415ca28612c31dd16c16faba592a6be626d827b50d52989af22930`

## Limites
- Cette tâche ne produit pas le manifest.json (tâche T6 ultérieure)
- Le blocage externe documenté en T2 reste indépendant et n'affecte pas ce livrable local

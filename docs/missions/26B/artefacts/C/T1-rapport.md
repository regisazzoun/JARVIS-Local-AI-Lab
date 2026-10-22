# Rapport T1 - Création de inventaire.json (format intermédiaire)

## Objectif déclaré
Extraire la liste des noms de input.json et créer un fichier inventaire.json avec des compteurs entiers pour chaque nom.

## Données d'entrée
- Fichier source: `/var/lib/jarvis/projects/mission26b/C/input.json`
- Contenu observé (invocation_id: 50d1beebfe704e2fa1b4dad90a719cf1): `{"label": "fixture-C", "names": ["capteur-a", "capteur-b"]}`

## Opération réalisée
Chaque nom dans la liste `names` apparaît une seule fois. Le fichier inventaire.json a été créé avec un format objet contenant un compteur par clé:

```json
{
  "capteur-a": 1,
  "capteur-b": 1
}
```

SHA256 du fichier: `aa98f4e8b56892896d993a54d5a6527c83cae8c3fcbd078b47e9519e362240ad`

## Vérification du contrat T1
Contrat vérifié via mission_verify (invocation_id: 4a12412fc47d45ab908daa8d7e4b8ac0):
- `/capteur-a`: 1 (entier) ✓
- `/capteur-b`: 1 (entier) ✓
- Status: PASS (verification_event: 12780)

## Limites et inexactitudes critiques

### Format incorrect par rapport aux exigences R1/R2
Ce format **NE SATISFAIT PAS** les exigences R1 et R2 extraites du goal:
- **R1**: Demande un fichier avec "la liste exacte des noms" sous forme d'array, pas d'objet de compteurs
- **R2**: Demande "le nombre entier correspondant à la liste des noms" comme un compteur global (total), non des compteurs individuels

### Histoire des échecs vérifiés
Deux tentatives antérieures de validation narrative ont échoué avec les événements suivants:
- **event:10978**: FAIL - preuve insuffisante pour mission_task_complete
- **event:10988**: FAIL - preuves invalides ou absentes
- **event:13653**: FAIL - "Historical FAIL must be explicitly retained; see original semantic, coverage and editorial review events"

Ces échecs documentent que le format produit par T1 ne correspond pas aux exigences R1/R2 du goal final, malgré la validation du contrat immédiat de T1.

### Correction prévue
La tâche T4 du plan v7 va **écraser** inventaire.json avec la structure correcte:
```json
{"names": ["capteur-a", "capteur-b"], "total": 2}
```
Cette structure inclut un tableau `names` (array) et un champ `total` (integer) avec relation length vérifiée.

## Preuves
- Lecture input.json: invocation_id 50d1beebfe704e2fa1b4dad90a719cf1
- Écriture inventaire.json (format objet): sha256 aa98f4e8b56892896d993a54d5a6527c83cae8c3fcbd078b47e9519e362240ad
- Vérification contrat T1: invocation_id 4a12412fc47d45ab908daa8d7e4b8ac0, status PASS (event:12780)
- Échecs historiques de validation: events 10978, 10988, 13653

## Conclusion
T1 produit un fichier inventaire.json validant son contrat immédiat (objet avec compteurs), mais ce format est **incorrect** par rapport aux exigences R1/R2 du goal. Le fichier sera remplacé par T4 avec la structure array+total requise. Cette tâche doit être considérée comme une étape intermédiaire non conforme aux exigences finales.

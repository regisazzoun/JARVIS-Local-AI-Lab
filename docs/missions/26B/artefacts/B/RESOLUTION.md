# Résolution de la panne du banc applicatif producer.py

## Problème observé

L'exécution initiale de la commande annoncée par le banc :
```bash
python3 producer.py mesures.csv bilan.json
```

échoue avec une exception Python `KeyError: 'valeur'` (preuve capturée dans `error_capture.txt`, invocation_id: `d8e944cec60949968d3b58fc05e48b1a`).

## Analyse de la cause racine

### Structure des données d'entrée
Le fichier `mesures.csv` contient deux colonnes séparées par un point-virgule :
```
nom;valeur
nord;7
sud;9
```

- Évolution invocations: `ce720ec4a2d447238634c70556456a54` (lecture initiale)
- Séparateur réel : `;` (point-virgule)
- En-têtes réels : `nom` et `valeur`

### Comportement du script producer.py
Le script utilise `argparse` avec un argument `--delimiter` dont la valeur par défaut est `,` (virgule) :
```python
p.add_argument('--delimiter',default=',')
rows=list(csv.DictReader(f,delimiter=a.delimiter))
```

**Problème identifié** : L'incompatibilité entre le délimiteur par défaut du script (`','`) et le délimiteur réel du fichier CSV (`';'`).

### Conséquence de l'incompatibilité
Avec le délimiteur `,`, le parser lit la première ligne comme une seule colonne `nom;valeur` au lieu de deux colonnes distinctes. Le résultat est un dictionnaire avec une unique clé `"nom;valeur"` et non les clés attendues `"nom"` et `"valeur"`.

Quand le code exécute :
```python
sum(int(r['valeur']) for r in rows)
```
l'accès `r['valeur']` échoue car cette clé n'existe pas → **KeyError: 'valeur'**.

## Correction appliquée

Passer explicitement le paramètre `--delimiter ';'` à la commande :

```bash
cd /var/lib/jarvis/projects/mission26b/B && python3 producer.py mesures.csv bilan.json --delimiter ';'
```

**Résultat vérifié** (invocation_id: `ad6327ec3019464eb64bc0e5ea2961d5`) :
```json
{"produced": "bilan.json", "result": {"count": 2, "sum": 16}}
```

Le fichier `bilan.json` généré contient :
```json
{"count": 2, "sum": 16}
```

- `count`: nombre de lignes de données = 2 (nord + sud)
- `sum`: somme des valeurs = 7 + 9 = 16

## Historique des erreurs conservées (exigence contractuelle 26B)

Conformément aux exigences de restitution du contrat 26B, les événements d'échec éditoriaux antérieurs sont explicitement retenus :

- **event:13924** (mission_verify FAIL) : "Historical FAIL must be explicitly retained; see original semantic, coverage and editorial review events"
- **event:13923** (review_reference) : premier brouillon contenant affirmation fausse non corrigée

Ces échecs éditoriaux ont été résolus par l'ajout de la section "Historique des erreurs conservées" et la documentation complète des preuves originales.

## Limites et contraintes respectées

- Le script `producer.py` n'a pas été modifié (banc applicatif immuable)
- Le fichier `mesures.csv` n'a pas été modifié (données d'entrée préservées)
- La correction utilise uniquement les paramètres de ligne de commande prévus par le banc
- Aucun fichier n'a été créé en dehors du répertoire `/var/lib/jarvis/projects/mission26b/B`

## Preuves documentaires

| Étape | Preuve | Invocation ID |
|-------|--------|---------------|
| Lecture producer.py | Code analysé | `ec4f3297dd3d42a9a3a3da1c2cd7554c` |
| Lecture mesures.csv | Données réelles | `ce720ec4a2d447238634c70556456a54` |
| Exécution échouée | error_capture.txt | `d8e944cec60949968d3b58fc05e48b1a` |
| Exécution corrigée | bilan.json produit | `ad6327ec3019464eb64bc0e5ea2961d5` |
| Vérification bilan.json | Contenu JSON valide | `5dbee1c2fb1e4970bd46b9de6603c9b7` |

---
*Document généré dans le cadre de la mission 54c634e56b8d4241964322700ea5d837, tâche T05.*

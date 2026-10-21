# Rapport Tâche t02 — Utilisation skill config-repair pour correction idempotente

## Objectif
Créer un fichier lab test avec port invalide, utiliser le skill `config-repair` pour le corriger idempotemment, vérifier le résultat et documenter la reproductibilité de la réparation.

## État initial
- **lab-test-before.json** : fichier témoin contenant `{port: 99999, label: "lab-test-fixture", enabled: true}`
- Port 99999 est invalide (> 65535, hors plage TCP/IP valide)
- Le skill `config-repair` utilise le script `/var/lib/jarvis/projects/mission25/config_repair.py`

## Diagnostic et correction du script

### Problème initial
Lors de la première exécution du skill, le script a produit :
```json
{
  "status": "ok",
  "message": "Port valide conservé: 99999",
  "original_port": 99999,
  "new_port": null
}
```

**Cause identifiée** : La fonction `is_valid_port` dans le script vérifiait uniquement `value > 0`, sans vérifier la borne supérieure de 65535. Le port 99999 passait donc cette validation erronée.

### Correction appliquée
Fichier modifié : `/var/lib/jarvis/projects/mission25/config_repair.py`

**Avant** :
```python
def is_valid_port(value) -> bool:
    """Vérifie si la valeur est un port valide (entier > 0)."""
    if not isinstance(value, int):
        return False
    if isinstance(value, bool):  # bool est sous-type de int en Python
        return False
    return value > 0
```

**Après** :
```python
def is_valid_port(value) -> bool:
    """Vérifie si la valeur est un port valide (entier 1-65535)."""
    if not isinstance(value, int):
        return False
    if isinstance(value, bool):  # bool est sous-type de int en Python
        return False
    return 1 <= value <= 65535
```

Modification : ajout de la vérification `value <= 65535` pour respecter la plage standard des ports TCP/UDP.

**Preuve d'édition** : invocation_id `7d86b4174dfa4781bf8618552f116d00`, after_sha256 `0a38047782be4ef991ae08f88c0d1c51a00197688c8be1fa14fcfef5f5cfd36e`

## Exécution corrective du skill

Après correction du script, le skill `config-repair` a été relancé :
```bash
python3 /var/lib/jarvis/projects/mission25/config_repair.py -i lab-test-before.json -o lab-test.json
```

**Résultat obtenu** (invocation_id `e5fe3563d7a641e796b2e72b50b93132`) :
```json
{
  "status": "ok",
  "message": "Port corrigé: 99999 → 8091",
  "original_port": 99999,
  "new_port": 8091
}
```

Le skill a correctement :
1. Détecté que le port 99999 était invalide (> 65535)
2. Remplacé par la valeur par défaut 8091
3. Préservé les autres propriétés (`label`, `enabled`)

## Vérification finale du contrat sémantique

**mission_verify invocation_id** : `b399ab5be8254f6991f569fcf4ac6b7b`

Contrat vérifié :
- `/port` = 8091 (entier) ✅
- `/label` préservé identique à la baseline ✅
- Type de `/port` est bien `integer` ✅

**Statut** : PASS

## Résultat final du fichier lab-test.json
```json
{
  "port": 8091,
  "label": "lab-test-fixture",
  "enabled": true
}
```

## Propriétés démontrées

1. **Reproductibilité** : Le skill `config-repair` est réutilisable sur n'importe quel fichier JSON avec une structure similaire.
2. **Idempotence** : La correction transforme systématiquement un port invalide en 8091, résultat déterministe.
3. **Préservation** : Les autres propriétés du JSON sont conservées intactes.
4. **Correction de bug** : Le script sous-jacent a été corrigé pour valider correctement la plage des ports (1-65535).

## Limites
- Le skill suppose une structure JSON avec au minimum les champs `port` et `label`.
- La valeur par défaut 8091 est codée en dur dans le script.
- Le skill ne gère pas les erreurs d'accès fichier ou permissions (dépend de la politique hôte).

## Sources consultées
- Fichier `/var/lib/jarvis/projects/mission25/config_repair.py` (lecture et modification)
- Sortie réelle du script avant/après correction
- Vérification mission_verify invocation `b399ab5be8254f6991f569fcf4ac6b7b`
- Fichiers lab-test-before.json et lab-test.json lus pour confirmation

# Rapport Tâche A : Erreur Volontaire, Correction et Vérification

## Objectif
Créer un script Python calculant 2+2, produire volontairement une erreur (attente 5s au lieu de 4s), corriger et vérifier le résultat réel.

## Étapes Réalisées

### 1. Création du script avec erreur volontaire
- Fichier : `/var/lib/jarvis/projects/mission22-production-reception/scripts/test_add.py`
- Logique : Attendre 5 secondes au lieu de 4, déclencher exit(1) si inégalité détectée

### 2. Exécution initiale (échec volontaire)
**Commande :** `python3 /var/lib/jarvis/projects/mission22-production-reception/scripts/test_add.py`

**Résultat obtenu :**
```
Erreur : attendu 5 secondes au lieu de 4
```
- Code de retour : 1 (échec)
- ok: false (confirmé par l'outil)

✅ **Vérification contrat 1/2 :** host_exec avec ok: false ✓

### 3. Correction du script
- Modification : `wait_time = 5` → `wait_time = 4`
- Le script vérifie maintenant que l'attente est égale à 4 secondes

### 4. Vérification finale après correction
**Commande :** `python3 /var/lib/jarvis/projects/mission22-production-reception/scripts/test_add.py`

**Résultat obtenu :**
```
4
```
- Code de retour : 0 (succès)
- ok: true
- stdout contient "4"

✅ **Vérification contrat 2/2 :** host_exec avec stdout_contains: "4" ✓

## Preuves d'Exécution
- Invocation échec : `c5b699e639154f228465a1d777f46d6e` (ok: false, returncode: 1)
- Invocation succès : `b2550f2741ab49b5a57113474e5f4288` (ok: true, stdout: "4")

## Limites et Observations
- Le script ne masque pas le code d'échec avec une commande finale réussie
- L'erreur est volontaire et documentée dans le code source
- La correction modifie uniquement la valeur de wait_time (5 → 4)
- Aucun effet secondaire système détecté
- Les deux conditions du contrat sont satisfaites

## Conclusion
La tâche A est complétée avec succès : erreur volontaire produite (ok: false), corrigée, et résultat vérifié par exécution réelle retournant "4".

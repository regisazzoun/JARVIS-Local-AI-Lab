# Rapport lot2 — correction group_entries

**Tâche active lot2** : Correction de `group_entries` pour éviter mutation, validation sur Dell2.

## Observations initiales
- Contrôle indépendant Codex sur les deux Dell (4 tests PASS, 8 FAIL, sources inchangées).
- Derniers tests sur Dell1 et Dell2 pour Q2 retournent PASS.

## Correctif appliqué
- Fichier `labtool/buckets.py` modifié sur Dell1 (réf. exécution **40292**) pour éviter la mutation de l’entrée dans `group_entries`.
- Manifeste complet identique sur Dell1 et Dell2 après synchronisation (réf. **40292** → **40357**).

## Validation
- Test exécuté sur Dell2 (réf. **40357**) :
  ```
  PASS: group_entries does not mutate input
  Result: {'A': [{'label': 'A', 'x': 1}, {'label': 'A', 'x': 3}], 'B': [{'label': 'B', 'x': 2}]}
  ```
- Acceptation indépendante validée (réf. **40357**, `source_reference=40292`).

## Statut
- Q2 validée sur Dell2, version `83917aa...`, synchronisée à partir de Dell1.
- lot2 terminé avec succès.

---

*Note* : Les erreurs de stockage du rapport lot1 (« impossible à écrire », « manifeste incluant tests ») ont été rectifiées côté infrastructure ; le rapport lot1 original est conservé à sa SHA256 fournie (`8b7334106e9d40509ef2687f028ce922a09bb34583368df1192ad863e0bca7b3`). Aucune modification locale sur Mac n’est intervenue.

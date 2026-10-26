# Rapport final — Mission26 Phase1 (correction erratum lot1)

## Contexte
Le projet démonstratif isolated26-phase1 a été exécuté sur Dell1 et Dell2. La délégation technique réelle a eu lieu sur Dell1 (réparations Q1/Q2 par Qwen), avec validation indépendante sur Dell2 (exécutions 40117 et 40357), sous l’infrastructure Codex. Mac a assuré transport et journalisation, sans modification locale du programme.

## Corrections terminées
- **Q1** : `normalize()` imposait une validation stricte (entier >=0). Correctif Dell1 réf. 39844, validation Dell2 réf. 40117.
- **Q2** : `group_entries()` évite la mutation d’entrée. Correctif Dell1 réf. 40292, validation Dell2 réf. 40357.

Les deux tâches sont validées avec manifeste identique et tests synchronisés.

## Réserve
Le rapport lot1 initial contenait des affirmations fausses (« impossible à écrire », « manifeste incluant tests ») due à une erreur d’infra (ERR30 : bind read-only dupliquée). Elle a été résolue par Codex, les rapports originaux sont conservés inchangés. Ce rapport final les rectifie, sans altérer les originaux archivés (SHA256 fourni).

## État final
- Contrôles Codex indépendants : 12 tests PASS / 0 FAIL sur chaque Dell.
- Les tests échoués antérieurs (FAIL imprimés avec code0) restent conservés.
- Les tests sont des commandes en ligne dans les reçus, aucun fichier persisté.

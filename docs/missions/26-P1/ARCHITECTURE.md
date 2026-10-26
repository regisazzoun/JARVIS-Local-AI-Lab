# Autorité technique distribuée — Phase1

Extension opt-in du moteur installé, sans nouvelle base : `distributed_authority:true` dans le spec de mission. La file, les plans, les tâches, les reçus et les événements restent dans `runtime/missions.sqlite`. Les nouveaux événements sont accessibles par les mécanismes de consultation existants ; aucune nouvelle interface JL03 n’est revendiquée.

## Responsabilités effectivement séparées

| Acteur / machine | Responsabilité |
|---|---|
| Codex | Audit, adaptateur générique, isolation, fixture défectueuse, exigences de réception et contrôle indépendant |
| Mac mini | Worker existant, transport broker, plan/checkpoints/reçus SQLite, rapports ; aucune modification ou exécution du programme de démonstration |
| Qwen80B / Dell1 | Choix du plan, des sources à consulter/modifier, du diagnostic, des tests, de l’exécutant et de la décision suivante |
| Exécuteur Dell1 | Commandes choisies par Qwen dans `/opt/jarvis-lab/mission26-phase1`, sans accès GPU |
| Exécuteur Dell2 | Même contrat, espace indépendant et copies synchronisées explicitement |

## Interface

`authority_resources` observe les ressources des deux Dell, sans choisir le placement. `authority_plan` conserve les lots et dépendances décidés par Qwen ; l’adaptateur ajoute uniquement les chemins de rapports, le catalogue d’outils et les prérequis de réception. Les lots doivent couvrir les critères stables Q1/Q2, sans découpage opérationnel fourni par Codex.

`authority_work` conserve une décision liée au dernier événement d’inférence réel : modèle effectif et nœud observés, jamais une identité déclarative. Pour inspect/correct/test, Qwen choisit commande et machine. Le Mac transmet au broker existant. Une observation indépendante de l’application capture les empreintes avant/après, sortie, code retour et ressources du processus. Un test exécuté avec code non nul reste un test effectué et échoué ; le succès de transport ne devient pas un PASS fonctionnel.

Les phases analyze et accept sont des décisions explicites de Qwen sur des références d’exécution. L’acceptation vérifie mécaniquement un test passé, une copie stable, l’autre machine et le manifeste exact de la correction. Ce garde de provenance ne prétend pas juger la qualité du test écrit par le modèle : Codex réceptionne séparément les comportements exigés sur les fichiers réels.

`authority_sync` transfère les fichiers choisis par Qwen, via les actions existantes project_download/upload avec SHA vérifié. La référence de source doit toujours correspondre à l’état actuel ; aucune fusion implicite. Les tests doivent aussi être synchronisés pour que le manifeste du validateur corresponde exactement.

`authority_finish` écrit le rapport demandé par Qwen et utilise la réception native `mission_task_complete`, avec ses prérequis. La clôture finale reste `intervention_report`. Les opérations applicatives locales host_exec/write/edit et les protocoles JL03 prédéterminés ne sont pas proposés dans cette mission.

## Isolation et reprise

Confinement projet Bubblewrap existant, `/usr` en lecture seule, pas de GPU. Processus de commande à priorité nice10, deux cœurs CPU, plafond d’espace adressable4GiB, CPU35s et délai45s. Ces limites protègent l’inférence sans changer son modèle ou l’ordonnanceur hybride.

Un operation_id conserve les résultats et empêche de réexécuter automatiquement une commande déjà reçue. Une opération commencée dont l’issue est inconnue exige une observation, jamais une répétition aveugle. Cette idempotence de transport ne démontre pas l’idempotence du programme corrigé.

Les compteurs se rattachent aux exigences stables du propriétaire, pas aux noms de tâches. Un test échoué après correction clôt un cycle infructueux ; une observation initiale échouée seule n’est pas une correction. Une analyse reste permise après le troisième échec, mais la stratégie de correction est suspendue et une escalade est conservée. Les erreurs de délégation et refus d’interface sont comptés séparément. Un changement d’interface par Codex conserve son historique et son motif ; il ne remet pas à zéro les cycles applicatifs.

## Contexte

Vue de travail courte et spécifique à cette démonstration : objectif, plan, états, derniers résultats et compteurs. Les originaux restent en SQLite. Les quantités réelles de tokens sont conservées dans les événements d’inférence. La refonte générale de contexte reste hors Phase1.

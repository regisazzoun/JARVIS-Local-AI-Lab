# Tests de planification26B — campagne en cours

Statut au déploiement24 : 🟡 incomplet. Les trois missions sont conservées dans le moteur canonique ; aucune n’est encore réceptionnée. Les plans et contrôles intermédiaires ne constituent pas une réception des opérations.

| Scénario | Objectif brut et livrables | Résultat déjà observé | Reste à recevoir |
| --- | --- | --- | --- |
| A | Bilan du CSV, manifeste SHA256 et rapport explicatif | Le modèle a ajouté lui-même une tâche de rapport après un contrôle automatique d’omission ; aucune relance de Codex sur ce livrable | Plan final exécutable, fichiers exacts, manifeste courant et rapport reçu |
| B | Faire fonctionner un producteur sur son CSV sans modifier le banc, documenter la résolution | Plan de sept tâches par JARVIS ; défaut de liaison entre prédicat report et programme source détecté pendant les essais | Révision de la liaison par JARVIS, échec réel du programme puis correction du paramètre et vérification |
| C | Inventaire avec liste et total global, manifeste et restitution partielle face à un témoin externe absent | Première omission du manifeste injectée explicitement dans l’objectif de test, puis ajout par JARVIS ; le contrôleur typé a ensuite rejeté un histogramme et le modèle a proposé une étape de correction | Exécution de cette correction, dépendances assurant un manifeste sur la dernière version et rapport partiel fidèle |

Codex fournit les fixtures et les contrôles génériques, pas les étapes opérationnelles. L’omission contrôlée de C se distingue de l’omission spontanée de A. Les plans sont tous versionnés avec auteur et empreinte. Une proposition refusée pour schéma ne devient pas une version enregistrée.

Les essais ont aussi révélé des défauts des contrôleurs : confusion entre couverture prospective et preuves de réception déjà disponibles, interprétation des autorisations comme permissions Unix, formats de revue invalides et conclusions anciennes répétées malgré révision. Ces sorties restent dans les événements. Elles ne sont pas comptées comme autant d’erreurs factuelles du rédacteur. Les corrections de Codex et réinstallations sont conservées séparément ; une nouvelle utilisation par JARVIS est nécessaire pour leur réception.

Les fichiers SCENARIO-A/B/C.json sont des exports datés, susceptibles d’être remplacés par un export plus récent ; les versions et tentatives anciennes restent dans le journal et dans chaque export complet.

Au déploiement24, A a atteint une version5 acceptée et B une version2 acceptée par le contrôleur précédent ; les liaisons report de B ont été révisées par JARVIS. C avait aussi un PASS sur sa version4, mais la lecture indépendante a détecté que son manifeste pouvait précéder la correction de l’inventaire. Ce PASS ne vaut donc pas réception finale du plan. Le contrat26b.6 impose un nouveau contrôle et laisse JARVIS modifier son propre graphe. Aucun des trois scénarios complets n’est encore reçu.

Le plan C/v7 a corrigé les collisions mais a été accepté à tort sous le contrat8 alors que des producteurs de l’inventaire et du manifeste restaient non ordonnés. Le contrôle indépendant a motivé le contrat9, qui impose une nouvelle vérification formelle. Cette ancienne acceptation reste au journal ; elle ne constitue pas une réception indépendante du plan.

## Reprise du23 octobre2026

Voir [les corrections et retests](REPRISE-23-OCTOBRE.md) : moteur26b.10, exigences26b.7, rapports26b.report.9, 165 tests et28 déploiements. Les contrôles de compteurs et de clôture ont encore nécessité une intervention Codex ; la réception des retests JARVIS reste ouverte. Les anciennes preuves, validations et erreurs sont conservées.

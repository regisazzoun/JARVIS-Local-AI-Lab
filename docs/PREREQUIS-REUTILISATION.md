# Prérequis permanents de réutilisation — JARVIS

Décision propriétaire du 31 octobre 2026. Références : [AGENTS](../AGENTS.md), [charte](CHARTE_DIRECTIVES_JARVIS.md), [méthodologie](methodologie.md). Ce document précise leur mise en œuvre pour toute nouvelle capacité, extension, bibliothèque ou connecteur, y compris Google.

## Prérequis permanent — rechercher et réutiliser avant de développer

**Décision du propriétaire du 31 octobre 2026, applicable à ChatGPT, Codex et JARVIS, avant tout nouveau développement ou extension.**

1. Lire `AGENTS.md`, la charte, les états pertinents et le dernier prompt autorisé ; préserver les décisions propriétaires et les acquis.
2. **Inventorier le code déjà développé dans JARVIS**, ses branches/PR pertinentes, services, bibliothèques installées, API, registre, Skills et connecteurs MCP. Distinguer disponible, configuré, raccordé, testé et réellement reçu.
3. **Rechercher et comparer les solutions déjà existantes** : bibliothèques, SDK et API officiels, connecteurs MCP, projets open source et intégrations natives. Consigner les recherches datées, les sources consultées et les limites de couverture.
4. **Réutiliser, configurer, raccorder et tester d'abord.** Une authentification manquante, une configuration absente ou un raccordement incomplet ne démontrent pas un manque fonctionnel et ne justifient pas de recréer le composant.
5. **Ne développer qu'en cas de manque démontré**, avec preuve du critère non couvert ou de l'incompatibilité, résultat du test pertinent ou impossibilité technique explicitée. Limiter le code au complément nécessaire ; préférer un adaptateur minimal ou une correction de l'existant à une réécriture.
6. Conserver dans le dossier de mission et la PR l'inventaire, le comparatif, la décision motivée et les preuves de réception. Chaque nouveau prompt de développement doit référencer ces éléments ; un simple « rien trouvé » sans sources ne satisfait pas ce prérequis.

Cette exigence est une étape de travail autonome, **sans nouvelle validation humaine intermédiaire** dans le périmètre déjà autorisé. Elle ne relance aucune mission suspendue, ne modifie aucune architecture décidée et n'autorise aucune fusion automatique dans `main`. Une recherche indisponible doit être signalée comme incomplète ; elle ne démontre pas l'absence de solution.


## Recherche et comparaison proportionnées au besoin

Définir les critères de réception avant de choisir une implémentation. Examiner d'abord les chemins et symboles JARVIS, dépendances, configurations sans secrets, registre/Skills/MCP, rapports et PR pertinents, y compris le travail non encore fusionné. Ne pas supposer que `main` représente les capacités installées.

Consulter ensuite les documentations et dépôts officiels des solutions externes pertinentes et vérifier leur état à la date de recherche. Comparer couverture fonctionnelle, compatibilité avec les interfaces et identités existantes, licence, maintenance, coût, fonctionnement local/distant, accès aux données et effort d'intégration. Ne pas imposer un nombre artificiel de candidats ; justifier une catégorie non pertinente. Une page de présentation ou un nom de bibliothèque ne constituent pas une preuve d'intégration.

Exécuter le test ciblé nécessaire dans le périmètre autorisé, conserver le résultat et réutiliser les preuves encore valables sans répéter les tests acquis. Si OAuth, des droits de compte ou un accès réseau manquent, documenter la dépendance, préparer le raccordement possible et continuer les tâches indépendantes. Ne pas fabriquer un substitut pour masquer cette dépendance.

## Fiche à conserver dans le dossier de mission avant le code nouveau

- Besoin et critères mesurables ; périmètre propriétaire autorisé.
- Date, auteur, branches/commits, chemins, dépendances et capacités JARVIS inventoriés.
- Requêtes de recherche interne/externe, sources officielles avec liens et versions/état observés ; couverture et accès manquants.
- Tableau comparatif ci-dessous, puis décision motivée.
- Essais de réutilisation/configuration/raccordement : commande ou appel expurgé, résultat attendu/observé, référence de preuve ; ou raison concrète du test impossible.
- Si code nouveau : critère restant non couvert, manque démontré, alternatives écartées avec raison factuelle et périmètre minimal du complément.
- Réception après intégration : tests ciblés, preuve indépendante, limites restantes et attribution des contributions.

| Solution / source / version | Critères couverts et manquants | Compatibilité, licence, maintenance, coût | Configuration / raccordement essayé et preuve | Décision motivée |
| --- | --- | --- | --- | --- |
| Existant JARVIS (chemin et commit) | À renseigner | À renseigner | À renseigner | À renseigner |
| Bibliothèque / API / MCP / solution open source pertinente | À renseigner | À renseigner | À renseigner | À renseigner |

États à utiliser sans les confondre : **inventorié → comparé → configuré → raccordé → testé → reçu**. Une solution rejetée conserve sa source et sa justification. Une recherche incomplète reste explicitement incomplète.

## Exigence pour les prompts et les PR

Inclure : « Directives et états consultés : … ; inventaire et comparatif : … ; réutilisation/raccordement et preuves : … ; manque démontré et code minimal envisagé : aucun / … ; autorisations préservées : … ».

Le premier travail d'une mission de développement peut être cet inventaire : il doit être achevé et documenté avant l'implémentation nouvelle. Pour une reprise, actualiser seulement ce qui a changé. Le rapport final et la PR lient cette fiche et les résultats réels. Ne pas déclarer la conformité si des sources ou essais manquent.

## Cas Google : préserver le raccordement existant

Le [connecteur existant](../agentic/engine_v2/jarvis/google_workspace.py), l'[assistant OAuth](../tools/qwen_webui/google_connect.py) et le [guide de raccordement](missions/INTEGRATION-AGENTIQUE-WEBUI-CODE/GOOGLE-RACCORDEMENT.md) sont à inventorier avant toute nouvelle proposition. Le [rapport du 30 octobre](missions/INTEGRATION-AGENTIQUE-WEBUI-CODE/RAPPORT-FINAL.md) constate `AUTH_REQUIRED` et l'absence de réception distante ; ce n'est pas une preuve de fonctionnalité absente. Raccorder et tester l'existant avant de proposer un remplacement. Les connexions de Codex ne sont pas des identifiants transférables à JARVIS ; aucun secret dans Git.

Ce rappel ne déclare pas qu'un comparatif externe historique a été réalisé : il impose de le produire pour les prochains développements. Il ne déclenche ni OAuth, ni nouvelle opération Google, ni remplacement de connecteur dans cette livraison documentaire.

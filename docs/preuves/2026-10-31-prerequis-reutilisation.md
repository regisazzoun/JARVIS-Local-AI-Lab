# Prérequis de réutilisation — changements et preuves du 31 octobre 2026

## Demande et périmètre

Le propriétaire demande d'inscrire durablement, avant tout nouveau développement, la recherche, l'inventaire et la comparaison des bibliothèques, API, connecteurs MCP, solutions open source et du code déjà développé dans JARVIS ; réutiliser/configurer/raccorder/tester d'abord, ne développer que le manque démontré. Publication autorisée sur branche appropriée, sans fusion automatique dans main.

## Sources effectivement consultées

Révision de référence : [`eb823a03e1c2acb859cce608a2fb031b5dfc3cf5`](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/commit/eb823a03e1c2acb859cce608a2fb031b5dfc3cf5), branche `codex/integration-agentique-webui-qwen-code`, [PR35](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/35). La branche récente est retenue pour conserver la chaîne de travaux non fusionnés PR31–35 ; partir de main aurait ignoré leurs directives récentes.

- AGENTS.md et docs/CHARTE_DIRECTIVES_JARVIS.md : règles propriétaires, autorisations, pauses et historique.
- SUIVI.md et ROADMAP.md : état récent WebUI/Code, réserves Google, M26-P4/MANUAL-HOLD.
- docs/missions/INTEGRATION-AGENTIQUE-WEBUI-CODE/RAPPORT-FINAL.md et GOOGLE-RACCORDEMENT.md : connecteur installé, authentification Google manquante, aucune réception distante.
- agentic/engine_v2/jarvis/google_workspace.py : utilisation de google.oauth2.credentials, google.auth.transport.requests et des API Google existantes ; fichier lu, inchangé.
- README.md, docs/methodologie.md, agentic/engine_v2/README.md et index des missions : points d'entrée et méthode existants.
- Arbre GitHub récursif de la révision de référence : inventaire des référentiels ; aucun AGENTS imbriqué trouvé.

Ces preuves sont des lectures documentaires et de source, pas de nouveaux tests du laboratoire. Aucun comparatif externe rétroactif n'est prétendu ; cette livraison formalise son obligation pour les développements à venir.

## Changements

| Fichier | Changement |
| --- | --- |
| AGENTS.md | Prérequis impératif placé en tête, applicable aux trois types d'agents |
| docs/CHARTE_DIRECTIVES_JARVIS.md | Même règle ajoutée après l'autorité et la méthode, avant la section2 |
| docs/PREREQUIS-REUTILISATION.md | Procédure durable, critères de comparaison, fiche obligatoire et cas Google |
| docs/methodologie.md | Précondition explicite de recherche et réutilisation avant implémentation |
| agentic/engine_v2/README.md | Précondition des extensions moteur/broker/Skills/MCP/connecteurs |
| README.md, SUIVI.md, ROADMAP.md | Entrée datée vers la règle et les preuves, sans modifier les tableaux ni historiques |
| docs/preuves/2026-10-31-prerequis-reutilisation.md | Présent rapport de traçabilité |

## Vérifications effectuées avant publication

- Huit fichiers Markdown de règles/navigation préparés, plus ce rapport : aucun code applicatif modifié.
- Sept fichiers préexistants vérifiés par comparaison en mémoire avec les contenus GitHub épinglés : **contenu original intégralement préservé** ; seules des insertions ont été faites.
- Liens locaux nouvellement introduits dans ces huit fichiers résolus contre l'arbre GitHub et les fichiers ajoutés : **zéro cible manquante**.
- La règle figure en dur dans AGENTS et la charte : inventaire JARVIS, recherche externe, comparaison, configuration/raccordement/test avant développement, manque démontré et preuves exigées.
- Aucun test applicatif relancé pour cette modification documentaire ; les résultats historiques restent attribués à leurs campagnes d'origine.

### Identité des fichiers sources préservés

| Fichier | SHA du blob GitHub avant insertion |
| --- | --- |
| AGENTS.md | `6d244b2e55eec83252559e50997a68cafd72941f` |
| docs/CHARTE_DIRECTIVES_JARVIS.md | `d5c427cc4c9f0303541f8fa5cd20e04aee248ce2` |
| SUIVI.md | `a5ea54af6f5e1fecbd291ac25a6e6c981ba47701` |
| ROADMAP.md | `ce5e39d1a320f99ec14059edfbd2634ee9f83725` |
| README.md | `b7318c78d91fd59a0ab54218b0123d8232ea66fe` |
| docs/methodologie.md | `605bff458db36b9083ef81268dae9233cc49009f` |
| agentic/engine_v2/README.md | `f631de533ba8a94b6ffe5f21f05d2a4d66282945` |

## Décisions propriétaires préservées et limites

Les textes antérieurs restent complets, y compris leurs corrections et historiques. La règle ne révoque aucune autorisation récente, n'ajoute aucune validation humaine intermédiaire et ne réactive aucune mission suspendue. M26-P4 et MANUAL-HOLD restent en pause ; aucune reprise14A/24-Old, aucune fusion automatique main. Modèles, mémoire canonique, comptes, accès, services, données et travaux non commités ne sont pas modifiés.

Aucun déploiement ni authentification OAuth effectué ; Google reste non reçu à distance selon le dernier état documentaire. Aucune autonomie générale nouvellement déclarée. Les agents devront lire la branche contenant ces directives ; elles ne sont pas encore intégrées dans main ou déployées dans les prompts actifs par cette livraison.

Attribution : rédaction et contrôles documentaires Codex, sur décision explicite du propriétaire ; aucune exécution ou preuve nouvelle attribuée à JARVIS.

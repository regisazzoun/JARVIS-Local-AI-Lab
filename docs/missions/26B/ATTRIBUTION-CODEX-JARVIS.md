# Attribution des contributions

## Codex

Codex conçoit et écrit les extensions du moteur, les schémas actifs, les contrôles déterministes et l'intégration des relectures par le modèle. Il déploie les modules avec sauvegardes, conserve les bases et services existants, diagnostique les défauts d'interface et de contrôle révélés pendant les essais, puis vérifie indépendamment les fichiers, empreintes et reçus. Ses interventions sont enregistrées comme infrastructure_correction / working_context_rebased et dans INSTALLATIONS.json ; elles ne sont pas des autocorrections de JARVIS.

Les fixtures stocks.csv (A), producer.py et mesures.csv (B), input.json et l'absence volontaire du témoin (C) sont Codex. Le programme producer.py est un banc applicatif fourni pour diagnostiquer ses paramètres ; il ne doit pas être attribué à JARVIS. L'omission initiale du manifeste dans C et le brouillon de comptage faux dans B sont des injections explicites dans les objectifs de test, pas des erreurs spontanées revendiquées.

Codex fournit les objectifs généraux et critères attendus, pas les tâches, leurs dépendances ni les contrats que JARVIS propose. Il n'adresse pas de coordinator_instruction rappelant un livrable manquant. Les améliorations des contrôleurs résultent toutefois de son diagnostic pendant la calibration : elles ne prouvent pas une mission longue sans assistance d'infrastructure. Les contrôles indépendants restent distincts des actions du modèle et ne sont pas injectés silencieusement comme plans JARVIS.

Codex exporte les journaux, documente les résultats et publie la branche / PR. Les tests logiciels avec réponses instrumentées sont des tests du moteur, jamais des exécutions autonomes du modèle. Les éventuels essais complémentaires de relecture avec un harnais Codex et de vraies inférences sont identifiés séparément des trois scénarios du worker.

## JARVIS

JARVIS, avec le modèle Qwen installé et la route Dell1 existante, propose réellement les tâches et leurs révisions via mission_plan dans les trois exécutions durables. Les nouvelles définitions proviennent de ses inférences ; les mécanismes de décodage ne corrigent que leur représentation de transport, sans inventer d'étape, de propriété métier ou de valeur attendue.

Les appels host_* et mission_verify sont exécutés par le Registry et le broker existants à la demande de JARVIS. Les sous-lectures exactes des vérificateurs sont réalisées par le moteur ; le broker enregistre JARVIS-runtime. La corrélation indépendante vérifie les identifiants et contenus reçus. Les opérations Codex ne sont pas importées dans ces reçus comme actions du modèle.

JARVIS-reviewer désigne le même modèle interrogé dans un contexte de contrôle séparé, sans outil d'action. Il extrait les exigences et classe les passages des rapports. JARVIS-engine effectue les validations de schéma, comparaisons de types/valeurs, conservation des versions et décisions de barrière. Cette séparation de contextes ne constitue pas l'indépendance d'un autre modèle ; la vérification indépendante finale est Codex.

Les brouillons, appels refusés, FAIL, INSUFFICIENT et faux positifs du contrôleur sont conservés. Une erreur de format du relecteur ne doit pas être comptée comme une affirmation fausse du rédacteur. Les rapports explicatifs sont produits et corrigés par JARVIS ; l'annexe de faits est déterministe, produite par le moteur développé par Codex.

## Hors réception

Aucune nouvelle création ou modification de skill n'est revendiquée automatiquement. Les quatre compétences historiques et le programme config-repair créé/corrigé en25/26 sont conservés. L'accès aux capacités existantes et la non-régression ne deviennent pas une nouvelle preuve d'utilisation agentique de chaque outil.14A reste ouverte ; son épreuve finale,24-Old et Dell2 ne sont pas lancés.

## Calibration au déploiement16

Seize installations successives sont documentées ; plusieurs rétablissent des interfaces de contrôle défectueuses. Ces interventions de Codex ne démontrent pas une autocorrection du moteur par JARVIS. Les missions interrompues pour déploiement reprennent leurs identifiants, tâches, versions et preuves ; les inférences non terminées ne sont pas inventées comme reçus. Les autres missions partageant le worker ont également été conservées et reprises après leurs interruptions temporaires nécessaires aux déploiements. Le test STRUCTURED-OUTPUT-PROBE est un essai technique Codex sur le modèle réel, sans opération JARVIS autonome revendiquée.

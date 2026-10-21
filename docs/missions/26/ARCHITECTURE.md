# Architecture du Mission Engine26

Extension du moteur21/22, du broker24 et du Skill Lab25. Même `runtime/missions.sqlite`, mêmes tâches, événements, reçus `tool_calls`, checkpoints, contexte et outbox ; aucune seconde base de missions. Le registre `skill-lab.sqlite` existant est conservé.

## Objectif et plan

Une mission soumise avec `spec.autonomous:true` reçoit un objectif brut, sans `spec.tasks`. Le modèle utilise `mission_plan` pour proposer tâches/dépendances, outils, observations, vérifications, récupération et artefacts, plus objectif/critères/conditions d'arrêt globaux. Le moteur valide le graphe puis enregistre atomiquement tâches et version dans `mission_plans` : auteur, raison, SHA256 et horodatage. L'auteur de l'outil modèle est fixé à JARVIS, jamais un paramètre libre du modèle.

`mission_progress` expose les versions et `current_plan_version`. L’option `append:true` ajoute les seules nouvelles tâches proposées par JARVIS, en conservant celles déjà enregistrées et leurs métadonnées. Une révision nécessite `expected_version` et une raison ; les tâches reçues sont immuables, une tâche déjà tentée ne peut disparaître, ses reçus restent conservés. Une déclaration de contrôle inexécutable peut être réparée par une nouvelle version, avec son ancien texte conservé. Les prédicats sémantiques valides antérieurs et les critères `spec.acceptance` ne peuvent être supprimés par révision. La compatibilité historique conserve le comportement sans écrasement des anciens plans.

La boucle utilise les tâches prêtes et le registre existant. Les outils proposés dépendent de la phase et les appels hors phase sont refusés avant exécution. Avant plan, seules découverte et lectures structurées sont proposées. Le contexte garde le dernier échange réel, le débogage et l'historique des plans ; la version complète demeure en SQLite.

## Observations et vérification

`mission_verify` effectue une nouvelle lecture via le registre et le broker : fichier local, SSH `read_file`, contenu GitHub ou service `is-active`. Il évalue des prédicats déterministes : valeurs/types JSON, conservation de sous-arbres, texte exact, SHA256 ou état effectif. Le contenu GitHub est extrait de son enveloppe avant comparaison. JSON invalide = FAIL ; accès impossible/troncature/contrat incomplet = INSUFFICIENT ; preuves de conservation manquantes = PARTIAL. Ces trois statuts empêchent la réception.

Les lectures ont leurs propres identifiants d'invocation et reçus broker ; les verdicts sont des événements persistants. Un succès de commande ou le mot `status` ne suffit pas. Les nouveaux contrats de tâche autonome exigent des `contract.semantic` exacts, un PASS récent et la preuve d'un appel `mission_verify`. Après une action, le contrôle doit être rejoué. Les critères propriétaire sont relus encore à la clôture finale. Les anciens contrats sont préservés : ce mode renforcé ne réécrit pas rétroactivement leurs réceptions.

Le Skill Lab accepte `mission_verify` comme étape `verify:true`. Les compétences anciennes restent activables/utilisables et leur faiblesse éventuelle n'est pas masquée ; la réception autonome26 exige en complément ses propres contrôles.

## Reprise et opérations

Les leases, le verrou canonique, les contextes, interruptions avant l'outil suivant, récupération après redémarrage et checkpoints de skills restent les mécanismes existants. `mission_action` ajoute une clé d'opération persistante dans la même base : un succès identique relit son reçu, un changement de paramètres exige une autre clé. Un résultat échoué/inconnu exige une nouvelle observation sémantique FAIL explicitement référencée avant tentative. Un cache de succès ne prouve jamais l'état actuel ; une lecture séparée reste nécessaire.

Limite assumée : aucun système distant non transactionnel ne garantit exactement une exécution après crash entre effet et reçu. L'état `started` est conservé comme incertain. Les skills historiques gardent leur mécanisme25 de reprise ; utiliser les clés pour les effets importants. Une réexécution volontaire d'une réparation idempotente constitue un test distinct, pas un doublon accidentel.

## Restitution et attribution

`mission_report_facts` construit les faits depuis les reçus, acteurs, paramètres, versions et verdicts. La clôture autonome archive intégralement le texte libre du modèle dans `model_report_original`, puis produit un rapport factuel déterministe. Elle ne promeut pas ses nombres et attributions libres en faits. Les rapports intermédiaires du modèle restent des artefacts à confronter au journal ; aucune compréhension universelle de prose n'est revendiquée.

Les opérations modèle sont déclenchées par JARVIS ; les outils hôte sont exécutés par le broker ; les prédicats par JARVIS-engine ; le développement/déploiement et contrôle indépendant par Codex. Les interventions Codex sont des événements explicites. L'empreinte du texte original et du relevé de faits est enregistrée.

## Référence externe

[JARVIS-OS](https://github.com/Grominet95/jarvis-OS) présente une séparation orchestrateur/vérificateur/reprise ; son dépôt indique AGPL-3.0. Consultation de référence uniquement : aucun code importé, aucune dépendance ajoutée, aucune règle d'approbation de ce projet tiers transposée au laboratoire. L'extension utilise les contrats déjà installés ici.

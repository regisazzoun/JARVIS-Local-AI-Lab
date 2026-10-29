# Finalisation factuelle de la préparation P4

## Diagnostic

Les trois tâches du plan3 sont validées nativement, dernière clôture71313.
La mission reste interrompue après les appels hors phase host_service71335 et
la répétition du registre de faits71398/escalade71400. Le mode de réception
proposait encore lecture, planification et contrôle, avec des consignes de tâche
qui invitaient à les réutiliser. La nouvelle lecture ne manquait pas : c’est
le passage de l’exécution au bilan qui était défaillant.

## Adaptation du moteur existant

Option `factual_finalization` activée pour cette seule unité. Elle s’applique
uniquement lorsque toutes les tâches sont déjà validées. Un paquet construit
sur SQLite fournit l’objectif complet, les états/artéfacts/empreintes acquis,
les références originales, l’historique FAIL/PARTIAL/INSUFFICIENT, les
interventions Codex et les réserves de clôture. Aucun texte de bilan à recopier.
JARVIS rédige librement son contenu via intervention_report.

La phase propose le bilan final, ou mission_block si une condition externe
interdit la clôture. Elle ne réexpose ni lecture du registre ni tâches acquises.
L’ancien contexte est archivé, pas réinjecté comme une liste d’actions à refaire.
La validation de couverture et le contrôle factuel du rapport restent dans les
outils backend existants, avant tout enregistrement ou publication. Cette
option ne reçoit aucune autonomie sans assistance ni aucune opération hors
des contrats effectivement vérifiés. Les modes historiques sont conservés.

## Vérification et installation

185 tests ciblés PASS sur registre, rapports, assurance et contexte. Nouveaux
cas : interdiction de finaliser des tâches en attente, objectif/historique
conservés, absence de lecture supplémentaire, texte réellement choisi par le
modèle, ancien contexte exclu, condition externe bloquant toujours la clôture.
Tests logiciels, pas preuves d’autonomie opérationnelle.

Sauvegarde privée du module avant installation. Préflight71403 avec identité
et objectif complets :12302/27648octets, fenêtre32768 inchangée, compteurs
vérifiés inchangés. Les workers ont été redémarrés hors appel actif et la même
mission remise en file. JARVIS rédige et soumet son propre bilan, aucun appel
intervention_report fait à sa place par Codex.

À ce stade : bilan en cours, réception de préparation etP4 non acquises par
ce seul correctif. Aucun déploiement canonique, aucune clôture14A/24-Old et
aucune fusion main.


## Revue factuelle adaptée à la phase finale

La première interface est réellement utilisée par Qwen (intervention_report71413),
mais ses trois propositions sont retenues avant publication : paquet de revue
trop volumineux, aucune approbation injectée. Une entrée réelle refusée71441
contenait les contrats détaillés de toutes les étapes et la longue liste des
interventions Codex. En phase finale seulement, les titres, états, artefacts
et empreintes proviennent directement des lignes canoniques de tâche ; contrats
complets et index restent persistants. Les références Codex explicitement citées
et les dernières références restent visibles, avec nombre d’entrées omises.
Toute affirmation sur un détail non fourni reste à étayer, jamais réputée vraie.
Préflight71490 :26648/27648, mêmes sept cartes source.186testsPASS.

Un nouvel essai71528 révèle une sélection de fichiers par sous-chaîne :
`plan-P4-ACTIVE-PREP.md` sélectionnait aussi l’ancien paquet
`P4-ACTIVE-PREP.md`, tandis que `unit_jarvis...` sélectionnait une lecture
du répertoire `jarvis`. La sélection utilise maintenant des noms/chemins
complets aux limites de tokens, sans ces confusions. Les cat de rapports du
modèle sont exclus des preuves techniques indépendantes, comme les lectures
host_read_file de ces mêmes rapports l’étaient déjà. Les documents restent
dans les archives et les statuts de réception/empreintes dans SQLite.

188testsPASS, dont correspondance exacte et refus de l’autopreuve par cat de
rapport. Préflight71533 sur la vraie entrée refusée71524 :19014/27648octets,
même passage et objectif, trois sources explicitement déclarées conservées,
cartes non pertinentes retirées, compteurs inchangés. Nouvelle reprise après
ce changement réel ; anciens refus et propositions conservés. Rapport encore
à recevoir ; aucune réception globaleP4 ni déploiement canonique déduits.

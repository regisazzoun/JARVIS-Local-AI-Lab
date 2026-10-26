# Architecture — état initial

NON VALIDÉ — conception P2 confiée à Qwen80B. Le moteur, MissionStore, broker et SSH existants sont réutilisés ; aucune seconde base de missions ni nouveau moteur d’inférence.

Bootstrap Codex : paramétrisation du workspace autorisé et des identifiants d’exigence des outils Phase1. Valeurs Phase1 conservées par défaut ;35 tests de non-régression passent. Cette adaptation rend possible une priorité P2 sur le vrai code copié, sans choisir son correctif ni sa répartition à la place du modèle. Les sources candidates sont sur les deux Dell ; les services actifs ne reçoivent pas automatiquement ces changements.

P3 et P4 ne sont pas transmis. Leur architecture sera établie après réception de la priorité précédente.

## Déblocage de l’édition distante structurée

Les deux derniers artefacts `edit_python` définissaient du code sans écrire les fichiers annoncés. Le relais exécutait ce contenu comme un programme et lançait ensuite un module unittest absent. L’interface confondait contenu source et instruction d’écriture ; son succès de transport ne démontrait aucune modification.

Codex ajoute `authority_edit` au même adaptateur opt-in. Qwen choisit l’exécutant et une liste d’éditions littérales : chemin relatif, ancre exacte à remplacer, nouveau texte ; pour une création, ancre nulle et contenu complet. Le programme d’édition vérifie toutes les ancres et les chemins avant la première écriture, refuse les doublons/écrasements ambigus, remplace chaque fichier via un temporaire local, puis le transport existant conserve les manifestes et le reçu. Le même `Authority.work(kind=correct)` conserve les décisions Qwen, l’idempotence et les compteurs. Le contenu n’est jamais évalué comme script d’édition.

Cela est une capacité d’outillage Codex, pas l’implémentation métier P2 ni une réception P3. Sept tests de l’éditeur, seize du garde existant et un du dialogue ont réussi. La qualification des changements P2 produits ensuite reste distincte.

Le test de l’insertion réelle a révélé un retour à la ligne manquant. L’éditeur contrôle désormais la syntaxe des fichiers Python avant la première écriture (huit tests d’éditeur). L’interface d’analyse surchargée demandait aussi au modèle de recopier un numéro d’événement, qu’il confondait avec une commande ou un événement de correction. `authority_analyze(issue, summary)` rattache maintenant le diagnostic rédigé par Qwen au dernier test échoué réellement enregistré pour cette issue. Il n’exécute aucune commande et ne prend aucune décision technique à la place du modèle. Dix-sept tests du garde réussissent, dont ce rattachement exact. Les compteurs ne sont pas réinitialisés.

### Reprise présentant encore une erreur résolue

Après réparation42627 et contrôles réels, la vue de travail réinjectait encore les dernières exécutions de syntaxe échouées, ainsi que `last_failed_test` et son ancien diagnostic, comme faits courants. Qwen a repris cette correction pourtant déjà effectuée. La vue présente désormais seulement les incidents non couverts par une résolution Codex attestée, et le nouveau défaut observé42688 ; les événements d’origine, références et compteurs restent intégralement dans SQLite. Le garde ne demande plus une nouvelle analyse d’un échec explicitement résolu. Une nouvelle panne postérieure à la résolution reste active et comptée. Deux tests couvrent ces cas :21tests du garde,8de l’éditeur et1du dialogue, tous réussis lors des contrôles ciblés. Les workers ont été rechargés avant la nouvelle mise en file, pour éviter un registre d’outils encore en cache.

La reprise conserve failed_cycles=3 avec un pointeur de résolution42656, lié à la réparation42627 et aux tests JARVIS postérieurs, puis borne à nouveau les échecs suivants. Ce pointeur est enregistré par Codex après changement technique et vérification ; aucun outil du modèle ne peut le produire. Ce n’est ni une remise à zéro par session, ni la réception du mécanisme P2 complet de problèmes stables, qui reste à développer et tester.

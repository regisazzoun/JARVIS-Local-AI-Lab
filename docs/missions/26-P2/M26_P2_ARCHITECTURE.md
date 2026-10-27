## Actualisation du27octobre2026

P2 historique et P3 reçus avec réserves ; la Phase2 globale reste ouverte. Corrections de contexte/isolation par tâche et version/pipefail au commit105c4ff,67tests ciblésPASS. Reprise réelle54911→54915→54930 et grandstdout219000octets vérifiés, compteurs conservés ; erreurs de prose conservées et corrigées. Voir [réceptionP3](p3/RECEPTION-P3.json), [déblocage](p3/DEBLOCAGE-54073.md), [errata](p3/ERRATA-RAPPORTS.md). P4 a démarré par [un audit court](M26_P2_P4_CODE_REEL.md), aucune réception du code actif encore prononcée. Les états et tests antérieurs ci-dessous restent leurs instantanés, pas des preuves rétroactives.

## Implémentation reçue dans le parcours ciblé P2

Même `DurableCycle`, même MissionStore, même base `runtime/missions.sqlite`, mêmes workers et broker : deux tables additives `mission_problems_v2` et `mission_attempts_v2`. Aucun second moteur de missions. Le champ propriétaire `spec.p2_reception.active` active les outils ciblés ; ils sont masqués pour les autres missions.

`attempt_ledger.py` : transactions, transitions attestées, contrat immuable, compteur durable, exclusion des doublons en cours/inconnus et plafond3. `attempt_execution.py` : délégation réelle via host_remote, fichiers de démarrage/résultat sur Dell, SHA du reçu, lecture indépendante et vérification sémantique existante. Le code retour du broker n’est jamais assimilé à celui du processus enfant. `p2_reception.py` : décisions du vrai modèle, paquet court par cas, états persistants, restitution des preuves et attente de revue Codex. Les choix de commandes/machines restent dans les appels de Qwen.

Les erreurs de format d’un vérificateur n’autorisent pas une relance de l’action. La reprise conserve la première preuve de comparaison exacte après redémarrage ; les consultations ultérieures référencent cet événement initial, sans prétendre que l’état n’a plus évolué après sa réobservation.

Les fichiers sont installés sur Mac et copiés sur les deux Dell, dont les SHA sont relus. La machine d’inférence reste Dell1 ; le ledger/transport restent sur Mac, les actions applicatives de démonstration sur Dell. L’ancien adaptateur d’autorité n’est pas intégralement migré : réserve essentielle, aucun déploiement général annoncé.

---

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

### Lecture de preuve et relais des escalades

Pour cette mission seulement, `authority_typed_evidence` remplace la lecture générique ambiguë par un choix de références d’exécution réellement enregistrées. L’API restitue la sortie d’un reçu complet après SHA, par fenêtre de lignes. Le statut de lecture est séparé du code de l’ancien processus (`observed_process_returncode`) : lire correctement un test FAIL ne fait plus échouer le lecteur.24tests du garde et du lecteur (dont Registry),8de l’édition et1de dialogue ont réussi. La supervision existante accepte un périmètre configurable, sans modifier ses valeurs par défautJL03 ;3tests supplémentaires couvrent stabilité de cause, arrêt après trois passages avec journal canonique et périmètre fixe. Les passages simulés des tests ne sont pas des preuves d’intervention autonome.

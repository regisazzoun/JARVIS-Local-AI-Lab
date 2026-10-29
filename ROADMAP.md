## P3 — circuit de reprise et versions corrigés — 29 octobre 2026

Le candidat Qwen75462 est appliqué75575 ; quatre cas ciblésPASS75624 surDell1.
Le testDell2 75723 utilisait une ancienne copie : le focus compare maintenant les
versions et les schémas de sync lient hôte et vraie référence d’exécution.
157tests ciblésPASS ; reprise75867, préflight24445/27648. P3 reste NON REÇUE :
contrôle indépendant des tailles variables et vérification du même code surDell2
restent requis. P4 attend, VF01 non transmis, compteurs/originaux conservés.
[Dossier](docs/missions/26-P2/p3/REPRISE-APRES-STAGNATION.md).

## Reprise P3 sur fonction réelle — 29 octobre 2026

Après arrêt borné74344, Codex ajoute l’édition AST d’une fonction dans son vrai
module, avec ancre exacte et contexte court. Observation74357 sur les deuxDell,
plan2 rédigé parQwen avec assistance de cadrage, préflight10755/27648,
résolution74381.90tests ciblés et5tests de supervisionPASS ; aucun candidat
applicatif reçu à ce jalon. Compteurs et arrêt antérieur conservés. P4 attend,
aucun14A/mémoire lancé. [Dossier](docs/missions/26-P2/p3/REPRISE-APRES-STAGNATION.md).

## Exécution déléguée autorisée — 29 octobre 2026

Décision propriétaire : JARVIS/Qwen80B décide et répartit les calculs sur les Dell ;
Codex contrôle, puis confie un test de validation distinct à JARVIS. Une priorité
principale à la fois : complément P3, intégration P4, correction JL03 ouverte,
contrôles puis test distinct. Mission P3 native `bfd9a813c1804ffcaad77c9f01d54045`
transmise ; blocage préalable de manifeste réparé71999 après contrôles réels sur
les deux Dell71998. P4 reste NON VALIDÉE ; test distinct NON TRANSMIS.
Aucune nouvelle confirmation humaine. Historique et acquis conservés.
[Ordre et attribution](docs/missions/26-P2/EXECUTION-DELEGUEE.md).

## Bilan P2–P4 et continuité — 29 octobre 2026

P2 (dix scénarios + intégration historique ciblée52932) etP3 sont **VALIDÉES AVEC RÉSERVES**. P4 reste **EN COURS — NON VALIDÉE**. Préparation native completed, trois tâches validées, bilan PASS71627/enregistré71630, réception indépendante71632 avec réserve d’abréviation de reçu corrigée dans un erratum, original conservé.188tests ciblés du dernier déblocage passent ; aucune autonomie éditoriale globale reçue. Suite P4-CANARY-STAGE c32347de3edf4288a4751a3e65afa7eb effectivement transmise : adapter/qualifier un artefact sur la base actuelle, deuxDell, avant activation. Aucun déploiement canonique ni réception des huit casP4 acquis. [Bilan complet](docs/missions/26-P2/BILAN-P2-P4-2026-10-29.md).

## P4 — trois tâches reçues nativement, finalisation débloquée — 29 octobre 2026

Les trois tâches du plan3 sont `validated`, dernière clôture71313. Le bilan final s’était bloqué sur des lectures répétées. Mode `factual_finalization` installé dans le même moteur : objectif et faits canoniques fournis, JARVIS rédige son propre bilan, contrôle factuel backend inchangé. **188 tests ciblés passent** ; paquet de décision12302/27648 et revue corrigée19014/27648 après sélection précise des sources. Originaux et compteurs conservés. JARVIS reprend le bilan ; préparation entière et P4 restent à réceptionner, aucun attester canonique déployé, aucune autonomie éditoriale globale reçue. [Architecture et preuves](docs/missions/26-P2/p4/FINALISATION-FACTUELLE.md).

## P4 — rapport des unités reçu, reprise systemd — 29 octobre 2026

`t1-read-service-files` est **VALIDÉ AVEC RÉSERVES** : PASS complet70544, clôture native70571/70572 et réception indépendante70607, rapport inchangé. Interface de citations par identifiants utilisée réellement par Qwen. Autonomie éditoriale non reçue ; lecture des fichiers ne prouve pas le code chargé. JARVIS a ensuite observé les services actifs70584/70586/70588/70590. Une fuite de consigne t1 dans le contexte réduit de la tâche suivante a été corrigée ; PARTIAL/INSUFFICIENT ne sont plus assimilés à des refus d’interface. **182 tests ciblés passent**. Résolutions70610/70648 : consignes limitées à la tâche, faits déjà acquis reconnus sans focus spécial, propriétés systemd originales conservées avec reçus, compteurs inchangés. La dernière tâche de préparation reprend ; P4 reste ouverte, aucun déploiement d’attestation acquis. [Réception](docs/missions/26-P2/p4/RECEPTION-RELEVE-UNITES.md) · [Correction du contexte](docs/missions/26-P2/p4/CONTEXTE-ENTRE-TACHES.md).

## P4 — reprise assistée du rapport t1, 28 octobre 2026

JARVIS a lu les deux unités réelles et écrit trois versions de son rapport. Après escalade, Codex a retiré deux passages non prouvés et corrigé les contrôleurs : conservation des sources, projection du brouillon, acquittement explicite des incidents sans effacer les totaux, phases de vérification et citations causales obligatoires. **129 tests ciblés passent**, correctifs installés, JARVIS reprend la vérification du même fichier. Les FAIL/INSUFFICIENT et compteurs sont conservés ; aucune réception globale P4, aucune preuve de déploiement de l’attestation active. Autonomie éditoriale toujours non reçue. La tâche systemd suit après t1 ; aucun rejeu P2/P3/candidat. [Dossier et attribution](docs/missions/26-P2/p4/PLANIFICATION-PLATE.md).

## P4 — rapport préparatoire débloqué le 28 octobre 2026

Réception **VALIDÉ AVEC RÉSERVES**, événement68595 : rapport `version0-plan` validé nativement68593 après PASS68493 et seconde revue complète68592. Même fichier relu, même SHA256 ; 11 passages et 7 sources contrôlés. Plan et brouillons JARVIS, rectification factuelle et déclenchement ponctuel de vérification/clôture Codex après escalades. L’autocorrection éditoriale autonome reste **non reçue**. 101 tests logiciels ciblés passent ; les avis erronés du contrôleur et tous FAIL/INSUFFICIENT sont conservés. Comparaison native des métadonnées originales, revue sémantique complète et contrôles des causes maintenus. Les deux autres tâches de préparation et le déploiement canonique restent à réaliser ; aucune réception globaleP4. [Réception et preuves](docs/missions/26-P2/p4/RECEPTION-RAPPORT-PREPARATOIRE.md). Continuer le même plan3, sans réécrire le rapport reçu ni rejouer P2/P3/candidat ; compteurs conservés.

## P4 — reprise technique du28octobre2026

Contexte corrigé7470d62 installé65588 ; fenêtre32768 conservée. Les propositions de plan imbriqué ont échoué, originaux/compteurs conservés. Après escalade, adaptateur plat571956d installé65968 : Qwen choisit chaque étape, même mission_plan/SQLite et mêmes contrôles de couverture/prose. Trois étapes réellement sauvegardées, couverture du plan3 acceptée66089 ; exécution de la première tâche relancée après correction de la vue d’interface66105. Aucun déploiement de l’attestation applicative ni réceptionP4. Paquet de coordination corrigé65937 pour retirer une lecture déjà effectuée ; ne pas remettre cette consigne obsolète. Interface mission_plan_report_step opt-in ; ni quatrième proposition assistée ni remise à zéro. [Dossier](docs/missions/26-P2/p4/PLANIFICATION-PLATE.md). Supervision normale suit aussi last_progress du worker ; garde3refus et périmètre identique.

## P4 — candidat reçu, préparation canonique transmise le28octobre2026

Candidat worker **VALIDÉ AVEC RÉSERVES**, réception65474 : application réelle JARVIS64975 surDell1, même manifeste synchronisé65185, quatre cas exécutés65099/Dell1 et65210/Dell2 (conformePASS, divergenceFAIL, absentINSUFFICIENT, désactivé sansrapport). Code de raccordement **Qwen80B assisté parCodex après escalade**, oracle et contrôle indépendantCodex. Originaux, refus et errata conservés. Ces essais isolés ne prouvent aucun déploiement canonique ni réceptionglobaleP4.

Nouvelle unité séquentielle `e98fd4bbe37c492b922db9b5a1d782aa` : **P4-ACTIVE-PREP**, dans le même moteurSQLite, prépare les chemins/services réels, canari, fraîcheur des rapports et retour arrière. Choix des observations et plan confiés àQwen80B ; fenêtre32768 inscrite avanttransmission. Pas de rejeuP2/P3/candidat. L'intégration réelle suivra après revue technique sans nouvelle validationhumaine. Supervision réorientée vers cette seule unité, compteurs historiques conservés. [Réception et attribution](docs/missions/26-P2/p4/RECEPTION-CANDIDAT-WORKER.md) · [Paquet transmis](docs/missions/26-P2/p4/LANCEMENT-ACTIF-PREPARATION.json). P4/phase2 restent **EN COURS — NON VALIDÉES** ; aucune14A/24Old/mainmerge.

## P4 — conservation des vraies lectures et API corrigées

Audit : un tool-ok contenant un processus rc1 pouvait remplacer le code utile par une erreur ; sélection corrigée, deux pages distinctes conservées, reçus complets vérifiés. Le helper attestation_report accepte la sélection explicite des symboles. Source f90790e, installation64398, API observée64399, préflight64402 à27016octets/27648 avec worker complet et API présents.145 tests locaux,17attest+33contexte surchaqueDell réussis sousCodex. JARVIS reprend le mêmeplan3 ; instrumentation candidate encoreàprouver, P4 NON VALIDÉE. Aucun attester installé danslesservicesactifsMac, compteurs conservés. [Détails](docs/missions/26-P2/p4/SOURCES-UTILES-ET-API.md).

## P4 — interfaces corrigées, reprise native

Les identités serveur, la conservation des pages de source utiles et l’édition par chemin absolu interne sont corrigées dans le moteur existant. Déploiement63326 : 136 tests ciblés locaux et24 tests sur chaque Dell réussis. La reprise a révélé une boucle contournant la signature par max_lines ; garde persistant du contenu effectif installé63429, 139 tests locaux et67 sur chaque Dell réussis. Références courantes séparées des archives63738, 140 tests locaux et15 de projection/identités parDell. Reprise de JARVIS sur le plan3 existant ; instrumentation du worker candidat et réceptionP4 restent à prouver. Compteurs conservés, pas de déploiement applicatif par cette intervention. [Détails et preuves](docs/missions/26-P2/p4/INTERFACES-PERENNES.md).

## P4 — correction pérenne des identifiants utilisée parJARVIS

Même missionP4, plan3 préservé. Les identifiants sont attribués parlemoteur depuis les appelsSQLite ; Qwen ne lesgénèreplus.130tests ciblésPASS,14nouveaux cas surchaqueDell. Usage réel reçu62931 : commande62737 exécutéeunefois, répétitionavecdescriptiondifférente renvoyantle reçuexistant62774. Compteurs/anciensalias préservés, garde deseffetsinconnus maintenu. Aucun nouveaumoteur ni déploiementduworker candidat ; P4globale reste nonreçue. [Architecture, migrationetpreuves](docs/missions/26-P2/p4/IDENTIFIANTS-DURABLES.md).

## P4 — faux match corrigé parCodex, retests JARVIS relancés

Après l’ordrepropriétaire de correction, le candidat compare désormais les objets__code__ aux candidats compilés sans exécution.15tests ciblésPASS surchaqueDell sousCodex, originaux conservés ; lanceurautonome corrigé après l’importéchoué61520. RetestsJARVIS relancés dans la même mission/SQLite, compteurs préservés. Pas d’attestationdesprocessusactifs ni de réceptionglobaleP4. [Correction et limites](docs/missions/26-P2/p4/CORRECTION-FAUX-MATCH.md).

## P4 reprise depuis l’état persistant —27octobre2026

Audit natif terminé (cinq tâchesvalidées), réception indépendante limitée aux deux sources/artefacts avec réserve de prose :58952, dossier d’erreurs58945. P4 globale NON VALIDÉE. Nouveau paquet court réellement transmis àQwen80B : attestation du codePython chargé, candidat surlesdeuxDell, missiond8fe752876db480cbe5f22cd5525e2dd. Plan/fichiers/tests/répartition à choisir parQwen ; déploiement ultérieur après contrôle, sans nouvelle validationhumaine. Objectif de contexte32768 déjàpersisté avant transmission ; aucune repriseP2/P3. [Paquet](docs/missions/26-P2/p4/LANCEMENT-ATTESTATION.json) · [Reprise et réserves](docs/missions/26-P2/p4/REPRISE-MEMOIRE.md).

## Budget Qwen80B — décision et essai du27octobre2026

Fenêtre32768tokens testée réellement et installée surDell1 : prompts18876 puis26614tokens, minimaVRAMlibre1129/1163Mio, sans erreur mémoire retournée. Réponse4096+marge1024, entrée27648 avec garde conservateur ; critère de résultat persisté avant transmission des sous-tâches. Inférence JARVIS reprise, P4 toujours non reçue. [Mesures, règle et limites](docs/missions/26-P2/p4/CONTEXTE-32768.md).

## P4 — intervention sur les vrais blocages

Stagnation Git/chemin corrigée par préflight surlesdeuxDell ; contrat d'exécution réparé au commit926ab42 (executor/command requis,70tests logicielsPASS). JARVIS a repris des programmesPython et produit deux artefacts, dont les empreintes de core.py/tools.py ont été relues indépendamment. Audit toujours NON VALIDÉ, code chargé non prouvé. [Dossier](docs/missions/26-P2/p4/INTERVENTION-GIT-CHEMINS-CONTRAT.md). Compteurs historiques conservés ; aucune installationGit, aucun rejeuP2/P3 ni fusionmain.

## Phase2 — P3 reçue, audit P4 réellement lancé

P3 **VALIDÉ AVEC RÉSERVES** (55310) : grandstdout219000octets, checkpoint/redémarrage/reprise réels, compteurs conservés, effetDell2 non régénéré dans le scénario.67tests logiciels ciblés ; développement et déblocagesCodex distingués des programmes/exécutionsJARVIS. Prose originale erronée conservée, version corrigée et errata. P4 **EN COURS, NON VALIDÉ**, premier audit natif `d1b0d69639724c60b5bd1b2143b1a5fa` surlesdeuxDell ; la preuve du code réellement chargé reste à construire. [P3](docs/missions/26-P2/p3/RECEPTION-P3.json) · [P4](docs/missions/26-P2/M26_P2_P4_CODE_REEL.md). MissionPhase2 non clôturée,14A non clôturée, aucunmainfusionné.

## M26-P2 — déblocage P3 du27octobre

P3-01 reçue avec réserves ; P3-02-run réellement exécutée par JARVIS surlesdeuxDell. Isolation des preuves par tâche/version, conservation des résultats utiles et pipefail corrigés parCodex,67tests logiciels PASS. Checkpoint54911 → redémarrage54915 → repriseJARVIS54930, compteurs conservés. P3 globale **NON VALIDÉ** : grandstdout et non-duplication encore à vérifier, errata de prose conservés. Supervision périodique existante désormais ciblée surP3, sans rejeuP2 ni lancementP4. [Dossier](docs/missions/26-P2/p3/DEBLOCAGE-54073.md).

## M26-P2 — actualisation du27octobre : P2 reçu, P3 active

✅🟡 P2 historique **VALIDÉ AVEC RÉSERVES**, reçu52932 ; deux continuations natives completed,40testsPASS réels sur chaque Dell au même manifeste complet. Aucun rejeu S01–S10. P3 **EN COURS, NON VALIDÉ** : garde du contexte déployé dans Core.ollama, premiers budgets réels enregistrés,14tests logiciels du garde PASS ; correctif Codex de conservation du dernier résultat outil après relectures stériles. Démonstration de reprise encore attendue. P4 attend réceptionP3. [État actuel](docs/missions/26-P2/REPRISE-27-OCTOBRE.md) · [P3](docs/missions/26-P2/M26_P2_P3_CONTEXTE.md). Pas de réception14A ni fusionmain.

## M26-P2 — reprise du27octobre : raccordements historiques en réception

🟡 P2 : adaptateurs Authority/Registry/actions/vérification et garde des retries workers installés. JARVIS a reçu ses paquets courts, utilisé le garde classique réellement surDell2 (JSON42, PASS et tâche validated) et exécuté40testsPASS sur chaque Dell. Refus d’acceptation correct sur une différence de manifeste complet ; fichier historique aligné par SHA, contrôle ciblé Dell2 en cours.156tests logiciels locaux PASS, séparés des preuves agentiques. Test initial JARVIS incorrect conservé/non reçu, adaptations et oracles Codex attribués. [Suivi actuel](docs/missions/26-P2/REPRISE-27-OCTOBRE.md). Dix scénarios antérieurs et ledger parent inchangés. P3 et P4 autorisées par le propriétaire, à transmettre successivement après réception précédente ; aucune clôture14A.

## M26-P2 — dix scénarios P2 reçus le26octobre2026

✅🟡 **VALIDÉ AVEC RÉSERVES sur le parcours natif instrumenté.** Neuf scénarios VALIDÉ et repriseS09 VALIDÉ AVEC RÉSERVES : contrôle sémantique réparé par Codex après trois vérifications infructueuses. Trois corrections réelles FAIL déclenchent escalade ; compteurs conservés après redémarrage ; quatrième opération renommée refusée, résultat perdu relu sans doublon.55 tests logiciels locaux ciblés PASS et11 nouveaux tests sur chaque Dell, distincts des opérations JARVIS. [Réception](docs/missions/26-P2/M26_P2_RAPPORT_FINAL.md) · [Dix preuves](docs/missions/26-P2/reception/RECEPTION.json) · [PR29](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/29). Migration globale des chemins historiques non reçue ; mission native en revue d’intégration, Phase2 non clôturée. P3/P4 non transmises ; aucune réception14A.

## M26-P2 — reprise avec relais périodique des escalades

**NON VALIDÉ — P2 en cours.** Arrêt42889 sur identifiants de preuve corrigé par lecteur typé, sorties complètes SHA et statut de lecture distinct du résultat historique. Superviseur Codex dédié raccordé au moteur existant, contrôle120s et passages bornés, périmètre P2 seul. [Fonctionnement et limites](docs/missions/26-P2/SUPERVISION-CODEX.md). Les4/14PASS sont des preuves du candidat antérieur, pas du candidat actuel. P3/P4 non confiées.

## M26-P2 — déblocage de l’édition et reprise P2

**NON VALIDÉ — reprise après intervention Codex.** Qwen a modifié le vrai code candidat surDell1 ; réparation ponctuelle du saut de ligne parCodex après3échecs, conservés. Vérification JARVIS4PASS Dell1 et14PASS Dell2. Oracle indépendantFAIL : SUCCESS sans preuve encore accepté ; correction suivante transmise, réceptionP2 non prononcée. [Preuves](docs/missions/26-P2/PREUVES-DEBLOCAGE.json). P3/P4 non confiées.

## M26-P2 — blocage constaté après reprises bornées

**BLOQUÉ, mission non clôturée.** Escalade42375, trois collisions d’identifiant ; diagnostic Codex amélioré, mais aucun incrément source P2 reçu après les reprises. Workers disponibles, mission interrupted ; ne pas confondre disponibilité et activité. [Dossier](docs/missions/26-P2/ESCALADE-INACTIVITE.json). P3/P4 non transmises.

## M26-P2 — Phase2 lancée le26octobre2026

🟡 **NON VALIDÉ — en cours.** P2 seule transmise à Qwen80B ; mission native `3aa717f3887e49daa7daf7e883ee52e4`. Les copies de code installé sont sur les deux Dell. Trois incidents de reçu tronqué ont entraîné un arrêt et une escalade ; Codex a réparé le transport, vérifié deux sorties réelles40001caractères, conservé le compteur3 et rendu la main. P3 et P4 ne sont pas transmises. [Audit](docs/missions/26-P2/M26_P2_AUDIT_INITIAL.md) · [Suivi](docs/missions/26-P2/M26_P2_RAPPORT_FINAL.md). Aucune réception anticipée, aucun autre chantier lancé.

## Mission 26 — Phase 1 : autorité Qwen80B et exécution distribuée — réception du26octobre2026

✅🟡 **GO AVEC RÉSERVES dans le projet isolé.** Qwen80B décide sur Dell1, répare réellement deux fichiers sur Dell1, choisit les contrôles et fait vérifier la version exacte sur Dell2. Deux lots natifs reçus ; oracle Codex final12/12 sur chaque Dell ;35 tests logiciels ciblés réussis. Services et anciennes missions JL03 conservés. Réserves importantes : assistance infrastructure Codex,106 inférences pour deux défauts, restitution encore fragile, activation ciblée et intégration complète autonomous/assurance non reçue. [Réception](docs/missions/26-P1/RAPPORT-FINAL.md) · [Preuves](docs/missions/26-P1/RECEPTION.json) · [Errata](docs/missions/26-P1/ERRATA-RAPPORTS.md) · [PR28](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/28), sans fusion. Aucune réception générale14A ni lancement de Phase2, mémoire24-Old ou autre mission.

## JL03-COR-P1 — D03/D04/D17 livrées techniquement,26octobre2026

✅🟡 GO technique avec réserves. Trois missions completed dans le moteur, vrais PASS sémantiques des corrections actuelles et rapports finaux natifs JARVIS. Correctifs40422f9installés dansJL03 ;55tests ciblésPASS et contrôle navigateur authentifié reçus. Codex a fourni interfaces/aides et intégré/vérifié ; autonomie sans assistance et qualification vocale physique restent réservées. D01captureacceptée ; D02transcriptionréservée/mémoiredifférée ; aucune autre mission lancée, aucune fusionmain. [Réception et preuves](docs/missions/JL03-COR-P1/RAPPORT-RECEPTION-26-OCTOBRE.md).

## JL03-COR-P1 — correctifs installés, contrôle navigateur reçu le26octobre

D03/D04/D17 intégrés dans JL03 commit40422f9 :55tests ciblésPASS, APIauthentifiée et rendu réel CPU/3090/3080 Dell2 reçus, réponseAPIvide affichéeunefois, saisieconservée, conversationréelle6,035s pendantcontrôlesDell. D03/D17 tâches réellement validated aprèsPASSsémantique et clôture conditionnelle déclenchéeparJARVIS ; finalisationglobale en cours, D04reste à recevoir. Codex a fourni une assistance importante et l'intégration ; aucune autonomie sansassistance ni qualification acoustique reçue. [Résultats, preuves et limites](docs/missions/JL03-COR-P1/REPRISE-26-OCTOBRE.md).

## JL03-COR-P1 — aide concrète aux trois défauts

Workers rechargés pour utiliser le correctif du vérificateur déjà installé ; vrai transport Qwen80BDell1 reçu en24576tokens, sans réception fictive de prose. D03/D04 reçoivent des corrections factuelles ciblées et la reprise de vérification. PourD17, bancbranché surrenderer/Handler réels et patch fourni : copieisolée6PASS/1FAILavant,7PASSaprès ; application/retest parJARVIS encore requis. Aucun nouveaucorrectifapplicatif live reçu. [Aide et preuves](docs/missions/JL03-COR-P1/AIDE-TROIS-DEFAUTS.md).

## JL-03-COR-P1 — reprise sur les Dell et supervision persistante

Les trois blocages sont diagnostiqués ; sources réellement déposées sur les deuxDell, D03préflightCodex6/6sur chaquehôte, sondeDell2réelle3090+3080, garde7aa6288installé et12testsPythonPASS. ReprisesJARVIS armées en contextesséparés, deuxau maximum ; coordinationpériodique configurée pour intervenir sur les prochains blocages sans attenteGO. Aucun nouveauGOglobalD03/D04/D17. [Supervision, limites et attribution](docs/missions/JL03-COR-P1/SUPERVISION-PERSISTANTE.md).

## JL-03-COR-P1 — D03 diagnostiquée, candidat corrigé et reprise ciblée préparée

Codex a reproduit puis corrigé le double message d’erreur sur réponse vide et la perte de saisie dans le candidat isolé D03. Harnais branché sur la fonction réelle :4PASS/2FAILavant,6PASSaprès ; capture8PASSconservée. Aucun déploiement ni réception globaleD03. Plan2 et repriseJARVIS préparés sans remiseàzéro des compteurs ; premier test natif puis vrais testsDell requis. D04/D17 continuent, maximum deux contextes. [Diagnostic et preuves](docs/missions/JL03-COR-P1/D03/DEBLOCAGE-CODEX.md).

## JL-03-COR-P1 — capture acceptée, suite active sans validation intermédiaire

Capture acceptée par le propriétaire ; transcription encore imparfaite, cause non établie, mémoire différée. D03 et D04 sont réellement en cours dans des contextes distincts. D17 est préparée dans le moteur et sera envoyée dès qu’une place se libère, y compris après blocage documenté ; coordinateur ciblé actif toutes les30s, maximum deux contextes. Aucun correctif D03/D04 encore reçu. Les dossiers d’escalade et compteurs restent persistants, aucune nouvelle attenteGO. [Continuité et attribution](docs/missions/JL03-COR-P1/CONTINUITE.md) · [Registre publié](docs/missions/JL03-COR-P1/REGISTRE.json).

## JL-03-COR-P1 — capture corrigée et installée, qualification propriétaire à faire

🟡 Sur demande du propriétaire, Codex a installé une correction ciblée de la fenêtre de parole et des sessionsmicro : parole après silence noncoupée, événementsanciens isolés, un traitement par segment sans éliminer les répétitionsvolontaires. Cinq régressions reproduites avant correction, huit cas ciblésPASSaprès ; navigateur réelWebAudio/MediaRecorder→Whisper : uneséquence après17,3sdesilence, unsegment/unetranscriptioncomplète. Sourcecommit`c1b49c8`dansLauncher3. Correctif développé parCodex après blocagesJARVIS ; D01/D02restent àqualifier avec le propriétaire, aucun GOglobal ou autonomie fictive. Whisper/modèle/routage/JL01/JL02inchangés. [Corrections et essais](docs/missions/JL03-COR-P1/CORRECTIONS-APPLIQUEES.md) · [Déploiement](docs/missions/JL03-COR-P1/DEPLOIEMENT-CAPTURE.json).

## JL-03-COR-P1 — démarrage séquentiel en contextes distincts,25octobre2026

🟡 D01etD02transmis successivement àJARVIS, missions/conversations/worktrees distincts selon dernière précision propriétaire. Checkpoints et demandes de capacité natifs reçus ; gardeD01arrêté après trois réécritures, historique conservé. Node/Bubblewrap et projets isolés fournis/testés sur les deuxDell, reprise par workers canoniques. Aucun défaut vocal déclaré corrigé ; D03/D04/D17nontransmis. Contextevolumineux non déclaré résolu, aucune modification de modèle/routage. [Suivi](docs/missions/JL03-COR-P1/ETAT-DEMARRAGE.md) · [RegistreCodex](docs/missions/JL03-COR-P1/REGISTRE.json).

## Mission14B — réception technique du25octobre2026

✅🟡 **GO technique avec réserves.** Dell2 booté sur Debian13, RAID1propre[UU], SSHclé/motdepasse/sudo et Ansible vérifiés ; piloteNVIDIA et calculCUDA numérique réussis sur chaqueGPU. Matériel réel :3090de24Go +3080de10Go, pasdeux3090. Suivi physique actif, horloge synchronisée, moniteurRAIDcorrigé, aucunserviceenéchec. JARVIS a exécuté les outils de réception ; assistanceCodex importante et erreurs conservées. AucunOllama/routage/charge modifié. Les états historiques du plan ne sont pas cochés artificiellement. [Réception et erratum](docs/missions/14B/POINT-RECEPTION-25-OCTOBRE.md) · [Preuve indépendante](docs/missions/14B/RECEPTION-INDEPENDANTE-25-OCTOBRE.json).

## Mission14B — reprise du25octobre2026

🟡 Debian13/EFI et paquetsNVIDIA/CUDA préparés ; RAID synchronisé puis arrêté proprement. La continuation nocturne est restée dans l'installateur au reboot et l'observateur a atteint6h : autonomie de cette sortie non reçue. Codex diagnostique les signaux bloqués duPID1 et corrige le reboot après garde d'arrêt propre ; démarrage installé et calculGPU restent à recevoir. [Diagnostic et reprise](docs/missions/14B/REPRISE-25-OCTOBRE.md). AucunOllama/routage/charges modifié.

## Mission14B — installation réelle et tableau physique,24octobre2026

🟡 **En cours.** Dell2 identifié ; deuxNVMe qualifiés. JARVIS a réellement déclenché l'installation Debian13/RAID1, la reprise après correctionCodex et la préparationNVIDIA/CUDA. Debian/EFI finalisés sous`/target`, RAID[UU]encore en synchronisation ; aucun GO avant reboot et contrôles. Tableau physique réel actualisé5s. Après trois appels d'actions inventées refusés, garde actif, diagnostic puis intervention ponctuelleCodex pour lancer la continuation bornée après synchronisation. Les erreurs, rapports incorrects et attributions sont conservés. Ollama/routage/charges et anciens profils inchangés. [Reprise, incidents et suite](docs/missions/14B/REPRISE-INSTALLATION.md) · [Reçus natifs](docs/missions/14B/PREUVES-REPRISE.json). Les états ci-dessous restent leurs instantanés historiques.

## Mission14B — précision propriétaire de la règle anti-boucle

Après arrêt sur trois plans refusés, la règle est reprécisée et transmise dans le même moteur : diagnostic, solution réellement différente avec limite de trois échecs comparables ; si non résolu, dossier succinct d'interventionCodex, pas de boucle indéfinie. Une demande prête et les tâches indépendantes doivent être conservées si assistance indisponible. Reprise par lecture du contrat actif, sans plan fourni parCodex, sans effacer compteurs/erreurs. Aucun changementOllama/routage/charges/architecture. [Directive et reçu](docs/missions/14B/PRECISION-REPRISE.json).

## Mission14B — initialisée et confiée àJARVIS

🟡 Missioncanonique `a1becab1a8244e2295463bd5be833784`, conversation `61495bec-f92e-42aa-b450-7bac4a6815a5` ; état observé `running`, cycle1. JARVIS prend l'installation/intégration duDell2 Debian13 et lesGPU sous condition d'alimentation. Codex a seulement préparé l'ordre, les références et la transmission. Aucun résultat d'installationDell2 n'est encore reçu. Ollama/routage/répartition/architecture exclus ; trois échecs comparables puis arrêt/diagnostic/correctif et reprise selon outils disponibles. AppelCodex uniquement pour capacité manquante démontrée, demande prête si assistance indisponible et autres tâches poursuivies. [Ordre14B](docs/missions/14B/MISSION.md) · [Reçu d'initialisation](docs/missions/14B/INITIALISATION.json). Les anciennes exclusionsDell2 sont remplacées dans ce seul périmètre ;14Adistincte.

## Mission27 — JL-03 livré pour essais,24octobre2026

✅🟡 **GO technique avec réserves ; autonomie de développement sans assistance non reçue.** V3 indépendante installée sur8766, dépôt privéJARVIS-Launcher3. Cristal3D/WebAudio, texte/voix canoniques, projets/historique/recherche/fichiers, flux complet des missions et télémétrie3machines/tousGPU. WorkerJARVIS de démonstrationcompleted, conversationMacpendantworker4,04s. Trois échecs contrôlésJARVISarrêtés, reprise409 ; neuf testsPython et huit modules contrôlés parJARVIS. Les correctionsCodexétendues, erreurs de prose, limites du gardecoopératif, macOS/acoustique et latenceLiveKitrestent explicites. JL-02préservée, aucune fusionmain. [Rapport27](docs/missions/27-JL-03/RAPPORT-FINAL.md) · [Application](https://github.com/regisazzoun/JARVIS-Launcher3/tree/codex/mission-27-jl03). Les sections datées ci-dessous restent historiques ; l'ordre explicite de lancement27 prévaut sans lancer14A/24-Old/Dell2.

## TTS-01 — réception technique du24 octobre2026

✅🟡 **GO avec réserves.** JARVIS a produit et livré trois WAV français avec Qwen3-TTS1.7B/Uncle_Fu sur Dell1. Durées6,16/8,24/7,60s, synthèses11,27/14,39/13,39s ; transcription indépendante, HTTP authentifié et lecture Chromium reçues3/3.246tests logiciels, sans confusion avec autonomie. Codex a fourni outillage, diagnostics, guidage et réception ; autonomie sans assistance et faible latence conversationnelle non validées. Piper conservé, aucun14A/24-Old/Dell2. [Rapport et liens privés](docs/missions/TTS-01/RAPPORT_TTS_01.md) · [PR22](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/22), sans fusion. Les sections datées plus anciennes restent historiques.

## TTS-01 — reprise propriétaire du24 octobre2026

🟡 Reprise de la mission existante, deux tâches reçues conservées. JARVIS lit les sources officielles avec le80B Dell ; venv torch2.6.0+cu124/qwen-tts0.1.1 déjà installé, aucune réinstallation. Fenêtre GPU sur file canonique et sonde indépendante des WAV développées/déployées par Codex,242tests logiciels. Aucune nouvelle voix encore reçue à cet instant. [Reprise](docs/missions/TTS-01/REPRISE-2026-10-24.md).28A reste clôturée ; aucun14A/24-Old/Dell2.

## Mission 28A — clôture propriétaire du 24 octobre 2026

🟡 **Clôturée incomplète en l’état.** Le propriétaire retient **Qwen3-Coder-Next80B pour les missions Dell1**, avec **Qwen3.5 27B conversationnel sur Mac**. Le cœur hybride reste installé ; six étapes principales sont validées. La réception du programme échoue encore sur quatre variantes et les rapports conservent des erreurs : ces réserves restent ouvertes. Les deux exécutions sont interrompues et la publication erronée est neutralisée ; nouveaux tests différés sans reprise automatique.238tests logiciels réussis, distincts de l’autonomie. [Clôture](docs/missions/28A/RAPPORT-FINAL.md) · [PR25](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/25).14A/24-Old/TTS/Dell2 non lancés.

## Mission28A — moteur80B sélectionné, réception agentique en cours

🟡 Qwen3-Coder-Next80B est installé et pilote réellement les missions Dell :5/6sur le screening ciblé, contre27B4/6,32B3/6et70B2/6 ; le cas coverage reste ambigu. Conversation27B conservée sur Mac, contextes stabilisés, priorité/repli et quotas75/25 reçus. Deux workers du moteur canonique sont actifs ; six réponses locales pendant deux missions running :0,828–0,961s.238tests logiciels réussis. La réception indépendante a détecté un programme JARVIS erroné malgré son code retour0 ; sa correction et les rapports restent en cours. [Comparatif](docs/missions/28A/MODELES-DELL-COMPARATIF.md) · [Tests](docs/missions/28A/TESTS-ET-REPRISES.md) · [PR25](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/25). Aucun lancement14A/24-Old/TTS/Dell2.

## Mission28A — continuation effective du23 octobre2026

🟡 Les contrôles indépendants C(routage/priorité/repli) et D(profils GPU) sont désormais reçus. Le moteur évite les cycles sans tâche prête. JARVIS a repris le téléchargement80Bdepuis le cache puis vérifié son installation ; la comparaison27/70/80au32B déjà mesuré reste en cours.226tests logiciels passent. Le27B conversationnel du Mac est conservé, le pilote Dell reste provisoire jusqu’aux mesures. [Ordonnancement](docs/missions/28A/ORDONNANCEUR.md) · [PR25](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/25). Aucun nouvel accord humain attendu.

## Mission28A — reprise des essais32B après blocage,23 octobre2026

🟡 Mission toujours en cours. Les six inférences32B ont été exécutées par JARVIS ; résultat3/6après correction d’un faux FAIL du vérificateur Codex, original conservé. Correction du contexte d’exécution et du propriétaire du dossier de collecte déployées ; JARVIS a réutilisé les fonctions corrigées.221tests logiciels réussis. Pilote70B mis en repli provisoire vers le27B déjà éprouvé sur Dell après appels de preuve fictifs ; conversation27B sur Mac inchangée. Le choix du nouveau moteur puissant et le comparatif complet restent ouverts. [Diagnostic et attribution](docs/missions/28A/INCIDENT-REPRISE-TESTS.md) · [PR25](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/25).

## Mission28A — lancement et déploiement effectifs,23 octobre2026

🟡 **En cours, non réceptionnée.** Qwen3.5:27b-q4_K_M est réellement utilisé sur le Mac mini ; routeur hybride et worker du moteur existant déployés, mêmes bases canoniques. Llama3.3:70B est installé et utilisé provisoirement sur Dell1 ; son gain qualitatif reste à démontrer. JARVIS a mesuré une pointe GPU cumulée699,37W, avec retour250W/carte vérifié ; aucune tenue prolongée700W ni consommation à la prise n’est affirmée. Quota de fond75% et réduction pendant interaction observés ; six réponses simples pendant worker Dell autour1,1–1,9s. Suite logicielle217tests réussis. Après correction d’interface Codex, JARVIS a installé le candidat32B exact et repris après une attente SHA256 ; présence et empreinte relues indépendamment. Les essais d’inférence/comparaison restent en cours. [Architecture](docs/missions/28A/ARCHITECTURE-HYBRIDE.md) · [Incident32B](docs/missions/28A/INCIDENT-INSTALLATION-32B.md). Aucun lancement14A/24-Old/TTS/Dell2 ; aucune fusion main.

Les décisions préparatoires ci-dessous sont conservées comme historique et ne décrivent plus l’état d’exécution actuel.

## Décision complémentaire propriétaire — 23 octobre 2026 : modèle conservé sur Mac mini

📋 **Mission28A — architecture cible hybride : conserver `qwen3.5:27b-q4_K_M` comme modèle conversationnel sur Mac mini Debian ; modèle plus puissant sur Dell1 pour missions complexes ; Dell2 préparé pour renfort futur.** Le modèle actuel est inventorié sur Dell1 en mission13 : son installation et ses performances **sur Mac mini restent à démontrer**, sans substitution silencieuse. Mac mini 75% missions /25% JARVIS/conversation. [Cahier28A](docs/missions/28A/MISSION.md).

## Mission 28A — Décision propriétaire du 23 octobre 2026

📋 **Préparée, non lancée.** Déploiement Mac mini + Dell1 : Mac mini cible75% calcul de missions / réserve25% JARVIS dont conversation et gestion, rééquilibrage pour faible latence ; Dell1 jusqu'à100% pour missions, priorité interactive à garantir ; Dell2 futur100% missions mais déclaré `pending/offline` jusqu'à mission14. **Upgrade de modèle prioritaire**, offload vers RAM DDR4 autorisé ; DDR5 matériellement incompatible avec Dell5820/i9-10980XE. Profil expérimental de pointes courtes GPU cumulées **jusqu'à700W** demandé, résultats de charge à mesurer, sans prétendre déjà qualifiés. Mission13 reconnaît les deux GPU et CUDA individuellement, réceptions conservées. [Cahier28A](docs/missions/28A/MISSION.md).

## Décision propriétaire du 23 octobre 2026 — réception fonctionnelle du raccordement de deux RTX3090

✅ **Raccordement et alimentation reçus fonctionnels pour le montage testé** : deux GPU détectés et CUDA réussi sur chacun, sur décision expresse du propriétaire. Réserves de certification formelle du brochage levées comme obstacle général ; brochage détaillé et puissance maximale demeurent non mesurés. **Mission13 : ✅🟡 GO avec réserves techniques restantes** pour essais d'inférence multi-GPU et comportement sous charge. [Addendum](docs/missions/13-extension-gpu/DECISION-RECEPTION-ALIMENTATION.md) · [PR23](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/23). Ne pas réinstaller ni répéter les calculs CUDA reçus.

## Mission13 — extension double RTX3090,23 octobre2026

🟡 **Réception partielle : deux GPU reconnus et petits calculs CUDA réussis sur chacun ; alimentation/faisceaux et inférence double non qualifiés.** Pilote existant conservé, Ollama limité à un UUID. Deux cartes identiques DellOEM indiquées par le propriétaire et sous-systèmes Dell observés. [Rapport](docs/missions/13-extension-gpu/RAPPORT-FINAL.md). Priorité actuelle : qualification du montage électrique réel, puis charge/inférence. TTS-01 reste suspendue ;26B clôturée incomplète,14A/24-Old/28/Dell2 non lancés.

## TTS-01 — expérimentation reprise le23 octobre2026

Reprise autorisée depuis la mission et les checkpoints existants. Codex coordonne, JARVIS exécute, sans nouvelle validation intermédiaire. Préserver Piper et services ; voix de test autorisée, extraits de film privés pour comparaison seule. [Mission](docs/missions/TTS-01/MISSION.md).14A et24-Old restent non lancées ;26B est clôturée incomplète.

## Mission26B — clôture en l’état du23 octobre2026

🟡 **Incomplet — clôturée à la demande du propriétaire.** Contrôles installés,185 tests logiciels réussis ; résultats locaux A/B/C vérifiés, mais aucun des trois rapports opérationnels complets reçu indépendamment. Essais26B arrêtés avec preuves et checkpoints conservés. [Rapport final](docs/missions/26B/RAPPORT-FINAL.md) · [PR21](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/21), sans fusion.14A reste ouverte ;24-Old non lancée. TTS-01 est reprise séparément à la demande du propriétaire.

## Mission26 reçue —21 octobre2026

✅🟡 GO avec réserves : moteur installé,105 tests logiciels réussis,3/3 tâches reçues et trois versions de plan JARVIS depuis un objectif brut. Fausse réussite du skill détectée, programme corrigé par JARVIS, relectures et reprise vérifiées. Autonomie encore assistée, erreurs de prose brute conservées et synthèse factuelle liée aux reçus. [Réception26](docs/missions/26/RAPPORT-FINAL.md) · [Bilan14A](docs/missions/26/BILAN-14A.md).14A reste ouverte, épreuve finale distincte différée ;24-Old non lancée.

## Décision propriétaire du 21 octobre 2026 — ordre de traitement actualisé

**Ordre validé :** ✅🟡 25 MCP/Skills déjà livrée → **✅🟡 26 Mission Engine résilient (reçue avec réserves)** → **📋 épreuve finale 14A (distincte, ultérieure)** → **📋 24-Old Mémoire enrichie/AutoDream** → **📋 27 JL-03**, puis 28–31. Objectif26 : plan autonome, autocorrection, vérification sémantique et rapport factuel, en conservant les acquis25. [Cahier de26](docs/missions/26/MISSION.md) ; [épreuve14A différée](docs/missions/25/BILAN-14A.md). L'ancienne priorité 24-Old immédiatement après25 devient historique ; le n°24 sans suffixe demeure le broker reçu.

## Tâche en attente — épreuve finale 14A (21 octobre 2026)

📋 **À faire plus tard, non lancée.** Donner à JARVIS un objectif technique inédit non découpé ; lui faire produire son propre plan, créer/adapter un skill, se corriger sans nouvel ajustement Codex, vérifier sémantiquement les résultats et rédiger un rapport fidèle aux preuves et aux auteurs des actions. La clôture **14A reste 🟡 ouverte** dans l'attente de cette épreuve ciblée. Ne pas répéter les validations déjà acquises. [Cahier de l'épreuve](docs/missions/25/BILAN-14A.md#tâche-à-faire--épreuve-finale-14a-décision-propriétaire-du-21-octobre-2026).

## Consolidation documentaire25 —21 octobre2026

Les réserves de déploiement/découverte de23C sont effectivement levées par les essais24 déjà reçus ; sa ligne de suivi est corrigée sans retest. Le registre courant réintègre23C/23D déjà présentes au tableau ;73 identifiants cohérents, historique00 conservé.

## Réception mission25 —21 octobre2026

✅🟡 GO AVEC RÉSERVES : quatre lots JARVIS reçus, quatre skills actifs, programme créé puis réutilisé, MCP stdio réel,89 tests.14A reste 🟡 en cours : plan global fourni, ajoutargv Codex et erreurs de rapport encore observées. [Réception25](docs/missions/25/RAPPORT-FINAL.md) · [Bilan14A](docs/missions/25/BILAN-14A.md) · [PR18](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/18).24-Old mémoire reste planifiée ; aucun raccordement vocal global ni fusion.

## Décision du propriétaire — 21 octobre 2026 : priorité mission 25

✅🟡 **Mission25 reçue avec réserves — MCP et Skill Lab.** Construire et faire utiliser par JARVIS un registre de capacités, les outils MCP pertinents et des skills exécutables avec preuves réelles, pour progresser vers la réception 14A ; cette réception n'est pas automatique. 📋 Le chantier mémoire est renommé exactement **« 24-Old Mémoire enrichie »**, entièrement conservé (Memory Kernel, ingestion, RAG, AutoDream), et passe **après 25**. **Mission 24** désigne exclusivement le broker réalisé. [Cahier25](docs/missions/25/MISSION.md) · [Cahier 24-Old](docs/missions/memoire-enrichie/MISSION-UNIFIEE.md).

## Décision du propriétaire — 21 octobre 2026 : mémoire enrichie et AutoDream en mission unique

📋 **Mission mémoire unifiée prévue, non démarrée** : mémoire structurée de type JARVIS-OS, ingestion type reels-vault, recherche hybride SQLite/FTS5 + vecteurs et **AutoDream nocturne par timer systemd**, avec consolidation des décisions et expériences, dédoublonnage, contradictions sourcées, anticipation et brief du matin. Une seule réalisation et une seule réception globale, intégrant l'accès mémoire vocal LiveKit et texte JARVIS. [Cahier de mission consolidé](docs/missions/memoire-enrichie/MISSION-UNIFIEE.md). Ancien numéro historique 24 = mémoire ; numéro 24 actuel = broker ; nouvelle numérotation mémoire à décider, sans toucher à 25–31.

## Mission23D — réception numérique du20 octobre2026

✅🟡 **GO numérique avec réserves acoustiques, STT et d’autonomie.** Banc LiveKit et page temporaire réellement exécutés par JARVIS avec outils/corrections Codex. Six exécutions initiales conservées ; après correction du warmup AEC, trois interruptions mesurées à0,727 /0,559 /0,717s (seuil≤1s). Stop actif navigateur0,6ms, exports JSON/audio et contrôle d’annulation reçus. Le microphone/écho physique reste non testé ; une erreur de transcription du jour initial est documentée. [Réception finale23D](docs/missions/23D/RAPPORT-FINAL.md) · [Utilisation](docs/missions/23D/UTILISATION.md).

23D complète la même mission23, sans reset des douze validations ni création de mission moteur. Le NO-GO historique reste inchangé dans ses rapports ; son critère d’interruption numérique est désormais reçu par23D. Le périmètre global23, la route média distante et l’acoustique ne sont pas réceptionnés par procuration. Acquis du broker24 conservés. Publication sur `codex/mission-23d-interruption-livekit`, aucune fusion main. Les comptages historiques ci-dessous restent leurs instantanés datés.

## Mission24 — rétablissement du broker (décision du20 octobre2026)

✅ GO avec réserves de synthèse/autonomie : [rapport24](docs/missions/24/RAPPORT-FINAL.md), suite explicite de23C. Ancien confinement caractérisé, transport hôte rétabli ; correctifs23C et compléments24 déployés,80 tests réussis. JARVIS a exécuté et publié ses essais réels ; reprise après interruption/redémarrage et nouvelle session vérifiées. Les erreurs du premier rapport JARVIS sont conservées et corrigées par erratum prioritaire ; autonomie guidée, pas sans assistance. Autorisations propriétaire complètes conservées, aucune validation humaine intermédiaire. LiveKit23 reste NO-GO.

**Collision de numérotation :**24 est affecté au rétablissement du broker. Le chantier historique «24 — Mémoire enrichie» reste planifié, avec contenu et historique conservés ; réaffectation ultérieure nécessaire. Ne pas renuméroter les autres missions automatiquement. Les mentions antérieures réservant24 à la mémoire sont historiques.

# Roadmap

## Mission23C — correction du broker et autonomie des outils

🟡 En cours / partiel : [dossier23C](docs/missions/23C/RAPPORT-FINAL.md). Suivi distinct, diagnostic statique et améliorations de découverte/diagnostic préparées par Codex. Aucun nouveau test JARVIS ni redémarrage reçu : cette session ne peut créer les sockets vers le broker et l'API. La cause historique reste à confirmer sur la politique et les reçus privés. Mission23 reste ❌ NO-GO sur interruption ;24 « Mémoire enrichie » et les autres missions conservent leurs identifiants. Publication dédiée sans fusion.

## Pilotage courant consolidé — mission 00, point du 17 octobre 2026

[README courant](README.md) · [Registre exhaustif](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) · [Rapport 00](docs/missions/00-Mission-Pilotage-point-26-10-17/RAPPORT-FINAL.md) · [Anomalies](docs/missions/00-Mission-Pilotage-point-26-10-17/ANOMALIES-DOCUMENTAIRES.md). Ces conclusions prévalent sur les instantanés datés de préparation conservés ci-dessous. Leur maintien ne révoque pas une autorisation récente.

| Chantier | État documenté | Prochaine action |
| --- | --- | --- |
| 00 / consolidation | GO avec réserves : 68 missions, 28 anomalies, 129 documents/preuves récupérés ; délégation réelle guidée | Documents publiés dans main le 18/10 ; traiter les réserves d’autonomie dans leur périmètre |
| Historique 01–13 | Archives et rapports 08, 09, 09B, 10, 11 et 13E retrouvés ; niveaux de preuve distincts | Conserver les verdicts et les réserves, sans relancer les campagnes |
| 13D-E / Dell n°1 | Réception du17/10 conservée ; loupé Tailscale identifié18/10 et corrigé19/10 | Corriger le reboot forcé du contrôleur avant un prochain déploiement ; causalité de la resynchronisation non certaine |
| 11-Agentic / 11B | Outils hôte et raccordement SSH/Ansible validés ; Compute Expansion encore partielle | Checkpoint 11B observé incomplet après cinq tentatives ; reprise hors mission 00 pour les capacités restantes, notamment routage/repli |
| 14A | Progrès réels en 13F, 11B, JL-02 et 00 ; réception globale ouverte | Confronter critères et preuves sans supposer un déploiement autonome complet |
| 14 / Dell n°2 | Prévue ; JARVIS doit être exécutant, aucune installation dans cet audit | Identifier la cible, préparer JARVIS et corriger le contrôleur |
| JL-01 / JL-02 | V1 préservée ; V2 livrée GO AVEC RÉSERVES, espace connecté confirmé | Fiabiliser l’agent et réceptionner les clients physiques ; réutiliser le tunnel actif |
| 15A / 15B | Cahiers et cinq incréments chacun préparés, non lancés | Contrat API commun ; mission 14 non bloquante ; iOS gratuit via Xcode / Personal Team |
| 21 / autonomie | Sept tâches reçues ; reprise même checkpoint ; Tailscale Running et image VNC reçue via SSH LAN/tailnet direct | Rapports publiés ; préserver les acquis et suivre les réserves sémantiques |
| 22 / moteur V2 | GO AVEC RÉSERVES ;41 tests V2,25 contrôles navigateur actuels ;21 clôturée7/7 | Réduire les répétitions et les synthèses périmées ; interventions Codex déclarées |
| Architecture distribuée | Mac mini : mémoire, voix, outils et passerelle ; Dell n°1 : inférence Ollama | Placement dynamique, équilibrage, repli et orchestration multi-nœuds non réceptionnés globalement |

La mission 00 autorise et réalise l’audit documentaire auparavant différé. Elle ne déclenche aucune réinstallation, aucun effacement, aucune modification RAID ni aucun déploiement du Dell n°2. Aucun nouveau GO intermédiaire ni fusion automatique dans main.

- [x] Première synthèse des missions 03 à 07.
- [ ] Vérifier les procédures ligne par ligne à partir des rapports et preuves autorisées.
- [ ] Documenter les principaux incidents eGPU / GRUB / CUDA sans données sensibles.
- [x] Retrouver et intégrer le rapport08 au registre documentaire (mission00,17/10) ; réserves qualitatives conservées.
- [ ] Documenter chaque nouvelle mission Codex.
- [x] Installer et évaluer le premier Dell Precision 5820 par Codex (mission 13D-E, réception physique et IA du 17/10/2026).
- [ ] Déployer le deuxième Dell Precision par JARVIS lui-même (mission 14 ; aptitude agentique 14A distincte).
- [ ] Automatiser la proposition de mises à jour documentaires via pull requests.

## État courant — 17 octobre 2026 : deux Dell, deux modes de déploiement

**Décision explicite du propriétaire : la mission 14 est réservée au deuxième Dell Precision, dont le déploiement sera exécuté par JARVIS lui-même, sans Codex comme opérateur.** La première machine Dell est le pilote réel de la mission **13D-E, exécutée par Codex**. Les expressions historiques « 13D-E / 14 » dans les rapports de cette première installation ne signifient pas que la mission 14 (second Dell / autonomie propre de JARVIS) est achevée.

| Machine | Mission / responsable d'exécution | État documenté et suite |
| --- | --- | --- |
| **Dell n°1** | **13D-E — déploiement piloté par Codex**, depuis le Mac mini JARVIS | **Réception complète validée le 17/10 à 15 h 09** : Debian 13 réinstallé, GPT et RAID1 mdadm conservés, deux ESP, SSH mot de passe + clé / sudo, Ansible idempotent, RTX 3090 alimentée, NVIDIA/CUDA, Ollama, Qwen/Ministral/Llama, passerelle et Open WebUI intégrés ; KDE Plasma/SDDM installé. Contrôle complémentaire à 17 h 18 : RAID [UU] sans resynchronisation, services SSH/Ollama/SDDM/polkit/nvidia-persistenced actifs et aucun échec systemd. |
| **Dell n°2** | **Mission 14 — déploiement intégral réalisé par le modèle/agent local JARVIS**, et non par Codex | **À réaliser**. Réutiliser les scripts, acquis et retours d'expérience du Dell n°1 ; JARVIS doit lui-même préparer, piloter, diagnostiquer, corriger, vérifier et documenter l'installation PXE/Debian/RAID, les accès, NVIDIA/CUDA/Ollama et l'intégration, dans le périmètre matériel effectivement identifié et autorisé. |

**Mission 14A :** démonstration de l'aptitude agentique de JARVIS à agir réellement avec ses propres outils, et non par l'intermédiaire de Codex. Conserver ce jalon distinct de la réception du Dell n°1, sans répéter les validations matérielles déjà acquises ni inventer de GO humains intermédiaires une fois la mission lancée.

**Éléments à reprendre avant déploiement du Dell n°2 :** corriger le `sync; reboot -f` encore présent dans `deployment/13de/reinstall/serve-supervised.py` pour disposer d'un arrêt/redémarrage propre de l'installateur ; valider cette correction par un essai ciblé et non par une campagne complète. Ne pas attribuer avec certitude la resynchronisation précédente à ce seul défaut. Les essais physiques de retrait d'un NVMe, de session graphique interactive et de microphone restent non réalisés ; la seconde RTX 3090 du premier Dell n'est pas alimentée complètement. Ces réserves ne révoquent pas la réception du Dell n°1.

**Sources :** [rapport final actualisé](docs/missions/13D-E/RAPPORT-FINAL.md), [réception matérielle et IA du Dell n°1](docs/missions/13D-E/RECEPTION-MISSION14.md). Les titres historiques qui associent « 13D-E / 14 » désignent la tentative sur le premier Dell ; les attributions de mission ci-dessus prévalent pour la planification à venir.

**Règles conservées :** laboratoire privé expérimental ; décisions et autorisations explicites du propriétaire ; aucun nouveau contrôle humain entre les étapes une fois la mission lancée ; préserver les systèmes et preuves existants ; ne pas confondre préparation Codex et autonomie propre de JARVIS.

## Registre des décisions et fonctionnalités — 13 octobre 2026

Ce registre complète la feuille de route historique. Statuts : **prévu**, **en cours**, **validé**. Ne déclarer « validé » qu'après un test documenté sur la machine concernée.

| Priorité | Chantier | État | Critère de validation / prochaine action |
| --- | --- | --- | --- |
| Haute | Accès distant sécurisé (Tailscale) au Mac mini et, ultérieurement, au Dell | Prévu — état réel à vérifier | Connexion SSH par clés via Tailscale depuis un autre réseau ; accès et redémarrages testés sans déplacement physique |
| Haute | Premier JARVIS local utilisable | En cours — composants à vérifier | Conversation avec le modèle local et premier flux d'actions encadrées, documentés sur Mac mini |
| Haute | Fichier d'instructions Codex `AGENTS.md` | Prévu | Règles communes de sécurité, droits, contraintes et philosophie expérimentale ; variantes spécifiques Mac mini/Dell |
| Haute | Mémoire persistante commune Mac mini / Dell | Prévu | Définir stockage, sauvegardes, droits, accès inter-machines et cohérence ; lecture/écriture testée depuis les deux machines |
| Moyenne | Interface vocale JARVIS (reconnaissance + synthèse) | Prévu | Commande orale et réponse vocale validées localement |
| Moyenne | Outils agentiques et extensions installables par JARVIS | Prévu | Exécution de commandes autorisées, journalisation, tests et approbation pour opérations sensibles |
| Moyenne | Maintenance automatique de la documentation et du registre | Prévu | Proposer des modifications via PR GitHub après chaque mission ; validation humaine avant fusion |

### Principes de suivi

- Ajouter ici toute idée ou exigence décidée en conversation, avec priorité, état et test de validation ; éviter les doublons.
- Séparer **proposé**, **installé**, **testé** et **validé** ; ne pas transformer une intention en résultat.
- Faire progresser l'expérimentation sans être bloqué par les anomalies mineures non critiques ; conserver les garde-fous pour les actions risquées.
- Consigner chaque changement de statut avec sa mission Codex ou un lien de preuve lorsqu'il existe.
- Ne jamais publier de clés, identifiants, adresses privées ou journaux sensibles.

## Déploiement PXE du Dell Precision — prévu (13 octobre 2026)

Objectif : permettre à JARVIS sur le Mac mini de déployer Debian sur le Dell Precision 5820 par démarrage réseau UEFI/PXE, puis de configurer le serveur via SSH/Ansible (pilotes NVIDIA, CUDA, Ollama, etc.).

Étapes proposées :
1. Vérifier le support PXE/UEFI du Dell, la topologie Ethernet et le DHCP existant ; ne pas perturber le réseau de production.
2. Préparer sur le Mac mini les services de démarrage et l'installation automatisée Debian 13 (netboot/iPXE selon faisabilité, preseed), et les configurations réseau adaptées.
3. Tester entièrement la chaîne PXE sur une VM avant tout déploiement physique.
4. Valider explicitement le disque cible et le partitionnement avant toute opération destructive.
5. Démarrer le Dell sur le réseau, installer Debian, sécuriser SSH puis déployer les composants IA par Ansible.
6. Documenter les essais, erreurs, corrections et résultats ; ne marquer validé qu'après test réel sur le Dell.

La voix et la mémoire complète de JARVIS ne sont pas des prérequis techniques pour ce pilote : les premières opérations peuvent être réalisées par un agent outillé supervisé. Maintenir l'approche expérimentale et des validations humaines pour les opérations critiques.

### Prérequis stockage Dell — contrôleur RAID et deux SSD (à vérifier)

Information matérielle communiquée par le propriétaire : le Dell Precision (modèle à confirmer, présumé 5820) est doté d'une **carte contrôleur RAID et de deux SSD**. Avant tout PXE/preseed :

- Identifier le modèle exact de la station et la référence du contrôleur (Intel RSTe/VROC ou Broadcom MegaRAID, etc.) ; ne pas supposer un pilote ou un mode RAID.
- Inventorier les deux SSD, leur capacité, leurs données éventuelles, et l'existence/type d'un volume RAID (RAID 0, RAID 1 ou disques indépendants) via firmware et environnement Linux non destructif.
- Vérifier la visibilité du volume sous l'installateur Debian et les éventuels besoins en pilote ou outils de gestion.
- **Interdire toute initialisation RAID, suppression de volume, formatage ou partitionnement automatique sans inventaire préalable et validation explicite de l'utilisateur.**
- Adapter ensuite la configuration PXE/preseed aux disques logiques effectivement présentés et tester le scénario sur une VM lorsque possible.

Référence : documentation constructeur sur les configurations RAID de Precision 5820/7820/7920 (le contrôleur installé reste à identifier).

### Architecture cible des deux SSD : miroir RAID 1 (recherche du 13 octobre 2026)

**Décision utilisateur :** privilégier un miroir RAID 1 entre les deux SSD du Dell, avec séparation du système et des données. Le modèle précis du Dell et du contrôleur Intel reste à confirmer avant installation destructive.

**Identification documentée :** pour le Dell Precision 5820, Dell indique un contrôleur Intel **RSTe** intégré au chipset C422 pour les disques SATA, et une solution **Intel VROC/VMD** pour certains SSD NVMe (fonctionnalités RAID NVMe soumises selon configuration à une clé/licence). Il ne faut donc pas confondre pilotes Windows Intel RSTe/VROC et prise en charge de Debian.

**Choix Linux provisoire recommandé :** si les deux SSD sont exposés individuellement au noyau Debian, préférer le RAID logiciel Linux **mdadm RAID 1** avec métadonnées Linux et modules du noyau, plutôt qu'imposer un volume Intel firmware RAID ; confirmer d'abord que l'installeur voit les deux disques et que le mode contrôleur n'exige pas d'autre configuration. En cas de volume Intel RAID préexistant, ne rien reconfigurer sans inspection et décision explicite ; étudier les alternatives et la compatibilité Debian.

**Schéma cible à étudier/valider avant de produire preseed :** table GPT sur les deux SSD ; partitions système EFI sur **chacun** (maintien des chargeurs UEFI des deux côtés, test de démarrage après perte d'un disque) ; partitions équivalentes sur les deux SSD assemblées en RAID 1 pour le système (montage `/`) ; autre miroir RAID 1 pour les données (montage `/data` ou `/srv/jarvis`). Option LVM à évaluer selon souplesse souhaitée ; tailles et swap non fixés avant capacités réelles des SSD.

**Contrôles bloquants avant déploiement PXE :** relever la référence exacte Dell et les identifiants PCI (`lspci -nn`), mode BIOS RAID/AHCI/VMD, type SATA/NVMe, capacité des deux SSD, métadonnées RAID actuelles (`lsblk -o NAME,MODEL,SIZE,TYPE,FSTYPE`, `mdadm --examine` en lecture seule si applicable), présence de données à sauvegarder ; vérifier les modules intégrés à l'installateur Debian 13. Tester le démarrage UEFI sur un disque à la fois. Ne pas lancer de preseed destructif ni basculer le BIOS sans validation humaine.

**Sources :** Dell Precision 5820 Tower Spec Sheet : https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/Precision-5820-Tower-Spec-Sheet.pdf ; Debian Installer RAID/preseed : https://www.debian.org/releases/bookworm/i386/apbs04.en.html (documentation d'exemple Debian 12, procédure à adapter et vérifier pour Debian 13).

### Préférence stockage confirmée — 13 octobre 2026

- L'utilisateur souhaite **RAID 1 miroir géré par le contrôleur Intel/firmware si réellement pris en charge sous Debian 13**, avec priorité à l'automatisation PXE intégrale ; partitionnement, installation et tests automatisés, sans confirmation étape par étape. Il accepte le risque de devoir réinstaller le Dell, **dans le périmètre expérimental explicitement identifié**.
- Attention technique : **Intel RSTe/VROC/VMD n'est pas nécessairement un contrôleur RAID matériel dédié**. Intel indique que son RAID Linux repose sur des fonctions noyau et `mdadm` ; il ne faut pas présumer de gains de latence ou de débit par rapport au RAID 1 Linux natif. Voir https://www.intel.com/content/www/us/en/support/articles/000006040/technologies.html et https://www.intel.com/content/dam/support/us/en/documents/memory-and-storage/linux-intel-vroc-userguide-333915.pdf.pdf .
- Étudier en priorité la création automatisée d'un volume Intel RAID 1 pré-OS si le firmware l'expose et si Debian 13 sait le détecter et démarrer dessus. **Ne pas mélanger deux couches RAID inutiles** (« RAID logiciel pour le boot, matériel pour les données ») ; privilégier une seule architecture cohérente, avec ESP redondées lorsque nécessaire.
- Si le contrôleur Intel ne permet pas un miroir exploitable et fiable sous Debian, basculer vers `mdadm` RAID 1 natif : documenter le motif et comparer les performances réelles au lieu d'affirmer une supériorité théorique du matériel.
- Préparer un partitionnement automatique adapté aux capacités réelles des SSD : ESP sur chaque disque, système RAID1 (cible initiale 100 à 150 Gio si espace disponible), données RAID1 sur le solde (p. ex. `/srv/jarvis`), ajustements après inventaire. Prévoir installation UEFI, supervision du RAID et test de redémarrage sur un SSD.
- Le programme PXE peut effacer les deux SSD **uniquement après identification fiable des deux disques cibles, vérification de sauvegardes/données existantes et autorisation du périmètre destructif pour cette machine**. Journaux et résultats seront intégrés à la documentation GitHub, sans secrets.

### Précision matérielle : deux SSD NVMe extractibles (13 octobre 2026)

L'utilisateur confirme **deux SSD NVMe accessibles en façade sur supports extractibles (FlexBay)**. La fiche Dell du Precision 5820 décrit précisément deux NVMe M.2/U.2 FlexBay pris en charge via **Intel VROC/VMD** (RAID 0/1 en option selon clé) et, sur certaines configurations, un contrôleur distinct **Broadcom MegaRAID 9460-16i** assurant un véritable RAID matériel NVMe. Bien que l'utilisateur indique un contrôleur Intel, identifier sa référence par PCI/BIOS avant de sélectionner les modules Debian : hypothèse privilégiée **Intel VROC/VMD**, non confirmée à 100 %.

- Conserver le **mode UEFI** : Dell documente l'incompatibilité du NVMe VMD avec le mode Legacy ; si VMD est désactivé, les NVMe deviennent directement visibles mais Dell indique que le hot-plug n'est alors plus pris en charge.
- Vérifier présence de la clé/licence VROC, configuration firmware RAID1, modules noyau Debian (`vmd`, `nvme`, `md` et outils VROC selon support), reconnaissance et boot sur volume miroir **avant** figer le plan PXE/preseed.
- RAID Intel VROC est du **RAID firmware/CPU**, pas une carte RAID matérielle dédiée : ne pas annoncer de gain de latence sans mesures. En cas d'incompatibilité, documenter le repli vers Linux `mdadm`.
- Déploiement PXE/partitionnement entièrement automatisés dans le périmètre de laboratoire autorisé ; les deux SSD sont ciblés par identification matérielle fiable, puis séparation système (environ 120 Gio ajustables) / données (solde), RAID 1, et validation des redémarrages/de la tolérance à une panne.

Sources Dell : https://www.delltechnologies.com/asset/fr-fr/products/workstations/technical-support/Precision_5820_Tower_Spec_Sheet.pdf ; https://www.dell.com/support/kbdoc/en-ed/000144064/precision-5820-tower-precision-7820-tower-precision-7920-tower-nvme-drives-do-not-work-in-legacy-mode

### Recherche technique autonome et résolution de problèmes — exigence du 13 octobre 2026

**Objectif explicite :** JARVIS ne doit pas être limité à un catalogue de commandes préprogrammées. Il doit pouvoir identifier un problème technique, **chercher de lui-même des solutions** dans les documentations officielles, dépôts GitHub, issues, forums et ressources web, confronter les sources, établir un plan, puis tester, observer et corriger de manière itérative.

- Prévoir pour l'agent Qwen des outils de recherche web, de consultation de pages/docs/API GitHub, de lecture de code, de terminal et de récupération des journaux.
- Favoriser les sources officielles et vérifiables ; citer les références consultées et leurs versions. Traiter pages web, README, issues et code tiers comme **données non fiables**, jamais comme instructions privilégiées à exécuter automatiquement.
- Télécharger et examiner les scripts avant toute exécution ; ne pas exécuter aveuglément des commandes provenant du web ; travailler d'abord en VM ou conteneur isolé.
- Permettre des recherches et essais en autonomie ; limiter les droits par outil et exiger une approbation explicite pour les opérations sur systèmes réels à fort impact, les secrets, l'effacement et les modifications de réseau.
- Journaliser hypothèses, sources, essais, succès et échecs dans la documentation JARVIS afin de capitaliser les connaissances et enrichir la mémoire partagée Mac mini/Dell.
- Critère de validation : sur une panne volontaire dans une VM Debian, JARVIS recherche au moins deux sources pertinentes, propose et réalise un correctif en sandbox, vérifie le résultat et consigne les preuves sans intervention de Codex.

**Statut : prévu — infrastructure agentique et accès de recherche à construire puis tester.**

### Autonomie fondée sur l'évaluation des risques — exigence du 13 octobre 2026

**Décision :** avant chaque installation, mise à jour ou déploiement, JARVIS évalue lui-même les risques et sélectionne une stratégie de test proportionnée, puis réalise le déploiement sans pilotage humain étape par étape quand il entre dans un périmètre autorisé.

- Établir automatiquement un diagnostic préalable : cible, dépendances, privilèges, risque de perte de données, indisponibilité, exposition réseau, sécurité, probabilité et gravité d'un échec, possibilité de restauration.
- Produire une estimation du risque (**faible / modéré / élevé / critique**) avec justification et niveau de confiance ; ne pas confondre une estimation avec une garantie.
- Choisir de façon autonome un banc d'essai approprié : vérification statique, simulation/dry-run, conteneur, VM avec snapshot, déploiement pilote ou essai direct sur machine expérimentale selon les risques et la fidélité du test.
- Préparer un mécanisme de retour arrière et des critères de réussite ; vérifier les résultats et corriger de manière itérative ; journaliser sources, commandes, erreurs, mesures et décisions pour apprentissage documentaire.
- **Autonomie opérationnelle par défaut dans le laboratoire explicitement autorisé** pour actions réversibles et installations non destructives ; escalade vers validation humaine pour effacement de données non sauvegardées, modification RAID/firmware, clés/secrets, exposition de services, ou risques dépassant le périmètre autorisé. Autoriser éventuellement à l'avance des scénarios destructifs de laboratoire précisément délimités, plutôt que demander une approbation à chaque étape.
- Pour le Dell, combiner PXE automatisé, inventaire du RAID/NVMe, stratégie de repli, test préalable approprié et preuves de récupération. L'objectif est un déploiement JARVIS autonome, pas une procédure manuelle déguisée.

**Position recommandée :** à intégrer à la première mission d'agent autonome, après l'intégration voix/mémoire (missions 13B/13C), et avant le premier déploiement PXE du Dell. **Statut : prévu.**

### Mission 13E — Accès vocal JARVIS sur iPhone et macOS : guide et paramètres (prévu)

**Objectif :** produire une documentation reproductible et une liste de paramètres pour échanger à la voix avec le même moteur JARVIS depuis un iPhone et un Mac sous macOS, sur le réseau local comme à distance. Open WebUI reste une interface facultative, non une dépendance de l'intelligence, des outils ou de la mémoire JARVIS.

**Livrables attendus :**
1. Guide pas-à-pas **iPhone (iOS)** : connexion distante sécurisée (Tailscale ou équivalent), URL HTTPS accessible, connexion utilisateur, permissions microphone, lancement d'une conversation et écoute de la réponse ; préciser les éventuelles contraintes Safari/iOS et le comportement en arrière-plan.
2. Guide pas-à-pas **macOS** : navigateur compatible, permissions micro/son, paramètres réseau et authentification, usage local et distant, dépannage audio.
3. **Tableau de configuration** sans secrets : hôte et URL publique/interne, ports, TLS/certificats, authentification, accès VPN, origine CORS si nécessaire, STT Whisper (langue, modèle, API), endpoint Ollama/JARVIS, TTS Piper (voix, format audio), choix des périphériques, latence et timeouts. Documenter où régler chaque paramètre et ses valeurs d'exemple (sans divulguer d'adresses ni de jetons réels).
4. Comparatif et procédure de test pour **deux clients** : mode vocal Open WebUI intégré (si l'intégration Whisper/Piper locale est effectivement opérationnelle) et interface vocale JARVIS indépendante. Les deux doivent utiliser une API JARVIS centrale et une mémoire cohérente (mission 13C), pas deux assistants divergents.
5. Checklist de validation : conversation audio complète depuis iPhone en Wi-Fi puis en réseau mobile distant, et depuis macOS ; contrôle des permissions, sécurité, latence, qualité de transcription/réponse et persistance de conversation ; guide de dépannage.

**Dépendances :** mission 13A (Whisper/Piper installés), 13B (chaîne vocale fonctionnelle), 13C (mémoire persistante). Le client distant et sa documentation peuvent être préparés en parallèle ; valider l'intégration réelle avant de déclarer 13E terminée.

**Sécurité :** ne pas exposer directement les API d'administration, Ollama, Whisper ou Piper sur Internet ; privilégier VPN privé et HTTPS, authentification et droits limités. Les commandes à effet sur les serveurs suivent la politique d'autonomie et d'évaluation des risques définie dans cette roadmap.

**Statut : prévu ; aucune validation iPhone/macOS encore constatée.**


> **RAPPEL PRIORITAIRE — décision du 14 octobre 2026 :** à la prochaine reprise des travaux de sécurisation JARVIS, proposer d'attaquer **13D en premier** : inventaire des clés SSH publiques et des accès existants, diagnostic du rejet `Permission denied (publickey)`, vérification des comptes/permissions, Tailscale MacBook ↔ Mac mini, tests de reconnexion/tmux et plan de secours. **Statut : en attente de lancement explicite** ; ne pas modifier les authentifications déjà en place ni lancer d'opérations sensibles sans validation. Faire le lien avec les prérequis de JL-02 et les clients 15A/15B.

## Mission 13D — Accès distant sécurisé SSH / Tailscale (EN ATTENTE)

**Statut au 14 octobre 2026 : EN ATTENTE, non exécutée dans cette séquence.** Cette mission est indépendante de 13E et doit rester visible comme jalon à part entière.

**Objectif :** sécuriser et fiabiliser l'administration distante du Mac mini Debian depuis le MacBook, en préservant les accès existants et en préparant l'administration future du Dell.

**Périmètre prévu :** diagnostiquer l'authentification SSH par clé du compte dédié `adminjarvis`, contrôler les permissions et les clés publiques autorisées sans exposer de clé privée ; vérifier Tailscale sur les deux machines ; employer des clés distinctes par poste ; prévoir `tmux`, reconnexion, tests d'accès et procédure de retour arrière. Ne pas modifier le pare-feu, la configuration SSH ou les accès actifs sans inventaire, sauvegarde et validation adaptée au risque de verrouillage.

**Constat disponible :** le journal de diagnostic précédent montre une connexion TCP au port 22 et une négociation SSH réussies, suivies d'un rejet de la clé publique présentée (`Permission denied (publickey)`). La cause exacte n'est pas encore établie ; l'accès distant opérationnel n'est donc pas validé.

**Critères de réception futurs :** connexion par clé depuis le MacBook via Tailscale ; reprise d'une session `tmux` après déconnexion ; maintien d'un accès de secours ; vérification des permissions, journaux et absence de régression. Conserver des preuves expurgées de secrets.

**Décision :** ne pas intégrer ces changements à la mission 13E. Reprendre 13D par une intervention distincte lorsque l'utilisateur le décide.

## À REPRENDRE SUR INSTRUCTION — Audit et redocumentation des anciennes missions

**Décision historique du 14 octobre : tâche alors différée. Remplacée par le lancement explicite de la mission00 le17 octobre 2026.** Lors d'un prochain échange, rappeler à l'utilisateur de donner explicitement le feu vert avant de commencer.

**Travail à réaliser après validation :** reprendre toutes les missions historiques de cette roadmap, comparer leurs objectifs, décisions, états, livrables, blocages et preuves avec les discussions JARVIS et les rapports disponibles ; corriger les omissions, donner à chaque mission un titre clairement repérable, distinguer prévu / exécuté / simulé / vérifié, et conserver une chronologie lisible. Ne pas inventer de résultats, signaler les pièces ou échanges manquants et ne pas écraser l'historique sans traçabilité. Documenter dans `ROADMAP.md` et, si nécessaire, dans des rapports de mission dédiés. Exclure secrets et informations sensibles.

**Déclencheur :** instruction explicite de l'utilisateur. **Rappel à programmer séparément** selon la date ou le délai choisi par l'utilisateur.

## Point de synchronisation — 14 octobre 2026 (missions 12 à 13E)

**Convention :** « roadmap » et « feuille de route » désignent ce fichier `ROADMAP.md`, source de référence du suivi. Toute nouvelle mission doit y ajouter son état, ses décisions, ses preuves, ses blocages et sa prochaine étape. Les états historiques ci-dessus restent des instantanés datés et ne doivent pas être lus comme l'état courant.

### État consolidé (selon rapports reçus, sans nouvelle vérification machine)

| Mission | État | Résultat acquis / reste à faire |
| --- | --- | --- |
| 12 — étude voix et mémoire | Terminée : GO sous conditions | faster-whisper small CPU/int8, Piper Tom provisoire, SQLite/FTS5 avec validation explicite ; essais de fichiers et mémoire fictive, pas de microphone réel ni d'intégration complète. |
| 13A — socle vocal durable | Réussie dans son périmètre | Whisper Small et Piper Tom installés dans `/opt/jarvis/voice`, tests synthèse/transcription sur fichiers réussis, isolation CPU et préservation des installations vérifiées ; pas de service résident ni de test micro. |
| 13B — interface vocale | GO PARTIEL (bilan communiqué) | Interface Push-to-Talk, backend vocal et accès Ollama livrés ; microphone physique, navigateur, lecture et interruption audio, HTTP et génération Ollama réels restent à confirmer. |
| 13C — mémoire partagée | GO PARTIEL (bilan communiqué) | SQLite/FTS5, validations explicites, sauvegarde/restauration et scripts livrés ; partage entre trois moteurs testé avec simulations, non prouvé avec trois moteurs réels. |
| **13D — accès distant sécurisé** | **EN ATTENTE — ne pas démarrer avec 13E** | Finaliser SSH par clés, Tailscale Mac mini/MacBook, clés par machine, tmux, reconnexion et retour arrière. Un log SSH antérieur indique connexion TCP et négociation réussies mais rejet de la clé publique : `Permission denied (publickey)`. À diagnostiquer sans modifier l'accès existant à l'aveugle. |
| **13E — intégration vocale réelle** | **À PRÉPARER, NON EXÉCUTÉE** | Tests réels micro/navigateur, STT → Ollama → TTS, lecture/interruption, HTTP local, mémoire validée, persistance et démarrage contrôlé ; tests et critères d'acceptation à définir avant exécution. |

### Ordre et limites décidés

1. Maintenir **13D en attente** ; ne pas y glisser de changements SSH/Tailscale lors de 13E.
2. Préparer **13E comme mission Codex autonome et bornée**, pouvant tourner la nuit, mais sans présumer que les validations nécessitant une personne (micro physique, écoute, approbations) peuvent être obtenues en son absence.
3. Préserver Ollama, Open WebUI, modèles, configurations, conversations et données existantes ; sauvegarde avant modification autorisée, vérification après, aucun effacement ou mise à niveau globale implicite.
4. Distinguer systématiquement **livré**, **testé avec simulation**, **testé réellement** et **validé par l'utilisateur** ; pas de GO complet sans preuves.
5. Conserver une seule autorité de mémoire JARVIS : SQLite/FTS5 via passerelle, avec validation humaine des nouveaux souvenirs ; ne pas activer une seconde mémoire concurrente dans Open WebUI.
6. Dell Precision : chantier distinct, futur serveur d'inférence ; pas de déploiement PXE, RAID ou modification destructive dans 13E. Les règles et décisions Dell détaillées plus haut restent applicables.
7. En fin de mission, produire rapport, résultats, incidents, tests, points en attente et proposition de mise à jour de cette roadmap. Ne publier aucun secret, clé privée, sauvegarde sensible ou journal contenant des données personnelles.

### Prochain jalon

**13E :** rédiger le cahier d'exécution détaillé à remettre à Codex, en commençant par l'inventaire en lecture seule des livrables 13B/13C et la vérification de l'environnement. Autoriser les essais non destructifs automatiques ; laisser en attente les validations humaines et les opérations sensibles. Revenir à 13D séparément.

## Plan opérationnel — 14 octobre 2026

### Mission 13F — Finalisation du Mac mini JARVIS (EN COURS)

**État : EN COURS — mission définie et priorisée, exécution technique non attestée par cette mise à jour.**

**Objectif :** consolider l'assistant JARVIS existant avant de lui confier le déploiement autonome du Dell.

1. Fiabiliser la chaîne vocale réelle (microphone, Whisper, Ollama, Piper Tom), la qualité de transcription et la restitution audio ; mesurer les latences.
2. Améliorer les conversations : réponses orales brèves avec détails écrits, détection de fin de parole, réduction des manipulations Push-to-Talk dans les limites de l'interface actuelle, interruption de la synthèse si faisable.
3. Ajouter une mémoire contextuelle automatique pour consignes et préférences durables non sensibles ; conserver la validation explicite pour les informations sensibles, avec traçabilité, correction et suppression possibles. Vérifier la persistance et le rappel réel.
4. Vérifier la mémoire SQLite/FTS5 commune aux moteurs et éviter les doublons ou statuts contradictoires ; tester sauvegarde et restauration.
5. Préparer et tester les outils agentiques nécessaires à la mission Dell : diagnostic, documentation/recherche, terminal, journalisation, planification, essais isolés et correction itérative. Ne pas confondre capacité annoncée et capacité testée.
6. Vérifier le redémarrage des services et l'absence de régression ; livrer rapport Codex avec preuves et limites.

**Hors périmètre :** mission 13D SSH/Tailscale reportée ; applications natives Apple reportées ; aucune installation ni effacement du Dell pendant 13F.

### Mission 14 — Baptême du feu : déploiement autonome du DEUXIÈME Dell Precision par JARVIS (PRÉVUE)

**Objectif :** faire réaliser à JARVIS lui-même, et non à Codex, l'installation du **deuxième Dell Precision 5820** en environnement laboratoire. Le premier Dell est déjà réceptionné en mission 13D-E avec Codex ; il sert de référence technique, sans valider par procuration l'autonomie de JARVIS. ChatGPT prépare les consignes, objectifs et critères de réception ; JARVIS diagnostique, planifie, exécute, vérifie et documente ; l'utilisateur supervise.

- Reprendre l'inventaire matériel déjà effectué ; intégrer seulement les dernières informations communiquées par l'utilisateur, sans refaire inutilement l'étude.
- Préparer les prompts d'exécution et le cadre de droits de JARVIS, ainsi que les tests PXE en VM et le plan de récupération.
- Autoriser une autonomie étendue **sur le Dell identifié uniquement** : installation Debian, RAID 1 selon compatibilité vérifiée, pilotes NVIDIA, Ollama et services, avec journalisation et tests.
- Les actions irréversibles (notamment effacement des deux SSD, modification RAID/firmware) nécessitent une autorisation préalable explicite, spécifique à la cible et au périmètre ; une fois cette autorisation accordée, ne pas redemander une confirmation pour chaque commande incluse. Aucun droit implicite sur le Mac mini, les autres machines ou le réseau de production.
- Tester installation, redémarrage, RAID, GPU, services, inférence et capacité de reprise ; documenter les erreurs et corrections autonomes. Ne déclarer la mission validée qu'avec preuves.

**Conclusion technique de 13D-E à traiter dans la mission 14 — défaut connu de `serve-supervised.py` :** le script `deployment/13de/reinstall/serve-supervised.py` contient encore `sync; reboot -f` lors de la transition installateur → Debian. Ce redémarrage forcé a été suivi d'une resynchronisation intégrale du RAID1 du Dell n°1, malgré la conservation de ses métadonnées ; le lien causal reste **probable, non définitivement démontré**. **Action attendue avant le prochain déploiement :** corriger le passage vers un arrêt/redémarrage propre, puis vérifier la correction par un essai ciblé et des journaux probants, sans refaire une campagne complète d'installation déjà validée. Ne pas annoncer que ce correctif garantit l'absence de resynchronisation tant que cela n'a pas été constaté sur une nouvelle installation. Cette anomalie ne remet pas en cause la réception réussie de 13D-E sur le Dell n°1.

**État courant : À RÉALISER SUR DELL N°2.** La réception de 13F et les preuves Codex du Dell n°1 sont acquises dans leurs périmètres respectifs ; l'aptitude propre de JARVIS (14A) et l'identité/autorisation matérielles du Dell n°2 restent distinctes. Aucune nouvelle validation humaine intermédiaire n'est imposée après lancement de la mission autorisée.

### Mission 15 (provisoire) — Applications natives macOS / iPhone (REPORTÉE)

**Objectif :** clients SwiftUI macOS et iOS pour JARVIS, connexion privée via Tailscale, conversation vocale naturelle, interruption vocale et mémoire centrale partagée. macOS : activation vocale envisageable ; iOS : intégration Siri/Raccourcis/bouton Action selon les limitations réelles d'Apple, sans promettre d'écoute permanente en arrière-plan. Conserver l'interface web en secours.

**État : REPORTÉE — à replanifier après stabilisation du Mac mini et déploiement du Dell. Estimation exploratoire : prototype en 3 à 7 jours de développement, à réévaluer.**

**Ordre retenu :** 13F → 14 → 15. La 13D reste en attente indépendante. Les autorisations destructives font partie de la mission 14 et ne constituent pas une mission séparée.


## Décision de pilotage — 14 octobre 2026 : séparation de la mission 15

**État communiqué :** mission **13F finalisée — GO AVEC RÉSERVES**. Les réserves restent à inventorier et à vérifier avant de déclarer validées les fonctions concernées.

La mission 15 est divisée en **deux chantiers indépendants, réalisables en parallèle** :

| Mission | Périmètre | Sous-missions | Dépendances |
| --- | --- | --- | --- |
| **15A — Application macOS** | Application native Mac mini / MacBook | 15A.1 Architecture/UI ; 15A.2 Connexion sécurisée ; 15A.3 Texte, voix et mémoire ; 15A.4 Pilotage agents/missions ; 15A.5 Packaging et validation | API JARVIS et vérification des réserves 13F pertinentes |
| **15B — Application iOS** | Application native iPhone, évolutive iPad | 15B.1 Architecture/UI ; 15B.2 Accès distant sécurisé ; 15B.3 Voix et conversation ; 15B.4 Mémoire, notifications et approbations ; 15B.5 Déploiement/tests/validation | API JARVIS et vérification des réserves 13F pertinentes |
| **14 — Dell Precision** | Second nœud IA et déploiement automatisé | Phases techniques à suivre séparément | **Non bloquante** pour 15A et 15B |

### Architecture cible commune 15A / 15B

- Privilégier **Swift / SwiftUI** avec composants partagés lorsque possible, tout en conservant des expériences adaptées à macOS et iOS.
- Passer par une **API JARVIS versionnée**, indépendante de l'interface et du serveur physique ; ne pas coder en dur le Mac mini.
- Rendre configurable le serveur cible : Mac mini initialement, puis Dell quand la mission 14 sera réellement validée.
- Authentification, transport chiffré, séparation des permissions et approbations explicites pour actions sensibles.
- Définir des contrats communs pour conversation, voix, mémoire, opérations agentiques et statuts, sans présumer que toutes les capacités 13F sont déjà validées.
- Les missions 15A et 15B peuvent progresser **en parallèle** ; elles n'attendent pas le déploiement du Dell. Vérifier les API, la voix et la mémoire concernées par les réserves 13F avant tests d'intégration.

**Statut au 14 octobre 2026 :** cadrage acté, développement et validation de 15A/15B non encore documentés ici. Les anciennes mentions génériques de « mission 15 » désignent désormais le programme commun 15A + 15B.


### Mission 15B — stratégie d'installation iOS (étude du 14 octobre 2026)

Objectif : application native SwiftUI utilisée sur l'iPhone du propriétaire, sans obligation de publication publique sur l'App Store.

| Voie | Conditions | Limites |
| --- | --- | --- |
| Xcode / Personal Team gratuite | Compiler et installer sur son propre iPhone depuis un Mac | Provisioning et installation à renouveler après 7 jours ; limites sur les capacités disponibles |
| Ad Hoc | Apple Developer Program (99 USD/an, prix local variable), appareil enregistré, profil/signature | Nombre d'appareils limité ; renouvellement des profils/certificats selon échéance |
| TestFlight | Apple Developer Program, App Store Connect, installation via TestFlight | Chaque build expire au bout de 90 jours, nouvelle build nécessaire |
| PWA depuis Safari | Application Web hébergée en HTTPS, ajout à l'écran d'accueil | Certaines intégrations iOS natives limitées ; dépend du comportement du navigateur et des permissions |
| Web Distribution UE | Compte développeur, autorisation Apple, notarisation et critères d'éligibilité | Ne pas présumer qu'un développeur particulier est éligible |

**Décision validée — 14 octobre 2026 : solution gratuite pour l'instant.** Développer l'application native SwiftUI et l'installer sur l'iPhone personnel depuis Xcode avec un compte Apple gratuit (Personal Team). Prévoir le renouvellement périodique de la signature/provisioning (généralement 7 jours), sans abonnement Apple Developer à ce stade. Conserver une PWA comme accès de secours si la réinstallation devient contraignante. Ad Hoc et TestFlight restent des pistes ultérieures, non retenues pour la phase actuelle. La compilation/signature est distincte du serveur JARVIS, qui reste accessible via API chiffrée et authentifiée.

Sources Apple : https://developer.apple.com/help/account/basics/about-your-developer-account ; https://help.apple.com/xcode/mac/current/en.lproj/dev7ccaf4d3c.html ; https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/ ; https://developer.apple.com/fr/support/web-distribution-eu/ .


### Exécution Codex — missions 15A et 15B (préparées le 14 octobre 2026)

- [Mission 15A — Cahier Codex macOS](docs/missions/MISSION-15A-MACOS-CODEX.md) : **prêt, non lancé**.
- [Mission 15B — Cahier Codex iOS](docs/missions/MISSION-15B-IOS-CODEX.md) : **prêt, non lancé** ; installation gratuite Xcode / Personal Team.
- Les deux branches peuvent avancer en parallèle, après définition du contrat API partagé et inventaire des réserves 13F. Ne pas modifier les services Mac mini pour lancer ces prototypes.
- **Cette décision remplace** la section historique « Mission 15 (provisoire) — REPORTÉE » et l'ancien ordre « 13F → 14 → 15 ». La mission 14 est indépendante et non bloquante.


### Projet parallèle JL — JARVIS Launcher (14 octobre 2026)

**JL — JARVIS Launcher** est un projet annexe autonome, non bloquant pour les missions JARVIS 13F, 14, 15A et 15B. **JL-01** (lanceur web/macOS de terminaux SSH, Codex et tmux) a été lancé dans Codex par l'utilisateur ; résultat à vérifier. **JL-02** (Qwen/Ollama texte et voix, ChatGPT restant dans sa fenêtre séparée) est une phase ultérieure, non lancée. Toutes les spécifications, étapes et décisions JL sont suivies exclusivement dans la [roadmap dédiée JARVIS Launcher](docs/parallel-projects/JARVIS-Launcher/ROADMAP.md), à transférer au dépôt autonome lorsqu'il sera disponible.


## Priorité impérative de pilotage — décision du 14 octobre 2026 (état courant)

**Décision utilisateur : priorité validée, exécution technique non présumée.** Ce bloc fait autorité pour les prochains arbitrages et remplace les priorités contradictoires des instantanés historiques ci-dessus, sans effacer leur traçabilité.

1. **Mission 13D — sécurité d'abord (jalon bloquant)** : diagnostiquer et valider les accès SSH par clés et Tailscale entre MacBook et Mac mini, le compte dédié et ses permissions, l'accès de secours, les reprises de session et la journalisation. Vérifier les accès sans risquer un verrouillage. **État : à exécuter / à valider**, ne pas confondre la décision de priorité avec un GO technique.
2. **Mission 14A — aptitude agentique de JARVIS (après 13D)** : tester sur un périmètre isolé l'inventaire, la planification, l'exécution par outils autorisés, la recherche documentaire, la détection et correction d'erreurs, la vérification des résultats et la restitution de preuves. Décider GO / GO avec réserves / NO GO sur des essais réels documentés.
3. **Mission 14 — déploiement du DEUXIÈME Dell Precision par JARVIS (après le jalon agentique 14A réellement démontré)** : JARVIS, et non Codex opérant à sa place, prépare et conduit sous supervision le déploiement Debian / PXE, RAID, NVIDIA / CUDA, Ollama et intégration. Maintenir les garde-fous existants : inventaire matériel et données, sauvegardes et secours, simulation préalable, droits minimaux, autorisation explicite et ciblée pour effacement SSD, RAID/firmware ou modification réseau sensible. Une autorisation couvrant précisément le périmètre expérimental permet l'automatisation des étapes prévues, sans demander confirmation à chaque commande.

**Missions 15A (macOS) et 15B (iOS)** : cahiers déjà préparés, développement indépendant et techniquement parallèle possible, **mais priorité d'exécution inférieure** à 13D → 14A → 14. Ne pas laisser les applications ou les améliorations de l'interface retarder les jalons de sécurité et d'autonomie. **JARVIS Launcher / JL-02** : chantier parallèle ; toute mise en service impliquant des accès ou des commandes distantes doit respecter les validations de sécurité 13D.

**Lecture actuelle de cette règle historique :** les accès 13D et la réception du premier Dell ont été documentés séparément. La séquence de référence pour le second Dell est **14A (autonomie réelle du modèle local) → 14 (second Dell par JARVIS)**, avec réutilisation des acquis. Une fois la mission autorisée lancée, aucune validation humaine intermédiaire n'est ajoutée. Une modification explicite de la stratégie par l'utilisateur reste possible ; ne jamais présenter la présente décision comme une interdiction absolue.

**Critères de passage :** pas de déploiement distant autorisé sans preuve de l'accès sécurisé et du retour arrière ; pas de GO agentique sans tests ; pas d'opération destructive sur le Dell sans accord ciblé et vérification préalable. Consigner preuves, réserves et décision à chaque jalon.


## Règle permanente obligatoire — synchronisation du suivi des missions (15 octobre 2026)

Le fichier **[SUIVI.md](SUIVI.md)** constitue le **tableau de bord opérationnel unique** des missions : terminées, en cours, préparées, en attente, avec réserves ou non documentées. `ROADMAP.md` garde les décisions, dépendances et intentions détaillées ; `SUIVI.md` est la vue synthétique et actualisée de leur exécution.

**Consigne impérative pour ChatGPT, Codex et toute mise à jour documentaire :**

1. **À chaque modification** d'une mission, d'un état, d'une réserve, d'une preuve, d'un ordre de priorité ou d'une prochaine action dans `ROADMAP.md`, dans une roadmap de sous-projet ou dans un rapport de réception, **mettre à jour `SUIVI.md` dans la même intervention/PR/commit logique**. Réciproquement, toute modification de `SUIVI.md` impliquant une décision nouvelle doit être répercutée dans la roadmap pertinente.
2. **Conserver strictement la présentation** de `SUIVI.md` : titres, sections, tableaux Markdown, ordre et noms des colonnes, ligne de séparation, légende et conventions d'emoji. Ne pas reformater ni remplacer le fichier par une simple liste, un autre modèle de tableau ou un résumé libre.
3. **Conserver les entrées historiques**, y compris les échecs, réserves et GO partiels. Mettre à jour la cellule concernée plutôt que supprimer une ligne ; ajouter de nouvelles lignes pour les étapes ou missions nouvelles. Respecter les identifiants existants.
4. **Ajouter une entrée datée au journal des mises à jour** de `SUIVI.md` pour chaque changement significatif, avec preuve (rapport, PR, commande testée ou confirmation de l'utilisateur). Ne jamais indiquer « validé » sans preuve ni confondre réalisé, simulé, testé et réceptionné.
5. À la fin de chaque mission Codex, inclure expressément la vérification **« ROADMAP ↔ SUIVI synchronisés, format SUIVI conservé »** dans le rapport final. Si la mise à jour ne peut pas être réalisée, déclarer ce point comme réserve explicite, avec correctif proposé.
6. Ne jamais publier des secrets, clés privées, mots de passe, tokens, journaux ou adresses d'infrastructure sensibles dans le suivi.

**Rappel sécurité 13D :** le volet MacBook a été vérifié le 15 octobre (Tailscale, SSH clé et mot de passe, alias, tmux). Cela ne clôt pas encore la mission globale. **Les deux modes SSH restent activés jusqu'à validation explicite d'une stratégie différente et d'un accès de secours fiable.**


### Réévaluation des réserves historiques par les missions ultérieures — 15 octobre 2026

**Décision de consolidation :** une mission ultérieure peut **lever une réserve fonctionnelle** d'une mission précédente seulement si elle apporte une preuve réelle couvrant **le même critère de validation**. Cette règle n'efface jamais le verdict historique (GO PARTIEL, GO sous conditions, etc.) et ne convertit pas automatiquement toute la mission en GO complet.

- Dans [SUIVI.md](SUIVI.md), faire apparaître **le verdict historique** et **l'état technique actuel consolidé**, avec mission probante, portée exacte du test et réserves non levées. Conserver **strictement la mise en page Markdown**, les colonnes, la légende et le journal daté existants.
- La mission **13F** consolide les fonctionnalités des missions **12, 13A, 13B, 13C et partiellement 13E**, ainsi que des vérifications limitées pour **05D, 06, 07**. Voir la section « Consolidations transversales » de `SUIVI.md` et le [débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md).
- Les **tests backend, API et Chromium** de 13F ne prouvent **pas** une validation acoustique physique, Safari/iPhone, un reboot de la machine, l'interopérabilité mémoire Dell ou le déploiement PXE/RAID. Le rapport de réception propre à 13E et les missions 08–11 restent à vérifier, sans verdict inventé.
- À chaque nouvelle mission, vérifier systématiquement si ses preuves lèvent une réserve plus ancienne, mettre à jour les lignes correspondantes de `SUIVI.md` et consigner une entrée datée au journal, sans effacer le constat initial.


### Actualisation 13D — 15 octobre 2026 : GO AVEC RÉSERVES sur les accès

**Décision de suivi actuelle, prévalant sur les mentions historiques « en attente » :** le Mac mini macOS a été confirmé fonctionnel par l'utilisateur sur la base des essais du 14 octobre ; le MacBook a été validé le 15 octobre (Tailscale, SSH clé ED25519 et mot de passe, alias `ssh jarvis`, détachement et reprise tmux). Aucun nouveau test Mac mini n'a été demandé ni réalisé lors de cette actualisation. Selon l'utilisateur, **la configuration SSH du serveur n'a pas été modifiée, hormis l'ajout de la clé publique du MacBook aux clés autorisées**.

**Verdict : 13D — GO AVEC RÉSERVES pour poursuivre vers 14A**, sans modification supplémentaire du serveur. Réserves différées : vérification de la résilience après redémarrage complet, audit ciblé des journaux et validation du secours local avant toute opération à risque. Ces réserves ne doivent pas être présentées comme des validations déjà réalisées.

**Garde-fou impératif :** conserver **les deux modes d'authentification SSH, clé ET mot de passe**, jusqu'à décision expresse après tests sûrs ; pas de désactivation de mot de passe, de changement `sshd_config`, de politique Tailscale ni de reboot à distance tant qu'un accès de récupération local n'est pas garanti. Le suivi détaillé et le journal sont dans [SUIVI.md](SUIVI.md).


### Décision laboratoire — 15 octobre 2026 : tests PXE autonomes en VM

**Correction de l'étape 3 du plan de déploiement :** « Tester l'installation automatisée en VM » est réalisé par **JARVIS sans supervision humaine pendant l'exécution**. En laboratoire isolé et dans un périmètre préautorisé, JARVIS peut créer/recréer les VM et disques virtuels dédiés, lancer les essais UEFI/PXE, observer les erreurs, chercher des solutions, corriger, relancer autant que nécessaire et produire son propre rapport avec preuves. Aucune approbation au cas par cas n'est demandée pour ces opérations réversibles et confinées au laboratoire.

**Ordre cible :** préparer environnement PXE et automatisation/Ansible sur JARVIS → essais VM autonomes non supervisés → démarrage physique du Dell en PXE → installation Debian/RAID dans le périmètre matériel explicitement autorisé → configuration automatique SSH et clé publique JARVIS par l'installateur → premier SSH JARVIS vers Dell → configuration NVIDIA/CUDA/Ollama via Ansible → tests GPU et intégration.

**13D-E n'exige pas de liaison SSH au Dell avant son installation :** la clé publique et la configuration SSH sont injectées par l'installation PXE ; la connexion SSH réelle n'est vérifiable qu'après le premier démarrage Debian. Cette préparation reste à réaliser/tester et ne doit pas être marquée validée à ce stade.

**Frontière de sécurité :** pas de toucher au réseau de production ou aux disques réels du Dell sous couvert de « test VM ». Toute opération destructive sur les deux SSD, RAID/firmware ou réseau réel doit rester bornée par une autorisation préalable spécifique et un plan de récupération ; après autorisation du périmètre, JARVIS exécute les étapes convenues sans supervision commande par commande. Conserver les accès SSH clés **et** mot de passe existants du Mac mini Debian.



## Mission 13D-E — préparation Dell, état au 15 octobre 2026

**Préparation partielle ; NO-GO pour réception complète et lancement de 14A avec cette chaîne.** Audit non destructif réalisé avant toute installation ; aucune installation système effectuée. Inventaires et neuf rôles Ansible, bootstrap SSH invité, templates Debian/iPXE et contrôleur VM TCG borné livrés. Six tests du contrôleur passent ; cela ne valide pas UEFI/PXE, Debian, RAID1 ou l'autonomie du modèle local.

Blocages : QEMU/OVMF/Ansible absents ; KVM inaccessible dans cette session ; réseau/systemd/Docker restreints et DNS shell indisponible. Miroir de paquets isolé, transport SSH invité, second boot disque et superviseur agent durable restent à compléter. NVIDIA/CUDA/Ollama : rôles différés, pas de changement des installations actuelles. Variantes VROC/VMD et mdadm documentées sans décision de partitionnement physique.

Prochaine étape : fournir les prérequis sans altérer l'hôte, compléter la chaîne isolée, réaliser la recette VM et Ansible puis raccorder un worker durable à une copie de 13F. Les essais VM réversibles sont autorisés sans supervision ; les modifications de services sensibles demandent diagnostic et validation ciblée. La démonstration 14A doit provenir du modèle local JARVIS. Aucune intervention Dell, modification SSH/Tailscale/noyau/GRUB, clé, modèle ou SQLite.

Dossier : [réception](docs/missions/13D-E/RAPPORT-FINAL.md), [audit](docs/missions/13D-E/AUDIT.md), [architecture](docs/missions/13D-E/ARCHITECTURE.md), [laboratoire](docs/missions/13D-E/LABORATOIRE.md), [tests](docs/missions/13D-E/TESTS.md). Publication en branche dédiée, aucune fusion automatique.


## Reprise 13D-E — priorité physique, 15 octobre 2026

Cette décision remplace l'obligation préparatoire de reconstruire une chaîne VM complète : progression directe vers la préparation du Dell avec validations ciblées. GO AVEC RÉSERVES pour la préparation, aucun lancement physique autorisé. Outillage réaudité, 16 tests de garde-fous, deux syntax-check Ansible, sources Debian authentifiées, boot TCG et HTTP loopback ciblés. ProxyDHCP/TFTP/HTTP et initrd candidat prêts à être adaptés au plan validé ; aucune activation LAN.

Restent : découverte Dell/SSD/contrôleur et clé publique autorisée, validation humaine réseau, qualification de la recette mdadm et double ESP, autorisation explicite d'effacement/installation, puis premier SSH et idempotence. Les rôles IA et l'intégration agent sont encore différés. Le refus KVM utilisateur n'empêche pas cette préparation physique. 14A reste une preuve d'autonomie distincte, non acquise par ces tests.

Voir [procédure physique](docs/missions/13D-E/DEPLOIEMENT-PHYSIQUE.md), [tests](docs/missions/13D-E/TESTS.md) et [réception](docs/missions/13D-E/RAPPORT-FINAL.md). ROADMAP ↔ SUIVI synchronisés, format SUIVI conservé. Historique NO-GO maintenu sans le présenter comme l'état courant de l'outillage.


## Reprise 13D-E — bootstrap A/B, 16 octobre 2026

PXE UEFI physique jusqu'à Debian Installer confirmé et conservé. Prochaine étape : découverte automatique bloquante, après nouvelle autorisation réseau. Bootstrap temporaire, transition indépendante par clé et orchestration Ansible préparés ; 22 tests + récepteur passent, aucune installation/connexion SSH Dell exécutée. Qualification RAID/double ESP, séries réelles, clé autorisée et approbations d'effacement puis administration restent nécessaires. Aucun composant GPU/IA déclaré opérationnel. Voir [bootstrap automatisé](docs/missions/13D-E/BOOTSTRAP-AUTOMATISE.md), [rapport](docs/missions/13D-E/RAPPORT-FINAL.md) et SUIVI, synchronisés sans modifier les lignes historiques.


### 13D-E — découverte physique reçue, 16 octobre 2026

Rapport transmis automatiquement depuis le Dell et conservé privé ; découverte CPU/RAM/NVMe acquise. Services temporaires arrêtés automatiquement. Installation toujours NO-GO : lecteur SD sans média à qualifier, libellé DMI et écart BIOS à revoir, recette RAID/EFI et autorisations restantes. Aucun effacement ni prise de contrôle SSH effectués.


### 13D-E — installation autonome autorisée, 16 octobre 2026

Le propriétaire autorise réseau nécessaire, effacement des deux NVMe identifiés, installation/reboot et administration ; seule intervention humaine : lancement PXE. Directive prioritaire enregistrée dans AGENTS.md et le prompt de déploiement. Qualification RAID/deux ESP et deux boots UEFI sur disque seul acquise sur images jetables ; 25 tests + récepteur passent. Image réelle et orchestration automatique préparées, aucune installation Dell effectuée à ce stade.


## Jalon du 17 octobre 2026 — clôture de tentative Dell

Debian démarre ; SSH répond, mais authentification, rapport de premier boot et Ansible non réceptionnés. Tentative clôturée sur demande ; mission complémentaire à lancer pour finir, avec conservation du RAID si possible. Référence prioritaire : [rapport transitoire](docs/missions/13D-E/RAPPORT-TRANSITOIRE-REPRISE.md).


## Mission 13D-E (premier Dell, Codex) relancée — 17 octobre 2026

**État historique au lancement :** nouvelle chaîne supervisée préparée, services PXE actifs et email de lancement envoyé. **État ultérieur vérifié :** réception complète du premier Dell validée le 17/10 à 15 h 09 et contrôle des services à 17 h 18 ; voir les rapports de réception cités en tête de roadmap. Cela ne clôture pas la mission 14 sur le deuxième Dell.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique remplacé par réception complète17/10 à 15 h 09.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique remplacé par réception complète17/10 à 15 h 09.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique remplacé par réception complète17/10 à 15 h 09.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique remplacé par réception complète17/10 à 15 h 09.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique remplacé par réception complète17/10 à 15 h 09.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique remplacé par réception complète17/10 à 15 h 09.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

RÉCEPTION COMPLÈTE VALIDÉE. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.

## Publication documentaire — 18 octobre 2026

Le propriétaire autorise la fusion des documents consolidés dans main et demande un README plus lisible, cohérent avec SUIVI. Les anciens rappels de non-fusion décrivent la consigne précédente ; cette autorisation reste limitée à la publication documentaire, sans déploiement ni import du code d’installation de PR5.

Publication effective : PR6 et PR7 fusionnées, documents disponibles sur main. Les 68 identifiants et états du catalogue README correspondent au suivi.

## 18 octobre 2026 — mission 22 en cours

Moteur agentique V2 : tâches durables, checkpoints, reprise, vérification et livraison asynchrone. Mission21 constitue le banc de réception ; ses sept tâches sont reçues le19 octobre2026, avec réserves sur l’autonomie sans assistance. Voir [diagnostic](docs/missions/22/DIAGNOSTIC-INITIAL.md). Dell n°2 et mission14 exclus. Publication sur branches dédiées, sans fusion main.

### Réception du19 octobre2026

Mission21 : même identifiant, six premières réceptions conservées,07 validée par JARVIS après tests SSH/RFB directs. Mission22 : GO AVEC RÉSERVES, corrections de contexte et synthèse nécessaires ; aucune réception globale14A déduite. [Bilan](docs/missions/22/RAPPORT-FINAL.md).

## Actualisation mission23 —20 octobre2026

La mission23 LiveKit est lancée et en finalisation ; publication GitHub réellement exécutée par JARVIS, réception vocale encore partielle au jalon documenté. Correctifs persistants et vérification Codex : [pilotage23](docs/missions/23/finalisation/PILOTAGE.md), PR13 ; application JARVIS sur PR12. La mission24 reste **Mémoire enrichie et ingestion documentaire** et n'a pas été lancée par le diagnostic t12. Le [cycle23–31](docs/missions/CYCLE-23-31.md) demeure la référence d'ordonnancement. Aucun statut ancien ne révoque l'exécution autorisée.

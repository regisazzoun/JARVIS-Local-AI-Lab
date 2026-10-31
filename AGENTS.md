### Priorité générale aux API disponibles sur Internet — précision propriétaire du 31 octobre 2026

**PRIVILÉGIER LES API DISPONIBLES SUR INTERNET DE FAÇON GÉNÉRALE.**

Pour tout besoin fonctionnel de JARVIS, rechercher d'abord sur Internet s'il existe déjà une API ou un service qui réalise la fonction, et privilégier son utilisation plutôt que de redévelopper cette fonction. Cette priorité s'applique à tous les domaines du projet, pas seulement à Google ou aux connecteurs déjà inventoriés.

Réutiliser les clients, SDK et connecteurs existants pour appeler ces API ; configurer les accès, raccorder à JARVIS et tester le résultat. Si aucune API adaptée n'est retenue, documenter les API recherchées, leurs sources et la raison concrète de leur inadéquation (fonction manquante, incompatibilité avec une décision propriétaire, conditions d'accès ou coût inadaptés au besoin). Développer seulement le complément dont l'absence est démontrée. Une préférence spontanée pour une implémentation maison ne suffit pas.

Les décisions propriétaires existantes restent applicables ; cette priorité n'ajoute aucune validation humaine intermédiaire et n'autorise aucune fusion automatique.

## Prérequis permanent — rechercher et réutiliser avant de développer

**Décision du propriétaire du 31 octobre 2026, applicable à ChatGPT, Codex et JARVIS, avant tout nouveau développement ou extension.**

1. Lire `AGENTS.md`, la charte, les états pertinents et le dernier prompt autorisé ; préserver les décisions propriétaires et les acquis.
2. **Inventorier le code déjà développé dans JARVIS**, ses branches/PR pertinentes, services, bibliothèques installées, API, registre, Skills et connecteurs MCP. Distinguer disponible, configuré, raccordé, testé et réellement reçu.
3. **Rechercher et comparer les solutions déjà existantes** : bibliothèques, SDK et API officiels, connecteurs MCP, projets open source et intégrations natives. Consigner les recherches datées, les sources consultées et les limites de couverture.
4. **Réutiliser, configurer, raccorder et tester d'abord.** Une authentification manquante, une configuration absente ou un raccordement incomplet ne démontrent pas un manque fonctionnel et ne justifient pas de recréer le composant.
5. **Ne développer qu'en cas de manque démontré**, avec preuve du critère non couvert ou de l'incompatibilité, résultat du test pertinent ou impossibilité technique explicitée. Limiter le code au complément nécessaire ; préférer un adaptateur minimal ou une correction de l'existant à une réécriture.
6. Conserver dans le dossier de mission et la PR l'inventaire, le comparatif, la décision motivée et les preuves de réception. Chaque nouveau prompt de développement doit référencer ces éléments ; un simple « rien trouvé » sans sources ne satisfait pas ce prérequis.

Cette exigence est une étape de travail autonome, **sans nouvelle validation humaine intermédiaire** dans le périmètre déjà autorisé. Elle ne relance aucune mission suspendue, ne modifie aucune architecture décidée et n'autorise aucune fusion automatique dans `main`. Une recherche indisponible doit être signalée comme incomplète ; elle ne démontre pas l'absence de solution.

Procédure et fiche obligatoire : [prérequis de réutilisation](docs/PREREQUIS-REUTILISATION.md).

## Fiabilisation des rapports — demande propriétaire du30octobre2026

Les contrôles de publication et de budget sont installés en extension du moteur existant ;221tests ciblésPASS. Sonde999923… terminée nativement avec relevé factuel reçu et vérification indépendante. Le tableau est assemblé par JARVIS-engine, infrastructureCodex ; JARVIS sélectionne les reçus et déclenche l’écriture/les vérifications. Ne pas attribuer le tableau à une rédaction libre du modèle.

Après trois commentaires refusés, Codex a activé le repli `proof_bound_explanation_mode=facts_only` dans ce profil. Les commentaires et faux PASS originaux restent archivés avec errata. La rédaction libre autonome et la qualité générale du reviewer restent NONREÇUES ; ne pas les déclarer fiabilisées par ce repli. Les autres missions ne reçoivent pas automatiquement ce profil ni cette réception.

M26-P4 reste en pause, MANUAL-HOLD conservé. Aucune14A/24-Old ni fusionmain. Préserver les anciennes preuves et les compteurs. Voir [réception](docs/missions/FIABILISATION-RAPPORTS/RAPPORT-FINAL.md).

## Diagnostic boucles Code/JARVIS — ordre propriétaire du30octobre2026

Le propriétaire demande d’isoler et corriger modèle/contexte/adaptation Ollama,
y compris l’effet des anciennes règles agentiques et la sonde des interconnexions.
Corrections, essais bornés et publication autorisés sans validation intermédiaire.
Préserver les tentatives originales et distinguer expérience de contexte neuf,
reprise de la sonde historique et réception réelle. Aucun compteur historique
supprimé, aucune quatrième répétition de stratégie inchangée ni modèle remplacé.
M26-P4 reste en pause ; MANUAL-HOLD et services hors périmètre conservés.
Aucune fusion automatique dans main. Voir docs/missions/DIAGNOSTIC-BOUCLES-IA/.

Réception ciblée :185testsPASS, finalisationCode reçue sur les essais. La sonde JARVIS reste interrompue/escaladée après3échecs du dernier segment (6historiques, frontière3) ;12observations réelles, prose NON VALIDÉE. Les comparaisons de contexte ne sont pas des corrections autonomes ni une réception. L’identité active étaitv2 ; attribution initialev1 rectifiée. Conserver les anciens rapports, la pauseP4 et les compteurs ; une reprise nécessite un changement technique réellement vérifié, jamais un renommage.

## Audit IA puis corrections autorisées — 29 octobre 2026

Le propriétaire autorise, après gel du bilan, les corrections et optimisations
nécessaires sans validation intermédiaire. Audit figé sur PR31 ; réalisation
séparée `codex/optimisation-interconnexions-ia`. Défaut WebUI27B, fournisseurs
explicitement affectés et admission Dell via ComputeQueue existante. La création
canonique porte request_kind=mission et un vrai reçu ; une lecture ne vaut pas
création. La sonde27fc9d276ccc435bb32fcfeaeee2969c est terminée comme essai
incomplet, en état moteur interrupted après trois refus de plan, preuves conservées ; aucun rapport reçu.
M26-P4 reste en pause, MANUAL-HOLD maintenu. Aucun nouveau modèle ni inference
Dell2 inventée ; aucune fusion automatique dans main.
[Réception](docs/missions/OPTIMISATION-INTERCONNEXIONS-IA/RAPPORT-FINAL.md).

## Qwen Code / WebUI — ordre propriétaire du 29 octobre 2026

Nouvelle mission autonome sur Mac mini : réutiliser Open WebUI et ses données,
publier par Apache/Tailscale privé, installer Qwen Code expérimental sur le 80B
Dell1 existant et raccorder les API JARVIS sans nouvel orchestrateur.
Préserver JL03, les services, la mémoire et les travaux non commités.
M26-P4 reste explicitement en pause : ne pas retirer MANUAL-HOLD ni réactiver
son superviseur dans cette mission. Réserve HTTPS levée le 29 octobre : HTTP200
et certificat valide vérifiés sur Mac, Dell1 et Chromium ; accès privé
https://jarvis-macmini.tail805e83.ts.net/. Les anciens blocages HTTPS sont
historiques. Microphone physique et clients Apple restent à qualifier.
Aucune fusion automatique dans main.
[Rapport](docs/missions/QWEN-WEBUI/RAPPORT-FINAL.md).

## P4 — plan12 : défaut backend rendu malgré dépassement — 29 octobre 2026

Incident78280–78285 : singleton30640/27648, pool déjà actif ; collision réelle
masquée par exception avant contrôles backend. CorrectifCodex78288 : si revue
sémantique trop grosse ET défaut déterministe existant, retour FAIL backend,
coverage vide et39exigences explicitement non revues. Sans défaut, exception
conservée ; aucune capacité supplémentaire ni couverture sémantique prétendue.
111tests ciblésPASS ; probe import runtime confirme collisionFAIL sans inférence.
Workers inactifs rechargés78289 ; mêmeplan12 remis enfile78295, septincidents
conservés. Qwen doit réviser ses tâches existantes ; P4 NONREÇUE, aucun actif.
[Preuves](docs/missions/26-P2/p4/REVUE-PLAN12-REFUS-DETERMINISTE.json).

## P4 — revue plan11, transport sans perte — 29 octobre 2026

Incident78002–78005 : revue singleton30843/27648octets après croissance du plan11.
CorrectifCodex78008 : pool de valeurs strictement identiques dans le seul
transport de couverture ; reconstruction intégrale vérifiée pour59paquets,
plan canonique inchangé, ordre/multiplicité/tableaux et valeurs distinctes conservés.
89tests ciblésPASS ; import runtime :39exigences en30lots, max27616/27648,
collision des rapports toujoursFAIL. Probe logiciel, pas qualité Qwen/autonomie.
Workers sans mission active rechargés78009, conversation préservée ; résolution
78015, mêmeplan11 remis enfile, sixincidents conservés. P4 NONREÇUE ; aucun
déploiement actif. [Preuves](docs/missions/26-P2/p4/REVUE-PLAN11-TRANSPORT-SANS-PERTE.json).

## P4 — revue plan10, déduplication par tâche — 29 octobre 2026

Incident77780–77783 : singleton29926/27648octets malgré déduplication des listes.
CorrectifCodex77786 : projections de tâches strictement identiques référencées
individuellement, textes historiques répétés référencés et JSON compact.
Plan complet, valeurs distinctes et39exigences conservés ; probe import runtime
22lots, max27565/27648, collision des rapports toujoursFAIL.54tests ciblésPASS.
Workers inactifs rechargés77787 après contrôles, conversation préservée.
Résolution77793, mêmeplan10 remis enfile, cinq incidents conservés.
Probe logiciel distinct de qualité revueQwen ; P4 NONREÇUE, aucun déploiement actif.
[Preuves](docs/missions/26-P2/p4/REVUE-PLAN10-DEDUPLICATION-PAR-TACHE.json).

## P4 — revue trop grosse : historique dédupliqué — 29 octobre 2026

Diagnostic77603/77605 : même une exigence seule dépassait le budget avec le
plan9 complet et les projections historiques répétées. CorrectifCodex77613 :
références explicites pour projections id/title/artifacts strictement identiques,
plan complet et historique distinct conservés ; seule cette fonction remplacée.
69tests ciblésPASS ; probe import runtime :39exigences en15lots, collision de
rapports toujoursFAIL. Aucun test de qualité réelle du reviewer déduit du probe.
Workers rechargés77614 après contrôle aucune mission running/queued/retrying,
aucun appel cible en cours ; conversation préservée. Résolution infrastructure
77617 et reprise77620 au mêmeplan9, quatre incidents historiques conservés.
Premier lot natif admis77636 :27150/27648octets, fenêtre32768 inchangée.
Réponses réelles Qwen observées77643/77650/77654 ; revue globale encore en
cours à ce relevé ; P4 NONREÇUE, aucun déploiement actif.
[Preuves](docs/missions/26-P2/p4/REVUE-HISTORIQUE-DEDUPLIQUEE.json).

## Surveillance des plantages et blocages — 29 octobre 2026

Contrôle de santé systemd installé toutes les60secondes, activé après reboot,
lié au même registre/moteur : workers, broker, conversation, JL03 et supervision.
RelevéHEALTH.json persistant, redémarrages natifs observés, état inconnu distingué
d’une panne ; pas de conclusion depuis une chargeGPU nulle. Escalade via le
coordinateur existant, compteursbornés conservés ; aucune commande rejouée par
le moniteur.21tests ciblésPASS et plantage contrôlé d’un serviceisolé (sortie42,
redémarrage natif1, processus différent) ; workersréels non interrompus.
Services sains au contrôle ; P4 a un blocageContextCapacityError distinct àtraiter.
[Preuves](docs/missions/26-P2/SURVEILLANCE-SANTE-PREUVES.json).

## P4 — adaptateur de rapport vérifié sur Qwen — 29 octobre 2026

Après refus de format, diagnostic77335 : le backend n’appliquait pas contains
pour imposer l’écrivain du rapport. Ce transport obligatoire est maintenant
ajouté mécaniquement par l’adaptateur Codex, limité au report_path ; les vrais
outils opérationnels restent choisis par Qwen. Erreurs de champs précises et
sorties originales refusées désormais archivées.177tests ciblésPASS ; essai
réel Qwen77347 conforme,23919/27648octets, aucune mutation pendant le contrôle.
Résolution77349, même checkpoint P4 repris, compteurs conservés. P4 etphase2
restent NONVALIDÉES, aucun artefact canari reçu à ce jalon.
[Preuves](docs/missions/26-P2/p4/ADAPTATEUR-RAPPORT-VERIFIE.json).

## P4 — contrats d’outils contrôlés avant reprise — 29 octobre 2026

Le plan historique retenait un rapport sans outil d’écriture et l’alias inexistant
host_exec#dell2. Garde installée77253 : Qwen doit corriger les déclarations des
tâches existantes avant exécution, avec vrais nomsAPI et écrivain du rapport.
Les chemins et critères existants sont préservés ; aucun plan rédigé par Codex.
Écriture centrale limitée au report_path77295, opérations applicatives surDell.
Le transport conditionnel JSON est corrigé pour les champs nommés title/type.
175tests ciblésPASS ; préflight77260 :24068/27648octets. P4 reprise au même
checkpoint, couverture77233 encoreFAIL : aucune réception P4/phase2.
[Déblocage](docs/missions/26-P2/p4/PREFLIGHT-OUTILS-REELS.json).

## Complément P3 reçu avec réserves ; P4 reprise — 29 octobre 2026

Réception indépendante77116 après clôture native JARVIS : CORE4+VAR2 passent
surDEUX Dell, reçus76710/76838/76888/76940 au même manifeste, contrôle77004.
Algorithme Qwen assisté, revue/application Codex après escalade ; historique conservé.
Fonction audit_plan intégrée dans la base canonique actuelle77115, rollback prévu,
125tests de régression et5tests sur import installé PASS, pas de somme avec suites
qui se recouvrent. API de réception par preuves réellement utilisée par JARVIS.
Bilan libre rectifié séparément77114 : autonomie éditoriale non reçue.
Même checkpoint P4 c32347de3edf4288a4751a3e65afa7eb remis enfile, préflight77123
16273/27648octets. Surveillance basculée surP4 ; P4 etphase2 restent NONVALIDÉES.
VF01 non transmis, ni14A ni24Old lancées.
[Réception et suite](docs/missions/26-P2/p3/RECEPTION-ADAPTATIVE-ET-REPRISE-P4.json).

## Continuité opérationnelle — directive propriétaire du 29 octobre 2026

Consigne permanente pour toutes les missions autorisées : en cas de blocage,
arrêter la stratégie infructueuse, diagnostiquer, corriger si nécessaire et
relancer depuis le checkpoint utile sans attendre une nouvelle sollicitation
humaine. La limite de trois échecs comparables reste obligatoire : elle arrête
une stratégie et déclenche son escalade, pas l’abandon silencieux de la mission.
Codex traite l’escalade, vérifie le changement technique et rend la main à
JARVIS ; les compteurs et preuves restent persistants. Ni redémarrage aveugle,
ni remise à zéro, ni quatrième tentative identique sous un autre nom.
Les travaux indépendants continuent. Une dépendance externe réellement absente
reste explicitement bloquée ; ne pas annoncer une activité inexistante.
Aucune nouvelle validation humaine pour les opérations déjà autorisées.

## P3 — candidat adaptatif et validation déléguée — 29 octobre 2026

Après escalade, proposition Qwen76621 revue/appliquée par Codex76636 surDell1.
Contrôle indépendant76653 : CORE4+VAR15000/18000 PASS ; ce ne sont pas des tests
JARVIS. Reprise76660 en tests seuls, même mission/plan/tâche. Trois échecs
qualifiés + deux classifications rectifiées conservés, problème correction
escaladé. JARVIS doit synchroniser et tester le même code sur les deuxDell.
P3 non reçue, P4 attend, aucun déploiement canonique ni VF01/14A/mémoire lancé.
[Preuves](docs/missions/26-P2/p3/REPRISE-ADAPTATIVE-ASSISTEE.json).

## P3 — probes déclarés exécutés, défaut confirmé — 29 octobre 2026

JARVIS a réellement choisi les probes déclarés : VAR FAIL76210/Dell2, correction
Qwen appliquée76325/Dell1, CORE PASS76377 sur ancienne versionDell2, VAR FAIL76477
sur version corrigéeDell1. Codex a vérifié les quatre reçus complets par SHA,
le test inchangé et le différentiel : le lot fixe2 reste présent ; les ajouts
après review_model ne peuvent prévenir son exception d’admission.
Trois échecs qualifiés + deux classifications rectifiées = historique5 conservé.
Diagnostic76597 et paquet de réparation76598 inscrits dans la même mission.
Arrêt maintenu après escalades76486/76594 : aucune quatrième tentative autonome,
aucun acquittement infrastructure. P3 NON REÇUE, P4 attend, VF01 non transmis.
[Preuves](docs/missions/26-P2/p3/DIAGNOSTIC-PROBES-76594.json).

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

## P4 — identifiants pérennes reçus dans le parcours natif

Le propriétaire autorise une correctionpérenne du blocage desclés. Mode authority_engine_operation_ids=true installé dans la missionP4 existante : authority_work/authority_edit ne reçoivent PLUS operation_id ; le moteur le lie àl’invocationSQLite réelle. Nouvellesmissionsdistribuées viaAPI activent cemode, anciennesmissions explicites legacy préservées. Qwen garde choix ducode/commandes/exécutants.130tests ciblésPASS,14nouveaux surchaqueDell, preuveJARVIS62931 : exécution62737 puis répétition descriptiondifférente réutilisée62774 sans doublecommande. Anciennesclés/compteurs préservés, résultat inconnu toujoursbloqué. Nepas proposer de noms de clés ni effacer les anciensrefus ; lire docs/missions/26-P2/p4/IDENTIFIANTS-DURABLES.md. L’ancien candidat59858 connu mais nonreçu est quarantinéBLOCKED comme supersédé62708, jamais reçu ni réinterprétécomme testPASS. Plan3 etmissiond8fe752876db480cbe5f22cd5525e2dd conservés. BibliothèqueCodeX reçue partiellement, instrumentationworker/suiteP4 encoreàdémontrer. Aucune fusionmain ni14A/24Old.

## P4 reprise depuis l’état persistant —27octobre2026

Audit natif terminé (cinq tâchesvalidées), réception indépendante limitée aux deux sources/artefacts avec réserve de prose :58952, dossier d’erreurs58945. P4 globale NON VALIDÉE. Nouveau paquet court réellement transmis àQwen80B : attestation du codePython chargé, candidat surlesdeuxDell, missiond8fe752876db480cbe5f22cd5525e2dd. Plan/fichiers/tests/répartition à choisir parQwen ; déploiement ultérieur après contrôle, sans nouvelle validationhumaine. Objectif de contexte32768 déjàpersisté avant transmission ; aucune repriseP2/P3. [Paquet](docs/missions/26-P2/p4/LANCEMENT-ATTESTATION.json) · [Reprise et réserves](docs/missions/26-P2/p4/REPRISE-MEMOIRE.md).

## Décision propriétaire du27octobre2026 — fenêtre avant transmission

Qwen80B Dell1 :32768tokens de contexte total après deux essais réels Codex (18876/26614tokens de prompt, VRAMlibremin1129/1163Mio). Réserver4096réponse+1024gabarit, entrée27648 avec contrôle conservateur explicitement distinct des tokens mesurés. Chaque sous-tâche doit porter cette fenêtre comme objectif de résultat dans son contrat avant transmission ; découper si trop gros, ne pas tronquer les exigences. Garde final du routeur et truncate=false ; pas de contournement par fallback. Compteurs préservés. Voir docs/missions/26-P2/p4/CONTEXTE-32768.md ; aucun succèsP4 ni autonomie déduit de ces testsCodex.

## Phase2 — réception P3 et lancement P4 du27octobre2026

P3 reçue **VALIDÉ AVEC RÉSERVES**, événement55310, continuation9e4a61d6faea4b73ad31251e72dcf7c1 completed ; lectures stériles/erreurs de rapports et correctionsCodex conservées. Lire docs/missions/26-P2/p3/RECEPTION-P3.json et ERRATA-RAPPORTS.md. P4 maintenant réellement lancée, premier audit natifd1b0d69639724c60b5bd1b2143b1a5fa ; lire M26_P2_P4_CODE_REEL.md. Le même timer de supervision cible P4-AUDIT, P2/P3 dans received_tasks, aucun rejeu. Copiesengine surDell ne sont pas l'application activeMac ; code disque/commit≠code chargé. Aucun déploiement dans ce premier audit ; suite P4 autorisée séquentiellement sans validation humaine. Autonomie complète sans guidage non reçue, ni14A/24Old/mainmerge. MANUAL-HOLD à retirer au retour au moteur.

## Ordre propriétaire du27octobre2026 — suite complète Phase2

Terminer P2 sur les chemins historiques concernés sans rejouer S01–S10, puis P3 contexte avec couches bleue/verte, puis P4 code réellement utilisé. Une priorité à la fois ; aucune validation humaine intermédiaire. Continuités natives P2-INTEGRATION b6d6cc3b05b94650acc5b26bfa2660d4 et P2-CANONICAL ad0b6c41dcde48dcb45829566336e494, liées au parent et même SQLite. Le test initial JARVIS incorrect est conservé/non reçu ; Codex a apporté les raccordements et oracles, JARVIS les utilise sur les Dell. Lire [état de reprise](docs/missions/26-P2/REPRISE-27-OCTOBRE.md). P3/P4 restent séquentielles, autorisées après réception précédente ; ne pas confondre cette autorisation avec une réception acquise. Définitions des couleurs non retrouvées dans les sources, clarification textuelle demandée. Préserver tous acquis, ni14A ni24-Old, aucune fusion main. MANUAL-HOLD actif pendant intervention interactive.

## M26-P2 — réception ciblée des dix scénarios

Dix scénarios reçus le26octobre2026 : VALIDÉ AVEC RÉSERVES dans le parcours natif opt-in. S09 a nécessité un contrôle Codex après trois vérifications infructueuses ; ne pas l’attribuer à une autocorrection JARVIS. Sources finales comparées Mac/deuxDell et11 nouveaux testsPASS sur chaque Dell. Ne pas rejouer les cas reçus, effacer compteurs ou conclure à une migration globale. La mission native reste en revue d’intégration ; ancienne liste de tâches non artificiellement clôturée. Registre superviseur `tasks` vide, réception classée dans `received_tasks`, donc aucune relance de ces tests négatifs. P3/P4 non transmises et14A distincte. [Rapport](docs/missions/26-P2/M26_P2_RAPPORT_FINAL.md).

## M26-P2 — relais de supervision installé

La supervision des escalades P2 réutilise le coordinateur périodique existant, avec unités dédiées `jarvis-m26-p2-supervision.*` et périmètre limité à la mission3aa717f3887e49daa7daf7e883ee52e4. Lire [son fonctionnement](docs/missions/26-P2/SUPERVISION-CODEX.md) avant intervention interactive. Vérifier un passage en cours et utiliser MANUAL-HOLD pour éviter une double intervention ; les passages périodiques détiennent déjà leur verrou et ne créent pas ce marqueur. Aucune réception P2/P3/P4 implicite ; compteurs préservés, trois passages comparables maximum. Les anciennes missions JL03 restent reçues et ne sont pas relancées.

## Mission26 Phase2 — lancement du26octobre2026

Mission M26-P2 lancée par le propriétaire : P2 boucles, puis P3 contexte, puis P4 code réel. Ne transmettre à JARVIS qu’une priorité à la fois, attendre réception avant suivante. Qwen80B décide et répartit les opérations réelles sur les deux Dell ; Codex audite, reçoit et traite les escalades. Conserver preuves et compteurs, ne pas reprendre automatiquement les correctifs Phase1 reçus. Pas de nouveau modèle ou chantier matériel, pas de fusion main. Nouvelle branche codex/mission-26-phase2-boucles-contexte-code-reel basée sur ba659f7/PR28. Les anciennes mentions Phase2 non lancée sont désormais historiques.

## Mission26 Phase1 — réception du26octobre2026

✅🟡 GO AVEC RÉSERVES pour la chaîne isolée Qwen80B/Dell1 → exécutants Dell1/Dell2. Mission native e26946bff84d4e06ad395b969ffcd72f completed, deux lots reçus, oracle Codex12/12 sur chaque Dell,35 tests logiciels. Ne pas relancer les correctifs reçus. Activation ciblée, mode assurance complet et bascule globale JL03 non qualifiés ; rapports libres encore fragiles, trois textes conservés avec errata. Conserver compteurs et origines Codex/JARVIS. [Réception](docs/missions/26-P1/RAPPORT-FINAL.md), [limites d’utilisation](docs/missions/26-P1/INSTALLATION-UTILISATION.md), PR28, aucune fusion main.14A et Phase2 restent distinctes, aucune autre mission lancée.

## Mission23D — réception numérique du20 octobre2026

✅🟡 **GO numérique avec réserves acoustiques, STT et d’autonomie.** Banc LiveKit et page temporaire réellement exécutés par JARVIS avec outils/corrections Codex. Six exécutions initiales conservées ; après correction du warmup AEC, trois interruptions mesurées à0,727 /0,559 /0,717s (seuil≤1s). Stop actif navigateur0,6ms, exports JSON/audio et contrôle d’annulation reçus. Le microphone/écho physique reste non testé ; une erreur de transcription du jour initial est documentée. [Réception finale23D](docs/missions/23D/RAPPORT-FINAL.md) · [Utilisation](docs/missions/23D/UTILISATION.md).

23D complète la même mission23, sans reset des douze validations ni création de mission moteur. Le NO-GO historique reste inchangé dans ses rapports ; son critère d’interruption numérique est désormais reçu par23D. Le périmètre global23, la route média distante et l’acoustique ne sont pas réceptionnés par procuration. Acquis du broker24 conservés. Publication sur `codex/mission-23d-interruption-livekit`, aucune fusion main. Les comptages historiques ci-dessous restent leurs instantanés datés.

## Mission24 — rétablissement du broker (décision du20 octobre2026)

✅ GO avec réserves de synthèse/autonomie : [rapport24](docs/missions/24/RAPPORT-FINAL.md), suite explicite de23C. Ancien confinement caractérisé, transport hôte rétabli ; correctifs23C et compléments24 déployés,80 tests réussis. JARVIS a exécuté et publié ses essais réels ; reprise après interruption/redémarrage et nouvelle session vérifiées. Les erreurs du premier rapport JARVIS sont conservées et corrigées par erratum prioritaire ; autonomie guidée, pas sans assistance. Autorisations propriétaire complètes conservées, aucune validation humaine intermédiaire. LiveKit23 reste NO-GO.

**Collision de numérotation :**24 est affecté au rétablissement du broker. Le chantier historique «24 — Mémoire enrichie» reste planifié, avec contenu et historique conservés ; réaffectation ultérieure nécessaire. Ne pas renuméroter les autres missions automatiquement. Les mentions antérieures réservant24 à la mémoire sont historiques.

# Barrière anti-régression des directives JARVIS

## Mission23C — ordre propriétaire du20 octobre2026

Suivi distinct `docs/missions/23C/`, branche `codex/mission-23c-broker-autonomie`. Codex coordonne/corrige les outils/vérifie ; JARVIS exécute prioritairement et reteste chaque capacité corrigée. Autorisations11/11B et23 conservées, sans validations humaines intermédiaires. Ne pas déduire une révocation d'un libellé historique11. Un refus de transport avant réponse ne démontre pas un refus de politique. Préserver IDs/checkpoints/mémoire/accès/services/PR11–13 ; aucune fusion main ni Dell2.23 reste NO-GO tant que l'interruption vocale n'est pas reçue ;24 reste Mémoire enrichie. État actuel23C partiel, aucun déploiement ni nouveau test JARVIS reçu ; lire son rapport avant reprise.

**OBLIGATOIRE avant toute rédaction de prompt Codex, instruction JARVIS ou reprise de mission :** lire [la charte fondamentale](docs/CHARTE_DIRECTIVES_JARVIS.md), puis le prompt d'exécution et le dernier état de la mission concernée. Ne jamais réintroduire des interdictions génériques contredisant une autorisation explicite récente du propriétaire.

**Mission 13D-E :** le propriétaire a déjà autorisé l'installation Debian 13 complète et autonome du Dell cible validé, dont la **destruction des partitions des deux NVMe identifiés**, le RAID1 mdadm, le redémarrage, le bootstrap SSH et Ansible. Le PXE UEFI IPv4 physique a été **réussi**. **Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire.** Cela comprend : lancement PXE à la demande de Codex, écriture et effacement déjà autorisés des disques identifiés, installation, reboot, bootstrap et Ansible. Aucun nouveau GO ne doit être ajouté artificiellement avant ou pendant cette exécution. En cas de divergence matérielle réelle ou d'impossibilité technique, arrêter la seule opération concernée et remonter le fait, sans inventer un nouveau processus d'approbation. Aucun benchmark NVMe. L'environnement est un laboratoire privé expérimental ; présenter les risques sans réécrire les décisions utilisateur.

Chaque nouveau prompt doit indiquer les documents relus, les autorisations conservées et les éventuelles contradictions corrigées. Ne pas interpréter une procédure historique plus restrictive comme annulant une décision récente.

---

# Politique de déploiement JARVIS

Décision explicite du propriétaire, 16 octobre 2026, à conserver pour les prochains déploiements. Ces directives remplacent les anciens prompts ChatGPT et consignes de mission contradictoires au même niveau utilisateur ; elles ne suppriment pas les vérifications techniques ni les instructions système applicables.

- Une demande explicite de déploiement complet autorise l'effacement des partitions, l'installation automatisée et le redémarrage sur les seuls disques du profil cible identifié et validé par les contrôles automatiques. Ne pas demander de confirmation à chaque commande de ce périmètre.
- Une demande de préparation ou de découverte seule n'autorise pas l'effacement. Une cible ou un disque inconnu ne devient pas autorisé par cette règle : découvrir, associer au profil et arrêter en cas d'ambiguïté.
- Conserver les contrôles UUID/DMI, séries, modèles et capacités exactes. Ne jamais sélectionner un disque par sa seule capacité ou par l'ordre de détection.
- Pour une demande explicite d’installation complète autonome, l’accord couvre les services temporaires nécessaires, l’effacement des seuls disques du profil validé, le reboot, le bootstrap SSH, l’accès permanent et le socle Ansible. La seule intervention physique normalement attendue est le lancement PXE. Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire. Enchaîner les opérations prévues ; n'arrêter qu'en cas de divergence de cible ou de blocage technique réel. Une demande limitée à la préparation/découverte conserve son périmètre limité. Les contrôles automatiques ne sont jamais supprimés.
- Ne jamais verrouiller le bootstrap avant preuve positive d'une nouvelle connexion indépendante par clé et validation de sudo. Aucun secret ni identifiant matériel unique dans Git.
- Préserver les services, comptes, clés, SSH/Tailscale et SQLite du Mac mini, le DHCP Bbox et les paramètres BIOS/VROC/VMD. Pas de benchmarks NVMe, de fusion automatique, ni de seconde RTX 3090 sans alimentation validée.
- Exécuter les opérations autorisées réellement et rapporter les résultats. Si une action physique reste indispensable faute d'accès distant, l'expliquer sans prétendre l'avoir réalisée.

Prompt de référence : [installation autonome](docs/missions/13D-E/PROMPT-INSTALLATION-AUTONOME.md). Cette règle exprime la demande du propriétaire ; elle ne permet pas d’effacer une cible inconnue ou de prétendre qu’un test a été réalisé.


## Directive de reprise — 17 octobre 2026

Tentative clôturée à la demande du propriétaire ; prochaine mission : finir l’installation en privilégiant la réparation de Debian et la conservation du RAID/partitionnement existants. Compte final imposé : **adminjarvis** ; mot de passe utilisateur conservé uniquement dans `deployment/13de/private/reprise-user-password.txt`, sans complexité supplémentaire imposée. Maintenir SSH par mot de passe jusqu’à validation indépendante par clé et sudo ; aucune suppression automatique du secours ensuite. Clavier français AZERTY à toutes les étapes. Suivi de toutes les tâches avec barres et coches de validation réelle. Ces directives remplacent les anciens noms de comptes et restrictions contradictoires. Lire `docs/missions/13D-E/RAPPORT-TRANSITOIRE-REPRISE.md` avant reprise. Ne pas relancer la mission pendant la clôture.


## Mission complète 13D-E / 14 relancée — 17 octobre 2026

Directive utilisateur actuelle : nouvelle installation Debian automatisée, conservation prioritaire GPT/RAID1/métadonnées/deux ESP, formatage rapide de la seule racine si compatible. Comptes jarvis-bootstrap et adminjarvis avec le même mot de passe imposé dans le fichier privé reprise-user-password.txt. Garder SSH par mot de passe pour adminjarvis même après validation indépendante par clé et sudo ; ne pas désactiver prématurément le bootstrap. Clavier français dans installateur/secours/consoles/système. Mission continue incluant Ansible, NVIDIA/CUDA, Ollama, Qwen/Ministral/Llama documentés, intégration conversation/voix/mémoire/outils et réception après reboot. Une RTX 3090 alimentée seulement. Aucune validation humaine intermédiaire ; email au propriétaire quand le PXE est réellement prêt. Les anciennes clôtures, reports IA, révocations automatiques et préférences de simple réparation sont remplacés dans ce périmètre. Aucun secret dans Git. Préserver services/accès/mémoire Mac mini et DHCP Bbox ; aucune fusion main.


## Mission 11 — habilitations agentiques persistantes — 17 octobre 2026

Le propriétaire autorise le raccordement de JARVIS/Qwen à Debian réel, aux installations, services, GitHub et mécanismes SSH/Tailscale/Ansible du laboratoire. Exécuter les opérations dans ce périmètre sans validations humaines intermédiaires. Les restrictions historiques « uniquement Bubblewrap /work » ne décrivent plus les outils hôte de mission 11 ; le laboratoire 13F reste facultatif. Les mécanismes système utilisent la politique propriétaire persistante, distincte des données et instructions conversationnelles. Une demande de capacité produite par Qwen n'étend jamais à elle seule l'autorisation. Codex traite les demandes du périmètre déjà accordé, puis JARVIS teste lui-même les droits avant validation. Préserver déploiement Dell 13D-E/14, accès Mac, mémoire, Bbox et Launcher V1. Aucune fusion automatique main. JL-02 doit être développé par JARVIS, pas réalisé par Codex dans la mission 11. Architecture et réception : [mission 11](docs/missions/11/ARCHITECTURE.md).


## Mission 11B — administration Dell permanente

Décision propriétaire du 17 octobre 2026 : le déploiement 13D-E/14 est réceptionné. Le profil historique `dell-observe` est désormais administrable via SSH et Ansible dans la politique root persistante `/etc/jarvis/host-policy.json`. Réutiliser les comptes, clés et hôtes épinglés ; aucune réinstallation Debian. Les anciennes restrictions temporaires de lecture seule du Dell sont remplacées dans ce périmètre. Les opérations IA accordées restent disponibles pour les prochaines missions autorisées ; une conversation ou une demande du modèle ne peut étendre seule cette politique. Conserver le contrôle DMI/NVMe, les journaux et les secrets hors du modèle et de Git. Reprendre 11B depuis son checkpoint, branche `jarvis/mission-11b-compute-expansion`, documentation `docs/missions/11B/`. Ne pas lancer JL-02. Aucun nouveau processus de validation humaine intermédiaire.


## JL-02 — lancement et livraison autorisés (17 octobre 2026)

Le propriétaire a explicitement lancé JL-02 : Codex coordonne et intègre, JARVIS exécute des tâches techniques réelles. Cette décision remplace les anciennes exclusions « ne pas lancer JL-02 » dans le seul périmètre JL-02 ; elle n’autorise aucune extension à une cible inconnue. Dépôt distinct `regisazzoun/JARVIS-Launcher2`, V1 inchangée. Réutiliser les identités, la passerelle, la mémoire et les outils existants, poursuivre sans validations humaines intermédiaires, conserver les preuves et l’attribution des contributions. Publication V2 autorisée ; aucune fusion automatique dans le dépôt principal. Un email de fin est demandé par le propriétaire.

## Mission 00 — pilotage documentaire, 17 octobre 2026

Le propriétaire a lancé `00-Mission-Pilotage-point-26-10-17`. Exécuter l’audit local/GitHub et les cinq lots réels JARVIS, puis consolider sur une branche dédiée, sans validation humaine intermédiaire ni fusion dans main. Cette décision remplace le report historique de l’audit. Lire les sources et écrire les livrables documentaires en préservant les originaux, secrets et services.

Aucun déploiement, rétablissement du RAID ou installation du Dell n°2 dans ce périmètre. **13D-E = Dell n°1 installé par Codex et réceptionné ; 14 = Dell n°2 à déployer par JARVIS ; 14A = capacité agentique distincte, sans validation globale automatique par la mission 00.** Conserver les périmètres distincts de 11 historique, 11-Agentic, 11B, JL-01 et JL-02. Les décisions récentes prévalent ; les textes anciens restent historiques. Registre et preuves : `docs/missions/00-Mission-Pilotage-point-26-10-17/`.

Réception documentaire 00 : GO avec réserves, cinq tâches JARVIS réellement exécutées avec guidage et corrections Codex. Les règles inventées dans les sorties modèle n’ont aucune autorité. Le [rapport final](docs/missions/00-Mission-Pilotage-point-26-10-17/RAPPORT-FINAL.md) et le registre précisent les résultats ; conserver les autorisations récentes et la séparation 13D-E / 14A / 14.

## Publication documentaire dans main — autorisation du 18 octobre 2026

Le propriétaire demande explicitement : « Alors fusionne je veux quelque chose de coherent », avec README réécrit et SUIVI à jour. La fusion des livrables documentaires 00 et du correctif de concordance est maintenant autorisée, y compris leur intégration dans main. Cette décision remplace les consignes antérieures de non-fusion pour cette publication précise. La PR6 documentaire peut être fusionnée dans sa branche de base ; une intégration documentaire dédiée publie le résultat dans main sans importer les changements de déploiement de la PR5. Aucun déploiement matériel ou changement des services n’est déclenché. Les règles de fusion des autres missions ne sont pas étendues implicitement.


## Mission 22 — finalisation autorisée, 18 octobre 2026

Poursuivre sur `codex/mission-22-agentic-engine-v2`, PR8, sans fusion dans main ni déploiement Dell2. Conserver les tâches21 déjà reçues ; JARVIS reste leur exécutant réel. Codex corrige le moteur, raccorde les capacités et vérifie indépendamment. Le propriétaire inclut désormais explicitement l’installation et l’enrôlement du client Tailscale propre au Dell1 : une passerelle Mac ne remplace pas cette correction. Aucune copie d’identité Tailscale ou exposition de secrets au modèle. Une absence réelle d’authentification d’enrôlement doit être documentée comme dépendance externe, sans réception fictive ni nouveau GO de mission. Préserver services, mémoire canonique, ressources disponibles et accès existants.

## Reprise finale22 —19 octobre2026

Le propriétaire confirme `jarvis-dell` enrôlé dans Tailscale et KDE/VNC utilisé depuis son Mac via tunnel SSH sur le tailnet. Ce témoignage utilisateur est distinct des nouvelles preuves du modèle. Reprendre la mission persistante `e370b0bef74f4deaa390b5c46bfdc299`, sans créer de mission ni recommencer les six tâches reçues. JARVIS vérifie lui-même Tailscale, SSH direct et RFB/image, clôture07 et publie ses rapports ; Codex vérifie et consolide22. Aucune validation intermédiaire, aucune fusion main, acquis/services/identités préservés.

## Mission23 — correctif agentique autorisé,19 octobre2026

Le propriétaire confie à Codex le diagnostic et la correction des limitations constatées pendant le développement LiveKit. JARVIS conserve le développement principal, l’exécution persistante originale et les quatre tâches reçues. Codex peut corriger moteur, outils, habilitations déjà autorisées et environnement, puis vérifier une progression réelle, sans écrire l’application à sa place. Aucun reset, nouvelle mission, plafond arbitraire ou validation humaine intermédiaire. Préserver voix/mémoire/accès/services, aucun Dell2 ni fusion main. Source de plan : CYCLE-23-31 et PR9 ; LiveKit=23, JL-03=27. Les anciens états «planifié» ne révoquent pas le lancement explicite actuel.


## Mission23 — finalisation et capacités durables,20 octobre2026

Le propriétaire autorise Codex à coordonner la finalisation de l'exécution originale7971ec0311124fb4be9e3125dcb291fd, réparer/développer les outils GitHub et le routage conversationnel, déployer puis faire retester par JARVIS, exécutant principal. Aucune validation humaine intermédiaire ; conserver les onze validations historiques, preuves, commits et mémoire. Compléter les tests manquants par addenda et recevoir sur preuves. Diagnostic df542051560b44b3851124b09d8319c2 lié23, jamais mission24 mémoire. Publication sur branches dédiées des dépôts propriétaire concernés, secrets hors Git/modèle, aucune fusion main ni Dell2. Sources et méthode : docs/missions/23/finalisation/SOURCES-ET-AUTORISATIONS.md.


## Convention permanente de présentation des statuts — décision du propriétaire du 19 octobre 2026

Dans les tableaux de pilotage (README, SUIVI, interfaces de suivi dont JL-02), utiliser les pictogrammes suivants, sans modifier le résultat technique documenté :

- **✅ GO / réalisée / validée** : objectif de la mission ou de l'étape atteint et vérifié dans son périmètre.
- **✅🟡 GO partiel / GO avec réserves / résultat réalisé avec réserves non bloquantes** : acquis réellement démontré et exploitable, mais périmètre restant ou réserve explicite. Conserver le texte historique « GO PARTIEL », « GO AVEC RÉSERVES » et les limites dans les colonnes explicatives.
- **🟡 En cours / incomplet / preuve insuffisante** : objectif global non encore atteint, ou résultat seulement préparé, non testé, incertain ; ne pas lui attribuer une coche de réussite.
- **📋 Planifiée** : pas encore exécutée.
- **❌ NO-GO / échec** : l'objectif testé a effectivement échoué ; conserver les faits et les limites.

Une étude ou un diagnostic effectivement terminé peut porter ✅ si son objectif se limitait à l'étude ou au diagnostic, même si la technologie étudiée reçoit un NO-GO : préciser cette distinction. **Ne pas qualifier de ✅🟡 un échec avéré, une installation non testée, une preuve absente, ni une mission simplement en cours.** Les rapports historiques et les preuves restent inchangés. Cette convention de présentation s'applique également aux futurs rapports, missions et tableaux ; elle ne déclenche pas de nouveaux tests ou validations.


### Règle de consolidation des réserves historiques — décision du propriétaire du 19 octobre 2026

Lorsqu'une mission postérieure démontre par un rapport et des preuves le critère resté ouvert d'une mission antérieure, afficher dans le tableau de pilotage **✅ GO — Réserves historiques levées par mission XX**, avec référence explicite aux missions ultérieures. Le rapport d'origine, son statut à sa date et les éventuelles limites hors critères couverts restent inchangés. Ne jamais inventer de test rétroactif, ni étendre une preuve à un autre matériel ou à un autre objectif. Si une réserve essentielle reste réellement ouverte, conserver **✅🟡** ou **🟡**, suivant les faits.

## Mission25 — MCP et Skill Lab lancée le21 octobre2026

Le propriétaire autorise l'exécution complète sans validation intermédiaire. Codex coordonne, développe l'infrastructure manquante et vérifie ; JARVIS reste l'opérateur observable des essais, de la création/correction d'un skill et de sa seconde utilisation. Ne pas réattribuer à JARVIS les corrections Codex. Exécution persistante `4612213a05624836abec58385813439c`, branche `codex/mission-25-skill-lab`, [dossier25](docs/missions/25/MISSION.md). Ne pas recréer cette exécution ni les tâches déjà reçues.

Acquis24 broker préservés ; ne pas refaire leur réception. Le prototype vocal23D est reçu par le propriétaire, mais son raccordement complet aux outils/mémoire est distinct et non réalisé par procuration. «24-Old Mémoire enrichie» reste planifiée après25. Aucun Dell2, réinstallation/RAID/partition, secret publié ou fusion main.14A n'est reçue que sur critères et preuves réels, avec bilan séparé.


## Mission26 — réception et fonctionnement durable —21 octobre2026

Mission26 lancée et reçue ✅🟡 avec réserves : [rapport](docs/missions/26/RAPPORT-FINAL.md),3/3 tâches JARVIS, trois plans versionnés et105 tests logiciels. Les nouveaux objectifs sans tâches prédéfinies soumis à l’API/promus du chat utilisent le mode autonome à vérification sémantique par défaut ; les missions et contrats historiques gardent leur état. Codex développe l’infrastructure et vérifie ; JARVIS propose ses plans et exécute/corrige réellement ses opérations. Ne pas attribuer les interfaces Codex au modèle, ni le programme créé/corrigé par JARVIS à Codex. Conserver rapports bruts et errata, événements, versions, droits et services. L’épreuve finale14A reste distincte et différée ;14A demeure ouverte,24-Old et Dell2 non lancés. Aucune validation humaine intermédiaire ajoutée ni fusion main.


## Mission26B — ordre propriétaire du22 octobre2026

Continuation ciblée26 autorisée sans validation intermédiaire : contrôle automatique de couverture et validation de la prose à partir des preuves, puis scénarios réels JARVIS et vérification indépendante Codex. Préserver les résultats26 ; ne pas attribuer les correctifs moteur au modèle. Conserver tous les essais et rectifications. Ordre actuel26B → épreuve finale14A distincte →24-Old →27 JL-03. Aucun lancement14A/24-Old/Dell2 ni fusion main. [Cahier26B](docs/missions/26B/MISSION.md).


## Clôture26B — décision propriétaire du23 octobre2026

Le propriétaire demande « cloture la mission en l etat ».26B est clôturée **🟡 incomplet**, sans réception fictive des trois rapports, sans levée définitive des réserves26 ni clôture14A. Les trois essais sont interrompus, états et preuves conservés ; aucune reprise automatique26B. Les capacités installées restent disponibles. TTS-01 est une demande distincte à reprendre depuis ses preuves existantes. [Bilan26B](docs/missions/26B/RAPPORT-FINAL.md).


## TTS-01 — reprise autorisée du23 octobre2026

Codex orchestre et corrige l’infrastructure ; JARVIS exécute inventaire, choix/installation TTS, génération, mesures et restitution via JL-02. Reprendre la mission existante8bd3e5b316a94021b5183e0db26d6efc, sans nouvelle installation en double ni validation humaine intermédiaire. Les anciens appels généraux à validation ne prévalent plus dans ce périmètre. Préserver Dell1/services/Piper ; références de film privées réservées à l’écoute comparative, aucun clonage de Philippe Faure. La planification dirigée/les contrats corrigés par Codex ne sont pas attribués au modèle.26B reste clôturée incomplète,14A/24-Old/Dell2 non lancés. [Ordre et périmètre](docs/missions/TTS-01/MISSION.md).


## Mission13 — complément double GPU,23 octobre2026

Codex coordonne et vérifie ; JARVIS exécute via les droits11B persistants, sans validation humaine intermédiaire. DeuxRTX3090 DellOEM détectées et petits calculs reçus ; alimentation non qualifiée, essais de charge différés. Aucune réinstallation, aucun branchement improvisé ni nouveau pilote. TTS-01 suspendue ;26B clôturée incomplète,14A/24-Old/28/Dell2 non lancés. [Réception13](docs/missions/13-extension-gpu/RAPPORT-FINAL.md).


## Mission28A — exécution propriétaire du23 octobre2026

28A est lancée, sans validation humaine intermédiaire. Conserver Qwen27B local conversation sur Mac mini, routage vers modèle Dell pour missions et réserve de capacité interactive. Les câbles doubleGPU sont reçus fonctionnels par décision propriétaire ; ne pas rouvrir le pinout comme condition générale. Profil700W limité à des pointes expérimentales :699,37W mesurés en essai court, pas certification de tenue. Codex développe et vérifie, JARVIS exécute/réutilise ; corriger les interfaces sans lui attribuer le code Codex. Branche `codex/mission-28a-routage-modeles`, même moteur/mémoire/checkpoints, aucun lancement14A/24-Old/TTS/Dell2 ni fusion main. [Architecture en cours](docs/missions/28A/ARCHITECTURE-HYBRIDE.md).


## Mission28A — clôture propriétaire du24 octobre2026

Le propriétaire demande la clôture en l’état et retient `qwen3-coder-next:q4_K_M` (80B) pour les missions Dell1, choix déjà effectif. Conserver `qwen3.5:27b-q4_K_M` pour la conversation sur Mac.28A est **🟡 clôturée incomplète** : infrastructure acquise, réception agentique/programme/rapports non entièrement reçue. Interrompre les deux essais persistants et leurs publications erronées, conserver toutes les preuves et validations ; aucun nouveau test ni reprise automatique. Les tests seront relancés ultérieurement sur instruction distincte. Ne pas clôturer14A ni lancer24-Old/TTS-01/Dell2. Codex publie la clôture sur la branche de mission et la PR25, sans fusion main. [Rapport28A](docs/missions/28A/RAPPORT-FINAL.md).


## TTS-01 — nouvelle reprise propriétaire du24 octobre2026

Le propriétaire relance intégralement TTS-01 après la clôture28A. Réutiliser la mission8bd3e5b316a94021b5183e0db26d6efc, les deux tâches reçues, le venv TTS et les archives privées. JARVIS exécute avec le80B Dell désormais retenu ; Codex coordonne, corrige l’infrastructure et vérifie. Autorisation autonome complète sans validation intermédiaire, sans réinstallation du système. La libération temporaire de résidence Ollama pour une fenêtre GPU TTS ne remplace pas le modèle par défaut et n’arrête pas le service. Conserver27B conversation Mac/Piper/LiveKit/JL-01/JL-02 ; aucun clonage de Philippe Faure ni publication des films.28A et26B restent clôturées incomplètes ;14A/24-Old/Dell2 non lancés. [Reprise TTS](docs/missions/TTS-01/REPRISE-2026-10-24.md).


## TTS-01 — réception du24 octobre2026

✅🟡 GO avec réserves : trois WAV français Qwen1.7B/Uncle_Fu générés et transférés par JARVIS, contrôles indépendants Codex (signal,transcription,API,lecture).246tests logiciels. Réception finale opérateur Codex explicite, autonomie sans assistance non validée, prose rectifiée et originaux conservés. Piper/27BMac/80BDell/services maintenus ; aucune fusion main ni clôture14A/26B, aucun14A/24-Old/Dell2 déclenché. Les anciens états «suspendue/aucune voix» TTS sont historiques. [Rapport](docs/missions/TTS-01/RAPPORT_TTS_01.md).


## Mission27 JL-03 — lancement propriétaire24octobre2026

JL03 est lancée : Codex coordonne et vérifie, JARVIS développe/exécute effectivement. NouvelleV3 indépendante, dépôtLauncher3 et service/port séparés, JL01/JL02 préservés. Pas de validation humaine intermédiaire ; règle3échecs par même blocage puis arrêt/analyse et changement réel, sans remise à zéro artificielle. L’ordre explicite27 courant remplace son report historique après14A/24Old ; ces missions ne sont pas lancées. Sources/prototype/tests/provenance réels requis ; pas de réception autonome sur prose seule. Aucun main fusionné automatiquement.


## Mission14B — ordre propriétaire courant

Le propriétaire lance l'installation et l'intégration duDell2avec Debian13, deuxRTX3090si alimentation correctement raccordée, procédures validées réutilisées. JARVIS exécute, documente causes/tentatives/corrections/résultats ; trois échecs comparables maximum puis arrêt/diagnostic/sous-mission corrective si utile. Codex intervient seulement pour capacité manquante réellement démontrée et rend aussitôt la main ; demande prête si assistance indisponible, autres tâches indépendantes continuées. Aucun changementOllama, modèles/services d'inférence, routage, quotas ou répartition des charges ; aucune autre modification d'architecture. Les anciennes exclusionsDell2sont remplacées seulement dans14B.14Aet24-Oldnon lancées ; identités de cible séparées duDell1. [Ordre14B](docs/missions/14B/MISSION.md).


## Précision propriétaire — sortie de boucle et appel àCodex

Après trois échecs comparables, arrêter immédiatement la stratégie en cours. Examiner les erreurs et reçus, formuler la cause probable et chercher une solution techniquement différente. Documenter ce qui change avant de reprendre. Cette nouvelle approche reste limitée à trois échecs comparables ; aucune quatrième répétition ni simple renommage ne remet les compteurs à zéro.

Si la recherche et les corrections bornées ne permettent pas de résoudre le blocage, demander explicitement l'intervention deCodex avec un dossier succinct : objectif bloqué, cause observée, approches et tentatives, erreurs exactes/références, correction envisagée et aide attendue. L'appel est désormais permis aussi pour un blocage persistant, pas seulement pour une capacité manquante. Ne pas poursuivre seul une boucle sans progrès. Si l'outil de demande n'est pas disponible dans la phase courante, conserver la demande prête dans mission_note et le journal pour transmission ; ne pas inventer une demande enregistrée.

Si l'assistance est indisponible, conserver ce dossier et continuer les tâches indépendantes réalisables. Codex intervient ponctuellement puis rend la main. Les interdictionsOllama/routage/répartition/autres changements d'architecture restent strictement inchangées.

## JL03-COR-P1 — capture acceptée et continuité propriétaire

Le25octobre, le propriétaire accepte la capture mais conserve une réserve de transcription ; le contexte manquant reste une hypothèse, mémoire à traiter plus tard. D03/D04 continuent réellement en contextes distincts, D17 est préparée pour prendre la place libre automatiquement via le moteur existant. Maximum deux contextes, aucune attente de validation humaine entre corrections. Un blocage après trois échecs est documenté/escaladé, ses compteurs préservés ; continuer les autres travaux indépendants sans réessai aveugle. Codex revoit les preuves et intègre lesdiffs successivement, sans réception fictive ni fusionmain.

## JL03-COR-P1 — supervision persistante demandée

Le propriétaire demande explicitement de débloquer et surveiller sans devoir relancerCodex. CoordinationCodex périodique autorisée dans le seul périmètreD03/D04/D17 ; JARVIS continue les opérations réelles surDell. Aucune validationintermédiaire ajoutée. Maximumdeux contextesJARVIS, gardestroiséchecs et compteurspréservés. Un passageCodexdiagnostique/corrige/contrôle et rendlamain ; aucunloopaveugle, aucune missionhorspérimètre, aucune fusionmain. Les sortiesCLI et secretsrestentprivés, publieruniquement faits/preuves/attributions.

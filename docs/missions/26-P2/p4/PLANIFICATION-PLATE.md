# Reprise P4 : interface plate de planification

Codex installe571956d après l’escalade65965, sans réinitialiser les refus.
La mission e98fd4bbe37c492b922db9b5a1d782aa et ses preuves restent inchangées.
Le paquet de coordination a été révisé65937 pour retirer une lecture déjà
réalisée, source de répétition ; l’ancien objectif reste dans l’événement.
Aucun objectif de préparation ni interdiction de déploiement n’est retiré.

## Adaptation

`mission_plan_report_step` reçoit une étape à paramètres plats. JARVIS choisit
id, titre, objectif, dépendances, outils, observations, vérification, reprise,
artefacts et report_path. Au premier appel il choisit aussi les métadonnées
globales. L’adaptateur fournit seulement la forme du contrat : le choix de cet
outil demande une vérification de rapport avec lecture réelle de report_path
et contrôle des affirmations contre les preuves, jamais une simple existence.
Il ne choisit aucune étape ou commande à la place du modèle.

Le même Registry appelle le même mission_plan, le même MissionStore et les
mêmes contrôles de couverture et de prose. Une étape ajoutée ne permet pas
l’exécution si des exigences manquent. La version courante est contrôlée ; les
tâches reçues restent immuables. Aucun second moteur ni stockage opérationnel.
L’interface est masquée et refusée si planning_report_steps n’est pas activé.
Elle sert à la préparation par rapports ; elle ne reçoit pas un déploiement
sur la seule prose. Les critères techniques d’intégration restent à prouver.

La phase de planification utilise l’identité complète et l’objectif complet,
avec les instructions de cette interface actuelle. Les descriptions de
l’ancienne interface imbriquée ne sont plus injectées dans cette phase ; les
instructions d’exécution ordinaires reviennent pour les tâches. Les contrats
canoniques et autorisations restent applicables, la fenêtre32768 n’augmente pas.

## Tests et limites

Trois tests Registry/SQLite réels vérifient la conservation des valeurs du
modèle, le prédicat de lecture du rapport, l’absence de réception sur seule
sauvegarde, l’ajout avec dépendance, le rejet d’une version ancienne, la
protection d’une tâche reçue et le refus hors activation. Six tests de portée
et cycle passent aussi. Ce sont des tests logiciels Codex, pas une preuve
d’autonomie ; l’utilisation effective parQwen est encore à contrôler.

Installation65968, sauvegardes privées des modules tools/durable_tools et du
cycle. Retour arrière : restaurer ces fichiers et désactiver l’option de la
mission, puis recharger uniquement les workers. Les copies candidates reçues
surDell ne sont pas modifiées. Aucun attester applicatif n’est installé ici.

## Utilisation réelle et non-régression

Qwen a utilisé l’adaptateur : première étape65982, contrôle de couverture65987
insuffisant, reçu d’interface65988 ; deuxième étape sauvegardée puis couverture
66014, reçu66015. Aucune tâche fournie parCodex ; le modèle révise son plan selon
les lacunes. Les versions sont persistantes et ne valent ni exécution ni
réception. Le premier contrôle conserve une incohérence locale d’explication
(booléen covered=true alors que la phrase dit non couvert) : statut global
insuffisant, pas une preuve de couverture totale. Revue indépendante nécessaire.

Les80tests existants de mission_engine26b passent après l’adaptateur, en plus
des3nouveaux tests et6de portée. Les trois essais assistés précédents restent
non reçus ; le nouvel adaptateur est un changement technique réel, pas leur
quatrième réexécution. Les copiesDell et l’attestation candidate ne sont pas
modifiées pendant cette reprise.

Le superviseur comptait uniquement les événementsAuthority comme progrès utile,
alors que cette unité utilise le moteur normal. Option normal_engine_progress
réutilise last_progress déjà classé par le worker : plans et observations utiles,
pas heartbeats ni simple polling mission_progress. Quatre tests du coordinateur
passent, dont la vérification avec SQLite d’une mission ancienne mais qui avance
et la conservation de la limite3passages après perte du cache. Aucun compteur
périodique effacé. Les deux anciens passages CLI en limite de compte restent
conservés, sans garantie implicite de disponibilité permanente de Codex.

## Plan3 et passage à l’exécution

Troisième étape sauvegardée avant sa revue ; la revue demandait8192tokens de
réponse alors que le routeur utilise déjà4096. Core applique désormais le même
profil avant admission : aucune augmentation de fenêtre ni réduction des preuves.
Rejeu du vrai payload66045 :26090octets/27648, tous champs conservés, préflight
66079. Les39tests de contexte passent. Si une revue est indisponible après la
sauvegarde, le retour conserve explicitement la version déjà enregistrée et
execution_allowed=false ; il n'invite plus à refaire la mutation. Un test réel
Registry/SQLite de ce cas porte la suite d'adaptateur à4cas.

La revue du plan3 passe66089. Cela ne reçoit pas les opérations ni les rapports.
Au passage vers la tâche active, les instructions et le schéma imbriqué obsolète
restaient exposés en double et provoquaient un nouveau dépassement66094.
Incident d’infrastructure4 enregistré, zéro échec fonctionnel ; rien effacé.
Projection d’interface actuelle1a60ca3 installée66105 : identité complète,
objectif complet et critères stockés inchangés ; retrait de l’ancien schéma
mission_plan de la vue modèle dans ce mode, appel interne canonique maintenu.
Préflight22425octets/27648. Cinquième test de l’adaptateur fait passer un vrai
DurableCycle et vérifie l’identité, l’objectif et le prédicat conservés.

JARVIS reprend version0-plan en état running. Contrôles réels du budget66138/
66147 :25236puis25473octets/27648 après compaction du contexte archivé ; aucune
hausse de la fenêtre. Le modèle a consulté les faits et la politique ; ces
lectures ne prouvent aucun service attesté. Le contrôle indépendant des rapports
et les observations systemd restent à réaliser. Codex a rappelé le mécanisme
de découverte existant de host_write_file pour écrire le rapport de la tâche,
sans le rédiger à sa place. Aucune réception globale ni autonomie sans assistance.

Core a été mis à jour sur disque pour harmoniser l’admission, et rechargé dans
les workers. Le service conversation n’a pas été redémarré pour cette correction.
Les copiesDell candidates restent à leur version reçue antérieure ; ne jamais
confondre leur ancien manifeste avec celui du SDK actuel ni en déduire le code
chargé du service conversation. La future réception d’intégration devra comparer
les versions effectivement concernées.

## Lecture systemd classée à tort en mutation, puis retest réel

277e05e corrige `host_service show` dans le Registry, le suivi des effets du
cycle et la réception des rapports. Onze tests du garde canonique passent,
dont une observation show autorisée pendant qu’une véritable mutation inconnue
reste protégée ; restart reste bloqué. Aucun garde de mutation n’est affaibli.

L’ancienne lecture30a1c76e987543c9a2a9eb730d2585cb avait réellement fini rc0,
mais était liée à la vérification du rapport futur encore absent. Son résultat
historique INSUFFICIENT est conservé, jamais reçu comme PASS. Liaison retirée du
flux de mutations sous état historique BLOCKED, unknown_outcome=0 conservé,
sans effacement ni nouvelle interprétation des compteurs. Contrôle indépendant
Codex66249 : les deux services actifs, show réel rc0 sur chacun, zéro nouvelle
tentative de mutation. Voir SYSTEMD-SHOW-RECEPTION.json ; aucune attestation
mémoire n’en est déduite.

Un passage périodique66241 a commencé pendant la reprise interactive. Codex
l’a arrêté avant installation pour sérialiser les changements, événement dédié
conservé, tentative1 non effacée. MANUAL-HOLD protège ensuite l’installation ;
les anciens logs, limites de compte et compteurs restent dans le dossier privé.

JARVIS a ensuite repris des lectures natives réussies des deux vrais fichiers
d’unité systemd. Voir REPRISE-EXECUTION-NATIVE.json pour identifiants, reçus broker
et modèle réellement observé. Ces actions sont distinctes du contrôle indépendant
Codex, et ne sont pas une preuve de clôture de la préparation ou de touteP4.
Le schéma host_write_file nécessaire à son rapport a été exposé par Codex via
la découverte existante66286 ; aucune écriture du contenu réalisée parCodex.

## Passage périodique après les trois relectures refusées66347

Passage1 démarré66349, aucune intervention Codex parallèle ni MANUAL-HOLD.
Les lectures natives66291/66335 et show66330 existaient ; trois répétitions
ont déclenché le garde. Le cycle avait chargé ses découvertes avant66286 :
son archive66338 omettait encore host_write_file. Codex archive le contexte
périmé66352, sans toucher aux tâches, au plan3 ni aux compteurs.

Le nouveau cycle expose réellement host_write_file dans66357. Il rencontre
ensuite la borne de contexte66359 avant toute inférence : incident5 conservé,
zéro échec fonctionnel déduit. Codex conserve les observations complètes66350
et remplace ses seuls rappels courants par des références compactes66367/66368,
avec instruction66369. Le préflight du vrai payload passe à26985octets/27648,
fenêtre32768 inchangée, outil d’écriture présent. Pas de modification logicielle
ni redémarrage de service dans ce passage. Les archives et refus restent intacts.

La remise en file rend la rédaction et les choix àQwen ; elle ne reçoit aucun
rapport. Le rapport de plan, la préparation et P4 restent à vérifier. La projection
des preuves natives dans le champ observed_evidence (actuellement Authority)
reste une limite identifiée ; aucune autonomie sans assistance n’est déduite.

Le garde persistant a encore bloqué la remise en file66376 : son incident
de capacité n’était pas marqué résolu. Après le préflight réel66373, Codex
marque uniquement ce problème RESOLVED66378 ; infra_incidents=5, failed_cycles,
escalation_event et tous les refus restent inchangés. Nouvelle remise en file
66379 ; aucune quatrième exécution de lecture n’est autorisée par ce changement.

## Passage périodique2 : diagnostic compact, compteurs conservés

Le passage2 démarre66423, sans Codex parallèle ni MANUAL-HOLD. Le cycle17
avait réellement observé le rapport absent66410 et sa vérification
INSUFFICIENT66411 ; aucune rédaction ni réception n'en est déduite.
L'incident de capacité6 reste conservé : la projection finale dépassait la
borne de208octets, notamment à cause de la trace Python historique répétée.

Correction infrastructure Codex : uniquement en dernier recours de compaction,
projeter la dernière ligne de l'erreur et la référence de son invocation.
Le reçu intégral, les objectifs, contrats, schémas et compteurs restent intacts.
40tests de contexte passent, dont une admission serrée avec conservation du
prédicat exact et de l'erreur originale. Préflight66430 :27316/27648octets ;
après instruction courte66431, préflight66435 :27216/27648.

Aucune mission running ni appel en attente avant rechargement des deux workers.
La tentative systemctl sans sudo a été refusée par l'authentification locale ;
sudo non interactif a effectivement rechargé les workers (PID298586/298588).
Cela ne constitue pas une attestation mémoire du candidat applicatif.
Seul le problème de capacité est marqué RESOLVED66436 sur preuve66435,
infra_incidents=6 et failed_cycles=0 conservés, autres refus inchangés.
Contexte précédent archivé66437 ; remise en file66438, cycle18 réellement
commencé66439 et admission native66444 à27455/27648octets, fenêtre32768.
Le modèle garde la rédaction du rapport, ses décisions et la suite du plan3.
Aucun attester applicatif déployé, aucune préparation ni P4 reçue ici.

## Passage périodique : faits déjà consultés, refus66513

Le passage1 de cette cause démarre66515. La mission est interrupted, sans
appel outil en cours. Les trois refus comparables de mission_report_facts
sont conservés ; le reçu réussi ef0f4ae3438d4c41b7a2e2911efa9a61 existe déjà.
Les deux fichiers d'unité et les observations show natives ont aussi réussi.
Le contexte courant présentait surtout la dernière sortie show volumineuse.

Codex projette66516 des extraits référencés de quatre vrais reçus natifs,
sans refaire de lecture système ni écrire le rapport du modèle. Le rappel
corrige explicitement la relecture des faits déjà reçus ; les attributions et
limites restent exigées. Préflight hors inférence66520 du dernier payload réel
avec cette projection :27377/27648octets, host_write_file présent. Ce rejeu de
projection ne garantit pas à lui seul l'admission du prochain contexte reconstruit.
Ancien dialogue archivé66521, remise en file66522 ; même plan3, tâches,
originaux, compteurs et fenêtre32768. Aucun changement logiciel, redémarrage,
attester applicatif ou réception de préparation/P4 dans cette intervention.
La rédaction et les choix techniques restent àQwen ; aucune autonomie sans
aide n'est déduite de cette correction de contexte Codex.

Confirmation native : cycle19 commencé66523, admission réelle66528 à
27377/27648octets après compaction, capacité32768 observée via api/ps.
L'inférence utile est laissée finir ; admission ne vaut pas rapport reçu.

### Résultat du cycle19 : reprise arrêtée, préparation non reçue

L'admission66528 a bien été suivie d'une inférence réelle66529 :8160tokens
de prompt mesurés. Qwen a choisi mission_verify active:0 avant rédaction.
Lecture66534 : fichier toujours absent ; verdict66535 INSUFFICIENT conservé.
Le tour suivant est refusé avant inférence66542 (payload28647octets avant
compaction, borne27648). Incident de capacité7 conservé66543/66544, aucun
échec fonctionnel déduit. État final interrupted66546, sans appel en attente.
La projection66516 n'a donc pas suffi à obtenir la rédaction. Pas de nouvelle
relance inchangée : les compteurs, le problème de capacité escaladé et les deux
refus mission_verify restent intacts. Prochaine correction à examiner : budget
de la projection après verdict de rapport absent, puis écriture réelle parQwen
avant toute nouvelle vérification. Aucun rapport, préparation ou P4 reçu.

## Passage2 après incident7 : compteurs projetés sans répétition des clés

Le passage66548 constate zéro mission running et zéro appel commencé en attente.
La dernière projection conservait17compteurs d'interface avec les mêmes clés
JSON répétées. Codex compacte ce seul format en dictionnaire empreinte→compteur,
en dernier recours d'admission ; toutes les valeurs restent présentes et les
liaisons epoch/catégorie restent dans le checkpoint référencé. Aucun garde,
objectif, contrat ou compteur n'est retiré.41tests de contexte passent, dont
un nouveau cas conservant les17compteurs et le checkpoint complet.

Sauvegarde privée du module installé, rechargement des seuls deux workers
sans opération active ; aucun attester applicatif installé. Instruction66549,
préflight66553 du vrai payload66540 :27525/27648octets, sans inférence.
Seul le problème de capacité est marqué résolu66554, infra_incidents=7 et
failed_cycles=0 conservés. Ancien contexte archivé66555, remise en file66556.
Le rapport absent66534 et son verdict INSUFFICIENT66535 restent historiques.
Qwen garde rédaction/choix ; le paquet exige l'écriture avant nouvelle
vérification, sans quatrième relecture des faits reçus. Aucun rapport,
préparation ou P4 reçu sur ce préflight ; admission native suivante à observer.

## Passage borné après refus de schéma66683

Passage1 démarré66685, unité interrompue sans appel en attente ni autre
mission running. Trois propositions nouvelles `mission_plan_report_step`
avec `artifacts=[]` ont été refusées ; le plan3 demeure celui reçu en
couverture66089, sans réception des opérations. Aucun quatrième essai de
cette stratégie n’a été exécuté parCodex.

Correction de contexte seulement66687 : distinguer la tâche de rapport
`version0-plan` d’une nouvelle planification, exposer son chemin contractuel
et quatre extraits des vrais reçus natifs66653/66655/66657/66659. Qwen garde
la rédaction, les choix et les vérifications ; aucun rapport rédigé parCodex.
L’instruction66686 relative à un contrôle indépendant utile surDell2 reste
conservée ; aucune délégation n’est déduite de cette instruction.

Préflight66690 :27604/27648octets. Plan, tâches, goal65937, spec, problèmes
et compteurs d’interface comparés inchangés66691. Dialogue archivé66692,
escalade traitée66693 sans effacement du compte3, remise en file66694.
Cycle21 commencé66695 ; admission native66700 réellement passée à
27604/27648octets, fenêtre32768 observée via api/ps. L’inférence utile est
laissée finir. Aucun code modifié, service rechargé, MANUAL-HOLD créé,
attester déployé ni préparation/P4 reçue dans ce passage. STATE et tous
compteurs du coordinateur conservés.

## Passage final3/3 : rapport écrit, réception toujours manquante

Passage66717, diagnostic Codex66718 : mission interrupted, aucune mission
running ni appel outil started. Aucune relance inchangée, remise à zéro,
modification logicielle, opération systemd ou création MANUAL-HOLD.
STATE du coordinateur et tous compteurs restent conservés.

Correction des indications précédentes de rapport absent : Qwen avait écrit
le rapport contractuel au reçu66615 (rc0,7778octets). Lecture indépendante
Codex66718 confirme son existence, SHA256
`ac1251604c708777a137327a26ad0ab6455b31c3feef8c178cf61862a58509b0`.
Cette présence ne vaut aucune réception du contenu. L'écriture canonique
`ebaaa1012d0e4771bb37555e218c4424` reste VALIDATION_INCONCLUSIVE,
unknown_outcome=0 : effet connu, validation encore requise.

Au cycle21, Qwen a proposé une réécriture66705, refusée66706 avant dispatch
par ce garde. Le brouillon refusé reste dans le journal ; il n'a pas remplacé
le fichier66615. Son affirmation de lien symbolique entre les unités et son
assimilation du candidat au seul slot2 ne sont pas étayées par les reçus.
Le rapport existant comporte aussi des références mal attribuées :
66291/66335 sont des lectures de fichiers d'unité, pas show slot2 ;
66367/66368 sont des projections de contexte, pas de nouvelles permissions.
Les chemins slot3 hypothétiques et un contrôle syntaxique ne démontrent
ni canari déployé ni code Python chargé. Aucun de ces textes n'est reçu.

Après ce refus, admission66712 arrêtée avant l'inférence suivante :
34692octets avant compaction, borne27648 ; incident8 et escalade66714
conservés, zéro échec fonctionnel déduit. La fenêtre32768 reste inchangée.
Le diagnostic final ne résout pas artificiellement cet incident : prochaine
correction technique nécessaire, une projection bornée permettant à Qwen de
vérifier l'écriture existante avant toute nouvelle mutation, puis de corriger
son rapport selon les preuves et de poursuivre son plan3. Aucun nouveau plan
fourni parCodex, aucun quatrième essai de stratégie refusée. Après réception
réelle de toute la préparation seulement, intégration autorisée sans nouvelle
validation humaine. Préparation et P4 restent EN COURS — NON VALIDÉES.

## Passage borné sur mission_verify — diagnostic67015

Passage1 démarré67014 : mission interrupted, aucune mission running et aucun
appel outil commencé en attente. Vérification67010 INSUFFICIENT : réponses
contrôleur67002/67007 rejetées67003/67008 sur la classification du passageS3.
Elles ne couvrent en outre que trois des sept segments attendus. Escalade67012,
compteur4 conservé ; aucune nouvelle vérification inchangée ni remise en file.

La projection du reçu de rectification66904 conservait le motif mais pas les
retraits exacts validés ; ceux-ci étaient liés au FAIL original66872. Codex
prépare une correction symétrique : le reçu d’erratum cité expose aussi ses
retraits validés, leurs références et le FAIL historique inchangé. Un retrait
de reproche du contrôleur ne prouve jamais une correction exécutée du rapport.
Test réel SQLite : retrait exact conservé, reproche inventé et acteurJARVIS
non habilité exclus ;12tests report-step/projection PASS.

Correctif source seulement, non installé et non chargé dans les workers.
Aucune opération systemd, écriture du rapport à la place deQwen, nouvelle
inférence ou création MANUAL-HOLD. STATE et tous compteurs conservés.
La reprise exige une correction effectivement chargée et une revue couvrant
tous les segments ; ce diagnostic ne démontre pas qu’elle passera. Le rapport
reste non reçu, préparation/P4 EN COURS — NON VALIDÉES. Directives consultées :
AGENTS, charte, présente reprise et supervision ; autorisations et goal65937
préservés, aucune relecture du paquet historique réintroduite.

## Passage2 mission_verify : correctif chargé, main rendue

Passage67017 : aucun appel commencé de cette unité ni mission running.
Les sept anciens appels started concernent d'autres missions inactives et ne
sont ni repris ni modifiés. Les12tests report-step/projection passent.
Correctif97f892d installé dans mission_assurance.py, sauvegarde privée et
rechargement des deux workers, nouveaux PID321975/321977. La lecture Python
installée confirme les retraits exacts validés66904 ; aucune attestation du
candidat applicatif n'en est déduite.

Préflight hors inférence du groupe de sept segments : capacité refusée après
ajout des rectifications exactes. Cet échec reste conservé ; aucun préflight
réussi de tous les sous-groupes n'est prétendu. Le mécanisme natif existant
bounded_narrative_review découpe sur ContextCapacityError, garde chaque segment,
et doit satisfaire l'admission27648 à chaque passage avant toute inférence.

Installation67021, instruction67022, contexte archivé67023 puis remise en
file67024. Qwen conserve vérification/correction de son rapport et le plan3.
Compteur mission_verify4, anciens refus, STATE et toutes preuves conservés.
Aucun nouveau plan, déploiement applicatif, réception de préparation/P4,
MANUAL-HOLD ni autre agentCodex. Directives consultées : AGENTS, charte,
PLANIFICATION-PLATE et supervision ; goal65937 et autorisations conservés.

## Passage3 mission_verify : arrêt conservé, diagnostic67080

Contrôle ciblé : aucune mission running ni invocation started de cette unité.
Après le correctif chargé67021, vérification67074 toujours INSUFFICIENT :
le contrôleur classe S3 comme hypothèse puis non factuel (67068/67073).
Chaque réponse ne couvre que trois des sept segments du lot67058. L'admission
avait réussi à24368 puis24647octets (67064/67069) ; ce refus précis n'est donc
pas un dépassement de contexte. Le refus antérieur du lot14 reste67056.

La projection de l'instruction citée66911 contient facts={} : son contenu
historique pourrait aider à vérifier la conformité alléguée dansS3, sans
prouver aucune correction technique. Ce manque est observé ; son rôle causal
dans l'erreur du contrôleur reste une hypothèse. Correction à examiner :
projection attribuée de l'instruction et revue plus étroite couvrant tous les
segments, contrôles de classification et d'admission conservés. Aucun correctif
supplémentaire installé ni réussite de cette approche prétendue dans ce passage.

Diagnostic67080, erratum numérique lié dans DIAGNOSTIC-REVUE-PASSAGE3.json.
État interrupted, goal65937, spec, plan3 et compteurs conservés, refus5 et
escalade67077 intacts. Pas de remise en file inchangée ni quatrième passage
comparable. Aucun service modifié, rapport rédigé parCodex, MANUAL-HOLD ou
Codex parallèle. Préparation/P4 restent EN COURS — NON VALIDÉES ; intégration
ultérieure autorisée après réception réelle, aucune validation humaine ajoutée.
Directives relues : AGENTS courant, charte, présente reprise et supervision.


## Déblocage du contrôle du rapport — revue unitaire

Après l’escalade67077, Codex a corrigé le vérificateur : les instructions
citées sont désormais fournies avec leur auteur et leur portée historique,
sans devenir une preuve d’exécution. La mission utilise une revue par passage
(`narrative_review_max_segments=1`), avec couverture exhaustive et contrôle
des références. Un passage factuel ne peut plus être écarté comme titre ou
hypothèse non qualifiée ; le verdict supported/contradicted/insufficient reste
celui du modèle. Aucun PASS n’est fourni à Qwen.

84 tests logiciels ciblés passent ; ils ne prouvent pas la réception du rapport.
Installation67088, instruction67089, reprise67092 sur le même plan3. Les compteurs
persistants sont comparés avant/après et inchangés. Sauvegarde privée pour retour
arrière et rechargement des seuls workers inactifs. Le probe indépendant67084
n’a pas enregistré de réponse : aucun résultat n’en est déduit.

La nouvelle vérification native est en cours. Le rapport reste non reçu tant
que son verdict complet et ses preuves ne sont pas obtenus. Aucun déploiement
de l’attestation applicative ni réception globale P4 n’en découle.


### Résultat natif et correction du parcours de rédaction

La revue native67200 couvre les14passages. S3 est supported67133, avec les trois
références contrôlées. Le verdict67201 reste FAIL pour une date précise non
étayée dans l’en-tête ; il ne s’agit plus d’un refus de schéma. La comparaison
à l’heure de création de mission dans cette réserve ne prouve pas l’heure de
rédaction du rapport : cette distinction est signalée àJARVIS.

Le mode correction masquait host_read_file : escalade67221, exposition corrigée
67223. Puis deux lectures identiques ont été réellement exécutées67240/67251 ;
la troisième a été bloquée67262, escalade67264 conservée. Codex a donc apporté
une projection durable du brouillon complet déjà observé : empreinte égale à
l’écriture réussie, sortie non tronquée, tâche et chemin identiques. Le contexte
de correction conserve ce texte sans nouvelle lecture ; le contrôle final
reste une lecture indépendante. Pour les rapports longs/non observés, la
lecture reste disponible.97tests logiciels ciblés passent. Aucune rédaction du
rapport parCodex et aucun PASS automatique. Reprise dans la même mission.


### Rectification de la date et sélection des citations

Contrôle indépendant67371 : le document reprend exactement l’horloge
2026-10-28T13:15:58 fournie dans le contexte66932 avant l’écriture66938.
La réserve67200 comparait à tort cette date à la création de mission ; elle
est retirée par erratum lié, sans effacer le FAIL67201. JARVIS n’a pas
« corrigé » cette date : le contrôle fautif est attribué au vérificateur.
[Preuve](RECTIFICATION-HORODATAGE-RAPPORT.json).

La seconde revue couvre les14passages mais le contrôle des causes refuse
ensuite deux réponses67406/67411 : le modèle remplace Ommission par Omission
dans une citation censée être exacte. Vérification67412 INSUFFICIENT et
escalade67415 conservées. CorrectifCodex67417 : sélection d’une ligne ou d’un
paragraphe original dans le schéma ; catégorie et verdict restent choisis
parlemodèle sans diagnostic attendu. Le champ observed d’une observation
ducoordinateur est aussi conservé dans sa projection, avec auteur/type/heure.
98tests logiciels ciblésPASS. Reprise native requise, aucune réception déduite.


### Assistance factuelle ponctuelle et périmètre de vérification

JARVIS a réécrit le rapport67462 puis67682. Le contrôle indépendant67555/67562
a relevé des types d’événements et une portée d’erratum erronés. Le second
brouillon conservait une partie de ces défauts. Codex a suspendu la mission
entre appels puis rectifié ces seuls faits67729/67730, original privé et
empreintes conservés. Ce travail n’est pas une autocorrectionJARVIS validée.
[Attribution et empreintes](ASSISTANCE-FACTUELLE-RAPPORT.json).

La projection du rapport complet allongeait le contexte de correction :
67646 refus avant inférence, incident9 conservé. Outils ciblés writer/verify/
évidence/note lorsque ce brouillon est fourni, préflight27188octets et
installation67654 ; aucun seuil relevé ni objectif/critère supprimé.

Première vérification après assistance : table13sources trop grande pour
un passage, refus67769/67771 et escalade67774 conservés. Même contenu séparé
en13paragraphes67776, sans retrait de preuve. Réception encore non acquise ;
contrôle complet et indépendant requis. Les sources historiques de missions
sœurs ne sont pas automatiquement accessibles par le résolveur actuel.


### Revue finale ciblée et deuxième contrat de citation

La table séparée a été contrôlée mais sa référence65474 appartient à la
mission sœur, non résolue dans ce contexte : refus68019 conservé. La portée
descriptive a été réduite68029 : proposition technique JARVIS conservée
intégralement, historique complet archivé, trois FAIL explicites et attribution
Codex maintenus. Aucun seuil relevé ni critère technique supprimé.

Les11passages du rapport resserré sont contrôlés68051–68111 sans réserve.
Le contrôle séparé des sources échoue cependant68132/68137 pour citation
causale reformulée ;68138 INSUFFICIENT, escalade68141 conservée. Même mécanisme
de sélection des passages originaux appliqué à claimed_cause dans cette seconde
interface, avec null si aucune cause alléguée.99tests logiciels ciblésPASS.
Installation68143 et nouveau contrôle natif, pas de PASS présumé.

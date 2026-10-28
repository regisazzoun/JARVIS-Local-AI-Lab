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

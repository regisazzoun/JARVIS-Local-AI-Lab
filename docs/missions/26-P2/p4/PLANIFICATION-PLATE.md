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

# Reprise après stagnation : fonction réelle, édition ciblée

L’arrêt74343–74346 reste conservé : deux corrections réellement exécutées mais
échouées sur des fichiers inexistants, aucun changement ni test fonctionnel.
La fonction `audit_plan` appartient à `p3-bounded-review/engine/jarvis/mission_assurance.py`.
Une autre fonction du même module, `bounded_narrative_review`, concerne la prose
et ne remplace pas le contrôle de couverture demandé.

## Capacité manquante corrigée par Codex

L’outil `authority_draft_edit` n’acceptait que des fichiers Python de6000octets
maximum. Le vrai module est plus grand. Un paramètre optionnel `symbol` extrait
par AST une fonction de premier niveau avec ses décorateurs, son chemin réel,
ses lignes, l’empreinte de l’unité et celle du module. L’unité conserve la limite
6000octets ; la garde de requête27648 et la fenêtre32768 restent inchangées.
Un symbole absent, ambigu, renommé dans la proposition ou un chemin hors périmètre
est refusé. L’application garde l’ancre littérale exacte, sans recopier le module.
Les autres fonctions et le préambule restent inchangés. Le code proposé appartient
à Qwen ; Codex n’a fourni aucun algorithme de couverture.

Le schéma peut borner cette unité au couple chemin/symbole réellement observé.
Une proposition ne devient applicable que lorsqu’elle existe ; le schéma d’application
expose ses vrais identifiants pour la tâche et l’auteur concernés. Le message de
la phase de codage ne demande plus un outil d’inspection non proposé. Après une
modification réelle, les outils de tests et de vérification indépendante reviennent.

## Contrôles et reprise

90tests logiciels ciblésPASS : extraction et modification d’une fonction dans un
grand module, conservation des autres sources, décorateurs, noms contenant les
marqueurs du template, refus des symboles absents/ambigus, contrats de chemin et
propositions de la bonne tâche.5tests de supervisionPASS. Aucun test logiciel
n’est présenté comme une démonstration d’autonomie.

Observation réelle74357 sur les deuxDell : `audit_plan`5437octets et mêmes
empreintes d’unité/module. La première révision de plan a été refusée parce que
Qwen supprimait la tâche déjà tentée ; l’original est conservé. Codex a demandé
un lot principal court et la conservation de son identifiant. Qwen a enregistré
la version2, inférence74368 et appel natif référencé dans
[REPRISE-UNITE-SOURCE.json](REPRISE-UNITE-SOURCE.json). Cette révision est assistée,
le titre retourné reste peu descriptif ; aucune planification sans aide n’est reçue.

Préflight74379 :10755/27648octets, prochain outil proposé `authority_draft_edit`,
sans appel exécuté par la sonde. Résolution74381 de l’escalade74344 après vérification
technique74380. Deux incidents d’exécution passés sont acquittés dans le registre
natif, sans effacer leurs totaux ni leurs reçus ; aucune défaillance fonctionnelle
convertie en réussite. [Preuves](REPRISE-SOURCE-REELLE.json).

La supervision distingue une nouvelle stratégie seulement après un événement
`coordinator_strategy_verified` Codex avec preuves du même journal et empreintes
des modules installés. Un changement de session, de libellé ou un événement sans
preuves ne débloque pas trois passages épuisés. Les compteurs de l’ancienne
stratégie restent enregistrés. Cela accompagne ici la vraie capacité nouvelle
d’édition AST et les observations des deuxDell, sans remettre STATE.json àzéro.

Retour arrière : sauvegardes privées des modules et du coordinateur ; restaurer
puis redémarrer les seuls workers, après observation d’absence d’opérations actives.
Conversation et interface préservées. Ni modèle, routage ni matériel modifiés.
P3 doit encore livrer son code et ses tests ; P4 reste en attente, VF01 non transmis.

## Proposition reçue, transport du patch et issue observée

JARVIS a utilisé le nouvel outil : proposition74445 surDell1, contexte de rédaction
8036octets74441. Son algorithme utilise des lots fixes500 ; Codex ne le reçoit pas
comme preuve de respect du budget. Les propositions74519 (style) et74585
(quasi identique) sont conservées mais ne remplissent pas l’objectif fonctionnel,
contrôle indépendant74629. Aucun de ces textes ne vaut test ou déploiement.

L’application a rencontré la limite de longueur du schéma `host_remote` : l’ancre
et le nouveau code rendaient l’enveloppe inline trop longue. La commande exacte
refusée a été reliée au registre natif avant tout rejeu ; une lecture indépendante
a confirmé module et fonction inchangés. L’issue auparavant inconnue est observée
`NOT_EXECUTED`74610, sans réécrire son ancien événement incertain.

Le transport durable transfère maintenant une enveloppe trop longue comme fichier
privé `.receipts/*.runner.py` via le broker existant, puis vérifie son empreinte
avant exécution d’une courte commande. Le script conserve le contenu original,
les limites du sandbox, les manifestes et le reçu complet ; aucune augmentation
de plafond, aucune troncature. Les octets vérifiés sont ceux compilés. Test réel
Codex surDell2 : commande logique25391caractères, exécution réussie et seconde
lecture du fichier privé concordante74622. C’est un contrôle d’infrastructure,
pas une correction applicative JARVIS.

148tests ciblésPASS. La transition d’une issue inconnue vers `NOT_EXECUTED`
nécessite une preuve explicite de non-exécution. Une réémission de la même intention
n’est autorisée qu’après réparation d’infrastructure attestée ultérieurement ;
elle réutilise l’identifiant de tentative et garde les événements et compteurs.
Une issue inconnue ou trois échecs fonctionnels restent bloquants. Résolution74626,
aucune issue inconnue restante avant reprise.

La limite des fonctions ciblées passe à12000octets pour permettre la reprise
d’une fonction modifiée plus grande que l’original ; la limite d’un fichier entier
reste6000, et la requête complète reste soumise à27648. Les trois brouillons sur
source inchangée sont épuisés : pas de quatrième génération autonome ; seuls les
vrais brouillons existants restent applicables jusqu’au prochain résultat observé.
[Preuves](TRANSPORT-PATCH-ET-REPRISE.json). Même mission et plan2 remis en file.

## Résultat attendu conservé dans le contexte de codage

L’application réelle74675/74682 surDell1 porte sur la proposition74585. Le contrôle
AST confirme que sa logique est identique à l’original : l’écriture de fichier est
prouvée, la correction fonctionnelle est rejetée74948. La synchronisation74920 vers
Dell2 est réelle, mais ne transforme pas cette proposition en solution.

Le test JARVIS74722 a lancé437cas :1échec et53erreurs d’import de composants
extérieurs à l’export. Cette campagne ne qualifie pas le contrôle de couverture.
Codex fournit donc un oracle ciblé indépendant, sans recopier `audit_plan` ni
`review_model` : il importe les vrais modules et exerce le vrai `ContextBudget`,
avec une réponse backend contrôlée. Il teste compatibilité petite entrée,
cinq exigences longues réductibles, omission qui ne doit pas produire PASS,
et entrée indivisible bloquée. Baseline locale :4tests,2PASS/2FAIL. Ce contrôle
logiciel n’atteste pas le raisonnement d’un modèle réel ni l’autonomie de JARVIS.
Ce n’est pas l’épreuve finaleM26-P2-VF01.

Le même script a été transféré sur les deuxDell74947 ; son empreinte doit rester
inchangée dans les contrôles indépendants. [Entrée et provenance](CONTROLE-CIBLE-FOURNI.json).
Le script reproductible est [coverage_budget_probe.py](../../../../tools/mission26_phase2/probes/coverage_budget_probe.py).
Les sorties originales restent en stockage privé ; aucune campagne P2 reçue rejouée.

Cause supplémentaire corrigée : la rédaction isolée n’avait pour objectif que la
chaîne choisie par le modèle ; `apply`/`propose` perdaient donc le résultat attendu.
Le mode ciblé conserve maintenant `authority_coding_objective` indépendamment de
cette chaîne, sans recharger le parent ni son historique. Une demande trop courte
est refusée en schéma et au backend. Le flag opt-in `authority_behavioral_change`
refuse une proposition dont l’AST est identique ; cela élimine le style seul sans
prétendre qu’un AST différent prouve une bonne correction. Les tests fonctionnels
et le contrôle Codex restent obligatoires. Les autres missions gardent leur mode.

Une correction ou un test réellement observé empêche désormais de réintroduire
l’obligation d’inspection initiale à chaque tour.141tests ciblésPASS, ensembles
recouvrant les campagnes précédentes (ne pas additionner). Installation et reprise
74951 : objectif conservé, oracle fourni, même mission/plan/compteurs. P3 reste non
reçue, P4 attend et l’épreuve finale distincte n’est pas encore transmise.

## Boucle corrective restaurée après le test ciblé

JARVIS a exécuté l’oracle surDell2 :74992,4tests,2PASS/2FAIL, code de processus1.
Source de test inchangée et manifeste stable, preuves
[CONTROLE-CIBLE-EXECUTE.json](CONTROLE-CIBLE-EXECUTE.json). Un essai suivant75083
surDell1 a doublé un préfixe de chemin et n’a pas lancé le test ; la commande avec
chemins absolus a été fournie pour supprimer cette ambiguïté, sans classer ce
refus de fichier comme un échec fonctionnel du contrôleur.

Le focus de codage ne s’appliquait qu’avant la première modification : après un
test échoué, il exposait à nouveau tout le catalogue au lieu de guider la boucle
courte. Il revient maintenant après chaque échec, avec diagnostic préalable si
le dernier vrai test n’a pas été analysé. L’analyse est écrite par Qwen et liée
à la référence réelle ; l’orchestrateur ne choisit pas son hypothèse.

Dans une tâche exigeant un changement de comportement, le filtre AST s’applique
aussi aux anciennes propositions. Les propositions déjà appliquées restent
idempotentes dans le backend, mais ne sont plus proposées comme prochaines
corrections. Les brouillons refusés sur une source inchangée restent limités ;
une vraie version ultérieure autorise son propre travail sans remettre à zéro
les cycles de l’anomalie. Le curseur de phase74951 écarte l’ancienne écriture
cosmétique de la réception de ce nouveau résultat ; les échecs et compteurs
précédents restent intacts.

88tests logiciels ciblésPASS. Préflight réel75274 :23538/27648octets, prochain outil
`authority_analyze`, aucune action exécutée par cette sonde, compteur inchangé.
[Contrat](BOUCLE-CORRECTION-REPRISE.json). Même mission et plan2 repris.
Cela prouve la réparation du chemin d’exécution, pas encore la réussite de P3.

## Frontière de fonction et version réellement testée

La proposition75462, rédigée par Qwen, passait l’analyse syntaxique isolée mais
n’avait pas de retour à la ligne final. À l’application, `return review` se collait
au `def ensure_plan_review` suivant. Le garde syntaxique du module a empêché
l’écriture. Codex corrige cette frontière de transport ; la sortie originale du
modèle reste conservée et la normalisation est journalisée. Les tests couvrent
une fonction immédiatement suivie d’une autre, ainsi qu’une proposition déjà
persistée sans saut de ligne. [Reprise](FRONTIERE-FONCTION-REPRISE.json).

Après réparation : application réelle75575 surDell1, quatre cas ciblésPASS75624,
module complet comparé à la composition attendue avec la seule normalisation
annoncée. [Preuves](QUATRE-CAS-DELL1-PASS.json). Le candidat reste un lot fixe2 :
deux exigences de15000octets dépassent27648 avant même le reste du paquet.
Le contrôle de tailles variables reste donc obligatoire avant réception générale.

Le test75723 surDell2 portait encore sur l’ancienne copie. Le focus de correction
considérait tout échec ultérieur comme rejet du code nouveau ; il renvoyait ainsi
le modèle rédiger sur une version dont les trois brouillons étaient épuisés.
Il compare maintenant le manifeste stable du test au manifeste de la correction.
Un échec d’une ancienne copie conduit à synchroniser/vérifier la version actuelle.
Les compteurs historiques ne sont pas remis à zéro.

Le schéma de synchronisation expose les références d’exécution de la dernière
version observée par hôte, liées au choix de l’hôte source ; un identifiant de
proposition ne peut plus être choisi à sa place. L’outil recontrôle la fraîcheur
avant transfert. Les nouveaux reçus d’application remontent aussi leur vraie
référence d’exécution au premier niveau, sans réécrire les anciens reçus.
157tests ciblésPASS, dont échec d’un pair sur ancienne version et références de
synchronisation hôte/version. Préflight75866 :24445/27648octets ; synchronisation
proposée, rédaction indisponible à cette phase. Résolution75867 de l’arrêt75856,
même mission/plan2 remis en file. [Contrat](REPRISE-VERSION-SOURCE.json).

Réserve de classification conservée :75391 était une erreur d’argument `.` ajouté
au lancement du probe, pas l’exécution de ses quatre cas. L’analyse erronée75427
reste archivée avec rectification ultérieure. Les compteurs bruts n’ont pas été
effacés ; leur interprétation et la portée des campagnes doivent rester explicites
dans la réception finale. La ponctuation ambiguë de la première consigne Codex a
été remplacée par une invocation ARGV/ENV complète dans le texte court transmis.

## Probes déclarés et arrêt fonctionnel vérifié

La classification76120–76144 reste exacte à son jalon : un échec qualifié et deux
classifications rectifiées, historique3. Les probes ont ensuite été choisis et
exécutés par JARVIS : VAR76210/Dell2 FAIL ; correction Qwen76325/Dell1 ;
CORE76377/Dell2 PASS sur l’ancien module ; VAR76477/Dell1 FAIL sur le nouveau.
Le test est resté au SHA indépendant déclaré. Les reçus complets ont été vérifiés
par Codex76597 ; [empreintes et versions](DIAGNOSTIC-PROBES-76594.json).

Les deux nouveaux échecs sont fonctionnels : ContextCapacityError pour une entrée
réductible. La correction conserve BATCH_SIZE=2 et ajoute des contrôles après
review_model, donc après le point qui lève l’exception. L’analyse Qwen assimilant
le PASS CORE de l’ancien Dell2 à une divergence de sérialisation est réfutée par
les versions et les contrats distincts. Le budget d’entrée est27648octets, pas32768.

Le registre porte désormais3échecs qualifiés +2classifications rectifiées =5.
Les compteurs, originaux et arrêt sont conservés ; aucune résolution infrastructure
ni nouveau segment d’exécution déclaré. Paquet court76598 pour JARVIS : revoir
le diagnostic, choisir une stratégie différente adaptant les lots au paquet réel,
préserver les contraintes globales et bloquer un singleton indivisible. Cette note
ne prouve pas une stratégie implémentée/vérifiée et ne débloque pas une quatrième
tentative. Mission interrupted ; P3 non reçue, P4 attend, VF01 non transmis.

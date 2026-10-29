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

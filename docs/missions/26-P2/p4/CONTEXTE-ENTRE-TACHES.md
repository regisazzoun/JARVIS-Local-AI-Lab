# Contexte entre tâches et résultat de vérification

Après la réceptiont1, JARVIS a réellement observé les deux workers par
host_service show et is-active (70584/70586/70588/70590). Une vérification du
rapport suivant, encore absent, a produit INSUFFICIENT70602 et escalade70605.
Les anciennes consignes de vérifier le rapportt1 sans le réécrire avaient été
réinjectées lors de la réduction du contexte de la nouvelle tâche.

Défaut : l’orchestrateur filtre déjà les consignes Codex par tâche active ou
portée globale autorisée, mais le checkpoint prenait la dernière consigne de
la mission entière. Correction : le checkpoint utilise exactement le même
sélecteur autorisé et la même portée que l’orchestrateur. Les anciennes
consignes restent dans l’archive, sans devenir des instructions de la nouvelle
tâche. Une nouvelle session n’efface aucune preuve ni aucun compteur.

Deuxième défaut : un résultat natif PARTIAL/INSUFFICIENT était traité comme un
refus d’interface. Le cycle conserve maintenant le verdict comme résultat de
vérification exécutée ; il ne prétend pas que l’opération ou le test fonctionnel
sous-jacent a été exécuté avec succès. Les vrais refus de paramètres/outils et
les gardes anti-répétition restent bornés. Les anciens compteurs incorrectement
incrémentés restent visibles et ne sont pas effacés.

177 tests ciblés PASS sur quatre modules, dont contexte entre tâches, absence de
perte des compteurs et distinction des verdicts PARTIAL/INSUFFICIENT. Correctifs
installés avec sauvegardes, checkpoint70609 contrôlé sur la tâche réelle et
compteurs inchangés, résolution70610. Contexte actif réinitialisé depuis le
checkpoint ; archives conservées, nouvelles observations systemd acquises.
JARVIS reprend la rédaction de son propre rapport à partir de ces preuves.
Aucune réception de cette tâche ni deP4 n’est annoncée par cette correction.


## Passage des faits observés à la rédaction

Après reprise, deux consultations réelles du registre (70623/70633), puis un
refus de répétition et escalade70645. Le moteur ne détectait l’acquisition des
faits que sous un focus d’outils explicite ; les tâches ordinaires gardaient
la consigne de consulter le registre avant chaque rédaction. La détection
porte désormais sur les reçus réussis de la tâche, même sans focus spécial.
L’outil de faits déjà consulté n’est plus proposé comme prochaine action ;
les autres outils d’observation restent disponibles. Le choix de contenu
reste celui du modèle. La garde anti-répétition n’est pas désactivée.

Les sorties systemd show complètes dépassent huit kilo-octets. Une simple
coupe début/fin pouvait retirer les propriétés nécessaires du milieu du
texte. Le checkpoint et le contrôleur reçoivent maintenant une sélection
exacte des champs réellement présents dans les sorties réussies et complètes
(PID, chemins, états, dépendances, environnement, commande). Références, heure
d’observation et SHA du texte original restent associés. Un champ non
sélectionné ne devient jamais absent ; aucune sortie échouée ou tronquée ne
peut fournir ces propriétés. Les textes complets demeurent dans les reçus.
Ces valeurs sont historiques et ne prouvent aucun état après redémarrage.

180 tests ciblés PASS sur les quatre modules. Le checkpoint réel70647 conserve
les quatre observations utiles après notes et consultations du registre ;
compteurs vérifiés inchangés. Installation et résolution70648, reprise native
de JARVIS. Rapport suivant etP4 toujours non reçus à ce stade.


Le premier paquet intégrant ces observations a été refusé avant inférence
(70657), sans effet exécuté. L’étape déclarait uniquement host_service ; la
sélection initiale ajoutait onze outils de contrôle sans exposer l’écriture
du rapport. Après acquisition des faits, le moteur propose désormais les outils
déclarés par le plan et l’écriture/note/blocage, sans boucle de découverte du
registre déjà lu. Les vrais outils d’observation déclarés restent disponibles.

Préflight70665 sur le paquet réellement refusé70655 : 24900octets/27648,
politique/objectif conservés, quatre observations intactes. Pas de hausse du
contexte32768. Les treize incidents de capacité restent comptés, acquittement
explicite70666/70667 après preuve ; aucun échec fonctionnel effacé. Reprise de
la même tâche après ce changement technique, sans répéter la stratégie refusée.


## Vérification du rapport effectivement écrit

JARVIS a écrit réellement son rapport d’état70691. La première revue a été
refusée : doublon entre propriétés systemd sélectionnées et extraits bruts longs
des mêmes reçus. La vue de revue conserve maintenant les propriétés exactes,
rc, références broker et empreintes, sans envoyer une seconde fois le stdout.
Les sorties complètes restent dans les reçus. Aucun champ omis n’est déclaré
absent. Le code observé sur disque n’est toujours pas assimilé au code chargé.

La phase de rapport vérifié expose uniquement la vérification native et
notes/blocage ; la phase de clôture expose la clôture native et notes/blocage.
Le contrôle complet reste dans les mêmes outils backend, avec relecture réelle,
revue des affirmations et fraîcheur. Cela supprime les schémas redondants du
contexte et les appels concurrents de revue du même rapport.

180 tests PASS. Deux préflights sur les vraies entrées refusées :70749,
25635/27648octets pour la revue ;70753,26911/27648 pour le décideur en phase
vérification. Même politique, objectif, passages, critères et sources conservés.
Preuve de réparation70754/acquittement70755 : incidents historiques maintenus,
pas de compteur remis àzéro ni PASS injecté. Le même rapport reprend son
contrôle natif ; cette correction ne le reçoit pas par anticipation.


## Correction de la narration après son premier verdict

Revue70893/70894 : le rapport ne conservait pas explicitement les FAIL
historiques ; ce point reste à corriger par JARVIS. Deux autres reproches
provenaient du parseur : les sources étaient citées sous `**Référence**`,
format Markdown non reconnu. La détection normalise ce seul balisage puis
résout les vrais reçus existants. Aucune référence inconnue n’est inventée.
Erratum70928 retire uniquement les reproches de références/sources absentes ;
le tableau doit être revu sur les sources, pas reçu par cet erratum.

La correction reçoit le brouillon complet. Si le paquet ne tient plus, les
anciennes valeurs systemd sont conservées intégralement dans le checkpoint,
avec champs, références et empreintes dans l’état actif ; la revue indépendante
continue de recevoir les propriétés originales. Les scopes explicatifs
identiques sont présentés une seule fois, sans perdre leur portée. Toutes les
contraintes, tous les compteurs et les textes originaux restent conservés.

181 tests ciblés PASS. Préflight70927 sur le vrai paquet refusé70904 :
27366/27648octets, brouillon5365octets entier, quatre observations référencées
et valeurs complètes archivées. Réparation70929/acquittement70930 après cette
preuve, totaux inchangés. JARVIS reprend la correction de son propre récit ;
aucune réécriture du rapport par Codex dans cette étape, aucun PASS injecté.

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

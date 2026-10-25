# Reprise distante et supervision persistante

Sur demande explicite du propriétaire (« débloque et surveille que je ne doive pas te relancer à chaque fois »), Codex traite les trois blocages sans les masquer.

- D03 : les fichiers de test manquaient sur Dell1 ; tentative write_file hors profil puis SSH sur un identifiant broker nonDNS. Sources et test réellement transférés/extraits par Codex dans les deux projetsDell. Le test source réelle passe6/6 sur chacune des deux machines lors de ce préflight. Ce sont des actions Codex, pas une réception JARVIS.
- D04 : ancien test copiant sa propre fonction, attentes incohérentes et commandesnode-e contenant desbackticks. Reprise demandée avec un vrai module importé et des scripts/fichiers exécutés surDell2 ; aucun succès du candidat D04 n’est encore reçu.
- D17 : paramètres host/action manquants et confusion entre cheminsMac et cheminsDell. Projet peuplé sur les2Dell ; la sonde hôte telemetry_v3 existante est exposée en lecture au profilDell2, sans autre changement de politique. Son préflightCodex observe réellement3090+3080. JARVIS doit la réutiliser avant de contrôler le raccordementJL03.

Le garde est corrigé et installé dans JL03 (commit7aa6288, redémarrage du seul serviceV3, santéHTTP reçue). Un TAP exécuté et échoué compte désormais comme contrôle effectué, sans effacer son échec. Les .mjs sont distingués par ressource ; une pipeline qui renvoie0 en masquant #fail>0 n’efface plus l’échec du test. Douze testsPython reçus, dont trois nouveaux cas ciblés. Pas de remiseàzéro des compteurs ni de réception simulée. JL01/JL02 n’ont pas été redémarrés.

Les plans canoniques des trois tâches sont révisés et les contextes repris depuis des paquets courts. Les outils techniques proposés sont distants ; host_write_file reste pour le rapport local. La sélection actuelle des outils dans le moteur est une sélection de schémas, et non une nouvelle frontière de permissions : une découverte dynamique d’un outil enregistré reste possible. La supervision doit donc contrôler les lieux réellement observés, sans prétendre que le simple prompt garantit à lui seul le placement.

Les sources sont déjà sur les Dell, sans sous-dossier source. Le Mac conserve les preuves, la coordination et la mémoire ; Qwen80B continue de raisonner surDell1. Les erreurs historiques de transfert restent conservées. Des événements coordinator_instruction transmettent les nouvelles preuves au prochain tour, afin d’éviter de prendre l’ancien reçu de fichier absent comme étatcourant.

## Supervision après la conversation

Deux mécanismes complémentaires et séparés de l’exécution : le dispatcher existant vérifie toutesles30s les places disponibles ; le nouveau timer de coordination vérifie toutesles2minutes les trois tâches ciblées. Il n’appelle Codex que pour un blocage, une réception à relire ou une absence de progression supérieureà15minutes. Il réutilise le moteur et la base canoniques, sans nouveau modèleJARVIS ni nouvelle mémoire.

La coordination périodique est un vrai processus CodexCLI noninteractif, avec l’authentificationCLI déjà présente, distinct des workersJARVIS. Le skill OpenAI Docs a été utilisé ; [documentation officielle du mode noninteractif](https://learn.chatgpt.com/docs/non-interactive-mode). Test de lancement effectué : SUPERVISION_READY. Aucun secret transmis au modèle ou aux journaux publics.

Une seule intervention Codex périodique peut tourner à lafois, au maximum7minutes. Elle doit diagnostiquer, corriger une cause réelle, contrôler, documenter l’attribution puis rendre la main àJARVIS. Trois passages maximum pour un même état irrésolu, puis arrêt documenté de cette stratégie, jamais répétition illimitée. Les compteurs natifs deJARVIS restent indépendants et persistants. Le programme ne garantit pas la résolution de tout incident matériel ou logiciel inconnu ; il permet le diagnostic et l’intervention sans attendre une relance de cetteconversation.

Les sorties détaillées Codex restent privées sous jl03-cor-p1-private/supervision ; seuls les rapportsfactuels et événements decoordination sont proposés dans les dossiers de mission. Le timer ne publie pas les raisonnements internes. Aucun email ou message tiers envoyé. Les corrections et réceptions restent attribuées selon les reçus, sans confondre une interventionCodex avec une autonomieJARVIS.

Services : jarvis-jl03-p1-supervision.timer et .service. Script : /usr/local/lib/jarvis-coordination/periodic_codex.py. Arrêt explicite du suivi : systemctl stop jarvis-jl03-p1-supervision.timer ; le dispatcher est séparé. Le superviseur est limité à D03/D04/D17 et ne lance aucune autre mission. Maximum deux contextes de travailJARVIS ; le processusCodex est de coordination, pas un troisième workerDell.

## Correction du dispatcher après contrôle d’avancement

Une reprise D03 révisée et armée restait en waiting_external ; le sélecteur ne traitait que interrupted. Codex étend la sélection aux attentes externes uniquement si une reprise contrôlée est armée et si son plan/événement correspondent toujours. Trois contrôles ciblés passent ; installation et exécution réelles : D03 queued. Les limites de concurrence, compteurs et barrières de preuve restent conservés. D04 demeure non réceptionnée ; D17 travaille.

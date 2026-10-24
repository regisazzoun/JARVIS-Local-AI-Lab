# Incidents et règle des trois tentatives

La stratégie générale de réécriture des modules a été arrêtée après trois délégations infructueuses par composant. Les modèles ont cependant effectué plusieurs écritures dans certaines délégations : le journal en conserve notamment17pourvoice.js avant interruption. Ces dépassements initiaux sont un défaut réel de supervision, pas un respect rétroactif de la règle. Les captures et sources disponibles sont gardées ; certaines captures initiales ont été remplacées avant durcissement de l'archivage, ce qui est signalé au lieu de prétendre un historique parfait.

| Blocage | Observation | Sortie de stratégie |
| --- | --- | --- |
| Cristal | FFTincorrecte, constructeur, pas de rendu, pistes externes stoppées | Arrêt des réécritures globales ; intégration ciblée Codex puis WebGL/WebAudio réels |
| Interface | SchémasAPI et nomsDOM faux, inlineJSrefusé parCSP | Adaptation ciblée au contrat canonique ; essais navigateur |
| Console | Curseur vide, polling interrompu, troisième version syntaxiquement invalide | Pas de quatrième réécritureJARVIS ; patch ciblé Codex et pagination/scroll testés |
| Voix | Analyseur débranché, MIME/MediaRecorder incorrects, réponseSTTmaltraitée | Conservation des sources, pipeline corrigéCodex, trois segments et interruption réelle |
| Compagnon | Quatrième essai possible, tunnel tué à la sortie, open supprimé | Arrêt de la stratégieJARVIS ; correction cibléeCodex et fixtures processus |
| Garde | Regroupement trop large des erreurs de fichiers | Clé de blocage fondée sur cible et catégorie ; comptage conservé, test d'alias |
| Conversation | Catalogue complet dépasse contexteMac | Sélection d'outils et routage vers moteur existant, modèle27Bpréservé |
| LiveKit | DistributionSDKabsente, agent non prêt lors première phrase | Ajout distributionofficielle/licence puis attente de préparation ; essai réel |
| RecetteCodex | FixtureSSHécrivait dans son propre exécutable | Correction de la fixture, premierFAILconservé, neuf tests reçus ensuite |

Le garde installé observe les appels terminés du moteur existant : trois échecs d'un même blocage, trois lectures identiques ou trois réécritures sans contrôle. Les alias de commande ne réinitialisent pas le compteur. Il interrompt de façon coopérative et journalise la cause. Une repriseV3sans diagnostic/changement de stratégieCodexpostérieur est refusée409. Les compteurs sont reconstruits après redémarrage ; les anciens arrêts déjà suivis d'une nouvelle approche documentée ne sont pas rejoués comme de nouveaux échecs.

Preuve opérationnelle : mission `2d13b9ec8bd547f9b8b481cefb4aa4d5`, JARVIS exécute réellement trois variantes visant le même fichier de test volontairement absent. TroisFAIL, étatinterrupted, événement33358, aucun quatrième appel, reprise409. Cette fixture ne prouve pas une réparation applicative. Les autres tâches restent possibles.

Limite : observateur externe au préappel, pas une barrière atomique universelle ; une commande déjà engagée peut terminer et un lot très rapide peut dépasser l'observation. La distinction sémantique d'une nouvelle stratégie reste coordonnée par Codex. Les dépassements historiques et cette limite empêchent de recevoir l'autonomie de développement sans assistance.

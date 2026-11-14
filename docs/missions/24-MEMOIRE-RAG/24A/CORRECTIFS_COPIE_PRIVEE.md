# Correctifs autorisés sur copie privée — 14 novembre 2026

> **Complément ultérieur :** le [recoupement extractif sur copie](RECOUPEMENT_SOURCES.md) a depuis passé la recette ciblée S407. Le présent document conserve les résultats des trois essais de synthèse libre précédents.

**✅ Citations et statuts d’erreurs vérifiés. ✅ Accès au modèle standard corrigé. ❌ Synthèse multi-sources non réceptionnée après trois essais. Réception fonctionnelle globale : NO-GO. Production préservée ; 24B non lancée.**

## Décision du propriétaire et périmètre
Le propriétaire autorise les trois derniers correctifs proposés, leurs tests sur copie privée et la mise à jour de la PR #50. Il rejette explicitement le premier : JARVIS doit pouvoir lui retrouver les informations d’authentification auxquelles il a droit. Cette décision récente remplace, pour cette capacité propriétaire, l’interdiction générique du plan « aucun secret dans le RAG ». Elle n’autorise pas leur publication ni leur accès par un autre utilisateur.

**Aucun filtre de contenu, coffre séparé ou blocage de restitution au propriétaire n’a été ajouté.** Le garde de recette a aussi cessé d’exclure une source uniquement parce que son titre évoque des identifiants. Les lectures restent dans le compte Éducation existant, les documents découverts et le périmètre de copie ; les mutations restent refusées. Les preuves et réponses publiées sont expurgées après le test. Une mention d’authentification dans une réponse au propriétaire n’est donc plus, à elle seule, un critère d’échec de cette réception. Le constat historique du 13 novembre est conservé avec sa politique d’alors.

Directives relues : AGENTS.md, charte fondamentale, SUIVI.md, ROADMAP.md, plan PR #49, rapport et tests de clôture 24A. Autorisations conservées : copies, lectures réelles, tests et publication expurgée. Aucune migration, ingestion 24B, activation de production ou fusion autorisée dans ce complément.

## Changements réellement essayés

| Correctif | Réalisation en copie | Résultat |
|---|---|---|
| Citations et erreurs | Adaptateur de lecture : URL canonique, titre et modification issus des métadonnées découvertes, date UTC de lecture, empreinte SHA-256 du texte effectivement lu et extrait. Middleware natif : cartes sources pour les lectures réussies ; returncode/MCP error détectés même avec HTTP 200. Un résultat de recherche seul ne devient plus une citation de document. | ✅ Vérifié sur les trois lectures de l’essai 2 et la lecture de l’essai 3 ; fenêtre de citation et lien réel observés dans le client. Deux anciens échecs auparavant « completed » deviennent « failed » au rejeu. |
| Dates et états | Instructions génériques ajoutées au modèle : date d’observation distincte de modification/lecture, critères matériels/SIP/appels séparés, proposition distincte de validation, contradictions conservées ; relance courte après recherche vide. Aucun fait ni réponse S407 injecté dans ces instructions. | ❌ Non réceptionné. Progrès sur le jeu fictif, mais instabilité sur le scénario réel après trois essais. |
| Modèle utilisateur | Deux droits explicites de lecture du moteur de base accordés aux deux utilisateurs fictifs déjà habilités à l’alias. Aucun rôle admin, outil supplémentaire ou contournement du contrôle d’accès. | ✅ Les deux alias passent de refus à inférence HTTP 200. B obtient aussi une réponse textuelle réelle par le proxy Ollama authentifié. Outils administrateur absents des deux requêtes forcées. |

L’empreinte du texte lu **n’est pas un identifiant de révision Drive**. La version exacte du fournisseur n’étant pas exposée par ce connecteur, nous ne l’inventons pas. Une modification inconnue reste null. La lecture réussie du document cible atteste sa résolution par le connecteur ; une connexion Google dans le navigateur n’a pas été retestée.

Les droits de base rendent également possible l’inférence directe sur ce moteur pour B/C : c’est un effet explicite de cette correction de configuration, pas une délégation limitée au seul alias. Le moteur n’ajoute aucun accès Drive ou outil administrateur. Ces droits existent **uniquement dans la copie**.

## Trois essais réels du client, question inchangée

| Essai | Documents effectivement lus | Cartes sources | Observation critique |
|---|---:|---:|---|
| 1 | 0 | 1 carte générique de l’ancien comportement | Recherche booléenne trop restrictive ; arrêt sur résultat vide. Ajout de la relance et suppression de la promotion des simples recherches en citations. |
| 2 | 3 | 3 cartes documentaires avec provenance | Réseau du 12/11, FusionPBX du 13/11 et Markdown lus. Sépare mieux SIP et appels, mais écrit une consultation « le 13 novembre » alors que le test date du 14, et « 10 à 11 » enregistrés au lieu du nombre précisément attesté. |
| 3, dernier état testé | 1 | 1 carte documentaire avec provenance | Ne lit que le Markdown, sans recouper l’architecture réseau ni le document FusionPBX pourtant découverts. Réponse complète et citation fonctionnelles, synthèse globale insuffisante. Le marqueur textuel « source id » reste peu élégant. |

Voir [mesures des trois essais](preuves/CORRECTIFS_CLIENT_S407.json), [essai 1](REPONSE_CLIENT_CORRECTIFS_ESSAI1.md), [essai 2](REPONSE_CLIENT_CORRECTIFS_ESSAI2.md) et [dernier essai](REPONSE_CLIENT_APRES_CORRECTIFS.md). Chaque réponse est une sortie observée, pas la vérité de référence. Le dernier essai n’a pas été remplacé par le meilleur dans les preuves.

**Arrêt après trois tentatives**, conformément à la limite du plan. L’hypothèse suivante à instruire serait une vérification structurée des sujets/sources effectivement couverts avant clôture de réponse, plutôt qu’un quatrième ajustement de prompt. Ce mécanisme n’est pas implémenté ni déclaré validé ici. Aucun lot 24B n’est lancé pour le contourner.

## Tests et preuves
- **40/40** contrôles applicatifs notes/mémoires/fichiers/vecteurs, partages et révocations : [CORRECTIFS_ACL.json](preuves/CORRECTIFS_ACL.json). Canaris synthétiques en copie seulement.
- **8/8** contrôles de modèles et sessions : [CORRECTIFS_MODELES.json](preuves/CORRECTIFS_MODELES.json). Les requêtes de fumée limitées en tokens prouvent l’accès à l’inférence, pas une réponse métier complète.
- **1/1** réponse textuelle standard positive : [CORRECTIFS_REPONSE_STANDARD.json](preuves/CORRECTIFS_REPONSE_STANDARD.json). Proxy Ollama natif, raisonnement désactivé seulement pour ce contrôle court ; pas un essai frontend standard de bout en bout.
- **12/12** vérifications unitaires de provenance/erreurs/contenu inchangé : [CORRECTIFS_UNITAIRES.json](preuves/CORRECTIFS_UNITAIRES.json). Six groupes de tests autonomes correspondants rejoués avec succès dans [test_provenance.py](correctifs/test_provenance.py) ; ils recouvrent ces vérifications et ne constituent pas douze nouvelles preuves indépendantes.
- **6/6** anciens reçus réels rejoués dans les fonctions exactes du middleware corrigé : [CORRECTIFS_REJEU_ERREURS.json](preuves/CORRECTIFS_REJEU_ERREURS.json). Ce rejeu ne simule pas un nouvel échec Google live.
- **3/3** mutations hors périmètre refusées avant transmission, détails dans [CORRECTIFS_ENVIRONNEMENT.json](preuves/CORRECTIFS_ENVIRONNEMENT.json).
- Jeu fictif : dates d’observation correctement prioritaires sur modification, quantités repérées/SIP séparées, emplacements non inventés, adresses proposées non prises pour réservées, recette complète non déduite d’un appel. Réserve : calcule un écart de cinq unités malgré la consigne de ne pas calculer. [Réponse fictive](REPONSE_DATES_FICTIVES.md), [revue](preuves/CORRECTIFS_REVUE_DATES.json). Un essai préparatoire avec limite de 1 800 tokens avait fini en raisonnement sans réponse ; il ne vaut pas réussite et a été rejoué à 4 096.

Ces tests ne créent ni deuxième identité Google ni révocation Drive réelle. La propagation des ACL fournisseur dans les index, l’autorité entre mémoires, la sauvegarde atomique multi-stores et la qualité sur un corpus général ne sont pas réceptionnées par ce complément.

## Reproduction, livrables et clôture
Le [module](correctifs/provenance24a.py), le [patch middleware](correctifs/middleware.patch), le [patch du connecteur de copie](correctifs/connecteur-copie.patch), les [instructions de synthèse](correctifs/synthese-dates.md) et le [script de configuration de copie](correctifs/apply-copy-config.py) rendent le candidat reviewable. Ce sont des éléments de correctif, **pas une procédure de déploiement production**. Le connecteur patché est l’adaptateur de recette limité à la lecture, pas le service MCPO réel. Son intégration permanente devra être traitée séparément.

Rejeu hors ligne : `python3 correctifs/test_provenance.py` depuis ce répertoire. Pour la recette réelle, reprendre le dispositif privé décrit dans [TESTS_CLIENT_ET_ACL.md](TESTS_CLIENT_ET_ACL.md), restaurer un nouveau snapshot avec comptes fictifs, appliquer le patch uniquement à l’arbre copié, placer le module auprès du garde et dans open_webui/utils, puis appliquer les paramètres à la copie arrêtée. Aucun credential n’est fourni dans ce paquet. L’ancienne limite réseau none, le garde de lecture et les droits applicatifs restent actifs.

Même image native, code de copie modifié explicitement ; l’affirmation antérieure « code inchangé » ne concerne que la baseline du 13 novembre. Code de production inchangé par comparaison SHA-256 du middleware initial et actuel ; conteneur de production toujours actif, même image et même démarrage. [Environnement](preuves/CORRECTIFS_ENVIRONNEMENT.json).

La copie corrective et son relais ont été arrêtés ; les cinq fichiers temporaires d’authentification ont été retirés, ainsi que le déverrouillage SSH local et les comptes de recette exportés. Les snapshots et sorties brutes restent privés. [Clôture](preuves/CORRECTIFS_CLOTURE.json). L’image [CLIENT_ENTETE.jpg](preuves/CLIENT_ENTETE.jpg) montre seulement le titre du client ; elle n’atteste pas le lien à elle seule.

**Deux correctifs ciblés validés en copie, troisième non réceptionné. Production inchangée. Aucune fusion. 24B non lancée.**

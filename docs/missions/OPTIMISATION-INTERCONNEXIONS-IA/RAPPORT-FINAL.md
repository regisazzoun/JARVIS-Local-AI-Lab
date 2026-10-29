# Réception des corrections après audit

**✅🟡 GO avec réserves pour les corrections d'interconnexion.** L'audit initial est conservé dans la [PR31](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/31), commitb29c80f. Le propriétaire a ensuite autorisé ces corrections sans validation intermédiaire. Ce rapport ne reçoit ni l'autonomie générale de JARVIS, ni P4.

## Résultats démontrés

| Correction | Résultat observé | Preuve |
|---|---|---|
| Défaut WebUI27B | Un navigateur neuf ouvre JARVIS — Qwen3.5 27B Qualité | NAVIGATEUR-27B.json |
| Appels d'outils de clarification | Formulaire de choix réellement affiché sur27B, pas un objetJSON textuel dans cet essai | NAVIGATEUR-27B.json |
| Placement explicite |27B/14B/8B surMac ;80B/32B/70B surDell ;un seul index de backend par identifiant | PLACEMENT-MODELES.json |
| API conversationnelle | Le même chemin sansallowed_tools qui échouait503 répond maintenant BONJOUR ;Qwen27B, Mac,16384tokens | API-CONVERSATION-APRES.json |
| Admission commune surDell1 | AppelsWebUI natifs etCodeOpenAI inscrits dans ComputeQueue existante ;vrais appels80B effectués | ADMISSION-REELLE.json, ADMISSION-CANONIQUE.json |
| Entrées trop grandes / concurrence | Refus avant dispatch, limites32768/4096/27648octets, priorité et bail conservés | Tests HTTP + reçus |
| Création depuisWebUI | Vrai identifiant27fc9d276ccc435bb32fcfeaeee2969c reçu par le navigateur, puis worker80B actif | CREATION-MISSION-REELLE.json, SONDE-MOTEUR.json |
| Données et modèles |12conversations antérieures identiques ;16avec les essais ;les trois catalogues de poids inchangés | VERIFICATION-INDEPENDANTE.json |
| Services et pauseP4 | Services centraux actifs ;P4 toujoursinterrupted/version0 ;MANUAL-HOLDprésent | VERIFICATION-INDEPENDANTE.json |

Deux inférences réelles concurrentes sur le garde ont ensuite répondu200 en6,502s et6,611s. La deuxième attend donc plus de deux secondes sans l’ancien429 ;l’énumération de charge limitée n’est pas présentée comme une réponse sémantiquement complète. [Preuve de concurrence](CONCURRENCE-REELLE.json).

**17tests logiciels ciblés passent** :5pour le vrai handlerconversation/création,5pour le garde/admission et7régressions existantes. Ces résultats sont distincts des inférences réelles et des validations historiquesP2/P3 ;aucune addition avec les anciennes campagnes.

## Ce qui a échoué, sans réécriture des faits

1. Le premier test de partage de file employait un délai WebUI2s. Plusieurs appels80B concurrents ont provoqué429. Le délai est corrigé à30s maximum, avec priorité entre les tours et erreurJSON exploitable. Les appelsCode gardent120s maximum. Aucun calcul engagé n'est préempté et aucune attente infinie n'est introduite.
2. Le profilCode multifonctions a consulté `jarvis_missions` au lieu de créer une mission, puis annoncé un faux identifiant et confondu nombre de missions et services. Il n'a pas créé de mission. Le contrat distingue désormais lecturecreated=false et créationcreated=true avecID32hex ;le profil explicite **Missions canoniques** n'expose que la création. Le contratHTTP `request_kind=mission` empêche l'API de reclasser l'objectif d'observation en simple question d'état.
3. La sonde créée a bien démarré dans le moteur existant, sous80B/Dell1, mais a rencontré trois refus de plan :88715,88740,88758. Le premier concerne une preuve de service mal définie ;les suivants contiennent duJSON syntaxiquement incomplet. Le parseur existant sait déjà décoder des conteneursJSON valides :inventer les champs manquants aurait écrit un plan à la place du modèle. Après diagnostic et cadrage des outils existants, l'essai est arrêté et classé**incomplete**, avec les compteurs et refus conservés. **Création/démarrage reçus ;rapport de mission non reçu.** Ce résultat ne relève pas la réceptionP4.
4. Le contrôle Qwen Code en lecture seule a atteint12tours/code53 en répétant des tests déjàPASS. Son admission fonctionne, sa finalisation générale demeure fragile. Le correctif neuf de l'audit avait terminé/code0 en32,889s avec3testsPASS ;ces deux résultats restent distincts.

## Attribution et limites

Codex développe et déploie les modifications de transport, configuration, admission et contrat. Les modèles choisissent leurs appels et leurs plans ;les mauvais choix restent dans les preuves. La nouvelle mission a été réellement créée par l'appel du modèleWebUI ;sa clôtureincomplete est une décision de contrôleCodex après trois refus, pas une réussite déclarée parJARVIS.

Aucun poids, pilote ou système n'est installé, déplacé ou supprimé. Aucun serviceOllama n'est redémarré. Dell2 reste un exécuteurSSH3090+3080, sans inférenceLLM installée ;une nouvelle copie de modèle n'était pas nécessaire pour corriger les flux constatés. JL03 et le prototype23D restent indépendants. L'accèsHTTPS précédemment reçu est conservé.

Les anciens échangesWebUI peuvent garder8B ;le défaut27B s'applique aux nouvelles sélections. Les messagesJSON historiques ne sont ni effacés ni exécutés arbitrairement. La gestion de profils reste disponible ;le port d'inférence ne publie pas les opérations de téléchargement/suppression de poids, qui restent des opérations d'administration distinctes.

Les limites restantes sont explicites :planification/finalisation du moteur, finalisationCode, admission des autres consommateurs historiques éventuels de11434, inférenceDell2, Safari/iPhone, microphone physique et rebootglobal. Elles ne nécessitent pas de réinstaller les composants déjà fonctionnels. [Utilisation et retour arrière](REPRISE-ET-RETOUR-ARRIERE.md), [réalisation](REALISATION.md).

Publication : [PR32](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/32), empilée sur laPR31 documentaire ;implémentation initiale3eb47eb, preuves et clarifications dans les commits suivants. Aucune fusion automatique.

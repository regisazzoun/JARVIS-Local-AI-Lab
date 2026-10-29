# Corrections après audit — 29 octobre 2026

Autorisation explicite du propriétaire : appliquer les modifications et connexions nécessaires après établissement du bilan, sans validation intermédiaire. Le constat initial est figé au commitb29c80f, [PR31](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/31). La présente réalisation est distincte ; elle n'efface aucun défaut historique.

## Changements installés

| Sujet | Avant | Après |
|---|---|---|
| Défaut Open WebUI | Llama3.1:8b | Qwen3.5:27b-q4_K_M ; les anciennes conversations et le profil8B restent disponibles |
| Placement des modèles | Choix aléatoire Mac/Dell pour les identifiants dupliqués | CatalogueMac :27B/14B/8B ; catalogueDell :80B/32B/70B ; chaque identifiant n'a qu'un backend |
| Appels Dell WebUI/Code | Inférences directes hors admission JARVIS | Passage par le garde8091 et **ComputeQueue existante**, dans missions.sqlite |
| Priorités | Files indépendantes au niveau applicatif | Appels natifs WebUI prioritaires entre tours ; Qwen Code en mission ; aucun calcul engagé préempté |
| Attente WebUI80B | Premier essai2s provoquant429 sous concurrence | Attente bornée30s ; priorité conservée, pas d'attente infinie |
| Fenêtres | APIchat complète élargissant au-delà du profilMac | API conversation bornée aux12outils déjà utilisés parJL03 ;16384tokens Mac inchangés |
| Contrat de création | Texte d'état pouvant être interprété comme question ; réponse sansID | `request_kind=mission` surPOST authentifié ; l'adaptateur exige un vrai identifiant32hex |
| Lecture/création | Un outil multifonctions favorisait une confusion du modèle | Reçu de lecture marquécreated=false ; reçu de créationcreated=true ; profil distinct **JARVIS — Missions canoniques** avec un seul outil de création |
| Retour d'erreur du garde | HTML générique | JSON compatible, cause explicite etRetry-After sur429 |

Les filtres sont persistants dans le compose existant. Le profil27B utilise le mode natif d'appels d'outils, think=false et16384 de contexte. La session neuve affiche le formulaire de choix ; les anciens messagesJSON restent intacts. Aucun contenu historique n'est exécuté arbitrairement comme un outil.

Le garde existant est étendu, pas remplacé par un second ordonnanceur. Il importe la traduction OpenAI→Ollama native déjà reçue pour Qwen Code et réutilise ComputeQueue. Le chemin natif Open WebUI est transféré vers le même OllamaDell1:11435 avec32768 de contexte maximum et4096 de réponse. Au-delà de27648octets d'entrée, refus avant inférence. Les endpoints de modification/téléchargement de poids ne sont pas exposés par ce port d'inférence ; l'administration des poids reste distincte des profils de conversation.

La file interne Ollama et la file canonique ont des fonctions différentes : Ollama sérialise son runner ; ComputeQueue donne priorités et baux aux consommateurs. Aucune seconde base ni mémoire canonique concurrente n'est créée. Le routage principal JARVIS et les affectations27B/80B sont conservés.

## Fichiers et activation

- Backend canonique : `server.py` et nouveau `conversation_tools.py`. Le journal de diagnostic503 déjà installé est conservé. Core, compute.py et les fichiers non commités deM26-P4 ne sont pas réinstallés depuis un ancien checkout.
- Garde : `tools/optimisation_interconnexions/inference_gateway.py`, sur le même port8091 et la même unitéjarvis-qwen-guard.
- Adaptateur : `webui_adapter.py`, même unitéjarvis-webui-tools et port8092 ; mêmes accès aux voix et à la mémoire.
- Interface : filtres de fournisseurs, défaut27B et deux profils spécialisésCode/Missions. Aucun poids supplémentaire pour ces profils.
- Le nouveau profilMissions utilise27B/Mac pour transmettre la demande ; le moteur canonique utilise80B/Dell1 pour la traiter. Il ne lance pas automatiquement Qwen Code.

Les redémarrages ont été précédés de contrôles d'inactivité et de sauvegardes privées. Le conteneurWebUI est recréé avec son image/volume existants. Conversation et nouvelles intégrations sont rechargées ; workers, Ollama, LiveKit et services desDell ne sont pas réinstallés ou arrêtés pour cette réalisation.

## Résultats et limites

Dix nouveaux contrôles logiciels portent sur le vrai handlerHTTP, la restriction par défaut, la conservation des autorisations explicites, la création canonique et l'admission. Avec sept régressions ciblées réutilisées, **17tests passent**. Ils ne remplacent pas les requêtes réelles et ne requalifient pas les dix scénariosP2.

Le chemin API qui renvoyait503 répond maintenant réellement BONJOUR sur Qwen27B/Mac, contexte16384, sansrestriction fournie par le client. Les appels de garde natifs renvoient une vraie réponse80B. Les requêtesCode etWebUI apparaissent dans la même tablecompute_jobs avec leurs rôles et identifiants. Les preuves d'inférence ne sont pas des validations sémantiques de fichiers.

Le contrôle Qwen Code en lecture seule a encore atteint la limite12tours/code53 en répétant des testsPASS. Ce défaut de finalisation reste explicitement ouvert ; son trafic a bien utilisé l'admission commune. Le nouveau correctif de programmation réalisé pendant l'audit avait, lui, terminé/code0 avec3testsPASS. Ces deux résultats ne sont pas confondus.

Le premier lancement de mission par le profilCode a échoué : un essai429, puis le modèle a appelé la lecture et présenté un faux identifiant. Après correction du contrat et profil spécialisé, le navigateur obtient le vrai reçu du moteur : **27fc9d276ccc435bb32fcfeaeee2969c**, étatqueued à la création. Le worker utilise ensuite80B/Dell1. La réception du lancement ne déclare pas la mission terminée. Après trois refus de plan88715/88740/88758, la sonde est classéeincomplete : création et démarrage reçus, exécution/rapport non reçus. Les détails et interventions sont dans SONDE-MOTEUR.json.

## Conservation et périmètre

M26-P4 reste interrupted, MANUAL-HOLD et compteurs historiques conservés. Aucun14A/24-Old ou ancien chantier n'est repris. Les catalogues sont comparés avant/après ; aucun téléchargement, déplacement ou retrait de modèle. Dell2 reste exécuteurSSH et ne devient pas par simple configuration un serveur d'inférence. Son matériel3090+3080 est conservé, sans nouvelle installation injustifiée.

Les fonctions manquantes ou fragiles du Mission Engine et de la finalisation Qwen ne sont pas déclarées corrigées par un changement de fournisseur WebUI. La distribution d'inférences surDell2, Safari/iPhone, le microphone physique et un reboot global restent hors des preuves actuelles.

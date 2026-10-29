# Réception — Qwen Code / Open WebUI / Apache / Tailscale

## Actualisation du 29 octobre 2026 — réserve HTTPS levée

**✅🟡 GO avec réserves.** Le propriétaire signale HTTPS fonctionnel. Codex vérifie
ensuite HTTP200 et validation TLS0, sans ignorer les certificats, sur le Mac et
réellement depuis Dell1. Chromium ouvre l'interface avec les contrôles de certificat
normaux : `isSecureContext=true`, API `mediaDevices` disponible. Accès actuel :
**https://jarvis-macmini.tail805e83.ts.net/**, privé au tailnet.
[Preuves indépendantes](HTTPS-RECEPTION.json).

L'activation HTTPS est constatée après intervention extérieure ; elle n'est pas
attribuée à Codex. Aucune configuration ni aucun service n'est modifié par cette
levée de réserve. Les accès HTTP existants restent présents. Le microphone physique,
Safari/iPhone, le reboot complet et les limites de finalisation Qwen Code restent
les réserves déjà documentées. La disponibilité de l'API micro ne prouve pas une
capture acoustique. M26-P4 reste en pause ; aucune fusion automatique.

## Instantané initial conservé — avant activation HTTPS

Le texte ci-dessous conserve la réception initiale et ses réserves à cette date ;
les mentions «HTTPS bloqué/non reçu» sont désormais historiques et remplacées
uniquement pour ce critère par l'actualisation ci-dessus.

**29 octobre2026 — 🟡 INCOMPLET : fonctions locales et accès tailnet HTTP démontrés ; HTTPS et microphone distant non reçus.** Le blocage restant dépend de l'activation HTTPS/Serve dans le compte Tailscale existant. L'installation n'attend aucune nouvelle approbation de mission ; le client réclame une action administrateur externe dont Codex n'a pas la session authentifiée. Aucun certificat accepté n'est inventé.

## Résultats livrés

| Contrôle | Résultat réellement obtenu |
|---|---|
| Open WebUI existant |0.12.0, compte existant, login réel Chromium, conversation80B réelle |
| Conservation des données |1compte conservé ;9conversations originales strictement identiques par empreinte ;10après ajout de l'essai |
| Apache2.4.69 |Reverse proxy loopback8088→conteneur3000 ;HTTP200 et réponses applicatives |
| WebSocket / streaming |Upgrade101 ;119événements SSE, premier0,326s, dernier2,394s dans cet essai ciblé |
| Accès Tailscale1.104.2 |HTTP privé accessible réellement depuis Dell1 ;pas de Funnel ni port Apache public |
| HTTPS / Safari / iPhone |NON REÇUS : HTTPS non activé dans le compte ;aucun essai physique Apple |
| Voix |Whisper/Piper canoniques raccordés ;MP3 Open WebUI lisible, retranscrit «Bonjour, le test vocal jarvis est opérationnel.» ;microphone physique non testé |
| Qwen Code |0.26.4, Node22.23.4 isolé ;Node20.19.2 système conservé |
| Modèle |`qwen3-coder-next:q4_K_M`,79,7B/Q4_K_M existant, Dell1 Ollama0.40.3 port11435 ;aucun poids téléchargé |
| Correction réelle |Source lue, tests exécutés :2FAIL/1PASS avant ;suppression du `+1` erroné dans prices.py ;3PASS après, test inchangé |
| Contrôle indépendant |Codex relance3testsPASS, compare diff et fichiers ;commit de fixture3ba9210 créé par Codex pour enregistrer le correctif Qwen |
| Déclenchement Open WebUI |Profil expérimental et outil installés ;conversation navigateur appelle réellement Qwen Code ;résultats des3tests affichés et conservés |
| Persistance |Nouvelles unités redémarrées, conteneur existant recréé ;données/profil/outils/réglages vocaux conservés ;unités activées au démarrage |
| Non-régression |Conversation JARVIS, broker, JL03 et workers actifs ;santé canoniqueOK ;aucun remplacement du moteur ni reprise M26-P4 |

[Preuves Qwen](QWEN-CODE-PREUVES.json), [intégration navigateur](OPENWEBUI-INTEGRATION-PREUVES.json), [transport](TRANSPORT-NAVIGATEUR.json), [voix/données/persistance](TESTS-HTTP-VOIX-PERSISTANCE.json), [services](ETAT-SERVICES.json), [Ollama/GPU](OLLAMA-GPU.json), [incidents](INCIDENTS.json).

## Modèle et ressources observées

Le garde d'entrée refuse les requêtes dépassant27648octets avant inférence. Cette borne conservatrice n'est pas un comptage exact en tokens. La traduction OpenAI→API native impose32768tokens de contexte et4096maximum de réponse. Le premier essai avec les outils implicites complets est refusé à46793octets ;la réduction partielle reste trop grosse à38740. Le profil explicite minimal corrige la cause, sans relever la limite. Les anciens refus et l'erreur d'authentification préalable du mode bare sont conservés.

Le point de départ Open WebUI historique visait11434 du Dell. Le vrai endpoint de missions déjà installé est11435 :le branchement a été corrigé après observation d'un runner CPU4096 sur11434. Ce runner temporaire est libéré ;aucun service Ollama n'est arrêté ou reconfiguré. Le modèle existant sur11435 est observé avec32768tokens et47695517447octets de résidenceGPU. Instantané des cartes :23285 et23092Mio occupés ;charge0% à cet instant après les calculs, pas une absence d'exécution. Ces mesures partagées ne prouvent pas une allocation exclusive de chaque octet à cet essai.

La correction autonome de la petite fixture prend14,620s,5tours, avec choix de lecture/édition/test par Qwen Code. Ceci n'est pas une comparaison générale de performance avec JARVIS. L'essai navigateur comporte d'abord un appel arrêté à12tours/code53 malgré des testsPASS, puis un appel réussi/code0 en4,98s. Les erreurs `python` absent puis pytest absent et la limite de tours restent dans les reçus ;le premier appel n'est pas renommé en réussite complète.

Un contrôle final du wrapper a de nouveau atteint12tours/code53 après répétition de tests déjàPASS. Codex a corrigé sa consigne de démarrage :périmètre limité à la demande, environnement Python explicite et restitution immédiate dès critères satisfaits. Le nouvel essai Qwen Code termine réellement/code0 en11,122s et3tours, avec une seule exécution des3tests, puis un `echo` inutile et son rapport. L’echo n’est pas une preuve ;la sortie unittest l’est. [Deux traces et rectification](FINALISATION-QWEN.json). Cette amélioration ciblée ne reçoit pas une garantie générale d’absence de répétitions.

## Attribution et comparaison

**Codex** inventorie, installe Apache/Node/Qwen Code, développe garde et adaptateur, configure le profil/outils/audio, prépare le défaut et ses tests, conduit les contrôles navigateur/API/distants, enregistre le commit et publie. **Qwen Code avec le80B Dell1** lit les sources, choisit les commandes, modifie le vrai fichier Python puis interprète ses tests. Le modèle de conversation Open WebUI choisit ses appels d'outils. **JARVIS existant** fournit effectivement son API de missions, son authentification, Whisper et Piper ;aucune nouvelle mission autonome du Mission Engine n'est reçue par cette campagne. Ne pas attribuer les développements d'infrastructure Codex à JARVIS.

Qwen Code est exploitable pour un petit projet de programmation avec outils réels et traces. Son lancement court est plus direct que les parcours de mission historiques, mais ses limites de tours, ses essais de commandes incorrectes et sa dépendance à l'adaptateur empêchent d'en déduire une supériorité générale. Il n'apporte pas à lui seul les checkpoints, la vérification sémantique, la distribution sur deux Dell ni la réception du code déployé de JARVIS. Les commandes de cet essai s'exécutent sur le Mac dans un projet dédié :ce périmètre expérimental explicite ne réceptionne pas les exécuteurs Dell de M26.

Open WebUI peut servir d'interface complémentaire quotidienne de conversation/voix/outils. Un remplacement complet de JL03 n'est pas recommandé sur ces seules preuves :la télémétrie, l'orbe, le flux détaillé des missions et les contrôles de reprise de JL03 ne sont pas remplacés par ce connecteur. Sa mémoire canonique reste celle de JARVIS.

## Réserves et suite exacte

1. Activer HTTPS/Serve dans l'administration Tailscale existante, puis exécuter le script de mise en service HTTPS. L'URL cible est préparée mais non accessible en HTTPS actuellement. Le microphone d'un navigateur distant sur HTTP n'est pas reçu.
2. Essayer Safari/MacBook/iPhone et les microphones physiques ;la transcription de test est issue d'une voix synthétique, pas d'un micro utilisateur.
3. Aucun reboot complet de Debian ni redémarrage de tailscaled :la persistance reçue concerne les composants contrôlés et leur activation systemd, pas un essai physique après coupure.
4. L'accès distant depuis Dell2 a expiré ;Dell1 fonctionne. Ne pas convertir ce timeout en panne générale du tailnet ni en preuve de fonctionnement de tous les clients.
5. L'outil de soumission de nouvelles missions canoniques est raccordé mais n'a pas déclenché de mission supplémentaire pendant cette campagne ;consultation et programmation sont utilisées réellement. Le garde des3corrections du Mission Engine n'est pas requalifié par Qwen Code.
6. L'adaptateur est expérimental et mono-appel, avec droits du compte existant et journaux privés ;ne pas le présenter comme un service multi-utilisateurs à isolation forte ou une file durable de missions. En cas de réponse perdue, vérifier le reçu et Git avant toute relance.

[Installation et accès](INSTALLATION-UTILISATION.md) · [architecture et schéma](ARCHITECTURE.md). Branche dédiée et PR sans fusion automatique. M26-P4 reste interrompue à la demande du propriétaire ;14A/24-Old et les autres chantiers ne sont pas relancés.

Références primaires utilisées : [Qwen Code providers](https://github.com/QwenLM/qwen-code/blob/main/docs/users/configuration/model-providers.md), [paramètres Qwen Code](https://github.com/QwenLM/qwen-code/blob/main/docs/users/configuration/settings.md), [outils Open WebUI](https://docs.openwebui.com/features/extensibility/plugin/tools/), [proxy/connexion Open WebUI](https://docs.openwebui.com/troubleshooting/connection-error/), [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve), [Apache WebSocket proxy](https://httpd.apache.org/docs/2.4/mod/mod_proxy_wstunnel.html). Les sources de la version effectivement installée ont également été contrôlées.

Publication : [PR30](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/30), base895e331 ;première livraison787075d, ajustement final et preuves dans les commits suivants de cette même PR. Aucune fusion.

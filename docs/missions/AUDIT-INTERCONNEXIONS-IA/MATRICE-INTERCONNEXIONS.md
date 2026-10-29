# Matrice des flux réellement constatés

V=validé par test cité ;C=configuré sans réception bout en bout actuelle ;A=absent/envisagé. «Historique» conserve la date/périmètre de réception, sans nouvel essai fictif.

| ID | Source | Destination | Protocole | Fonction | État | Preuve |
|---|---|---|---|---|---|---|
|F01|Chromium audit / Dell1|TailscaleMac443|HTTPS/TLS|Accès privé|V|RéceptionHTTPS QWEN-WEBUI + navigateur neuf sécurisé |
|F02|MacBook/iPhone|MêmeURL|HTTPS/Tailscale|Accès utilisateur|C|Signalement propriétaire HTTPS ;pas de test physique Apple attribué àCodex |
|F03|TailscaleServe|Apache8088|HTTP loopback|TerminaisonTLS/proxy|V|Serve configuré, certificat0 et API200 |
|F04|Apache8088|WebUI3000|HTTP,WebSocket,SSE|Proxy applicatif|V|VHost lu ;WS101/SSE119événements reçus précédemment |
|F05|WebUI|OllamaMac11434|HTTP /api/chat|8B/27B/14B|V|Catalogueurls[0,1],8B chargé et formulaire neuf |
|F06|WebUI|OllamaDell1:11435|HTTP /api/chat|Catalogue partagé/80B|V|8B chargé pendantclarification ;profilCode historique |
|F07|WebUI outilqwen_code|Adaptateur8092|HTTPBearer|Appel spécialiste|V historique +Cactuel|Reçus navigateur précédents ;outil/sourceactuels ;CLI neuve reçue |
|F08|Adaptateur8092|QwenCodeMac|Subprocess/Git|Lecture/édition/test|V|Source actuelle ;projetneufE04 viawrapper |
|F09|QwenCode|Garde8091|HTTP OpenAIcompatible|Inférence limitée|V|Session réelle, requêtes/tailles archivées |
|F10|Garde8091|OllamaDell1:11435|HTTP natif /api/chat|80B32768|V|E04/E03 et sourceguard |
|F11|WebUI jarvis_missions|APIJARVIS8765|HTTP via8092|Consultation missions|V|Réponse réelle51missions |
|F12|WebUI jarvis_task|MissionEngine|HTTPPOST /api/missions|Création mission|C|Outil/source raccordés ;aucune nouvellemission soumise pendant l'audit |
|F13|WebUIaudio|Whisper/PiperJARVIS|HTTP compatible via8092|STT/TTS|V historique +Cactuel|Réceptionvoix et config moteurs actifs ;pas de microphysique |
|F14|JL03:8766|JARVIS:8765|HTTP session|Conversation et missions|V|PageJL03 identifiée ;conversationQwen27 actuelle200 |
|F15|Prototype23D:8783|LiveKit7880/agent|HTTP/WebSocket|Voixprototype|V historique|Réception23D ;aucun nouveau test acoustique |
|F16|JARVIS/Engine|MémoireSQLiteFTS5 / missionsSQLite|SQLite local|Mémoire/événements/plans|V|Bases lues et API conversation/preferences ;événementsE05 |
|F17|JARVISconversation|OllamaMac11434|HTTPviaHybridRouter|Qwen27|V avec outils limités ;FAILsansrestriction|E10/E12 ;503/E09 sansallowed_tools |
|F18|MissionEngine|OllamaDell1:11435|HTTPviaHybridRouter|Décision80B|V historique|26-P1 etP3 ;routageactuel identique |
|F19|MissionEngine|Brokerhôte|SocketUnix /run/jarvis-host/bridge.sock|Actionsautorisées|V historique ;socketactuel|Sourcebridge, socketécouté, reçus26 |
|F20|BrokerMac|Dell1 / Dell2|SSH22 ;AnsibleauMac|Exécutiondistante|V historique +SSH actuelCodex|E05 et inventaireE01 |
|F21|QwenCode|MissionEngine|Aucunadaptateurworker|Checkpoint/délégation|A|Les outilsWebUI distincts ne créent pas ce lien |
|F22|QwenCode|Dell2exécuteur|SSH possible sans profilagentconfiguré|Répartitionautomatique|A|Shellcapable, maisaucunMCP/workerDellspécifique branché |
|F23|HybridRouter|OllamaDell2|URLabsente|Inférencedistribuée|A|enabled=false,url=null ;serviceabsent |
|F24|OpenWebUI|HistoriquepropreWebUI|SQLitevolumeDocker|ConversationsWebUI|V|Profils/messagesinterrogés ;distinct mémoirecanonique |
|F25|QwenCode|SessionsQwen|Fichierslocaux|Traces/sessiondéveloppement|V|JSONL/sessionréels ;non importésautomatiquementenmémoireJARVIS |
|F26|OllamaMac / Dell1missions|GPU Mac / deuxGPU Dell1|CUDA|CalculIA|V|Inférencesneuves et mémoireGPU relevée |
|F27|OllamaDell2absent|GPU3090/3080Dell2|CUDAenvisagé|CalculLLM|A|GPUprésents maisaucuneinférence actuelle |

**Correction de cartographie importante :**8766 estJL03 ;8783 estleprototype vocal23D. Le brokerhôte utilise un socketUnix et non ces deux ports. UnHTTP200 sur8783 ne réceptionne pasJL03. Les deux servicesont été identifiés parPID, ExecStart, titreHTML etsources pendant cet audit.

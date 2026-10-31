# Tests ciblés et niveaux de réception

Code1abd51d. **20tests logiciels PASS** :15nouveaux (profils, confinement, permissions, pagination, erreurs/timeout, promotion avant écriture et callbackOAuth) et5tests ciblés du clientGoogle historique. Les93tests/cinqcontrôles de PR35 n’ont pas été relancés. Les mocks logiciels ne sont pas des opérations Google réelles.

| Cas | Observation réelle | Réception |
|---|---|---|
| MCP amont sur personal/education | InitialisationSDK stdio, serveur google-workspace-server0.0.8, protocole2025-11-25, catalogue30outils autorisés | ✅ installation et contrats |
| Deux méthodes Sheets additionnelles | Schémas réellement retournés ; appel sans OAuth refusé avant dispatch ; catalogue total32 | ✅ préparation ; 🟡 API distante non reçue |
| MCP JARVIS → MCP Google | Appel time.getCurrentDate au travers du MCP canonique enrichi | ✅ protocole ; ce calcul local ne prouve pas Drive/Gmail |
| Appel Google sans jeton | Refus réel amont « No browser available for authentication » sur chaque profil ; façade renvoie AUTH_REQUIRED sans requêteAPI | ✅ refus correct ; aucune authentification simulée |
| OAuth applicatif fourni | Chromium sans compte ouvre Sign in - Google Accounts, intitulé Gemini CLI Workspace Extension ; aucun invalid_client/invalid_scope/redirect_uri_mismatch visible avant login | ✅🟡 prélogin uniquement ; ni consentement ni token reçu |
| Open WebUI → modèle27B | NavigationHTTPS authentifiée, catalogue/schéma, trois appels réels (deuxstatuts et date locale) et réponse affichée | ✅ raccordement et résultat modèle ; 🟡 donnéesGoogle absentes |
| Qwen Code → modèle80B Dell1 | Session réelle6tours,63552ms ; catalogue/schéma et trois appelsMCP, réponsefrançaiseAUTH_REQUIRED | ✅ raccordement ; aucunGoal ni modèle changé |
| MoteurJARVIS → google_mcp | Septstatuts réellement exécutés,4personal/3education, résultats renvoyés au modèle | ✅ appel natif ; 🟡 planification/rapport autonome non reçus |
| Isolation des profils | Dossiers700, clés locales600, inodes distincts ; aucun jeton dans les deuxprofils | ✅ séparation préparée ; 🟡 renouvellement/auth persistante non reçus |
| Services | Conversation, deuxworkers, adaptateur, garde, Apache et Tailscale actifs après recharge ciblée | ✅ conservation au contrôle ; aucunrebootglobal |

## Sonde native et intervention Codex

Mission0cd10730c6b841839c5d62b4fef32359, dans le moteur et la base existants. Le premier plan du modèle inventait des noms de fichiers OAuth et omettait l’appel google_mcp. Le modèle a écrit un brouillon refusé. Codex a interrompu cette stratégie et fourni explicitement le plan de réception d’interface version2, auteurCodex, avec nouvelle destination de rapport. Le plan1, ses fichiers, erreurs et vérifications restent historiques.

JARVIS a ensuite appelé réellement le connecteur pour les deuxprofils. Il a répété les statuts sans progresser vers son rapport ; Codex a interrompu la sonde, événement94552. Les septlectures sont des succès techniques de statut, pas septéchecs de correction. Aucun compteur n’est remis à zéro. **L’appel moteur est prouvé ; aucune clôture autonome ou fiabilité générale du rapport n’est reçue.** Cette mission ne modifie pas l’architecture ou le statut de M26P2/P3/P4.

## Rectification de restitution

La réponse WebUI initiale disait d’exécuter la commande «dans un navigateur». C’est incorrect : la commande va dans Terminal, puis seulement l’URL affichée dans le navigateur. L’original reste privé avec son empreinte ; le guide et les champs structurés setup_execution_location/browser_step portent la correction. Les étatsAUTH_REQUIRED et la distinction entre heure locale et donnéeGoogle étaient correctement rapportés.

## Réception après authentification — en attente

Pour chaque compte : statutOAuth, rechercheDrive, lecture d’un document autorisé, création d’un document d’essai, relecture exacte ; lectureCalendar, lectureSheets, création/écriture/lectureSheets, lectureGmail et brouillon si pertinent. Répéter des opérationsGoogle réelles depuis WebUI et Code, puis contrôler après redémarrage du service concerné. Aucun de ces essais distants n’est déclaré réussi avant authentification.

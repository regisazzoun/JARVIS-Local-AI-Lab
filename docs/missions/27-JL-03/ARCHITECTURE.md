# Architecture installée

## Un seul JARVIS canonique

Le nouveau service `jarvis-launcher3.service` sert `/var/lib/jarvis/projects/jl03/site` sur127.0.0.1:8766. L'adaptateur Python relaie les requêtes authentifiées vers la passerelle existante8765. Même cookie, même mémoire SQLite/FTS5, même moteur de missions et checkpoints. Aucun autre CoreLLM, worker ou magasin de messages n'est créé. Titres et projetsV3 sont deux tables de métadonnées ajoutées à la base mémoire existante.

Les échanges ordinaires sélectionnent un petit ensemble d'outils existants, au lieu du catalogue intégral qui dépassait le profil de contexte Mac16K. Les directives d'exécution explicites reconnues par `jarvis.intent.classify` deviennent des missions du moteur canonique avec origineV3. Le bouton Mission conserve l'accès explicite au moteur. Les outils opérationnels complets restent disponibles dans ce moteur. Le routage27B Mac/80B Dell n'est pas remplacé. Un résultat de mission est associé à son identifiant et à la conversation canonique.

## Composants

- `api.js` : transport de session, erreurs, BlobSTT et WAVTTS.
- `app.js` : interface initialement JARVIS, intégration API/états/navigation par Codex.
- `orb.js` : base JARVIS ; rendu, spectre, géométrie, pistes et ressources corrigés par Codex.
- `voice.js` : pipeline JARVIS repris et intégré par Codex après échecs ; segmentation/VAD, STTsérialisé, TTSet interruption locale.
- `livekit.js` : intégration Codex du serveur/agent23D existant, SDKofficiel2.23.0.
- `console.js` : base JARVIS ; pagination/cycle de polling/syntaxe et intégration corrigés par Codex.
- `telemetry.js` : rendererJARVIS ; dates, slots absents et intégration corrigés par Codex.
- `backend/loop_guard.py` : observateur coopératif des reçus existants, pas un nouveau moteur.

## Flux et télémétrie

`/api/v3/events` lit le journal canonique,100 événements par page, sans troncature ajoutée des arguments/sorties. Les secrets identifiés sont masqués ; une sortie déjà tronquée en amont ne peut pas être reconstituée et conserve ses indicateurs. Attribution et horodatages viennent du journal. Tous les événements disponibles restent ouverts ; seuls les raisonnements internes non exposés sont absents.

L'API de ressourcesJL-02 est réutilisée et enrichie par une sonde locale et la commande distante fixe `telemetry_v3`, ajoutée au profil `dell-observe` existant. TousGPU détectés, CPU/RAM et températures disponibles. Dell2 reste indisponible, avec deux emplacements non peuplés. Aucun nouveau serveur installé ni profil énergétique changé.

## Session et déploiement

Connexion web canonique réutilisée surlocalhost ; aucun mot de passe dans le client. Host/Origin et en-tête de mutation contrôlés. Service lié au loopback, accès distant par tunnel. CSPsansunsafe-eval ; Three.js MIT et LiveKit Apache2.0 fournis localement avec leurs licences. Les références Neort n'ont pas été accessibles pendant cette exécution et aucun code artistique n'a été copié.

Seul le serviceV3 est redémarré pendant l'intégration. Conversation, broker, workers et LiveKitexistants restent actifs. Arrêter V3 ne supprime ni messages ni missions ; son observateur anti-boucle n'est cependant plus actif lorsque V3 est arrêtée.

# Rapport final t13 — Mission 23 LiveKit

**Mission originale :** `7971ec0311124fb4be9e3125dcb291fd`  
**État au 20 octobre 2026 :** **❌ NO-GO pour la réception finale — chaîne partielle, t13 bloquée**  
**Tâches :** t01 à t12 restent validées selon leur historique; t13 est rouverte et bloquée par les critères de réception vocale qui échouent ou restent non testés. La mission n’est pas clôturée.

## Verdict vérifié

Un client WebRTC automatisé a rejoint une salle LiveKit, envoyé un fichier WAV français, reçu sa transcription, puis des trames PCM Piper distantes non silencieuses. Cela prouve un aller-retour vocal automatisé sur le Mac mini. Cela ne prouve ni l’interruption d’une réponse en cours, ni la reconnexion, ni un appel depuis un autre nœud Tailscale, ni une réception au microphone/haut-parleur physique. L’interruption est exigée par l’objectif de conversation et ne peut être déclarée non bloquante ici : le verdict final demeure **❌ NO-GO**.

## SIGKILL : cause établie

Les receipts historiques des appels `verify_livekit_voice.py` montrent `returncode=-9`, `timeout=true` et environ 60 secondes d’exécution. L’implémentation de `host_bridge.py` termine explicitement le groupe de processus avec `SIGKILL` quand son délai `host_exec` expire. Ces `-9` sont donc des expirations de la passerelle, pas une preuve d’un kill OOM du noyau.

Les éléments contrôlés concordent : `memory.events` du cgroup de l’agent indique `oom=0`, `oom_kill=0`, `oom_group_kill=0`; aucune limite `MemoryMax` active; environ 27–29 GiB disponibles sur l’hôte pendant les prélèvements. LiveKit a émis un avertissement PSS au-dessus de 1 000 MiB, explicitement consultatif, sans limite de mémoire configurée. Les premières sorties en erreur des workers comprenaient aussi un import d’API absent et une construction `Agent` sans `instructions`, qui étaient des défauts applicatifs distincts et ont été corrigés. Le mélange multiprocessing/Bubblewrap et un OOM ne sont pas établis comme cause des `-9` historiques.

La passerelle a reçu une option de délai explicite bornée à 300 secondes pour permettre ces essais longs. L’agent utilise maintenant les API installées de LiveKit Agents 1.8.8; le service enregistre le worker `jarvis-agent`.

## Réception et mesures

Le condensé vérifiable des résultats Codex, avec références d’évidence et empreintes SHA-256 des preuves détaillées, est conservé dans `RECEPTION-RESULTATS-CODEX.json`. Il exclut les trames brutes du rapport de synthèse.

- **WebRTC / WAV / STT / LLM / TTS / retour audio, essai indépendant Codex :** réussi dans `RECEPTION-WEBRTC-CODEX.json`. Durée WAV 3,564 s; transcription française reçue à 7,677 s depuis le début; premier PCM distant non silencieux à 83,126 s; fin d’entrée → premier son : **78,459 s**. Microphone physique : non.
- **WebRTC indépendant relancé par JARVIS :** reçu et vérifié dans `RECEPTION-WEBRTC-INDEPENDANTE.json`. Fin d’entrée → premier son : **34,421 s**; trames distantes non silencieuses et transcription reçues. Ce résultat confirme l’aller-retour automatisé, pas l’interruption.
- **Essai d’interruption instrumenté Codex :** échec, détails dans `RECEPTION-INTERRUPTION-CODEX.json`. Le premier transcript utilisateur arrive à 7,178 s. Le second audio commence à 35,217 s. Aucun second transcript utilisateur n’arrive pendant le délai de 180 s; le seul transcript ultérieur est la réponse de l’agent à 44,053 s. L’outil avait commencé l’envoi au premier événement audio, avant d’avoir établi une période suffisante de réponse active; l’essai ne prouve donc pas un barge-in réussi. Un second essai JARVIS avec la consigne longue s’est terminé en 130,861 s (`returncode=1`, `timeout=false`) après l’expiration du délai interne de 120 s à l’attente du premier audio agent : aucune sortie audio n’a commencé pour cet essai. Le journal STT confirme le traitement de 8,896 s d’entrée. Cela ne démontre pas une interruption; c’est un échec additionnel du tour avec cette requête. Receipt canonique : `b1f7e9593fc3445888197c7b286c8acd`.
- **Interruption après correction VAD :** `agent.py` configure explicitement `turn_handling.interruption.mode="vad"` et `enabled=true`, vérifié avec le SDK installé. Le résultat de réception reste négatif/non conclu­ant; cette configuration seule ne valide pas l’annulation et la reprise d’un tour.
- **Composants :** Whisper français sur fichier, 2,17 s; Piper sur fichier, 2,33 s; tests indépendants STT/TTS/LLM conservés dans leurs receipts. Ce sont des mesures de composants, pas la latence conversationnelle.
- **Ressources :** l’agent a signalé un PSS d’environ 1 015 MiB sur un job (seuil d’avertissement seulement). Un relevé séparé Dell n°1 indiquait CPU 27,8 %, RAM 4 309/257 453 MiB, GPU RTX 3090 à 84 % et 72 °C, VRAM 17 136/24 576 MiB; il n’était pas synchronisé avec les essais WebRTC et ne représente pas une mesure de charge attribuable à ceux-ci. Aucun pourcentage d’autonomie n’est calculé, faute de méthode définie.
- **Tailscale :** le test historique t11 depuis le contexte confiné échouait (`Connection refused`). Un contrôle HTTP séparé lancé depuis Dell n°1, vrai nœud Tailscale, a maintenant atteint l’endpoint LiveKit du Mac mini : HTTP 200 en 0,0178 s; receipt bridge `1dd75ffe36d949ae93e215fb271ca4a2`. Cela confirme la joignabilité HTTP depuis un autre nœud. Aucun client WebRTC distant n’a encore transmis de média via Tailscale; le transport UDP et le flux vocal distant restent non validés. La connexion SSH directe depuis l’environnement Codex a été refusée par la politique distante.
- **Déconnexion/reconnexion WebRTC automatisée :** réussie dans `RECEPTION-RECONNECT-CODEX.json`. Premier agent rejoint à 0,976 s; après déconnexion du premier client, l’API serveur a confirmé le départ de l’agent à 21,711 s; un second client s’est reconnecté et l’agent redispatché a rejoint à 22,786 s. Aucune conversation audio/LLM n’a été exécutée dans ce test. **Microphone/haut-parleur physique :** non testé.

Les délais 34,421 s et 78,459 s sont des observations murales d’essais distincts et variables, pas une estimation générale ni un objectif atteint. Toute latence après échauffement reste non mesurée.

## Services et disponibilité

Au contrôle du 20/10, `jarvis-mission23-livekit-server.service` et `jarvis-mission23-livekit-agent.service` étaient actifs et activés au démarrage. L’agent avait été redémarré après correction et s’était réinscrit. `jarvis-conversation.service` a également redémarré et était actif. Les journaux contiennent des avertissements de latence de boucle pendant le chargement Piper et des échecs LLM intermittents par timeout; ils doivent rester visibles dans la réception, pas être effacés comme preuve de succès.

## Contributions et provenance

Le développement initial, les tâches t01–t12, les rapports historiques et la publication GitHub initiale sont attribués à **JARVIS**. **Codex** a diagnostiqué l’origine des `SIGKILL` de timeout; corrigé `agent.py` pour les symboles, la signature SDK, le cycle de démarrage et le mode d’interruption VAD explicite; amélioré le vérificateur WebRTC et l’option de délai de la passerelle; exécuté les contrôles finaux et rédigé le présent addendum de correction après que JARVIS eut laissé deux verdicts GO erronés. L’archive du rapport précédent de JARVIS est conservée dans `historique/t13_rapport_final_JARVIS_20261020_1045_historique.md`.

**Hash SHA-256 de `RECEPTION-INTERRUPTION-CODEX.json` :** `ee695928277953b6282ffb8e3cdf6f91d3129a7513cd4d6fab18af6cdd2b854b`.

## Suite requise pour JARVIS

JARVIS doit publier le code, les preuves et ce rapport corrigé sur les PR existantes #12 et #13, sans créer de doublon et sans fusion vers `main`; vérifier les empreintes distantes; garder t13 non validée tant que l’interruption n’est pas démontrée; poursuivre un essai où la seconde voix commence au milieu d’une réponse effectivement audible, vérifier son annulation, son second transcript, le nouveau flux audio et la reconnexion; puis effectuer l’essai depuis un vrai nœud Tailscale. Si un microphone physique reste indisponible, la réception finale doit le dire et donner une procédure utilisateur courte. Le rapport et les erreurs antérieurs restent archivés; cette correction ne clôt pas la mission.

**Addendum de réception corrigé par Codex — 20/10/2026.** Rapport original et exécution principale par JARVIS. Tâche t13 à reprendre et publier par JARVIS.

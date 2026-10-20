# Rapport final t13 — Mission 23 LiveKit

**Mission originale :** `7971ec0311124fb4be9e3125dcb291fd`  
**État au 20 octobre 2026 :** **❌ NO-GO pour la réception finale — chaîne partielle, t13 bloquée**  
**Tâches :** t01 à t12 restent validées selon leur historique; t13 est rouverte et bloquée par les critères de réception vocale qui échouent ou restent non testés. La mission n’est pas clôturée.

## Verdict vérifié

Un client WebRTC automatisé a rejoint une salle LiveKit, envoyé un fichier WAV français, reçu sa transcription, puis des trames PCM Piper distantes non silencieuses. Cela prouve un aller-retour vocal automatisé sur le Mac mini. Cela ne prouve ni l’interruption d’une réponse en cours, ni la reconnexion, ni un appel depuis un autre nœud Tailscale, ni une réception au microphone/haut-parleur physique. L’interruption est exigée par l’objectif de conversation et ne peut être déclarée non bloquante ici : le verdict final demeure **❌ NO-GO**.

## SIGKILL : cause établie

Les receipts historiques des appels `verify_livekit_voice.py` montrent `returncode=-9`, `timeout=true` et environ 60 secondes d’exécution. L’implémentation de `host_bridge.py` termine explicitement le groupe de processus avec `SIGKILL` quand son délai `host_exec` expire. Ces `-9` sont donc des expirations de la passerelle, pas une preuve d’un kill OOM du noyau.

Les éléments contrôlés concordent : `memory.events` du cgroup de l’agent indique `oom=0`, `oom_kill=0`, `oom_group_kill=0`; aucune limite `MemoryMax` active; environ 27–29 GiB disponibles sur l’hôte pendant les prélèvements. LiveKit a émis un avertissement PSS au-dessus de 1 000 MiB, explicitement consultatif, sans limite de mémoire configurée. Les premières sorties en erreur des workers comprenaient aussi un import d’API absent et une construction `Agent` sans `instructions`, qui étaient des défauts applicatifs distincts et ont été corrigés. Le mélange multiprocessing/Bubblewrap et un OOM ne sont pas établis comme cause des `-9` historiques.

La passerelle a reçu une option de délai explicite bornée à 300 secondes pour permettre ces essais longs. L’agent utilise maintenant les API installées de LiveKit Agents 1.8.8; le service enregistre le worker `jarvis-agent`. Le journal du run initial a montré un blocage de boucle de 1,636 s pendant `PiperVoice.load`, accompagné d’un avertissement VAD plus lent que le temps réel. Codex a préchargé Piper en thread avant `ctx.connect`; le run suivant ne montre plus de blocage ONNX/Piper, et le warmup a duré 1,828 s. Cette correction seule ne résout pas la coupure.

## Réception et mesures

Le condensé vérifiable des résultats Codex, avec références d’évidence et empreintes SHA-256 des preuves détaillées, est conservé dans `RECEPTION-RESULTATS-CODEX.json`. Il exclut les trames brutes du rapport de synthèse.

- **WebRTC / WAV / STT / LLM / TTS / retour audio, essai indépendant Codex :** réussi dans `RECEPTION-WEBRTC-CODEX.json`. Durée WAV 3,564 s; transcription française reçue à 7,677 s depuis le début; premier PCM distant non silencieux à 83,126 s; fin d’entrée → premier son : **78,459 s**. Microphone physique : non.
- **WebRTC indépendant relancé par JARVIS :** reçu et vérifié dans `RECEPTION-WEBRTC-INDEPENDANTE.json`. Fin d’entrée → premier son : **34,421 s**; trames distantes non silencieuses et transcription reçues. Ce résultat confirme l’aller-retour automatisé, pas l’interruption.
- **Nouvel essai d’interruption sur réponse effectivement audible :** échec confirmé, résumé dans `RECEPTION-INTERRUPTION-CODEX-TIMEOUTFIX-SUMMARY.json`, trames brutes conservées dans `RECEPTION-INTERRUPTION-CODEX-TIMEOUTFIX.json`. La transcription utilisateur initiale arrive à 8,945 s; le premier audio agent non silencieux commence à 41,488 s. La seconde intervention commence à 42,089 s, donc pendant la réponse; elle se termine à 44,431 s. Aucun second transcript utilisateur n’arrive durant 150 s. L’agent continue à publier des trames non silencieuses jusqu’à 57,410 s, soit 15,32 s après le début de l’interruption. Le transcript agent arrive à 56,729 s. Le test confirme une réponse WebRTC réelle mais aussi que la réponse n’est pas interrompue. Whisper transcrit isolément le WAV « Stop ! Réponds maintenant ! »; son passage dans un second tour LiveKit échoue. Résultat brut, SHA-256 `33c76bcdf56b9b9f9ac2b1068cb126b1234217bd6f6d31fb8ddc0bcf0a7fca33`.
- **Interruption après correction VAD :** `agent.py` configure explicitement `turn_handling.interruption.mode="vad"` et `enabled=true`, vérifié avec le SDK installé. Le résultat de réception reste négatif/non conclu­ant; cette configuration seule ne valide pas l’annulation et la reprise d’un tour.
- **Composants :** Whisper français sur fichier, 2,17 s; Piper sur fichier, 2,33 s; tests indépendants STT/TTS/LLM conservés dans leurs receipts. Ce sont des mesures de composants, pas la latence conversationnelle.
- **Ressources :** l’agent a signalé un PSS d’environ 1 015 MiB sur un job (seuil d’avertissement seulement). Un relevé séparé Dell n°1 indiquait CPU 27,8 %, RAM 4 309/257 453 MiB, GPU RTX 3090 à 84 % et 72 °C, VRAM 17 136/24 576 MiB; il n’était pas synchronisé avec les essais WebRTC et ne représente pas une mesure de charge attribuable à ceux-ci. Aucun pourcentage d’autonomie n’est calculé, faute de méthode définie.
- **Tailscale :** le test historique t11 depuis le contexte confiné échouait (`Connection refused`). Un contrôle HTTP séparé lancé depuis Dell n°1, vrai nœud Tailscale, a maintenant atteint l’endpoint LiveKit du Mac mini : HTTP 200 en 0,0178 s; receipt bridge `1dd75ffe36d949ae93e215fb271ca4a2`. Cela confirme la joignabilité HTTP depuis un autre nœud. Aucun client WebRTC distant n’a encore transmis de média via Tailscale; le transport UDP et le flux vocal distant restent non validés. La connexion SSH directe depuis l’environnement Codex a été refusée par la politique distante.
- **Déconnexion/reconnexion WebRTC automatisée :** réussie dans `RECEPTION-RECONNECT-CODEX.json`. Premier agent rejoint à 0,976 s; après déconnexion du premier client, l’API serveur a confirmé le départ de l’agent à 21,711 s; un second client s’est reconnecté et l’agent redispatché a rejoint à 22,786 s. Aucune conversation audio/LLM n’a été exécutée dans ce test. **Microphone/haut-parleur physique :** non testé.

Les délais 34,421 s et 78,459 s sont des observations murales d’essais distincts et variables, pas une estimation générale ni un objectif atteint. Toute latence après échauffement reste non mesurée.

## Services et disponibilité

Au contrôle du 20/10, `jarvis-mission23-livekit-server.service` et `jarvis-mission23-livekit-agent.service` étaient actifs et activés au démarrage. L’agent avait été redémarré après correction et s’était réinscrit. `jarvis-conversation.service` a également redémarré et était actif. Le SDK installé donnait par défaut 10 s au premier morceau LLM, alors qu’un contrôle Ollama court a mesuré 57,105 s avant le premier token (HTTP 200, 57,926 s au total). Codex a porté le délai LiveKit à 90 s et le délai HTTP à 120 s. Un nouveau tour WebRTC a produit des trames non silencieuses, mais le second tour n’a pas été reconnu.

## Contributions et provenance

Le développement initial, les tâches t01–t12, les rapports historiques et la publication GitHub initiale sont attribués à **JARVIS**. **Codex** a diagnostiqué l’origine des `SIGKILL` de timeout; corrigé `agent.py` pour les symboles, la signature SDK, le cycle de démarrage et le mode d’interruption VAD explicite; amélioré le vérificateur WebRTC et l’option de délai de la passerelle; exécuté les contrôles finaux et rédigé le présent addendum de correction après que JARVIS eut laissé deux verdicts GO erronés. L’archive du rapport précédent de JARVIS est conservée dans `historique/t13_rapport_final_JARVIS_20261020_1045_historique.md`.

**Hash SHA-256 de `RECEPTION-INTERRUPTION-CODEX.json` :** `ee695928277953b6282ffb8e3cdf6f91d3129a7513cd4d6fab18af6cdd2b854b`. Le nouvel essai actif détaillé porte l’empreinte `33c76bcdf56b9b9f9ac2b1068cb126b1234217bd6f6d31fb8ddc0bcf0a7fca33`.

## Suite requise pour JARVIS

JARVIS a publié des versions antérieures sur les PR #12 et #13; Codex a ensuite synchronisé les sources et preuves actuelles par le broker GitHub JARVIS, et publié le correctif de description de l’outil sur la PR #11. Les arbres distants ont été vérifiés par SHA-256, sans créer de PR et sans fusion vers `main`. La PR #11 contient le commit `eeca8d913f248e59cc7a0e1029e568327b6656a4`; #12 les commits `20c94bd6d85ad12a2a3483fc7169bb099e1c1b01`, `a3a3870798127f28803f0dc44240c1c22c32a2cd`, `081b2623e468a2b81ef4ffc3a5a817efc30df330`; #13 les commits `8eb0a603e19ede8a77c4fe5889c9301fdf8946e7`, `6a67f5b739b0dedf86d7c9efba338763e7aede97`, `0fd48da6ef304706a26e389b3e31ff7f7644189a`. t13 reste bloquée tant que l’interruption n’est pas démontrée; poursuivre un essai où la seconde voix commence au milieu d’une réponse, vérifier son annulation, le second transcript, le nouveau flux audio, puis le média WebRTC depuis un vrai nœud Tailscale. Si un microphone physique reste indisponible, la réception finale doit le dire et donner une procédure utilisateur courte. Le rapport et les erreurs antérieurs restent archivés; cette correction ne clôt pas la mission.

**Addendum de réception corrigé par Codex — 20/10/2026.** Rapport original et exécution principale par JARVIS. Corrections ciblées Piper/LLM et essais complémentaires par Codex. La tâche t13 reste bloquée; aucune clôture n’est justifiée.

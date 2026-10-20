# Réception finale — mission 23D

**✅🟡 GO numérique avec réserves acoustiques, STT et d’autonomie.** Le banc réel est créé et exécuté ; les verdicts des essais initiaux et les rapports historiques sont conservés. Aucune fusion dans main.

## Sujet et protocole mesurable

Visite fictive du musée des sciences : samedi14h, deux adultes,40€. La correction vocale impose dimanche10h,20€. Aucune réservation ni action externe. Les fixtures françaises Piper sont conservées avec leurs SHA256 dans mission23d/fixtures/. Les tests publient les vrais WAV sur une piste WebRTC ; Whisper, le modèle Ollama Dell et Piper sont réellement utilisés, puis le client reçoit le PCM. Le troisième tour de la campagne initiale interroge le jour, l'heure et le budget pour vérifier la continuité de la session.

Seuils fixés avant la baseline : son actif dans les200ms avant injection ; coupure en≤1s avec silence RMS≤20 pendant≥500ms ; nouvelle transcription correcte dans20s après fin du WAV ; reprise audio dans90s. Une réponse déjà terminée rend l'essai d'interruption invalide. Les absences de preuves restent incomplètes. Les cases PASS ci-dessous sont calculées depuis les mesures, pas depuis les validations du moteur.

| Campagne / exécution | Coupure s (≤1) | Transcription après entrée s (≤20) | Reprise après transcription s (≤90) | Continuité | Verdict |
|---|---:|---:|---:|---|---|
| initial / nominal | — | — | — | None | PASS |
| initial / barge-early-1 | 2.453 | 2.123 | 1.331 | True | FAIL |
| initial / barge-early-2 | 2.408 | 2.195 | 1.146 | True | FAIL |
| initial / barge-late | 0.946 | 2.189 | 35.872 | True | PASS |
| initial / silence | — | — | — | None | PASS |
| initial / noise | — | — | — | None | PASS |
| après réglage / barge-early 1 | 0.727 | 2.258 | 1.185 | vérifiée dans la campagne initiale | PASS |
| après réglage / barge-early 2 | 0.559 | 2.404 | 1.116 | vérifiée dans la campagne initiale | PASS |
| après réglage / barge-late 3 | 0.717 | 2.265 | 28.153 | vérifiée dans la campagne initiale | PASS |

La baseline indépendante antérieure avait mesuré2,401s, une transcription en2,095s et une reprise en60,007s. Le premier outil Codex bloquait sur wait_for_playout avec silence continu ; cette tentative a été classée invalide et corrigée avant la baseline recevable. Sa réussite n'est jamais comptée.

## Cause et corrections réellement exécutées

Le SDK LiveKit Agents1.8.8 installé définit _DEFAULT_AEC_WARMUP_DURATION=3.0. Sa documentation locale et AgentActivity._interrupt_by_audio_activity montrent que les interruptions sont ignorées tant que ce délai court au premier tour de parole. Dans la campagne initiale, le VAD détecte l'utilisateur, puis l'agent s'arrête environ3,05s après son propre début de parole : cela explique les deux échecs précoces et le succès de l'interruption tardive.

JARVIS a exécuté l'outil correctif Codex : aec_warmup_duration=0.0 dans AgentSession, interruption VAD explicite de0,3s, min_words0, reprise après fausse interruption désactivée ; génération anticipée maintenue désactivée. Le SDK n'est pas modifié. L'annulation d'écho du navigateur reste disponible ; la robustesse acoustique réelle reste à réceptionner. Une relance réelle de l'agent et ses nouveaux PID sont corrélés aux reçus de host_project_service.

Autres corrections reçues : Piper déclare désormais sa fréquence réelle44100Hz et le PCM est extrait via un lecteur WAV ; le flux SDK non silencieux a été mesuré à44100Hz. La factory Qwen demande reasoning_effort=none. L'URL CDN inexistante a été remplacée par le bundle local LiveKit Client2.4.0 et sa licence. Le client fournit une seule piste WAV réutilisable et attend la piste agent avant d'injecter la parole.

## Client et Stop vérifiés indépendamment

Le navigateur Mac a réellement connecté la piste WAV, reçu l'audio distant et transcrit le scénario. Lors du test Stop, l'audio était actif dans les200ms précédentes (RMS953.1). Coupure locale mesurée à0.600ms, aucun lecteur audio restant, déconnexion et suppression de la salle. Deux secondes plus tard : session toujours déconnectée=True, lecteurs=0. JSON et WebM ont été réellement téléchargés ; aucun jeton n'est exporté. Ces mesures numériques ne sont pas une mesure acoustique d'un haut-parleur.

La page propose micro, démarrer/arrêter, statut, transcriptions séparées, réponses, WAV prédéfinis ou choisi, tests automatiques et exports JSON/audio. Les tests automatiques utilisent une salle dédiée : ils sont distincts de la conversation ouverte. Le micro physique n'a pas été utilisé pour ces preuves. Une conversation complète a été reçue et affichée dans le navigateur, avec son export WebM. Le bouton de test automatique a produit un PASS réel sur le contrôle silence. Un premier contrôle d'annulation du processus a échoué car SIGINT était hérité comme ignoré ; l'outil réinitialise maintenant ce signal avant les imports. Le contrôle rejoué donne ABORTED, code−2, sans prétendre avoir capturé un audio absent. Les traces avant/après restent dans les exports navigateur.

## Conservation et attributions

Même exécution7971ec0311124fb4be9e3125dcb291fd ; 12 validations historiques identiques=True. CONTINUITE.json compare aussi les anciens checkpoints, événements et appels aux sauvegardes cohérentes. Les vues de travail ont été archivées puis reconstruites ; aucun reset de la mémoire ni des identifiants. La politique du broker conserve son empreinte bb434ec70feb1d78759ace6abbd72b0876016fbd051d44f39b63220aab9d5ca9. Les services de broker et de conversation restent disponibles. Les opérations de code et de redémarrage concernent le prototype LiveKit et sa passerelle temporaire.

JARVIS a produit les premiers fichiers, exécuté les contrôles, appliqué les correctifs fournis, lancé les campagnes et publié des sources et rapports. Codex a coordonné, refusé les premiers résultats insuffisants, fourni la logique client et les outils manquants, diagnostiqué le délai AEC, produit les correctifs et contrôlé le navigateur et les preuves. **Autonomie fortement guidée** : les validations initiales01–03 du moteur ont précédé les essais complets ; elles restent historiques et ne constituent pas une réception globale. Les rapports du modèle et le blocage t13 historique doivent être lus avec les errata et ce rapport de réception.

## Limites effectives

- Aucun essai acoustique au micro/haut-parleur, ni réception iPhone/Safari. La sensibilité à l'écho après suppression du warmup reste ouverte.
- Whisper a transcrit « samedi » par « Sunday » dans la phrase initiale, et JARVIS par « Jarvie ». Les trois consignes correctives dimanche/10h/20€ sont reçues correctement. Le PASS nominal concerne la chaîne sonore ; aucune transcription intégrale sans erreur n'est revendiquée.
- Silence et bruit sont testés dans une salle au repos ; cela ne démontre pas l'absence de fausse interruption par du bruit pendant une réponse.
- La continuité prouvée est celle du dialogue LiveKit en mémoire de session ; aucune intégration nouvelle à la mémoire personnelle canonique ou aux outils du broker n'est revendiquée.
- Les horaires du premier nominal incluent un bref chevauchement avec le probe Stop navigateur ; les répétitions barge-in suivantes sont séparées. Les latences sont celles de ces essais, pas un engagement de performance.
- Les statistiques réseau contenant les adresses restent privées. La signalisation via tunnel ne prouve pas à elle seule une route média Tailscale.

## Preuves et utilisation

PREUVES-JARVIS.json corrèle commandes, tâches, evidence_id, codes de retour et empreintes des reçus canoniques. MANIFESTE-ARTEFACTS.json référence les sources et audio copiés, avec SHA256. Les WAV, PCM reçus et événements UTC/monotones sont dans mission23d/reports/. Les rapports initiaux et les campagnes échouées ne sont pas écrasés. Voir UTILISATION.md pour ouvrir, arrêter et reproduire le banc.

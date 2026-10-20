# Mission 23D — réception indépendante en cours

Date : 20 octobre 2026. Codex coordonne ; JARVIS exécute la mission persistante originale. **🟡 En cours ; interruption au seuil fixé : ❌ NO-GO sur la baseline.** Aucun changement du verdict historique23 ou de la réception24.

## Attendu / réellement observé — baseline02

Scénario : musée des sciences, samedi14h, deux adultes,40€. Interruption synthétique : dimanche10h,20€. Transport réellement parcouru : piste WebRTC → agent LiveKit → Whisper → Ollama Dell → Piper → audio reçu par le client RTC. Aucun microphone physique.

| Critère annoncé avant essai | Attendu | Mesure réelle | Résultat |
|---|---|---|---|
| Audio actif avant injection | PCM RMS>20 dans les200ms précédentes | Oui | PASS |
| Coupure stable | ≤1s ; silence RMS≤20 pendant500ms | 2,4009s | FAIL |
| Nouvelle transcription | dimanche/10h/20€, ≤20s après fin WAV | Contenu reçu ;2,0947s après fin WAV | PASS |
| Reprise audio | ≤90s après transcription | 60,007s | PASS temporel ; contenu final à vérifier séparément |
| Premier son | Mesure informative | 97,6692s après fin entrée | Latence élevée |
| Continuité, Stop UI, bruit/silence, reconnexion | Essais distincts | Pas encore reçus à ce jalon | INCOMPLET |

La réponse initiale était réellement audible au moment de l'interruption. La transcription finale reçue est « Dimanche à10h, budget20€, confirme uniquement les nouveaux horaires et le budget. » Le PCM retour, les événements UTC/monotones, les RMS de chaque trame et leurs empreintes sont dans `preuves/baseline-02/`. La capture s'arrête six secondes après le début de la seconde réponse ; elle ne prouve donc pas son contenu complet ni la continuité ultérieure.

## Limites et corrections de méthode

La première tentative indépendante baseline01 a mis en évidence un défaut de l'outil Codex : `wait_for_playout()` ne termine pas lorsque la piste est alimentée en silence continu. Elle est **INVALIDE pour la mesure d'interruption** et ne compte pas comme répétition. Son audio et ses traces restent privés ; aucune réussite n'en est déduite. Baseline02 utilise une attente bornée après vidage de la file WAV, avec piste continue et journalisation immédiate. La coupure est déterminée à partir de trames audio effectivement reçues, pas d'un changement d'état du SDK.

Les temps du WAV retour sont alignés sur l'arrivée des trames au client. Il s'agit d'une mesure numérique du client, pas d'une mesure acoustique haut-parleur. Les statistiques de route contenant des adresses restent privées ; leur empreinte figure dans le manifeste original. Un accès de signalisation via Tailscale ne prouve pas à lui seul la route média.

Le premier runner écrit par JARVIS a été refusé par revue Codex : syntaxe et API incompatibles, factories inexistantes et injection encore vide. Codex a fourni un outil de mesure RTC réellement exécuté et l'a copié dans le périmètre lisible de JARVIS après un refus réel d'accès à son répertoire privé. Les versions rejetées restent dans les événements canoniques ; elles ne sont pas une réception logicielle.

## Pistes transmises à JARVIS

Piper produit réellement des WAV44100Hz avec la voix locale ; l'adaptateur TTS consulté déclare16000Hz. Une correction et une preuve composant sont nécessaires avant retest. Le moteur conversation désactive le thinking Qwen, contrairement à la factory LiveKit observée. La possibilité `reasoning_effort="none"` est documentée par [Ollama](https://github.com/ollama/ollama/blob/main/docs/api/openai-compatibility.mdx) et exposée par le SDK installé ; sa compatibilité locale reste à tester. Ces pistes ne sont pas présentées comme des causes déjà résolues.

## Conservation et attribution

Branche23D basée sur `ed3536393acddcd757ce23d55586a881a1d2d8f5` (mission24). Sauvegarde SQLite cohérente privée avant ajout de trois tâches23D. Même identifiant de mission, douze validations historiques conservées ; la clôture t13 dépend maintenant de la publication23D. Aucun reset de mémoire, changement de broker, nouvelle mission ou fusion main. Directives consultées et transmission horodatée : `INSTRUCTION-JARVIS.md` et `TRANSMISSION.json`.

Cette réception est guidée : scripts indépendants, fixtures de mesure, coordination et revue attribués à Codex ; développement du client et des corrections applicatives demandé à JARVIS. Aucun succès d'autonomie sans assistance revendiqué.

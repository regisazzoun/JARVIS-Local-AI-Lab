# Mission 13E — tests et recette

## Nature des preuves
**Réel** : serveur HTTP, authentification, trois modèles Ollama installés, CPU Whisper/Piper, lecture Chromium, backup/restauration, restart systemd. **Substitution** : microphone Chromium alimenté par un véritable WAV de parole synthétique française, disposition mobile émulée. **Physique partiel** : capture ALSA 2 s quasi silencieuse ; aucune personne ne prononce de phrase de recette. **Simulé** : certains tests unitaires de connexion échouée, timeout et adaptateur LLM, identifiés comme tels.

Preuves locales regroupées dans `mission13e-preuves/` ; elles restent hors publication automatique. Les tests utilisent uniquement des données fictives. Les fixtures de recette sont supprimées par IDs/projets exacts, pas par purge générale. Aucun souvenir personnel approuvé créé.

| Critère | État | Preuve |
|---|---|---|
| 1 Démarrage JARVIS | Validé réel | systemd actif, HTTP après activation |
| 2 Interface sur origine compatible | Validé localhost Chromium ; réserve clients distants | browser-tests.json, secure origin localhost |
| 3 Audio français transcrit | Validé réel, voix synthétique | real-integration.json, voice-tests.json |
| 4 Transcription envoyée au modèle réel | Validé | real-integration.json et deployed-reception.json |
| 5 Réponse réelle | Validé Qwen/Ministral/Llama | réponses et mesures, real-integration.json |
| 6 Piper produit l’audio | Validé Tom CPU | WAV valide, deployed-reception.json |
| 7 Audio récupérable et lisible | Validé HTTP/Chromium ; écoute humaine en réserve | browser-tests.json |
| 8 Conversation écrite | Validée | navigateur et requêtes HTTP Qwen |
| 9 Historique persistant | Validé | 4 messages relus après changement de PID |
| 10 Souvenirs approuvés persistants | Validé avec fixture | réponse après restart dans deployed-reception.json |
| 11 Mémoire commune modèles | Validé stockage et rappel LLM réel | même code AZUR-713 retrouvé par les trois modèles |
| 12 Suppression active | Validée en nouvelle conversation | recherche vide, IDs absents, plus de code dans réponse réelle |
| 13 Sauvegarde/restauration | Validée réel | tests unitaires, base d’intégration restaurée, backup canonique restauré vers test |
| 14 Service redémarre | Validé réel | PID différent, reconnexion, données conservées |
| 15 Ollama/WebUI préservés | Validé | health HTTP, unités actives, SHA protégés, modèles identiques |
| 16 Outil diagnostic choisi par JARVIS | Validé réel | tool_call Qwen et réponse française corrigée après diagnostic HTTP |
| 17 Procédures exploitation | Livrées | installation/utilisation/reprise/architecture |
| 18 Roadmap/rapport | Livrés localement, publication sur branche dédiée | fichiers MISSION-13E et ajout daté ROADMAP ; PR à valider avant fusion |

## Campagnes
- 15 tests unittest : migration v1→v2/idempotence, transactions, FTS5, consentement explicite, refus, suppression, déduplication, obsolescence, expiration, documents séparés, historique, sessions éphémères, backup/restore, erreurs, authentification, outils et risques.
- 4 tests d’intégration réels : audio→Whisper→Qwen→Piper ; trois modèles/même mémoire/correction/suppression ; diagnostic natif ; proposition LLM pending puis refus.
- 8 essais navigateur sur service installé : login, capture WebM→Whisper, écrit Qwen, lecture/arrêt, texte long segmenté, chaîne automatique, mobile sans débordement, logout/API 401.
- Voix : invalidité, vide, silence, durée excessive réellement rejetés. Reconnexion/reprise réelle ; appels successifs réussis.
- Performance : génération GPU en parallèle des workers CPU réussie ; VRAM 17 503 MiB, GPU observé jusqu’à 87 %, pas de demande CUDA pour STT/TTS.

Commandes reproductibles : `scripts/test`, `scripts/test-voice`. Les scripts `tests/real_integration.py` et `tests/browser_test.py` visent une instance temporaire sur 8767 par défaut ; ne pas relancer le test multi-modèles sur la base personnelle ni pendant une conversation WebUI. Le script deployed_reception utilise des fixtures taggées et nettoyées, mais effectue un restart de la passerelle : réserver une fenêtre de maintenance. Aucun reboot machine testé.

## Vérification humaine du lendemain
1. Ouvrir localhost par tunnel, se connecter, autoriser micro et sortie son.
2. Prononcer une courte question française, écouter Tom et vérifier la transcription.
3. Désactiver envoi automatique, corriger une transcription, envoyer ; interrompre l’audio.
4. Reprendre la conversation et proposer un souvenir fictif, refuser puis approuver un autre via bouton explicite ; le supprimer.
5. Après future activation HTTPS privée, répéter sur Safari iPhone et macOS ; garder 13D distincte.

GO AVEC RÉSERVES : aucune simulation n’est présentée comme microphone/parole humaine ou test Safari physique.

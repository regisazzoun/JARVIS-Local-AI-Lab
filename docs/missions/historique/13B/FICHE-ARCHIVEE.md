> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS-Documentation/missions/mission-13b/README.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 13B

- Identifiant : 13B.
- Date ou période : Date de contenu non établie ; métadonnées disponibles dans MANIFESTE.json.
- Objectif initial : Rapport 13B — GO PARTIEL
- Matériel mentionné : Non documenté dans les rapports retenus.
- Logiciels mentionnés : CUDA / Ollama / Open WebUI / Whisper / Piper
- État final documentaire : **PARTIEL**. Passerelle et mémoire testées ; Ollama réel et navigateur non validés à cette étape.

## Actions et résultats confirmés

Passerelle et mémoire testées ; Ollama réel et navigateur non validés à cette étape.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Passerelle et mémoire testées ; Ollama réel et navigateur non validés à cette étape.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- 13B.md (référence locale historique non publiée)

## Références et dépendances

Aucune référence explicite extraite.. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### 13B.md (référence locale historique non publiée)

Navigateur localhost → tunnel SSH préexistant → HTTP Python sur [ADRESSE PRIVÉE EXPURGÉE]:8765 → orchestrateur → workers Whisper Small/Piper Tom CPU et API Ollama existante. Interface HTML/CSS/JS sans framework ni service cloud. Développement sous /home/adminjarvis/JARVIS/conversation : /opt ne fait pas partie des emplacements autorisés en écriture. Aucun fichier 13A modifié volontairement, aucun paquet installé, aucun moteur téléchargé.

Versions vérifiées par métadonnées : faster-whisper 1.2.1, piper-tts 1.8.0, onnxruntime 1.31.0, av 15.1.0. Python applicatif 3.13, venv sans pip. Modèles locaux Whisper Small et fr_FR-tom-medium.onnx présents, utilisés réellement. Les versions Ollama/Open WebUI et la liste réelle des modèles restent non confirmées ; la configuration reprend la liste autorisée fournie par l’utilisateur.

## Fonctionnement
Push-to-Talk avec capture MediaRecorder côté client, arrêt au relâchement et limite 45 s configurable. Transcription française affichée et modifiable avant envoi. Dialogue écrit, historique, choix du moteur, projet, réponse vocale désactivable, indicateurs de phases, erreurs lisibles. Identité JARVIS commune aux moteurs, aucun outil d’automatisation. Un verrou global limite STT/LLM/TTS à une opération à la fois ; une seconde opération reçoit HTTP 409. Ollama : API chat non streaming, délai 240 s, sortie plafonnée à 1024 tokens, aucun changement du service. Voice timeout 120 s ; fichiers temporaires retirés après réussite ou erreur. Silence, audio vide/invalide et durée réelle contrôlés. Piper CPU exclusivement, voix Tom, segments 600 caractères côté navigateur. Lecture interrompable, synthèse en attente invalidée côté UI sans tuer d’autres services.

## Validation intermédiaire et finale
- Réel : synthèse Piper → WAV → transcription Whisper correcte d’une phrase française fictive.
- Réel : audio vide/invalide/silence et durée excessive rejetés.

# Notes techniques — Mission 11

Inspection statique au commit `68cfe48d3ae775dd56d4ef0e7bd69843b346b228`. Les numéros de ligne concernent ce snapshot. Sources publiques copiées pour vérification, jamais importées ni exécutées. Le texte des licences est conservé ; les copies ne sont pas des modules installés.

## Points décisifs

- STT : `bin/stt.py:25–49` construit WhisperModel, CPU/int8 et VAD ; aucune langue explicite. La configuration amont consultée fixe `small.en`. Changer de modèle multilingue avant tout test français.
- TTS : `bin/say-local.sh` implémente des clients Kokoro et Qwen3-TTS. Pas de branche Piper active ; une mention dans un document d’archive ne constitue pas un backend.
- Web : `jarvis-web/client/js/talk.js` utilise réellement getUserMedia et MediaRecorder. `docs/WEB_TALK.md` décrit l’alternance, les limites acoustiques et l’approbation Web.
- Sécurité : `orchestrator/executor.py:509–518` annonce un avertissement puis continue ; commentaire TODO de confirmation vocale. Les callbacks Web dans `orchestrator_v2.py` ne justifient pas une protection universelle.
- Mémoire : `lib/memory_db.py` contient les tables SQL, CRUD, FTS et recherche sémantique. `lib/user_profile.py` lit la carte profil ; `response_formatter.py` l’ajoute au prompt. `orchestrator_v2.py:3704+` récupère les souvenirs pertinents. La qualité comportementale n’a pas été testée.
- Embeddings : `lib/embeddings.py` impose EmbeddingGemma/Jarvis BF16 et 768 dimensions. `/api/embed` ne suffit pas à démontrer la compatibilité avec Ollama exact ; aucun modèle d’embedding n’apparaît dans les tags locaux.
- Documents : `lib/source_library.py` conserve originaux et passages, recherche FTS/vecteurs. Ces sources sont distinctes des index WebUI.
- Sync : `docs/SYNC_ARCHITECTURE.md` et `bin/sync-memory-db.py` concernent les bases cloud/local ; limite annoncée de 100 échanges récents ; pas une réplication de deux machines.
- Ports : `docker-compose.yml` API 8880, UI 5001, Canvas 8890, extras 5002–5004. Exemple local Kokoro 8880 : collision si API et TTS partagent l’hôte. Qwen3-TTS exemple 8881.
- Installation : `install.sh`, `install-system-deps.sh`, `setup.sh` inspectés uniquement. Ils comportent des mutations APT/venv/config et ne sont pas appropriés à la présente mission.

## Observations locales et preuve antérieure

`ollama-version.json` et `ollama-tags.json` résultent de GET strictement consultatifs. `verification-locale.txt` : Python/RAM/disque/métadonnées dpkg. Une sortie dpkg sans version ne confirme pas un paquet installé ; aucune tentative de réparation.

Les rapports locaux 06, 07, 08, 09, 09B, 10 ont été lus sans export de données privées. Références principales : Mission 06 réseau Docker hôte, API Ollama loopback et WebUI ; Mission 07 limites de contexte/RAG ; Mission 08 un seul modèle chargé et avertissements de sécurité ; Mission 09B résolution GPU ; Mission 10 Qwen 17 489 Mio, 65 couches, 38 tokens/s et limites d’administration autonome. Les résultats GPU sont historiques, non reproduits pendant Mission 11.

## Incidents de consultation

- Anciennes URLs docs Open WebUI audio/memory : erreurs de consultation. Repli sur source v0.12.0.
- Ancien chemin `routers/audio.py` : HTTP 404. Résolu via arbre GitHub : paquet `routers/audio/__init__.py` et `realtime.py`, sources sauvegardées.
- Premier chemin Kokoro VOICES sur GitHub : HTTP 404. Résolu via dépôt officiel du modèle sur Hugging Face.
- strognoff LICENSE : HTTP 404 à la racine ; MIT du README non corroboré par un fichier de licence. EN ATTENTE.
- Deux recherches locales de chemins supposés inexistants ont été corrigées par inspection de l’arborescence ; aucun impact sur l’environnement.

## Références complémentaires

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper), README sauvegardé : CPU int8 et dépendances CUDA/cuDNN pour GPU. Les mesures amont proviennent d’un autre CPU/GPU.
- [Piper maintenu](https://github.com/OHF-Voice/piper1-gpl), README sauvegardé ; moteur GPL-3.0. [Siwis français](https://huggingface.co/rhasspy/piper-voices/blob/main/fr/fr_FR/siwis/medium/MODEL_CARD), carte sauvegardée : corpus CC-BY 4.0. Conditions exactes du modèle à figer avant distribution.
- [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI), README sauvegardé ; [voix](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md), `ff_siwis` française.
- [Audio WebUI v0.12.0](https://github.com/open-webui/open-webui/blob/v0.12.0/backend/open_webui/routers/audio/__init__.py), source sauvegardée : clients TTS compatibles OpenAI et faster-whisper local.
- [Mémoire WebUI v0.12.0](https://github.com/open-webui/open-webui/blob/v0.12.0/backend/open_webui/routers/memories.py), source sauvegardée : routes authentifiées CRUD/query. Activation et usage automatique non testés.
- [MDN getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia), contexte sécurisé nécessaire.

## Limites des conclusions

Aucun test de runtime, aucun essai audio, aucune validation du français ni des protections en situation réelle. Audit ciblé des chemins utiles, pas certification de sécurité, couverture intégrale des outils ou qualification juridique. Les estimations de temps/RAM/disque du rapport sont des enveloppes d’ingénierie explicitement séparées des mesures.

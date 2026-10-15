# Notes techniques — Mission 12

## Périmètre réel

Tests : synthèse fichiers Piper et Kokoro ONNX ; transcription fichiers faster-whisper ; démo originale SQLite avec profils simulés. Pas de conversation Ollama, service WebUI, microphone ni agent Mem0/Letta exécutés. Les packages tiers ont été inspectés avant leurs chemins d’exécution ; revue ciblée, pas certification de binaries.

L’inférence refuse les sockets connect/bind, emploie des fichiers locaux et CPU. `run_guarded.py` échantillonne VmRSS toutes les 20 ms et borne le worker à 180 s/2 Gio RSS. `audio_worker.py` limite l’affinité à deux CPUs et les threads, garde les caches dans le temporaire. Les modèles vocaux ne sont pas des modèles Ollama.

## Mesures et limites

Les JSON par moteur conservent temps par extrait, durée audio, RTF et texte. Les JSON guard conservent pic RSS échantillonné et code retour. Pic non continu, court dépassement non exclu ; pas de benchmark thermique ni charge avec Qwen. Piper charge puis recrée sa session CPU pour fixer les threads : son chargement est double dans ce test. Piper et Kokoro ne sont pas au même sample rate, et Kokoro est quantifié int8. Corpus de trois textes répétés dans trois voix ; fichiers TTS synthétiques, aucune voix humaine enregistrée.

`stt-results.json` : 9 transcriptions base. `stt-small-results.json` : 9 transcriptions small et silence. WER brut = distance d’édition de mots Unicode minuscules, ponctuation séparée, nombres non normalisés. Les différences dix-sept/17h30 sont comptées, donc ces scores ne prouvent pas la qualité sémantique. Aucune écoute subjective/MOS revendiquée.

`memory-results.json` : 16 tests, dont nouveaux processus avec profils SIM-Llama et SIM-Qwen. Pas de vraie extraction de conversation : entrée structurée explicite. Profil de routage distinct, mémoire et identité identiques. Date fictive fixe pour expiration. `/tmp` est tmpfs : pas persistance au reboot, pas reboot exécuté. Copie de base dans les preuves sur disque, sans utilisation comme application.

La démo est un prototype limité : pas d’API/authentification, pas de chiffrement ni tests de crash. Suppression des faits actifs/index/logique de contexte, pas effacement physique de pages SQLite/backups. L’audit garde les révisions d’événements, pas un historique complet des anciennes valeurs de projets. Les tests de namespace vérifient les filtres internes, pas une sécurité réseau.

## Sources déterminantes

- WebUI v0.12.0 `utils/memory.py:410+` : revue après tour conditionnée, puis `update_memories` sans validation humaine obligatoire identifiée. `models/memories.py` : user/type/path/content et opérations par ID. Sources de routes audio et mémoire réutilisées de Mission 11 ; références relatives ci-dessous.
- Mem0 `mem0/memory/main.py` : add(infer=True/False), update/delete/history et expiration. `mem0/embeddings/ollama.py` : `_ensure_model_exists` peut appeler pull. `mem0-telemetry.py` : MEM0_TELEMETRY True par défaut. `mem0-config.py` : history.db configurable, défaut sous .mem0. Aucun import Mem0 réalisé.
- Letta dépôt principal README : développement dans letta-code, ancien serveur V1 archive. Letta Code `memory-filesystem.ts`, `memory.ts`, contraintes et réparation de conflits : mémoire Git, résolution de conflits de fichiers ne démontre pas résolution factuelle. `pi-ollama-provider.ts` inclut préchargement ; jamais exécuté.
- Voix Piper : manifest Hugging Face officiel figé, aucun chemin fr_CA. Les deux cartes de corpus sont à conserver : Siwis CC-BY4 ; Tom projet/corpus AGPLv3, portée des poids à confirmer avant redistribution.
- Kokoro : modèle int8 et fichier de voix release model-files-v1.0 ; wrapper CPU from_session/lang fr-fr ; source de tokenizer et loader espeak inspectée.
- F5 québécois : modèle explicite mais CC-BY-NC et volumineux ; pas téléchargé. La liste de fichiers de son snapshot ne fournit pas de WAV hors répertoire dataset au relevé ; pas de sample auteur présenté comme généré localement.

## Incidents résolus / reportés

- Vocabulaire base .json 404, corrigé en .txt selon inventaire officiel ; premier log conservé.
- PyAV19 refuse metadata_errors, fixé à15.1.0 dans venv ; deuxième log conservé. Aucun patch d’Open WebUI ni des packages système.
- Anciennes URLs docs Letta/Mem0 déplacées/404 ; source figée utilisée. Kokoro sources sous src/, corrigé avant inspection et exécution.
- Recherche d’un modèle québécois léger bornée ; absence non généralisée à tout le Web. Accent/naturel EN ATTENTE.

## Références Mission 11 réutilisées, sans réinvestigation inutile

- [Notes Mission 11](../mission11-preuves/notes-techniques.md)
- [Audio WebUI](../mission11-preuves/openwebui-backend-open_webui-routers-audio-__init__.py)
- [Routes mémoire WebUI](../mission11-preuves/openwebui-memories.py)
- [Voix Kokoro officielles](../mission11-preuves/kokoro-voices.md)
- [README faster-whisper](../mission11-preuves/faster-whisper-README.md)

Ces liens sont à lire depuis ce dossier ; le rapport renvoie aussi aux URLs upstream. Les observations GPU et Docker viennent des missions précédentes, pas d’un nouvel essai.

# Mission 12

- Identifiant : 12.
- Date ou période : 13 octobre 2026, 2026-10-12, 2026-10-12T22:35:33
- Objectif initial : JARVIS — Mission 12 : modules vocaux et mémoire persistante
- Matériel mentionné : Dell
- Logiciels mentionnés : Debian / CUDA / Ollama / Open WebUI / Whisper / Piper / SQLite / FTS5
- État final documentaire : **PARTIEL**. Essais voix CPU et mémoire fictive réussis ; écoute humaine et deux modèles réels non validés.

## Actions et résultats confirmés

Essais voix CPU et mémoire fictive réussis ; écoute humaine et deux modèles réels non validés.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Essais voix CPU et mémoire fictive réussis ; écoute humaine et deux modèles réels non validés.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/jarvis/__init__.py)
- [middleware.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission07-preuves/middleware.py)
- [README.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/README.md)
- [SHA256SUMS](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/SHA256SUMS`
- [after.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/after.json`
- [audio-validation.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/audio-validation.json`
- [audio_worker.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/audio_worker.py)
- [av-pin-download.log](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/av-pin-download.log`
- [av-pin-install.log](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/av-pin-install.log`
- [av15-metadata.txt](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/av15-metadata.txt`
- [before.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/before.json`
- [corpus.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/corpus.json`
- [download-manifest.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/download-manifest.json`
- [ecoute.html](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/ecoute.html`
- [installed-temporary-packages.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/installed-temporary-packages.json`
- [kokoro-guard.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/kokoro-guard.json`
- [kokoro-results.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/kokoro-results.json`
- [kokoro-run.log](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/kokoro-run.log`
- [measurements-summary.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/measurements-summary.json`
- [memory-results.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/memory-results.json`
- [memory-run.log](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/memory-run.log`
- [memory_demo.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/memory_demo.py)
- [OHF-Voice-piper1-gpl.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/OHF-Voice-piper1-gpl.json`
- [faster-whisper.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/faster-whisper.json`
- [ggml-org-whisper.cpp.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/ggml-org-whisper.cpp.json`
- [kokoro-assets.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/kokoro-assets.json`
- [kokoro-onnx.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/kokoro-onnx.json`
- [letta-ai-letta.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/letta-ai-letta.json`
- [mem0ai-mem0.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/mem0ai-mem0.json`
- [onnx-community-Kokoro-82M-v1.0-ONNX-hf.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/onnx-community-Kokoro-82M-v1.0-ONNX-hf.json`
- [pip.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/pip.json`
- [piper-tts.json](../../archives/preuves-controlees/part-031.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/piper-tts.json`
- [rhasspy-piper-voices-hf.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/rhasspy-piper-voices-hf.json`
- [thewh1teagle-kokoro-onnx.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/thewh1teagle-kokoro-onnx.json`
- [tontate-f5-tts-quebec-french-finetune-hf.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/tontate-f5-tts-quebec-french-finetune-hf.json`
- [whisper-base-hf.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/whisper-base-hf.json`
- [whisper-small-hf.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/metadata/whisper-small-hf.json`
- [model-download.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/model-download.log`
- [notes-techniques.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/notes-techniques.md)
- [pip-download.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/pip-download.log`
- [pip-install.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/pip-install.log`
- [piper-siwis-guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/piper-siwis-guard.json`
- [piper-siwis-results.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/piper-siwis-results.json`
- [piper-siwis-run.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/piper-siwis-run.log`
- [piper-tom-guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/piper-tom-guard.json`
- [piper-tom-results.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/piper-tom-results.json`
- [piper-tom-run.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/piper-tom-run.log`
- [requirements-tested-cp313-linux.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/requirements-tested-cp313-linux.txt`
- [run_guarded.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/run_guarded.py)
- [small-download.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/small-download.log`
- [source-manifest.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/source-manifest.json`
- [pyproject.toml](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/OHF-Voice-piper1-gpl/pyproject.toml`
- [revision.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/OHF-Voice-piper1-gpl/revision.txt`
- [__main__.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/OHF-Voice-piper1-gpl/src/piper/__main__.py`
- [voice.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/OHF-Voice-piper1-gpl/src/piper/voice.py`
- [f5-quebec-model-card.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/f5-quebec-model-card.md)
- [LICENSE](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta-code/LICENSE`
- [README.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta-code/README.md)
- [package.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta-code/package.json`
- [revision.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta-code/revision.txt`
- [memory-constraints.ts](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta-code/src/agent/memory-constraints.ts`
- [memory-filesystem.ts](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta-code/src/agent/memory-filesystem.ts`
- [memory.ts](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta-code/src/agent/memory.ts`
- [memory_filesystem.mdx](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta-code/src/agent/prompts/memory_filesystem.mdx`
- [pi-ollama-provider.ts](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta-code/src/backend/dev/pi-ollama-provider.ts`
- [memory.ts](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta-code/src/tools/impl/memory.ts`
- [LICENSE](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta/LICENSE`
- [README.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta/README.md)
- [revision.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/letta-ai-letta/revision.txt`
- [mem0-config.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/mem0-config.py`
- [LICENSE](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/mem0ai-mem0/LICENSE`
- [README.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/mem0ai-mem0/README.md)
- [prompts.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/mem0ai-mem0/mem0/configs/prompts.py`
- [ollama.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/mem0ai-mem0/mem0/embeddings/ollama.py`
- [main.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/mem0ai-mem0/mem0/memory/main.py`
- [storage.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/mem0ai-mem0/mem0/memory/storage.py`
- [qdrant.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/mem0ai-mem0/mem0/vector_stores/qdrant.py`
- [pyproject.toml](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/mem0ai-mem0/pyproject.toml`
- [revision.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/mem0ai-mem0/revision.txt`
- [LICENSE](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/openwebui-v0.12.0/LICENSE`
- [memories.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/openwebui-v0.12.0/backend/open_webui/models/memories.py`
- [memory.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/openwebui-v0.12.0/backend/open_webui/utils/memory.py`
- [pip-pip-__main__.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/pip-pip-__main__.py`
- [pip-pip-_internal-cli-main.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/pip-pip-_internal-cli-main.py`
- [sqlite-license.html](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/sqlite-license.html`
- [LICENSE](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/thewh1teagle-kokoro-onnx/LICENSE`
- [README.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/thewh1teagle-kokoro-onnx/README.md)
- [pyproject.toml](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/thewh1teagle-kokoro-onnx/pyproject.toml`
- [revision.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/thewh1teagle-kokoro-onnx/revision.txt`
- [__init__.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/thewh1teagle-kokoro-onnx/src/kokoro_onnx/__init__.py`
- [config.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/thewh1teagle-kokoro-onnx/src/kokoro_onnx/config.py`
- [tokenizer.py](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/sources/thewh1teagle-kokoro-onnx/src/kokoro_onnx/tokenizer.py`
- [static-review.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/static-review.json`
- [stt-first-attempt-stt-guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/stt-first-attempt-stt-guard.json`
- [stt-first-attempt-stt-run.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/stt-first-attempt-stt-run.log`
- [stt-guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/stt-guard.json`
- [stt-results.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/stt-results.json`
- [stt-run.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/stt-run.log`
- [stt-second-attempt-stt-guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/stt-second-attempt-stt-guard.json`
- [stt-second-attempt-stt-run.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/stt-second-attempt-stt-run.log`
- [stt-small-guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/stt-small-guard.json`
- [stt-small-results.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/stt-small-results.json`
- [stt-small-run.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/stt-small-run.log`
- [wheel-manifest.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-manifest.json`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/anyio-4.15.1-py3-none-any/anyio-4.15.1.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/anyio-4.15.1-py3-none-any/anyio-4.15.1.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/attrs-26.1.0-py3-none-any/attrs-26.1.0.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/av-19.0.1-cp312-abi3-manylinux_2_28_x86_64/av-19.0.1.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/av-19.0.1-cp312-abi3-manylinux_2_28_x86_64/av-19.0.1.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/click-8.5.0-py3-none-any/click-8.5.0.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/cloudpickle-3.1.2-py3-none-any/cloudpickle-3.1.2.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/ctranslate2-4.8.2-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64/ctranslate2-4.8.2.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/ctranslate2-4.8.2-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64/ctranslate2-4.8.2.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/dlinfo-2.0.0-py3-none-any/dlinfo-2.0.0.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/espeakng_loader-0.2.4-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64/espeakng_loader-0.2.4.dist-info/METADATA`
- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/espeakng_loader-0.2.4-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64/espeakng_loader/__init__.py)
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/faster_whisper-1.2.1-py3-none-any/faster_whisper-1.2.1.dist-info/METADATA`
- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/faster_whisper-1.2.1-py3-none-any/faster_whisper/__init__.py)
- [audio.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/faster_whisper-1.2.1-py3-none-any/faster_whisper/audio.py)
- [feature_extractor.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/faster_whisper-1.2.1-py3-none-any/faster_whisper/feature_extractor.py)
- [tokenizer.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/faster_whisper-1.2.1-py3-none-any/faster_whisper/tokenizer.py)
- [vad.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/faster_whisper-1.2.1-py3-none-any/faster_whisper/vad.py)
- [version.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/faster_whisper-1.2.1-py3-none-any/faster_whisper/version.py)
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/filelock-4.1.1-py3-none-any/filelock-4.1.1.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/flatbuffers-25.12.19-py2.py3-none-any/flatbuffers-25.12.19.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/fsspec-2026.9.0-py3-none-any/fsspec-2026.9.0.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/h11-0.16.0-py3-none-any/h11-0.16.0.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/hf_xet-1.7.0-cp38-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64/hf_xet-1.7.0.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/httpcore2-2.13.1-py3-none-any/httpcore2-2.13.1.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/httpx2-2.13.1-py3-none-any/httpx2-2.13.1.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/httpx2-2.13.1-py3-none-any/httpx2-2.13.1.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/huggingface_hub-2.2.0-py3-none-any/huggingface_hub-2.2.0.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/huggingface_hub-2.2.0-py3-none-any/huggingface_hub-2.2.0.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/idna-3.20-py3-none-any/idna-3.20.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/idna-3.20-py3-none-any/idna-3.20.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/joblib-1.6.0-py3-none-any/joblib-1.6.0.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/kokoro_onnx-0.6.1-py3-none-any/kokoro_onnx-0.6.1.dist-info/METADATA`
- [chunker.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/kokoro_onnx-0.6.1-py3-none-any/kokoro_onnx/chunker.py)
- [log.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/kokoro_onnx-0.6.1-py3-none-any/kokoro_onnx/log.py)
- [pauses.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/kokoro_onnx-0.6.1-py3-none-any/kokoro_onnx/pauses.py)
- [session.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/kokoro_onnx-0.6.1-py3-none-any/kokoro_onnx/session.py)
- [sliding.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/kokoro_onnx-0.6.1-py3-none-any/kokoro_onnx/sliding.py)
- [trim.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/kokoro_onnx-0.6.1-py3-none-any/kokoro_onnx/trim.py)
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/numpy-2.5.4-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64/numpy-2.5.4.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/numpy-2.5.4-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64/numpy-2.5.4.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/onnxruntime-1.31.0-cp313-cp313-manylinux_2_28_x86_64/onnxruntime-1.31.0.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/onnxruntime-1.31.0-cp313-cp313-manylinux_2_28_x86_64/onnxruntime-1.31.0.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/packaging-26.3-py3-none-any/packaging-26.3.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/pathvalidate-3.3.1-py3-none-any/pathvalidate-3.3.1.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/phonemizer-3.4.0-py3-none-any/phonemizer-3.4.0.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/phonemizer-3.4.0-py3-none-any/phonemizer-3.4.0.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/pip-26.2.1-py3-none-any/pip-26.2.1.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/pip-26.2.1-py3-none-any/pip-26.2.1.dist-info/entry_points.txt`
- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/__init__.py)
- [audio_playback.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/audio_playback.py)
- [config.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/config.py)
- [const.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/const.py)
- [download_voices.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/download_voices.py)
- [g2pw_onnx.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/g2pw_onnx.py)
- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/hebrew/__init__.py)
- [hebrew_ipa.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/hebrew/hebrew_ipa.py)
- [http_server.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/http_server.py)
- [patch_voice_with_alignment.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/patch_voice_with_alignment.py)
- [phoneme_ids.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/phoneme_ids.py)
- [phonemize_chinese.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/phonemize_chinese.py)
- [phonemize_espeak.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/phonemize_espeak.py)
- [phonemize_hebrew.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/phonemize_hebrew.py)
- [phonemize_japanese.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/phonemize_japanese.py)
- [phonemize_thai.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/phonemize_thai.py)
- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/tashkeel/__init__.py)
- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/__init__.py)
- [__main__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/__main__.py)
- [export_generator.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/export_generator.py)
- [export_onnx.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/export_onnx.py)
- [infer_torch.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/infer_torch.py)
- [attentions.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/attentions.py)
- [commons.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/commons.py)
- [config.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/config.py)
- [dataset.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/dataset.py)
- [lightning.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/lightning.py)
- [losses.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/losses.py)
- [mel_processing.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/mel_processing.py)
- [models.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/models.py)
- [modules.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/modules.py)
- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/monotonic_align/__init__.py)
- [setup.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/monotonic_align/setup.py)
- [mos.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/mos.py)
- [transforms.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/transforms.py)
- [utils.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/train/vits/utils.py)
- [voice.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper/voice.py)
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper_tts-1.8.0.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/piper_tts-1.8.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64/piper_tts-1.8.0.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/protobuf-7.36.2-cp310-abi3-manylinux2014_x86_64/protobuf-7.36.2.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/pyyaml-6.0.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64/pyyaml-6.0.3.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/tokenizers-0.23.3-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64/tokenizers-0.23.3.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/tqdm-4.70.1-py3-none-any/tqdm-4.70.1.dist-info/METADATA`
- [entry_points.txt](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/tqdm-4.70.1-py3-none-any/tqdm-4.70.1.dist-info/entry_points.txt`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/truststore-0.10.4-py3-none-any/truststore-0.10.4.dist-info/METADATA`
- [METADATA](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/wheel-review/typing_extensions-4.16.0-py3-none-any/typing_extensions-4.16.0.dist-info/METADATA`
- [mission12.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12.md)

## Références et dépendances

10, 11, 11-P, 12-P, 13B. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [mission12.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12.md)

13 octobre 2026, heure de Paris — recherches et essais CPU temporaires, sans modification du cœur JARVIS.

## 1. Synthèse exécutive

**GO sous conditions pour une première version modulaire : faster-whisper `small` multilingue CPU/int8, Piper et mémoire SQLite/FTS5 dédiée, pilotés par une seule passerelle JARVIS.** La voix **Piper `fr_FR-tom-medium` est le choix technique provisoire** ; Siwis et Kokoro restent disponibles à l’écoute. Le choix définitif du timbre et du naturel demeure **EN ATTENTE d’écoute humaine**, pas d’un problème d’installation.

Résultats concrets : **9 fichiers WAV français générés**, **9 transcriptions par Whisper base et 9 par small**, **1 test de silence small**, **16 contrôles de mémoire réussis** avec données fictives. Les essais ont réellement fonctionné sur Debian 13/Python 3.13, exclusivement sur CPU, dans `/tmp/jarvis-m12-EC3FOY`. Aucun appel de génération, d’embedding ou de téléchargement à Ollama. La mémoire commune est démontrée avec **deux profils simulés**, pas deux modèles réels.

La voix québécoise est une limite explicite : aucun `fr_CA` dans le catalogue officiel Piper inspecté ; Kokoro `ff_siwis` est français, non annoncé québécois. Un finetune **F5-TTS québécois** existe, mais ses poids sont **CC-BY-NC-4.0**, volumineux et non testés. Ne pas confondre vocabulaire québécois dans une phrase et accent québécois du locuteur.


### [notes-techniques.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/notes-techniques.md)

## Périmètre réel

Tests : synthèse fichiers Piper et Kokoro ONNX ; transcription fichiers faster-whisper ; démo originale SQLite avec profils simulés. Pas de conversation Ollama, service WebUI, microphone ni agent Mem0/Letta exécutés. Les packages tiers ont été inspectés avant leurs chemins d’exécution ; revue ciblée, pas certification de binaries.

L’inférence refuse les sockets connect/bind, emploie des fichiers locaux et CPU. `run_guarded.py` échantillonne VmRSS toutes les 20 ms et borne le worker à 180 s/2 Gio RSS. `audio_worker.py` limite l’affinité à deux CPUs et les threads, garde les caches dans le temporaire. Les modèles vocaux ne sont pas des modèles Ollama.

## Mesures et limites

Les JSON par moteur conservent temps par extrait, durée audio, RTF et texte. Les JSON guard conservent pic RSS échantillonné et code retour. Pic non continu, court dépassement non exclu ; pas de benchmark thermique ni charge avec Qwen. Piper charge puis recrée sa session CPU pour fixer les threads : son chargement est double dans ce test. Piper et Kokoro ne sont pas au même sample rate, et Kokoro est quantifié int8. Corpus de trois textes répétés dans trois voix ; fichiers TTS synthétiques, aucune voix humaine enregistrée.


### [README.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission12-preuves/README.md)

Début : 2026-10-12 22:18:28 UTC (13 octobre 00:18:28 Paris). Finalisation : 2026-10-12T22:35:33.161473+00:00. Recherche et essais terminés en moins d’une heure ; plafond 4 h + 1 h respecté, aucune prolongation artificielle.

- Rapport (référence dans l’original : `../mission12.md`)
- Lecteur local (référence dans l’original : `ecoute.html`) et `audio/` : neuf WAV synthétisés, trois voix, trois textes identiques.
- Corpus (référence dans l’original : `corpus.json`), validation WAV (référence dans l’original : `audio-validation.json`), `silence-fixture.wav` : fixture technique, pas voix candidate.
- Synthèse des mesures (référence dans l’original : `measurements-summary.json`), `*-results.json`, `*-guard.json`, `*-run.log` : succès et traces reproductibles.
- Mémoire 16/16 (référence dans l’original : `memory-results.json`), source démo (référence dans l’original : `memory_demo.py`), bases `*-fictive.sqlite` / `*-fictif.sqlite` : données fictives exclusivement.
- Notes techniques (référence dans l’original : `notes-techniques.md`), revue statique (référence dans l’original : `static-review.json`), `sources/`, `wheel-review/` : code/documentation publique examinés, licences préservées dans sources disponibles.
- Manifest sources (référence dans l’original : `source-manifest.json`), manifest modèles (référence dans l’original : `download-manifest.json`), manifest wheels (référence dans l’original : `wheel-manifest.json`), `metadata/` : snapshots, SHA-256, dates/versions.
- Lock temporaire testé (référence dans l’original : `requirements-tested-cp313-linux.txt`), `installed-temporary-packages.json` : 32 distributions, venv uniquement.

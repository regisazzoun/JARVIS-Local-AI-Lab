# Mission 13A

- Identifiant : 13A.
- Date ou période : 13 octobre 2026, 2026-10-13T10:15:24
- Objectif initial : JARVIS — Mission 13A : installation durable et isolée du socle vocal
- Matériel mentionné : Mac mini / RTX 3090
- Logiciels mentionnés : Debian / T2Linux / CUDA / NVIDIA / Ollama / Open WebUI / Whisper / Piper
- État final documentaire : **VALIDÉ**. Deux cycles fichiers Piper/Whisper réels, hors réseau, installés durablement ; validation limitée aux fichiers audio.

## Actions et résultats confirmés

Deux cycles fichiers Piper/Whisper réels, hors réseau, installés durablement ; validation limitée aux fichiers audio.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Deux cycles fichiers Piper/Whisper réels, hors réseau, installés durablement ; validation limitée aux fichiers audio.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/jarvis/__init__.py)
- [A-stt.guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/A-stt.guard.json`
- [A-stt.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/A-stt.log`
- [A-tts.guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/A-tts.guard.json`
- [A-tts.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/A-tts.log`
- [D-stt.guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/D-stt.guard.json`
- [D-stt.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/D-stt.log`
- [D-tts.guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/D-tts.guard.json`
- [D-tts.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/D-tts.log`
- [PROCEDURES.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/PROCEDURES.md)
- [README.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/README.md)
- [SHA256SUMS](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/SHA256SUMS`
- [acceptance-checks.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/acceptance-checks.json`
- [acceptance-runs.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/acceptance-runs.json`
- [after.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/after.json`
- [audit.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/audit.py)
- [jarvis-ollama.service](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/backup-configs/etc/systemd/system/jarvis-ollama.service`
- [jarvis-open-webui.service](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/backup-configs/etc/systemd/system/jarvis-open-webui.service`
- [compose.yaml](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/backup-configs/home/adminjarvis/JARVIS/open-webui/compose.yaml`
- [before.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/before.json`
- [checksums-verification.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/checksums-verification.log`
- [final-disk.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/final-disk.json`
- [finalize.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/finalize.py)
- [gpu-during-tests.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/gpu-during-tests.json`
- [incident-A-stt.guard.json](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/incident-A-stt.guard.json`
- [incident-A-stt.log](../../archives/preuves-controlees/part-032.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/incident-A-stt.log`
- [installation-SHA256SUMS](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/installation-SHA256SUMS`
- [installation-integrity.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/installation-integrity.json`
- [installed-models.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/installed-models.json`
- [measurements-summary.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/measurements-summary.json`
- [offline-namespace.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/offline-namespace.json`
- [pip-check.log](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/pip-check.log`
- [pip-install.log](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/pip-install.log`
- [pip-tooling.log](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/pip-tooling.log`
- [prepare_install.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/prepare_install.py)
- [requirements-voice-cp313-linux.txt](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/requirements-voice-cp313-linux.txt`
- [run-offline](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/run-offline`
- [run_acceptance.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/run_acceptance.py)
- [run_guarded.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/run_guarded.py)
- [selected-dependencies.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/selected-dependencies.json`
- [jarvis-voice-stt.service](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/systemd/jarvis-voice-stt.service`
- [jarvis-voice-tts.service](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/systemd/jarvis-voice-tts.service`
- [verified-inputs.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/verified-inputs.json`
- [versions.json](../../archives/preuves-controlees/part-033.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/versions.json`
- [voice_worker.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/voice_worker.py)
- [mission13a.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a.md)

## Références et dépendances

11, 12, 13A-P, 13B. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [mission13a.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a.md)

13 octobre 2026 — Mac mini 2018, Debian 13 T2Linux. Finalisation : 2026-10-13T10:15:24.045376+02:00, heure de Paris.

## 1. Bilan et réception

**RÉUSSI : les sept critères de réception sont satisfaits dans le périmètre des tests fichiers.** Whisper small et Piper Tom sont installés et réellement exécutés depuis `/opt/jarvis/voice`, sur disque permanent. Deux cycles synthèse/transcription ont réussi avec quatre processus moteurs distincts, sans accès réseau et sans chargement Ollama. Les quatre processus se sont terminés. Aucun moteur permanent ni démarrage automatique activé. Mission 13B non commencée.

| Critère | Résultat et preuve |
|---|---|
| 1. Moteurs dans un répertoire permanent | **RÉUSSI**, `/opt/jarvis/voice`, modèles copies réelles et venv propre sans liens vers `/tmp` |
| 2. Arrêt et relancement | **RÉUSSI**, nouveaux PID pour D-tts et D-stt après terminaison des processus A |

### [PROCEDURES.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/PROCEDURES.md)

Installation : `/opt/jarvis/voice`, Debian 13 T2Linux, Python 3.13.5. Whisper small multilingue et Piper Tom uniquement. Aucun daemon, port ou démarrage automatique. Dépendances figées dans `config/requirements-voice-cp313-linux.txt`; pip local figé séparément dans `config/requirements-tooling.txt`. Wheels vérifiés conservés pour une réinstallation hors ligne du seul venv.

## Démarrage manuel et arrêt

Depuis un terminal de l’utilisateur adminjarvis :

```bash
/opt/jarvis/voice/scripts/run-offline tts /opt/jarvis/voice/logs/manuel-tts --wav /opt/jarvis/voice/logs/manuel.wav
/opt/jarvis/voice/scripts/run-offline stt /opt/jarvis/voice/logs/manuel-stt --wav /opt/jarvis/voice/logs/manuel.wav
```

### [README.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission13a-preuves/README.md)

Rapport (référence dans l’original : `../mission13a.md`) · Procédures (référence dans l’original : `PROCEDURES.md`)

- `before.json`, `after.json`, `acceptance-checks.json` : intégrité configurations, 29 fichiers modèles Ollama, dpkg, kernel, services, sockets et GET Ollama sans génération.
- `verified-inputs.json`, `installed-models.json`, `requirements-voice-cp313-linux.txt`, `versions.json`, `installation-integrity.json`, `final-disk.json` : versions, chemins, SHA-256, disque, liens et caches.
- `A-tom.wav`, `D-tom.wav` : synthèses locales Piper Tom ; `A-tts`, `A-stt`, `D-tts`, `D-stt` logs/results/guards et measurements-summary.
- `incident-A-stt*` : assertion initiale trop stricte, corrigée pour int8_float32 CPU. Les logs de l’échec ne sont pas écrasés.
- `gpu-during-tests.json`, `offline-namespace.json` : relevés nvidia-smi et test isolation réseau noyau.
- `pip-install.log`, `pip-tooling.log`, `pip-check.log`, `systemd-verify.log` : installation locale sans index, cohérence dépendances, vérification statique propositions systemd.
- `systemd/`, `PROCEDURES.md`, scripts Python et lanceur : reproductibilité ; aucune unité installée/activée.
- `backup-configs/` : copies privées 0700/0600, notamment .env contenant des secrets. Ne pas partager. Les sauvegardes privées sont exclues de SHA256SUMS public.

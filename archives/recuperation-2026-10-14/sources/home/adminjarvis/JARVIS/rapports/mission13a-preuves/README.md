# Mission 13A — preuves

[Rapport](../mission13a.md) · [Procédures](PROCEDURES.md)

- `before.json`, `after.json`, `acceptance-checks.json` : intégrité configurations, 29 fichiers modèles Ollama, dpkg, kernel, services, sockets et GET Ollama sans génération.
- `verified-inputs.json`, `installed-models.json`, `requirements-voice-cp313-linux.txt`, `versions.json`, `installation-integrity.json`, `final-disk.json` : versions, chemins, SHA-256, disque, liens et caches.
- `A-tom.wav`, `D-tom.wav` : synthèses locales Piper Tom ; `A-tts`, `A-stt`, `D-tts`, `D-stt` logs/results/guards et measurements-summary.
- `incident-A-stt*` : assertion initiale trop stricte, corrigée pour int8_float32 CPU. Les logs de l’échec ne sont pas écrasés.
- `gpu-during-tests.json`, `offline-namespace.json` : relevés nvidia-smi et test isolation réseau noyau.
- `pip-install.log`, `pip-tooling.log`, `pip-check.log`, `systemd-verify.log` : installation locale sans index, cohérence dépendances, vérification statique propositions systemd.
- `systemd/`, `PROCEDURES.md`, scripts Python et lanceur : reproductibilité ; aucune unité installée/activée.
- `backup-configs/` : copies privées 0700/0600, notamment .env contenant des secrets. Ne pas partager. Les sauvegardes privées sont exclues de SHA256SUMS public.
- `SHA256SUMS` : rapport et preuves partageables ; `installation-SHA256SUMS` : toutes les ressources installées sauf journaux/caches évolutifs.

Les scripts audit/install sont des traces de cette mission, pas une instruction de réinstallation sur un répertoire existant. Les tests réseau isolés fonctionnent via le lanceur permanent. Aucun serveur, micro ni client conversationnel.

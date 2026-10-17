> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/MISSION-13E-INSTALLATION.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 13E — installation

Installation réelle sous `/opt/jarvis/conversation`, Python 3.13 isolé. Backend bibliothèque standard, SQLite/FTS5, workers vocaux utilisant l’environnement 13A existant. Versions constatées : faster-whisper 1.2.1, Piper 1.8.0, onnxruntime 1.31.0, PyAV 15.1.0. Aucun paquet système ni pilote installé. Dépendances de tests isolées : Playwright 1.63.0, pyee 13.0.1, greenlet 3.5.6, typing-extensions 4.16.0 ; Chromium 153.0.8010.12 et FFmpeg de test téléchargés dans le cache utilisateur, pas dans les services existants.

Arborescence : `jarvis/` backend, `static/` interface, `identity/JARVIS-v1.md`, `config/13e.json` configuration locale, `runtime/` données et secrets privés, `runtime/backups/`, `scripts/`, `tests/`, `deployment/`, `docs/`. Le dossier d’origine 13B/13C reste conservé avec sauvegarde privée avant modification. Venv neuf créé sans pip ; installation des outils de test dans ce venv seulement.

Unités installées : `/etc/systemd/system/jarvis-conversation.service`, `jarvis-memory-backup.service` et `jarvis-memory-backup.timer`. Passerelle non privilégiée, uniquement `[ADRESSE PRIVÉE EXPURGÉE]:8765`, restart on-failure, NoNewPrivileges, système en lecture seule sauf runtime, KillMode=control-group. Après test manuel et essais intégrés, service et timer activés. `systemctl daemon-reload` n’a pas redémarré les services existants.

Configuration : modèle principal Qwen, contexte demandé 8192 tokens, sortie 512 tokens, timeout Ollama 180 s, voix 120 s, enregistrement 45 s, charge audio 8 Mo, français CPU/int8. Un verrou évite les générations concurrentes internes ; les demandes Open WebUI restent extérieures à ce verrou. L’identité est dans le code versionné et inaccessible aux outils du LLM.

Authentification mono-utilisateur : sel et dérivation PBKDF2-SHA256, 300 000 itérations, cookie HttpOnly/SameSite=Strict, session 8 h en RAM, limitation des tentatives, contrôles Host/Origin et en-tête de mutation obligatoire. Secrets runtime en permissions 0600, dossier 0700. Pas de token dans le code source. Un redémarrage invalide les connexions, sans altérer mémoire et identité.

HTTPS privé : exemple `deployment/https-private.nginx.example` préparé uniquement. Pour une future activation, certificat reconnu par les clients, adresse VPN vérifiée, origine/Host exacts en allowlist et Secure cookie. Ne pas lancer cet exemple tel quel ; SSH, Tailscale et pare-feu n’ont pas été changés dans 13E.

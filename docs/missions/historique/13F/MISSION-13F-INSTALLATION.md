> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/MISSION-13F-INSTALLATION.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 13F — installation réellement effectuée

Installation existante `/opt/jarvis/conversation` conservée, venv passerelle et venv vocal réutilisés. Aucun apt upgrade, pip système, modèle téléchargé ou pilote remplacé. Python 3.13.5 ; Bubblewrap 0.12.0 et Playwright 1.63.0 étaient déjà installés. Whisper 1.2.1, CTranslate2 4.8.2, Piper 1.8.0, ONNX Runtime CPU 1.31.0, PyAV 15.1.0 revérifiés.

1. Lire la roadmap GitHub et les rapports 13A/13B/13C/13E ; auditer unités, API, GPU, SQLite, fichiers actifs, journaux, tests.
2. Sauvegarde SQLite Online Backup, archive privée du code/config/runtime sans recopier le venv, copies des unités. Répertoire privé hors publication. Contrôle d'intégrité avant migration.
3. Ajouter preferences.py, agent.py, identité v2, AudioWorklet et tests ; modifier memory.py, core.py, tools.py, server.py, app.js/index.html. Migration additive v2 → v3, aucun DROP des données historiques.
4. Configuration active : `config/13e.json` garde son nom historique ; num_predict 1100, num_ctx 8192, tool_rounds 32, voix courte/résumé activé, lab_enabled true, identité v2. Authentification, bind [ADRESSE PRIVÉE EXPURGÉE]:8765 et santé WebUI existants préservés. Ce fichier actif contient des paramètres privés et n'est pas publié.
5. Unité conversation : ajouter AF_NETLINK, TasksMax=128 et MemoryMax=2G. Conserver User, NoNewPrivileges, ProtectSystem=strict, ProtectHome=read-only, ReadWritePaths=runtime et capabilities vides. Recharger systemd et redémarrer uniquement la passerelle à chaque changement nécessitant cette reprise.
6. Exécuter les tests puis corriger les anomalies réelles ; vérifier les indices, la sauvegarde et la restauration, le restart/relogin et la préservation des données.

Commandes réellement utilisées :
```sh
python3 -m py_compile /opt/jarvis/conversation/jarvis/*.py
cd /opt/jarvis/conversation
.venv/bin/python -m unittest discover -s tests -p 'test*.py'
sudo -n systemctl daemon-reload
sudo -n systemctl restart jarvis-conversation.service
sudo -n systemctl start jarvis-memory-backup.service
systemctl is-active jarvis-conversation jarvis-ollama jarvis-open-webui
sudo -n systemd-analyze verify /etc/systemd/system/jarvis-conversation.service
```

Les tests navigateur/API/autonomie sont exécutés depuis tests/ avec le venv existant. L'authentification est lue uniquement depuis le fichier privé ; aucune valeur n'est intégrée au code ou aux rapports. Les tests d'autonomie nécessitent une fixture neuve ; ne pas les relancer sur une configuration déjà réparée en prétendant reproduire la panne.

La publication contient le code et des exemples sûrs, pas la configuration active, les venv, les modèles, runtime, archives, bases ni preuves privées. Les unités publiées sont des templates `.service.in` : remplacer le compte local à l'installation, sans reprendre un identifiant réel dans GitHub. Les modèles vocaux/Ollama restent des prérequis locaux, pas redistribués. Avant toute réinstallation, suivre REPRISE et sauvegarder l'état courant ; aucun remplacement aveugle de runtime.

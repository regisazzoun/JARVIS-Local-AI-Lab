# Socle vocal JARVIS — Mission 13A

Installation : `/opt/jarvis/voice`, Debian 13 T2Linux, Python 3.13.5. Whisper small multilingue et Piper Tom uniquement. Aucun daemon, port ou démarrage automatique. Dépendances figées dans `config/requirements-voice-cp313-linux.txt`; pip local figé séparément dans `config/requirements-tooling.txt`. Wheels vérifiés conservés pour une réinstallation hors ligne du seul venv.

## Démarrage manuel et arrêt

Depuis un terminal de l’utilisateur adminjarvis :

```bash
/opt/jarvis/voice/scripts/run-offline tts /opt/jarvis/voice/logs/manuel-tts --wav /opt/jarvis/voice/logs/manuel.wav
/opt/jarvis/voice/scripts/run-offline stt /opt/jarvis/voice/logs/manuel-stt --wav /opt/jarvis/voice/logs/manuel.wav
```

Chaque commande démarre un seul moteur, traite le fichier, écrit `.log`, `.guard.json` et `.result.json`, puis termine tous ses processus. Attendre le retour au terminal avant la suivante. CTRL+C interrompt le lancement en premier plan ; le superviseur arrête le groupe du moteur. Pour un processus lancé en arrière-plan, envoyer SIGTERM au PID du lanceur identifié pour cette seule invocation, puis vérifier l’arrêt avec `pgrep -af '/opt/jarvis/voice/(scripts|venv)'`. Ne pas utiliser `killall python` ou arrêter les services JARVIS existants.

Le lanceur exige `sudo -n` uniquement pour créer un namespace réseau vide. Il redescend immédiatement en UID/GID 1000, retire toutes les capabilities et impose no-new-privileges avant Python. Il n’ouvre aucun port. Ne pas appeler directement le worker si l’on veut conserver cette isolation réseau noyau. Le hook Python refuse aussi connect/bind. CPU uniquement, affinité sur deux processeurs logiques, deux threads d’inférence, priorité réduite. Watchdog : 180 secondes, RSS 2 Gio et RAM disponible minimale 6 Gio. Les chemins des modèles sont explicites, Whisper `local_files_only=True`, `language='fr'`, `compute_type='int8'`. CTranslate2 rapporte `int8_float32` : poids quantifiés int8 et opérations flottantes CPU ; cela ne signifie pas utilisation de GPU.

Le texte TTS par défaut est français de France. Un autre texte français peut être fourni avec `--text 'Votre phrase française.'` aux deux commandes pour obtenir la comparaison correspondante. Aucun lexique québécois ajouté. Le WAV est généré et décodé, pas lu automatiquement sur les haut-parleurs. L’écoute humaine peut se faire en ouvrant le WAV dans un lecteur local ; le volume et le naturel ne sont pas qualifiés par les mesures automatiques.

Piper construit directement une unique session ONNX CPU bornée à deux threads via l’API Piper 1.8.0 ; aucun patch du package. Les ressources intégrées espeak restent celles du wheel. Les caches ONNX Runtime sont limités à `logs/cache`; ils ne sont pas des modèles téléchargés. Ne pas remplacer le lock par des contraintes larges : PyAV 19.0.1 a échoué en Mission 12, PyAV 15.1.0 est imposé.

## Vérification locale

```bash
/opt/jarvis/voice/venv/bin/python -m pip check
/opt/jarvis/voice/venv/bin/python -m pip list --disable-pip-version-check
systemctl is-active jarvis-ollama.service jarvis-open-webui.service
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv
```

L’environnement Python système est utilisé comme interpréteur de base, sans paquets système supplémentaires. Aucun lien de modèle ni de package ne pointe sur `/tmp`. Les modèles et les wheels sont sur le disque racine, non sur tmpfs. Pas de mise à jour automatique ni de récupération de modèle lors de l’inférence.

## Désinstallation limitée — non exécutée

1. Obtenir la validation avant suppression, arrêter uniquement les nouvelles commandes vocales et vérifier leur absence.
2. Conserver le rapport, les WAV et `mission13a-preuves` hors de `/opt/jarvis/voice`. Exporter les journaux si souhaité.
3. Vérifier que `/opt/jarvis/voice` est exactement le répertoire créé par Mission 13A, pas un lien symbolique, et qu’il n’a pas reçu d’autres composants depuis. Aucun service vocal n’a été installé ; aucune commande systemctl sur les services existants n’est nécessaire.
4. Après validation explicite, supprimer uniquement ce répertoire avec `sudo rm -rf -- /opt/jarvis/voice`. Ne supprimer ni `/opt/jarvis`, ni des caches globaux, ni des modèles Ollama, ni le venv Mission 12. Ne pas lancer cette étape depuis un script automatique.
5. Vérifier que jarvis-ollama et jarvis-open-webui restent actifs. Les sauvegardes de configurations sont documentaires : ne pas les restaurer sur l’installation active puisque rien n’a été changé.

## Propositions systemd pour la suite

`docs/systemd/jarvis-voice-tts.service` et `jarvis-voice-stt.service` sont des propositions de tests fichier Type=oneshot, validées uniquement par `systemd-analyze verify`. Elles restent dans la documentation : non copiées dans `/etc/systemd/system`, non chargées, non démarrées, non activées. Elles n’ont aucune section Install.

Elles imposent réseau privé, devices privés, aucun privilège/capability, système de fichiers en lecture seule hors `logs`, 2 Gio de RAM et 200 % CPU. L’affinité de deux CPU est aussi imposée par le worker. La proposition STT attend le WAV produit au préalable par TTS. Un service résident et son transport local restent à concevoir pour Mission 13B après validation ; aucune API ni passerelle n’a été développée ici. L’API Piper doit rester compatible avec la version figée lors de cette future intégration.

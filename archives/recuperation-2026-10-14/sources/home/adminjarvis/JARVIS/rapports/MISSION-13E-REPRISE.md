# Mission 13E — reprise et sauvegarde

Le service et le timer sont activés au démarrage ; reboot complet non exécuté. Reprise de la seule passerelle testée réellement :
```bash
sudo systemctl restart jarvis-conversation.service
systemctl is-active jarvis-conversation.service
curl --max-time 5 http://localhost:8765/api/health
```
Après restart, se reconnecter : cookies précédents invalidés, historique et souvenirs conservés. Arrêt/lancement : `sudo systemctl stop/start jarvis-conversation.service`. Ne pas redémarrer Ollama/Open WebUI pour un incident de passerelle.

Sauvegarde manuelle :
```bash
/opt/jarvis/conversation/scripts/backup-now
systemctl list-timers jarvis-memory-backup.timer
```
Sauvegardes privées dans `runtime/backups`, permissions 0600, SQLite Online Backup utilisable pendant fonctionnement. Plan quotidien validé par lancement de l’unité et restauration du backup vers une base de test. Pas de purge automatique : surveiller l’espace et définir une rétention avant suppression de sauvegardes privées.

Restauration sûre, sans écraser la base active :
```bash
cd /opt/jarvis/conversation
scripts/memory restore-test /CHEMIN_PRIVE/backup.sqlite /tmp/jarvis-restauration-nouvelle.sqlite
```
La destination doit être nouvelle ; l’intégrité est contrôlée. Avant une reprise depuis la copie, arrêter uniquement la passerelle, sauvegarder encore l’état actuel, puis tester manuellement `scripts/start --db /tmp/jarvis-restauration-nouvelle.sqlite`. Le venv et la version de code doivent accepter le schéma restauré. Ne jamais remplacer la base réelle sans conserver son état le plus récent.

Configurations 13E, identité et code sont versionnés localement. Sauvegarde initiale 13B/13C conservée dans le dossier privé de mission ; les données plus récentes de 13E doivent rester sauvegardées même si l’on revient à un ancien code. Le code v1 refuse le schéma v2 : ne pas ouvrir la nouvelle base avec le code 13B ancien. L’ancien dossier home reste disponible pour inspection, pas pour une migration inverse destructive.

Journaux : journalctl unité ; contenu personnel et identifiants de connexion non journalisés par les requêtes. KillMode=control-group évite les workers orphelins lors d’un arrêt systemd ; subprocess timeout tue puis attend le worker et nettoie ses fichiers temporaires. Aucun processus vocal résident n’est requis.

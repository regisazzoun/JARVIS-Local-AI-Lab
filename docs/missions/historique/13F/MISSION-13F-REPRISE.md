> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/MISSION-13F-REPRISE.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 13F — reprise et retour arrière

## Diagnostic sans mutation globale

```sh
systemctl status jarvis-conversation.service --no-pager
curl -fsS http://[ADRESSE PRIVÉE EXPURGÉE]:8765/api/health
systemctl is-active jarvis-ollama jarvis-open-webui
systemctl is-enabled jarvis-conversation.service jarvis-memory-backup.timer
```

Les logs propres sont dans runtime/service.log ; journalctl dépend des droits Unix. Vérifier les APIs via l'interface authentifiée. Le nom config/13e.json est historique : c'est bien la configuration active mise à jour en 13F. Le modèle reste sur l'API Ollama existante.

Si la passerelle seule est défaillante, sauvegarder l'état courant puis redémarrer uniquement jarvis-conversation.service. Attendre api/health, se reconnecter (sessions invalidées au restart), reprendre l'historique et vérifier les préférences. Ne pas redémarrer Ollama/WebUI ou la machine sans diagnostic justifiant cette action. La reprise automatique on-failure reste active.

Si Bubblewrap échoue NETLINK_ROUTE sous systemd, vérifier AF_NETLINK dans l'unité ; ne pas supprimer NoNewPrivileges/capability restrictions pour contourner le défaut. Si une commande échoue, lire returncode/stdout et ajuster dans /work. Le quota du laboratoire peut être récupéré en retirant uniquement les fichiers d'essai identifiés ; ne jamais utiliser ce mode pour des données personnelles.

## Sauvegarde/restauration

Sauvegardes privées quotidiennes sous runtime/backups via timer ; contrôle manuel réel :
```sh
sudo -n systemctl start jarvis-memory-backup.service
systemctl show jarvis-memory-backup.service -p Result -p ExecMainStatus
```

Pour tester une sauvegarde, restaurer vers un **nouveau fichier** avec Memory.restore(source, destination), contrôler PRAGMA integrity_check, foreign_key_check, FTS5 et préférences. Ne pas lancer un second serveur sur cette copie. La restauration finale a été testée réellement vers une destination neuve et n'a jamais remplacé la base active.

Avant toute restauration en production : conserver une sauvegarde nouvelle de l'état actuel, arrêter seulement la passerelle, choisir la sauvegarde approuvée et préserver les messages arrivés depuis celle-ci. Le helper refuse d'écraser une destination existante. Une restauration ancienne perdrait les nouveaux échanges : ne pas l'exécuter aveuglément. Ne pas partager les exports/snapshots.

## Retour arrière du code

Archive avant mission et SQLite v2 conservés dans le répertoire privé de sauvegarde, hors GitHub. Le schéma actif est v3 : le code memory.py de 13E refuse une base plus récente. Pour un repli non destructif de l'interface/core/outils, conserver le repository mémoire v3 et la base courante, restaurer sélectivement les autres fichiers, puis retester. Ne pas copier l'ancienne archive avec runtime sur les données actuelles. Le rollback intégral vers v2 exige une préparation et réconciliation des nouveaux échanges ; il n'est pas testé ni automatiquement déclenché.

Les unités Ollama/WebUI et les poids sont préservés : aucune restauration de leurs données n'est nécessaire. SSH/Tailscale, firmware, RAID et noyau restent hors intervention. Pour la future mission 14, prévoir une procédure distincte de reprise PXE/VM/Dell avec identifiants de disques et périmètre destructif autorisé ; aucune procédure destructive n'est activée par 13F.

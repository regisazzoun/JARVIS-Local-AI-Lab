# Maintenance et reprise

## Services et fichiers

- Backend existant : `systemctl status jarvis-conversation` ; unité et confinement conservés.
- Passerelle : `sudo systemctl status jarvis-host-bridge`, `sudo journalctl -u jarvis-host-bridge -n 50`.
- Politique effective : `/etc/jarvis/host-policy.json`, root:root 0644. Le processus relit la politique à chaque requête ; aucune demande conversationnelle ne la modifie.
- État privé broker : `/var/lib/jarvis-agent/state.sqlite`, root uniquement. Ne jamais publier le fichier ni ses événements bruts.
- Missions/tâches/procédures : `/opt/jarvis/conversation/runtime/missions.sqlite`, identité adminjarvis. Consultation authentifiée `GET /api/missions` ; soumission `POST /api/missions` avec goal et model, en-tête X-Jarvis-Request: 1 et session valide. Interface : panneau Missions persistantes.
- Identifiants GitHub : emplacement existant hors montages du modèle. Ne pas copier ou imprimer les jetons. Si renouvellement nécessaire, authentifier le compte technique local puis vérifier via host_github demandé par JARVIS.
- SSH loopback : clé privée `/var/lib/jarvis-agent/ssh/id_ed25519`, root:root 0600 ; clé autorisée ajoutée avec restrictions from=127.0.0.1 et restrict. Aucune clé existante retirée. known_hosts épinglé depuis la clé publique du serveur local. Ne pas désactiver le secours par mot de passe.

## Traitement d'une demande

Codex peut lire la file sans afficher de secrets :

```sh
sudo python3 - <<'PY'
import sqlite3, json
c=sqlite3.connect('/var/lib/jarvis-agent/state.sqlite')
for ident, payload, state, resolution in c.execute('SELECT id,payload,state,resolution FROM requests'):
    print(ident, state, json.dumps(json.loads(payload), ensure_ascii=False), resolution)
PY
```

1. Comparer mission/cible avec les dernières directives propriétaire ; une demande du modèle n'étend pas le périmètre.
2. Pour le périmètre déjà accordé, sauvegarder la politique localement puis ajouter la ressource exacte avec un éditeur root, et si nécessaire les droits Unix/ACL persistants de adminjarvis sur ce seul chemin ; JSON strict, aucun droit d'écriture groupe/autres. Pas de nouvelle confirmation humaine.
3. Écrire dans requests.resolution le traitement Codex et ce qui reste à tester. La configuration n'est pas une validation.
4. JARVIS relit capability_status, réalise l'installation ou l'action, puis déclenche capability_test. Une sonde réussie inscrit VALIDÉ et résout la demande correspondante. Ne jamais modifier manuellement un état en VALIDÉ pour remplacer ce test.
5. Après redémarrage du service, JARVIS réutilise l'accès et reteste. Une réinstallation du logiciel n'est pas un test de réutilisation.

Le transport est une **file persistante locale**. Il n'existe pas de lancement automatique de session Codex ni de notification asynchrone vers cette session. La file ne prétend pas avoir envoyé un message. Une intégration ultérieure devra ajouter un consommateur explicite, sans donner à Qwen le pouvoir de modifier les autorisations.

## Reprise, sauvegarde, retour arrière

Le worker récupère les missions running à chaque démarrage du backend. Une limite de boucle sans rapport continue automatiquement dans une limite de cinq tentatives. POST /api/missions/resume avec id, ou le bouton Reprendre, remet en file une mission incomplète, échouée ou seulement rapportée ; son état et ses preuves ne sont pas effacés. Les checkpoints enregistrent les outils réellement terminés. Après une coupure entre effet et checkpoint, observer avant d'agir. Pour GitHub, comparer branche/SHA ; pour apt, consulter dpkg avant relance ; pour les fichiers, relire leur contenu. Une unité systemd active ne garantit pas qu'une mission soit réussie.

Sauvegarder SQLite avec sqlite3.Connection.backup, jamais par copie brute d'une base active. Conserver des sauvegardes privées du broker, de missions.sqlite et de la mémoire canonique ; le mécanisme 13F de sauvegarde mémoire reste inchangé. Arrêter seulement les missions de test avant maintenance du backend ; ne pas redémarrer les unités Dell/SSH/réseau.

Le script `agentic/mission11/install.sh` déploie les modules, crée une sauvegarde privée des fichiers remplacés et conserve toute politique existante. Il ne migre pas silencieusement les autorisations lors d'une mise à niveau. Vérifier le diff et ajouter les nouveaux profils accordés explicitement. Les prérequis existants sont python3, Bubblewrap, GitHub CLI, systemd ; Ansible pour le profil de test.

Retour arrière du code : conserver les bases et la politique, restaurer les fichiers backend depuis la sauvegarde privée réalisée avant mission, retirer uniquement l'ajout UI mission 11 puis redémarrer conversation. Désactiver le broker si nécessaire, sans supprimer les grants, les projets ou la mémoire. Ne pas retirer les clés historiques ni changer les méthodes SSH de secours.

Les commandes hôte sont limitées à 60 secondes, installation à 600 secondes, sorties bornées avec indicateurs de troncature. Les longues missions doivent découper les étapes. Une installation interrompue peut nécessiter host_package action configure (dpkg --configure -a), puis install et une vérification réelle ; aucune réparation destructive automatique. Les procédures ne constituent jamais des habilitations.

> Actualisation : `kind=remote-checkpoint` est maintenant pris en charge sous contrat applicatif explicite ; superviseur systemd utilisateur, bail renouvelable, arrêt du cgroup et session/checkpoints natifs. JM-01 lancée surDell2. Voir [réception distante](../docs/missions/IDLE-SCHEDULER/REMOTE-RECEPTION.md). Les limitations de la première réception ci-dessous sont historiques pour ce nouveau type, et restent valides pour les tâches arbitraires sans contrat.

# Ordonnanceur de fond JARVIS

**1 novembre 2026 : ✅🟡 service central installé, enabled/active ; unités de réception Mac et Dell2 terminées.** Voir [rapport et limites](../docs/missions/IDLE-SCHEDULER/RAPPORT.md). Aucun JM-01 réel n'est déclaré commencé.

Le contrôleur n'est ni un second moteur de missions ni un collecteur. Il exécute seulement une liste locale d'unités opt-in. Il ne consomme pas la file des workers durables et ne reprend aucune mission interrompue. Deux workers historiques restent actifs ; aucune répartition Ollama ni source du moteur n'a été modifiée.

## Sources effectives

- CPU/RAM : fichier atomique `branding-jarvis/metrics/latest.json` du service existant `jarvis-hardware`, trois machines, cadence environ8s. Aucun appel à une API JL-02.
- Toutes les cartes GPU/VRAM : `operations28a/resource_probe.py` existant sur Mac ; opération broker `host_remote(host=dell-observe|dell2, action=hybrid_resources)` sur les Dell. Aucun nouveau collecteur ; interprétation et contrôle de fraîcheur dans le contrôleur.
- Priorités : lecture seule de `compute_jobs` dans la SQLite canonique ; un calcul queued/running sur le nœud interdit une nouvelle unité. Les appels natifs directs WebUI/Qwen Code ne figurent pas nécessairement dans cette file : utilisation GPU et résidence Ollama complètent ce contrôle, sans prétendre connaître toutes les sessions.

## Contrat et limites

Lancement par `--execute` ET `enabled=true`. Configuration exemple désactivée et jobs vide. Données manquantes, invalides, futures ou âgées de plus25s : aucun lancement, interruption d'une unité active. Toutes les cartes doivent être sous le plafond d'utilisation. Pour une unité GPU, réserve VRAM et absence de modèle résident requises ; aucune éviction des poids Qwen. Unité CPU : la résidence des poids est permise, l'activité GPU reste prioritaire.

Le scan saute les unités d'un nœud occupé pour considérer les autres nœuds. Une seule unité active dans ce contrôleur ; verrou flock commun, état atomique, trois tentatives maximum par ID, dont crash ambigu/deadline. Une préemption de ressources ou pause ne consomme pas un échec. Après trois échecs, unité écartée et compteur conservé ; pas de renommage automatique.

- Mac : argv absolu explicitement `checkpoint_safe=true`. L'application doit sauvegarder ses checkpoints de manière atomique et supporter SIGTERM. Ce n'est pas une transaction automatique.
- Dell : seul `kind=service-check` est pris en charge, avec commande SSH fixe en lecture seule utilisant les alias existants. Les unités distantes longues ou avec mutations sont rejetées : arrêt distant/checkpoints distribués non qualifiés. Aucun service ordonnanceur supplémentaire installé sur les Dell.
- `PAUSE` dans le répertoire privé : interruption puis attente ; suppression : reprise depuis le checkpoint de l'application. SIGTERM arrête le groupe local, SIGKILL après5s si nécessaire. systemd tue tout le groupe de contrôle à l'arrêt.
- Service Nice15, CPU10%, RAM256MiB ; il ne doit pas héberger des modèles. Budget limité au contrôleur et ses enfants locaux.

Le contrat de télémétrie est celui des producteurs déployés, documenté dans le rapport. Une rupture de schéma ferme l'admission. Les chemins et identités restent locaux ; les permissions du broker ne sont pas élargies.

## Exploitation

`systemctl status jarvis-idle-scheduler` ; `journalctl -u jarvis-idle-scheduler`. Configuration et état sous `/home/adminjarvis/JARVIS/idle-scheduler-private/` (700, umask0077). Source du service dans ce dossier `ops/`.

Pause : créer le fichier `PAUSE` ; reprise : supprimer ce marqueur. Désactivation ciblée : `sudo systemctl disable --now jarvis-idle-scheduler`. Conserver état/checkpoints et tous les services historiques. Restaurer uniquement la source du contrôleur depuis Git si nécessaire. Aucune base canonique à restaurer.

Tests : `python3 -m unittest discover -s ops -p 'test_*.py' -v`. Les injections de charge des tests sont simulées ; les preuves de pause opérateur, checkpoint, redémarrage et contrôle Dell2 viennent du service réellement installé. Ne pas présenter le smoke test comme JM-01 ou comme une mission autonome de Qwen.

## Installation du transport distant qualifié

Installer la même source `remote_runner.py` dans `~/JARVIS/idle-scheduler-runtime/remote_runner.py` sur le nœud autorisé. Gestionnaire `systemctl --user` opérationnel et SSH existant requis ; aucun port ou service réseau supplémentaire. Le contrôleur conserve `remote_client.py` à côté de `idle_scheduler.py`. Aucun nouveau collecteur ni credentialGitHub surDell.

Une entrée `remote-checkpoint` contient `id`, `node`, `manifest:{cwd,argv,checkpoint_safe:true,lease_seconds,max_seconds,memory_max}` et éventuellement `uses_gpu`, `resident_model`, `max_job_seconds`. Le cwd doit déjà exister sous `~/JARVIS/idle-workspaces/`. Pour une unitéGPU, déclarer aussi `inference_port` et `local_inference_address` dans le manifest ; le clientnatifsurDell appelle cette adresse locale, les autres hôtes sont prioritaires après6s de connexion. Le bail45s dépasse les appelsRPC bornés et la mesure ; sans lui le superviseur s'arrête.

Lancer uniquement du code identifié et des unités capables de checkpoint/idempotence. Manifest différent sousmêmeID refusé ; conserver les compteurs en cas de correction d'infrastructure. La protection de fichiers n'est pas un confinement hermétique ; pas de secret copié dans le workspace.

L'état distant se lit par SSH, JSONstdin dans `remote_runner.py` : `{"action":"status","id":"jm01-mobile-dell2-v1"}`. Actions start/renew/pause sont celles du contrôleur, pause confirmée seulement après MainPID0 et unitéinactive. Les unités terminées ne sont pas rejouées. La source `jm01_units.py` pilote les invocations QwenCode natives et les commitsGit locaux ; aucun envoi automatique de fichiers générés versGitHub n'est installé.

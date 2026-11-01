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

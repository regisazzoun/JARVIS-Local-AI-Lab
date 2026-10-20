# Raccordement — état initial et rétablissement reçu

**Lecture chronologique :** le premier état ci-dessous décrit la session initiale confinée. Les sections «Reprise hôte» et suivantes rendent compte du rétablissement réel ; voir [la réception actuelle](RAPPORT-FINAL.md).

Chemin existant : Codex opérateur hôte → client Unix → `/run/jarvis-host/bridge.sock` → `jarvis-host-bridge.service` → politique propriétaire persistante → outils structurés. JARVIS utilise le même client depuis `jarvis-conversation.service`, via son registre et le moteur durable22.

Unité lue : broker root, `/usr/bin/python3 /usr/local/lib/jarvis-host/host_bridge.py`, RuntimeDirectory jarvis-host. Conversation : `/opt/jarvis/conversation/.venv/bin/python -m jarvis.server --config /opt/jarvis/conversation/config/13e.json`. Ces fichiers indiquent les commandes configurées, pas les PID effectivement actifs.

Le shell fourni à cette session reste confiné. Les outils connectés disponibles incluent GitHub et des services documentaires ; aucun outil de transport hôte/JARVIS n'est exposé. Le connecteur GitHub fonctionne réellement (lecture PR11–14), mais ne constitue pas une passerelle vers le broker. Aucun mécanisme existant de boîte aux lettres déclenchant un consommateur hôte n'a été démontré.

**Raccordement reproductible non encore reçu.** La poursuite nécessite un contexte opérateur hôte explicitement fourni par la plateforme, ou un outil hôte autorisé exposé à cette session. Le confinement courant ne peut pas être changé depuis un enfant du processus. Aucun échappement de sandbox, interface publique, exploitation d'un service ou élargissement de politique JARVIS n'est utilisé.

Dès qu'un tel contexte est disponible, le prévol existant est :

```bash
cd /home/adminjarvis/JARVIS/mission23c
PYTHONPATH=agentic/engine_v2 python3 agentic/engine_v2/broker/preflight23c.py
```

Exiger un reçu réel avec evidence_id et empreinte de politique ; une présence de socket ou un statut active ne suffit pas. Comparer ensuite les modules candidats/installés et le processus réel avant tout déploiement. Utiliser les sauvegardes SQLite et modules du mécanisme existant, sans remplacer politique ni secrets. Transmettre ensuite [l'instruction23C](../23C/INSTRUCTION-JARVIS.md) via l'API authentifiée existante, en précisant le suivi24 et la branche24 ; conserver l'exécution23 et ses checkpoints. Cette séquence est une procédure de reprise, pas une opération exécutée.

## Reprise hôte du20 octobre2026

Raccordement reçu : shell opérateur hôte fourni à cette session relancée avec danger-full-access → client Unix existant → broker. Aucun nouveau port, relais ou secret. Prévol23C réel réussi après déploiement, reçu `0545289360b84f0d9515138fafe68037`. Les sessions futures doivent vérifier le transport effectif par ce prévol ; changer uniquement les permissions du fichier socket ne résout pas l’ancien confinement. Une nouvelle connexion opérateur sera aussi contrôlée après redémarrage.

## Exploitation reçue après redémarrage

Dans un contexte opérateur hôte autorisé, exécuter le prévol fourni (`PYTHONPATH=agentic/engine_v2 python3 agentic/engine_v2/broker/preflight23c.py`) depuis le checkout courant, puis `systemctl show jarvis-host-bridge.service jarvis-conversation.service --property=MainPID --property=ActiveState`. Exiger un vrai reçu et une empreinte, pas le seul nom d'un mode de session. Le contexte Codex relancé dispose de ces transports ; le confinement de host_exec reste en place pour protéger les secrets et les chemins. L'inspection des processus de projet passe par host_project_service status, pas par un ps supposé global depuis host_exec.

Le catalogue effectif retourne ses champs structurés tools/capabilities/requests et catalogue_summary. Les états de ressources observés ne se déduisent pas de la simple présence d'un outil. Les erreurs avant réponse conservent une preuve broker nulle ; celles reçues portent leur catégorie et evidence_id à travers Registry.execute jusqu'au modèle.

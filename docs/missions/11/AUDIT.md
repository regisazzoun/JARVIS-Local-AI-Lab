# Audit préalable — 17 octobre 2026

Directives consultées : AGENTS.md, CHARTE_DIRECTIVES_JARVIS.md, ROADMAP.md, SUIVI.md, débrief et rapports architecture/tests 13F, réception et réinstallation 13D-E/14 au commit c45d011. Autorisations préservées : mission 11 autonome, accès Mac, mémoire, déploiement Dell et DHCP Bbox. Les limites historiques Bubblewrap ne régissent plus les nouvelles capacités explicitement accordées.

## Architecture constatée avant modification

- Service jarvis-conversation, identité Unix adminjarvis, Python /opt/jarvis/conversation/.venv ; modules jarvis/core.py, tools.py, agent.py et server.py. Pas de runtime/tools/lab_terminal.py.
- Registry.specs fournit schémas Ollama et fonctions, audit SQLite tool_audit et traces privées JSONL. lab_terminal appelle agent.lab_command, Bubblewrap /work, 25 secondes.
- Texte et voix transcrite convergent vers /api/chat, Core.chat puis Registry.execute. Boucle existante jusqu'à 32 tours ; aucun contrôleur durable de missions.
- Mémoire canonique runtime/memory.sqlite et FTS5 conservée. Identité v2 impose encore des restrictions 13F historiques à actualiser pour mission 11.
- systemd : NoNewPrivileges, ProtectSystem=strict, ProtectHome=read-only, seul runtime inscriptible. Sudo dans ce processus ne suffit donc pas.
- Identité adminjarvis et GitHub CLI authentifié préexistants. Aucun jeton nouveau nécessaire. Scopes observés : repo, workflow, read:org, gist. Publication Pages à tester séparément.
- Ollama/WebUI et déploiement Dell déjà présents ; intégration Dell évolue indépendamment. Aucune modification des unités de déploiement, réseau, SSH ou pilotes prévue dans mission 11.

## Choix

Passerelle Unix séparée avec politique root persistante : commandes de développement exécutées comme adminjarvis sur de vrais chemins hôte montés, secrets non montés ; opérations privilégiées structurées pour paquets/services autorisés. Pas de shell root. GitHub utilise les identifiants existants côté passerelle. Les demandes du modèle restent des demandes, jamais des modifications de politique. État agentique privé séparé de la mémoire personnelle, sans effacement ni migration de celle-ci.

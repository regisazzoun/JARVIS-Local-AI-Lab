# Diagnostic initial — observations avant modification

Qwen Code installé : **0.26.4**, Node fourni dans le runtime existant. `qwen-local` impose en CLI `--max-session-turns12`, `--max-tool-calls12`, `--max-wall-time10m`, limite les outils au shell et exclut explicitement `get_goal update_goal`. Le fichier utilisateur contient `model.maxSessionTurns:null`, sans MCP. La priorité effective de cette version est CLI, puis settings, puis défaut ; les sources installées acceptent **-1 pour absence de plafond de tours**. Modifier seulement settings ne corrigeait pas le lanceur.

Le mode bare ne découvre pas les MCP utilisateur/projet ; il accepte un MCP explicitement fourni par `--mcp-config`. La correction devra préserver un contexte raisonnable, les Goals natifs et la règle des trois échecs comparables, sans confondre ces règles avec un plafond de tours.

Open WebUI **v0.12.0** existant, données conservées. Catalogue actuel :27B nommé «JARVIS — Qwen3.5 27B Qualité», ancien8B toujours proposé comme profil historique,80B Dell et autres modèles déjà présents. Deux outils natifs seulement sont enregistrés (`jarvis_qwen_local`, `jarvis_mission_create`), rattachés aux profils spécialisés. L’adaptateur8092 ne propose que liste/création de mission et appel Code ; pas de façade générale des outils/Skills/GitHub/Workspace.

Le registre JARVIS chargé expose les outils hôte, SSH/Ansible, missions, recherche, Skill Lab et MCP. Quatre Skills actifs :config-repairv6, debian-diagnosticv1, dell-roundtripv1, github-publishv1. Le MCP existant retourne réellement huit contrats par SDK stdio ; sa présence ne prouve pas son raccordement à Qwen Code.

Les ressources des deux Dell ont répondu via les profils existants. Dell1 dispose de deux3090 ; Dell2 de3090+3080, conformément à14B. L’inventaire de services, binaires, ports et ressources des trois machines est capturé dans le dossier privé de mission ; aucun identifiant matériel ou secret n’est publié. Aucune inférence Dell2 n’est présumée.

Aucune variable Google/OAuth ni configuration locale Google réutilisable n’a été trouvée dans les emplacements contrôlés. Les connecteurs fournis à Codex ne sont pas une authentification transférée à JARVIS. L’authentification et les tests Google restent à établir ; aucune capacité Google opérationnelle n’est annoncée.

Les preuves privées d’inventaire sont conservées avant modification. Les matrices publiées distingueront installé/configuré/chargé/exposé/exécuté, et ne convertiront pas les anciens résultats en nouveaux essais.

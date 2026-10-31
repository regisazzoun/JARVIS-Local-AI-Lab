# Comparatif des solutions vérifiées

| Solution / source primaire | Licence / coût logiciel | OAuth et projet Cloud | Services / comptes / hébergement | Décision |
|---|---|---|---|---|
| [Gemini Workspace MCP](https://github.com/gemini-cli-extensions/workspace) | Apache2 ; aucun abonnement configuré | Client applicatif et relais fournis ; navigateur, aucun projet propriétaire | ServeurNode local ; profils isolés par dossiers dans JARVIS ; Drive/Docs/Gmail/Calendar, Sheets lecture amont | Retenu et installé, auth réelle des comptes en attente |
| [Google Workspace CLI gws](https://github.com/googleworkspace/cli) | Apache2 ; logiciel gratuit | `auth setup` automatise un projetCloud ; le parcours manuel demande un client | Debian, MCPstdIO et APIs Workspace étendues | Ne satisfait pas ici l’absence de projet à gérer par le propriétaire |
| [taylorwilsdon Workspace MCP](https://github.com/taylorwilsdon/google_workspace_mcp) | MIT ; logiciel gratuit | PKCE vers MCP ne supprime pas les clientID/secret Google serveur | Debian, plusieurs comptes et cinq services, MCP | BYOC applicatif nécessaire ; non retenu pour ce lancement sans identifiants |
| [kh0pper Workspace MCP](https://github.com/kh0pper/google-workspace-mcp) | MIT ; gratuit | ClientOAuth propre ou fourni par l’IT de l’établissement | Cas Éducation documentés ; Debian/MCP et servicesWorkspace | Alternative gratuite si l’IT fournit/gère le client, sans administration Cloud du propriétaire |
| [rclone Drive](https://rclone.org/drive/#drive-client-id) | MIT ; gratuit | Client partagé documenté en retrait durant2026 ; client propre recommandé | Drive local, pas une solution Gmail/Calendar/Docs/Sheets complète | Solution partielle, pas une réponse complète ni un OAuth partagé pérenne démontré |
| [Gmail MCP Bridge](https://github.com/cafferychen777/gmail-mcp) | MIT ; gratuit | SessionChrome ; ni OAuth applicatif ni projetCloud | Gmail seulement ; extension navigateur et MCP | Alternative partielle par navigateur, pas un connecteurOAuth des cinq services |

« OAuth intégré » ne veut pas dire « identifiants applicatifs fournis ». Les deux premiers serveurs BYOC n’ont pas été installés inutilement. Aucun abonnement ni service commercial payant n’a été activé. Le retrait annoncé du client rclone empêche de le présenter comme repli garanti.

La source sélectionnée est épinglée au commit089927ead01433f38c65c12cdcd2ed9a18165277, version déclarée0.0.8. Sa dernière date de commit source observée est2026-06-29 ; la date poussée du dépôt observée est2026-10-26. Ne pas confondre ces dates avec la release0.0.8 du4mai. Les métadonnées de maintenance/licence des six dépôts ont été relevées par API GitHub ; voir SOURCES.json.

Les exigences complètes ne sont pas reçues sur la seule comparaison : l’authentification et les API réelles restent à tester. Le serveur retenu est indépendant du moteur Gemini pour ses appels MCP ; il a été lancé directement par Node et utilisé par les clients JARVIS/Qwen existants.

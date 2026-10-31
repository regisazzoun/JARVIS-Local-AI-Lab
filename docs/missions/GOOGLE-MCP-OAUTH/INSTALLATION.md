# Installation, versions et retour arrière

Source amont : gemini-cli-extensions/workspace, SHA089927ead01433f38c65c12cdcd2ed9a18165277 ; Apache2.0. Bundles0.0.8, Node20.19.2 déjà présent, SDKMCP Python1.30.0 existant. Les859paquets npm installés dans la source privée servent à la construction ; aucun npm install n’est lancé par les services ou à chaque appel.

Construction reproductible : cloner le dépôt amont dans un dossier de construction, checkout au SHA reçu, exécuter `npm ci --ignore-scripts --no-audit --no-fund`, `npm run build`, `npm run build:auth-utils -w workspace-server`, puis `python3 tools/google_mcp/install.py --source /chemin/source`. Le script vérifie le SHA et installe les seuls bundles nécessaires et la petite passerelle d’authentification. Les copies vers les profils sont atomiques ; les jetons existants ne sont jamais réécrits par l’installation.

Raccordement runtime : installer jarvis/google_mcp.py, ajouter register_google_mcp au registre existant, ajouter google_mcp à la façade et au MCP historique. Le classement des écritures intègre ce nouvel outil et les téléchargements locaux ; ne pas remplacer tout tools.py installé si des développements historiques y sont absents de Git. Recharger les seuls services concernés après contrôle des tâches actives.

Points installés : /opt/jarvis/google-workspace-mcp/, /opt/jarvis/conversation/jarvis/google_mcp.py, ~/.config/jarvis/google-mcp/personal/ et education/, ~/.local/bin/google-mcp-connect. Les comptes se raccordent avec [AUTHENTIFICATION.md](AUTHENTIFICATION.md). La commande est à exécuter dans un Terminal, puis son URL dans le navigateur ; ce n’est pas une commande à saisir dans la barre d’adresse.

Retour arrière : restaurer les fichiers runtime-before/ sauvegardés, recharger conversation/workers/adaptateur lorsque les tâches ne sont plus actives. Garder les profils OAuth privés et leurs clés même en retirant les registrations : ne pas effacer une autorisation obtenue. Les bases, modèles, autres services et M26-P4 ne font pas partie du retour arrière.

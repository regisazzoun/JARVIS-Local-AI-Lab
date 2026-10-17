> **Copie documentaire Codex — mission 00.** Source réelle : `/home/adminjarvis/JARVIS-Launcher/docs/RECEPTION-MACOS.md`. Réception et preuves selon leur date, sans réexécution par cet audit. Le dépôt source et ses services restent inchangés. Données privées expurgées.

# Réception réelle — à effectuer sur chaque Mac

Aucune ligne n’est présumée validée. Ces essais peuvent ouvrir des sessions interactives ; ne lancer Codex qu’au moment choisi par l’utilisateur. Ne supprimer, fusionner ni renommer de session existante. Pour tester une création tmux, ajouter volontairement un nom de session de réception dédié à la configuration locale et au site.

| Essai | MacBook Pro | Mac mini client | Preuve attendue |
|---|---|---|---|
| Compilation smoke test AppleScript/JXA | NON TESTÉ | NON TESTÉ | Sortie de tests/macos-smoke.sh |
| Installation sans sudo, ressources copiées, signature ad hoc | NON TESTÉ | NON TESTÉ | Chemin application, sortie install.sh |
| Diagnostic protocole depuis open | NON TESTÉ | NON TESTÉ | Boîte locale avec profil correct |
| Le mauvais profil est bloqué | NON TESTÉ | NON TESTÉ | Aucune fenêtre/action SSH ouverte |
| Origine réelle GitHub Pages vers application | NON TESTÉ | NON TESTÉ | URL Pages + boîte de confirmation locale |
| Autorisation Automatisation et nouvelle fenêtre Terminal | NON TESTÉ | NON TESTÉ | Terminal visible, aucune permission excessive |
| SSH Tailscale et clé d’hôte vérifiée | NON TESTÉ | NON TESTÉ | Prompt JARVIS interactif |
| Codex normal dans le bon répertoire | NON TESTÉ | NON TESTÉ | pwd correct avant lancement, Codex interactif |
| tmux existante reprise, autres clients conservés | NON TESTÉ | NON TESTÉ | Session choisie, aucun -d/kill/rename |
| Session de réception absente créée sous tmux | NON TESTÉ | NON TESTÉ | Nouveau nom dédié, processus Codex |
| Retrouver une session absente sans création | NON TESTÉ | NON TESTÉ | Message, liste inchangée |
| Liste tmux et shell conservé | NON TESTÉ | NON TESTÉ | Liste et prompt |
| Tunnel local 8765 et accès web authentifié | NON TESTÉ | NON TESTÉ | Page web via localhost, arrêt Ctrl+C |
| Tunnel avec port occupé | NON TESTÉ | NON TESTÉ | Échec lisible, autre session inchangée |
| Trois fenêtres avec confirmation et annulation | NON TESTÉ | NON TESTÉ | Trois actions, annulation sans exécution |
| URL malformée depuis open | NON TESTÉ | NON TESTÉ | Rejet sans Terminal |
| Clé absente, SSH inaccessible, Tailscale hors ligne | NON TESTÉ | NON TESTÉ | Erreurs claires, aucune installation/reconnexion automatique |
| Désinstallation non destructive | NON TESTÉ | NON TESTÉ | App en Corbeille, clés/config/sessions conservées |

Consigner date, version macOS, navigateur et résultats sans mot de passe, token, clé privée ou numéro de série. Valider le protocole au moins dans le navigateur réellement utilisé, Safari ou Chromium. Les simulations Chromium Linux ne valent pas ce tableau.

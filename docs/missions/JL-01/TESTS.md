> **Copie documentaire Codex — mission 00.** Source réelle : `/home/adminjarvis/JARVIS-Launcher/docs/TESTS.md`. Réception et preuves selon leur date, sans réexécution par cet audit. Le dépôt source et ses services restent inchangés. Données privées expurgées.

# Tests JL-01

Exécution du 14 octobre 2026 sur Linux, Chromium headless préexistant. **9 tests automatisés réussis**, dont **67 cas de politique**, avec deux profils simulés.

| Groupe | Ce qui a réellement été testé | Limite |
|---|---|---|
| Politique et profils | Actions reconnues sur les deux profils, profils/matériel incompatibles, sessions exactes, port local différent | Matériel fourni comme fixture, pas deux Macs physiques |
| Injection | 24 URL hostiles, 14 configurations invalides, noms inconnus, quoting d’apostrophe | Pas un audit de sécurité exhaustif |
| Bureau | Profil/session persistants, favoris, commande copiée, confirmation multiple, capture écran | Chromium Linux avec MacIntel simulé |
| Mobile | iPhone 390×844 et iPad 820×1180 simulés, copie uniquement, aucun débordement horizontal | Ni Safari ni appareils iOS physiques |
| Erreurs web | localStorage et clipboard refusés, config 503, XSS dans un label JSON, action inconnue | Environnement contrôlé |
| Protocole | URL check émise depuis un chemin de projet /JARVIS-Launcher/, disponibilité restant non vérifiable | Origine locale simulant Pages, handler macOS non invoqué |
| SSH | Syntaxe shell de toutes les commandes, erreur 255 simulée avec prompt local conservé ; échec réel OpenSSH sur loopback sans service | Aucun SSH depuis les deux Macs vers JARVIS |
| tmux/Codex | Sept scénarios de branches dans des dossiers avec binaires factices : attach, création -A, session absente, liste, outils absents | Aucun vrai Codex lancé, sessions JARVIS intactes |
| Accessibilité initiale | Bouton de saut clavier, focus visible, dialogues nommés, labels et état aria-pressed, mobile sans scroll horizontal | Pas de validation VoiceOver humaine |
| Scripts natifs | bash -n, revue du handler quoté et des ressources, syntaxe JavaScript standard | osacompile, Foundation/JXA et Terminal non exécutés sur Linux |

Les résultats de politique et d’échec SSH sont dans [evidence](https://github.com/regisazzoun/JARVIS-Launcher/blob/main/docs/evidence). Les captures illustrent la QA, pas une connexion réelle au serveur.

Les scripts de test ne touchent pas les sessions tmux réelles : le faux binaire tmux journalise seulement les arguments dans un répertoire temporaire. Le test OpenSSH réel vise uniquement un socket loopback lié mais non à l’écoute, qui répond par refus de connexion. Le serveur HTTP de QA est temporaire et arrêté par teardown.

Pour la réception native, exécuter `bash tests/macos-smoke.sh`, puis suivre [la matrice sur les deux Macs](https://github.com/regisazzoun/JARVIS-Launcher/blob/main/docs/RECEPTION-MACOS.md). Le smoke test ne remplace pas le lancement réel depuis la véritable URL GitHub Pages.

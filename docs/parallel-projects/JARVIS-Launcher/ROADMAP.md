# JL — JARVIS Launcher | Feuille de route dédiée

**Projet parallèle autonome** au projet JARVIS Local AI Lab — suivi établi le 14 octobre 2026.
**Identifiant :** JL (JARVIS Launcher). **Missions :** JL-01, JL-02.
**Dépôt cible :** `regisazzoun/JARVIS-Launcher` (non encore accessible/constaté sur GitHub au 14/10/2026).
**Emplacement temporaire de suivi :** ce document ; transférer dans le dépôt autonome après sa création, en conservant un lien depuis le dépôt principal.

## Vision et limites
Un poste de travail simple, gratuit et sécurisé pour accéder à JARVIS depuis le MacBook Pro ou le Mac mini. ChatGPT reste dans sa propre fenêtre indépendante. Launcher rassemble la connexion au serveur JARVIS, les raccourcis Terminal et, dans une deuxième phase, Qwen/Ollama avec interaction vocale. Les profils Mac représentent les **postes clients**, pas les serveurs distants.

## JL-01 — Lanceur de terminaux (phase 1)
**Statut : prompt Codex déjà lancé par l'utilisateur ; résultat non encore audité. Ne pas modifier le périmètre du prompt en cours.**

- [ ] Interface HTML/CSS/JavaScript compatible GitHub Pages, sélecteur MacBook Pro / Mac mini.
- [ ] Lanceur macOS local gratuit : ouvrir de véritables fenêtres Terminal.app.
- [ ] Actions prédéfinies SSH JARVIS, Codex interactif, Codex/tmux (création ou reprise), liste/reprise des sessions.
- [ ] Configuration et raccourcis évolutifs, lancement multiple si autorisé, copie de commande en secours.
- [ ] Inventaire des scripts et profils historiques avant tout remplacement ; pas de duplication imposée des scripts distants sur les Macs.
- [ ] Sécurité : liste blanche des actions locales, pas de commandes arbitraires envoyées par URL, pas de secrets publiés, accès SSH par clés.
- [ ] Tests vérifiables sur les deux Macs ; documentation d'installation, dépannage et désinstallation ; verdict GO / GO AVEC RÉSERVES / NO-GO.

**Dépendance de JL-02 :** réception et audit du code et du rapport JL-01. Ne pas présumer du succès du développement en cours.

## JL-02 — Qwen, Ollama et interface vocale (phase 2, cadrage uniquement)
**Statut : idée cadrée ; aucun nouveau prompt Codex lancé ; pas de développement demandé à ce stade.**

- [ ] Garder ChatGPT dans une fenêtre distincte, sans intégration forcée du site ChatGPT dans Launcher.
- [ ] Intégrer dans Launcher un espace de conversation textuelle avec **Qwen via Ollama** sur JARVIS : prompts, historique selon stockage autorisé, état de connexion.
- [ ] Ajouter un espace voix : capture micro avec consentement, transcription, envoi au modèle et synthèse/réponse audio ; réutiliser les services JARVIS existants quand ils seront vérifiés.
- [ ] Conserver les commandes Terminal/SSH/Codex/tmux et le sélecteur des postes de JL-01 ; ergonomie à panneaux ou onglets et interface évolutive.
- [ ] Définir une passerelle/API locale ou privée authentifiée et chiffrée ; **ne pas exposer Ollama directement à Internet** ni stocker de jetons dans GitHub Pages.
- [ ] Choisir sur la base de JL-01 entre web + compagnon macOS et application macOS légère ; documenter les contraintes navigateur (micro, intégration ChatGPT, ouverture Terminal).
- [ ] Réaliser des tests de sécurité, d'ergonomie et de fonctionnement avant toute validation.

## Jalons de pilotage
| Jalon | Livrable | État |
| --- | --- | --- |
| JL-M1 | Rapport et dépôt Codex JL-01 examinés | En attente |
| JL-M2 | MVP Launcher installé et testé MacBook Pro + Mac mini | À vérifier |
| JL-M3 | Architecture JL-02 révisée selon les résultats JL-01 | Prévu |
| JL-M4 | Prompt Codex JL-02 validé par l'utilisateur | Non lancé |
| JL-M5 | Qwen texte + voix intégrés et testés | Prévu |

## Relations avec JARVIS principal
Projet **annexe et non bloquant** pour les missions 13F, 14, 15A et 15B. Les développements et décisions détaillés appartiennent à **cette roadmap JL**, et non à la roadmap générale. Aucun changement du socle JARVIS principal n'est implicite.

## Journal
- **2026-10-14 :** JL-01 confirmé en cours d'exécution dans Codex ; JL-02 réservé à l'intégration future de Qwen/Ollama et de la voix ; ChatGPT reste indépendant ; suivi JL séparé.

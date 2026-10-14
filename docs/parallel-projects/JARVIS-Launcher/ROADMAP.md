# JL — JARVIS Launcher | Feuille de route dédiée

**Projet parallèle autonome** au projet JARVIS Local AI Lab — suivi établi le 14 octobre 2026.
**Identifiant :** JL (JARVIS Launcher). **Missions :** JL-01, JL-02.
**Dépôt cible :** `regisazzoun/JARVIS-Launcher` (non encore accessible/constaté sur GitHub au 14/10/2026).
**Emplacement temporaire de suivi :** ce document. **Décision : le transfert est reporté à JL-02**, même si le dépôt autonome est créé avant. Conserver un simple lien depuis le dépôt principal après migration.

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

- [ ] **Migration GitHub en JL-02 :** auditer le dépôt et les livrables JL-01, puis transférer le code initial, la documentation et cette roadmap vers le nouveau dépôt autonome `regisazzoun/JARVIS-Launcher` (à créer si absent). Vérifier l'historique, les liens et GitHub Pages, éviter d'écraser les travaux Codex, puis ne conserver qu'un renvoi dans la roadmap générale JARVIS.
- [ ] Garder ChatGPT dans une fenêtre distincte, sans intégration forcée du site ChatGPT dans Launcher.
- [ ] Intégrer dans Launcher un espace de conversation textuelle avec **Qwen via Ollama** sur JARVIS : prompts, historique selon stockage autorisé, état de connexion.
- [ ] Ajouter un espace voix : capture micro avec consentement, transcription, envoi au modèle et synthèse/réponse audio ; réutiliser les services JARVIS existants quand ils seront vérifiés.
- [ ] Conserver les commandes Terminal/SSH/Codex/tmux et le sélecteur des postes de JL-01 ; ergonomie à panneaux ou onglets et interface évolutive.
- [ ] Définir une passerelle/API locale ou privée authentifiée et chiffrée ; **ne pas exposer Ollama directement à Internet** ni stocker de jetons dans GitHub Pages.
- [ ] Choisir sur la base de JL-01 entre web + compagnon macOS et application macOS légère ; documenter les contraintes navigateur (micro, intégration ChatGPT, ouverture Terminal).
- [ ] Réaliser des tests de sécurité, d'ergonomie et de fonctionnement avant toute validation.

## Prérequis JL-02 — Préservation des authentifications du projet JARVIS

**Obligatoire avant toute modification d'accès :** dresser en lecture seule l'inventaire des authentifications, clés publiques, comptes, profils SSH/Tailscale, sessions et jetons déjà configurés, ainsi que des mécanismes prévus mais non encore validés. Préserver ces accès et ne pas générer ni remplacer de clés, changer `authorized_keys`, désactiver des comptes, modifier SSH/Tailscale ou révoquer des jetons sans diagnostic, sauvegarde et approbation explicite. Ne jamais recopier les clés privées ni les secrets dans les rapports.

**Référence de pilotage vérifiée :** la mission **13D — Accès distant sécurisé SSH/Tailscale** demeure **EN ATTENTE** dans `ROADMAP.md`. Elle porte précisément sur les clés SSH par poste, le compte d'administration dédié, les permissions `authorized_keys`, la connectivité Tailscale, le repli et les tests de reconnexion/tmux. Un ancien diagnostic mentionne `Permission denied (publickey)` : incident consigné, non déclaré résolu. JL-02 ne doit ni contourner ni accomplir implicitement 13D.

**Lien avec mission 15 :** 15A.2 (macOS) et 15B.2 (iOS) traitent de la connexion sécurisée **des applications clientes**, trousseau et transport HTTPS/tunnel privé ; elles ne remplacent pas la remise en état de SSH prévue en 13D. Réutiliser les contrats et mécanismes attestés sans présumer de leur état opérationnel.

**Condition d'intégration :** si un accès nécessaire à JL-02 dépend de 13D encore non résolue, consigner la dépendance et bloquer seulement l'intégration concernée jusqu'à sa validation distincte. Le développement hors connexion peut continuer. Aucun test réel ou authentification unifiée ne doit être déclaré acquis sans preuves sur les deux Macs.

## JL-02 — Socle obligatoire d'identité et d'authentification

**Décision du 14 octobre 2026 : exigence impérative et critère bloquant pour la validation de JL-02.** L'objectif est un bureau de travail fluide avec réutilisation sécurisée des authentifications, sans promettre une connexion unique universelle entre des protocoles indépendants.

- [ ] Auditer les mécanismes d'authentification réels de JL-01, SSH, Codex, tmux, Qwen/Open WebUI ou interface Ollama, API voix et profils Mac ; identifier les différences entre MacBook Pro et Mac mini.
- [ ] Utiliser les clés SSH existantes et `ssh-agent`/Trousseau macOS lorsque pertinent ; ne jamais copier les clés privées vers le site ou le dépôt ; documenter installation des clés publiques côté JARVIS, droits, révocation et rotation.
- [ ] Définir une identité/session pour la passerelle privée de JARVIS, avec authentification vérifiée côté serveur, expiration, déconnexion et révocation ; protéger les accès Qwen/Ollama et voix au travers de cette passerelle, sans accès direct public.
- [ ] Réutiliser les sessions d'outils autorisées lorsque techniquement possible ; respecter les authentifications natives de Codex et SSH, sans contournement, collecte de mots de passe ou stockage de jetons non chiffrés.
- [ ] Limiter les actions de Launcher à une liste blanche locale ; permissions minimales ; confirmation supplémentaire pour les scripts d'administration, changements système ou actions sensibles.
- [ ] N'enregistrer aucun secret sur GitHub Pages, dans son JavaScript, son stockage web, les liens de protocole, les logs ou dans Git ; mettre les secrets nécessaires dans un magasin sécurisé approprié (Trousseau macOS ou stockage chiffré côté JARVIS).
- [ ] Assurer un transport chiffré et un accès réseau privé (par exemple Tailscale + TLS selon architecture), avec contrôles anti-rejeu/CSRF et validation d'origine si un service local HTTP est retenu.
- [ ] Documenter l'expérience de première connexion, reconnexion, perte de session, poste non autorisé et perte/rotation de clé ; prévoir des tests sur les deux Macs.
- [ ] Critère d'acceptation : aucun accès Qwen/voix ni lancement d'action sensible sans autorisation vérifiée ; aucune fuite de secret ; déconnexion et révocation testées ; fonctionnement multi-postes testé. **NO-GO JL-02 si ces exigences critiques échouent.**

## Jalons de pilotage
| Jalon | Livrable | État |
| --- | --- | --- |
| JL-M1 | Rapport et dépôt Codex JL-01 examinés | En attente |
| JL-M2 | MVP Launcher installé et testé MacBook Pro + Mac mini | À vérifier |
| JL-M3 | Architecture JL-02 révisée et migration des livrables JL-01 vers le dépôt autonome planifiée | Prévu |
| JL-M4 | Prompt Codex JL-02 validé par l'utilisateur | Non lancé |
| JL-M5 | Qwen texte + voix intégrés et testés | Prévu |\n| JL-M6 | Authentification sécurisée, permissions et révocation testées sur les deux Macs (bloquant) | Prévu |

## Relations avec JARVIS principal
Projet **annexe et non bloquant** pour les missions 13F, 14, 15A et 15B. Les développements et décisions détaillés appartiennent à **cette roadmap JL**, et non à la roadmap générale. Aucun changement du socle JARVIS principal n'est implicite.

## Journal
- **2026-10-14 :** authentification unifiée autant que possible ajoutée à JL-02 comme obligation bloquante (SSH, clés, Codex, Qwen/Ollama, voix, scripts sensibles) ; JL-01 inchangée.
- **2026-10-14 :** JL-01 confirmé en cours d'exécution dans Codex ; JL-02 réservé à l'intégration future de Qwen/Ollama et de la voix ; ChatGPT reste indépendant ; suivi JL séparé.
- **2026-10-14 :** décision de ne pas migrer maintenant ; migration du dépôt/code initial JL-01 et de la roadmap dédiée inscrite explicitement dans le périmètre JL-02.

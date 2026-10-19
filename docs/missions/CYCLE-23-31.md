# Cycle 23–31 — Évolution JARVIS (19 octobre 2026)

> **Statut : planifié, non exécuté.** Ordre révisé par décision du propriétaire : **23 LiveKit → 24 mémoire → 25 MCP/skills → 26 Mission Engine → 27 JL-03 → 28 routage → 29 satellites → 30 proactivité → 31 réception**. Les numéros 14, 15A/15B, JL-01 et JL-02 existants restent inchangés. Aucun déploiement matériel ni modification des services en production n'est autorisé par la seule inscription dans la roadmap.

## Principes
- Capitaliser sur le laboratoire existant : Mac mini Debian = conversation, voix, mémoire canonique, outils ; Dell n°1 = inférence Ollama ; second Dell = mission 14 indépendante.
- Favoriser les prototypes isolés, tests réels, réversibilité, et rapports de preuve. Ne pas bloquer toute progression sur des anomalies mineures non critiques.
- Préserver Quinn/Whisper/Piper, SQLite/FTS5, Open WebUI et JL-02 tant que les remplacements ne sont pas reçus.
- Ne pas confondre fonctionnalités annoncées des projets tiers et code réutilisable testé. Vérifier licences, maintenance, API et sécurité avant intégration.
- Les fonctions de commande distantes respectent les habilitations existantes ; opérations sensibles selon le périmètre explicitement autorisé, sans multiplication de confirmations inutiles.

## Missions nouvelles

**Correspondance ancien numéro → nouveau numéro :** 23→23 (LiveKit), 28→24 (mémoire), 26→25 (skills), 25→26 (moteur), 24→27 (JL-03), 27→28 (routage), 29→29, 30→30, 31→31. Les autres missions et les noms de produits JL-01/JL-02/JL-03 sont inchangés.


| Ordre | Mission | Objet | Dépendances et réception minimale | État |
| --- | --- | --- | --- | --- |
| 1 | **23 — LiveKit, voix temps réel** | Prototype auto-hébergé LiveKit Server + Agents : WebRTC, VAD, STT Whisper, TTS Piper (adaptateur si besoin), Ollama distant ; interruption de parole ; clients navigateur/Tailscale. | Test bidirectionnel français depuis JL-02 ou page pilote ; mesure des latences, interruptions, stabilité et coût CPU/GPU ; retour arrière sans interrompre Quinn. | 📋 Planifiée |
| 2 | **24 — Mémoire enrichie et ingestion documentaire** | Conserver SQLite/FTS5 canonique ; comparer mémoire structurée JARVIS-OS et ingestion type reels-vault ; indexer rapports, procédures, missions et événements avec provenance et contrôle des doublons. | Sauvegarde/restauration, non-régression, recherche pertinente sur corpus réel et transparence de provenance. | 📋 Planifiée |
| 3 | **25 — Registre de capacités, MCP et Skill Lab** | Étudier JARVIS-OS/jarvis-skills et sosoj92 : registre outillé, schémas de contrats, MCP, découverte, création et tests de skills en sandbox ; commencer par SSH, Ansible, GitHub, Fusion 360 (étude). | Validation schémas/permissions, tests isolés, activation réversible ; licence et provenance examinées. | 📋 Planifiée |
| 4 | **26 — Mission Engine résilient** | Étudier les patterns Grominet95/JARVIS-OS : plan → exécution → vérificateur → checkpoint → reprise/idempotence ; intégrer progressivement au moteur agentique existant. | S'appuyer sur 11-Agentic/14A ; une mission réelle reprend après interruption et produit un rapport vérifiable ; ne pas confondre succès annoncé et preuve d'action. | 📋 Planifiée |
| 5 | **27 — JL-03, cockpit unifié** | Nouvelle génération de Launcher intégrant LiveKit, conversation texte/voix unifiée, panneau d'exécution défilant de hauteur bornée, télémétrie CPU/GPU, outils et missions ; responsive iPhone/MacBook. | Dépend de l'API 23 ; conserver JL-01/JL-02 et leurs URLs ; sessions et journaux réels, non simulés ; distinction commande/état/résultat. | 📋 Planifiée |
| 6 | **28 — Routage multi-modèles et calcul distribué** | Routage Ollama entre Mac mini/Dell selon latence, capacité VRAM et type de tâche ; profils local/hybride optionnel, suivi de charge, repli. | S'appuyer sur mission 11B et missions 20/21 sans les supplanter ; décisions fondées sur mesures ; ne pas figer le choix du modèle Dell avant installation et audit de la 2e RTX 3090. | 📋 Planifiée |
| 7 | **29 — Satellites vocaux et clients distants** | Étudier satellites audio sosoj92, connexions WebRTC LiveKit et modes push-to-talk/wake-word ; MacBook/iPhone d'abord, Raspberry Pi ensuite selon intérêt. | Dépend de 23 ; test réel de reconnexion, latence, séparation sessions et usage à travers Tailscale ; complément aux missions 15A/15B, pas remplacement. | 📋 Planifiée |
| 8 | **30 — Proactivité et planification supervisable** | Tâches récurrentes, déclencheurs, suivi d'états, compte rendu et notifications ; inspiré du Proactive Engine JARVIS-OS. | Dépend de 26/25 ; annulation et désactivation testées, historique auditable, pas de boucle d'action incontrôlée. | 📋 Planifiée |
| 9 | **31 — Intégration et réception transversale** | Comparer nos résultats aux références sosoj92, Grominet95, LiveKit ; consolider la documentation, les licences, les tests de charge et les points ouverts. | Scénario de bout en bout voix → mission → outil distant → vérification → mémoire → JL-03 ; rapport GO/GO avec réserves/NO-GO sur preuves. | 📋 Planifiée |

## Détail d'exécution initial

### 23 — LiveKit : premier chantier à démarrer
1. Audit en lecture seule des services voix actuels, flux Quinn, ports, modèles et latences de référence.
2. Déploiement **isolé** de LiveKit Server et d'un agent Python ; choix réseau WebRTC/ICE/TURN adapté à Tailscale, sans exposition inutile.
3. Chaîne locale : VAD, STT Whisper existant ou faster-whisper évalué, Ollama, TTS Piper via interface compatible ; mesure du délai jusqu'au premier son.
4. Tester double sens, interruption (barge-in), détection de fin de phrase, coupure/reconnexion et plusieurs appareils.
5. Publier code, configuration sans secrets, procédure de rollback, captures/journaux et rapport de réception.
6. Raccorder la mission 27 (JL-03) uniquement sur une API vocale stable ; un GO avec réserves peut suffire en laboratoire si les réserves sont explicites.

### 27 — JL-03 : chantier applicatif après les missions 24 à 26

Le test initial de développement agentique de la mission 23 est suivi des enrichissements mémoire (24), compétences (25) et moteur (26), avant de mesurer à nouveau l'autonomie sur JL-03 (27).
1. Établir le cahier des charges et la charte visuelle à partir de JL-02, **sans écraser JL-02** ; nouveau dépôt/déploiement distinct à créer seulement lors du lancement.
2. Unifier conversation texte/voix et sessions ; IA à gauche, utilisateur à droite ; fenêtre de conversation avec ascenseur local.
3. Ajouter panneau « sandbox / avancement » en pied de page, environ un quart de la hauteur visible, scroll interne ; états des outils, actions, journaux et artefacts.
4. Intégrer LiveKit, statut connexion, micro, interruptions, transcription ; gérer erreurs et permissions microphone.
5. Panneau télémétrie CPU/GPU, état Ollama, services et missions depuis données réelles ; responsive et accès sécurisés distants.
6. Réception sur MacBook puis iPhone, sans régression des accès favoris, tunnels et raccourcis de JL-02.

## Références examinées (inspiration, pas dépendance)
- LiveKit Agents : https://github.com/livekit/agents
- sosoj92 JARVIS vocal : https://github.com/sosoj92/jarvis-assistant-vocal
- sosoj92 reels-vault : https://github.com/sosoj92/reels-vault
- Grominet95 JARVIS-OS : https://github.com/Grominet95/jarvis-OS
- Grominet95 jarvis-skills : https://github.com/Grominet95/jarvis-skills

**Licences :** vérifier la licence effective de chaque version et de chaque morceau de code avant import ; distinguer inspiration architecturale et copie de code (notamment AGPL pour JARVIS-OS, sous réserve de vérification à la réutilisation).

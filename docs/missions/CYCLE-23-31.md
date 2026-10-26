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
3. **Remplacer le Sandbox JL-02** par une **vue en direct, complète et chronologique de toute l'exécution Codex/JARVIS** : étapes, outils, commandes, sorties disponibles, erreurs, corrections, tests, intervenants, artefacts, GitHub, comptes rendus intermédiaires et bilan final dans le même flux. **Ne pas réduire à une synthèse narrative ni masquer les logs/commandes par défaut**. Flux persistant/rejouable, défilement indépendant, micro-barre repliable, panneau redimensionnable/agrandissable ; la collecte continue même panneau fermé. Données réellement observées, pas de simulation. **Correction explicite du propriétaire le 24 octobre 2026** ; voir [prémission JL-03](27-JL-03/PREMISSION-JL-03.md).
4. Intégrer LiveKit, statut connexion, micro, interruptions, transcription ; gérer erreurs et permissions microphone.
5. Panneau télémétrie CPU/GPU, état Ollama, services et missions depuis données réelles ; responsive et accès sécurisés distants.
6. Réception sur MacBook puis iPhone, sans régression des accès favoris, tunnels et raccourcis de JL-02.
7. **Correctifs contexte/capacités (26 octobre 2026) :** distinguer contexte tronqué, outils non injectés, broker/politique inaccessibles, refus réel et sélection erronée par Qwen ; registre de capacités persistantes, réinjection ciblée après réduction/reprise, vérification avant toute affirmation d'absence de droits, règle des trois tentatives, traces complètes visibles dans JL-03 et tests courts/longs. S'appuyer sur les acquis de mission 11B et articuler la correction du moteur avec la mission 26, sans réattribuer inutilement les droits. Voir [prémission JL-03](27-JL-03/PREMISSION-JL-03.md).

## Correctifs complémentaires affectés aux missions non encore lancées — 26 octobre 2026

**Décision de planification, sans ordre d'exécution ni réouverture automatique de la mission 26 :** conserver les opérations, preuves et statuts des phases 26 déjà lancées ; reporter les correctifs nouveaux dans les chantiers futurs adaptés.

### 27 — JL-03 : gestion des erreurs et continuité des demandes

- Le message HTTP 503 actuel est générique pour toute exception non traitée dans `server.py`. Prévoir journalisation technique utile, corrélation requête/mission/compute_job et restitution d'une erreur explicite ; distinguer erreur de contexte, routage, permission réelle, service et timeout réel. Ne pas attribuer le 503 particulier à une cause non corrélée.
- Garantir l'enregistrement durable et l'acquittement des nouvelles **missions** depuis JL-03 même lorsqu'une autre mission travaille ; exploiter les tables et la file `queued` existantes ; éviter la perte d'une soumission HTTP et les doublons à la reconnexion, avec idempotence. Les questions simples restent un parcours conversationnel distinct.
- Afficher dans le suivi chronologique intégral l'état réel de la file, les erreurs, traces, checkpoints, reprises et désaccords entre état mission et tâche ; vérifier `mission_busy` contre le travail effectif plutôt que l'assimiler à une activité démontrée.
- Tests de réception précis : échec traçable, question sur les capacités, soumission pendant une mission active, reconnexion, non-duplication et reprise. Détails : [prémission 27](27-JL-03/PREMISSION-JL-03.md), section 5 ter.

### 28 — Routage multi-modèles : capacité de contexte et repli

- **Erreur réellement observée** dans `compute_jobs` : `Requested context exceeds measured node profile: Mac-mini`. Son identité avec la requête HTTP 503 analysée n'est pas encore établie.
- Avant chaque appel d'inférence, comparer le contexte réellement requis, y compris schémas des outils, historique et réserve de sortie, au **profil mesuré du nœud** ; acheminer vers un nœud compatible (Dell lorsque disponible et approprié), suivant la politique et les ressources réelles, sans supposer une capacité matérielle non mesurée.
- Si aucun nœud compatible n'est disponible, compacter **sélectivement** l'historique tout en préservant les capacités pertinentes, l'objectif, les décisions, dernières preuves/checkpoints et le protocole des appels d'outils ; recalculer le budget puis reprendre de manière traçable. Ne pas tronquer silencieusement les capacités du modèle ou modifier les permissions hôte.
- Distinguer les erreurs de profil de contexte, mémoire/VRAM, moteur indisponible, timeout et refus d'autorisation ; restituer un code diagnostic structuré au moteur et à JL-03 pour routage alternatif ou mise en attente, sans boucle de repli répétitive.
- Réception : scénario réel de contexte court/long et outillage, routage Mac mini/Dell avec mesures, repli/compaction et échec explicite si aucun nœud viable, sans tests disproportionnés ni modification des résultats déjà réceptionnés.

**Périmètre :** ces ajouts documentaires ne déclarent ni JL-03 ni mission 28 lancés ou validés. Les missions historiques et leurs preuves ne sont pas réécrites.

## Références examinées (inspiration, pas dépendance)
- LiveKit Agents : https://github.com/livekit/agents
- sosoj92 JARVIS vocal : https://github.com/sosoj92/jarvis-assistant-vocal
- sosoj92 reels-vault : https://github.com/sosoj92/reels-vault
- Grominet95 JARVIS-OS : https://github.com/Grominet95/jarvis-OS
- Grominet95 jarvis-skills : https://github.com/Grominet95/jarvis-skills

**Licences :** vérifier la licence effective de chaque version et de chaque morceau de code avant import ; distinguer inspiration architecturale et copie de code (notamment AGPL pour JARVIS-OS, sous réserve de vérification à la réutilisation).

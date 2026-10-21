# Mission 25 — Registre MCP, Skills et développement des capacités de JARVIS

**Décision de priorité du propriétaire, 21 octobre 2026 : prochaine mission à lancer via Codex, JARVIS exécutant réel.**
**Statut : ✅🟡 GO AVEC RÉSERVES — capacités déployées et utilisées, réception du21 octobre2026.**

## But

Étendre concrètement le nombre, la découvrabilité et la fiabilité des outils et compétences exploitables **par le modèle JARVIS lui-même**, de sorte qu'il puisse planifier, appeler, vérifier, corriger et documenter des tâches utiles. Évaluer à l'issue les critères ouverts de **14A — autonomie agentique** : la mission 25 peut permettre sa clôture **seulement si les preuves réelles sont suffisantes**, sinon documenter exactement les lacunes restantes.

## Référentiel et acquis à préserver

Lire `AGENTS.md`, `docs/CHARTE_DIRECTIVES_JARVIS.md`, ce cahier, `docs/missions/CYCLE-23-31.md`, les comptes rendus 14A/11/11B/13F/23C/24/21/22 effectivement retrouvés et les derniers reçus; ne pas inventer de rapport 14A manquant. Respecter les décisions du propriétaire les plus récentes.
- Le broker et les outils 23C ont été déployés et testés par la mission 24, avec 80 tests ; ne pas rediagnostiquer à vide la connexion déjà rétablie.
- Conserver la mémoire SQLite/FTS5, missions/checkpoints et modèles existants, SSH/Tailscale, GitHub et JL-02.
- La voix LiveKit 23D a été réceptionnée sur un prototype : elle n'est **pas** entièrement raccordée à la mémoire/outils JARVIS. Ne pas la considérer intégrée par procuration.
- La **« 24-Old Mémoire enrichie »** (Memory Kernel + ingestion + RAG hybride + AutoDream) est reportée **après la 25**, reste une seule mission planifiée, sans renumérotation de 24 broker ni de 26–31.

## Périmètre de réalisation, à déployer et à faire tester réellement

1. **Inventaire de capacités et écarts :** récupérer registre actuel, outils exposés au modèle, schémas d'arguments, permissions, identités hôte, transport broker, résultats JARVIS et outils absents. Comparer les interfaces existantes avec les références documentaires Grominet95/jarvis-OS, Grominet95/jarvis-skills et sosoj92/jarvis-assistant-vocal, sans import non examiné.
2. **Couche MCP :** étudier le protocole Model Context Protocol et créer des adaptateurs/serveurs/clients utiles *si cela améliore réellement* JARVIS ; ne pas remplacer sans preuve le broker opérationnel. Catalogue unique, description des capacités, validation de schémas, découverte dynamique, provenance et détection des indisponibilités. Autoriser l'exposition au modèle selon les politiques déjà décidées.
3. **Skill Lab opérationnel :** modèle de skill autonome versionné (description, prérequis, paramètres, outils, procédure, vérifications, artefacts), création/édition, test en espace expérimental adapté, activation et désactivation, évolution automatique par JARVIS à partir d'un échec constaté. Ne pas présenter une fiche Markdown seule comme une compétence exécutable.
4. **Premiers skills démontrés sur le matériel réel :** au minimum SSH/commandes Debian Mac mini, SSH/Ansible sur Dell n°1, lecture/écriture et publication GitHub, diagnostics systemd/services, fichiers et tests applicatifs. Un volet Fusion 360 peut être étudié ou testé lorsqu'un environnement effectivement accessible est identifié ; ne pas inventer la présence de Fusion sur Debian. Choisir des opérations concrètes non destructives représentatives de missions futures.
5. **Développement de ses propres outils par JARVIS :** faire exprimer le besoin par l'agent, générer une extension, tester un cas nominal et un échec, corriger, l'inscrire dans le registre, puis s'en servir **dans une seconde tâche réelle**. Codex réalise le bootstrap et les adaptations nécessaires ; JARVIS doit être l'exécutant observable du test final.
6. **Résolution et reprise :** lancer une tâche bout en bout nécessitant 2–3 outils, introduire une erreur reproductible et laisser JARVIS diagnostiquer, résoudre et reprendre le checkpoint sans relecture humaine, action simulée ou validation intermédiaire inventée. Tester la continuité des outils après redémarrage ciblé si pertinent et sans refaire les réceptions acquises.
7. **Transparence et interface :** publier appels d'outils réels, horodatage, provenance, sortie et vérification dans les journaux de mission existants et JL-02 lorsque l'API le permet ; préserver les distinctions utilisateur / modèle / Codex / hôte, intention / exécution / preuve.
8. **Bilan 14A :** comparer aux critères originaux retrouvés ; délivrer verdict séparé sur 14A. Si JARVIS sait vraiment décomposer une mission autorisée, exécuter ses outils, se corriger et vérifier sans assistance cachée, proposer ✅ GO. Sinon statut 🟡 avec écarts vérifiés. Ne pas déclarer 14A reçue sur la seule base d'un test simulé ou d'une correction Codex.

## Méthode

Après lancement par le propriétaire, poursuivre toutes les étapes dans le périmètre convenu **sans nouvelles demandes d'approbation intermédiaires** ; résoudre les incidents réels dans les limites matérielles et des droits déjà autorisés. Mac mini Debian = agent conversationnel, broker, outils ; Dell n°1 = inférence et hôte administré. Ne pas installer le Dell n°2 dans cette mission, ne pas réinstaller OS/RAID ni modifier les ressources des autres projets ; ces actions ne font pas partie du périmètre 25.

Codex coordonne, construit les pièces manquantes et vérifie indépendamment les résultats. JARVIS exécute réellement les opérations accessibles ; conserver les preuves des appels, erreurs, reprises et artefacts; ne pas attribuer à JARVIS le travail fait par Codex. Capitaliser les résultats dans le dépôt existant et mettre à jour SUIVI/ROADMAP/registre sans fusion automatique main.

## Preuves attendues

- Comparatif **avant/après** outils visibles par le modèle et taux d'exécution réussie sur les scénarios définis.
- Contrats MCP, catalogue et au moins un service ou adaptateur effectivement utilisé si techniquement utile ; si refus d'adopter MCP natif, justification instrumentée par comparaison.
- Skills créés, versionnés, enregistrés, accessibles, testés et **réutilisés** par JARVIS.
- Exécution réelle bout en bout Mac mini + Dell1 + GitHub, erreur corrigée, checkpoint repris et rapport de JARVIS confronté aux preuves indépendantes.
- Tests d'idempotence, de persistance du registre, de non-régression des capacités existantes.
- État de 14A après mission 25 clairement séparé ; publication sur branche et PR de mission25 avec rapports/tests/procédure.

Réception effective : [rapport final](RAPPORT-FINAL.md), [bilan14A](BILAN-14A.md), [preuves](PREUVES-JARVIS.json), [PR18](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/18). Le cahier ci-dessus est conservé.

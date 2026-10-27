# P7 — Supervision des cinq GPU et diagnostic agentique sur incident

**Statut : ajout documentaire demandé par le propriétaire le 27 octobre 2026. Planifié, non exécuté par ce document.**

## Identité de priorité (registre opérationnel P0–P9)

- **P7 — Supervision CPU/GPU Dell 2**, élargie à la supervision des **cinq GPU documentés** du laboratoire et au déclenchement de diagnostics agentiques lorsqu'une charge attendue s'arrête anormalement.
- Il ne s'agit **ni du P4 stratégique** créé lors d'une synthèse conversationnelle ni d'une phase d'exécution distincte ; préserver les numéros opérationnels : phase 1 = P0/P1, phase 2 = P2/P3/P4, priorités suivantes P5 à P9.
- Aucun redémarrage ni modification des phases lancées n'est autorisé implicitement par cette note.

## Acquis vérifiés et frontières

- Mac mini : RTX 3090 eGPU, modèle conversationnel ; Dell 1 : deux RTX 3090, Qwen 80B sur Ollama ; Dell 2 : **RTX 3090 24 GiB + RTX 3080 10 GiB**, pilote et tests CUDA indépendants validés le 25 octobre (mission 14B). Cela fait **cinq GPU** ; ne pas appeler les cinq « RTX 3090 ».
- Mission 26 phase 1 : exécution Dell1/Dell2 et décisions Qwen démontrées ; **cela ne prouve pas une inférence Ollama sur Dell 2**.
- PR #29 / mission 26 phase 2, état consulté le 27 octobre : **P2 reçue avec réserves**, **P3 reçue avec réserves**, **P4 lancée, non reçue** dans le rapport lu. Conserver leur historique, reçus, tâches et états ; ne pas les rejouer.
- Des fonctions de supervision JL-03 sont documentées. Le nouveau diagnostic agentique en cas de panne GPU n'est **pas** démontré installé.

## Fonction attendue

1. Un moniteur léger, indépendant de l'inférence IA (sur Mac mini avec sondes sur les machines disponibles), observe les GPU et les services, sans charger Qwen en permanence pour collecter des métriques.
2. Relever : présence PCI/NVIDIA, utilisation, VRAM, température, puissance si disponible, erreurs Xid/CUDA, PID/processus, état d'Ollama et de ses modèles, files et progression d'inférence, connectivité des nœuds. Conserver horodatages, hôte, GPU et source de mesure.
3. **Pas d'incident sur la seule VRAM vide** : distinguer repos, déchargement normal `keep_alive`, tâche attendue sans progrès, hang, crash, défaillance pilote/GPU, saturation thermique, service Ollama indisponible et perte réseau.
4. En anomalie confirmée, produire **un incident persistant dans les systèmes existants** et demander une micro-tâche de diagnostic au Mission Engine, sans nouveau moteur ni seconde mémoire concurrente.
5. JARVIS analyse lui-même les causes et choisit les contrôles puis la réparation adaptée dans le périmètre autorisé. Tester après correction la **progression réelle de la charge et la réponse fonctionnelle**, pas seulement l'état du service.
6. En cas d'indisponibilité du GPU Dell 1 qui héberge Qwen, conserver l'incident indépendamment de Qwen et utiliser un autre nœud/modèle **seulement si effectivement disponible et routable** ; sinon reporter le diagnostic avec preuves, sans prétendre l'avoir exécuté.
7. Remonter l'état d'incident, l'analyse, les actions et les preuves dans JL-03 ; transmettre l'expérience à la mémoire/AutoDream quand les composants seront disponibles.

## Dépendances vérifiées AVANT intégration à P7

| Priorité opérationnelle | Responsabilité | Contrat transversal sans duplication |
|---|---|---|
| **P2 — Trois boucles** | Typologie tentatives/échecs, stagnation et stratégie | Appliquer le compteur durable par **cause stable**, sans relancer mécaniquement trois fois le même restart ; distinguer collecte, test échoué et refus avant action. P2 historique reçue avec réserves dans PR29. |
| **P3 — Gestion durable du contexte** | Budget, mémoire opérationnelle, checkpoints | Donner à l'agent un **dossier court** contenant symptôme, télémétrie pertinente, mission impactée, dernière progression et références de preuves ; ne jamais injecter tous les logs. P3 reçue avec réserves. |
| **P4 — Diagnostic et correction du code réel** | Provenance application active / candidats et correction effective | Diagnostiquer séparément défaut GPU/pilote/service/routeur/application, vérifier PID/version active, éviter de corriger une copie ou un simple test sans réparer le service. P4 en cours, sans réception dans l'état lu. |
| **P5 — Contrats de réception** | Preuve indépendante du rétablissement | Exiger disponibilité GPU si pertinente, chargement effectif du modèle, inférence/réponse valide, progression et reprise de la mission impactée. Un GPU visible ou HTTP 200 seul ne suffit pas. |
| **P6 — Visibilité JL-03** | Journal UI des décisions et exécutions | Afficher incident, GPU réel, observations, diagnostic Qwen, corrections, test final et statut, réutiliser interfaces de preuves existantes. |
| **P9 — Réduction de l'assistance Codex** | Autonomie JARVIS et escalade | Diagnostiquer d'abord par JARVIS, appeler Codex uniquement sur blocage réel / réparation structurelle hors capacités de l'agent ; pas de validations humaines intermédiaires ajoutées. |

## Critères de réception proposés pour P7

- Les **cinq identités GPU réelles** sont reconnues et les états « inactif », « modèle déchargé normalement » et « calcul attendu interrompu » sont différenciés.
- Une panne simulée de service d'inférence, une déconnexion de nœud et un calcul qui ne progresse plus génèrent des incidents distincts, sans faux redémarrage lors du repos.
- L'incident est persistant et relié à une mission/tâche ; JARVIS reçoit le contexte bref, exécute un diagnostic tracé et choisit une réponse.
- La clôture repose sur les preuves fonctionnelles définies par P5 ; si aucun moteur de diagnostic n'est disponible, l'incident reste ouvert et documenté.
- Aucun acquis P2/P3/P4 n'est réinitialisé, aucune modification de l'architecture Ollama / du routage non validée n'est déduite de ce document.

## Sources de référence consultées

`AGENTS.md` ; `docs/CHARTE_DIRECTIVES_JARVIS.md` ; `docs/architecture/P0-P3-2026-10-25/PRIORITES-ET-PROGRESSION.md` (priorités historiques distinctes du registre P0–P9) ; PR #29, `docs/missions/26-P2/MISSION.md`, `REPRISE-27-OCTOBRE.md`, `M26_P2_P4_CODE_REEL.md` ; réception Dell2 mission 14B. Le suivi réel de P7 devra être porté dans le registre opérationnel approprié lors de sa consolidation.

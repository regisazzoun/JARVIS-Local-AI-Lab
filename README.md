# JARVIS — Local AI Lab

Laboratoire privé d’IA locale réparti entre un **Mac mini Debian** et un **Dell Precision n°1**. Le Mac mini porte la passerelle JARVIS, la mémoire et la voix ; le Dell fournit l’inférence GPU. Un deuxième Dell reste prévu pour un déploiement exécuté par JARVIS.

## État courant — bilan du 17 octobre 2026

Ce bilan décrit les derniers résultats documentés, pas une mesure de disponibilité en temps réel. Il est cohérent avec [SUIVI.md](SUIVI.md), [ROADMAP.md](ROADMAP.md) et le [registre consolidé des missions](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md). Les instantanés historiques conservés plus bas ne remplacent pas ces réceptions.

| Périmètre | Résultat établi | Réserves / suite |
| --- | --- | --- |
| Mac mini Debian | Passerelle conversationnelle, mémoire SQLite/FTS5, Whisper/Piper et outils agentiques documentés | Mémoire canonique sur le Mac ; orchestration distribuée globale encore partielle |
| Dell n°1 — 13D-E | Réception complète du 17/10 : Debian, RAID1, deux ESP, SSH/sudo, Ansible, NVIDIA/CUDA, Ollama, modèles et intégration JARVIS | Une RTX 3090 alimentée ; seconde carte en extension future. Correctif du reboot forcé du contrôleur avant réemploi |
| 11-Agentic / 11B | Outils hôte et administration distante SSH/Ansible pérenne validés | Compute Expansion reste partielle ; checkpoint 11B à reprendre hors audit |
| 14A | Exécutions réelles démontrées dans des scénarios ciblés | Réception globale de l’autonomie ouverte ; le guidage de Codex est explicite |
| Dell n°2 — 14 | Mission future, à exécuter par JARVIS lui-même | Le titre historique « 13D-E / 14 » du Dell n°1 ne vaut pas réception du second Dell |
| JL-01 / JL-02 | Launcher V1 préservé ; V2 publiée dans un dépôt distinct, GO avec réserves | Fiabilité agentique et tests des clients physiques restent à compléter |
| 15A macOS / 15B iOS | Cahiers natifs et cinq incréments chacun définis, non exécutés | Mission 14 non bloquante ; iOS gratuit via Xcode / Personal Team, PWA en alternative explicite |
| Mission 00 | 68 missions/sous-missions recensées, 28 anomalies ; inventaire réel JARVIS de 671 fichiers Markdown | Analyses JARVIS guidées et contrôlées par Codex ; les erreurs originales sont conservées et signalées |

## Accéder aux résultats

- [Rapport de consolidation — mission 00](docs/missions/00-Mission-Pilotage-point-26-10-17/RAPPORT-FINAL.md), [registre](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) et [anomalies](docs/missions/00-Mission-Pilotage-point-26-10-17/ANOMALIES-DOCUMENTAIRES.md).
- [Bilan des actions réellement exécutées par JARVIS](docs/missions/00-Mission-Pilotage-point-26-10-17/BILAN-AGENTIQUE-JARVIS.md), distinctes de celles de Codex.
- [Réception Dell n°1](docs/missions/13D-E/RECEPTION-MISSION14.md) et [raccordement administratif 11B](docs/missions/11B/RACCORDEMENT-ADMIN-DELL.md).
- [Launcher V1](https://regisazzoun.github.io/JARVIS-Launcher/) · [Launcher V2](https://regisazzoun.github.io/JARVIS-Launcher2/). Les fonctions privées nécessitent l’espace connecté et le tunnel/compagnon existant ; un écran public sans mesures ne prouve pas l’arrêt des machines.
- [Index des missions](docs/missions/README.md), [suivi](SUIVI.md), [roadmap](ROADMAP.md) et [chronologie](docs/chronologie.md).

Les modifications documentaires sont publiées sur une branche dédiée et proposées en PR, sans fusion automatique dans `main`. Les secrets, preuves privées brutes et identifiants matériels uniques restent hors du dépôt.

## Objectif

Documenter les tests reproductibles, les échecs, les contournements et les limites sans confondre hypothèses et résultats validés. L'objectif est d'avancer vers la faisabilité, pas de résoudre chaque anomalie secondaire avant de continuer.

## Historique — état documenté le 12 octobre 2026

| Composant | Mac mini | Dell Precision 5820 |
| --- | --- | --- |
| Debian et SSH | Documentés (mission 03) | Prévus |
| Pilote NVIDIA / eGPU | Missions 04–05 | Prévus |
| Calcul CUDA réel | Validé (mission 05D) | Non testé |
| Ollama / Llama 3.1 8B | InférenceGPU validée (05D) | Non testé |
| Open WebUI | Fonctionnel sur LAN (06) | Non testé |
| Optimisations conversation / RAG | Tests documentés (07) | Non testé |

**Attention :** les résultats Mac mini ne constituent pas des validations sur Dell.

## Documentation

- [Chronologie des missions](docs/chronologie.md)
- [Méthodologie expérimentale](docs/methodologie.md)
- [Mac mini](platforms/mac-mini/README.md)
- [Dell Precision 5820](platforms/dell-precision-5820/README.md)
- [Feuille de route](ROADMAP.md)
- [Suivi global des missions — tableau de bord](SUIVI.md)
- [Débrief de pilotage — mission 13F (GO AVEC RÉSERVES)](docs/missions/MISSION-13F-DEBRIEF.md)
- [Précautions de publication](SECURITY-PUBLICATION.md)

## Sources et confidentialité

Synthèse initiale des rapports de mission Codex reçus. Les preuves brutes, logs et données privées ne sont pas importés dans le dépôt. Chaque résultat reste à confronter au rapport source avant de publier un guide reproductible.

## Historique — pilotage du 14 octobre 2026

- Mission 13F : GO AVEC RÉSERVES.
- Mission 14 : déploiement Dell Precision, indépendant des applications.
- Mission 15A : application native macOS (Mac mini et MacBook).
- Mission 15B : application native iOS (iPhone et éventuellement iPad).
- Missions 15A et 15B réalisables en parallèle, avec API JARVIS commune.
- Installation iOS : Xcode pour les tests, Ad Hoc ou TestFlight à évaluer pour la diffusion privée ; PWA en solution alternative.

Les détails et les critères de validation sont décrits dans [ROADMAP.md](ROADMAP.md).

[Rapports récupérés sur JARVIS]( docs/missions/historique/README.md ) : 100 documents historiques repris avec provenance et expurgation.

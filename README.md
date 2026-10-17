# JARVIS — Local AI Lab

Laboratoire privé d’IA locale réparti entre un **Mac mini Debian** et un **Dell Precision n°1**. Le Mac mini porte la passerelle JARVIS, la mémoire et la voix ; le Dell fournit l’inférence GPU. Un deuxième Dell reste prévu pour un déploiement exécuté par JARVIS.

## État courant — bilan du 17 octobre 2026

Ce bilan décrit les derniers résultats documentés, pas une mesure de disponibilité en temps réel. Il est cohérent avec [SUIVI.md](SUIVI.md), [ROADMAP.md](ROADMAP.md) et le [registre consolidé des missions](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md). Les instantanés historiques conservés plus bas ne remplacent pas ces réceptions.

Cette synthèse regroupe les fonctions par périmètre ; le catalogue exhaustif de **68 identifiants**, plus bas, correspond ligne par ligne à SUIVI.

| Périmètre | Résultat établi | Réserves / suite |
| --- | --- | --- |
| Mac mini Debian | Passerelle conversationnelle, mémoire SQLite/FTS5, Whisper/Piper et outils agentiques documentés | Mémoire canonique sur le Mac ; orchestration distribuée globale encore partielle |
| Dell n°1 — 13D-E | Réception complète du 17/10 : Debian, RAID1, deux ESP, SSH/sudo, Ansible, NVIDIA/CUDA, Ollama, modèles et intégration JARVIS | Une RTX 3090 alimentée ; seconde carte en extension future. Correctif du reboot forcé du contrôleur avant réemploi |
| 11-Agentic / 11B | Outils hôte et administration distante SSH/Ansible pérenne validés | Compute Expansion reste partielle ; checkpoint 11B à reprendre hors audit |
| 14A | Exécutions réelles démontrées dans des scénarios ciblés | Réception globale de l’autonomie ouverte ; le guidage de Codex est explicite |
| Dell n°2 — 14 | Mission future, à exécuter par JARVIS lui-même | Le titre historique « 13D-E / 14 » du Dell n°1 ne vaut pas réception du second Dell |
| JL-01 / JL-02 | Launcher V1 préservé ; V2 publiée dans un dépôt distinct, GO avec réserves | Fiabilité agentique et tests des clients physiques restent à compléter |
| 15A macOS / 15B iOS | Cahiers natifs et cinq incréments chacun définis, non exécutés | Mission 14 non bloquante ; iOS gratuit via Xcode / Personal Team, PWA en alternative explicite |
| Mission 00 | 68 missions/sous-missions recensées, 28 anomalies ; inventaire réel JARVIS de 671 fichiers Markdown | GO avec réserves ; 129 documents/preuves récupérés. Analyses JARVIS guidées et contrôlées par Codex, erreurs originales conservées |

<!-- BEGIN MISSION CATALOGUE -->
## Catalogue des missions — 68 identifiants

**68 missions et sous-missions recensées**, dont dix incréments 15A/15B prévus, non exécutés. Cette liste reprend exactement les identifiants, intitulés et états du tableau courant de [SUIVI.md](SUIVI.md). Les lignes « 09 à 11 » (regroupement historique) et « Documentation » (activité transversale) ne sont pas des missions supplémentaires et ne sont pas comptées.

| Mission | Objet / étapes | État |
| --- | --- | --- |
| **00** | Audit général et concordance documentaire | ✅ GO avec réserves |
| **01** | Audit de JARVIS | 🟡 PARTIEL |
| **02** | Configuration Apple T2 et administration Debian | 🟡 PARTIEL |
| **02B** | Administration et préparation système | 🟡 Préparation et script testés ; administration non exécutée |
| **03** | Debian 13, démarrage, diagnostic, SSH du Mac mini | ✅ Réalisée avec réserves |
| **04** | GRUB, Thunderbolt et eGPU NVIDIA | 🟡 Réalisée avec réserves |
| **04B** | À confirmer : intitulé à réconcilier | 🟡 À confirmer |
| **04C** | Plan exact, non exécuté | 📋 Préparée |
| **04E** | Plan d’essai et récupération | 📋 Préparée |
| **04G** | vérification après branchement du Razer Core | 🟡 Non concluante |
| **04H** | validation de la réallocation PCIe | 🟡 Échec historique |
| **04I** | Entrée réserve PCIe 512M installée | 🟡 Configuration installée, essai non établi |
| **04J** | vérification avant branchement | 🟡 Non concluante |
| **04K** | limitations PCIe du Mac mini 2018 | 🟡 Étude terminée |
| **04L** | préparation de la réallocation PCIe ciblée | 🟡 Configuration installée, essai non établi |
| **04M** | validation de la réallocation PCIe ciblée | 🟡 Non concluante |
| **04N** | Complément Mission 04N — Installation autorisée | 🟡 Configuration installée, candidat non testé |
| **04O** | Vérification des ressources PCIe NP/PREF avant essai eGPU | 🟡 Vérification préparatoire positive |
| **04P** | validation de la réallocation PCIe | 🟡 Allocation PCIe testée |
| **04Q** | écran conservant le fond GRUB | 🟡 Diagnostic exécuté |
| **04R** | disparition du GPU Intel avec Core présent au boot | 🟡 Diagnostic exécuté |
| **04S** | Essais comparatifs DEVEN avec/sans Core | 🟡 À confirmer : rapport autonome manquant |
| **04T** | préparation du diagnostic pré-Linux de DEVEN | 📋 Préparée |
| **04U** | localiser le masquage Intel entre GRUB et Linux | 🟡 Analyse exécutée |
| **04V** | préparation de la mesure DEVEN en fin de GRUB | 📋 Préparée |
| **04W** | Analyse d'un démarrage interrompu | 🟡 Analyse réalisée |
| **05A** | Sélection du pilote NVIDIA | ✅ Préparation réalisée |
| **05B** | Installation contrôlée du pilote | 🟡 Réalisée avec réserves |
| **05B-A** | audit des avertissements NVIDIA objtool | 🟡 Audit terminé avec conditions |
| **05B-P** | préparation sécurisée NVIDIA | 📋 Préparation terminée |
| **05C** | Détection eGPU et CUDA initial | ✅ Testée |
| **05D** | Calcul GPU, Ollama et Llama 3.1 8B | ✅ Validée sur Mac mini, confortée par 13F |
| **06** | Open WebUI et accès conversationnel | 🟡 Fonctionnelle, disponibilité reconfirmée par 13F |
| **07** | Qualité des réponses et RAG | 🟡 Partiellement confortée par 13F |
| **08** | Ministral3 14B et comparaison de raisonnement | 🟡 Installation testée ; qualité limitée |
| **09** | validation rapide RTX 3090 / CUDA | 🟡 CUDA validé ; Ollama GPU en échec historique |
| **09B** | Correction du verrou GPU Ollama | 🟡 Correction testée |
| **10** | Qwen 3.5 27B : installation et évaluation | 🟡 Installation testée ; qualité partielle |
| **11** | Audit statique Jarvis Voice | 🟡 Étude terminée ; intégration intégrale NO-GO |
| **11-Agentic** | Habilitations hôte persistantes | 🟡 GO AVEC RÉSERVES |
| **11B** | Compute Expansion et administration Dell | 🟡 Raccordement validé ; extension complète partielle |
| **12** | Étude voix et mémoire | ✅ GO sous conditions historique ; architecture consolidée en 13F |
| **13A** | Socle vocal durable Whisper/Piper | ✅ Réussie ; fonctionnement backend consolidé par 13F |
| **13B** | Interface vocale, Push-to-Talk | 🟡 GO PARTIEL historique ; consolidation technique 13F |
| **13C** | Mémoire persistante canonique | 🟡 GO PARTIEL historique ; fonctions centrales consolidées |
| **13D** | Sécurisation des accès distants (mission globale) | 🟡 GO AVEC RÉSERVES — accès multi-postes |
| **13D-E** | Premier Dell Precision — installation et serveur IA via Codex | ✅ Réception complète 17/10/2026 |
| **13D.1** | MacBook : Tailscale, SSH par clé et par mot de passe | ✅ Validée le 15/10 |
| **13D.2** | MacBook : alias `ssh jarvis`, reconnexion et tmux | ✅ Validée le 15/10 |
| **13D.3** | Accès Mac mini macOS et MacBook, SSH/Tailscale, secours | 🟡 Accès multi-postes validés, contrôles finaux à compléter |
| **13E** | Passerelle conversation, voix et mémoire | 🟡 GO AVEC RÉSERVES retrouvé |
| **13F** | Conversation, mémoire v3 et outils agentiques | ✅ **GO AVEC RÉSERVES** |
| **14** | **Deuxième Dell Precision — déploiement par JARVIS lui-même, sans Codex comme opérateur** | ⏳ Prévue, non réceptionnée |
| **14A** | Aptitude agentique de JARVIS avant deuxième Dell | 🟡 Progression prouvée ; réception globale ouverte |
| **15A** | Application native SwiftUI macOS | 📋 Préparée, non lancée |
| **15A.1** | macOS — Architecture/UI | 📋 Prévue, non exécutée |
| **15A.2** | macOS — Connectivité sécurisée | 📋 Prévue, non exécutée |
| **15A.3** | macOS — Conversation, voix et mémoire | 📋 Prévue, non exécutée |
| **15A.4** | macOS — Pilotage des missions | 📋 Prévue, non exécutée |
| **15A.5** | macOS — Distribution et tests | 📋 Prévue, non exécutée |
| **15B** | Application native SwiftUI iOS | 📋 Préparée, non lancée |
| **15B.1** | iOS — Architecture/UI | 📋 Prévue, non exécutée |
| **15B.2** | iOS — Connectivité sécurisée | 📋 Prévue, non exécutée |
| **15B.3** | iOS — Conversation, voix et mémoire | 📋 Prévue, non exécutée |
| **15B.4** | iOS — Mémoire et validations | 📋 Prévue, non exécutée |
| **15B.5** | iOS — Installation gratuite et réception | 📋 Prévue, non exécutée |
| **JL-01** | Launcher macOS et GitHub Pages : SSH, Terminal, Codex, tmux | ✅ GO AVEC RÉSERVES — deux Macs utilisés |
| **JL-02** | LauncherV2 — conversation et supervision agentique | 🟡 Livrée — GO AVEC RÉSERVES |

Catalogue synchronisé avec `python3 agentic/mission00/sync-mission-index.py --write`. Sans option, la commande vérifie la concordance ligne par ligne.
<!-- END MISSION CATALOGUE -->

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

[Rapports et preuves Launcher récupérés](docs/missions/README.md#rapports-launcher-récupérés) : 29 documents supplémentaires ; total du manifeste : 129.

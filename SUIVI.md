# JARVIS — SUIVI GLOBAL DES MISSIONS

**Dernière mise à jour : 17 octobre 2026**  
**Références :** [Feuille de route](ROADMAP.md) · [Chronologie](docs/chronologie.md) · [Débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md) · [Roadmap Launcher](docs/parallel-projects/JARVIS-Launcher/ROADMAP.md)

> **Tableau de pilotage permanent.** Conserver la présentation, l'ordre des colonnes, les intitulés, les identifiants de missions et les lignes historiques lors de chaque mise à jour. Modifier uniquement les informations nécessaires, ajouter une ligne si un nouveau jalon apparaît, dater et expliquer les changements dans le journal. Ne jamais déduire un GO de la seule existence de fichiers. Les étapes sans rapport complet restent « à confirmer ». Les statuts représentent la dernière information documentée, pas une surveillance temps réel.


> **Point du 17 octobre — mission 00 :** [README courant](README.md) et [registre](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) réconciliés : 68 missions/sous-missions, 28 anomalies. 13D-E = Dell n°1 reçu ; 14 = Dell n°2 futur exécuté par JARVIS ; 14A ouverte ; 11B partielle ; JL-02 livrée avec réserves. Les sections datées ci-dessous conservent leurs états historiques.

## Vue d'ensemble — toutes les missions

| Mission | Objet / étapes | État | Résultat vérifié / réserves | Prochaine action |
| --- | --- | --- | --- | --- |
| **03** | Debian 13, démarrage, diagnostic, SSH du Mac mini | ✅ Réalisée avec réserves | Diagnostics et premières procédures documentés ; certains états intermédiaires historiques | Consolider les procédures et preuves |
| **04** | GRUB, Thunderbolt et eGPU NVIDIA | 🟡 Réalisée avec réserves | Investigations et contournements documentés ; essais de démarrage non concluants | Documenter les cas restant ouverts |
| **04W** | Analyse d'un démarrage interrompu | 🟡 Analyse réalisée | Entrée dans le noyau non prouvée sur les traces considérées | Conserver la réserve |
| **05A** | Sélection du pilote NVIDIA | ✅ Préparation réalisée | Choix de pilote documenté ; cette étape seule ne valide pas le fonctionnement | Se référer aux tests 05C/05D |
| **05B** | Installation contrôlée du pilote | 🟡 Réalisée avec réserves | Installation documentée ; vérifier les réserves DKMS du rapport | Consolider les preuves |
| **05C** | Détection eGPU et CUDA initial | ✅ Testée | Tests matériels et CUDA léger documentés | Référence 05D |
| **05D** | Calcul GPU, Ollama et Llama 3.1 8B | ✅ Validée sur Mac mini, confortée par 13F | Calcul CUDA et inférenceGPU réels en 05D ; Ollama et inférences réelles retestés en 13F (sans nouveau benchmark comparatif) | Maintenir la non-régression |
| **06** | Open WebUI et accès conversationnel | 🟡 Fonctionnelle, disponibilité reconfirmée par 13F | Service actif et santé HTTP retestée en 13F ; réserve historique HTTP local non chiffré non levée | Poursuivre sécurisation sans perturber le service |
| **07** | Qualité des réponses et RAG | 🟡 Partiellement confortée par 13F | Gestion du contexte et réponses écrites/orales améliorées en 13F ; performances RAG de 07 non revalidées intégralement | Garder la réserve RAG ; étendre les tests si nécessaire |
| **08** | Ministral3 14B et comparaison de raisonnement | 🟡 Installation testée ; qualité limitée | Rapport08 retrouvé :41/41couches GPU ; comparaison Llama/Ministral ; commandes proposées non exécutées | Conserver réserves de qualité ; voir registre00 |
| **09 à 11** | Regroupement historique — détaillé ci-dessous | 📋 Rapports retrouvés et réconciliés | 09CUDA/CPU puis09Bcorrection GPU ;10Qwen ;11auditJarvisVoice,distinct11-Agentic | Lire les lignes individuelles et le registre00 |
| **12** | Étude voix et mémoire | ✅ GO sous conditions historique ; architecture consolidée en 13F | Choix Whisper/Piper/SQLite concrétisés et chaîne backend/mémoire réelles testées en 13F ; validation acoustique physique encore nécessaire | Conserver verdict d'étude ; suivre les réserves physiques |
| **13A** | Socle vocal durable Whisper/Piper | ✅ Réussie ; fonctionnement backend consolidé par 13F | Whisper Small et Piper Tom réutilisés et retestés en chaîne réelle en 13F ; pas de nouveau test micro/haut-parleurs physiques | Garder la validation matérielle dans les missions clientes |
| **13B** | Interface vocale, Push-to-Talk | 🟡 GO PARTIEL historique ; consolidation technique 13F | Interface, chaîne vocale et échanges navigateur réels testés en 13F (micro WAV artificiel) ; VAD/interruption expérimentaux, périphériques physiques non revalidés | Tester la voix sur micro/haut-parleurs réels et clients Apple |
| **13C** | Mémoire persistante canonique | 🟡 GO PARTIEL historique ; fonctions centrales consolidées | SQLite/FTS5v3 et trois moteurs testés 13F ; requêtes modèle Dell via passerelle intégrées 13D-E/JL-02 | Préserver autorité Mac ; réplication/placementdistribués non globalement réceptionnés |
| **13D.1** | MacBook : Tailscale, SSH par clé et par mot de passe | ✅ Validée le 15/10 | Connexion SSH par les deux méthodes testée ; clé publique ajoutée sans retirer les accès existants | Préserver **les deux méthodes** d'accès |
| **13D.2** | MacBook : alias `ssh jarvis`, reconnexion et tmux | ✅ Validée le 15/10 | Alias SSH fonctionnel ; sessions existantes préservées ; création, détachement et reprise de `jarvis-test` réussis | Réutiliser les accès dans Launcher |
| **13D.3** | Accès Mac mini macOS et MacBook, SSH/Tailscale, secours | 🟡 Accès multi-postes validés, contrôles finaux à compléter | Mac mini macOS confirmé fonctionnel lors des tests du 14/10 par l'utilisateur ; MacBook testé le 15/10 (clé + mot de passe, alias, tmux). Aucun changement de configuration SSH serveur signalé, hormis l'ajout de la clé publique MacBook | Vérifier uniquement la persistance après reboot et la journalisation lorsque l'accès de secours sur place sera disponible |
| **13D-E** | Premier Dell Precision — installation et serveur IA via Codex | ✅ Réception complète 17/10/2026 | Debian/RAID1/deux ESP, SSH mot de passe + clé et sudo, Ansible idempotent, RTX 3090/CUDA, Ollama Qwen/Ministral/Llama, intégration JARVIS ; contrôle supplémentaire 17 h 18 sans service en échec ; voir [réception](docs/missions/13D-E/RECEPTION-MISSION14.md) et [rapport final](docs/missions/13D-E/RAPPORT-FINAL.md) | Préserver les acquis ; corriger le reboot forcé du contrôleur avant nouveau déploiement ; ne pas confondre avec mission 14 sur Dell n°2 |
| **13D** | Sécurisation des accès distants (mission globale) | 🟡 GO AVEC RÉSERVES — accès multi-postes | Accès des deux Macs confirmés ; clés et mots de passe préservés ; administration Dell distincte réceptionnée 13D-E/11B | Conserver réserves clients/reboot/journaux13D ; ne plus bloquer sur SSHDell déjà validé |
| **13E** | Passerelle conversation, voix et mémoire | 🟡 GO AVEC RÉSERVES retrouvé | Rapport et tests 13E publiés dans PR1 ; Ollama/STT/TTS/Chromium réels, audio artificiel ; confortés 13F | ClientsApple/micro/HTTPSdistants restent à réceptionner |
| **13F** | Conversation, mémoire v3 et outils agentiques | ✅ **GO AVEC RÉSERVES** | 27 tests backend, 8 API, 8 navigateur et 6 finaux ; autonomie Qwen prouvée dans laboratoire isolé, non sur Dell | Suivre réserves voix physique, reboot et opérations longues ; [débrief](docs/missions/MISSION-13F-DEBRIEF.md) |
| **14A** | Aptitude agentique de JARVIS avant deuxième Dell | 🟡 Progression prouvée ; réception globale ouverte | 13F laboratoire,11/11Bhôte / distant,JL02tâchesréelles ;00 ajouteanalysesdocumentaires | Consolider critères 14A,ne pasdéclarer autonomiecomplète par procuration |
| **14** | **Deuxième Dell Precision — déploiement par JARVIS lui-même, sans Codex comme opérateur** | ⏳ Prévue, non réceptionnée | Dell n°1 installé par Codex (13D-E) ; cela ne démontre pas l'autonomie agentique de JARVIS sur Dell n°2 | Après 14A : JARVIS prépare, déploie, diagnostique et valide le second Dell dans le périmètre autorisé, sans GO intermédiaires |
| **15A** | Application native SwiftUI macOS | 📋 Préparée, non lancée | [Cahier Codex](docs/missions/MISSION-15A-MACOS-CODEX.md) disponible | Inventaire API 13F, contrat commun, développement |
| **15B** | Application native SwiftUI iOS | 📋 Préparée, non lancée | [Cahier Codex](docs/missions/MISSION-15B-IOS-CODEX.md) ; installation gratuite Xcode/Personal Team retenue | Contrat API commun et prototype iPhone |
| **JL-01** | Launcher macOS et GitHub Pages : SSH, Terminal, Codex, tmux | ✅ GO AVEC RÉSERVES — deux Macs utilisés | Mac mini fonctionnel confirmé le 14/10 ; MacBook : compagnon local, connexion SSH, reprise tmux et trois actions du site GitHub Pages déclarées fonctionnelles par l'utilisateur le 15/10. Autres commandes et sécurité complète non toutes réceptionnées | Garder les tests acquis ; documenter uniquement les actions restantes sans retester inutilement |
| **JL-02** | LauncherV2 — conversation et supervision agentique | 🟡 Livrée — GO AVEC RÉSERVES | SiteV2publié ; Qwenoutilsréels,voix synthétique,métriques etévénements testés ; espaceconnecté confirmé propriétaire | Suivre réserves nativesetfiabilitéagentique ; préserver V1 |
| **Documentation** | Rapports, roadmap, gouvernance | 🔄 En continu | Synthèse, débrief 13F et cahiers 15A/15B présents | Synchroniser `SUIVI.md` après chaque changement d'état |
| **00** | Pilotage — point du 17/10 | 🟡 En cours de réception documentaire | Audit GitHub et délégations réelles à compléter au bilan | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Publier les preuves et le registre sans merge main |
| **01** | Audit de JARVIS | 🟡 PARTIEL | Audit matériel en lecture seule ; accès hôte limité par le bac à sable. | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Retrouver le verdict et les preuves manquantes |
| **02** | Configuration Apple T2 et administration Debian | 🟡 PARTIEL | Préparer Debian et le support T2 ; validation complète différée. | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Retrouver le verdict et les preuves manquantes |
| **02B** | Administration et préparation système | 🟡 Préparation et script testés ; administration non exécutée | Diagnostics accessibles, script créé et syntaxe/aide/refus en bac à sable testés ; aucun OpenSSH Server installé dans cette mission | Voir le registre 00 et les étapes suivantes |
| **04B** | À confirmer : intitulé à réconcilier | 🟡 À confirmer | Références et preuves identifiées ; rapport autonome non retrouvé | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04C** | Plan exact, non exécuté | 📋 Préparée | Plan exact non exécuté | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04E** | Plan d’essai et récupération | 📋 Préparée | Plan d’essai et de récupération | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04G** | vérification après branchement du Razer Core | 🟡 Non concluante | Branchement déclaré ; visibilité hôte insuffisante | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04H** | validation de la réallocation PCIe | 🟡 Échec historique | BAR1/BAR3 non attribués dans cet essai | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04I** | Entrée réserve PCIe 512M installée | 🟡 Configuration installée, essai non établi | Entrée GRUB réserve PCIe 512M installée après autorisation ; addendum prioritaire | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04J** | vérification avant branchement | 🟡 Non concluante | Vérification avant branchement, données hôte manquantes | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04K** | limitations PCIe du Mac mini 2018 | 🟡 Étude terminée | Analyse des limitations PCIe, aucun essai | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04L** | préparation de la réallocation PCIe ciblée | 🟡 Configuration installée, essai non établi | Addendum : entrée de réallocation installée, pas de reboot dans cette étape | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04M** | validation de la réallocation PCIe ciblée | 🟡 Non concluante | PREF reconstruit, NP insuffisant ; visibilité incomplète | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04N** | Complément Mission 04N — Installation autorisée | 🟡 Configuration installée, candidat non testé | Candidat NP32M + PREF512M installé avant reboot manuel | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04O** |  | 🟡 Vérification préparatoire positive | NP/PREF utilisables sans Core ; ne démontre pas le fonctionnement GPU | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04P** | validation de la réallocation PCIe | 🟡 Allocation PCIe testée | Quadro et fonctions associées correctement allouées ; pilote/calcul non validés ici | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04Q** | écran conservant le fond GRUB | 🟡 Diagnostic exécuté | Écran fond GRUB : collecte en lecture seule | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04R** | disparition du GPU Intel avec Core présent au boot | 🟡 Diagnostic exécuté | Intel masqué avec Core présent ; origine firmware probable non prouvée | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04S** | Essais comparatifs DEVEN avec/sans Core | 🟡 À confirmer : rapport autonome manquant | Résultats propriétaire cités dans 04T/04U, pas de nouvelle collecte | Voir registre mission 00 |
| **04T** | préparation du diagnostic pré-Linux de DEVEN | 📋 Préparée | Méthode de mesure pré-Linux DEVEN, non exécutée | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04U** | localiser le masquage Intel entre GRUB et Linux | 🟡 Analyse exécutée | Transition DEVEN observée entre GRUB et Linux ; auteur non identifié | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **04V** | préparation de la mesure DEVEN en fin de GRUB | 📋 Préparée | Mesure de fin GRUB conçue ; pas d’essai | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver le résultat historique ; aucune nouvelle expérience dans mission 00 |
| **05B-A** | audit des avertissements NVIDIA objtool | 🟡 Audit terminé avec conditions | Audit objtool et modules sur disque ; pas une qualification GPU de production | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Retrouver le verdict et les preuves manquantes |
| **05B-P** | préparation sécurisée NVIDIA | 📋 Préparation terminée | Qualification APT, authenticité et sauvegardes prévues ; aucune installation à ce stade | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Retrouver le verdict et les preuves manquantes |
| **09** | validation rapide RTX 3090 / CUDA | 🟡 CUDA validé ; Ollama GPU en échec historique | Calcul CUDA correct ; Ollama s’exécutait sur CPU | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Lire 09B sans effacer le constat initial |
| **09B** | Correction du verrou GPU Ollama | 🟡 Correction testée | Retrait du verrou ancien ; 33/33 couches Llama et inférenceGPU réelles | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Préserver la correction ; pas de répétition du benchmark |
| **10** | Qwen 3.5 27B : installation et évaluation | 🟡 Installation testée ; qualité partielle | 65/65 couches GPU et échanges WebUI ; comparaison indicative | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Retrouver le verdict et les preuves manquantes |
| **11** | Audit statique Jarvis Voice | 🟡 Étude terminée ; intégration intégrale NO-GO | Audit statique du candidat bigsk1 et alternatives ; option modulaire sous conditions | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Conserver cet audit distinct du jalon 11-Agentic |
| **11-Agentic** | Habilitations hôte persistantes | 🟡 GO AVEC RÉSERVES | 42 contrôles documentés, outils réels, reprise Qwen | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Réutiliser les capacités acquises |
| **11B** | Compute Expansion et administration Dell | 🟡 Raccordement validé ; extension complète partielle | Écriture/relecture réelle Qwen avant et après restart, SSH/Ansible testés | [Fiche, sources et réserves](docs/missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) ; Reprendre le checkpoint sans réinstallation ; vérifier les capacités restantes |

## Consolidations transversales — preuves apportées par 13F

La **réception historique** d'une mission est conservée (ex. « GO PARTIEL »), même lorsqu'une mission ultérieure valide ses fonctionnalités. Le **statut technique actuel** est alors complété avec la preuve précise et les réserves non levées : une validation de fonctionnalité ne transforme pas rétroactivement le verdict de mission.

| Mission source | Fonction consolidée en 13F | Réserve effectivement levée | Réserve conservée / limite | Référence |
| --- | --- | --- | --- | --- |
| 05D | Inférences Ollama réelles de nouveau opérationnelles | Disponibilité de l'inférence reconfirmée | Aucun nouveau benchmark GPU équivalent à 05D | [Débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md) |
| 06 | Open WebUI actif, contrôle santé HTTP réussi | Disponibilité technique reconfirmée | Sécurisation HTTP/TLS non validée par 13F | [Rapport 13F (PR n°4)](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/4) |
| 07 | Résumés vocaux, contexte et gestion des réponses améliorés | Amélioration conversationnelle documentée | Évaluation RAG historique non entièrement reprise | [Débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md) |
| 12 | Architecture voix/mémoire devenue opérationnelle | Passage de l'étude à une implémentation backend testée | Les limites de l'étude et les tests acoustiques ne sont pas effacés | [Débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md) |
| 13A | Whisper Small et Piper Tom réutilisés en chaîne | Fonctionnement intégré backend démontré | Micro et haut-parleurs physiques non retestés en 13F | [Tests 13F (PR n°4)](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/4) |
| 13B | Conversation vocale, réponse orale distincte, navigateur | Partie backend/navigateur des réserves initiales couverte | Acoustique physique, VAD heuristique, interruption expérimentale | [Tests 13F (PR n°4)](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/4) |
| 13C | Mémoire SQLite/FTS5 v3 et trois moteurs réels | Simulation multi-modèles remplacée par essais réels ; restauration/dédoublonnage vérifiés | Mémoire partagée inter-machines et catalogue automatique illimité non démontrés | [Débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md) |
| 13E | API et boucle vocale technique réelles | Intégration backend/navigateur démontrée | Rapport de réception 13E non retrouvé dans le suivi ; pas de validation physique iPhone/Safari par 13F | [Rapport 13F (PR n°4)](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/4) |

**Important :** la 13F ne prouve pas que les missions 08–11 sont clôturées. Leur rapport et leur périmètre restent à réconcilier ; les réserves purement matérielles, SSH et Dell ne sont pas levées par un test backend.

## Mise à jour du 17 octobre 2026 — répartition des deux Dell

- **Dell n°1 / 13D-E :** réception complète par Codex, voir [réception](docs/missions/13D-E/RECEPTION-MISSION14.md) et [bilan de corrections](docs/missions/13D-E/RAPPORT-FINAL.md). RAID [UU] et services essentiels actifs à 17 h 18 ; défaut de reboot forcé du contrôleur à corriger avant réemploi. Le titre historique « mission 14 » du rapport ne clôture pas la mission 14 du deuxième Dell.
- **Dell n°2 / 14 :** installation et intégration à effectuer par JARVIS lui-même, sans Codex comme exécutant. 14A reste la démonstration agentique distincte. Aucune approbation humaine intermédiaire à ajouter une fois la mission autorisée lancée.

## Décision 13D-E / mission 14 — autonomie en laboratoire

**Décision du 15 octobre 2026 :** JARVIS teste **sans supervision humaine** la chaîne d'installation automatisée UEFI/PXE sur des VM et disques virtuels dédiés, dans un périmètre de laboratoire préautorisé. Il peut diagnostiquer, corriger et recommencer ses essais, puis restitue journal et preuves. La première connexion SSH au Dell physique intervient **après** l'installation Debian/PXE : JARVIS aura lui-même injecté sa clé publique et configuré le service SSH. Ces capacités sont **à préparer/tester**, pas encore validées. Les opérations destructives sur les SSD/RAID/firmware réels restent soumises à autorisation ciblée préalable ; les deux modes SSH du Mac mini sont conservés.

## Focus opérationnel — 13D côté MacBook

| Fonctionnalité | Statut | Preuve / condition |
| --- | --- | --- |
| Tailscale MacBook → JARVIS | ✅ Validé | Connexion SSH à JARVIS via l'adresse Tailscale observée |
| SSH par clé ED25519 | ✅ Validé | Connexion réelle avec la clé dédiée du MacBook |
| SSH par mot de passe | ✅ Validé | Connexion réelle forcée en mode mot de passe |
| Alias `ssh jarvis` | ✅ Validé | Connexions successives réussies |
| Reconnexion SSH | ✅ Validé | Sessions SSH successives réussies |
| Persistance tmux | ✅ Validé | `jarvis-test` reste listée après détachement |
| Reprise de session tmux | ✅ Validé | Retour explicite de l'utilisateur dans `jarvis-test` |
| Sessions historiques | ✅ Préservées | `jarvis-13f` et `jarvis-codex` retrouvées dans `tmux ls` |
| Intégration Launcher sur MacBook | ✅ Testée le 15/10 | Profil et application locale reconnus ; SSH/tmux fonctionnels ; trois actions du site GitHub Pages confirmées par l'utilisateur |
| Mot de passe SSH en secours | 🔒 Maintenu | Ne **pas** désactiver avant décision distincte et accès de secours éprouvé |
| Accès depuis Mac mini macOS | ✅ Confirmé (14/10) | Tests du 14 octobre confirmés par l'utilisateur le 15/10 ; pas de nouveau test exécuté ici |
| Configuration SSH serveur | 🔒 Préservée | Seul ajout déclaré : clé publique du MacBook dans les clés autorisées ; aucune modification de `sshd_config` demandée |
| Validation globale 13D | 🟡 GO AVEC RÉSERVES | Deux postes opérationnels ; tests après reboot et audit des journaux différés |

## Priorités et règles permanentes

**Séquence stratégique actuelle :** 13D (GO AVEC RÉSERVES sur les accès) → 14A → 14. Missions 15A/15B techniquement parallèles, mais priorité moindre à ce stade. Launcher suit son propre chantier, avec la sécurité 13D comme dépendance pour les accès distants et JL-02.

**Protection des accès :** garder SSH par **clé et mot de passe** sur le serveur jusqu'à décision explicite après validation ; ne pas modifier automatiquement le serveur à partir du constat positif côté MacBook.

**Format immuable :** chaque future modification doit conserver les deux tableaux, leurs colonnes et séparateurs Markdown, leurs emoji de statut, les sections et les lignes historiques. Toute nouvelle mission reçoit une nouvelle ligne ; aucune mission ne doit disparaître sans entrée d'historique explicite. Ne pas réorganiser le fichier au gré des mises à jour.

**Légende :** ✅ validée ou réalisée selon périmètre décrit ; 🟡 partielle / réserves / réception incomplète ; 🔄 en cours ; 📋 préparée ; ⏳ en attente ; ⚪ preuve à confirmer ; 🔒 protection maintenue.

## Journal des mises à jour

| Date | Mission | Modification | Source / preuve |
| --- | --- | --- | --- |
| 2026-10-17 | 00 — pilotage | Réconciliation archives/branches ; rapports 08–11/13E retrouvés ; séparation 13D-E/14A/14,11/11B et JL-02 ; historique préservé | [Rapport 00](docs/missions/00-Mission-Pilotage-point-26-10-17/RAPPORT-FINAL.md) · [Anomalies](docs/missions/00-Mission-Pilotage-point-26-10-17/ANOMALIES-DOCUMENTAIRES.md) |
| 2026-10-16 | 13D-E — installation autonome | Propriétaire autorise réseau/effacement/reboot/administration ; seul lancement PXE humain ; qualification RAID/EFI et deux boots isolés acquise, image réelle préparée | [Prompt prioritaire](docs/missions/13D-E/PROMPT-INSTALLATION-AUTONOME.md) · [Tests](docs/missions/13D-E/TESTS.md) |
| 2026-10-16 | 13D-E — découverte physique | Rapport automatiquement reçu ; services temporaires arrêtés ; manifeste installation refusé (lecteur SD vide/profil DMI), BIOS à revoir ; aucun effacement | [Réception](docs/missions/13D-E/RAPPORT-FINAL.md) · [Tests](docs/missions/13D-E/TESTS.md) |
| 2026-10-16 | 13D-E — bootstrap A/B | PXE UEFI physique acquis ; découverte automatique bloquante et bootstrap SSH temporaire/transition par clé préparés ; 22 tests + récepteur ; RAID/EFI et installation non réceptionnés ; trois autorisations distinctes | [Bootstrap](docs/missions/13D-E/BOOTSTRAP-AUTOMATISE.md) · [Tests](docs/missions/13D-E/TESTS.md) |
| 2026-10-15 | 13D-E — reprise physique | GO AVEC RÉSERVES préparatoire ; outils réaudités, sources authentifiées, garde disques, templates ProxyDHCP et initrd candidat ; 16 tests et 2 syntax-check ; pas de service PXE LAN ni installation physique ; laboratoire complet non préalable | [Procédure](docs/missions/13D-E/DEPLOIEMENT-PHYSIQUE.md) · [Tests](docs/missions/13D-E/TESTS.md) · [Réception](docs/missions/13D-E/RAPPORT-FINAL.md) |
| 2026-10-15 | 13D-E — préparation technique | Audit non destructif, inventaires/rôles, templates Debian/iPXE et worker borné livrés ; 6 tests de garde-fous ; NO-GO réception complète faute de tests VM/PXE/Ansible et intégration agent ; accès existants préservés | [Audit](docs/missions/13D-E/AUDIT.md) · [Tests](docs/missions/13D-E/TESTS.md) · [Réception](docs/missions/13D-E/RAPPORT-FINAL.md) |
| 2026-10-15 | JL-01 — GitHub Pages MacBook | Compagnon local vérifié, SSH et tmux testés, puis trois actions de l'interface web confirmées fonctionnelles ; GO AVEC RÉSERVES JL-01, pas de validation implicite de toutes les fonctions | Tests et confirmation explicite de l'utilisateur du 15/10 ; [site GitHub Pages](https://regisazzoun.github.io/JARVIS-Launcher/) |
| 2026-10-15 | 13D-E / 14 | Correction de l'ordre PXE : pas de SSH Dell avant installation ; JARVIS teste seul et sans supervision les déploiements en VM isolée, puis configure lui-même SSH sur Debian | Décision explicite utilisateur en conversation de pilotage ; [ROADMAP](ROADMAP.md) |
| 2026-10-15 | 13D-E | Contrôle du suivi : préparation SSH/Ansible vers Dell non encore vérifiée ; ne pas confondre GO des accès Mac avec capacité d'administration Dell | Relecture de SUIVI.md et confirmation de l'absence de test Dell dans les rapports consultés |
| 2026-10-15 | 13D — validation multi-postes | Mac mini macOS confirmé opérationnel à partir des essais du 14/10 ; MacBook testé le 15/10. GO AVEC RÉSERVES sur 13D, sans retester ni toucher aux accès serveur | Confirmation utilisateur du 15/10 ; échanges de validation Launcher/Mac mini du 14/10 |
| 2026-10-15 | Consolidation 05D, 06, 07, 12, 13A, 13B, 13C, 13E | Mise à jour de l'état technique grâce aux preuves de 13F ; verdicts historiques et réserves non couvertes préservés ; 08–11 toujours à confirmer | [Débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md) · [Rapports PR n°4](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/4) |
| 2026-10-15 | 13D | Deux méthodes SSH, alias, sessions tmux et reprise testés depuis MacBook ; mission globale laissée ouverte | Résultats de commandes et confirmation utilisateur dans la conversation 13D |
| 2026-10-14 | 13F | GO AVEC RÉSERVES ; débrief archivé | [Débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md) et rapports PR n°4 |
| 2026-10-14 | 15A / 15B | Missions séparées, cahiers préparés ; iOS gratuit retenu | [Roadmap](ROADMAP.md) |
| 2026-10-14 | Pilotage | Priorité 13D → 14A → 14 ; Launcher en chantier parallèle | [Roadmap](ROADMAP.md) |



## Jalon du 17 octobre 2026 — clôture de tentative Dell

Debian démarre ; SSH répond, mais authentification, rapport de premier boot et Ansible non réceptionnés. Tentative clôturée sur demande ; mission complémentaire à lancer pour finir, avec conservation du RAID si possible. Référence prioritaire : [rapport transitoire](docs/missions/13D-E/RAPPORT-TRANSITOIRE-REPRISE.md).


## Mission 13D-E / 14 relancée — 17 octobre 2026

Nouvelle chaîne supervisée préparée, services PXE actifs et email de lancement envoyé. Installation physique de cette tentative non encore validée. Voir [réinstallation supervisée](docs/missions/13D-E/REINSTALLATION-SUPERVISEE.md). Objectif continu incluant NVIDIA/CUDA/Ollama/modèles et intégration JARVIS ; aucun nouveau GO intermédiaire.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique incomplet, remplacé par la réception complète du 17/10 à 15 h 09 ; ne pas utiliser comme état courant.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique incomplet, remplacé par la réception complète du 17/10 à 15 h 09 ; ne pas utiliser comme état courant.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique incomplet, remplacé par la réception complète du 17/10 à 15 h 09 ; ne pas utiliser comme état courant.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique incomplet, remplacé par la réception complète du 17/10 à 15 h 09 ; ne pas utiliser comme état courant.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique incomplet, remplacé par la réception complète du 17/10 à 15 h 09 ; ne pas utiliser comme état courant.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

**Instantané historique incomplet, remplacé par la réception complète du 17/10 à 15 h 09 ; ne pas utiliser comme état courant.**

INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.


## Réception nouvelle tentative Dell 13D-E / 14

RÉCEPTION COMPLÈTE VALIDÉE. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.

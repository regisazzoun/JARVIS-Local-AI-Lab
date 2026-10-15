# JARVIS — SUIVI GLOBAL DES MISSIONS

**Dernière mise à jour : 15 octobre 2026**  
**Références :** [Feuille de route](ROADMAP.md) · [Chronologie](docs/chronologie.md) · [Débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md) · [Roadmap Launcher](docs/parallel-projects/JARVIS-Launcher/ROADMAP.md)

> **Tableau de pilotage permanent.** Conserver la présentation, l'ordre des colonnes, les intitulés, les identifiants de missions et les lignes historiques lors de chaque mise à jour. Modifier uniquement les informations nécessaires, ajouter une ligne si un nouveau jalon apparaît, dater et expliquer les changements dans le journal. Ne jamais déduire un GO de la seule existence de fichiers. Les étapes sans rapport complet restent « à confirmer ». Les statuts représentent la dernière information documentée, pas une surveillance temps réel.

## Vue d'ensemble — toutes les missions

| Mission | Objet / étapes | État | Résultat vérifié / réserves | Prochaine action |
| --- | --- | --- | --- | --- |
| **03** | Debian 13, démarrage, diagnostic, SSH du Mac mini | ✅ Réalisée avec réserves | Diagnostics et premières procédures documentés ; certains états intermédiaires historiques | Consolider les procédures et preuves |
| **04** | GRUB, Thunderbolt et eGPU NVIDIA | 🟡 Réalisée avec réserves | Investigations et contournements documentés ; essais de démarrage non concluants | Documenter les cas restant ouverts |
| **04W** | Analyse d'un démarrage interrompu | 🟡 Analyse réalisée | Entrée dans le noyau non prouvée sur les traces considérées | Conserver la réserve |
| **05A** | Sélection du pilote NVIDIA | ✅ Préparation réalisée | Choix de pilote documenté ; cette étape seule ne valide pas le fonctionnement | Se référer aux tests 05C/05D |
| **05B** | Installation contrôlée du pilote | 🟡 Réalisée avec réserves | Installation documentée ; vérifier les réserves DKMS du rapport | Consolider les preuves |
| **05C** | Détection eGPU et CUDA initial | ✅ Testée | Tests matériels et CUDA léger documentés | Référence 05D |
| **05D** | Calcul GPU, Ollama et Llama 3.1 8B | ✅ Validée sur Mac mini | Calcul CUDA et inférence GPU réels ; performance ponctuelle non généralisable | Maintenir la non-régression |
| **06** | Open WebUI et accès conversationnel | 🟡 Fonctionnelle avec réserves | Inférence fonctionnelle sur LAN ; HTTP local non chiffré dans le rapport historique | Préserver et sécuriser les accès |
| **07** | Qualité des réponses et RAG | 🟡 Tests réalisés | Optimisations testées ; résultats limités aux scénarios documentés | Étendre les tests si nécessaire |
| **08** | Mission historique 08 | ⚪ À confirmer | Présence de preuves insuffisante sans rapport de réception vérifié | Retrouver le rapport et statuer |
| **09 à 11** | Missions historiques intermédiaires | ⚪ Documentation à consolider | Aucun verdict individualisé établi dans les sources de suivi consultées | Réconcilier rapports et historique, sans inventer de statut |
| **12** | Étude voix et mémoire | ✅ GO sous conditions | Choix faster-whisper, Piper et SQLite/FTS5 ; essais préliminaires sur fichiers/fictifs | Historique conservé ; voir 13A–13F |
| **13A** | Socle vocal durable Whisper/Piper | ✅ Réussie dans son périmètre | Installation et tests sur fichiers ; micro physique exclu du périmètre initial | Compléments via 13E/13F |
| **13B** | Interface vocale, Push-to-Talk | 🟡 GO PARTIEL | Interface et backend livrés ; validations physiques initialement incomplètes | Voir essais complémentaires 13E/13F |
| **13C** | Mémoire persistante partagée | 🟡 GO PARTIEL | SQLite/FTS5, sauvegarde, validation des souvenirs ; premiers tests multi-modèles partiels | Compléments réels documentés en 13F |
| **13D.1** | MacBook : Tailscale, SSH par clé et par mot de passe | ✅ Validée le 15/10 | Connexion SSH par les deux méthodes testée ; clé publique ajoutée sans retirer les accès existants | Préserver **les deux méthodes** d'accès |
| **13D.2** | MacBook : alias `ssh jarvis`, reconnexion et tmux | ✅ Validée le 15/10 | Alias SSH fonctionnel ; sessions existantes préservées ; création, détachement et reprise de `jarvis-test` réussis | Réutiliser les accès dans Launcher |
| **13D.3** | Contrôles globaux SSH/Tailscale, secours et sécurité multi-postes | 🔄 En cours | Volet MacBook validé ; pas de validation complète de tous les postes ni d'un redémarrage serveur | Vérifier les autres postes, secours et journalisation sans verrouillage |
| **13D** | Sécurisation des accès distants (mission globale) | 🔄 EN COURS — GO MacBook | SSH mot de passe **et** clés maintenus. Ne pas changer `sshd_config` ni retirer un mode d'accès avant validation explicite | Terminer 13D.3 puis prononcer GO global |
| **13E** | Intégration vocale réelle | 🟡 Réalisations antérieures rapportées, réception à consolider | Confirmation humaine antérieure mentionnée dans 13F ; statut officiel ancien de la roadmap « à préparer » devenu historique | Retrouver rapport de réception 13E et distinguer ses preuves de 13F |
| **13F** | Conversation, mémoire v3 et outils agentiques | ✅ **GO AVEC RÉSERVES** | 27 tests backend, 8 API, 8 navigateur et 6 finaux ; autonomie Qwen prouvée dans laboratoire isolé, non sur Dell | Suivre réserves voix physique, reboot et opérations longues ; [débrief](docs/missions/MISSION-13F-DEBRIEF.md) |
| **14A** | Validation aptitude agentique avant Dell | ⏳ À lancer après 13D | 13F prouve des réparations HTTP simples, pas un déploiement intégral | Définir essais et GO/NO-GO |
| **14** | Déploiement autonome supervisé du Dell Precision | ⏳ En attente | Préparation PXE, RAID1 NVMe, GPU et Ansible documentée ; aucune installation Dell validée | Après 13D/14A : inventaire, essais VM et autorisation ciblée |
| **15A** | Application native SwiftUI macOS | 📋 Préparée, non lancée | [Cahier Codex](docs/missions/MISSION-15A-MACOS-CODEX.md) disponible | Inventaire API 13F, contrat commun, développement |
| **15B** | Application native SwiftUI iOS | 📋 Préparée, non lancée | [Cahier Codex](docs/missions/MISSION-15B-IOS-CODEX.md) ; installation gratuite Xcode/Personal Team retenue | Contrat API commun et prototype iPhone |
| **JL-01** | Launcher macOS : SSH, Terminal, Codex, tmux | 🔄 Tests / réception à consolider | Launcher local et ouverture SSH/tmux signalés fonctionnels sur Mac mini ; état MacBook à vérifier. Roadmap JL historique non encore synchronisée | Tester le profil MacBook, les actions autorisées et consigner les preuves |
| **JL-02** | Launcher : Qwen/Ollama, voix, authentification | ⏳ Prévue, non lancée | Sécurité 13D, identité, secrets, permissions, déconnexion et révocation requis | Auditer JL-01, valider sécurité, cadrer l'intégration |
| **Documentation** | Rapports, roadmap, gouvernance | 🔄 En continu | Synthèse, débrief 13F et cahiers 15A/15B présents | Synchroniser `SUIVI.md` après chaque changement d'état |

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
| Intégration Launcher sur MacBook | ⏳ À vérifier | Tester les profils et actions depuis le MacBook |
| Mot de passe SSH en secours | 🔒 Maintenu | Ne **pas** désactiver avant décision distincte et accès de secours éprouvé |
| Validation globale 13D | 🔄 En cours | Autres postes, scénarios de secours et journalisation non tous réceptionnés |

## Priorités et règles permanentes

**Séquence stratégique actuelle :** 13D → 14A → 14. Missions 15A/15B techniquement parallèles, mais priorité moindre à ce stade. Launcher suit son propre chantier, avec la sécurité 13D comme dépendance pour les accès distants et JL-02.

**Protection des accès :** garder SSH par **clé et mot de passe** sur le serveur jusqu'à décision explicite après validation ; ne pas modifier automatiquement le serveur à partir du constat positif côté MacBook.

**Format immuable :** chaque future modification doit conserver les deux tableaux, leurs colonnes et séparateurs Markdown, leurs emoji de statut, les sections et les lignes historiques. Toute nouvelle mission reçoit une nouvelle ligne ; aucune mission ne doit disparaître sans entrée d'historique explicite. Ne pas réorganiser le fichier au gré des mises à jour.

**Légende :** ✅ validée ou réalisée selon périmètre décrit ; 🟡 partielle / réserves / réception incomplète ; 🔄 en cours ; 📋 préparée ; ⏳ en attente ; ⚪ preuve à confirmer ; 🔒 protection maintenue.

## Journal des mises à jour

| Date | Mission | Modification | Source / preuve |
| --- | --- | --- | --- |
| 2026-10-15 | 13D | Deux méthodes SSH, alias, sessions tmux et reprise testés depuis MacBook ; mission globale laissée ouverte | Résultats de commandes et confirmation utilisateur dans la conversation 13D |
| 2026-10-14 | 13F | GO AVEC RÉSERVES ; débrief archivé | [Débrief 13F](docs/missions/MISSION-13F-DEBRIEF.md) et rapports PR n°4 |
| 2026-10-14 | 15A / 15B | Missions séparées, cahiers préparés ; iOS gratuit retenu | [Roadmap](ROADMAP.md) |
| 2026-10-14 | Pilotage | Priorité 13D → 14A → 14 ; Launcher en chantier parallèle | [Roadmap](ROADMAP.md) |

# JARVIS — Débrief de pilotage de la mission 13F

**Date :** 14 octobre 2026  
**Plateforme :** Mac mini 2018 — Debian 13 T2Linux  
**Décision de réception :** **GO AVEC RÉSERVES**  
**Nature :** synthèse de pilotage, complémentaire aux rapports techniques et aux preuves de [la PR n°4](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/4).

> Ce document distingue fonctionnalités livrées, tests réels, simulations et points non validés. La réception de la 13F ne vaut pas preuve d'autonomie de déploiement du Dell Precision. Les preuves brutes et données privées demeurent locales.

## 1. Résumé exécutif

La mission 13F constitue une évolution structurante : JARVIS passe d'un assistant conversationnel doté d'une voix et d'une mémoire à un **premier agent technique capable de diagnostiquer une panne, choisir des outils, appliquer une correction en laboratoire isolé, puis vérifier le résultat**. L'autonomie est réelle mais limitée au périmètre de tests autorisé.

Les services Ollama/Open WebUI existants, les données SQLite et les modèles ont été préservés. Les réserves n'empêchent pas les travaux clients macOS (15A) et iOS (15B), mais imposent des préparatifs spécifiques pour la mission 14 (Dell).

## 2. Résultats vérifiés

| Domaine | Résultat | Portée / nuance |
| --- | --- | --- |
| Tests backend | **27/27** réussis | Tests unitaires et backend |
| API réelle | **8 contrôles** réussis | Authentification, mémoire, moteurs, audio, sauvegarde/reprise |
| Navigateur | **8 contrôles** réussis | Chromium ; microphone artificiel et au moins un contrôle algorithmique simulé |
| Vérifications finales | **6 contrôles** réussis | Préférences, rappels et diagnostics |
| Conversation / modèles | **Fonctionnel** | Inférences retestées sur trois modèles |
| Voix Whisper → Ollama → Piper | **Fonctionnelle dans les essais documentés** | Bruit, écho et périphériques physiques non testés dans la 13F |
| Mémoire SQLite/FTS5 v3 | **Validée pour les scénarios testés** | Transactions, dédoublonnage, correction, suppression, persistance |
| Réponses écrites/orales différenciées | **Testées** | Synthèse orale adaptée, avec préférence persistante |
| Détection de silence et interruption | **Prototype testé sous navigateur** | VAD heuristique ; interruption expérimentale, désactivée par défaut |
| Agent autonome de réparation | **Démontré en laboratoire isolé** | Pannes HTTP et configuration simples, pas déploiement système |
| PXE / RAID / installation Dell | **Non testés** | Hors périmètre 13F |

### Performance vocale constatée

| Étape | Durée mesurée |
| --- | ---: |
| STT / Whisper | 4,07 s |
| Génération | 1,95 s |
| Synthèse Piper | 2,16 s |
| **Total** | **8,17 s** |

Audio généré : 3,36 s. Réponse écrite : 4 239 caractères ; réponse orale : 259 caractères. Ces valeurs proviennent d'un essai documenté et **ne constituent pas un SLA ni une moyenne générale**. La latence reste un objectif d'amélioration pour une conversation plus naturelle.

## 3. Trois avancées majeures

### 3.1 Conversation et voix

- Capture audio via AudioWorklet ; pré-enregistrement, arrêt sur silence et échanges successifs.
- Push-to-Talk et arrêt manuel conservés.
- Réponse écrite complète et champ `spoken_answer` distinct, avec reformulation vocale des contenus longs.
- Choix de longueur de la réponse orale, préférence conservée et demande ponctuelle de davantage de détails.
- Validation acoustique physique, Safari et iPhone à faire dans les missions clientes.

### 3.2 Mémoire persistante

- Passage au schéma SQLite v3, historique des préférences et souvenirs canoniques.
- Transactions atomiques, dédoublonnage, remplacement et suppression cohérente avec FTS5.
- Catalogue limité de préférences non sensibles mémorisables automatiquement ; les autres souvenirs restent soumis à proposition/validation.
- Rappel réel des préférences par Qwen, Ministral et Llama ; préservation vérifiée de 2 conversations, 14 messages et 1 souvenir initiaux.
- Restauration sur base neuve et contrôles d'intégrité réussis.

### 3.3 Agent technique autonome : première démonstration

Dans un laboratoire **Bubblewrap** isolé, Qwen a :
1. Observé une panne de configuration/HTTP sur une fixture contrôlée.
2. Utilisé ses outils pour inspecter, rechercher et consulter des documents techniques.
3. Choisi une stratégie de modification et de sauvegarde.
4. Constaté puis corrigé une erreur de sauvegarde récursive et un problème de répertoire de travail.
5. Vérifié le service via une sonde HTTP réelle (`HTTP 200` et `HEALTH_OK`).
6. Rendu un rapport d'intervention.

**Essai final documenté :** 17 appels d'outils et 125,51 s. Deux documents distincts ont été consultés sur le site officiel Python ; il ne s'agit pas de deux éditeurs indépendants. Codex a créé les fixtures et le dispositif de test, mais n'a pas effectué les corrections à la place du modèle.

**Limite essentielle :** des sorties textuelles du modèle ont déjà attribué à tort des consultations ou mal nommé des exceptions. Les preuves d'outils, contrôles et traces priment sur ses déclarations.

## 4. Préservation et sécurité

- Isolation avec Bubblewrap : `/usr` en lecture seule, seul espace `/work` modifiable, pas d'accès aux fichiers personnels, pas de sudo et pas de réseau hôte.
- Limites de durée, mémoire, CPU et volume de travail.
- Sauvegarde et restauration réelles, timer systemd de sauvegarde activé.
- Redémarrage du service, reconnexion, préférences et historique revérifiés.
- Pas de modification déclarée du noyau, des pilotes, des modèles existants ni des accès distants.
- **Reboot complet de la machine non réalisé.**

## 5. Réserves et niveau de priorité

| Réserve | Priorité de suivi | Chantier concerné |
| --- | --- | --- |
| Microphone, haut-parleurs, bruit et écho réels | Moyenne | 15A / 15B |
| Safari, iPhone et utilisation sur vrai macOS | Moyenne | 15A / 15B |
| VAD heuristique et interruption vocale expérimentale | Moyenne | 15A / 15B |
| Mémoire automatique limitée à un catalogue | Faible | Évolutions mémoire |
| Explications du modèle parfois approximatives | Moyenne | Outils / audits |
| Reboot global et persistance système complète | Moyenne | Exploitation |
| Outils PXE/RAID/firmware et permissions Dell | Élevée | Mission 14 |
| Contrôleur de mission longue avec reprise après reboot | Élevée | Mission 14 |

Les niveaux de priorité ci-dessus sont des **arbitrages de pilotage**, pas des classements issus d'une mesure de risque formelle.

## 6. Conséquences sur la feuille de route

### Mission 15A — Application macOS

**Démarrage possible.** Réutiliser les API et capacités existantes (conversation, mémoire, audio) en les vérifiant avant intégration. Tester sur matériel macOS réel, sans supposer que les essais Chromium du backend valent validation de l'application native.

### Mission 15B — Application iOS

**Démarrage possible en parallèle de 15A.** Construire sur le même contrat API. Conserver la décision d'installation initialement **gratuite par Xcode / Personal Team**, avec limites iOS, signature périodique et permissions microphone. La mission 14 n'est pas bloquante.

### Mission 14 — Dell Precision 5820

**Préparation spécifique nécessaire.** Les essais 13F ne démontrent ni déploiement PXE ni installation RAID/NVIDIA autonome. Avant la première intervention physique : périmètre d'autorisation, transport et exécution bornés, PXE/Ansible, VM UEFI et snapshots, identification stable des deux SSD NVMe, plan de récupération et contrôleur de mission résistant aux redémarrages.

## 7. Verdict de pilotage

**GO AVEC RÉSERVES justifié.**

- Infrastructure assez stable pour poursuivre les prototypes clients.
- Voix et mémoire opérationnelles dans le périmètre réellement testé.
- Autonomie agentique démontrée pour une catégorie limitée d'incidents en laboratoire.
- Garde-fous et préservation des données vérifiés.
- **Objectif d'administration autonome complète d'un second serveur : non atteint, à construire dans la mission 14.**

**Décision recommandée :** poursuivre **15A macOS et 15B iOS en parallèle**, avec priorité au contrat API partagé et à la validation physique. Préparer la 14 en chantier indépendant.

## 8. Traçabilité

Rapports techniques et tests détaillés visibles dans [PR n°4 — mission 13F](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/4), notamment :

- `rapports/MISSION-13F-RAPPORT.md`
- `rapports/MISSION-13F-TESTS.md`
- `rapports/MISSION-13F-INCIDENTS.md`

**Ne pas publier** les données de mémoire, journaux bruts, identifiants, inventaires réseau, sauvegardes ou empreintes permettant d'exposer des secrets. Ce document est une synthèse et ne remplace pas les preuves techniques.

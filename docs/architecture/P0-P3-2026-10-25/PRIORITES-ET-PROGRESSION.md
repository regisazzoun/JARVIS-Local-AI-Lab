# JARVIS — Architecture et nouvelles priorités P0.1 à P3.2

**Décision propriétaire du 25 octobre 2026.** Ces priorités **s'ajoutent** aux missions initialement prévues ; elles ne les remplacent pas, ne changent pas leurs numéros, ne rouvrent pas leurs réceptions et ne déclenchent pas ici leur exécution. Référentiel : `AGENTS.md`, `docs/CHARTE_DIRECTIVES_JARVIS.md`, états de 26, 28A, 14B, JL03-COR-P1, 11B, 00. L'état GitHub de certaines branches est plus récent que le `SUIVI.md` de main.

## Convention
✅ validé · ✅🟡 fonctionnel avec réserves · 🟡 en cours / non démontré · 📋 prévu · ❌ échec avéré. Chaque état indique **la fonction** et son périmètre, pas automatiquement le GO global de la mission. Aucun ❌ sans essai échoué.

## Registre additif des nouvelles priorités

| ID | Niveau | Problème et action attendue | Statut au 25/10 | Missions associées | Dépendance / sortie attendue |
|---|---|---|---|---|---|
| P0.1 | Critique | Contextes excessifs, réitérations improductives ; lots courts envoyés **un par un** de Codex à JARVIS puis délégation aux workers ; règle 3 itérations sans progrès, analyse et escalade Codex | 🟡 | 26 ✅🟡 ; 26B 🟡 clôturée incomplète ; JL03-COR-P1 🟡 | Reprendre D01/D02 au dernier checkpoint ; aucun quatrième essai identique |
| P0.2 | Critique | Réconcilier actions réelles, reçus, preuves sémantiques, acteurs et rapports ; ne pas transformer code 0 ou completed en validation | ✅🟡 | 26 ✅🟡 ; 28A 🟡 clôturée incomplète ; JL03-COR-P1 🟡 | Rapport factuel sourcé par des preuves réellement relues |
| P1.1 | Haute | Matrice applicative symétrique Dell1/Dell2 (OS, réseau, CUDA, Ollama, modèles, workers, conteneurs, supervision) avec statut par couche | 🟡 | 14B 📋 dans sa fiche du 24/10 ; JL03-COR-P1 🟡 ; 13D-E ✅ Dell1 | Inventaire consolidé sans réinstaller, distinguer confirmation propriétaire du test hôte |
| P1.2 | Haute | Caractériser sens, protocole, couche, statut et preuve des liaisons Mac-Dell1, Mac-Dell2 et inter-Dell | ✅🟡 | 11B ✅🟡 ; 28A ✅ pour liaison Mac-Dell1 ; JL03-COR-P1 ✅🟡 | Distinguer exécution distante, inférence API, SSH/Ansible, métriques et liens physiques |
| P1.3 | Haute | Établir présence et usage réels Ollama/CUDA/modèles sur Dell2 ; profil 28A n'atteste pas l'activation | 📋 | 14B (préparation) ; 28A (Dell2 désactivé) | Preuve de démarrage, modèle, requêtes réelles et GPU ; aucune sélection de modèle imposée |
| P2.1 | Moyenne | Documenter séparément distribution de tâches sur les deux Dell et équilibrage des **inférences** IA ; ne pas les confondre | ✅🟡 tâches / 📋 inférence Dell2 | 28A ; JL03-COR-P1 ; 14B | Adressage et admission réelle des nœuds sans modifier les acquis Mac/Dell1 |
| P2.2 | Moyenne | Faire remonter et afficher CPU + **deux GPU Dell2** (D17) ; mesurer les données observées, pas des valeurs simulées | 🟡 | JL03-COR-P1 D17 non transmis | Affichage JL03 associé à sondes prouvées et statut de connectivité |
| P2.3 | Moyenne | Réception des défauts JL03 : D01 répétitions vocales, D02 Whisper, D03 commandes sans réponse visible, D04 réponse trop administrative, D17 CPU/GPU | 🟡 | JL03-COR-P1 ; JL-03 / 27 | Tests ciblés par défaut, voix réelle si pertinente, visibilité des preuves |
| P3.1 | Documentation | Quatre inventaires liés par IDs et diagramme à couches empilées, flèches orientées et statuts homogènes | 🟡 | 00 ; présente branche d'architecture | V2 après levée des écarts, sans falsifier les rapports anciens |
| P3.2 | Évolution | Ajouter à la répartition 28A l'inférence Dell2 **si et seulement si** son moteur est prouvé actif ; critères d'admission/repli | 📋 | 14B ; 28A clôturée incomplète | Test ciblé Mac/Dell1/Dell2, pas de nouveau screening des modèles reçus |

## Ordre d'exécution proposé (complément des missions prévues)

1. **Parallèle A : P0.1 + P0.2.** Corriger l'agentique et le suivi sémantique sur les tâches existantes. Chaque tâche est envoyée isolément ; JARVIS pilote ses exécutants, Codex traite les blocages. Ne pas réinitialiser le garde trois boucles.
2. **Parallèle B : P1.1 + P1.2.** Réconcilier les inventaires Dell1/Dell2 et le graphe des liaisons à partir des preuves GitHub puis des observations réelles disponibles. Compatible avec le chantier A.
3. **P1.3, après B.** Qualifier les installations IA Dell2 ; si absent, la fonction est simplement non installée, sans remettre en cause l'exécution distante déjà acquise.
4. **P2.3 + P2.2.** Terminer les correctifs JL03-COR-P1, dont D17. La correction du contexte P0.1 précède les nouveaux cycles agentiques longs.
5. **P2.1 puis P3.2.** Vérifier l'attribution des tâches ; étendre le routeur d'inférence seulement après preuves P1.3, avec essais de disponibilité/repli ciblés. Conserver modèle conversation Mac27B et mission Dell1 80B.
6. **P3.1.** Consolider les tableaux et régénérer le diagramme complet avec preuves nouvelles et version datée.

Ce plan est une **progression**, pas le lancement des missions. Les missions 23–31, 14B et JL03 existantes demeurent au registre ; elles gagnent des priorités transversales. Le dossier ne doit pas provoquer de réinstallation ni de validation humaine intermédiaire inventée après le lancement d'une mission autorisée.

## Points de concordance à préserver

- **28A (24/10)** : Mac mini Qwen3.5 27B conversation, Dell1 Qwen3-Coder-Next 80B MoE pour missions, deux RTX3090 réellement sollicitées ; deux slots de mission mais sérialisation GPU ; repli de conversation testé sur configuration de copie ; Dell2 non enrôlé en inférence dans cette mission.
- **JL03-COR-P1 (25/10)** : `host_remote/project_exec` avec Node.js/Bubblewrap sur **les deux Dell**, répertoires de tâches isolés. Ceci atteste une capacité d'exécution distante, pas un deuxième serveur Ollama actif.
- **14B (24/10)** : préparation dédiée Dell2 indiquée non lancée dans ce document. Le propriétaire indique ensuite Dell2 déployé ; enregistrer cette confirmation et rechercher les preuves techniques récentes, sans déduire silencieusement OS/GPUs/modèles/RAID.
- **D01 / D02** : corrections non réceptionnées ; D03, D04 et D17 non transmises à la date du registre consulté.
- Objectif **10 Gb/s** interserveurs communiqué par le propriétaire ; vitesse négociée par carte, liens physiques inter-Dell et topologie précise non établis dans cette réception documentaire.
- **Symétrie documentaire ≠ identité applicative** : même matrice de champs pour Dell1/Dell2, états éventuellement différents.

## Inventaires et diagrammes

- [Matériels](inventaire_materiels.csv)
- [Liaisons](inventaire_liaisons.csv)
- [Applications](inventaire_applications.csv)
- [Fonctionnalités](inventaire_fonctionnalites.csv)
- [Diagramme source Mermaid](diagramme-architecture.md)
- [Diagramme SVG](diagramme-architecture.svg)

Les quatre CSV proviennent de l'inventaire V1 réalisé en conversation, transféré avec reformulations mineures. L'archive ZIP originale et son PDF restent des livrables de conversation et ne doivent pas être confondus avec un binaire déjà publié dans ce dossier GitHub.

## Sources primaires (branches)

- `main:AGENTS.md`, `main:docs/CHARTE_DIRECTIVES_JARVIS.md`
- `codex/mission-28a-routage-modeles:docs/missions/28A/RAPPORT-FINAL.md`
- `codex/mission-26-mission-engine:docs/missions/26/RAPPORT-FINAL.md`
- `docs/mission-14b-dell2-20261024:docs/missions/14B/MISSION.md`
- `codex/jl03-cor-p1:docs/missions/JL03-COR-P1/ETAT-DEMARRAGE.md` et `REGISTRE.json`
- `main:docs/missions/00-Mission-Pilotage-point-26-10-17/RAPPORT-FINAL.md`

**Publication :** branche documentaire dédiée ; aucun changement de l'état des missions de `main`. Lors de l'intégration ultérieure : appliquer la synchronisation obligatoire `ROADMAP.md ↔ SUIVI.md`, en conservant sections, colonnes et historique.

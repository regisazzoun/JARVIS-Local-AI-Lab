# Planification réellement observée

Objectif brut et critères utilisateur : [OBJECTIF-BRUT.json](OBJECTIF-BRUT.json). Aucune liste de tâches fournie à la soumission. Exécution `28c3fdf877ba47718dfc55e46f386656`, modèle `qwen3.5:27b-q4_K_M` sur la route Dell1 existante.

Les [versions intégrales](PLANS-JARVIS.json) sont exportées depuis `mission_plans`, avec auteur, raison, horodatage et SHA256. Elles sont produites par les appels inférés de JARVIS à `mission_plan` ; Codex ne rédige pas leurs tâches.

| Version | Auteur | Tâches | Raison |
| --- | --- | --- | --- |
| 1 | JARVIS | 1 | initial plan |
| 2 | JARVIS | 3 | Ajout des tâches t02 (utilisation skill config-repair sur fichier lab) et t03 (rapport final) requises par coordination pour démontrer réparation réutilisable |
| 3 | JARVIS | 3 | Correction du contrat sémantique pour t03-rapport-final : remplacement de expected:{} par sha256 vérifié (11f61d4c...) pour type 'text', conformément aux exigences de mission_verify |

La première version est trop étroite : une correction ponctuelle, sans couvrir correctement la compétence réutilisable. Codex rappelle ce livrable manquant au niveau de l'objectif, sans fournir de tâches. JARVIS propose ensuite ses étapes et dépendances ; l'API append développée par Codex lui évite de recopier les tâches reçues. Ce guidage empêche de qualifier le scénario de planification complexe entièrement sans assistance.

13 propositions de plan refusées sont conservées dans [PREUVES-JARVIS](PREUVES-JARVIS.json) : type tableau/chaîne, ancien format checks, critères propriétaire absents, métadonnées, confusion version courante/suivante, contrôle inexécutable et tentative de changer une tâche reçue. Un refus n'incrémente jamais la version.

La version2 conserve exactement la première tâche et ajoute des dépendances. Le contrôle de texte inexécutable accepté par une version intermédiaire du moteur exige une réparation explicite par JARVIS ; le correctif infrastructure Codex le détecte désormais avant sauvegarde et permet de réparer une ancienne déclaration invalide sans affaiblir un critère valide.

L'objectif, les propositions échouées et les corrections d'interface restent visibles : il s'agit d'une progression réelle de planification et de reprise, avec réserves de qualité et d'ergonomie observées, pas d'un graphe Codex présenté comme autonome.

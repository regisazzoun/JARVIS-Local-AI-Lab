# Méthodologie des expériences

1. Définir l'objectif de faisabilité.
2. Noter le matériel et les versions **observés**, et distinguer l'état réel du projet.
3. Séparer les commandes exécutées de celles seulement proposées.
4. Conserver les preuves en espace privé ; citer leur nature dans le compte rendu public.
5. Qualifier le résultat : **validé**, **partiel**, **non concluant** ou **non testé**.
6. Décrire les contournements et leur périmètre de validité.
7. Continuer vers l'objectif principal sans sur-investiguer les anomalies secondaires non bloquantes.

Une mesure isolée n'est pas un benchmark global. Une configuration prévue n'est pas une installation réussie.

## Prérequis avant toute implémentation

Avant l'étape 1, lire [AGENTS](../AGENTS.md), la [charte](CHARTE_DIRECTIVES_JARVIS.md) et les états pertinents. Avant tout code nouveau, appliquer les [prérequis permanents de réutilisation](PREREQUIS-REUTILISATION.md) : inventaire du code/capacités JARVIS et recherche/comparaison de bibliothèques, API, connecteurs MCP et solutions open source. Réutiliser, configurer, raccorder et tester d'abord ; développer seulement le manque démontré, avec fiche et preuves dans le dossier de mission et la PR. Cette étape s'exécute dans l'autorisation existante, sans ajouter de validation humaine intermédiaire.

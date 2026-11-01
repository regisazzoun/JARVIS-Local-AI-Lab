# Cluster Jarvis

**Statut : piste d'étude — mise en œuvre différée.**

## Objectif
Étudier l'extension de JARVIS à une infrastructure IA locale pour un lycée d'environ 1 200 élèves et 130 à 140 personnels, avec comptes individuels, préférences, historiques et connecteurs aux ressources pédagogiques.

## Hypothèse préliminaire (non validée)
- Cluster de 3 à 4 stations Dell Precision 5820, en conservant les deux machines existantes si elles sont réparées et adaptées.
- Hypothèse cible : 256 Go de RAM par station, jusqu'à deux RTX 3090 par station **sous réserve de compatibilité électrique, mécanique et thermique**.
- Estimation exploratoire d'extension : 8 000 à 15 000 € ; **ni devis ni capacité garantie**.
- Dimensionnement à établir à partir de la simultanéité effective, du débit de génération en tokens/s, de la longueur des contextes, de la latence et des modèles retenus.

## Évolutions structurelles à étudier
1. Séparer comptes, authentification, profils, mémoire, connecteurs et stockage du service d'inférence.
2. Placer un routeur de requêtes devant plusieurs instances de modèles ; orienter tâches courantes et tâches complexes vers des ressources distinctes.
3. Organiser la file d'attente, les quotas par utilisateur et les priorités pédagogiques.
4. Prévoir supervision, gestion des pannes, sauvegardes, sécurité et protection des données des élèves.
5. Comparer la répartition de requêtes entre serveurs et l'exécution répartie d'un même modèle (non équivalentes).
6. Tester les performances et la montée en charge avant tout engagement pour l'ensemble du lycée.

Aucun déploiement ni modification de l'architecture JARVIS existante n'est engagé par ce dossier.

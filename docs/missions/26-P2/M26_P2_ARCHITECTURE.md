# Architecture — état initial

NON VALIDÉ — conception P2 confiée à Qwen80B. Le moteur, MissionStore, broker et SSH existants sont réutilisés ; aucune seconde base de missions ni nouveau moteur d’inférence.

Bootstrap Codex : paramétrisation du workspace autorisé et des identifiants d’exigence des outils Phase1. Valeurs Phase1 conservées par défaut ;35 tests de non-régression passent. Cette adaptation rend possible une priorité P2 sur le vrai code copié, sans choisir son correctif ni sa répartition à la place du modèle. Les sources candidates sont sur les deux Dell ; les services actifs ne reçoivent pas automatiquement ces changements.

P3 et P4 ne sont pas transmis. Leur architecture sera établie après réception de la priorité précédente.

# Tests des rapports26B — campagne en cours

Statut : 🟡 incomplet. Les 144 tests logiciels passent ; cela ne démontre pas à lui seul une correction autonome de la prose par JARVIS.

La réception attend trois rapports réels : réussite locale complète (A), échec du programme puis correction (B), résultat local vérifié avec dépendance externe impossible à observer (C). Aucun de ces trois rapports n’est encore reçu au déploiement16.

Les tentatives originales sont conservées dans narrative_review avec texte intégral, empreinte, preuves et verdicts par passage. Les FAIL et INSUFFICIENT historiques ne sont pas effacés. Les défauts de format du relecteur sont journalisés séparément ; ils ne prouvent pas que la prose du rédacteur était factuellement fausse.

Le test de B demande explicitement un premier brouillon au comptage faux « observations : 999 ». C’est une injection de test par Codex annoncée dans l’objectif, pas une erreur spontanée imputable au modèle. Il reste à constater son rejet et la rédaction corrigée dans l’exécution réelle. Le test complémentaire d’attribution, d’horodatage et de comptage n’a pas encore été exécuté : aucune détection de ces trois fautes ne peut être annoncée comme acquise.

Une revue positive du modèle ne remplace pas les contrôles indépendants : exactitude des JSON, empreintes du manifeste, exécution effective du producteur, conservation du banc et absence du témoin externe. Une réception partielle de rapport ne clôture pas une opération techniquement incomplète.

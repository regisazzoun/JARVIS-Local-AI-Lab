# Persistance réellement vérifiée

Les seuls composants redémarrés sont jarvis-host-bridge et jarvis-conversation. Une interruption explicite par l'API a précédé le redémarrage ; les appels déjà réussis, identifiants et rapports historiques restent en base. Les PID/InvocationID changent, le socket est recréé et le prévol répond avec la même politique. REDEMARRAGE.json conserve le checkpoint avant et l'état après ; cela ne repose pas sur le seul statut active.

JARVIS a réellement repris la même exécution, consulté le marqueur de redémarrage et réutilisé les outils ; les nouveaux appels JARVIS-runtime et leurs résultats sont corrélés dans PREUVES-JARVIS.json. Codex reçoit indépendamment politique/catalogue/service et processus Python hôte après redémarrage. Une nouvelle session HTTP authentifiée indépendante accède aux41 schémas exposés : NOUVELLE-SESSION.json. Aucune dépendance à un serveur temporaire de cette intervention.

CONTINUITE.json compare les bases courantes aux sauvegardes SQLite cohérentes : mêmes identifiants, treize tâches historiques23 et quatre du diagnostic inchangées, checkpoints/événements/appels historiques identiques, cinq souvenirs et quatre préférences inchangés. Tables FTS5 conservées et requête réelle possible ; quick_check des bases réussit. Aucun reset de mémoire ni replanification des tâches reçues. Ce test couvre les redémarrages de composants et nouvelles sessions, pas un reboot complet de l'hôte.

## Rapport final et fenêtre de crash

Le retest JARVIS a réellement sauvegardé7453 caractères avec intervention_report après le refus initial à6000. Une injection contrôlée a ensuite retiré uniquement le pointeur de clôture, en conservant le fichier, le reçu durable et toutes les validations. Après redémarrage réel de conversation et reprise du même identifiant, le moteur a rétabli completed depuis le reçu signé par l'empreinte de fichier : **zéro nouvelle inférence, zéro tâche réexécutée**. SYNTHESE-RECEPTION.json donne invocation, SHA256, événement de récupération et nouveaux PID/InvocationID. La simulation de perte de pointeur est explicitement attribuée à Codex ; elle n'est pas présentée comme une nouvelle panne spontanée.

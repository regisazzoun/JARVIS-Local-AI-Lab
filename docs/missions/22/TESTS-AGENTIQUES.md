# Tests — mission 22

État : réception réelle en cours, aucun succès global déclaré.

-16 tests V2 : dépendances, plan atomique, conservation après réouverture, reprise après plus de cinq cycles, intention sans résultat, priorité de l'interruption, session persistante et logout, rejet des preuves insuffisantes, assertion fonctionnelle et chronologie rapport/vérification.
-18 tests historiques13E/13F réussis sur les nouveaux modules : mémoire, outils, voix textuelle et frontières.
-12 contrôles du broker installé réussis : secrets masqués, refus des chemins/actions hors politique, garde cible et codes d'échec.
-Tests JavaScript existants de format et modèle de tâches réussis ; syntaxe app.js vérifiée.

Essai réel Qwen27B : calcul, échec volontaire, correction et relecture réellement exécutés via broker. Les premières itérations ont répété des opérations et ne sont pas reçues. Corrections apportées : persistance des échanges, contexte élargi et exclusion de l'écriture du rapport du contrôle chronologique portant sur le code. Les tests simulés valident ces mécanismes mais ne remplacent pas la réception réelle.

Interruption/reprise, clôture multitétapes, SSH/Ansible, publication vérifiée, affichage connecté et reprise21 restent à réceptionner. Les traces intégrales restent privées ; seules des preuves expurgées seront publiées.


## Premières réceptions réelles terminées

[Preuves de production](PREUVES-RECEPTION-PRODUCTION.json), [rapports rédigés par le modèle](reception/RAPPORT-AGENT-FINAL.md) et [manifestes de récupération GitHub](MANIFESTE-RAPPORTS-AGENT.json). Trois tâches validées,30 appels,27 retours réussis ; corrections Codex de publication identifiées. Cette réussite ciblée ne suffit pas à réceptionner les sept tâches21.

[Crash SIGKILL et reprise](INTERRUPTION-REPRISE.json) : tâche21.01 et son rapport conservés, empreinte identique ; systemd relance le serveur, worker reprend automatiquement en122,92s. Aucun changement manuel de l'état de tâche pour ce test. L'amélioration de récupération immédiate sous verrou exclusif est postérieure à cet essai et doit être distinguée de sa mesure.

[14 contrôles Chromium connectés](RECEPTION-NAVIGATEUR.json) : événements réels, acteur, géométrie et défilements sur trois dimensions. [Sessions après redémarrage](SESSION-RESTART.json) : même cookie encore valable. [Mémoire préservée](PRESERVATION-MEMOIRE.json) : toutes les lignes personnelles initiales intactes, seules des additions.

Réserve documentaire observée : un rapport modèle21.01 reprend une date historique et attribue à tort son pied de page à JARVIS-engine. Les journaux et manifestes font autorité sur l'auteur et les heures réels. L'horloge serveur et l'attribution explicite sont maintenant injectées dans le contexte ; la qualité sémantique des rapports reste à examiner séparément de leur présence.

# Incident de réception80B — historique conservé

> Décision propriétaire du24 octobre2026 : mission clôturée incomplète,80B conservé pour les missions Dell,27B conversationnel sur Mac. Les états «en cours» ci-dessous documentent les essais antérieurs ; leurs critères non reçus sont différés, sans relance automatique. Le RAPPORT-FINAL.md de clôture prévaut.

Le80B passe5/6cas courts et produit effectivement des appels d’outils ainsi que du code dans le moteur. Cela ne suffit pas à recevoir son autonomie sur une mission longue. La réception E a observé des lectures répétées, une confusion de chemins Mac/Dell, des paramètres project/action absents, un programme erroné et des comptes rendus inexacts. Les refus du backend ont évité des clôtures avec des preuves d’autres tâches.

## Défauts développés/corrigés par Codex

Les références de vérification pouvaient désigner un reçu enfant plutôt que son parent mission_verify ; le candidat de clôture et le contrôle sémantique de mission dirigée ont été corrigés. Les tailles de contexte variables rechargeaient le runner ; elles sont stabilisées. compute_status injectait les métriques sérialisées de nombreux anciens jobs ; seule sa vue modèle est désormais bornée, tous les reçus restent en base.

Une nouvelle tâche recevait aussi les derniers reçus et notes de tâches précédentes. Ce contexte encourageait la réutilisation d’identifiants périmés et des conclusions de clôture non applicables. Codex a isolé le ledger, les notes de travail et l’évaluation de progression au périmètre de la tâche active. Un test vérifie qu’une preuve et une conclusion d’une ancienne tâche ne réapparaissent pas dans son prompt, tout en restant accessibles dans SQLite.238tests logiciels passent. Le réemploi réel après déploiement reste la vérification opérationnelle, distincte de ce test.

## Coordination explicite

Codex a fourni des diagnostics et exemples des interfaces réellement installées. Il a isolé E_program comme prérequis court de E_reception dans le plan10, sans enlever aucun contrat initial ni modifier les étapes reçues. Cette décomposition est Codex, pas une planification autonome du modèle. Les interruptions techniques et archives de contexte n’effacent aucun reçu.

## Code et prose JARVIS

La première version consolider.py additionne11succès sur18pour chaque modèle. Le contrôle indépendant retourne FAIL4/4 malgré code0 et manifeste valide. Une version suivante sépare les cas par modèle mais ne reçoit pas automatiquement un PASS. Les copies versionnées sont conservées dans preuves/. Codex n’a pas écrit la correction du programme.

Le JSON d’audit parallèle contient les bons nombres, mais sa première prose invente une citation3échecs et prétend à tort que les cas individuels ne sont pas dans le JSON. Codex a rejeté cette restitution et transmis les contradictions à JARVIS. Le rapport initial reste JARVIS-AUDIT-v1-BRUT.md ; aucune rectification n’est considérée reçue avant relecture. Les réserves26B ne sont pas effacées par cet essai.

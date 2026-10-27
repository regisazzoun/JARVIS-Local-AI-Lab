# P4 candidat — capacité de lecture rétablie

27 octobre 2026, mission unique `d8fe752876db480cbe5f22cd5525e2dd`, même parent et MissionStore. Directives relues : AGENTS, charte, LANCEMENT-ATTESTATION, reprise, supervision, SUIVI et ROADMAP. Autorisation de toute P4 préservée sans nouvelle approbation humaine.

L’arrêt 60901/60902 suit trois appels à authority_read_execution indisponible : le spec retirait cet outil alors que le prompt système le recommandait toujours. Le retrait historique 59405 avait borné les relectures stériles ; il ne démontre aucune défaillance du stockage. Le candidat reste non terminé, tâche P4-ATTEST-01 non validée, plan version 2.

Correction de capacité limitée au spec de cette mission : réactivation du lecteur, context_recall restant désactivé. Vérification 60904 : lecture réelle du reçu complet 60682 avec contrôle SHA par Authority.read_execution, schéma à référence entière, outil désormais autorisé, objectif de contexte inchangé. Tous problèmes, compteurs authority/interface et opérations comparés avant/après : identiques. Sauvegarde et script privés conservés hors Git. Aucun code applicatif écrit, aucun reload nécessaire.

Dossier court 60905 transmis à Qwen : le refus d’édition 60887 précède toute exécution (path absent) ; le texte proposé, qui retourne seulement un attribut code_hash, ne résout pas le faux MATCH 60411. Dell2 existe : seul attest.py y était absent lors du contrôle précédent. Conception, fichiers, commandes, correction et tests restent à Qwen. Événement Codex-periodic 60907, contexte archivé puis reprise queued après changement technique vérifié.

technical_review_recorded reste false. Aucune continuation créée avant fin réelle et revue indépendante. Registre, allowed_tasks/allowed_mission_ids, script superviseur et compteurs inchangés ; aucun déploiement du candidat. Après conformité démontrée, seul prochain paquet P4 intégration/déploiement/validation réelle avec retour arrière vérifiable autorisé, même parent/moteur, ancienne entrée et compteurs conservés. Les huit situations et réception globale restent dues. Aucun rejeu P2/P3, autre mission, changement modèle/routage ou fusion main.

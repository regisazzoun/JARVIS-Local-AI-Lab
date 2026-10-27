# P4 — arrêt conservé au passage 3/3

27 octobre 2026. Directives relues : AGENTS, charte, SUIVI, ROADMAP, supervision, paquet d’attestation, reprise et événements ciblés. Toute P4 reste autorisée sans approbation humaine ; le candidat courant reste sans déploiement. Les restrictions historiques P2 du prompt de supervision ne révoquent pas cette autorisation.

Mission d8fe752876db480cbe5f22cd5525e2dd toujours interrupted, plan v2, tâche P4-ATTEST-01. Refus 61358 de la lecture répétée de 61212 ; escalade 61360, compteur d’interface 5. La commande n’a pas été réexécutée. Aucune fin réelle du candidat ni revue finale acquise.

Le reçu complet 61212 a été relu indépendamment avec vérification SHA : ses quatre lignes disent explicitement que get_object_code_hash et attestation_report sont absentes. Ce résultat décrit le candidat observé, pas une panne du lecteur. La source 60858 emploie inspect.getsource ; le contre-exemple 61056 (fonction chargée retournant 1, disque retournant 2, faux match) reste non résolu dans les preuves consultées. Les contrôles de cet arrêt ne constituent pas une nouvelle campagne sur les Dell.

Hypothèse d’infrastructure à vérifier : les deux derniers aperçus d’exécution conservés dans le checkpoint peuvent évincer le source utile ; le refus de lecture répétée ne restitue pas le contenu déjà reçu. Prochaine intervention distincte : régression ciblée de conservation du dernier contenu de lecture réussi, de sa référence et de sa fenêtre après inspections et refus, dans une véritable compaction. Corriger seulement si ce défaut est reproduit, sauvegarder/tester puis recharger les workers si nécessaire. Ne pas désactiver lecteur/garde ni réinitialiser les compteurs. Qwen conserve conception, diagnostic et correction de son application.

Aucune remise en file inchangée au troisième passage. Dossier 61363, checkpoint 61364, événement Codex-periodic 61365. Compteurs Authority/opérations/problèmes/refus comparés avant/après : identiques. Registre conservé avec technical_review_recorded=false ; configuration et script du superviseur inchangés. Aucun nouveau paquet ni sous-mission créé. P4 globale non validée.

Après correction attestée et fin réelle du candidat : revue indépendante, puis seulement si conforme, continuation P4 intégration/déploiement/scénarios avec retour arrière vérifiable dans le même moteur/parent. Huit situations et réception globale restent dues. Aucun nouveau GO humain requis.

Preuve structurée : [checkpoint](CHECKPOINT-LECTEUR-PASSAGE3.json).

# Reprise initiale TTS-01

Codex a relu AGENTS, charte, SUIVI/ROADMAP, architecture11, raccordement11B, réception13D-E, bilan14A de26 et rapports vocaux historiques13A/13F ; les rapports JL-02 et agentique, architecture et mécanismes de fichiers/missions/voix ont également été consultés. Les documents utiles13A/13F se trouvent sous historique ; aucun dossier courant14A n’a été trouvé. Les sources consultées ne constituent pas de nouvelles réceptions.

La mission persistante existait et avait accumulé40 versions de plan sans tâche validée. Des appels d’identité ont été refusés tant que la couverture n’était pas acceptée. Les contrats prenaient des titres pour le contenu intégral de rapports et un pointeur `/length` pour une longueur de tableau. JARVIS doit corriger ces contrats ; aucune installation ne découle d’un plan ni d’une note annonçant son acceptation.

Deux capacités manquaient réellement : terminal distant réservé au projet LiveKit, sans périphériques GPU ; archive de référence invisible depuis le confinement local malgré sa présence réelle. Codex a ajouté un périmètre TTS-01 au broker existant, avec garde d’identité inchangé, accès GPU et racine dédiée. L’archive est exposée en lecture seule. Le transfert binaire compare les SHA256 et la lecture WAV utilise l’API authentifiée de JL-02.

Les répétitions de l’historique de plus de40 plans dépassaient le budget de travail du modèle. Seule sa vue de travail est réduite : chaque version/auteur reste indexé, les définitions complètes restent consultables. Les contextes antérieurs sont archivés sans suppression de tâches ou de reçus. Une régression du comptage de versions dans cette vue a été détectée et corrigée ; le journal des essais est conservé.190 tests passent après correction, sans constituer une réception de TTS.

Le contrôle indépendant confirme la présence de l’archive et14 WAV valides plus14 métadonnées AppleDouble, non28 extraits. Le Dell est Debian13.7, noyau6.12.113, Python3.13.5 et RTX3090/24576MiB, pilote550.163.01. Une mesure initiale observe18960MiB de VRAM occupée : l’installation et les essais devront tenir compte de cette concurrence réelle.

La mission créée à partir de l’ancienne question conversationnelle sur l’exécution parallèle est interrompue comme clarification remplacée par le nouvel ordre. Son historique reste conservé ; elle ne doit pas déclencher une seconde installation TTS.26B est clôturée incomplète et ses trois scénarios restent interrompus.

## Mode de reprise retenu

La répétition des refus après réduction du contexte a conduit Codex à sélectionner, pour TTS-01 uniquement, le mode d’orchestration dirigée avec les barrières sémantiques de26 et une réception indépendante. Le contrôle automatique expérimental de couverture26B est désactivé dans la spécification de cette mission ; les contrôles de politique/identité et les vérifications sémantiques restent actifs. Le plan42 est une révision Codex des huit tâches initiales JARVIS, pas une preuve de planification autonome. Les versions1–41 restent intactes. Les rapports narratifs explicitement prévus restent soumis à leur propre vérification. Les commandes d’inventaire, les installations et les productions audio sont exécutées par JARVIS, puis contrôlées indépendamment.

Le premier test de transport CodeX a masqué l’absence du lien nvidia-smi dans le confinement par le succès de pwd ; ce premier résultat est conservé sans réception GPU. La liaison en lecture seule des alternatives Debian a corrigé le problème, puis le nouveau contrôle avec arrêt sur erreur a réellement observé la RTX3090. Le transfert WAV aller-retour est reçu sur empreinte ; ce fichier silencieux est une fixture d’outillage, jamais un échantillon TTS.

## Contrat de vérification corrigé et retest réel

Le contrat42 écrit par Codex utilisait project_exec comme lecture indépendante, alors que Verifier.read refusait ce mode. Le premier verdict INSUFFICIENT est donc un défaut du contrat Codex, et non une panne GPU ou un défaut d’habilitation. JARVIS a tenté une vérification d’un JSON local et obtenu PASS sur ce contenu, mais le moteur a correctement refusé de l’utiliser pour valider le contrat distant.

Codex a ajouté project_probe : quatre programmes fixes (gpu_inventory, archive_inventory, tts_runtime, script_syntax), sans code fourni par le modèle, avec racine de projet montée en lecture seule, garde d’identité et liste d’habilitations propres à TTS-01. Les contrats43 de Codex utilisent ces sondes ; le probe runtime teste aussi une somme effectivement calculée sur CUDA. La déclaration d’un project_exec comme observation indépendante est désormais refusée dès validation du contrat.193 tests logiciels passent.

JARVIS a réellement retesté gpu_inventory via mission_verify, obtenu PASS, puis appelé mission_task_complete avec la preuve dacf88a95753464fb0cd7cd523920f6e. T01 est validée dans le moteur ; T02 a commencé. Ce résultat reçoit l’utilisation de la nouvelle sonde, pas une planification autonome ni l’installation d’un TTS.

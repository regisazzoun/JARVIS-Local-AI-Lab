# Pilotage — finalisation mission23

| Étape | Instruction / résultat | Vérification / verdict |
|---|---|---|
|01 — reprise | Même mission originale, état waiting_external → queued/running ; onze validations conservées | Sauvegarde SQLite avant intervention, aucun reset |
|02 — GitHub initial | JARVIS réessaie push avec dossier racine, publie d99ce5e et relit le fichier | Codex confirme SHA distant ; capacité un fichier reçue, README fonctionnel refusé |
|03 — connecteur lots | Codex développe push_tree/verify_commit/verify_tree/PR idempotente | JARVIS publie0d7ac04 puis vérifie lui-même sa présence ; livraison4 fichiers insuffisante, source complète exigée |
|04 — question/mission | Défaut confirmé : /api/missions créait une mission pour toute question en mode agent ; promotion d'outil pouvait aussi créer une mission | Router corrigé, tests HTTP réels sans nouvelle mission ; état rendu depuis faits canoniques après réponses modèle contradictoires |
|05 — identité diagnostic | Métadonnées liées23, objectif/ID/preuves originaux conservés | Vraie24 mémoire non lancée ; affichage Launcher dérivé des métadonnées |
|06 — WebRTC initial | Codex génère WAV test et rejoint le serveur ; job dispatché à JARVIS | Échec confirmé dans Agent.__init__, aucune réception vocale |
|07 — preuve08-11 | JARVIS rédige addendum, mais invente des tests WAV inexistants dans test-livekit.py et reprend mauvaise cible Tailscale | Addendum refusé, instruction de correction explicite transmise ; version initiale conservée dans historique et événements |
|08 — client Dell | Codex fournit project_exec distant confiné sur profil Dell1 déjà autorisé, installe bubblewrap après absence constatée | Sonde Codex réussie, clésSSH absentes ; retest JARVIS encore à obtenir |

Les reçus intégraux et instructions horodatées sont dans mission_events et le journal broker privé. Publication ≠ réussite vocale ; contrôles programmatiques ≠ microphone physique.

Contrôle Codex supplémentaire : depuis le Dell1, dans project_exec confiné, HTTP sur le Tailscale du Mac mini actuel retourne `OK` (reçu broker a8a24c01f9694c60931ef988fa2f7ba8). Le refus historique vers l'ancien Mac ne justifie donc pas une modification aveugle de pare-feu. Le transport audio distant reste à démontrer par JARVIS.

Correction de contexte : les directives récentes du coordinateur sont épinglées dans la vue durable, afin qu'une compression n'en conserve pas seulement les anciennes conclusions du modèle. Les preuves canoniques restent intactes.

JARVIS a révisé le README et l'addendum après refus ; il reconnaît désormais l'absence de WAV dans le script historique et le caractère partiel du prototype. Une nouvelle correction ciblée a été demandée sur le pare-feu (HTTP actuel réussi par Codex), le flux LLM4491 (réel, pas seulement construction) et le job qui échoue sans arrêter le worker. Réception sémantique finale encore en cours.

Défaut réel supplémentaire : appel PR JARVIS5861 refusé par gh2.46, qui consulte le champ GraphQL projectCards retiré. Codex remplace création/édition par POST/PATCH REST et transmet une instruction de retest. La PR12 applicative existe déjà et doit être mise à jour, pas dupliquée. Contrat REST vérifié dans la [documentation officielle GitHub](https://docs.github.com/en/rest/pulls/pulls#update-a-pull-request).

Étape13 : JARVIS a commencé la correction du callback, mais a introduit deux API absentes (`livekit.api.Video`, `cli.server`), vérifiées indépendamment par Codex. Correction ciblée demandée : conserver le bootstrap AgentServer existant, corriger Agent/AgentSession et vérifier avant redémarrage. Ce défaut est classé programmation, pas permission manquante.

Lecture d'erreurs : reçu5920 tronqué. Le journal de projet retourne désormais les messages récents en premier et l'activation courante ; `history=true` conserve l'accès aux activations passées. La source inclut aussi UnitFileState pour distinguer service démarré et démarrage automatique configuré. Le contrôle Codex constate les deux services LiveKit encore disabled à ce jalon ; ils devront être activés par JARVIS après réception fonctionnelle.

Édition ciblée : après régressions dues aux réécritures complètes, Codex ajoute host_edit_file (préconditions exactes, empreinte optionnelle, écriture atomique, SHA avant/après). JARVIS l'utilise réellement aux événements6053/6056 pour corriger import et démarrage AgentSession, sans remplacer le reste du bootstrap. Contrôle postérieur encore requis ; le succès d'édition ne valide pas le son.

Lecture locale paginée : relectures longues STT/TTS6092/6128 constatées avec extrait de contexte, milieu absent. Le broker reçoit désormais offset/limit pour lire des pages de6000caractères, avec next_offset et empreinte de source ; la lecture intégrale des rapports reste inchangée pour réception. Tests UTF8/milieu/fin/empreinte et offset invalide ajoutés ; suite71 tests au déploiement. JARVIS doit utiliser les pages sur une lecture réelle.

Composants : nouveau vérificateur protégé exécute réellement STT sur la fixture française et impose un ChunkedStream TTS avec PCM non silencieux. JARVIS l'appelle en6155/6156 ; échec réel de cheminWhisper relatif interprété par HuggingFace. Correction de la valeur factory demandée, aucun nouveau modèle téléchargé par Codex.

Limite de raisonnement encore observée : après le diagnostic de chemin relatif, JARVIS modifie d'abord le bloc __main__ de démonstration de stt_adapter.py, pas la factory appelée par le vérificateur. Codex fournit une instruction d'édition exacte sur la valeur de factories.py, avec hash attendu. Cette correction guidée ne doit pas être présentée comme une découverte autonome.

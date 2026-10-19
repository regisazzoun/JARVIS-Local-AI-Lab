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

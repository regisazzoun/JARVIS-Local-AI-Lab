# Intervention Codex-periodic — fixtures et preuve de succès

P2 🟡 non reçue, mission native 3aa717f3887e49daa7daf7e883ee52e4 uniquement.

Lecture du dernier dossier43294 et des événements récents : SQL mission_events déjà corrigé, lecteur déjà réparé. Le reçu43353 créait un événement temporaire, sans changement de fichier : ce n'était pas la correction annoncée. Lecture actuelle Dell1, reçu e01dd2da4c1448818319e06b40f7e979, confirme les deux fixtures obsolètes et la validation limitée à l'existence de la référence.

Aide concrète Codex-periodic43362 : correction des deux fixtures positives avec événements tool_finished de la même mission issus d'un vrai sous-processus réussi en base temporaire ; assertions de persistance conservées. Ajout de refus pour référence absente, inventée, étrangère, événement de plan et processus réellement échoué. Source applicative inchangée. Copie des tests dans CODEX-43341-test_mission_store_attempts.py, explicitement attribuée à Codex et non destinée à être exécutée comme suite locale du dépôt.

Test réel Dell1 : 7 exécutés, 5 PASS, 2 FAIL. Le candidat accepte encore SUCCESS pour plan_created et pour tool_finished ok=false / processus exit7. AssertionError: ValueError not raised dans les deux cas. Code enfant1 ; reçu broker e3feb34262ad433c82e381b276be4e43, événement canonique43363. Le client broker a levé BrokerError après l'échec applicatif : aucun second lancement, résultat observé et conservé. Ces tests temporaires ne prouvent pas l'autonomie ni les dix cas réels.

Pause explicite43358, état interrupted43359 ; les deux workers ont fini proprement et été observés inactive avant mutation. Aucun appel distant d'issue inconnue tué. Instruction43364 remise au moteur existant : Qwen corrige la validation sémantique source, conserve les assertions, reteste puis synchronise source ET tests Dell2. Contexte actif archivé, même mission/conversation/plan/checkpoints ; transition queued puis workers redémarrés. Aucune modification des helpers live nécessitant une nouvelle installation.

failed_cycles=4 et correction_resolved_through=3 conservés. Aucune résolution artificielle du défaut source. Aucun superviseur/compteur modifié, aucun MANUAL-HOLD ni agent Codex créé. Aucun P3/P4, autre mission ou merge main. Directives consultées : AGENTS, charte, SUPERVISION-CODEX, MISSION, P2-LANCEMENT et dernier dossier43294. Autorisations autonomes conservées ; les instantanés périmés sont remplacés par les observations ci-dessus.

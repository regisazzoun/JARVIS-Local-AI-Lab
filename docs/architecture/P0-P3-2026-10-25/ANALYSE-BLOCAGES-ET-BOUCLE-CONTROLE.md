# Analyse des échecs JARVIS et boucle de continuité contrôlée

**25 octobre 2026 — proposition technique documentaire, non déployée.** Références lues : AGENTS.md, Charte, 26, 26B, 28A, JL03-COR-P1, 23C et 24. Ne pas relancer les missions interrompues par décision du propriétaire.

## Diagnostic des échecs récurrents

| Mission | Symptôme prouvé | Cause ou mécanisme documenté | Déclenchement de l'arrêt | Reprise pertinente |
|---|---|---|---|---|
| JL03-COR-P1 D01 | 3 écritures de checkpoint sans vérification puis 3 lectures identiques ; correctif vocal non reçu | absence de contrôle de progrès/diagnostic ciblé et contenu de contexte mal maîtrisé | garde de stagnation, état waiting_external | correctif ciblé, lire résultat une fois, test réel, nouveau checkpoint |
| JL03-COR-P1 D02 | 3 relectures identiques ; audit Whisper encore à effectuer | répétition sans action discriminante | interrupted ; pas de réception STT | corpus court, essai pertinent et preuve avant retour au superviseur |
| 26B | sorties techniques A/B/C parfois correctes mais rapports finaux non reçus ; erreurs de champs et preuves | contrats complexes, extraction des références, réduction du contexte et défauts aussi du contrôleur de réception | clôture explicite propriétaire le 23/10, 3 runs interrupted | **pas de reprise automatique** ; conserver erreurs et correctifs pour prochaine mission |
| 28A | programme JARVIS échoue 4/4 malgré code 0 ; mauvais nombre de modèles et chemins d'entrée ignorés ; prose inexacte | contrôle sémantique et invariants d'entrée/sortie non satisfaits ; mauvais rapprochement des preuves | clôture explicite propriétaire le 24/10 | **pas de reprise automatique** ; préserver 80B et routage acquis |
| 23C → 24 | socket / systemd refusé dans contexte Codex isolé | blocage de transport lié au contexte d'exécution, pas perte prouvée de politique | mission23C non reçue ; reprise côté hôte en mission24 | ✅🟡 transport 24 reçu : ne pas recommencer le diagnostic initial |
| 23 LiveKit | interruption vocale non reçue | chaîne voix/interruptions incomplète | NO-GO fonctionnel (à conserver) | reprendre uniquement selon mission vocale autorisée |
| 11B | Compute Expansion durable incomplet après cinq tentatives | progression/reprise et preuve insuffisantes | réceptions partielles documentées | checkpoint existant, pas de nouvelle installation |

**Synthèse :** la boucle qui manque n'est pas « relancer le modèle sans limite », mais « maintenir la responsabilité de résolution par un superviseur durable hors modèle ». Le modèle peut se tromper, terminer sa réponse HTTP ou perdre son contexte ; le contrôleur doit rester maître de l'état.

## Machine à états proposée (extension du Mission Engine 26)

`QUEUED → RUNNING → VERIFYING → COMPLETED` uniquement si contrat sémantique et preuves indépendantes PASS. Toute anomalie : `RUNNING/VERIFYING → DIAGNOSING → STRATEGY_CHANGE → QUEUED`, ou `→ ESCALATED_CODEX → QUEUED` après correction externe, ou `→ BLOCKED_EXTERNAL` si dépendance réellement indisponible. `CANCELLED_BY_OWNER` et `CLOSED_INCOMPLETE_BY_OWNER` terminent l'obligation de poursuivre et ne déclenchent aucune reprise.

La mission est **ouverte et suivie** tant que les critères autorisés ne sont pas reçus ; l'activité peut être un diagnostic, traitement d'une tâche indépendante, attente surveillée de dépendance ou intervention Codex. Ne pas brûler CPU/GPU en boucle improductive. Le superviseur persiste par systemd / SQLite, indépendamment de la session et du contexte LLM.

### Cycle atomique

1. Charger depuis SQLite seulement l'ID, l'objectif, le statut, **la prochaine tâche** (une seule), le dernier checkpoint, les contraintes et les preuves minimales ; conserver l'historique intégral hors prompt.
2. Vérifier préconditions/capacité/worker disponibles ; sélectionner Dell1 ou Dell2 comme **exécuteur de commandes** prouvé, sans supposer Dell2 serveur d'inférence.
3. Exécuter une action bornée avec ID d'opération idempotent ; enregistrer l'artefact, l'auteur, la sortie, l'empreinte et la preuve source avant l'appel suivant.
4. Contrôle sémantique indépendant (invariants, arguments effectivement utilisés, contenu, nouveaux artefacts, tests réels) ; `exit 0` ou `completed` ne suffit jamais.
5. **Progrès mesurable** : tâche reçue, invariant auparavant faux devenu vrai, preuve nouvelle utile, nouvelle cause établie ou blocage changé. Un texte reformulé, lecture inchangée, écriture identique, heartbeat seul ou nombre de tokens dépensés ne constituent pas un progrès.
6. Si aucun progrès, incrémenter `stagnation_count` pour le couple tâche/erreur/stratégie. **Après trois itérations**, interdire une quatrième invocation identique ; capturer diagnostic compact, choisir **une stratégie matériellement différente**, ou transmettre un paquet à Codex avec traces et correction recherchée.
7. Codex diagnostique les blocages réels dans les droits existants, fournit une capacité/correction testée et réinjecte un checkpoint. JARVIS demeure superviseur métier, redélègue les tâches une à une aux exécutants. Les erreurs impossibles à corriger sont décrites précisément dans BLOCKED_EXTERNAL sans inventer de validation humaine.
8. Le watchdog traite toute perte de worker, 409 « conversation occupée », timeout ou reboot : relire l'ID et les artefacts persistants, décider reprise/reconnexion, **ne pas recréer une opération externe réussie** (absence de garantie exactly-once).
9. À chaque itération publier statut, progrès, compteur, exécutant, erreur, diagnostic, résultat et prochaine action dans le flux mission/JL03. Replier le panneau n'arrête pas la collecte.
10. Vérifier une dernière fois les objectifs de la mission et les tâches dépendantes ; **seul un PASS probant clôture COMPLETED**. Une réussite locale n'est pas un GO global.

### Pseudocode de référence

```python
while mission.is_authorized_and_open():
    task = mission.next_ready_task()
    if task is None:
        mission.reconcile_dependencies_and_checkpoints()
        mission.wait_for_event_or_retry_window()
        continue
    context = mission.compact_context(task)  # jamais tout l'historique
    result = dispatch_one_task(task, context, eligible_worker())
    proof = independent_verify(task.contract, result, task.expected_outputs)
    mission.persist_atomic(result, proof)
    if proof.pass_all:
        mission.complete_task(task, proof)
        continue
    sig = failure_signature(task, proof, result)
    if mission.has_meaningful_progress(sig):
        mission.record_progress_and_reset_stagnation(sig)
    else:
        attempts = mission.increment_stagnation(sig)
        if attempts >= 3:
            mission.freeze_repeated_strategy(sig)
            diagnosis = mission.persist_compact_diagnostic(sig)
            if mission.has_distinct_strategy(sig):
                mission.switch_strategy(task, diagnosis)
            else:
                mission.escalate_to_codex(task, diagnosis)
                mission.schedule_other_ready_tasks()
    mission.yield_resources_and_resume_on_event()
```

**Attention :** pseudo-code logique, non un script prêt à exécuter ; `wait_for_event_or_retry_window` correspond à des réveils durables, pas à une boucle active qui tourne à vide. Le compteur suit une signature de panne et reste conservé lors de reprise/redémarrage ; changement cosmétique de prompt ne vaut pas stratégie différente.

## Protections contre de nouvelles pannes

- **Saturation contexte** : une tâche et quelques preuves compactes par invocation ; résumé déterministe vérifiable, pointeurs vers les documents hors fenêtre LLM ; séparation des conversations D01/D02.
- **Échec de contrôle sémantique** : contrat positif explicite et vérificateur externe ; distinguer FAIL de l'application et FAIL du juge (26B a prouvé les deux).
- **Réentrance** : verrou par tâche + lease/heartbeat et clé idempotente, relire les résultats réels après délai d'expiration ; deux slots existants de 28A conservés.
- **Dépendances matérielles ou droits** : ne pas inventer de réussite ; état BLOCKED_EXTERNAL suivi, alerte Codex, passage à un travail indépendant, reprise événementielle.
- **Arrêt utilisateur** : priorité supérieure ; `CLOSED_INCOMPLETE_BY_OWNER` bloque tout redémarrage automatique. Une nouvelle autorisation explicite déclenche seulement la reprise volontaire de cette mission.
- **Pas de condition de durée infinie artificielle** : fonctionnement persistant tant que la mission est autorisée et qu'une action utile est possible ; aucune garantie de résolution d'un problème techniquement impossible.

## Critères de réception de la nouvelle boucle

1. Trois échecs identiques provoquent zéro quatrième essai identique, un diagnostic et un basculement de stratégie ou escalade durable.
2. Coupure conversation/worker + redémarrage : même mission, même tâche/checkpoint, aucun doublon de modification.
3. Une fausse réussite `exit=0` mais invariant erroné est refusée, et signalée à Codex.
4. Deux tâches sur Dell1/Dell2 : un blocage ne tue pas l'autre et les preuves remontent à JARVIS.
5. Rapport fidèle aux auteurs, preuves et statut ; traces intégrales accessibles à JL03.
6. Demande d'arrêt propriétaire respectée sans nouvelle exécution.
7. Réveil sur événement utile après `BLOCKED_EXTERNAL` sans répétition aveugle.

## Priorisation et intégration

**P0.1** = intégration prioritaire de ce contrôleur anti-boucle / compression de contexte avec 26/26B/JL03-COR-P1. **P0.2** = contrôleur de preuves et états de clôture. Ce sont des compléments aux missions existantes, non une réécriture de leurs résultats. **Ne pas créer de nouveau moteur de missions** : étendre le moteur 26, son broker, les workers et SQLite canoniques.

Le document est une analyse et un cahier technique. **Aucune boucle autonome n'est installée** par ce commit ; son implémentation passe par une mission explicitement lancée.

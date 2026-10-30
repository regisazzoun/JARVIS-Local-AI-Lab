# Observation manquante pendant la vérification d’un rapport

## Cause reproduite

La sonde native864da7c457ef4d82b0b284d9ceb30eeb a exécuté une écriture de brouillon puis `mission_verify`. Le vérificateur a retourné `INSUFFICIENT`, avec `Choose each latest original service receipt exactly once: []` : aucune observation runtime systemd n’avait été produite. L’étatP2 est resté `VALIDATION_INCONCLUSIVE`, conformément à son sens ; ce n’est ni une réussite ni une correction fonctionnelle échouée.

Le workflow `pending_report_validation` projetait donc la phase `verify`. `durable_cycle` n’y proposait que `mission_verify`, `mission_note` et `mission_block`, même sous le profil `read_only_service_snapshot`. Qwen ne pouvait pas appeler l’outil permettant d’obtenir le reçu manquant. Il a proposé un blocage sans preuve réelle, refusé et escaladé. Changer le profil ou résumer le contexte ne suffisait pas à ouvrir l’outil caché.

## Correction Codex

Commit`0ad2e8c` : dans ce profil de service explicitement sélectionné seulement, la phase `verify` propose aussi `host_service` et `mission_report_facts`. Le schéma offert limite l’action à `status`, `show`, `is-active`, `is-enabled` ; la politique réelle du broker continue de s’appliquer. Aucune écriture ni clôture n’est offerte à cette étape. Qwen choisit les observations et la suite.

L’état de la tentative, les compteurs, les FAIL et INSUFFICIENT ne sont pas modifiés. Aucune réexécution d’écriture n’est déclenchée par le correctif. Le test de cycle contrôle à la fois les outils proposés, la protection du brouillon et l’identité des états/compteurs avant-après.

## Installation et reprise

La source active correspondait exactement à la version Git précédente avant intervention. Sauvegarde privée `durable_cycle.before-observation-recovery.py`, copie ciblée vers `/opt/jarvis/conversation/jarvis/durable_cycle.py`, puis recharge des deux workers alors qu’aucune mission n’était running/queued/retrying. La conversation n’a pas été redémarrée pour ce correctif.

Événement93898 : cause/correction/retour arrière enregistrés par Codex. Reprise de la même mission après correction structurelle vérifiée ; ni nouveau nom de problème ni remise à zéro. Qwen a effectivement choisi et exécuté `host_service show`93925/93926, puis `status`93949/93950 et `is-active`93973/93974. Ces lectures prouvent l’utilisation de la capacité réparée ; la clôture du rapport exige encore ses preuves propres. Le résultat terminal est publié dans `PREUVES-JARVIS.json` et les tests.

Les instructions courtes d’assistance sont attribuées à Codex. Le plan et les choix d’outils restent ceux du modèle. Les observations de cette sonde ne valent pas validation autonome des autres missions historiques.


## Résultat réellement obtenu

Après les trois observations, `mission_verify` rejette le brouillon initial94001 FAIL. Qwen sélectionne le compositeur et les références réelles94024 ; le broker écrit le relevé corrigé94039. Nouvelle lecture indépendante par le vérificateur94062, résultat94064/94067 PASS. Qwen complète T194089 puis appelle intervention_report ; publication factuelle94107, clôture native94109. Durée de cette reprise supervisée :196,65secondes.

Codex a relu directement le fichier et recomparé ses références/contenu aux trois reçus originaux : SHA256f49c7c435695198029b164ddf64776abd53e1785c17bd29c9c44e48d4c83ef96. Une nouvelle commande systemctl confirme active/rc0. Le contrôle utilise le rendu canonique pour la comparaison exacte ; il ne prétend pas être une seconde revue sémantique indépendante de prose. La tâche source reste un exemple de plan initial imparfait, malgré cette réception fonctionnelle de l’observation.

# Support borné de l’escalade 63894

🟡 Candidat non terminé ; P4 non validée. Même mission
`d8fe752876db480cbe5f22cd5525e2dd`, même plan 3.

Directives consultées : AGENTS, charte, supervision, LANCEMENT-ATTESTATION,
PLAN-REPRISE-INSTRUMENTATION, CORRECTION-FAUX-MATCH, INTERFACES-PERENNES,
SUIVI et ROADMAP ciblés. Autorisation de la suite P4 conservée, candidat sans
installation applicative avant revue indépendante.

L’escalade 63894 suit trois demandes de références anciennes 63528, 63653,
63623, refusées par le schéma qui propose les reçus courants 63869, 63839,
63809, 63779. Le filtrage installé à 63738 fonctionne. En revanche, sa voie
d’archive annoncée `context_recall` restait désactivée dans le contrat persistant.

Correction de capacité : retrait du seul `context_recall` de
`authority_disabled_tools`, sauvegarde privée de la spec précédente. Contrôles
réels : outil présent dans Registry, autorisation persistante active, lecture
ciblée réussie de l’événement 63653. Aucun changement de source applicative,
reload, script de supervision ou compteur.

Revue indépendante 63897 : reçu complet 63869 contrôlé par SHA-256
`c554dadf555dbdcba8f517dd0c4abdf73836a5d2f46c13e341c442821f89acdd`, rc 0,
worker de 44 lignes analysable par AST, fonctions worker_locks/run/main.
L’instrumentation attendue reste absente. Cette observation ne teste pas le
candidat et ne prouve aucun objet chargé dans les services actifs.

Instruction courte 63898, archivage natif du dialogue périmé 63899, action
Codex-periodic 63900, puis remise en file. États d’autorité et événements de
refus comparés avant/après : identiques. Aucune lease avant intervention.
Qwen conserve le choix du code, des tests et des exécutants ; priorité à
l’édition réelle et à ses tests. Aucune réception technique inscrite au registre.

Observation après reprise : inférence native 63911, inspection rc0 à 63926,
puis nouvelle inspection de structure 63942. Événement Codex-periodic 63980 :
la reprise est réelle, mais aucune édition ni aucun test du candidat n’est
encore observé à ce contrôle. Le retour aux lectures reste une limite explicite,
pas un progrès applicatif ni une réception de l’instrumentation.

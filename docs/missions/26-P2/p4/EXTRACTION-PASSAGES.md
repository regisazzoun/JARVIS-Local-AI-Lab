# Reprise du contrôle des causes — 29 octobre 2026

Le rapport t1 reste inchangé, SHA256
`7fe47c83ae837d85b6baf0a0cde29500fe445f41587abae2bc1185c7be98dac1`.

## Blocage constaté

Deux réponses réelles du modèle (70376/70381) ont sélectionné une citation vide,
malgré une cause classée `missing_original_reference` et le rôle
`past_rejection_cause`. Le contrôle de format a correctement refusé les deux
sorties (70377/70382), puis produit INSUFFICIENT70383 et escalade70386.
La supervision était arrêtée sur sa borne ; aucune opération n'était en cours.
Une relance identique n'aurait pas constitué une correction.

## Modification de Codex

Pour les revues bornées, contrat interne `report-cause-span.v1` : le modèle
sélectionne un identifiant dans les passages originaux fournis. Le moteur
récupère le texte exact correspondant ; il ne crée ni citation ni catégorie.
Le modèle continue de déterminer la catégorie et le rôle, sans connaître les
diagnostics originaux lors de cette extraction. Le choix est ensuite comparé
aux diagnostics réellement enregistrés. Les autres revues gardent leur contrat.

Identifiant inconnu : refus de schéma. `NO_CAUSE` avec une cause passée : refus
de validation. Deux sorties invalides : INSUFFICIENT, jamais PASS. Un statut
historique erroné ou une cause incompatible reste bloquant, même si le modèle
annonce un accord. La revue complète du récit et la relecture du fichier restent
obligatoires ; ce changement ne valide aucun déploiement.

## Vérifications

133 tests logiciels ciblés réussis : registre des tentatives, cycle des rapports
et contrôle de couverture/prose. Nouveaux cas : choix exact conservant une faute
d'orthographe, identifiant inconnu, cause passée sans passage, absence légitime
de cause, statut et diagnostic incompatibles. Ces tests ne prouvent pas une
autonomie opérationnelle.

Module installé avec sauvegarde privée. Sonde réelle déclenchée par Codex :
Qwen a sélectionné `P1`, catégorie `missing_original_reference`, citation exacte
non vide, événement70393. Cette sonde vérifie la nouvelle interface ; elle ne
constitue pas une réception du rapport ni une tâche autonome JARVIS.

Résolution70394 liée à cette preuve, compteurs et originaux conservés. Les
workers ont été redémarrés sans appel actif, puis JARVIS a été remis en file
sur la même tâche et le même plan pour la vérification complète. Services
conversation et JL03 préservés. Pas de reprise des dix scénarios P2 ni du
candidat P4 reçu ; pas de fusion dans main.

Statut à la transmission : vérification native en cours, t1/P4 non reçues.

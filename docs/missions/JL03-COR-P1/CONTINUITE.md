# Continuité des corrections — décision propriétaire du 25 octobre 2026

Le propriétaire accepte la capture (« c’est bon pour la capture »), tout en signalant que la transcription reste imparfaite. D01 est donc acceptée sur le périmètre capture ; cela ne valide ni une autonomie sans assistance ni tous les défauts vocaux. D02 garde une réserve. L’absence de contexte est une hypothèse du propriétaire, pas une cause démontrée ; le chantier mémoire est différé.

Codex avait laissé la qualification ultérieure bloquer la suite. Cette interprétation est corrigée : aucune approbation intermédiaire n’est requise. D03 et D04 sont transmises successivement et réellement prises en charge par les deux workers du moteur canonique, dans des missions, conversations et worktrees séparés. Des lectures et commandes natives sont observées ; aucune correction D03/D04 n’est encore réceptionnée à cette date.

D17 est préparée dans sa propre mission canonique, en état draft. Le coordinateur ciblé `phase1_dispatch.py` observe uniquement cette liste finie. Toutes les 30 secondes, il confie D17 aux workers existants dès qu’un des deux contextes est disponible. Un blocage, un échec ou une attente extérieure documenté ne bloque pas les travaux indépendants. Une opération native encore engagée conserve sa place jusqu’à sa fin ; on ne dépasse pas deux contextes en activité. Aucun redémarrage ou réessai aveugle d’une tâche bloquée n’est déclenché.

Le timer `jarvis-jl03-p1-dispatch.timer` et son service sont installés. Ils utilisent MissionStore et la même SQLite ; ils n’exécutent aucun outil de mission, ne font aucune inférence, ne créent aucune base et n’acceptent aucun correctif. Les trois tentatives restent contrôlées par le garde existant. Un arrêt produit un dossier COORDINATION.json et un événement canonique à relire par Codex ; cet enregistrement n’est pas une intervention technique accomplie. Les intégrations et réceptions restent des contrôles Codex explicites.

Registre opérationnel : `/var/lib/jarvis/projects/jl03-cor-p1/REGISTRE-CODEX.json`. REGISTRE.json dans Git est un instantané publié, pas une télémétrie en direct. Le timer journalise ses décisions via systemd et les événements de mission. Il est limité aux missions préparées D03/D04/D17, sans nouvelle mission hors périmètre. Après épuisement de cette liste, il n’en crée aucune.

Contrôles Codex : cinq cas du sélecteur reçus (deux places occupées ; place libérée par blocage ; opération en vol ; réception différée ; absence de deuxième envoi). Première exécution réelle : D03 et D04 running, D17 draft, aucun troisième envoi. Ce sont des contrôles d’ordonnancement, pas des preuves de réussite des corrections.

Les capacités projets isolées sont fournies sur les deux Dell pour D03/D04/D17 avec les runtimes déjà installés. Aucun modèle, routage, mémoire, quota, JL01 ou JL02 modifié. Dell2 comporte réellement une RTX3090 et une RTX3080 ; D17 doit vérifier l’existant avant toute modification et ne doit pas interpréter une charge à zéro comme une panne.

## Reprise corrective D03

Après diagnostic et réparation source/harnais contrôlée par Codex, une reprise ciblée unique peut être armée sur un plan versionné et un événement de stratégie vérifié. Cela ne réessaie pas automatiquement un blocage inchangé. D04/D17 conservent leurs places jusqu’à libération. Voir [déblocage D03](D03/DEBLOCAGE-CODEX.md).

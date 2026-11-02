# Essais réels de l’ordonnanceur — 1 novembre 2026

**✅ Sept scénarios réels reçus sur la version déployée de l’ordonnanceur, via Tailscale.** Une tâche utile a terminé : contrôle en lecture seule des **1 384 fichiers de référence** du paquet Qwen Code copié sur Dell2. Toutes leurs empreintes correspondent à la référence du Mac JARVIS.

| Scénario | Preuve observée |
|---|---|
| Admission et démarrage | Processus distant actif, progression jusqu’au fichier49 |
| Pause opérateur | Groupe arrêté ; checkpoint112 resté112 pendant la pause |
| Reprise | Progression depuis le checkpoint conservé jusqu’au fichier152, puis au-delà |
| Perte du contrôleur | SIGKILL ciblé sur le seul contrôleur ; bail distant8s expiré, arrêt au checkpoint311 ; reprise native systemd du contrôleur observée, PID différent et NRestarts1 |
| Achèvement utile | 1384/1384 empreintes conformes, aucun fichier manquant dans les checkpoints, aucun doublon dans les1384 étapes enregistrées |
| Redémarrage après achèvement | Entrée témoin réactivée pour le contrôle, puis contrôleur redémarré : aucun rejeu, nombre d’exécutions distantes et compteurs inchangés |
| Préservation | JM-01 désactivée individuellement et toujours paused/MainPID0 ; services centraux actifs, WebUIHTTPS200 |

Le témoin a été lancé trois fois au niveau distant : début, reprise après pause, reprise après expiration du bail. Le compteur central final vaut2 : l’interruption ambiguë du contrôleur reste comptée, la préemption normale ne consomme pas un échec. Aucun ancien compteur n’a été remis à zéro. Les fichiers déjà enregistrés ont été sautés à la reprise ; le journal de commits d’étapes contient exactement1384 chemins distincts.

## Erreur du harnais et contrôle indépendant

La première orchestration a signalé FAIL après l’achèvement : le calcul de référence suivait l’ordre des objetsPath, le rapport utilisait l’ordre des chemins relatifs sous forme de chaînes. Certaines arborescences donnent des ordres différents. Cette erreur de mon harnais de comparaison ne concernait ni le contenu des fichiers ni le traitement de l’ordonnanceur. Le résultat initial, les compteurs et les artefacts restent conservés ; aucune tâche terminée n’a été relancée pour obtenir un succès.

Le contrôle indépendant vérifie désormais chaque chemin et chaque empreinte, les entrées du checkpoint, l’unicité du journal et la racine calculée après tri canonique. Il a passé sur les artefacts réels : **1384 fichiers, zéro écart, zéro doublon**, racine`481dd9ce7940f794df2149082f1ac0925ea68549ccc0b17f2bc2038fe58b0392`.

Quatre tests du vérificateur passent : ordres de tri différents acceptés si les données sont identiques ; doublon, entrée manquante et contenu modifié refusés. Ces quatre tests concernent le harnais, pas quatre nouveaux cas du moteur. Les21tests logiciels de la réception précédente ne sont pas recomptés ni rejoués dans cette campagne.

## Périmètre réel

La tâche est déterministe, préparée et exécutée sous contrôle Codex. Elle ne démontre pas une autonomie nouvelle du modèle Qwen ni une réception mobile. Elle lit les fichiers de programme de référence et écrit seulement ses résultats/checkpoints dans son espace de test. Une temporisation volontaire rend les interruptions observables ; aucun débit disque ou benchmarkNVMe n’est mesuré.

La coupure a concerné uniquement le processus du contrôleur, sans arrêt du réseau, de Tailscale ou des machines. Le bail prouve ici le comportement en l’absence de renouvellement ; il ne constitue pas une réception d’un déplacement intersite ou d’un reboot matériel. Aucun changement des modèles, du routage réseau ou des autres services n’a été effectué. JM-01 et M26-P4 restent hors du travail exécuté.

Le service de l’ordonnanceur est à nouveau enabled/active et idle. Le témoin terminé est conservé dans le registre ; il n’est pas rejoué. La version déployée n’a pas été changée pour ces essais.

## Reproduction et traces

`ops/fixtures/scheduler_integrity/integrity_unit.py` est le témoin à checkpoints. Son manifest de référence attendu reste privé et fixe un répertoire de code approuvé, des chemins relatifs et leursSHA256. Le programme refuse une résolution de chemin hors de ce répertoire ; il n’exécute aucun fichier audité.

`verify_integrity.py` reçoit quatre chemins locaux : référenceJSON, checkpointJSON, journalJSONL, rapportJSON. Tests : `python3 -m unittest discover -s ops/fixtures/scheduler_integrity -p 'test_*.py' -v`.

Les états et journaux détaillés sont conservés dans le répertoire privé de campagne. Le JSONpublic est expurgé et conserve la mention du premier FAIL du harnais. Les scripts privés pilotant les services ne sont pas publiés avec des adresses réelles. Sources de consignes : AGENTS/charte et réception finale relus ; demande propriétaire de tests contrôlés ; périmètre ordonnanceur seul, pas de fusionmain.

# Mission14B — installation et intégration du Dell n°2

Ordre propriétaire : initialiser dans le moteur existant et transmettre à JARVIS, exécutant principal. Codex intervient ponctuellement uniquement lorsqu'une capacité réellement manquante est démontrée, puis rend la main.

## Périmètre autorisé

Installer et intégrer le Dell n°2 sous Debian13 en réutilisant les procédures validées : identité propre de cible et disques, accès administratifSSH/Ansible, socle système, pilotesNVIDIA/CUDA et vérifications ciblées. DeuxRTX3090 seulement si leur alimentation est correctement raccordée ; une carte non raccordée ne bloque pas les tâches indépendantes. Ne pas assimiler les identifiants, disques ou autorisations du Dell1 à ceux du Dell2.

## Exclusions impératives

Aucune modification du moteurOllama, de ses modèles ou services, du routage, de l'ordonnanceur, des quotas ou de la répartition des charges existants. Ne pas activer le nœudDell2dans le routeur ni installer une nouvelle pile d'inférence dans ce périmètre. Ne pas exécuter en bloc un ancien playbook qui installeraitOllama. Aucun autre changement d'architecture. Préserver Dell1, Mac mini, JL-01/JL-02/JL-03, mémoire, checkpoints, SSH/Tailscale et DHCPBbox.14Aet24-Oldrestent distinctes et non lancées.

## Exécution et incidents

JARVIS propose son plan et sélectionne les opérations réellement disponibles. Il documente chaque blocage : cause observée, catégorie, tentative, correction, résultat réel, reçu/événement et prochaine action. Après trois échecs comparables, arrêter cette stratégie, diagnostiquer et, si utile, créer une sous-mission corrective avec les mécanismes disponibles, puis reprendre au checkpoint utile ; aucun renommage artificiel ni quatrième répétition. Si la création de sous-mission manque réellement, préparer le dossier et la tâche corrective sans inventer une fonction disponible.

N'appelerCodexqu'en présence d'une capacité manquante réellement constatée : dossier bref via capability_request avec objectif/cible, opération et erreur, preuves, trois essais au maximum, accès ou outil manquant, correction minimale proposée et test de retour. Si assistance indisponible, conserver la demande prête et continuer les tâches indépendantes. Une dépendance physique ou une cible non identifiée n'est ni un succès ni un motif pour répéter les mêmes scans indéfiniment.

Les identités exactes et secrets restent privés. L'installation est autorisée sur la cibleDell2 identifiée ; aucune opération destructive sur une cible ambiguë ou sur le profilDell1 `dell-observe`. Ne pas reprendre les contrôles déjà reçus du Dell1 ; les appliquer à la nouvelle cible selon leur pertinence. Aucun benchmarkNVMe ni nouveau processus d'approbation.

## Références disponibles

Dans references/ : référenceDell1pourmission14, préparation logiqueDell2en28A, raccordement11B et leur provenance. Les anciennes étapesOllama/routage sont explicitement exclues par le présent ordre. Les scripts originaux de déploiement existent sous /home/adminjarvis/JARVIS/13de-reprise/deployment/13de ; ne pas recopier leurs secrets/manifesteDell1 ni exécuter un installateur avant observation/qualification de sa cible. Si un accès agentique à une procédure manque, demander cette seule capacité avec preuve.

Livrables persistants dans /var/lib/jarvis/projects/mission14b : plan/checkpoints du moteur, journal des blocages, inventaire expurgé, dossier de capacités si nécessaire et rapport d'installation distinguant préparé/exécuté/vérifié. Aucun GO d'installation sur une simple réponse du modèle.

Directives consultées parCodex : AGENTS, charte, SUIVI/ROADMAP courants, REFERENCE-DELL1-POUR-MISSION14, PROMPT-INSTALLATION-AUTONOME13D-E, DELL2-PREPARATION28A et raccordement11B. Autorisations préservées : installation duDell2, autonomie dans ce périmètre, accès/procédures déjà validés. Contradictions corrigées : anciennes exclusions généralesDell2 remplacées uniquement pour14B ; anciennes étapesOllama/routage non reprises. Aucun changement de moteur ni d'architecture.

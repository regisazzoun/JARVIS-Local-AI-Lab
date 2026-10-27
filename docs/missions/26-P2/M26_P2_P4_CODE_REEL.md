# P4 — code réel, audit lancé le27octobre2026

**EN COURS — NON VALIDÉ.** Après réceptionP3 avec réserves55310, paquet court transmis à Qwen80B dans la continuation native `d1b0d69639724c60b5bd1b2143b1a5fa`, liée au parent et à la même SQLite. [Paquet effectivement transmis](p4/LANCEMENT.json).

Premier objectif : inventorier les vrais environnements et distinguer source/copies/candidat/application active. Les deuxDell exécutent l'audit des exports engine ; le service central tourne surMac dans /opt/jarvis/conversation. Un disque ou un commit Git ne prouve pas les objetsPython chargés. Codex fournit une observation réelle desPID etSHA surdisque, explicitement NON reçue comme attestation mémoire. JARVIS choisit ses contrôles surlesdeuxDell, identifie les inconnues et la capacité manquante. Aucun déploiement pour ce premier audit.

La suite autoriséeP4 devra traiter provenance source/candidat/version active, divergence, déploiement partiel, vrai contrôle d'application et rollback. Aucun de ces critères n'est reçu par ce lancement. Le profil du paquet est test-only ; l'artefact d'audit reste horsengine. Les corrections et tests de l'application surDell, puis les déploiements utiles, seront tracés dans les paquets suivants, sans accord humain supplémentaire.

Le superviseur périodique existant cible désormais ce seul paquet P4 ; P3 est dans received_tasks. Maximum3passages par cause stable, reçus/compteurs conservés. Ni14A ni24-Old, aucune fusionmain ni modification des modèles/routage.

## Intervention ciblée après stagnation

Git absent sur copies exportées et mauvais chemin engine/core.py ont provoqué trois incidents. Préflight57077 confirme engine/jarvis/core.py et cinq empreintes surlesdeuxDell. Un défaut du schéma d'exécution a aussi été corrigé au commit926ab42 : executor/command obligatoires selon mode,70testsPASS. JARVIS a réellement produit des artefacts surDell2(57177) etDell1(57205), relus parCodex57490 : deux fichiers correspondants, pas une réception complète. Mode d'exécution contraint ensuite relâché pour la suite. [Dossier et limites](p4/INTERVENTION-GIT-CHEMINS-CONTRAT.md). Code chargé toujours non prouvé, P4 toujours NON VALIDÉ.

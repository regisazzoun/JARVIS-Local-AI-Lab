# JM-01 — JARVIS Mobile

Ordre propriétaire du1novembre2026 : lancer surDell2 s’il est disponible, avec suspension/reprise et checkpoints. Issue46. Directives consultées parCodex : AGENTS, charte, rapportsPR39/41, état26/PR29, rapportPR47 et issue46 ; autorisations conservées sans validations intermédiaires.

Objectif : réutiliser OpenMobileUI deRonasIT, iOS d’abord, Android ensuite, et charteLauncher. Première tranche : audit code/licence/branche, inventaireAPI/fonctions, prototype de connexion isolé, tests et bilan. Sources épinglées dansreferences/ENVIRONMENT.json. Aucun accès aux secrets, aucune distributioniPhone ni déploiementprod. Dell1 et servicesQwen/WebUI préservés.

Exécutant : QwenCode0.26.4 officiel, modèle80BDell2 à32768. Codex prépare le superviseur, les objectifs et les vérifications. Les résultats du modèle restent à vérifier indépendamment ; un code0 ne prouve pas toutes ses affirmations. Les checkpointsGit des unités terminées sont conservés ; reprise native de session pour unité interrompue, maximumtrois échecs comparables sans remiseàzéro.

# Audit initial avant adaptation — 26octobre2026

Les sources lues sont les fichiers réellement installés sous /opt/jarvis/conversation/jarvis, le backendJL03 et la politique hôte propriétaire (seulement ses champs publics exportés). D03/D04/D17 sont completed ; aucune reprise de ces missions.

| Question | Réponse observée avant cette phase | Preuve |
|---|---|---|
| Où sont les services centraux et files ? | Mac mini : API8765, JL038766, deuxworkers Python, SQLite canonique | systemctlExecStart et jarvis/worker.py, missions.py |
| Où raisonne JARVIS ? | Le rôle mission utilise Qwen3-Coder-Next80B surDell1 ; conversation27B surMac. Dell2 n’est pas nœud d’inférence actif | config13e champs modèles/profils et événements compute_route_observed |
| Qui choisissait le fichier et le test ? | Dans les appels bruts, arguments émis par le modèle sous les instructions Codex. Dans jl03_run_checked_protocol, code et contrats Codex choisissent effectivement fichiers/commandes | tool_calls des missionsJL03 ; jl03_assist.py fonctions repair/check/protocol |
| Qui choisissait la machine ? | host_exec reste local auMac ; host_remote utilise l’hôte demandé. Le protocoleJL03 boucle sur des hôtes fixes dans son code | jarvis/host_client.py ; jl03_assist.py ; reçushost_remote |
| Qui interprétait le test ? | Qwen peut lire un reçu et proposer la suite ; gardes/contrats/protocoles codés contrôlent états et PASS. De nombreuses corrections de stratégie sont Codex | décisions/outils et événements Codex, validationssémantiques |
| Qui clôture ? | JARVIS déclenche les outils ; les prérequis persistants et le vérificateur conditionnent la validation ; Codex reçoit indépendamment | durable_tools.complete, mission_store.contract_status, verification.py, réceptionJL03 |

## Pourquoi les opérations D03/D04 étaient surMac

L’emplacement de l’inférence ne déplace pas un processus shell. host_exec lance un shell hôte Mac ; host_write_file/edit_file modifient des chemins Mac. Ce sont ces outils que le modèle a demandés dans les premiers reçus. Les espaces distants, introduits ensuite, n’étaient initialement pas peuplés ; les erreurs host/action/chemins et les anciens reçus ont entretenu le blocage. La clôture a nécessité une aide Codex fortement déterministe. Elle ne démontre pas une autorité technique autonome deQwen.

Le dernier état n’est toutefois plus «Dell2 ne fait quels» : les correctionsJL03 comportent de vrais tests et modifications distants, puis des protocoles exécutés parJARVIS. Leur attribution détaillée est conservée dans JL03-COR-P1 ; la nouvelle réception devra prouver des choix du modèle, pas réutiliser ces scripts comme preuve d’autonomie.

## Capacités existantes réutilisables

Broker root et SSH à hôtes épinglés ; espacesprojet autorisés surles2Dell ; project_exec Bubblewrap, project_upload/download avec vérificationSHA. Python3 et Node20 réellement exécutés surchaqueDell ; Git absent dans ces environnementsdeprojet. Les dépôts Git documentaires sont disponibles surMac ; une version exacte peut être représentée par un manifesteSHA des sources, sans prétendre disposer d’un commit distant.

Les projets actuels ne donnent pas accèsGPU lorsque gpu=false. Ils isolent /usr et la racine mais n’ajoutent pas à eux seuls de limiteCPU/RAM au shell. La nouvelle zone de démonstration doit limiter les processus de test indépendamment de l’inférence. Aucune modification des pilotes, modèles, profilsGPU ou services conversationnels n’est nécessaire.

## Défauts structurels à corriger

1. Séparer l’émission d’une décisionQwen du transport/exécution, avec l’identité effective d’inférence issue des mesures réelles, pas d’un champ libre.
2. Offrir des outils distants typés qui laissent au modèle le fichier, la commande et l’exécutant, sans Mac commeexécutant par défaut.
3. Retourner au modèle sorties et empreintes bornées, avec versions exactes pour validationcroisée.
4. Compter les cycles de correction et les erreurs de délégation de manière durable, sans assimiler un test échoué à une absence de vérification.

Les règles de permission, transport, quotas et dépendances restent déterministes. Elles ne doivent choisir ni la correction applicative ni le test à la place deQwen. Cette distinction est le critère de réception central.

# Comparatif mesuré des modèles Dell

État : modèle80B retenu pour la recette opérationnelle, encore en cours. Les mesures sont des inférences réelles déclenchées par JARVIS via compute_benchmark, avec réservation de la file canonique. Le programme et son juge sont Codex. Trois modèles ont chacun reçu les mêmes six prompts, contexte4096, température0, seed7,768tokens maximum. Le32B conserve ses six réponses précédentes avec juge rectifié, sans nouvelle inférence.

| Modèle | Score brut | Débit médian tokens/s | Chargement du premier appel(s) | MémoireVRAM totale déclarée par Ollama(Gio) |
|---|---:|---:|---:|---:|
|qwen3.5:27b-q4_K_M|4/6|29.7|6.5|15.5|
|llama3.3:70b-instruct-q4_K_M|2/6|18.5|12.32|40.87|
|qwen3-coder-next:q4_K_M|5/6|87.5|17.29|44.42|

Le32B atteint3/6 après correction du faux FAIL du juge, autour38tokens/s sur son essai antérieur. Le27B Dell est la référence de cette comparaison ; ces29,7tokens/s ne sont pas la mesure du Mac, ni un débit conversationnel de bout en bout. Le chargement du premier appel correspond à un runner/modèle chargé, sans purge du cache disque du système. Les temps de premier contenu et les sorties complètes sont dans les JSON.

Le80B atteint environ2,95fois le débit médian du27B sur ces cas, avec une réussite supplémentaire. Cela justifie son essai agentique concret, sans démontrer une supériorité universelle ni une autonomie générale. Le70B est plus gros que le27B et sous-performe ici ; le nombre de paramètres ne suffit pas à sélectionner.

## Réserve sur le cas de planification

Le juge brut refuse coverage pour les quatre modèles, car il exige la vérification avant le rapport. Les réponses proposent de vérifier l’ensemble des artefacts, rapport compris, à la fin. Le prompt parle à la fois d’un rapport expliquant les vérifications et de vérifications après les artefacts concernés : cette ambiguïté ne permet pas de conclure à elle seule à une incapacité globale de planification. Les verdicts bruts sont conservés ; la revue indépendante qualifie ce critère de non concluant hors interprétation stricte du juge. Les cinq autres cas donnent respectivement4/5(27B),3/5(32B),2/5(70B),5/5(80B), sans nouvelles générations ni effacement de FAIL.

## Ressources et offload observés

Les deux cartes sont effectivement utilisées par le80B. Au contexte opérationnel24576, une lecture indépendante montre environ23044MiB et22968MiB utilisés. Le journal annonce49/49couches sur GPU, des buffersCUDA0/1et un buffer CPU_Mapped6511,19MiB. L’API indique une empreinte totale supérieure à size_vram. Il existe donc un mappageCPU/RAM ; il ne faut pas présenter cela comme des couchesCPU partiellement déchargées puisque le journal indique toutes les couches sur GPU. La taille du mappage n’est pas une mesure de RAM physique résidente exclusive au modèle. Le Dell conserve sa DDR4 existante ; aucune DDR5 n’est installée.

Les mesures applicatives à24576tokens diffèrent du screening4096 et sont documentées avec la recette. La conversation27B reste sur Mac ; les changements de contexte internes sont stabilisés pour éviter le rechargement répété du runner.

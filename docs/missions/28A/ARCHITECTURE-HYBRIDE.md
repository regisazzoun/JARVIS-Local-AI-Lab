# Architecture28A — déploiement en cours

🟡 Mission en cours, pas de réception finale. Branche `codex/mission-28a-routage-modeles`, base préparatoire `ac2b0cb`. Les réceptions précédentes et la décision propriétaire sur le raccordement électrique restent acquises dans leur périmètre.

Le modèle conversationnel reste `qwen3.5:27b-q4_K_M`, réellement exécuté sur le Mac mini et son GPU externe. Le routeur `jarvis/compute.py` choisit le Mac pour la conversation et le Dell1 pour les missions ; les demandes critiques peuvent utiliser le Dell avec repli vers le même27B local. Le Dell utilise une instance Ollama expérimentale distincte, port11435, partageant son catalogue existant et exposant les deux GPU. L’instance historique11434 reste conservée. Après essais réels déclenchés par JARVIS, le moteur mission retenu est `qwen3-coder-next:q4_K_M` (80B MoE, environ3B actifs). Les scores bruts sur six cas sont27B4/6,32B3/6,70B2/6,80B5/6 ; le cas coverage est ambigu et reste non concluant pour une aptitude globale. Voir [comparatif](MODELES-DELL-COMPARATIF.md). Le80B utilise les deux cartes et49/49couches GPU ; les buffers CPU mappés ne prouvent pas un offload de couches sur CPU.

Le worker reprend `Missions`/`DurableCycle` existants dans un processus séparé, avec deux slots de worker, verrou partagé global et verrou exclusif par slot, dans les mêmes fichiers SQLite. Il ne crée pas de seconde mémoire. Les files d’inférence et leurs baux sont conservés dans la base des missions. La priorité opère entre deux inférences bornées ; aucune préemption d’un calcul GPU en cours n’est démontrée. Les missions ne se replient pas automatiquement sur le Mac, pour préserver le modèle interactif.

Les unités `jarvis-background.slice` et `jarvis-interactive.slice` appliquent quotas et poids CPU. Sur12threads, CPUQuota900% correspond à9CPU, soit75% de la capacité logique. Le watchdog réduit le quota de fond à300% pendant une interaction ou une pression détectée puis le rétablit. Les commandes hôte de mission héritent aussi du slice via le broker. MemoryLow est établi sur le parent et le slice interactif ; l’admission vérifie la mémoire disponible avant chargement. Ces protections ne constituent pas une partition matérielle de25% de VRAM.

Le Dell2 reste explicitement désactivé, sans URL ni tentative de découverte réseau. Son profil logique ne vaut pas enrôlement ni test matériel. Le routage est intégré aux appels existants, avec nœud/modèle effectifs et métriques dans les événements de mission.

Les profils GPU sont des programmes protégés installés par Codex et des actions structurées exécutées par JARVIS. L’essai court a atteint699,37W cumulés ; retour250W/carte vérifié indépendamment. Cette mesure n’est pas une certification électrique ni une tenue prolongée700W. Aucun wattmètre système n’est disponible dans les preuves.

La comparaison et les contrôles opérationnels de priorité/repli sont exécutés. La réception agentique finale et ses artefacts restent en cours.14A,24-Old,TTS-01 et l’installation Dell2 ne sont pas lancés par28A.

## Stabilisation et reprise

Les contextes sont fixés à16384tokens sur Mac et24576sur Dell. Une requête interne plus petite conserve cette taille ; une demande dépassant le profil est refusée explicitement. Cela évite les rechargements alternés du runner. La file critique attend au plus2s avant repli local ; il ne s’agit pas d’une interruption d’inférence GPU. Les événements distinguent modèle demandé historique et moteur effectivement exécuté.

Les vérifications sémantiques conservent la référence du reçu parent mission_verify. Le candidat de clôture inclut le vrai identifiant de preuve et le rapport écrit puis relu ; il évite la boucle sur un identifiant de lecture enfant. Un contrat sémantique déclaré bloque aussi la clôture d’une mission dirigée s’il n’est pas satisfait. Un outil enregistré manquant dans la sélection active peut être découvert avec son schéma, puis appelé dans la phase d’exécution ; cela n’étend pas la politique hôte.

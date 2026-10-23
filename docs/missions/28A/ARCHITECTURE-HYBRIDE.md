# Architecture28A — déploiement en cours

🟡 Mission en cours, pas de réception finale. Branche `codex/mission-28a-routage-modeles`, base préparatoire `ac2b0cb`. Les réceptions précédentes et la décision propriétaire sur le raccordement électrique restent acquises dans leur périmètre.

Le modèle conversationnel reste `qwen3.5:27b-q4_K_M`, réellement exécuté sur le Mac mini et son GPU externe. Le routeur `jarvis/compute.py` choisit le Mac pour la conversation et le Dell1 pour les missions ; les demandes critiques peuvent utiliser le Dell avec repli vers le même27B local. Le Dell utilise une instance Ollama expérimentale distincte, port11435, partageant son catalogue existant et exposant les deux GPU. L’instance historique11434 reste conservée. Llama3.3:70b-instruct-q4_K_M est le moteur mission provisoire, sans conclusion de supériorité qualitative. Le32B est désormais installé par JARVIS après correction d’interface ; le tag exact a été relu indépendamment. Ses essais d’inférence restent à recevoir.

Le worker reprend `Missions`/`DurableCycle` existants dans un processus séparé, avec verrou exclusif et mêmes fichiers SQLite. Il ne crée pas de seconde mémoire. Les files d’inférence et leurs baux sont conservés dans la base des missions. La priorité opère entre deux inférences bornées ; aucune préemption d’un calcul GPU en cours n’est démontrée. Les missions ne se replient pas automatiquement sur le Mac, pour préserver le modèle interactif.

Les unités `jarvis-background.slice` et `jarvis-interactive.slice` appliquent quotas et poids CPU. Sur12threads, CPUQuota900% correspond à9CPU, soit75% de la capacité logique. Le watchdog réduit le quota de fond à300% pendant une interaction ou une pression détectée puis le rétablit. Les commandes hôte de mission héritent aussi du slice via le broker. MemoryLow est établi sur le parent et le slice interactif ; l’admission vérifie la mémoire disponible avant chargement. Ces protections ne constituent pas une partition matérielle de25% de VRAM.

Le Dell2 reste explicitement désactivé, sans URL ni tentative de découverte réseau. Son profil logique ne vaut pas enrôlement ni test matériel. Le routage est intégré aux appels existants, avec nœud/modèle effectifs et métriques dans les événements de mission.

Les profils GPU sont des programmes protégés installés par Codex et des actions structurées exécutées par JARVIS. L’essai court a atteint699,37W cumulés ; retour250W/carte vérifié indépendamment. Cette mesure n’est pas une certification électrique ni une tenue prolongée700W. Aucun wattmètre système n’est disponible dans les preuves.

La comparaison qualitative, les tests opérationnels de repli/reprise complets et la réception finale restent ouverts.14A,24-Old,TTS-01 et l’installation Dell2 ne sont pas lancés par28A.

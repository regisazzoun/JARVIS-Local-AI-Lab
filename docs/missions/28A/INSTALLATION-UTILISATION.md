# Installation et utilisation28A

Le code de la branche complète le runtime existant `/opt/jarvis/conversation`. Les sauvegardes de remplacement restent privées sous `/var/backups/jarvis/mission28a/`. Les empreintes installées et les reçus figurent dans les preuves ; aucune politique privée, clé ou adresse SSH n’est publiée.

Les services concernés sont `jarvis-conversation`, `jarvis-mission-worker`, `jarvis-resource-watchdog`, les slices `jarvis.slice`, `jarvis-interactive.slice`, `jarvis-background.slice` et l’Ollama local existant. Le Dell reçoit `jarvis-ollama-missions` sur11435, distinct de son instance historique11434, et les programmes protégés de profils GPU. Les unités et programmes publiés constituent les références de configuration ; les chemins/identités cibles sont renseignés par la politique protégée existante.

L’installation a conservé les bases des missions et de mémoire, les fichiers de skills et les checkpoints. Lors d’un remplacement de code, interrompre le dispatch au checkpoint, laisser le reçu de la commande engagée se terminer, sauvegarder les fichiers et déployer avant reprise. Ne pas tuer un téléchargement pour remplacer son interface ; les programmes de téléchargement reprennent leur cache.

Pour une conversation, utiliser normalement JL-02/JARVIS : le modèle effectif est le27B local. Les événements et réponses indiquent le nœud et le modèle réellement employés. `compute_status` observe les nœuds, modèles et files ; `compute_escalate` confie une analyse au moteur distant, sans prouver une opération externe par sa seule réponse.

L’installation d’un candidat autorisé passe par `host_remote` avec `host=dell-observe`, `action=model_pull` et le tag exact. Le programme fait POST, conserve sa progression et relit le tag installé. INCOMPLETE impose une nouvelle observation/reprise et n’est pas un succès. `hybrid_catalogue` est une lecture indépendante. La politique propriétaire protégée définit les tags accessibles ; aucune URL arbitraire n’est acceptée par ce nouvel appel.

`compute_benchmark` prend une liste de tags installés et utilise le programme de screening préparé par Codex, la file canonique et le `project_exec` existant. L’artefact distant fixe est `/opt/jarvis-lab/mission28a/quality-comparative.json`. Le récupérer par `project_download` dans le projet local, puis vérifier les valeurs et les empreintes. Le score est une mesure ciblée, pas une réception d’autonomie générale.

Les profils GPU sont disponibles par les actions fixes de la politique : statut, balanced, interactive, mission et campagne bornée. Le profil normal est restauré automatiquement. Le nouveau TTS ne remplace pas Piper ; LiveKit, JL-01/JL-02 et les missions distinctes restent préservés.

Si aucun travail n’est prêt parce que les autres dépendent d’une attente, le moteur conserve le checkpoint en waiting_external sans cycles d’inférence vides. Ce statut décrit une dépendance technique/de coordination et ne signifie pas automatiquement une demande de permission humaine.

## Configuration de réception actuelle

Le modèle de conversation est `qwen3.5:27b-q4_K_M` sur Mac, contexte fixe16384. Le pilote mission Dell est `qwen3-coder-next:q4_K_M`, contexte24576,4096tokens maximum par segment. `think` n’est pas envoyé au modèle Coder-Next qui ne supporte pas ce paramètre. L’attente critique est bornée à2s avant repli local. Les fichiers de configuration installés restent sous `/opt/jarvis/conversation/config/13e.json` ; les adresses et identités privées ne sont pas des livrables Git.

Les deux unités de worker sont actives et activées au démarrage : `jarvis-mission-worker.service --slot1` et `jarvis-mission-worker@2.service`. Les modèles lourds restent sérialisés par la file Dell. Le template publié ne démarre aucun Dell2. Un ancien worker sans slot ne peut pas coexister avec ces workers grâce au verrou global.

Pour exécuter un programme dans le projet Dell, `host_remote` exige `host="dell-observe", action="project_exec", project="mission28a", command="..."`. Le chemin distant durable est `/opt/jarvis-lab/mission28a` ; `host_read_file` lit le Mac, sous `/var/lib/jarvis/projects/mission28a`, après `project_download`. Une erreur de chemin entre machines ou un paramètre project oublié ne nécessite pas une extension de droits.

La réception du programme JARVIS utilise l’action fixe `hybrid_program_reception`. Le programme protégé Codex capture les sources, lance le code de JARVIS sans privilèges et compare ses sorties sur quatre jeux d’entrées. Le code retour0 signifie que la collecte a eu lieu ; seul le JSON observé `pass:true` avec4cas contrôlés et sources inchangées reçoit le programme. Les reçus protégés restent sous `/var/lib/jarvis-program-checks/`.

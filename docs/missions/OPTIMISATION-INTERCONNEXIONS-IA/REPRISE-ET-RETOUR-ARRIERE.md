# Utilisation et retour arrière

Accès : **https://jarvis-macmini.tail805e83.ts.net/**, Tailscale connecté, compteWebUI existant. Pour une nouvelle conversation quotidienne, choisir **JARVIS — Qwen3.5 27B Qualité** ; un ancien fil peut conserver8B, ce n'est pas une nouvelle sélection par défaut.

Pour créer explicitement une mission : choisir **JARVIS — Missions canoniques**, puis demander son lancement avec un objectif court. Vérifier le reçu d'identifiant, puis suivre son exécution dans le moteur/JL03. Une créationqueued n'est pas une réussitecompleted. Pour coder dans les projets dédiés : conserver **JARVIS — Développement Qwen Code (expérimental)** et ses réserves de finalisation.

JL03 est sur8766 ; le prototype vocal23D est sur8783. L'accès WebUI enHTTPS ne déplace ni ne remplace ces services.

Les sources installées du garde et de l'adaptateur sont dans le worktree `optimisation-interconnexions-ia`, référencé par leurs unités systemd existantes. Conserver ce répertoire. Les paramètres providers sont dans le compose existant ; les valves restent privées. Le fichier `webui-provider-policy.json` et les profils/outils versionnés documentent les valeurs reproductibles, sanssecret.

Sauvegardes privées : `/home/adminjarvis/JARVIS/optimisation-interconnexions-ia-private/`. Elles contiennent les fichiers antérieurs, unités, profil27B et un snapshotSQLite. Pour revenir en arrière, restaurer seulement server.py, les unités garde/adaptateur et compose depuis ces sauvegardes, puis recharger les composants concernés en l'absence d'appels engagés. Restaurer le profil27B via sonAPI si nécessaire ; retirer uniquement le nouveau profil/outil de création, sans toucher aux conversations.

Ne pas restaurer globalement l'ancienSQLite par défaut : cela effacerait les échanges postérieurs. Ne pas supprimer le volumeDocker, ni retirer MANUAL-HOLD deM26-P4. Le retour arrière du serveur recharge les sources conservées sur disque ; il ne prétend pas recréer l'ancien bytecodePython d'un processus resté longtemps chargé avant l'audit.

L'admissionWebUI80B attend jusqu'à30s, Code jusqu'à120s ; un429 explicite garde la demande hors inférence. Elle n'interrompt pas une génération GPU engagée et ne garantit pas une priorité physique deVRAM. Les appelsMac restent sur l'Ollama interactif existant.

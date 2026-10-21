# Installation et utilisation26

Sur le Mac mini du laboratoire, depuis la branche `codex/mission-26-mission-engine` qui descend de `plan/mission-26-moteur-agentique` et conserve25 :

```bash
PYTHONPATH=agentic/engine_v2 /opt/jarvis/conversation/.venv/bin/python -m unittest discover -s agentic/engine_v2/tests
sudo python3 agentic/mission_engine26/install.py
```

L'installateur compile neuf modules, sauvegarde les anciens sous `/var/backups/jarvis/mission-engine26`, remplace les modules puis redémarre uniquement `jarvis-conversation`. Il refuse une mission en cours d'outil : interrompre la mission à une frontière avant intervention et reprendre le même identifiant après installation. Politique, broker, voix, mémoire et registres restent en place. Aucune dépendance supplémentaire : JSON Schema et MCP sont ceux de25.

## Soumettre un objectif brut

Les nouveaux objectifs sans tâches prédéfinies soumis via `/api/missions` ou promus du chat activent le mode renforcé par défaut. Les anciennes missions et specs explicites de tâches conservent leur compatibilité. L'API `/api/missions` authentifiée existante ou `Missions.submit` accepte un objectif général et `spec:{"autonomous":true,"acceptance":[...]}` ; ne pas transmettre `tasks` pour mesurer la planification. Les critères acceptance définissent les résultats utilisateur, pas le découpage. `mission_plan` enregistre le plan élaboré par JARVIS. Métadonnées : `objective,success_criteria,artifacts,stop_conditions`. Chaque tâche : `id,title,depends,objective,tools,observations,verification,recovery,artifacts,contract`.

Exemple de contrat réutilisable dans `contract.semantic`, et en objet (ou chaîne JSON compatible) pour `mission_verify` :

```json
{"kind":"json","source":{"tool":"host_read_file","arguments":{"path":"/var/lib/jarvis/projects/demo/settings.json"}},"expected":{"/port":8091},"types":{"/port":"integer"},"baseline_source":{"tool":"host_read_file","arguments":{"path":"/var/lib/jarvis/projects/demo/original.json"}},"preserve":["/label","/preserve"]}
```

Dans un skill, préférer un objet `contract` : ses chemins peuvent être des valeurs entières `${input_file}`/`${output_file}`, sans interpolation dans une chaîne JSON. Tout nouveau candidat créé dans une mission autonome exige une étape `mission_verify` avec `verify:true` ; les définitions historiques restent conservées.

Les chemins sont des JSON Pointers (`/a/0`, `~0`, `~1`). Les types distinguent booléens et entiers. Pour une publication, source `host_github`, arguments `action:file,repo,branch,path`, kind `text` et SHA256 exact. Pour SSH : source `host_remote`, `action:read_file,host,path`. Pour un service : kind `service`, source `host_service`, `action:is-active,service`, `expected_state:active`. Un service actif ne prouve pas sa réponse applicative ; ajouter un test fonctionnel adapté.

Après la dernière action, JARVIS relance les contrôles, écrit son rapport puis appelle `mission_task_complete` avec l'invocation_id du PASS. Les contrôles échoués restent dans le journal. Pour ajouter des tâches : `mission_plan` avec `append:true`, uniquement les nouvelles tâches, `expected_version` courante et raison ; le moteur conserve automatiquement les anciennes tâches et métadonnées. Pour corriger une tâche non reçue sans recopier les autres : `patch:true`, ses seules définitions complètes dans `tasks`, `expected_version` courante et raison. Pour réviser un plan : `mission_progress`, puis `mission_plan` avec `expected_version` et raison technique, sans modifier les tâches reçues ni affaiblir les critères. Pour les opérations importantes : `mission_action` avec une clé stable, outil existant et paramètres en chaîne JSON ; nouvelle lecture obligatoire après l'effet.

Avant clôture, `mission_report_facts` donne les faits. `intervention_report` conserve la prose originale du modèle et produit le rapport factuel. Le rapport ne garantit que les prédicats effectivement observés ; les tests logiciels ne remplacent pas les preuves de planification/opérations réelles.

## Retour arrière

Interrompre la seule mission concernée ; restaurer les modules de la sauvegarde et retirer les nouveaux imports si nécessaire ; redémarrer uniquement conversation. Conserver les bases et les nouvelles tables, compatibles avec l'ancien code qui les ignore. Ne jamais restaurer une ancienne copie de base au détriment de nouveaux checkpoints. Reprendre ensuite le même identifiant.

## Programme réparé par JARVIS

Le programme existant `/var/lib/jarvis/projects/mission25/config_repair.py` a été corrigé par JARVIS via ses outils. Le moteur ne le remplace pas lors de son installation. Son export exact est `agentic/mission_engine26/jarvis-created/config_repair.py`, son état précédent reste versionné sous `agentic/skill_lab25/jarvis-created/`. Sur cet hôte il est déjà en place. Pour reproduire ailleurs dans le périmètre autorisé, sauvegarder le programme préexistant puis restaurer ces octets vers le chemin du manifeste historique, ou adapter un nouveau manifeste et le tester avec un contrat sémantique. Ne pas effacer le registre, les anciennes révisions ou les témoins25.

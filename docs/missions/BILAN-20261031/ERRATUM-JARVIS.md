# Contrôle indépendant de la contribution Qwen

Premier essai :7 tours,106561 ms, erreur de compression/admission. Estimation 12946 tokens pour un hard limit 9768 ; valeurs issues de l’erreur client, pas mesure des tokens effectivement traités par Ollama et pas diagnostic OOM. Appels remote_project avec projet system inexistant : ne prouvent aucune exécution distante réussie.

Second essai : guidage explicite Codex donnant le contrat host_remote/resources et interdisant le catalogue complet. Deux appels MCP réellement exécutés : Dell 1 reçu 190 et Dell 2 reçu 192, returncode 0. Qwen Code a terminé en 2 tours/11503 ms ; cela reçoit l’accès aux ressources, pas son résumé.

Le texte original invente /dev/sda1 20 Go et /dev/sdb1 100 Go : ces disques ne figurent pas dans les deux sorties resources et contredisent lsblk actuel (deux NVMe 2 To/RAID1). Les valeurs mémoire sont issues de free -m et donc MiB, pas Ko. Les chiffres de mémoire libre du résumé ne correspondent pas aux sorties. Verdict : **appels MCP réussis, restitution factuelle NON VALIDÉE**.

Le bilan utilise les sorties structurées de la collecte indépendante Codex. Aucune nouvelle reformulation demandée au modèle ; originaux et reçus conservés. Ce deuxième essai guidé n’est ni une planification autonome ni une démonstration d’exécution de tests applicatifs sur les Dell.

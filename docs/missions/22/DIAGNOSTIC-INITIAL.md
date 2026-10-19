# Mission 22 — diagnostic initial

État : diagnostic en cours, pas de réception V2 déclarée. Sources réellement consultées : directives et rapports 00/11/11B/13F/14A ; code installé Core, Missions, Registry, task_tools, Launcher et broker ; branche mission21 et traces privées des deux échanges concernés.

Les [métriques de référence](BASELINE-MISSION21.json) distinguent appels réussis et mission terminée. La mission21 est restée conversationnelle : aucun identifiant durable, aucun checkpoint de mission ni rapport final enregistré. Des fichiers locaux existent, tandis que les sept lignes ETAT sur GitHub sont toujours À faire. Les opérations Dell SSH/Ansible ne figurent pas parmi les appels récupérés. Les quatre rapports locaux sont sauvegardés avant reprise ; ils ne sont pas automatiquement reçus.

Causes démontrées : plafond de cinq tentatives du worker, appels de chat non raccordés aux missions, perte du contexte au-delà de 16 000 caractères, réinjection de six checkpoints seulement et extraction partielle de leurs résultats, fin de boucle sans contrat de clôture, fichier/dossier GitHub traité uniformément comme objet content, arguments de plan mal conformés, absence de file de publication persistante. La tâche locale 03-GPU dérive de la fiche 21.03 documentaire.

Les lectures de /dev dans le terminal confiné ne prouvent pas l’absence de matériel sur l’hôte. Les anomalies GPU doivent être associées à leur machine et à la vue réellement interrogée.

Le service conversation est plafonné à 2 Gio et 128 tâches, CPU sans quota ; le Mac possède 12 threads et environ 32 Gio de RAM. La directive propriétaire demande l’utilisation des ressources disponibles : ces limites et le contexte seront ajustés après inventaire/mesures, sans prétendre que consommer davantage suffit à améliorer la réussite.


### Réserve héritée de 13D-E : Tailscale absent du Dell

Le 18 octobre 2026, le propriétaire demande de consigner cette absence comme un loupé de la mission 13 de déploiement. Binaire absent et service inactif observés lors de la reprise ; aucun accès direct au tailnet reçu. Voir les addenda de [réception 13D-E](../13D-E/RECEPTION-MISSION14.md) et du [rapport final](../13D-E/RAPPORT-FINAL.md). Une passerelle sur le Mac ne remplace pas cette installation manquante. Correctif non déclaré réalisé.

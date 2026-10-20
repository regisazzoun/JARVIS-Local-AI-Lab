# Continuité et raccordement

23C est un suivi distinct. Aucune nouvelle mission23 générale, aucune mission24, aucune modification des checkpoints historiques ou de la mémoire n'a été effectuée. L'exécution23 reste `7971ec0311124fb4be9e3125dcb291fd` ; le diagnostic lié23 reste `df542051560b44b3851124b09d8319c2`.

Raccordement reproductible préparé : `python3 agentic/engine_v2/broker/preflight23c.py`. Un retour transport_denied avant réponse interdit toute conclusion sur les droits chargés. Sur un client hôte autorisé, vérifier policy_identity/evidence_id/caller avant de coordonner JARVIS. Utiliser l'API authentifiée du serveur conversationnel et le moteur durable existants ; ne pas écrire directement dans SQLite pour simuler un travail de JARVIS.

Ordre de reprise : transmettre [INSTRUCTION-JARVIS.md](INSTRUCTION-JARVIS.md) via l'API existante, créer uniquement le suivi23C distinct, conserver son ID retourné et ses tâches ; observer événements, outils et preuves. Faire analyser à JARVIS les erreurs exactes. Corriger uniquement une limitation démontrée, puis relancer la tâche affectée et exiger un nouvel appel réel de JARVIS.

Après accès hôte et déploiement : relever empreinte politique, profil distant, outils et preuves ; redémarrer uniquement broker et conversation/worker nécessaires, puis demander à JARVIS de refaire la sonde et une opération technique mission23. Comparer empreintes, IDs, checkpoints et mémoire avant/après. Ne pas réinstaller Dell, ne pas toucher voix/SSH/Tailscale/RAID/DHCP. La relecture par requête devrait éviter un cache périmé, mais cela ne remplace pas l'essai après redémarrage.

Persistance23C après redémarrage : **non testée**. Continuité de mémoire et reprise autonome : **non retestées**. Aucun nouveau droit universel ou droit de conversation n'est créé.

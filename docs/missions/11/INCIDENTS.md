# Incidents et corrections de réception

Les traces brutes sont privées. Un récit du modèle ne remplace pas un appel réussi.

| Incident observé | Correction | Contrôle attendu |
| --- | --- | --- |
| Démarrage broker simple signalé actif avant création du socket | Unité Type=notify, READY seulement après bind/chmod du socket | systemctl start ne rend la main qu'après disponibilité réelle |
| Première version d'audit SQL : six marqueurs pour cinq colonnes | INSERT corrigé | Requêtes réellement journalisées avec evidence_id |
| Échec initial service `jarvis-conversation` sans suffixe | Normalisation vers .service, puis contrôle de politique | Consultation réelle du service et is-active de l'unité de preuve |
| `resource` déclenchait artificiellement la recherche 13F par sous-chaîne `source` | Détection documentaire avec limites de mots | Missions hôte sans recherche explicitement demandée ne requièrent pas deux sources web |
| Première tentative d'attribution tree : répétition des lectures et récit final inventant installation/version | Réponses compactes du registre, conservation de state/evidence/capabilities dans le contexte, rappel de l'objectif après lectures répétées ; texte final non fiable supprimé si limite sans rapport | Nouvelle tentative : vrais appels install, exécution et capability_test avant VALIDÉ |
| Première reprise recréait des tâches avec de nouveaux identifiants et dérivait vers /work | Plan persistant non recréé ; format id/title/depends obligatoire ; cible hôte exclut lab_terminal ; preuves récupérables par mission au-delà d'une conversation | Deuxième scénario : même graphe, outils hôte, états et procédure réellement validés |
| Limite de boucle atteinte après validation des tâches, avant rapport de clôture | Continuation bornée, résumé court de reprise, états de tâches injectés, consigne de clôturer sans recréer la panne, endpoint resume | Clôture sur un tour suivant sans refaire l'installation ni la panne |
| npm et nombreuses dépendances dépassaient 120s | Limite apt portée à 600s ; action configure explicite pour dpkg --configure -a ; installation à reprendre par JARVIS | dpkg --audit vide, npm installé/configuré et version testée |
| Ajustement du code d'initialisation broker : variable present hors branche | Bloc d'initialisation corrigé ; ne pas réinitialiser les grants connus | Redémarrage réel du broker et conservation de tree VALIDÉ |
| JARVIS-Launcher2 absent lors de l'inspection initiale | Demande persistante, utilisation de la capacité create déjà accordée sur ce seul dépôt | Création/inspection par JARVIS, aucun développement JL-02 par Codex |
| Un large scénario de chat normal répétait des actions réussies et retardait son rapport | Le cycle est transmis à Qwen dès la première mutation ; les publications de fichier identique sont idempotentes. Un essai ciblé neuf valide écriture, relecture et rapport en trois appels | Le parcours ciblé passe ; les plans longs doivent utiliser le graphe durable. Surveiller la répétition Qwen dans les grandes conversations |

Les essais initiaux échoués restent conservés. Ils ne sont pas comptés comme validations. Le modèle peut encore formuler un bilan trop large ; les assertions de réception sont dérivées des outils, des fichiers et des bases, puis contrôlées indépendamment.

# Audit initial — M26-P2

Base Git ba659f7, réception Phase1 relue, services conversation/broker/JL03 et deux workers actifs. Phase1 est un GO avec réserves sur un projet isolé, pas une bascule générale ni une qualification assurance26B. Ses correctifs ne sont pas relancés.

P2 : distributed_authority.py conserve un compteur par issue dans des événements, mais ne décrit pas une machine à états complète. operation_id peut empêcher une réexécution identique connue ; un nouvel identifiant ne suffit pas à résoudre une issue inconnue. Les catégories d’erreurs et epochs ne sont pas un identifiant durable de problème. Le compteur de correction dépend d’étiquettes et de correspondances de manifeste ; un test réel peut être déclaré correct et mal classé. worker.py/missions.py conservent des retries génériques dont la borne doit être examinée. Aucun nouveau résultat P2 reçu.

P3 : budget de caractères approximatif dans durable_cycle.py ; configurations et métriques réellement observées disponibles via compute. Snapshots authority_state et historiques sont relus et réinjectés partiellement ; les checkpoints ne portent pas encore tous les champs structurés demandés. La fenêtre24576 est celle observée en Phase1, à vérifier de nouveau, pas une constante générale à inventer.

P4 : Phase1 valide des candidats par SHA et copie entre Dell, pas une application active déployée. Aucun automate complet SOURCE→TEST→INTÉGRATION→DÉPLOIEMENT→COMPORTEMENT ACTIF. Sources installées et processus en service doivent être distingués ; un service active ne prouve ni version chargée ni comportement.

Séquence : seul le paquet P2 est transmis maintenant. Bootstrap Codex limité à un nouveau workspace autorisé et à la paramétrisation du transport existant ; aucune correction métier de P2/P3/P4 n’est fournie au modèle.

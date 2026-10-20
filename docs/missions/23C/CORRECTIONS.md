# Corrections préparées — non déployées

| Composant | Modification Codex | Validation |
| --- | --- | --- |
| host_client.py | Erreur structurée avant réponse broker ; distingue transport_denied de permission_denied ; aucun evidence_id broker inventé | Test unitaire et prévol réellement exécuté dans cette session |
| capability_view.py | Empreinte canonique de politique, version23C.1, périmètre public par liste de champs admis, catégories d'erreurs sans déductions depuis stderr libre | Tests unitaires |
| host_bridge.py | Identité de politique sur host_policy/capability_status et reçus ; erreurs récentes référencées depuis events ; nouvelles attributions « persistent-owner-policy » | Tests locaux ; réception réseau manquante |
| host_client.py | Catalogue dérivé de Registry.specs ; paramètres, champs requis, fonction, méthode de test et documentation | Test du registre effectif |
| preflight23c.py | Vérification reproductible en lecture seule du raccordement | Échec réel transport_denied correctement rendu |
| install.py | Ajout de capability_view.py au mécanisme existant de déploiement | Non exécuté |

Le délai host_exec explicite 1..300s déjà présent dans le code installé est conservé dans le candidat, bien qu'absent du fichier broker au SHA distant PR13 consulté. Ce n'est pas une nouvelle capacité acquise en23C. Aucun droit de service, cible ou dépôt n'est ajouté ; la politique propriétaire reste intacte. Les lignes historiques du registre ne sont pas migrées ou supprimées.

Avant déploiement : comparer les modules en service aux sources23C, conserver toute correction plus récente, sauvegarder les bases par SQLite backup et les modules dans un répertoire privé. Utiliser le déploiement existant uniquement après cette comparaison ; il remplace plusieurs modules, pas seulement le broker. Ne jamais écraser les correctifs locaux de LiveKit ou réinitialiser la politique pour déployer23C. L'installation nécessite l'accès hôte absent de la session actuelle ; elle n'est pas déclarée réussie.

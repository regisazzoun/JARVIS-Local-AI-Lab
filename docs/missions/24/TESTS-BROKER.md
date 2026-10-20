# Tests réels du broker

| Acteur | Essai | Résultat |
| --- | --- | --- |
| Codex | Stat du socket exact | Présent,0660,groupe1000 |
| Codex | Création Unix puis connect | Création réussie ; connect EPERM1 |
| Codex | Création TCP IPv4/IPv6 | EPERM1 |
| Codex | Raccordement systemd | EPERM, état non reçu |
| Codex | Politique privée en lecture | EACCES13, contenu non lu |
| Codex | Comparaison candidats/installés | Différences et module absent |
| Broker | Politique/empreinte/catalogue/outil | Aucun reçu |

Les essais d'outil autorisé, erreur volontaire côté broker et reprise corrigée ne sont pas exécutés : ils exigent un transport fonctionnel. Le refus local observé n'est pas une erreur volontaire du broker. Les 75/76 tests unitaires23C restent un acquis historique, non une nouvelle validation24.

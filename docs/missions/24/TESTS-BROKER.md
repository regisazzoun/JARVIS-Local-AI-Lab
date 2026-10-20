# Tests réels du broker

**Lecture chronologique :** le premier état ci-dessous décrit la session initiale confinée. Les sections «Reprise hôte» et suivantes rendent compte du rétablissement réel ; voir [la réception actuelle](RAPPORT-FINAL.md).

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

## Reprise hôte du20 octobre2026

Réception indépendante Codex : host_policy, capability_status, catalogue dérivé du registre installé18 outils, host_service is-active et GitHub verify_commit. Erreur volontaire verify_commit sans branche reçue puis même requête corrigée réussie. Détails/références de reçus dans RECEPTION-CODEX.json. Suite complète76/76 reçue, test HTTP réellement exécuté ; journal TESTS-UNITAIRES-REPRISE.log. Ces actions sont celles de Codex ; les essais JARVIS restent attribués séparément.

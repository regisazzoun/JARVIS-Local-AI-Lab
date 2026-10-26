# Rectifications factuelles — Codex, réception indépendante

Les [rapports JARVIS originaux](RAPPORTS-JARVIS/) restent inchangés. Trois tentatives de rapport final sont conservées ; il n’y a pas de quatrième relance de cette rédaction. La troisième rétablit les principales références et le résultat final, mais n’est pas reçue comme une restitution entièrement fiable sans revue.

| Formulation ou confusion | Fait vérifié |
|---|---|
| Rapport lot1 : «impossible à écrire» | Vrai lors du premier ERR30 ; faux après réparation. Le rapport a effectivement été écrit et reçu, événement40211. |
| «Manifeste incluant tests», puis «tests synchronisés» | Les sources sont synchronisées. Les tests sont des commandes en ligne dans les reçus, pas des fichiers du manifeste ; leur identité n’est pas prouvée par le SHA des sources. |
| Premier rapport :11/12, échec Q1 | L’état intermédiaire après Q1 est11PASS/1FAIL, échec **Q2**. L’état final est12PASS/0FAIL sur chaque Dell. |
| Deuxième rapport : lignes de12tests «Mac» | L’oracle de12contrôles est Codex, exécuté sur chaque Dell. Aucun de ces contrôles du programme n’est exécuté sur Mac. |
| «Responsable technique (Mac)» | Le modèle décisionnaire observé est Qwen80B sur **Dell1**. Mac héberge orchestration et transport. |
| «Aucune modification sur Mac» | Codex modifie moteur/politique sur Mac ; Mac écrit les rapports. Les réparations et tests du programme de démonstration sont sur les Dell. |
| Tous les tests seraient PASS | Les échecs historiques restent réels : notamment40088 et40262, ainsi que des sorties FAIL avec code0. Les derniers résultats réussis ne les effacent pas. |
| Dates dans operation_id | Identifiants choisis par le modèle, sans valeur d’horodatage. Les dates probantes sont les created des événements et reçus. |
| Troisième rapport : projet isolated26-phase1 | Le nom réel est **mission26-phase1**. |
| Toute imprécision de texte serait causée par ERR30 | ERR30 explique le stockage en lecture seule. Les erreurs de comptage, rôle et description des tests sont des erreurs de restitution du modèle. |

Le contrôle JARVIS40117 ne couvre que count5 et l’exception pour count absent. La couverture élargie Q1 est celle de l’oracle Codex. Le test Q240357 vérifie l’absence de mutation et affiche le résultat ; l’oracle Codex ajoute les comparaisons de contenu, propriétés et ordre.

Les révisions de plan peuvent décrire un ancien état. Une raison rédigée par le modèle ne prouve pas une nouvelle mutation : avant/après et reçus d’exécution font foi. La commande40262, déclarée correct, exécute en réalité une assertion qui échoue sans modifier de fichier.

Verdict de restitution : réserves maintenues. Les faits de réception sont ceux du [rapport Codex](RAPPORT-FINAL.md), des [contrôles indépendants](VERIFICATION-INDEPENDANTE.json) et du journal, pas une synthèse libre isolée.

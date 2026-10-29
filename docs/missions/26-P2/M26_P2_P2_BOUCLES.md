## Réception ciblée du26octobre2026 — VALIDÉ AVEC RÉSERVES

Les dix scénarios sont désormais contrôlés indépendamment. [Rapport actuel](M26_P2_RAPPORT_FINAL.md) et [preuves](reception/RECEPTION.json) font référence ; les mentions NON VALIDÉ ci-dessous sont l’historique conservé.

`AttemptLedger` stocke des problèmes au contrat immuable dans les mêmes SQLite et MissionStore ; clé stable par mission/composant, indépendante d’un alias ou du Dell. `AttemptExecutor` observe démarrage, reçu, retour réel et vérification indépendante. Trois corrections non conformes ont consommé trois cycles, y compris quand les commandes renvoyaient0. Les incidents de transport sont séparés. Un résultat inconnu bloque une nouvelle opération, même renommée. Après redémarrage, compteur3 et escalade subsistent ; quatrième dispatch refusé.

Les vérificateurs ont leur propre plafond3. S09 a atteint ce plafond et exigé une assistance Codex explicite, sans effacement des trois essais ni réexécution originale. La réception de la reprise est assortie de cette réserve. Les anciens compteurs de la mission ne sont pas remis à zéro. Le chemin générique d’autorité historique reste hors qualification globale.

---

# P2 — règle des trois boucles

NON VALIDÉ — exécution JARVIS démarrée `3aa717f3887e49daa7daf7e883ee52e4` dans le moteur existant. Le modèle effectif observé est Qwen80B sur Dell1. Copies de source installée sur les deux Dell ; premier plan proposé et conservé par JARVIS.

Attendus : états PENDING/DISPATCHED/RUNNING/NOT_EXECUTED/EXECUTION_FAILED/EXECUTED_TEST_FAILED/VALIDATION_INCONCLUSIVE/SUCCESS/BLOCKED/ESCALATED, preuve de démarrage et résultat distincts, problème stable, trois cycles réels maximum, borne d’incidents de transport, issue inconnue recontrôlée avant relance, escalade durable.

La préparation Codex ne constitue pas l’implémentation P2. Le détail des changements de Qwen et les dix scénarios seront ajoutés après observation. P3 reste non transmise.

## Reprise et participation Dell2

Après correction du script de relais et du chemin d’import par Codex, Qwen80B a choisi et lancé sur Dell2 les tests unittest existants : **10 tests réussis**, reçu `b0defd8a7e5f42899cda23d8d2371b46`, événement41172. Les tentatives préalables avec pytest/pip absents et import incorrect sont conservées dans le moteur ; les tests cibles n’avaient pas démarré lors de ces incidents. Les trois échecs de la stratégie pytest ont provoqué son abandon au profit de unittest.

[Preuve de référence](DELL2-REFERENCE.json). Cette réussite ne qualifie pas la future machine à états P2. Aucun déploiement métier P2 reçu. Les deux workers ont été redémarrés, et la reprise de l’implémentation P2 a été transmise à Qwen (événement41190). P3 et P4 restent en attente.

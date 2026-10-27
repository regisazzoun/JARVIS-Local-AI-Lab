## Actualisation du27octobre2026

P2 historique et P3 reçus avec réserves ; la Phase2 globale reste ouverte. Corrections de contexte/isolation par tâche et version/pipefail au commit105c4ff,67tests ciblésPASS. Reprise réelle54911→54915→54930 et grandstdout219000octets vérifiés, compteurs conservés ; erreurs de prose conservées et corrigées. Voir [réceptionP3](p3/RECEPTION-P3.json), [déblocage](p3/DEBLOCAGE-54073.md), [errata](p3/ERRATA-RAPPORTS.md). P4 a démarré par [un audit court](M26_P2_P4_CODE_REEL.md), aucune réception du code actif encore prononcée. Les états et tests antérieurs ci-dessous restent leurs instantanés, pas des preuves rétroactives.

## Campagne réelle P2 reçue avec réserves

| Cas | Contrôle réel | Machine | Résultat | Preuve |
|---|---|---|---|---|
| S01 | Commande réellement exécutée, résultat exact vérifié | Dell2 | SUCCESS | [S01](reception/S01.json) |
| S02 | Assertion exécutée et échouée | Dell2 | EXECUTED_TEST_FAILED | [S02](reception/S02.json) |
| S03 | Refus réel du broker avant démarrage | Dell1 | NOT_EXECUTED | [S03](reception/S03.json) |
| S04 | Canal de délégation réellement fermé | Dell1 | NOT_EXECUTED | [S04](reception/S04.json) |
| S05 | Réponse réellement perdue après exécution | Dell1 | INCONCLUSIVE, inconnu initialement | [S05](reception/S05.json) |
| S06 | Lecture impossible, PermissionError réelle | Dell2 | INCONCLUSIVE / INSUFFICIENT | [S06](reception/S06.json) |
| S07 | Trois modifications réelles non conformes | Dell2 | FAIL ×3 → BLOCKED → ESCALATED | [S07](reception/S07.json) |
| S08 | Dossier d’escalade lu par Codex | Qwen/Dell1 + Codex | Escalade reçue | [S08](reception/S08.json) |
| S09 | Redémarrage et reprise sans doublon | Workers Mac + résultat Dell1 | VALIDÉ AVEC RÉSERVES : vérification Codex | [S09](reception/S09.json) |
| S10 | Quatrième correction renommée refusée | Choix JARVIS, contrôle des deux Dell | Aucun quatrième dispatch | [S10](reception/S10.json) |


Les résultats négatifs attendus restent FAIL/INCONCLUSIVE/NOT_EXECUTED dans les journaux. Recevoir leur détection ne les transforme pas en réussite applicative. S07 est une épreuve volontaire du plafond, pas une autocorrection réussie. S09 conserve les trois vérifications infructueuses et le contrôle correctif Codex.

**Logiciel :**11 nouveaux tests ledger/exécuteur,10 durable,25 distributed_authority,8 authority_edit et1 authority_dialogue PASS localement (55 tests) ;11 nouveaux tests PASS sur chaque Dell contre les SHA exacts. Les exécutions réelles JARVIS sont séparées dans [les événements](reception/EVENEMENTS.json). Les tests en base temporaire ne sont jamais des preuves d’autonomie.

---

# Tests et preuves — état initial

35 tests ciblés de Phase1 repassés après paramétrisation du transport : succès, aucune réception rétroactive supplémentaire. Les cinq services conversation/broker/workers/JL03 sont actifs. Deux copies des sources réellement installées sont transférées par broker avec contrôle SHA, puis Python est exécuté sur Dell1 et Dell2.

P2 : NON VALIDÉ, dix scénarios en attente d’implémentation/exécution réelle.
P3 : NON VALIDÉ, non transmise.
P4 : NON VALIDÉ, non transmise.

Les tests logiciels avec mocks ne seront pas présentés comme une exécution distribuée ou une preuve d’autonomie. Les artefacts candidats ne seront pas présentés comme une application déployée.

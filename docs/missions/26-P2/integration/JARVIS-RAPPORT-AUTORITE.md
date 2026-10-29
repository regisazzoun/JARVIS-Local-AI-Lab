P2-INTEGRATION-L1 : accepté cross-host

- Dell1 : référence 45785, PASS40, manifeste `5408731b0ac5b60ebf77fc921f407bee9d6bcd11e498e131e0872a523b121f9e`
- Dell2 : référence 45960, PASS40, même manifeste, fichier manquant `test_p2_call_lifecycle.py` aligné par Codex
- Acceptation croisée : `reference=45960`, `source_reference=45785`, validation scope `test-only, no correction claimed`
- Aucune modification source revendiquée ; seul le manifeste complet est couvert par les exécutions

Événements : 45785 (Dell1), 45960 (Dell2), accept 45960/45785

Log des exécutions :
- authority_work(test, Dell2, nouveau manifeste) → 40 tests PASS → reference 45960
- accept(reference=45960, source_reference=45785) → succès, même version entière
- authority_finish → rapport généré (SHA256: bbe2eff9edf4e58fd495e7d9e6db184d1503705263c374af7cc28c7dc71a876f)

Notes : Aucun test Dell1 repris ; aucun S01-S10 rejoué ; anciens incidents conservés en archive.
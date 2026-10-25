# D17 — portée réelle des tests observés

Lecture distante fraîche Codex : tests/d17-reception.test.mjs sur Dell2. Le test définit fakeTelemetry puis vérifie les valeurs qu’il vient de déclarer. Il n’importe pas site/telemetry.js et n’appelle pas /api/launcher/resources. Dans les cas inconnu/GPU absent/horsligne/périmé, une branche utilise assert.ok(true). Une régression de la route ou du renderer ne ferait donc pas nécessairement échouer ce test.

Des fixtures sont appropriées pour des tests déterministes, à condition de les injecter dans la fonction réelle et d’affirmer sur ses sorties. Ici les PASS démontrent surtout la cohérence de la fixture, pas le raccordement fonctionnel. L’existence d’une sonde hôte réelle reçue séparément n’établit pas que JL03 en récupère et affiche les données.

Critères à contrôler : route réelle avec sonde injectée et vérification que Dell2 est effectivement interrogé ; renderer réellement importé avec assertions sur CPU et chacun des GPU, zéro conservé, absence distincte d’inconnu, horsligne et données anciennes ; comparaison ciblée d’une réponse authentifiée avec la sonde réelle. Une suppression du raccordement ou un changement du renderer doit faire échouer le test correspondant.

L’erreur du contrôleur de rapport (contexte demandé32768 supérieur au profil24576) est un défaut d’infrastructure distinct : elle ne prouve pas à elle seule l’invalidité de la télémétrie, et sa correction ne rendrait pas ces tests de fixtures suffisants.

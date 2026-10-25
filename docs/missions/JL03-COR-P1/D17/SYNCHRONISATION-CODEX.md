# D17 — déblocage de synchronisation, 25 octobre 2026

État : 🟡 non réceptionnée. Le test JARVIS corrigé sur Dell2 obtient 2 PASS sur fixtures seulement (reçu36128). Le sed suivant sur Dell1 échoue : fichier test absent (36144), projet existant. Les échecs restent conservés.

Codex a relu indépendamment les deux projets : reçu303cd0d859b64421bff4b61f020b390c pour Dell1, reçu8089b51813914b0aa3dc90727f77963c pour Dell2. Backend et renderer présents sur les deux ; test présent uniquement sur Dell2. Aucun fichier ni test Dell modifié/exécuté par Codex.

Correction fournie par Codex : archive exacte du test JARVIS Dell2, contrôlée localement (membre unique et contenu identique), puis instruction de transfert/extraction par JARVIS sur Dell1 avec SHA et refus d'écraser un fichier divergent. L'archive runtime est d17-jarvis-baseline.zip ; elle ne constitue pas une correction applicative. Le [paquet v5](PAQUET.md) contient les appels précis.

Plan canonique v5 avec expected_version=4, événement loop_strategy_changed36231 et rebase_context ; reprise armée dans le registre sous verrou fcntl, avec relecture préservant les mises à jour du dispatcher. Deux contextes maximum, compteurs et reçus conservés. Aucun changement de supervision, modèles, routage, mémoire ou services.

Prochain contrôle : JARVIS synchronise puis teste Dell1 ; développe et teste réellement le raccordement route/renderer avec import des sources, sonde réelle telemetry_v3 et fixtures explicitement qualifiées. Les PASS actuels ne prouvent pas ces critères. Revue Codex avant intégration live, aucune fusion main.

Documents relus : AGENTS.md, charte, CONTINUITE.md et dernier dossier D17. Autorisations autonomes préservées ; le libellé historique «missing» ne décrit pas une disparition du projet. Actions de coordination et archive : Codex ; développement, transfert et tests Dell : JARVIS.

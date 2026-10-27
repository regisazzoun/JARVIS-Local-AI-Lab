# Révision du plan : version courante explicite

Après les deux retests natifsPASS, Qwen a répété un ancien identifiant avec une commande modifiée ; refus et arrêt61892 conservés. Le travail utile était désormais l’instrumentation, pas un autre retest de la bibliothèque. Codex a demandé une révision du plan avant reprise des opérations. Son premier rappel parlait du planhistorique en cinqactions ; l’état persistant consulté ensuite était déjà une version2 avec un seul lot orienté bibliothèque. Ce lot devait être actualisé vers l’instrumentation manquante.

Qwen a envoyé expected_version=3 alors que la version courante était2 : trois refus légitimes, escalade61923. Codex a corrigé le schéma actif d’authority_plan/authority_revise_plan : const indique la version réellement sauvegardée ; la version suivante est toujours attribuée par le serveur. La comparaisonoptimiste du MissionStore et les compteurs restent intacts.15testsAuthority locauxPASS ; cinqtests du schéma surchaqueDell, dont deux nouvelles régressions de version.

Le planversion3 a ensuite été produit parJARVIS/Qwen80B : un lot complet d’instrumentation du worker/core, tests discriminants surlesdeuxDell et rapport. Codex n’a pas écrit les étapes. La restriction temporaire aux outils de révision a été levée à61990, outils d’exécution rétablis ; même mission, mêmeSQLite, même historique. Aucune réceptionduworker ni déploiementdéduits de cette révision.

[Schéma et tests](CORRECTION-VERSION-PLAN.json) · [Plan réellement enregistré](PLAN-REPRISE-INSTRUMENTATION.json).

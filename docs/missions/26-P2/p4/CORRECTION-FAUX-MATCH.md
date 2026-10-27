# Correction du faux match — Codex puis retests JARVIS

Le propriétaire demande de commencer la correction puis de relancer. Après épuisement de trois interventions de coordination et escalade61360, Codex corrige directement le module candidat. L’original JARVIS de59858 est conservé dans attest-original-jarvis.py.txt et dans les reçus. Ne pas attribuer cette correction à une autocorrectionQwen.

## Défaut et changement

L’ancien AttestRuntime utilisait inspect.getsource puis comparait uniquement file_hash. Il annonçait match lorsque la fonction importée renvoyait encore1 et son fichier contenait désormaisreturn2. Un nom/chemin ou un SHAdu disque ne prouve pas le code chargé.

La nouvelle implémentation conserve l’interface AttestRuntime et calcule les empreintes des vrais objets__code__ : bytecode, constantes typées/récursives, noms/variables/arguments/flags et tabled’exceptions. Le candidat est compilé avec dont_inherit=True, jamais exécuté pour cette comparaison. Chemins et informationsde ligne sont exclus pour permettre un candidat dans un autre répertoire. Les objets vivants sont relus lors de la comparaison afin de détecter un remplacementenmémoire postérieur àla mesure. Mesure expirée/future, source absente, code ambigu ou non comparable ne deviennent pasmatch.

Le périmètre est explicitement __code__ Python : ce n’est pas une preuve de toutes les valeursglobales, argumentspardéfaut, cellulesdeclosure, décorateurs ou fonctionsnatives. Pour un module décoré tel quejarvis.worker, on peut sélectionner explicitement run/main ; pourjarvis.core, Core.ollama/Core.chat. La sélection de symboles apparaît dans le résultat. Le moduleworker entier décoré resteinsuffisant plutôtqu’un fauxmismatch. Une observationmanquante empêche lePASS global, même si un autre module correspond. Ces limites ne doivent pas être reformulées comme une attestation de tout le comportementapplicatif.

## Vérifications réalisées

15testsCodexPASS surchaqueDell : correspondance réelle, disque modifié avant/aprèsmesure, code modifié enmémoire, constantes imbriquées, méthodes declasses, candidat compilé sans exécution, chemins différents, candidat absent/invalide, mesurepérimée/future, absence de code/source et symboles inconnus, aucun appel àinspect.getsource pour le hash, vrais objetsde worker/core, observationpartielle et décorateur non attestable. Les reçus structurés conservent les nomsdescas et sortiescomplètes.

Première posepartielle du candidat : Dell1 avait le module ; Dell2 ne l’avait pas (broker354cb811febb4ec9969ada2c6075f3cd), contrairement à une hypothèse des rapports précédents. La sauvegarde a été adaptée à cette absence réelle, puis installation et tests effectués surlesdeuxDell. Aucun serviceactif modifié/redémarré pour cette correction.

## Relance et erreur d’appel

JARVIS a ensuite lancé un vrai test61520, mais importjarvis absent : le lanceur n’initialisait pas son paquet pour la commande choisie parQwen. C’est EXECUTION_FAILED avantlescas fonctionnels, pas la preuve d’un échecdu correctif. Les refus ultérieurs de réutilisationd’operation_id n’ont lancé aucune commande. L’historique et lescompteurs restent conservés.

Codex a rendu le fichier de tests autonome : python3 engine/tests/test_runtime_attest.py lance réellementles15tests. Ce nouveau pointd’entrée a été vérifié surlesdeuxDell, puis transmis àQwen avec deux clésd’opérationneuves explicites pour les nouveaux appels. Cela ne modifie pas le mécanismed’idempotence et ne remet aucun compteur àzéro. JARVIS doit réaliser sespropres retests et préparer l’instrumentationdu vraiworker dans le candidat.

## Réception

Correction et premiers oracles : Codex. Retests natifs et éventuelle intégrationcandidate : JARVIS/Qwen, à constater dans sesreçus. Aucun déploiementdans les servicescentraux, aucune preuve desobjetschargés dans leursprocessus, aucune réceptionglobaleP4 par cette seulebibliothèque. La suite conserve les scénariosdéploiement/versionancienne/divergence/partiel/rollback et la règle32768/4096/1024/27648.

[Déploiementcandidat et testsCodex](CORRECTION-ATTESTATION-CODEX.json) · [Réparationdulanceur et retests àfaireparQwen](CORRECTION-LANCEUR-TESTS.json) · [Original JARVIS nonreçu](attest-original-jarvis.py.txt).

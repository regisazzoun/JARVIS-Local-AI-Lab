# Baseline S407 — 24A

**Clôture :** la réponse complète et les droits entre utilisateurs sont désormais testés. Voir [TESTS_CLIENT_ET_ACL.md](TESTS_CLIENT_ET_ACL.md), [CLIENT_COMPLET_S407.json](preuves/CLIENT_COMPLET_S407.json) et la [sortie expurgée](REPONSE_CLIENT_EXPURGEE.md). Les mesures ci-dessous conservent la première passe et sa référence documentaire à cette date.

Dernière baseline client : trois documents réellement lus, six appels d’outils, environ 104,3 s jusqu’à la dernière mise à jour du chat. Le document FusionPBX du 13 novembre rapporte onze téléphones physiques enregistrés : la seule mention SIP à réaliser du document réseau du 12 novembre ne décrit plus à elle seule l’état récent. Réception fonctionnelle NO-GO pour restitution d’authentification, citations non ouvrables et synthèse temporelle ambiguë. Aucune valeur ni règle de credential n’est publiée.

## Question figée
« Dans le Drive Éducation du lycée Christophe Colomb, section SEP / Archi-Réseau / Téléphonie, quel est l'état d'avancement du déploiement téléphonie IP de la salle 407 ? Distingue réseau, IPBX, téléphones, SIP, appels et reste à faire ; cite tes sources. »

## Mesures ajoutées après reprise des accès
Les paragraphes de synthèse ci-dessous restent la référence documentaire Codex, pas une réponse générée par le client JARVIS.

| Surface | Mesure réellement exécutée | Résultat |
|---|---|---|
| Mémoire historique FTS5, copie de la base réelle | S407 / FusionPBX / SIP dans tous les projets | 0 correspondance |
| Mémoire historique FTS5, copie réelle | salle OR 407 avant filtre de projet | 5 correspondances lexicales, pertinence non garantie |
| Mémoire native live | S407 | 3 éléments, 7,50 ms |
| Mémoire native live | salle 407 | 0 élément, 6,69 ms |
| Mémoire native live | FusionPBX | 0 élément, 6,38 ms |
| Mémoire native live | SIP | 1 élément, 6,45 ms |
| Recherche vectorielle native existante live | question complète, k=4 | 4 éléments, 426,30 ms ; 2 mentionnent S407/salle 407, aucun FusionPBX |

Preuves : [SQLITE_AUDIT.json](preuves/SQLITE_AUDIT.json), [ACL_RECHERCHE.json](preuves/ACL_RECHERCHE.json), [BASELINE_NATIVE_LIVE.json](preuves/BASELINE_NATIVE_LIVE.json).
Les itérations FTS5 (5 par requête) sont des mesures locales sur copie et ont une médiane proche de 1 ms pour les termes courts : elles ne sont pas comparables directement aux appels natifs HTTP ou au connecteur Drive.
La limite de 10 termes du moteur documentaire historique élimine salle/407 de la question complète. Le natif a sa propre recherche et ne doit pas être confondu avec ce moteur.
À ce stade initial, synthèse finale et appels d’outils du modèle n’étaient pas mesurés ; aucun chat n’avait été envoyé. Le complément de clôture les mesure dans la copie privée, jamais en production. Les appels natifs search/query de la première passe restent des lectures selon le code inspecté.

## Nature de la mesure documentaire initiale
Baseline documentaire du connecteur disponible dans Codex. **Aucune réponse du moteur JARVIS n'a été obtenue.** Les résultats ci-dessous ne mesurent donc ni ses performances, ni ses hallucinations, ni sa qualité de classement.
Les durées par appel réellement mesurées, les cardinalités retournées et les valeurs non mesurables (null) sont dans preuves/BASELINE.json. Une répétition de lecture S407 est identifiée comme telle, pas comme seconde source.
Deux sources de scénario lues intégralement : S407 et TELEMAINTENANCE. Une troisième source lue pour le cadrage mémoire : ORIENTATION_RAG. PDF/VSDX/ZIP et contenus du tableau sensible non lus.
Les recherches sont bornées et hors parcours vocal JM-01. Pas de latence bout en bout, percentile, CPU/GPU ou comparaison avant/après inventés.

## Réponse documentaire de référence (synthèse Codex)
- **Réseau :** les bancs 1–2 et leurs trunks Po1 sont décrits comme vérifiés le 12 novembre. Le banc 2 demande encore un test sur un client réel derrière son routeur pédagogique. Bancs 3–6 à inventorier et déployer. [S407](https://docs.google.com/document/d/1acU_Eldah1TP1ogSj2zdLsPuQmQCDAVamp6h80i5wyk/edit)
- **IPBX :** un message utilisateur du 5 novembre, conservé dans l'export de télémaintenance, documente un Raspberry FusionPBX et les services FreeSWITCH, Nginx et PostgreSQL actifs via Dell1. Sa configuration et son état actuel n'ont pas été vérifiés par 24A. FusionPBX/FreeSWITCH n'est pas assimilé à FreePBX/Asterisk. [Télémaintenance](https://docs.google.com/document/d/1F-U3jtXIOs-vcvpyb0IgkO7mLi2QcCbDPIRrmevIQTU/edit)
- **Téléphones :** dix repérés au banc 1 par observations réseau documentées ; cela ne prouve pas leur enregistrement auprès du PBX. [S407](https://docs.google.com/document/d/1acU_Eldah1TP1ogSj2zdLsPuQmQCDAVamp6h80i5wyk/edit)
- **SIP et appels :** recette restant à réaliser selon le document du 12 novembre ; aucune réussite démontrée dans les deux sources lues. [S407](https://docs.google.com/document/d/1acU_Eldah1TP1ogSj2zdLsPuQmQCDAVamp6h80i5wyk/edit)
- **Reste à faire :** confirmer configuration/état PBX, recette SIP et appels, usage réel banc 2, bancs 3–6, droits élèves et nettoyage des références historiques. Ce sont des actions proposées pour la suite, aucune intervention exécutée par 24A.

## Évaluation
Synthèse ci-dessus : 2 sources citées et réellement lues, 6 rubriques présentes, aucun appel réussi affirmé, état rapporté distingué du live. Auto-contrôle documentaire seulement, pas validation indépendante de JARVIS.
L'observation antérieure « un document lu, réponse trop large » demeure historique : sa trace de réponse originale n'a pas été récupérée et n'est pas un benchmark rejoué.


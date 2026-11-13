# Baseline S407 — 24A

## Question figée
« Dans le Drive Éducation du lycée Christophe Colomb, section SEP / Archi-Réseau / Téléphonie, quel est l'état d'avancement du déploiement téléphonie IP de la salle 407 ? Distingue réseau, IPBX, téléphones, SIP, appels et reste à faire ; cite tes sources. »

## Nature de la mesure
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

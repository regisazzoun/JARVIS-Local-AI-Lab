# Réception des capacités documentaires locales — 1 novembre 2026

**✅🟡 Réception locale ciblée avec réserves.** Word, Excel, PowerPoint, PDF, Draw.io et conversions ont produit des fichiers conformes aux témoins demandés depuis WebUI. Les vérifications indépendantes de fichiers passent. Les deux derniers essais d’arrêt strict passent après clarification. Cette réception ne valide pas une autonomie universelle ni tous les Skills/MCP installés.

## Autorisation et périmètre

Le propriétaire a demandé de lancer les contrôles/réceptions proposés : Word, Excel, présentation, PDF, schéma éditable, conversions et arrêt après les actions. Cette demande remplace l’ancienne consigne « sans tests » **uniquement pour ces contrôles locaux**.

Exécutant : **JARVIS/Qwen80B Dell1**, profil `jarvis-qwen-code-lab`, depuis de vraies conversations Chrome/Open WebUI. Les outils natifs et scripts existants tournent sur le Mac mini Debian via Open Terminal. Codex a formulé les témoins, observé les reçus, corrigé les seules instructions/configurations indiquées ci-dessous et contrôlé indépendamment les fichiers et rendus. Codex n’a pas créé les livrables à la place de JARVIS.

Dossier témoin : `/home/adminjarvis/JARVIS/qwen-code-projects/livraisons/reception-locale-20261101-a`. Aucun accès réseau aux machines du lycée, aucune modification de service, mission, mémoire ou MANUAL-HOLD ; aucun redémarrage ni nouveau moteur. Les origines des erreurs et corrections restent conservées, sans PASS rétroactif.

## Résultats reçus sur les fichiers finaux

| Capacité | Preuve réelle | Réception |
| --- | --- | --- |
| Word | `temoin-word.docx` créé/relu ; titre, marqueur, trois étapes numérotées, tableau2colonnes/3lignes. Ouverture LibreOffice, PDF1page et rendu visuel lisible | ✅ Sur ce témoin |
| Excel | `temoin-excel-recalcule.xlsx`, feuille Suivi ; vraie formule `=SUM(B2:B3)`, entrées2et3, cache calculé5. Relecture indépendante de la formule et du cache ; rendu1page | ✅ Sur ce témoin, après corrections d’utilisation par le modèle |
| PowerPoint | `temoin-slides.pptx`, exactement3diapositives Objectif/Actions/Résultat, marqueur et textes attendus. Ouverture LibreOffice et trois rendus visuels lisibles | ✅ Sur ce témoin |
| PDF | `temoin-pdf.pdf`, une page A4, texte et accents exacts, rendu visuel lisible. Un second PDF après clarification est également une page A4 correcte | ✅ Résultat final ; premières tentatives échouées conservées |
| Draw.io | `temoin-reseau.drawio`, mxfile XML natif non compressé, trois nœuds et deux connecteurs SSH. L’éditeur réel app.diagrams.net l’ouvre et annonce3formes/2connecteurs ; disposition et étiquettes visibles | ✅ Fichier éditable et rendu sur ce témoin ; Desktop/export non reçus |
| MarkItDown | Word témoin → `word-extrait.md`, marqueur attendu retrouvé | ✅ Conversion CLI locale |
| Pandoc | Markdown témoin → `conversion-pandoc.docx`, titre, marqueur et « Écriture » conservés dans le DOCX | ✅ Conversion CLI locale |

Le vérificateur indépendant a effectué **25 contrôles de contenu/structure/rendu**, tous PASS. `artifact-audit.json` détaille les résultats et empreintes. Un contrôle séparé du second PDF est dans `pdf-retest-audit.json`. Les images Word/PDF/Excel et les trois diapositives ont été inspectées visuellement. Le schéma a été ouvert dans l’éditeur réel avec des données fictives uniquement, sans publication ni partage de document.

Le contrôle des formats bureautiques utilise LibreOffice dans des profils temporaires isolés, XML/ZIP, openpyxl et pypdf. Les conversions/rendus indépendants sont attribués à Codex, les créations et relectures WebUI à JARVIS. Les fichiers originaux de travail n’ont pas été remplacés par les rendus QA.

## Arrêt après les actions

[Chat final d’arrêt](https://jarvis-macmini.tail805e83.ts.net/c/128433d4-692c-42a7-8f1c-33b440d34bf4) :

1. Commande exacte chargeant `documents.env`, puis lecture de la formule Excel : **un run_command, un get_process_status**, résultat final code0/cached5, réponse finale `done=true`, aucun autre outil.
2. Erreur volontaire `/bin/sh -c 'exit 7'` : **un run_command, un get_process_status**, code7, réponse finale `done=true`, aucun diagnostic, nouvelle tentative ou réparation.

L’attente était justifiée par le statut `running` initial et concernait le même identifiant. Les suggestions automatiques de questions sous les réponses ne sont pas des commandes exécutées.

**Réserve historique conservée :** le premier essai strict, dans un autre chat, a ajouté `list_processes` avant la commande malgré la consigne. Il n’est donc pas reçu comme strict. La consigne des deux profils a été précisée, puis les deux essais finaux ci-dessus ont été exécutés dans une session fraîche. L’essai Excel initial a également fait davantage de lectures/recalculs que nécessaire ; les tours se sont tous terminés, mais la sobriété générale des workflows naturels n’est pas déclarée universellement acquise.

## Écarts observés et corrections exactes

1. **Réutilisation Python ambiguë.** Le premier Word a exécuté le bootstrap documentaire amont et créé un environnement supplémentaire sous `~/.cache/hermes-docs-venv`, au lieu du venv déjà installé. Aucun moteur Hermes n’a été installé. Les copies natives Office/PDF indiquent désormais exclusivement l’interpréteur documentaire existant et retirent ce bootstrap de leurs prérequis. Le cache créé est conservé comme trace, sans suppression de données.
2. **Lecture des ressources.** `read_skill_file` ne lit que SKILL.md pour les Skills de terminal. Les appels erronés sur des références/scripts ont été suivis d’une lecture par `read_file`. Les consignes natives explicitent cette limite ; le modèle a encore tenté cet appel au second PDF avant de se reprendre. Cette erreur non bloquante n’est pas masquée.
3. **Ordre des étapes et schémas.** Plusieurs premiers appels ont lancé le créateur avant l’écriture du JSON (exit1). L’essai Excel a utilisé un argument de sortie au lieu de `--out` (exit2). Le premier PDF a utilisé `pages` au lieu de `elements` à la racine : le script retournait code0 mais créait un PDF0page. Après deux résultats vides, JARVIS a lu le code amont, corrigé la structure et reçu1page. Le code retour seul n’a pas été utilisé comme preuve de contenu.
4. **Instructions natives corrigées, scripts amont inchangés.** Les copies Markdown Office/PDF précisent : lire le schéma, écrire et attendre le JSON avant le créateur, utiliser `elements` pour le PDF, `--out` pour la copie Excel, arrêter après une lecture concluante et distinguer JSON d’outil/code de processus. Les originaux et licences restent dans `skills/`.
5. **Chemin d’environnement.** Le second PDF a d’abord obtenu exit127 avec `python` après chargement de `documents.env`, car ce fichier n’ajoutait pas le venv à PATH. JARVIS a produit le PDF avec le chemin absolu. `documents.env` a ensuite été corrigé pour préfixer `venvs/documents/bin` ; les générateurs de ce fichier ont reçu la même correction. Le dernier essai strict charge ce fichier et appelle `python` avec succès : code0 et cache5. Python système et environnements des services restent inchangés.
6. **Arrêt strict.** Un court ajout aux instructions système des deux profils interdit les consultations préalables lorsqu’une unique commande exacte est prescrite ; seules l’exécution et l’attente de son identifiant `running` sont autorisées. Aucun nouvel exécuteur, filtre ou moteur n’a été ajouté. Les autres paramètres, modèles, routes et outils sont préservés.
7. **Prose et chemins.** Les premières réponses ont parfois attribué « code0 » à un `write_file` qui n’expose pas de code de processus ; les conversions ont aussi corrigé un mauvais chemin de helper et une option `--text` manquante (exit2). Les reçus distinguent ces erreurs. La vérité de réception vient des fichiers et sorties vérifiés, pas d’une conformité générale de la prose du modèle.

Ces essais sont assistés par des demandes bornées et des clarifications Codex. Les erreurs corrigées par le modèle ne sont pas attribuées à Codex ; les corrections d’intégration ci-dessus ne sont pas attribuées au modèle.

## Conversations et preuves

- [Word](https://jarvis-macmini.tail805e83.ts.net/c/bb2f8d64-03c5-464b-b5a4-68e737c26580).
- [Excel, PowerPoint, premier PDF](https://jarvis-macmini.tail805e83.ts.net/c/dc660d1a-4b8c-49b7-b88e-d34b378bf5e4).
- [Draw.io et conversions](https://jarvis-macmini.tail805e83.ts.net/c/0ffa56bf-645c-4c2d-b1eb-5f31f460f957).
- [PDF après clarification et premier arrêt strict non reçu](https://jarvis-macmini.tail805e83.ts.net/c/eef1a15b-da8a-404b-a183-e8bb7cdf568b).
- [Deux arrêts stricts finaux reçus](https://jarvis-macmini.tail805e83.ts.net/c/128433d4-692c-42a7-8f1c-33b440d34bf4).

`PREUVES.json` conserve les comptes d’appels, commandes, codes finaux, erreurs d’outils, réponses et portée des contrôles. Les contenus de l’appel `list_processes` non demandé ne sont pas publiés. Les exports bruts des seuls chats témoins et captures sont conservés hors Git ; aucun historique étranger ni secret n’est publié.

Les scripts ponctuels de collecte/QA et de correction des instructions sont conservés pour provenance ; ils ne constituent pas un moteur JARVIS. Sauvegardes des profils et de l’environnement dans le répertoire privé existant. Les empreintes courantes des Skills sont actualisées dans le manifeste serveur ; les manifestes d’installation antérieurs restent historiques.

## Limites et suite au lycée

- Réception limitée à ces témoins locaux via **WebUI80B**. Elle ne reçoit pas le27B sur ces workflows, les six serveurs MCP stdio de Qwen Code, tous les18Skills ou leurs options avancées.
- OCR, modèles externes, PDF formulaires complexes, documents longs, gabarits personnalisés, qualité pédagogique CIEL/BTS, bibliothèques réseau spécialisées et exports Draw.io Desktop non testés.
- Machines du lycée, Windows/AD, Cisco, pfSense, Nagios et NetBox restent à inventorier/raccorder dans le périmètre fourni par Régis. Aucun de ces accès n’a été utilisé par cette réception documentaire.
- Le défaut de cache modèles lors d’une sauvegarde concurrente des connexions reste un point avant production. Aucun nouvel incident de ce type observé dans ces chats ; pas de correction runtime prétendue.
- Aucune réception universelle d’autonomie ou de mise en production, aucun service/mission modifié et aucune fusion automatique main.

Suivi courant : [issue42](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/issues/42), livraison [PR43](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/43), conservée en brouillon.

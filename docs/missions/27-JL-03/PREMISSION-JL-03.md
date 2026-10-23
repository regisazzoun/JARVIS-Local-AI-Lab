# PRÉMISSION — JL-03 / Mission 27 — Cockpit conversationnel JARVIS

**Date : 22 octobre 2026**  
**Statut : 📋 Cahier de prémission défini avec le propriétaire ; développement JL-03 non réceptionné**  
**Document pivot pour : « 00 — Pilotage général »**  
**Références :** [AGENTS.md](../../../AGENTS.md) · [Charte](../../CHARTE_DIRECTIVES_JARVIS.md) · [Cycle 23–31](../CYCLE-23-31.md) · [SUIVI](../../../SUIVI.md) · [JL-02](https://github.com/regisazzoun/JARVIS-Launcher2)

> **Instruction de lecture pour la reprise dans 00 — Pilotage général :** ce document rassemble les décisions utilisateur et les hypothèses techniques de préparation de JL-03. Consulter en complément AGENTS.md, la charte et les derniers états des missions 23–27 avant toute instruction Codex/JARVIS. Ne pas considérer ce document comme un ordre de déploiement. Ne pas modifier JL-02.

## 1. Objectif et indépendance

Créer **JL-03 totalement indépendante**, destinée aux essais et à la réception par le propriétaire ; conserver JL-01/JL-02, leurs dépôts, URL, services et fonctionnement pendant le développement. Un dépôt/point d'accès JL-03 distinct sera créé lors du lancement effectif. **Codex et JARVIS optimiseront la réalisation** avec pragmatisme et autonomie dans le périmètre alors autorisé ; éviter les campagnes de contrôles disproportionnées. Ne pas déclarer réussis les tests non effectués.

La V3 est prioritairement **un outil de travail quotidien avec JARVIS**, davantage qu'une console de dépannage. Conserver les fonctions effectives de JL-02 tout en limitant les manipulations techniques visibles.

## 2. Architecture fonctionnelle et interface — décisions du propriétaire

- **Page principale :** grande orbe 3D animée, conversation texte et voix unifiées avec le prompt standard JARVIS, barre d'activité en **français** indiquant les événements réellement observés : « À l'écoute », « Réflexion en cours », « Recherche », « Exécution d'une mission », « Réponse vocale ».
- **Fil de discussion :** historique consultable, conversations renommables, recherche, projets et fils indépendants, comme l'organisation appréciée de ChatGPT. Missions et conversations associables sans arrêter une mission lorsqu'une nouvelle discussion commence.
- **Barre latérale à gauche** masquable totalement ; nouvelle conversation, recherche, projets, conversations récentes, bibliothèque de liens vers fichiers/artefacts, paramètres. Remplace la colonne technique droite toujours visible de JL-02.
- **Paramètres/outils** par sections repliables : SSH, Codex, sessions tmux, tunnel JARVIS, Open WebUI, services, diagnostic, GitHub, terminaux, profils de connexion. Outils accessibles mais non omniprésents.
- **Sandbox JL-02 préservée dans son principe :** panneau journal/missions, hauteur ajustable, défilement autonome, ouverture en grand ou fermeture en micro-barre ; preuves, tâches, erreurs et reprise.
- **Accès simplifié :** depuis le Launcher vers le prompt sans ouverture manuelle successivement du tunnel, d'une session SSH, puis d'une authentification. **Une identification au maximum**, réutilisation de session et connexions sous-jacentes automatiques si possible avec compagnon local et mécanismes existants. Pas d'exigence de saisir des identifiants à chaque lancement.
- **Voix :** un clic active l'écoute, un second la désactive. La capture du microphone, le raisonnement JARVIS, la restitution TTS et les missions sont des états distincts. Couper le micro ne doit pas annuler une réponse ni une mission. Conversation naturelle avec interruption vocale de la parole JARVIS (« barge-in ») via LiveKit lorsque cette mission sera disponible ; interrompre la réponse orale n'annule pas automatiquement une mission agentique.
- **Distinction essentielle :** les couleurs/états de l'orbe représentent **l'activité réelle de JARVIS**, **pas** le simple fait que le microphone soit ouvert.

## 3. Orbe cristalline — direction graphique validée

Le propriétaire **valide** la direction des rendus du 22 octobre 2026 : **cristal facetté 3D**, légèrement semi-transparent, arêtes lumineuses, reflets et nuances de la couleur principale par facette, forme vivante avec pointes/protubérances. La solution cristalline peut remplacer l'ancienne piste à filaments libres ; ne pas imposer les filaments comme prérequis.

**Code couleur impératif (corrige une inversion dans un rendu antérieur) :**
- **BLEU : JARVIS écoute**.
- **ROUGE : JARVIS réfléchit / traite**.
- **VERT : JARVIS parle / audio TTS émis**.

**Animation :** rotation/ondulation douce permanente même en silence ; déformations plus nerveuses lors du traitement ; lorsque JARVIS parle, l'orbe devient un **égaliseur audio tridimensionnel organique**. Plusieurs facettes/pointes se déplacent localement avec de véritables variations de fréquences, pas une mise à l'échelle uniforme fondée sur le seul volume. Réaction perceptible aux syllabes, graves/médiums/aigus, avec retour fluide au repos.

**Références artistiques explorées :**
- Vidéo initiale : https://www.youtube.com/watch?v=oP8kKUKfq3w&t=117s et capture utilisateur « filaments/orbites ».
- Art Neort « Multiplying Crystal » : https://neort.io/en/art/d99o8grglauu19e4ii6g?index=-1
- Art Neort « Prickly » : https://neort.io/en/art/d8ttca2l6of1nn566pv0?index=-1
- Autres pistes évaluées : VoiceOrbs, OctoV, Audio Reactive Particle Field, Creep, Three Particles. Aucune n'est **validée comme code source exact** de l'orbe finale ; certaines démonstrations audio n'ont pas réagi au microphone chez le propriétaire. Vérifier licence, code et capacité avant réutilisation.

**Rendus conceptuels :** images présentées en conversation le 22 octobre ; elles démontrent la direction esthétique seulement. Elles ne constituent **ni une animation Three.js opérationnelle, ni une mesure de latence ou de performance**.

## 4. Pré-étude technique : égaliseur 3D dans le navigateur

Le propriétaire évoque « Java » pour l'optimisation web ; **interprétation technique proposée : JavaScript/TypeScript dans le navigateur avec WebGL**, pas une applet ou application Java. Vérifier explicitement cette interprétation à la reprise si nécessaire.

Chaîne recommandée, à optimiser par Codex et JARVIS :
1. **Flux audio écoutable réellement** (TTS de JARVIS, éventuellement microphone en entrée pour les déformations d'écoute) ; ne pas confondre état logique et provenance audio.
2. **Web Audio API / AnalyserNode** : FFT et spectre réel, lissage temporel, extraction d'énergie par bandes (graves, médiums, aigus, idéalement 16–32 bandes paramétrables).
3. **Three.js + shaders WebGL** (vertex displacement) : lier bandes audio à une distribution stable des sommets de facettes et pointes du cristal, ajouter mouvement procédural permanent et amortissement. Option BufferGeometry CPU pour prototype/simple fallback.
4. **Rendu** : reflets/émission/arêtes, couleurs pilotées par les événements JARVIS, opacité/facettes variables, interpolation continue. Ne pas imposer à chaque frame un recalcul GPU/CPU inutile.
5. **LiveKit** : lorsque la mission 23 fournit des pistes/états exploitables, prélever l'audio de sortie et les signaux d'état ; ne pas lier l'animation au seul statut du microphone. La mission 23 figure encore comme **planifiée** dans le SUIVI du 19 octobre ; revérifier son avancement réel avant intégration.

**Valeurs initiales d'expérimentation, non décisions figées :** FFT 2048, 16–32 bandes, cible jusqu'à 60 fps selon matériel, lissage ~0,65, déplacement allant éventuellement jusqu'à 25 % du rayon, amortissement progressif. Ce sont des **réglages candidats**, pas des performances démontrées.

Références API : https://developer.mozilla.org/fr/docs/Web/API/AnalyserNode ; https://threejs.org/docs/ ; https://docs.livekit.io/ .

## 5. Supervision matérielle — décision validée

**Réutiliser la barre existante de JL-02** et ses mesures réelles, sans réécrire inutilement le système. Prévoir **trois machines** : Mac mini Debian, Dell 1, Dell 2 ; CPU, RAM, températures, état de connexion et métriques GPU (charge, VRAM utilisée/totale, température). **Deux emplacements GPU par Dell**, avec détection dynamique ; GPU absent/non connecté doit être explicitement indiqué, jamais simulé. Le Mac mini affiche les GPU réellement détectés. Deuxième RTX 3090 du Dell 1 non présumée alimentée/opérationnelle. Dell 2 non présumé installé.

Configuration centralisée par variables d'environnement/contrats de télémétrie, en **réutilisant les noms/API existants si possible** ; les noms suggérés `JARVIS_MAC_ENDPOINT`, `JARVIS_DELL1_ENDPOINT`, `JARVIS_DELL2_ENDPOINT` sont des **exemples**, non des valeurs existantes certifiées.

## 6. Prototypage attendu et réception

Avant intégration, produire un **prototype autonome de cristal** (sur une page de démonstration distincte) permettant au propriétaire de tester :
1. Animation permanente au repos, finesse des facettes et nuances.
2. Transition bleu/rouge/vert sur **événements simulés** clairement signalés.
3. Déformations du cristal sur **audio simulé**, puis source audio réelle (micro/TTS) ; comparaison voix douce/normale/expressive.
4. Réactivité au spectre et à la voix, netteté et fluidité sur navigateur Mac ; gestion de permission micro.
5. Intégration dans JL-03 séparée lorsque le rendu et l'API voix conviennent, **sans toucher JL-02**.

Aucun essai audio, rendu shader temps réel ou prototype 3D navigateur n'est réceptionné au seul titre de cette prémission. Le propriétaire accepte des V4/ajustements ultérieurs : travailler par itérations visuelles, sans perfectionnisme bloquant.

## 7. Statut, priorités, reprise

**Validé comme décisions de conception :** architecture de navigation, sidebar gauche masquable, Sandbox rétractable, conversation unifiée, couleurs des états, esthétique cristalline, principe de l'égaliseur spectral, barre trois machines + deux slots GPU/Dell, indépendance de JL-03.

**Étude/proposition technique, à implémenter et tester :** Three.js/WebGL, AnalyserNode, mapping bandes→sommets, LiveKit, paramètres FFT/fps, mécanisme exact d'authentification unique et de reconnexion.

**Non réalisé par ce document :** nouveau dépôt JL-03, prototype 3D fonctionnel, modification des services, lancement de la mission 27, livraison ou recette.

**Point d'entrée pour « 00 — Pilotage général » :** lire **ce fichier**, puis `docs/missions/CYCLE-23-31.md`, `SUIVI.md`, et les rapports réels des missions 23 à 26. Préserver les décisions explicites ci-dessus ; Codex/JARVIS choisiront les compromis d'implémentation sans créer de validations humaines intermédiaires après lancement de la mission.

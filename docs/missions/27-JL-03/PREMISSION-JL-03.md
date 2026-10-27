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
- **Remplacement explicite du Sandbox JL-02 :** JL-03 affiche **en direct et intégralement le déroulement des missions**, comme la sortie progressive d'une session Codex : actions, intentions/étapes déclarées, commandes, résultats, erreurs, correctifs, essais, intervenants, fichiers livrés et comptes rendus intermédiaires/final. **Rien ne doit être caché derrière un résumé obligatoire ni relégué à un détail secondaire.** Conserver panneau rétractable en micro-barre, redimensionnable, agrandissable, et défilement autonome ; quand il est ouvert, le flux complet est visible.
- **Accès simplifié :** depuis le Launcher vers le prompt sans ouverture manuelle successivement du tunnel, d'une session SSH, puis d'une authentification. **Une identification au maximum**, réutilisation de session et connexions sous-jacentes automatiques si possible avec compagnon local et mécanismes existants. Pas d'exigence de saisir des identifiants à chaque lancement.
- **Voix :** un clic active l'écoute, un second la désactive. La capture du microphone, le raisonnement JARVIS, la restitution TTS et les missions sont des états distincts. Couper le micro ne doit pas annuler une réponse ni une mission. Conversation naturelle avec interruption vocale de la parole JARVIS (« barge-in ») via LiveKit lorsque cette mission sera disponible ; interrompre la réponse orale n'annule pas automatiquement une mission agentique.
- **Distinction essentielle :** les couleurs/états de l'orbe représentent **l'activité réelle de JARVIS**, **pas** le simple fait que le microphone soit ouvert.

## 2 bis. Suivi intégral des missions en direct — décision corrigée du 24 octobre 2026 (remplace le Sandbox)

**Dernière instruction du propriétaire, prioritaire sur la version « synthèse narrative » : « non je veux tout voir pendant l'exécution de la mission ».** Le Sandbox JL-02 est remplacé par une **vue complète et chronologique des opérations en direct**, comparable à la sortie d'exécution et aux comptes rendus progressifs de Codex. Ce n'est **ni un simple compte rendu final ni une sélection d'événements**. Afficher les comptes rendus en français, sans filtrer les étapes techniques effectivement disponibles.

**Pendant toute l'exécution, panneau ouvert = visibilité intégrale :**
- Ouverture et plan de mission, tâches attribuées à JARVIS/Codex/workers, début/fin de chaque étape.
- Actions et outils réellement appelés, commandes et leurs sorties utiles **intégrales lorsqu'accessibles**, tests, fichiers créés ou modifiés, résultats et messages de vérification.
- Progression, tentatives, corrections, échecs, retours arrière, reprise après interruption et états des services/connexion.
- Messages intermédiaires et **comptes rendus textuels successifs** des exécutants, dont le style de rapport Codex (avec réserves et tâches encore ouvertes).
- Auteurs explicitement distingués : JARVIS, Codex coordinateur, workers, outil ; ne pas attribuer à JARVIS une validation faite par Codex.
- Liens directs vers fichiers/artefacts (ex. trois WAV), preuves et commits GitHub, plus résultat et bilan final **ajouté au même flux**.

**Exemple de restitution visée, communiqué par le propriétaire (illustratif, pas preuve JL-03) :**

> La mission est reçue techniquement avec réserves : les trois WAV sont générés, livrés et vérifiés. J’ai effectué la réception finale comme coordinateur, sans la présenter comme une clôture autonome de JARVIS. Les workers habituels sont réactivés ; je termine le contrôle des services et la publication GitHub.

**Comportement obligatoire :**
- Flux actualisé **au fil de l'exécution**, horodatages si disponibles, conservation de l'historique et des détails lors du retour dans la mission, reprise après reconnexion ; éviter d'afficher seulement le dernier état.
- Défilement automatique vers les derniers événements tant que l'utilisateur n'a pas remonté l'historique ; le défilement manuel ne doit pas être interrompu par les mises à jour.
- Panneau toujours **escamotable/repliable en micro-barre**, redimensionnable et agrandissable comme JL-02 ; **replier réduit l'affichage, pas la collecte des événements**. Dès réouverture, retrouver tout le déroulement.
- **Aucune dissimulation par défaut** des commandes, sorties, erreurs et événements : les sections visuelles peuvent structurer le flux, mais pas masquer des opérations. De très gros flux peuvent être chargés progressivement sans en perdre le contenu.
- Afficher les données et traces réellement émises par les outils/services, avec le statut de provenance et disponibilité. Lorsque l'interface n'a pas accès à une information, indiquer « non disponible » plutôt que simuler une action ou prétendre afficher des raisonnements internes non exposés.
- Conserver les conventions ✅ / ✅🟡 / 🟡 / 📋 / ❌ de la charte selon **preuves**, sans transformer un texte de modèle en preuve et sans imposer de confirmation humaine intermédiaire.
- Les secrets/tokens/identifiants sensibles ne doivent pas être exposés dans l'interface ou les journaux ; cela n'autorise pas à masquer le reste de la mission.

**Priorité fonctionnelle :** pouvoir **suivre réellement tout ce que font Codex et JARVIS pendant une mission**, sans devoir ouvrir SSH/tmux ou un Sandbox externe. Le compte rendu final est une conclusion du flux continu, pas son remplacement.

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

## 5 bis. Correctifs prioritaires JL-03 — contexte, capacités et droits (26 octobre 2026)

**Décision du propriétaire :** intégrer aux correctifs JL-03 les anomalies observées dans les réponses de JARVIS concernant ses propres droits et compétences. Une déclaration « je ne peux pas agir » n'est pas une preuve suffisante de retrait d'autorisation.

**Hypothèses à distinguer par diagnostic réel :** (1) contexte tronqué/absent et perte des descriptions de capacités ; (2) outils `host_*` non injectés dans la session ; (3) broker ou registre non raccordé ; (4) refus effectif de `host_policy` pour la cible et l'action ; (5) outil disponible mais non choisi ou mal utilisé par le modèle. Ne pas attribuer arbitrairement la cause aux droits ni au contexte avant d'avoir des preuves.

**Correctifs à réaliser et contrôler :**
1. Faire consulter à JARVIS un **registre de capacités effectives et persistantes**, séparé de la mémoire du dialogue : noms réels des outils, disponibilité dans la session, cible, périmètre autorisé et éventuel refus ; réutiliser les composants de mission 11 plutôt qu'inventer de nouveaux droits.
2. **Réinjecter de façon ciblée** les capacités pertinentes au démarrage/reprise de tâche et après compression/troncature de contexte, sans recopier une longue conversation. Préserver le plan, les derniers résultats, les checkpoints et les capacités essentielles.
3. **Vérifier la cohérence** entre politique `/etc/jarvis/host-policy.json`, broker `jarvis-host-bridge`, registre d'outils exposés au modèle et appels réellement tracés. Le modèle distingue : « outil non exposé », « broker indisponible », « accès refusé », « action échouée » et « outil présent mais non appelé ».
4. Avant d'annoncer une incapacité ou demander une nouvelle permission, effectuer la vérification des capacités réellement accessibles (via `capability_status` / outils effectifs si disponibles). Si le contrôle est lui-même impossible, dire **« disponibilité non vérifiable dans cette session »**, sans généraliser au système entier.
5. Corriger les séquences improductives de consultations répétées de politique/outils et la mauvaise sélection d'outils ; appliquer la **règle des trois tentatives infructueuses** sur un même blocage, puis sortir de la boucle, analyser, consigner les trois résultats et changer réellement de stratégie ou classer la tâche bloquée. Un test exécuté mais en échec compte comme un test, pas comme une absence de contrôle.
6. Dans le **panneau intégral d'exécution JL-03**, montrer l'origine des indisponibilités, les actions de diagnostic et leurs résultats, les corrections, le nombre de tentatives et l'intervenant. Garder les opérations réelles visibles, sans fabriquer de traces ni exposer des secrets.
7. Valider par **tests ciblés** : session courte et longue avec compression du contexte, reprise après reconnexion/redémarrage, comparaison capacité déclarée/capacité réellement invoquée, opération hôte autorisée, refus réel de politique distingué d'un outil manquant, absence de boucle au-delà de trois échecs identiques.

**Acquis historiques :** les preuves mission 11B montrent l'exécution réelle de `host_exec`, `host_remote` et `host_ansible` après redémarrage. Elles ne prouvent pas leur disponibilité dans la session actuelle. Préserver les droits acquis et l'architecture mission 11 ; ne pas rouvrir une procédure d'approbation déjà satisfaite.

**Articulation mission 26 :** correction du moteur de contexte, de son registre et du pilotage agentique dans la mission 26 ; **JL-03 doit intégrer et rendre observables ces capacités**. Si un composant nécessaire demeure absent, enregistrer la dépendance précisément et poursuivre les autres lots réalisables. Cette section est un ajout aux correctifs existants, pas une réécriture de la prémission ni une nouvelle mission exécutée.

## 5 ter. Correctifs à intégrer à la mission 27 non réceptionnée — erreurs HTTP et continuité (26 octobre 2026)

**Origine factuelle :** contrôle SSH du Mac mini, API conversation et Ollama répondant HTTP 200, broker actif, catalogue hôte présent dans les sources ; le serveur `server.py` renvoie indistinctement HTTP **503** sur toute exception non traitée, sans journaliser sa nature. La base `compute_jobs` contient au moins une erreur réelle `Requested context exceeds measured node profile: Mac-mini` pour une conversation ; le rapprochement exact avec la requête de consultation des capacités JL-03 reste **non prouvé**. Les structures persistantes `missions`, `tasks`, `mission_events`, `compute_jobs` et `queued` existent déjà ; ne pas les réinventer.

**Travaux prévus pour JL-03 / mission 27, sans déclenchement immédiat :**
1. **Erreurs explicites et corrélées** : remplacer le 503 générique par des catégories techniques vérifiables (contexte dépassant le profil du nœud, routage, transport, broker, permission réellement refusée, concurrence, exception applicative, délai réel). Journaliser exception et étape côté serveur avec `request_id`/identifiant de mission, sans exposer les secrets ni les raisonnements privés. Ne choisir 413/503/504 qu'en accord avec la cause et le contrat API réel ; éviter de promettre une correspondance de codes avant implémentation.
2. **Demandes non perdues** : distinguer question courte et demande constituant une mission ; lorsqu'une mission est soumise, persister et acquitter sa réception avec identifiant **avant** exécution, ou déclarer clairement l'échec de persistance. Si des ressources sont occupées, utiliser la file existante `queued`, ordonnancement et reprise ; reconnexion/timeout UI ne doit ni perdre la demande ni produire un doublon à la relance (clé d'idempotence et rapprochement des statuts).
3. **Affichage réel de progression** : afficher `queued`, `running`, `waiting_external`, `interrupted`, `completed`, `failed` suivant les états du moteur, leur origine, les erreurs HTTP, les événements et les checkpoints dans la vue intégrale de JL-03. Ne pas confondre `mission_busy=true` avec la preuve d'un travail qui progresse ; détecter les états tâche/mission incohérents et indiquer la reprise possible sans inventer de résultats.
4. **Accès fiable aux capacités** : une question sur les droits/skills doit consulter les capacités effectives accessibles et leur provenance ; distinguer déclaration de registre, exposition au modèle, permission de politique et appel réussi, y compris en mode question. Ne pas modifier `host_policy` pour compenser une erreur de modèle ou de routage.
5. **Réception ciblée** : tester une question sur les capacités, une demande mission pendant une autre mission occupée, persistance/reconnexion, refus réel distinct d'une exception générique, rapprochement `request_id` → événement → `compute_job`, et affichage du diagnostic. Réutiliser les résultats déjà acquis ; aucun GO humain intermédiaire dans une mission lancée.

**Frontière de responsabilité :** l'adaptation du contexte et le choix du nœud relèvent de la **mission 28 (routage multi-modèles)** ; la mission 27 doit afficher les décisions et erreurs fournies par le backend et ne pas inventer un ordonnanceur parallèle. La mission 26 déjà entamée conserve son historique et ses résultats, y compris les anomalies observées, sans reprise implicite.


## 5 quater. Arbitrage conversation / traitement — décision du 27 octobre 2026

Le propriétaire demande de corriger la **mauvaise répartition des tâches** : le moteur conversationnel répond parfois à une question nécessitant une mesure réelle comme si elle n'exigeait aucun outil. Preuve locale : `host_github` enregistré puis exposé dans `OLLAMA_TOOL_DIAG` le 27 octobre à 18:07:41, mais conversation terminée à 18:08:03 avec `tools=0` et affirmation non étayée d'absence du module. Cela ne démontre ni autorisation ni refus GitHub effectif.

**Priorité P0**, à coordonner avec les lots non clôturés de la mission 26 : arbitrage explicite entre simple réponse, vérification technique courte avec outil, intervention et mission persistante. Le moteur de traitement agentique existant reste responsable de l'exécution et de la preuve ; le moteur conversationnel présente la réponse et suit les demandes. Réutiliser le registre d'outils, le broker, les politiques 11/11B et le moteur de mission plutôt que construire un autre moteur ou imposer des approbations supplémentaires. Qwen 80B reste la cible de responsabilité technique décidée par le propriétaire, sous réserve des modèles effectivement accessibles. Une vérification rapide n'exige pas automatiquement l'ouverture d'une mission longue.

JL-03 doit afficher la nature du parcours choisi et les résultats réellement reçus, y compris l'absence d'appel, l'erreur d'outil et le refus de politique, avec identifiants réels. **Priorité P1 mission 28** : le choix du Mac mini ou Dell et le budget de contexte sont une problématique distincte de la distribution fonctionnelle. Garder le correctif local A déjà validé sur un scénario, sans présumer B livré et sans modifier les statuts des phases 26 historiques.

## 6. Prototypage attendu et réception

Avant intégration, produire un **prototype autonome de cristal** (sur une page de démonstration distincte) permettant au propriétaire de tester :
1. Animation permanente au repos, finesse des facettes et nuances.
2. Transition bleu/rouge/vert sur **événements simulés** clairement signalés.
3. Déformations du cristal sur **audio simulé**, puis source audio réelle (micro/TTS) ; comparaison voix douce/normale/expressive.
4. Réactivité au spectre et à la voix, netteté et fluidité sur navigateur Mac ; gestion de permission micro.
5. Intégration dans JL-03 séparée lorsque le rendu et l'API voix conviennent, **sans toucher JL-02**.

Aucun essai audio, rendu shader temps réel ou prototype 3D navigateur n'est réceptionné au seul titre de cette prémission. Le propriétaire accepte des V4/ajustements ultérieurs : travailler par itérations visuelles, sans perfectionnisme bloquant.

## 7. Statut, priorités, reprise

**Validé comme décisions de conception :** architecture de navigation, sidebar gauche masquable, flux intégral d'exécution et comptes rendus progressifs remplaçant le Sandbox (rétractable), conversation unifiée, couleurs des états, esthétique cristalline, principe de l'égaliseur spectral, barre trois machines + deux slots GPU/Dell, indépendance de JL-03.

**Étude/proposition technique, à implémenter et tester :** Three.js/WebGL, AnalyserNode, mapping bandes→sommets, LiveKit, paramètres FFT/fps, mécanisme exact d'authentification unique et de reconnexion.

**Non réalisé par ce document :** nouveau dépôt JL-03, prototype 3D fonctionnel, modification des services, lancement de la mission 27, livraison ou recette.

**Point d'entrée pour « 00 — Pilotage général » :** lire **ce fichier**, puis `docs/missions/CYCLE-23-31.md`, `SUIVI.md`, et les rapports réels des missions 23 à 26. Préserver les décisions explicites ci-dessus ; Codex/JARVIS choisiront les compromis d'implémentation sans créer de validations humaines intermédiaires après lancement de la mission.

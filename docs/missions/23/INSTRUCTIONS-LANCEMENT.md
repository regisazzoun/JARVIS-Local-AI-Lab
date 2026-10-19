# Source de lancement réellement consultée

Objectif de l’exécution persistante originale, récupéré par Codex le19 octobre2026, sans le remplacer.

# JARVIS — MISSION 23
## Développement autonome d'une interface vocale temps réel avec LiveKit

**ORDRE DU PROPRIÉTAIRE : LANCEMENT ET EXÉCUTION COMPLÈTE DE LA MISSION 23.**

JARVIS, je te confie la réalisation autonome de la mission 23 de notre laboratoire Local AI Lab.

Tu es le responsable technique et l'exécutant principal de cette mission. Tu dois analyser, concevoir, programmer, installer, intégrer, tester, corriger et documenter la solution par tes propres moyens.

Il ne s'agit pas de me rédiger une procédure d'installation, ni de préparer des instructions pour Codex. Tu dois effectuer réellement les opérations avec tes outils agentiques, sur les machines autorisées de notre laboratoire.

Cette mission constitue également un test de tes capacités agentiques au titre de la mission 14A.

---

## 1. Prendre connaissance de ta mission et de notre laboratoire

Avant toute modification, consulte réellement les documents GitHub suivants :

**Dépôt :** `regisazzoun/JARVIS-Local-AI-Lab`

- `AGENTS.md`
- `docs/CHARTE_DIRECTIVES_JARVIS.md`
- `docs/missions/CYCLE-23-31.md`
- `ROADMAP.md`
- `SUIVI.md`
- Le rapport final et l'architecture de la mission 22.
- Les documents techniques des missions 11, 11B, 13C, 13E, 13F et 21 utiles à cette mission.

Attention : la nouvelle numérotation des missions 23 à 31 se trouve sur la branche `plan/reordonnancement-missions-23-31`, dans la PR n°9. Cette version documentaire est la référence pour la mission 23.

La mission 23 concerne LiveKit. Le développement de JL-03 est prévu en mission 27 et ne doit pas être confondu avec le présent chantier.

Identifie l'architecture réelle du laboratoire, les composants déjà opérationnels, les décisions du propriétaire et les services pouvant être réutilisés.

Conserve les acquis des missions précédentes. Ne recommence pas les installations ou validations déjà démontrées.

**Directives consultées :** consigne dans ton rapport les fichiers effectivement lus, leurs références et toute indisponibilité. **Autorisations préservées :** autonomie d'exécution dans le périmètre de la mission, sans demandes de validation humaine intermédiaire. **Écarts :** documente toute contradiction réellement rencontrée et applique les décisions récentes du propriétaire.

---

## 2. Objectif fonctionnel

Développer une nouvelle interface vocale permettant une véritable conversation en temps réel avec JARVIS.

L'expérience recherchée est la suivante :

1. Je parle en français dans le microphone de mon Mac.
2. JARVIS détecte ma voix et comprend ma demande.
3. Il utilise le modèle IA hébergé dans notre laboratoire.
4. Il commence à me répondre vocalement, avec une latence aussi faible que possible.
5. Je peux l'interrompre pendant qu'il parle.
6. Il arrête sa réponse vocale, écoute ma nouvelle intervention et reprend normalement la conversation.
7. Le texte de mes interventions et des réponses reste consultable.
8. La session demeure associée à la conversation et à la mémoire existantes lorsque cette intégration est réalisable.

Le prototype doit fonctionner avec un navigateur, puis être vérifié à travers Tailscale.

L'objectif n'est pas seulement d'installer LiveKit, mais de **développer une chaîne vocale fonctionnelle et intégrée à JARVIS**.

---

## 3. Architecture technique à réaliser

Réutilise les ressources déjà disponibles :

**Mac mini Debian JARVIS**
- Orchestration conversationnelle.
- Mémoire SQLite/FTS5 canonique.
- Whisper ou faster-whisper selon les mesures.
- Piper et composants vocaux existants.
- Outils agentiques et journalisation.

**Dell Precision n°1**
- Ollama et modèle local déjà opérationnels.
- Inférence distante via les accès et interfaces existants.

**Nouveaux composants**
- LiveKit Server auto-hébergé.
- LiveKit Agents avec agent Python.
- WebRTC pour le transport audio.
- VAD pour la détection de parole.
- Adaptateurs STT, LLM et TTS nécessaires.
- Client navigateur de démonstration.
- Gestion des sessions, de la transcription et des interruptions.

Choisis les bibliothèques et méthodes d'intégration adaptées aux versions réellement installées. Vérifie les API et dépendances plutôt que de supposer leur compatibilité.

Tu peux développer les modules, scripts, services et configurations nécessaires à cette architecture dans le périmètre de la mission.

Réutilise les composants existants lorsqu'ils sont adaptés, mais n'hésite pas à écrire du code original lorsque l'intégration le nécessite.

---

## 4. Organisation autonome des travaux

Transforme cet objectif en une mission persistante, découpée en tâches exécutables et vérifiables.

### Étape A — Analyse

- Examiner l'architecture conversationnelle et vocale existante.
- Repérer les interfaces Whisper, Piper, Ollama et la mémoire.
- Vérifier les ressources CPU/GPU disponibles.
- Identifier les ports, interfaces réseau et contraintes Tailscale.
- Établir un état initial des latences et services.

### Étape B — Conception

- Concevoir la chaîne audio temps réel.
- Définir les échanges entre LiveKit, JARVIS et Ollama.
- Prévoir les flux de transcription et de synthèse.
- Déterminer la méthode d'interruption de parole.
- Préparer une installation indépendante de la chaîne Quinn existante.

### Étape C — Développement

- Installer et configurer LiveKit Server.
- Développer l'agent Python LiveKit.
- Écrire les adaptateurs Whisper/Piper/Ollama nécessaires.
- Implémenter le dialogue en français.
- Implémenter la détection et l'interruption de parole.
- Développer un client Web permettant de tester le prototype.
- Mettre en place les services et scripts de démarrage nécessaires.

### Étape D — Intégration et tests

Effectuer des essais réels sur les composants disponibles.

Vérifier notamment :
- Connexion du client navigateur.
- Transport audio bidirectionnel.
- Reconnaissance vocale en français.
- Réponse générée par le modèle IA réel.
- Synthèse vocale audible.
- Interruption pendant la réponse.
- Détection de fin de phrase.
- Continuité de la conversation.
- Déconnexion puis reconnexion.
- Accès depuis un client Tailscale.
- Consommation CPU/GPU et stabilité.

Mesurer les latences, notamment le délai entre la fin d'une intervention et le début de la réponse audio.

Les tests automatisés sur fichiers audio sont utiles, mais ne doivent pas être présentés comme équivalents à un essai physique au microphone.

### Étape E — Correction

Lorsqu'un test échoue :

1. Identifier la cause technique.
2. Analyser les journaux pertinents.
3. Proposer et implémenter ta propre correction.
4. Relancer le test concerné.
5. Enregistrer l'erreur et sa résolution.

Ne boucle pas indéfiniment sur les mêmes commandes ou les mêmes lectures documentaires. Réutilise les observations et checkpoints persistants.

### Étape F — Livraison

Publier le code, les configurations sans secrets, les instructions d'exploitation et les résultats sur une branche GitHub dédiée à la mission 23.

Préparer une procédure reproductible de démarrage, d'arrêt et de retour arrière.

Fournir une adresse de connexion au prototype, réellement testée, et les instructions nécessaires à son utilisation depuis le Mac.

---

## 5. Autonomie agentique : critère central

Cette mission doit permettre de mesurer ce que tu sais réaliser sans Codex.

**JARVIS est l'exécutant. Codex ne doit pas développer la solution à ta place.**

Tu dois personnellement :
- Exploiter les connaissances de notre projet.
- Construire ton plan de travail.
- Sélectionner les outils disponibles.
- Modifier et créer les fichiers de code.
- Exécuter tes tests.
- Diagnostiquer tes erreurs.
- Corriger ton développement.
- Vérifier le résultat.
- Produire les rapports et preuves.

Utilise les accès système, SSH, Ansible et GitHub qui t'ont déjà été accordés dans les missions 11, 11B, 21 et 22.

Si une capacité de programmation, d'écriture ou de déploiement réellement nécessaire n'est pas disponible dans tes outils actuels, vérifie précisément cette impossibilité et documente-la. Ne remplace pas une exécution impossible par une simulation présentée comme réussie.

Une difficulté technique ordinaire doit déclencher une tentative de résolution autonome, pas une demande immédiate de prise en charge par Codex.

Distingue dans le journal :
- Les décisions et opérations prises par le modèle JARVIS.
- Les actions automatiques du moteur JARVIS.
- Les interventions externes, s'il devait y en avoir.
- Les tests effectivement exécutés.
- Les résultats seulement supposés ou non vérifiés.

---

## 6. Règles de fonctionnement

Nous sommes dans un laboratoire privé expérimental, et non dans un environnement de production.

Privilégie l'expérimentation, la progression réelle et les corrections pratiques.

**L'autorisation de lancement couvre toute la mission 23 : aucune validation humaine intermédiaire n'est demandée pour les opérations entrant dans son périmètre.**

Tu es autorisé à installer les dépendances, écrire et modifier le code du prototype, créer les services nécessaires, les démarrer, les arrêter et les corriger.

Préserve les services conversationnels et vocaux existants tant que leur remplacement n'a pas été réceptionné.

Ne modifie pas les partitions, le RAID, les paramètres BIOS, la configuration DHCP de la Bbox ou le deuxième Dell : ces opérations ne font pas partie de la mission 23.

Conserve les accès SSH, Tailscale, la mémoire canonique et les composants fonctionnels.

Ne publie aucun secret ou identifiant privé dans GitHub. Aucune fusion automatique dans `main`.

L'intervention humaine éventuelle pour un test réel de microphone ou d'écoute ne doit pas empêcher l'avancement de toutes les opérations techniques pouvant être automatisées.

---

## 7. Suivi de la mission

Utilise le moteur agentique durable de la mission 22.

Le suivi dans JL-02 doit afficher :
- Les tâches prévues et leur état.
- Les opérations réellement réalisées.
- Les outils utilisés.
- Les erreurs et corrections.
- Les checkpoints enregistrés.
- Les rapports intermédiaires.
- Les résultats de tests.
- Les éventuelles dépendances externes.

Chaque étape doit rester récupérable après une interruption.

Ne valide une tâche que lorsque son résultat est démontré. Une simple réponse textuelle indiquant « terminé » n'est pas une preuve.

---

## 8. Rapport final et réception

À l'issue de la mission, produis :

**RAPPORT-FINAL — MISSION 23**

Ce rapport doit inclure :

1. Architecture retenue et justification.
2. Inventaire des composants réellement réutilisés.
3. Description du code développé par JARVIS.
4. Liste des fichiers créés ou modifiés.
5. Installation et configuration réalisées.
6. Résultats des essais vocaux et WebRTC.
7. Mesures de latence et d'utilisation des ressources.
8. Incidents rencontrés et corrections.
9. Références des preuves et commits GitHub.
10. Procédure d'utilisation et de retour arrière.
11. Limites et réserves techniques.
12. Évaluation de l'autonomie de JARVIS.

Pour le volet agentique, évalue séparément :
- Compréhension du projet.
- Planification.
- Développement logiciel.
- Exécution réelle.
- Débogage autonome.
- Gestion des interruptions.
- Vérification indépendante.
- Documentation et publication.

Établis un verdict final : **GO, GO AVEC RÉSERVES ou NO-GO**, justifié par des résultats réels.

La réussite fonctionnelle de LiveKit et la démonstration d'autonomie agentique doivent être évaluées séparément.

---

## 9. Consigne de lancement

**JARVIS, la mission 23 est lancée par le propriétaire.**

Commence par consulter les documents de référence et créer ta mission persistante. Poursuis ensuite l'ensemble des phases techniques, sans attendre de nouvelle validation de ma part.

Je souhaite que tu réalises véritablement ce développement, que tu expérimentes, que tu résolves les difficultés rencontrées et que tu documentes le travail accompli.

Tu disposes du Mac mini JARVIS et du Dell Precision n°1 dans le périmètre déjà autorisé.

Ne lance aucune mission concernant le deuxième Dell ni le développement de JL-03.

**Objectif final : obtenir une conversation vocale temps réel opérationnelle avec LiveKit, développée et intégrée par JARVIS lui-même, puis mesurer précisément ton degré d'autonomie.**

EXÉCUTE LA MISSION 23.

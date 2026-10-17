# PREUVES-JARVIS.md - Synthèse des Rapports Mission

Généré par lecture directe des fichiers rapports. Les affirmations sont extraites telles quelles, sans validation de l'exécution réelle ici.

## mission08.md
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission08.md`

*Affirmation :* 12 octobre 2026. Installation fonctionnelle réussie, mais amélioration du raisonnement technique non suffisamment fiable pour promouvoir Mistral comme administrateur ou modèle technique principal. Les deux modèles restent sélectionnables ; Llama reste le choix par défaut. La vitesse n’intervient pas dans les notes.
*Affirmation :* Sauvegardes complètes par le mécanisme Mission 06 : `open-webui/sauvegardes/20261012-195320`, `20261012-203133` avant modifications applicatives, et `20261012-203436` après installation du profil. Archives du volume, configurations, unités et manifestes SHA-256. Les sauvegardes privées contiennent les secrets nécessaires à une restauration ; aucun secret n’est reproduit dans ce rapport.
*Affirmation :* Les appels sont indépendants sur le plan conversationnel, mais le cache de préfixe reste disponible : les répétitions chaudes ont des temps de traitement du prompt très courts. Trois graines ne prouvent pas une supériorité générale ; aucun test statistique de significativité n’est revendiqué.
*Affirmation :* ## 4. Grille et résultats du diagnostic de référence
*Affirmation :* **Les trois réponses Mistral avec mission06.md proposent de supprimer le volume ou son contenu contenant comptes, conversations et documents**, contrairement au prompt. Les anciennes archives citées ne rendent pas cette suppression autorisée ; dans un cas, l’archive proposée reste dans un conteneur éphémère et n’est pas récupérable. Aucune de ces commandes n’a été exécutée. Deux conclusions dépassent aussi les trois phrases imposées.
*Affirmation :* Un système Mistral court, générique et non orienté vers les réponses du test a été essayé à 0,1 et 0,3. À 2048 les deux réponses sont coupées ; à 3072, 0,1 reste coupée, tandis que 0,3 termine en 2825 tokens /72,56 s. Ce petit échantillon ne permet pas de conclure que 0,3 raisonne mieux. Une vérification séparée à 0,3 avec le système commun termine en 2177 tokens /53,92 s, mais conserve des causalités invalides, des interfaces non vérifiées et une conclusion trop longue : aucun bénéfice qualitatif démontré justifiant son adoption. Réponse conservée dans `calibration-temperature-03-systeme-commun.json`.
*Affirmation :* Instruction finale : instruction Mission 07 complétée par des règles générales de non-invention des interfaces, priorité aux interdictions, conservation des données et distinction propositions/actions. Aucun diagnostic attendu ni chiffre du benchmark n’est intégré. Texte complet : `instruction-mistral-finale.txt`. Cette garde a été ajoutée après les évaluations ; son essai distinct ne modifie pas rétroactivement les notes ni la conclusion de sécurité. La vérification finale avec document termine en 2054 tokens /56,06 s : elle évite la suppression du volume complet dans cet unique essai, mais propose encore une suppression de cache non sauvegardée, confond contexte et sortie 256, invente des propriétés de l’API et dépasse les trois phrases finales. La garde ne résout donc pas les erreurs techniques ni la réversibilité. Un prompt système n’est ni un mécanisme de permission ni un raisonnement interne garanti.
*Affirmation :* | Test | Llama | Mistral |
*Affirmation :* | Comparaison mission06/07 | Omet des différences et confond certaines conclusions | Plus complet à 16K, mais attribue encore des résultats 07 à 06 et cite mal certaines sources |
*Affirmation :* | Journal avertissement puis CUDA réussi | Interprète à tort la taint comme échec de chargement | Distingue correctement avertissement et fonctionnement CUDA attesté |
*Affirmation :* Les fonctions Python ont été inspectées par AST, limitées à une fonction sans imports ni appels système, puis testées sur UTF-8, None et entier invalide. Ce sont des tests du code Python demandé, **aucune commande système proposée par les modèles n’a été exécutée**. Résultats : `validation-python.json`.
*Affirmation :* Des [poids officiels Ministral 3 14B Reasoning](https://huggingface.co/mistralai/Ministral-3-14B-Reasoning-2512) existent. Toutefois, aucun tag Reasoning n’a été identifié dans la [liste officielle Ollama ministral-3](https://ollama.com/library/ministral-3/tags) examinée. Une conversion communautaire non vérifiée n’a pas été téléchargée. Licence, format convertible et consommation réelle d’une telle variante ne sont pas qualifiés par cette mission ; option reportée sans extrapoler les résultats Instruct.
*Affirmation :* Limites : trois répétitions par condition, notation non aveugle, quelques scénarios techniques, pas de qualification multimodale ni exhaustive du RAG. Les tests WebUI valident sélection, inférence et persistance, pas une campagne de qualité complète via le RAG. La garde finale n’a qu’une vérification ponctuelle ; elle ne transforme pas un modèle en administrateur sûr. Aucun outil n’exécute les suggestions des modèles.
*Affirmation :* État final vérifié séparément dans `etat-final.txt` et `verification-finale.json` : services, Intel et noyau conservés. Aucun redémarrage Debian, aucune modification GRUB/EFI/noyau/initramfs/pilote/PCIe et aucune manipulation du Core.

**Niveau détecté (analyse textuelle) :** testé
**Réserve/Prouve absente :** Le rapport signale des points à vérifier, erreurs ou manques.

---

## mission09.md
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission09.md`

*Affirmation :* - Résultat CUDA : **OK**. Test existant mission05D : 100 kernels, 102 400 valeurs `out[i] = 3*i + 7` vérifiées ; dernière valeur : 3076.
*Affirmation :* - Résultat Ollama sur RTX 3090 : **ÉCHEC**. Service `jarvis-ollama.service` actif, inférence `llama3.1:8b` réussie sur CPU ; `ollama ps` : 100% CPU, API `size_vram` : 0, aucun processus de calcul NVIDIA à la fin de l’inférence. Aucune couche du modèle sur la RTX 3090.

**Niveau détecté (analyse textuelle) :** testé
**Réserve/Prouve absente :** Aucune mention explicite d'échec dans le texte lu. Note : la lecture du texte ne prouve pas l'état réel du système.

---

## mission09B.md
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission09B.md`

*Affirmation :* - Résultat Ollama GPU : **OK**, inférence courte `llama3.1:8b` réussie ; **33/33 couches sur RTX 3090**, `ollama ps` : **100% GPU**, processus `llama-server` confirmé par `nvidia-smi`.

**Niveau détecté (analyse textuelle) :** préparé (documentaire)
**Réserve/Prouve absente :** Aucune mention explicite d'échec dans le texte lu. Note : la lecture du texte ne prouve pas l'état réel du système.

---

## mission10.md
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission10.md`

*Affirmation :* - **Compatibilité / installation : OK**, Ollama **0.40.3 conservé**, aucune mise à jour nécessaire. Modèle officiel [qwen3.5:27b-q4_K_M](https://ollama.com/library/qwen3.5:27b-q4_K_M), 26,9B, manifeste `64ae5b1d651f`, environ 17,5 Go téléchargés avec vérification SHA par Ollama. Aucun modèle existant supprimé.
*Affirmation :* **Incidents qualitatifs :** sans document, Qwen propose explicitement de supprimer le volume Open WebUI : violation de conservation des comptes/conversations/documents. Tag `llama3` inadapté au modèle testé, référence d’image incorrecte et causalités trop affirmatives. Avec document, volume préservé mais règle de compatibilité WebUI/Ollama inventée, seuil de température de génération abusivement causal et rollback sans revue des migrations. Aucune commande suggérée exécutée ; aucune réinstallation de pilote recommandée. Petit essai initial avec fragment chinois ; essais WebUI à 64/512 tokens coupés pendant le raisonnement, puis validation avec le budget normal réussie : **17 × 23 = 391**, fin naturelle.

**Niveau détecté (analyse textuelle) :** testé
**Réserve/Prouve absente :** Aucune mention explicite d'échec dans le texte lu. Note : la lecture du texte ne prouve pas l'état réel du système.

---

## mission11.md
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission11.md`

*Affirmation :* 12 octobre 2026 — étude statique, sans installation ni exécution du code téléchargé.
*Affirmation :* **Décision recommandée : NO-GO pour intégrer intégralement Jarvis Voice en l’état ; GO sous conditions pour l’option B, modulaire.** Une réutilisation ciblée est envisageable, mais son gain de temps doit être démontré avant adoption.
*Affirmation :* Le candidat le plus proche du besoin est **[bigsk1/jarvis-voice](https://github.com/bigsk1/jarvis-voice)** : voix, interface Web, Ollama, outils et mémoire structurée sont présents dans le code. L’identité du projet initial reste **EN ATTENTE**, car aucune URL ni auteur n’était fourni. Les conclusions détaillées concernent ce candidat, pas tous les logiciels appelés Jarvis.
*Affirmation :* Il ne constitue pas une extension prête à brancher sur notre Open WebUI. Il apporte son propre environnement Python, ses interfaces, bases et services. Sa licence est restrictive, ses valeurs par défaut sont anglaises, son système d’embeddings impose un modèle supplémentaire et ses protections varient selon le canal d’exécution. Le contrôle vocal d’actions sensibles n’est pas acceptable en l’état. La mention « Production Ready » du README n’est pas une validation pour notre machine.
*Affirmation :* ## 3. Maintenance, licence, technologies et installation
*Affirmation :* ### État daté
*Affirmation :* Le fichier [LICENSE au commit audité](https://github.com/bigsk1/jarvis-voice/blob/68cfe48d3ae775dd56d4ef0e7bd69843b346b228/LICENSE) accorde l’usage personnel et la modification, exige attribution et conservation de la licence, et soumet l’usage commercial à une permission écrite. C’est une licence personnalisée **source available**, pas une licence libre sans restriction commerciale. Réutiliser un module copie aussi ses contraintes. Usage personnel envisageable ; usage professionnel/commercial **EN ATTENTE** de qualification et, si applicable, de permission. Ce constat résulte du texte publié, sans interprétation juridique exhaustive.
*Affirmation :* Python **≥3.12**, scripts Bash, SQLite/FTS5, FastAPI/Uvicorn, Flask/Socket.IO, JavaScript navigateur ; clients de fournisseurs LLM dont Ollama. STT faster-whisper **1.2.0**, CTranslate2 **4.6.0**, PyAV, openWakeWord, ONNX Runtime, sounddevice ; traitement audio SoX/FFmpeg/ALSA. TTS local via serveurs externes Kokoro ou Qwen3-TTS. Nombreuses autres dépendances : SDK cloud, Docker, PDF, Paramiko, outils Web et multimédia. `pyproject.toml` et `uv.lock` sont archivés ; aucune résolution ni installation n’a été exécutée.
*Affirmation :* Documentation abondante : INSTALL_GUIDE, QUICKSTART, MEMORY_SYSTEM, USER_PROFILE_SYSTEM, WEB_TALK, SYNC_ARCHITECTURE, SECURITY_HARDENING et documentation Ollama. Présence de 489 fichiers sous `tests` au relevé ; ni leur succès ni leur couverture réelle ne sont établis. Les documents d’archive ne sont pas traités comme implémentation actuelle.
*Affirmation :* Procédure officielle étudiée : clone dans `~/jarvis-voice`, `install.sh`, dépendances système, environnement partagé `~/jarvis-venv` via uv/lockfile, initialisation et vérification ; réglage de `config/local.env`, lancement local, services optionnels. L’installateur peut appeler sudo/APT, télécharger puis exécuter l’installateur uv et appeler setup. **Ne pas employer cette procédure sur JARVIS sans mission d’intégration explicitement autorisée.** Dans cette étude elle a seulement été lue.
*Affirmation :* « Native et documentée » signifie documentation et chemin de code identifiés, **pas test fonctionnel sur notre machine**. « Possible avec adaptation » inclut configuration, ajout de service ou modification nécessaire. Les preuves correspondent au commit figé ; [index détaillé](mission11-preuves/notes-techniques.md).
*Affirmation :* | 1. STT français | **Possible avec adaptation** | `bin/stt.py` appelle WhisperModel avec détection de langue ; défaut `small.en` incompatible avec l’objectif. Choisir `small` multilingue, idéalement exposer `language="fr"`. Qualité française non testée. |
*Affirmation :* | 4. Navigateur/appareil distant | **Native et documentée** | `getUserMedia`, MediaRecorder, états Talk, transcription et lecture audio ; micro du client. HTTPS/localhost et authentification nécessaires. |
*Affirmation :* | 5. Ollama | **Native et documentée** | `OllamaProvider` dans `llm_provider.py`, appels `/api/chat`, URL et modèle configurables. Version locale exacte non testée avec ce logiciel. |
*Affirmation :* ## 5. Compatibilité avec notre installation
*Affirmation :* Python local **3.13.5** satisfait le minimum déclaré. Cela ne prouve pas que toutes les roues binaires du lockfile sont compatibles avec Debian 13/Python 3.13. L’installation est orientée Ubuntu 24.04+, le script système accepte Debian via `/etc/debian_version`. SoX/FFmpeg/ALSA et périphériques audio devront être qualifiés ; aucune particularité T2Linux n’est traitée dans le projet. Le microphone du navigateur évite de dépendre du micro interne du Mac, mais pas de la capture sur le client.
*Affirmation :* La configuration bigsk1 suggère des modèles distincts pour statut, feedback, construction d’outils, helper et embeddings. Aucun des modèles vocaux/embedding nécessaires n’est actuellement garanti présent. Avec `OLLAMA_MAX_LOADED_MODELS=1` documenté en Mission 08, charger les embeddings ou auxiliaires peut évincer Qwen, même si ceux-ci emploient le CPU. Désactiver ces fonctions dans le MVP ; commencer avec FTS5 sans embeddings. Les performances CPU, latence TTS et stabilité thermique restent à mesurer lors d’une mission autorisée.
*Affirmation :* **Dialogue et client distant.** Web Talk est réellement implémenté, avec états écouter/transcrire/travailler/parler, suspension du micro et boutons d’interruption. Des phrases de contrôle sont anglaises ; les traduire fait partie de l’adaptation. Pour le MVP, alternance stricte avec appui pour parler, micro coupé pendant la réponse, pas de wake word ni interruption automatique. Un navigateur distant nécessite un contexte sécurisé HTTPS : notre accès WebUI HTTP LAN ne suffit généralement pas à autoriser `getUserMedia`. Préparer une origine HTTPS indépendante et authentifiée dans une future mission réseau autorisée, ou débuter sur localhost. [Exigences navigateur MDN](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia).
*Affirmation :* Le code `memory_db.py` crée réellement les tables et implémente recherche/correction/suppression. `orchestrator_v2.py` prépare l’injection automatique ; `response_formatter.py` ajoute la carte utilisateur. Il existe donc une mémoire personnelle structurée, distincte de la simple conservation d’échanges. **La présence d’un score de confiance ou d’un évaluateur LLM ne garantit pas que les habitudes apprises soient vraies.** Les règles FTS `porter unicode61` emploient un stemming anglais ; la recherche française mérite une stratégie testée, par exemple unicode61 et clés structurées.
*Affirmation :* | Compatibilité | Plausible, adaptations multiples et API exacte à tester | Bon alignement avec services actuels | Dépend des dépendances extraites |
*Affirmation :* | Réversibilité | Bonne seulement dans installation entièrement séparée | Arrêt/retrait des ajouts dédiés | Bonne si aucune migration active |
*Affirmation :* Estimations d’ingénierie pour un développeur connaissant l’installation, **pas un devis ni des durées mesurées**. Un jour représente 6–8 heures utiles. HTTPS distant et validation opérationnelle peuvent ajouter 0,5–1,5 jour. L’inférence des habitudes et le RAG approfondi demandent des missions distinctes.
*Affirmation :* **Hybride tangible :** reprendre les idées d’états Talk, IDs explicites de mémoire, provenance et portabilité ; éventuellement une extraction étroite après vérification de licence et mesure du couplage. Réutiliser directement les moteurs indépendants faster-whisper/Piper ne nécessite pas de reprendre Jarvis Voice. Copier son orchestrateur complet pour un simple dialogue n’apporte pas de gain établi. Réutiliser Kokoro seul à la place de Piper peut être utile pour une voix plus expressive, à comparer sur CPU après le MVP.
*Affirmation :* Ce schéma décrit une proposition, aucun composant n’a été déployé. Les échanges vocaux ne sont pas automatiquement des chats WebUI. La mémoire peut être indépendante du modèle dès cette première version ; son raccordement à l’interface WebUI demandera une mission applicative supplémentaire.
*Affirmation :* - **A complet : NO-GO en l’état.** Français non prêt par défaut, licence restrictive, couche applicative concurrente, dépendances et modèles auxiliaires, protections vocales insuffisantes, aucune compatibilité exécutée sur Debian/Ollama exacts.
*Affirmation :* | **12A — prototype vocal isolé CPU** | Dépendances/versions et licences figées, STT `small` français, Piper, client local appui pour parler ; 4–8 h | 20 phrases de test synthétiques en français, transcription et lecture audible ; aucun GPU vocal ; ressources et erreurs documentées ; cœur inchangé |
*Affirmation :* | **12B — dialogue Ollama** | Passerelle, états et appels `/api/chat`, trois modèles existants ; 4–8 h | Dix tours cohérents par modèle, silence/timeout traités, micro coupé pendant TTS, raisonnement jamais lu ; latences médianes/p95 et VRAM relevées |
*Affirmation :* | **12C — mémoire personnelle minimale** | SQLite/FTS, CRUD, contexte injecté, export ; 4–8 h | Fait retenu après nouvelle session, corrigé puis supprimé, plus aucune restitution du fait supprimé ; même préférence retrouvée avec deux modèles ; tests avec données fictives |
*Affirmation :* | **12D — client distant sécurisé** | Origine HTTPS/authentifiée dédiée, test navigateur réel ; 4–8 h | Micro/lecture sur appareil distant, accès non authentifié refusé, aucune exposition directe d’Ollama ; configuration réseau à autoriser séparément |
*Affirmation :* Avant toute installation ultérieure : état de référence et sauvegarde par le mécanisme existant dans la mission autorisée, ajouts dans un répertoire indépendant, versions fixées, aucune modification Ollama/pilote/noyau. Vérifier que le plan de retour arrière retire uniquement les nouveaux composants et conserve leur mémoire exportable. Ne pas démarrer le Compose amont tel quel.
*Affirmation :* | Fonctionnement français réel | Installation et exécution interdites | 12A : qualité STT/TTS, voix choisie et prononciation |
*Affirmation :* | Dépendances Debian/Python 3.13 | Wheels, audio T2 et runtime non installés | Résolution isolée et qualification 12A ; pas de modification système dans cette étude |
*Affirmation :* | Navigateur distant | HTTP LAN actuel et aucun client réel testé | 12D, HTTPS dédié ; localhost pour première preuve |
*Affirmation :* | Habitudes fiables | Mécanismes présents mais efficacité non démontrée | Souvenirs explicites pour MVP, corpus/test 14 |
*Affirmation :* Travaux réalisés : lecture des rapports 06–10 et 09B, consultations GitHub/docs officielles, clone superficiel dans `/tmp/jarvis-m11-3Ah6eH`, inspection statique, GET version/tags Ollama, lecture des sockets/RAM/disque et métadonnées de quelques paquets. **Aucune inférence, aucun script téléchargé exécuté, aucune dépendance installée, aucun conteneur démarré, aucun changement de service/configuration/base/modèle/réseau et aucun redémarrage.** Écritures limitées au temporaire d’inspection et aux nouveaux livrables Mission 11. Aucun secret ni conversation privée exporté.

**Niveau détecté (analyse textuelle) :** testé
**Réserve/Prouve absente :** Le rapport signale des points à vérifier, erreurs ou manques.

---

❌ **Fichier absent :** `/home/adminjarvis/JARVIS/rapports/MISSION-13E/13F-TESTS.md`
## RECEPTION-MISSION14.md
**Chemin :** `/home/adminjarvis/JARVIS/mission00/docs/missions/13D-E/RECEPTION-MISSION14.md`

*Affirmation :* # Mission 13D-E / 14 — réception de la nouvelle tentative
*Affirmation :* **RÉCEPTION COMPLÈTE VALIDÉE**
*Affirmation :* | Tâche | État | Preuve / réserve |
*Affirmation :* | debian | validated | Fresh Debian completed, sshd configuration checked and signed EFI copies match; see installer log |
*Affirmation :* | integration | validated | Authenticated gateway and Open WebUI inference plus canonical memory/tools/voice tests passed |
*Affirmation :* | tests | validated | Real inference, authenticated integration, memory, tool call and synthetic voice evidence saved |
*Affirmation :* | plasma | validated | KDE Plasma et session X11 installés, SDDM activé pour le reboot ; ouverture de session graphique à vérifier après redémarrage |
*Affirmation :* Comptes demandés : adminjarvis et jarvis-bootstrap, mot de passe utilisateur privé identique ; secours par mot de passe conservé. Réinstallation de la racine uniquement prévue sur miroir/GPT/ESP existants, sans recréation volontaire du RAID. Les étapes non validées dans le tableau ne sont pas réputées réussies. Aucun essai physique de retrait des disques ni de seconde RTX 3090 alimentée. Aucun test de microphone physique ; les essais vocaux utilisent un WAV synthétique. Voix, outils et mémoire SQLite/FTS5 restent sur le Mac mini, sans base parallèle.
*Affirmation :* Pilote NVIDIA : 550.163.01 ; Ollama : 0.40.3 ; modèles réellement testés : qwen3.5:27b-q4_K_M, ministral-3:14b-instruct-2512-q4_K_M, llama3.1:8b.
*Affirmation :* Les journaux, inventaires, UUID, clés et secrets restent sous deployment/13de/private/reinstall-02, hors Git. Les éventuelles erreurs détaillées et données de test sont privées. Aucune fusion main.
*Affirmation :* Le [bilan des erreurs et scripts corrigés](RAPPORT-FINAL.md#bilan-explicite-des-erreurs-et-des-scripts-corrigés--17-octobre-2026) distingue les incidents, les corrections vérifiées et les défauts restants. En particulier, le contrôleur `serve-supervised.py` utilise encore un reboot forcé de l’installateur : sa correction reste nécessaire avant de promettre la conservation du RAID sans nouvelle resynchronisation. Le reboot final normal et le RAID sain sont validés pour cette réception.

**Niveau détecté (analyse textuelle) :** réception
**Réserve/Prouve absente :** Le rapport signale des points à vérifier, erreurs ou manques.

---

## RACCORDEMENT-ADMIN-DELL.md
**Chemin :** `/home/adminjarvis/JARVIS/mission00/docs/missions/11B/RACCORDEMENT-ADMIN-DELL.md`

*Affirmation :* Directives consultées : AGENTS, charte JARVIS, rapport et architecture 11, SUIVI/ROADMAP, dernière réception 13D-E/14 et ordre 11B conservé dans la conversation canonique. Autorisations préservées : administration Dell IA sans validation intermédiaire, identités existantes, préservation du Mac/mémoire/voix/Bbox, une RTX alimentée, secrets privés, aucune fusion main. Exclusion : JL-02.
*Affirmation :* Le Dell est sous Debian 13.7, RAID1 [UU] sans resynchronisation. SSH adminjarvis et sudo non interactif ont été vérifiés. L’installation 13D-E/14 est réceptionnée : aucune réinstallation, aucun nouveau compte ou clé.
*Affirmation :* `/etc/jarvis/host-policy.json`, propriété root et mode 0600, conserve `dell-observe` pour compatibilité. `allow_admin=true`, `ansible_enabled=true`. Le broker est activé au boot et recharge cette politique protégée ; les mises à niveau install.sh ne remplacent pas les droits existants. L’ancien provisionneur d’observation refuse maintenant de rétrograder un profil déjà administrable.
*Affirmation :* - Paquets IA/développement explicitement listés : outils Python, compilation, OpenBLAS, ffmpeg, outils système, pilotes NVIDIA/CUDA et dépendances courantes. Installation SSH et Ansible disponibles.
*Affirmation :* | activate_dell_admin.py | Provisionnement opérateur reproductible : réception préalable, contrôle cible/stockage, sauvegarde et politique atomique, identités existantes. |
*Affirmation :* | core.py | Suppression de la consigne périmée « Dell en cours d’installation » ; conservation de tous les profils distants lors de la réduction du contexte. La troncature précédente masquait le Dell derrière loopback et provoquait des lectures répétées. |
*Affirmation :* | reception_11b.py | Tests authentifiés : Qwen choisit et appelle les outils ; aucune réponse ou invocation de modèle simulée. Preuves brutes privées. |
*Affirmation :* | test_bridge.py | Vérifications du périmètre distant, absence de références aux clés et refus avant mutation en cas d’identité divergente. |
*Affirmation :* Le premier essai Qwen s’est mis à répéter host_policy avec l’ancien résumé tronqué. Il a été interrompu pour charger la correction ; cet essai interrompu ne vaut pas réception. Les traces sont conservées. Le second essai a atteint les actions réelles, avec encore plusieurs lectures répétées de politique : une réussite ciblée ne démontre pas une planification parfaite.
*Affirmation :* ## Preuves et réception
*Affirmation :* Voir [PREUVES-RACCORDEMENT.json](PREUVES-RACCORDEMENT.json) pour les assertions et identifiants de preuves expurgées. Les traces intégrales restent dans un répertoire privé hors dépôt. Ne pas confondre réussite du raccordement et réception de toutes les fonctions Compute Expansion, notamment routage/repli automatique.
*Affirmation :* ### Résultats vérifiés
*Affirmation :* - Qwen avant redémarrage : identité/sudo, Ansible ping, création du fichier par Ansible, relecture SSH et état actif d’Ollama ; tous les retours d’opération sont à zéro et identifiés `JARVIS-runtime` par le broker.
*Affirmation :* - 12 tests des frontières du broker réussis, dont refus de lecture de /etc/shadow, refus d’arrêt SSH, paquet hors liste refusé et arrêt avant mutation sur identité divergente.
*Affirmation :* - 27 tests du backend conversationnel réussis après correction du contexte ; compilation Python réussie.
*Affirmation :* **GO pour le raccordement permanent SSH/Ansible du Dell.** Cela ne clôture pas à lui seul la mission Compute Expansion. Les répétitions d’appels Qwen restent une limite observée ; les écritures répétées de ce scénario portaient le même contenu de preuve. Le budget de réduction du contexte a été ajusté pour éviter de supprimer tout l’historique des opérations lorsque les instructions et souvenirs occupent déjà 9 000 caractères. La reprise durable 11B doit vérifier le routage/repli et les capacités restantes, sans réinstaller les composants acquis ni lancer JL-02.
*Affirmation :* Le checkpoint conversationnel a été transmis au planificateur existant via l’API authentifiée, par `resume_11b.py`. Exécution durable : `4d824f2bbc664b5789144f146e845e14`, état observé `running`, tentative 1. Qwen a enregistré le plan audit → modèles → expansion et exécuté des outils réels, dont SSH distant et lecture des ressources. Ce n’est pas une simple instruction laissée dans un fichier. Les observations durables sont conservées dans missions.sqlite ; les opérations acquises restent dans le checkpoint et ne demandent pas de réinstallation.

**Niveau détecté (analyse textuelle) :** réception
**Réserve/Prouve absente :** Aucune mention explicite d'échec dans le texte lu. Note : la lecture du texte ne prouve pas l'état réel du système.

---

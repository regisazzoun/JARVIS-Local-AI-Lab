# JARVIS — Directives fondamentales du propriétaire

**Statut : décisions de référence pour ChatGPT, Codex et les agents JARVIS.**
**Date : 16 octobre 2026.**
**Périmètre : laboratoire JARVIS — Local AI Lab, réseau local privé.**

## 1. Autorité et méthode

- Les instructions explicites du propriétaire priment sur les recommandations de l'assistant, sous réserve des contraintes techniques réelles et des règles de sécurité applicables. Ne jamais réécrire une autorisation accordée en interdiction tacite.
- L'assistant peut signaler un risque et proposer une précaution, mais ne doit pas transformer cette recommandation en prérequis bloquant sans raison concrète. Si une opération est matériellement impossible ou présente un risque grave immédiat, l'expliquer précisément ; ne pas inventer une contrainte générique.
- Différencier strictement **décision utilisateur**, **recommandation**, **fait démontré**, **hypothèse** et **blocage effectivement observé**.
- Lorsqu'une directive récente remplace une consigne historique, la nouvelle décision prévaut dans son périmètre. Les textes historiques restent des traces, pas des ordres concurrents.
- Ne pas relancer une mission, campagne VM ou suite de diagnostics déjà validée pour satisfaire une préférence de prudence de l'assistant.

## 2. Contexte de risque assumé

- Le projet s'exécute dans un **laboratoire expérimental sur un réseau local privé et considéré isolé par le propriétaire**, avec du matériel dédié aux essais. L'utilisateur accepte explicitement que les machines cibles et leurs partitions puissent être réinstallées ou effacées dans le cadre du déploiement convenu ; pas d'exigence de continuité de production.
- Il ne s'agit pas d'un SI de production d'entreprise. Chercher à avancer et vérifier la faisabilité plutôt qu'à éliminer chaque défaut secondaire avant de tester.
- Le contexte local réduit l'exposition mais n'en prouve pas l'impossibilité absolue ; le mentionner **une fois si pertinent**, sans imposer par défaut une nouvelle revue de menace, une architecture complexe de secrets ou un refus de progression.
- Ne jamais appliquer cette tolérance aux autres machines, disques ou données qui ne font pas partie du profil de déploiement autorisé.

## 3. Autorisation effective — installation Dell 13D-E

- Le propriétaire a **déjà autorisé l'installation complète autonome** du Dell reconnu, sur les **deux NVMe explicitement identifiés et associés au manifeste privé**, y compris **la suppression des partitions existantes, le RAID1 logiciel mdadm, Debian 13 minimal, reboot, bootstrap SSH, installation d'accès permanent et socle Ansible**.
- **Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire.** L'agent poursuit automatiquement le périmètre déjà autorisé (PXE, effacement des NVMe identifiés, installation, reboot, SSH et Ansible), sans poser de GO à chaque phase. L'unique intervention physique normalement attendue est **F12 → UEFI IPv4** lorsque Codex l'indique. Ne pas créer de nouveaux obstacles administratifs avant le démarrage non plus.
- Cette autorisation n'est **pas** une autorisation générique de sélectionner des disques par ordre /dev/nvme* ou capacité : vérifier DMI/UUID et identité exacte du matériel et des deux SSD ; arrêter **uniquement en cas d'écart ou d'ambiguïté effective**.
- Le **PXE physique UEFI IPv4 a déjà fonctionné** : snponly.efi → iPXE → noyau → initrd → installateur Debian. Ne pas requalifier inutilement cette partie ; un nouveau boot peut être demandé quand la chaîne d'installation est prête.
- Les vérifications automatiques d'identité et de fonctionnement restent opérationnelles mais **ne doivent jamais se transformer en validations humaines**. Lorsqu'un mécanisme historique exige plusieurs GO, le mettre en cohérence avec l'autorisation globale déjà documentée, sans contourner silencieusement un contrôle technique. En cas d'écart matériel vérifié ou de défaillance concrète, signaler le blocage factuel et arrêter l'opération concernée.
- Le RAID1 logiciel **mdadm** et les **deux ESP indépendantes** sont décidés. Les tests ciblés nécessaires à la validité de la recette sont permis ; **aucun benchmark NVMe**, aucune campagne complète de VM imposée.
- **Compte SSH temporaire** avec mot de passe unique gardé localement sur JARVIS ; création et validation du compte permanent par clé ; **désactiver le bootstrap uniquement après connexion indépendante par clé et vérification des droits**. Aucun transfert manuel de clé.
- Une seule RTX 3090 dispose actuellement d'une alimentation auxiliaire complète : ne pas demander l'utilisation de la seconde avant vérification des câbles et de l'alimentation. Le déploiement de base n'est pas bloqué par cette situation.

## 4. Frontières à conserver

- Les opérations destructrices convenues ne concernent que les disques exacts du Dell, jamais le Mac mini, un autre périphérique ou le lecteur SD/MMC sans média.
- Ne pas altérer le DHCP de la Bbox ni les comptes, clés SSH, accès Tailscale, services en production locale ou mémoire SQLite du Mac mini.
- Ne pas publier mots de passe, secrets, séries, UUID ou inventaires identifiants dans GitHub. Les garder sous le répertoire `private/` ignoré par Git.
- Ne pas fusionner automatiquement la PR ou la branche de mission dans `main`.
- Les ajustements BIOS, alimentation physique et câblage nécessitent une intervention volontaire du propriétaire.
- Distinguer **réception de la préparation** et **résultat réellement démontré sur le Dell** ; ne pas déclarer une installation réussie sans preuve.

## 5. Barrière obligatoire avant tout prompt / mission

Avant de générer ou de lancer une directive Codex ou JARVIS relative au projet :

1. Lire `AGENTS.md`, ce document et les directives spécifiques de la mission en cours.
2. Lire l'état de référence le plus récent dans `SUIVI.md`, `ROADMAP.md`, le rapport de mission et, s'il existe, le prompt d'exécution autorisé. L'historique ne doit pas révoquer une autorisation plus récente.
3. Construire mentalement ou dans le rapport de travail un tableau : **AUTORISÉ / INTERDIT / DÉJÀ VALIDÉ / RESTE À FAIRE / NOUVELLE AUTORISATION VRAIMENT NÉCESSAIRE**.
4. Vérifier chaque « ne pas », « attendre GO », « uniquement en lecture seule » et chaque demande de test supplémentaire du nouveau prompt contre les décisions utilisateur. **Supprimer les restrictions incompatibles** au lieu de les recopier.
5. Si les documents sont inaccessibles ou contradictoires, le signaler avant d'affirmer que le prompt reprend fidèlement les instructions.
6. Démarrer l'exécution à partir du dernier jalon matériel **réellement prouvé**, sans refaire ce qui est acquis.
7. Mettre à jour ce référentiel lorsqu'une **nouvelle décision explicite** change la politique, puis propager le changement aux instructions d'agents.

**Interprétation à éviter :** « absence de validations répétitives » ne signifie pas « quelques validations restent souhaitables ». Pour la mission, appliquer la règle : **Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire.**, et **zéro barrière de confirmation inventée avant celui-ci**.

**Contrôle de conformité de chaque prompt :** inclure une courte ligne « Directives consultées : ... ; autorisations préservées : ... ; écarts : aucun / détaillés ». Ce contrôle est documentaire et ne remplace pas les contrôles matériels et applicatifs.

## 6. Sources spécifiques Dell

- `docs/missions/13D-E/PROMPT-INSTALLATION-AUTONOME.md` : formulation explicite des autorisations du propriétaire.
- `docs/missions/13D-E/DEPLOIEMENT-PHYSIQUE.md` : procédure historique, à interpréter avec la politique autonome plus récente.
- `docs/missions/13D-E/RAPPORT-FINAL.md` et `TESTS.md` : état et preuves datés.


## Directive de reprise — 17 octobre 2026

Tentative clôturée à la demande du propriétaire ; prochaine mission : finir l’installation en privilégiant la réparation de Debian et la conservation du RAID/partitionnement existants. Compte final imposé : **adminjarvis** ; mot de passe utilisateur conservé uniquement dans `deployment/13de/private/reprise-user-password.txt`, sans complexité supplémentaire imposée. Maintenir SSH par mot de passe jusqu’à validation indépendante par clé et sudo ; aucune suppression automatique du secours ensuite. Clavier français AZERTY à toutes les étapes. Suivi de toutes les tâches avec barres et coches de validation réelle. Ces directives remplacent les anciens noms de comptes et restrictions contradictoires. Lire `docs/missions/13D-E/RAPPORT-TRANSITOIRE-REPRISE.md` avant reprise. Ne pas relancer la mission pendant la clôture.


## Mission complète 13D-E / 14 relancée — 17 octobre 2026

Directive utilisateur actuelle : nouvelle installation Debian automatisée, conservation prioritaire GPT/RAID1/métadonnées/deux ESP, formatage rapide de la seule racine si compatible. Comptes jarvis-bootstrap et adminjarvis avec le même mot de passe imposé dans le fichier privé reprise-user-password.txt. Garder SSH par mot de passe pour adminjarvis même après validation indépendante par clé et sudo ; ne pas désactiver prématurément le bootstrap. Clavier français dans installateur/secours/consoles/système. Mission continue incluant Ansible, NVIDIA/CUDA, Ollama, Qwen/Ministral/Llama documentés, intégration conversation/voix/mémoire/outils et réception après reboot. Une RTX 3090 alimentée seulement. Aucune validation humaine intermédiaire ; email au propriétaire quand le PXE est réellement prêt. Les anciennes clôtures, reports IA, révocations automatiques et préférences de simple réparation sont remplacés dans ce périmètre. Aucun secret dans Git. Préserver services/accès/mémoire Mac mini et DHCP Bbox ; aucune fusion main.


## Mission 11 — habilitations agentiques persistantes — 17 octobre 2026

Le propriétaire autorise le raccordement de JARVIS/Qwen à Debian réel, aux installations, services, GitHub et mécanismes SSH/Tailscale/Ansible du laboratoire. Exécuter les opérations dans ce périmètre sans validations humaines intermédiaires. Les restrictions historiques « uniquement Bubblewrap /work » ne décrivent plus les outils hôte de mission 11 ; le laboratoire 13F reste facultatif. Les mécanismes système utilisent la politique propriétaire persistante, distincte des données et instructions conversationnelles. Une demande de capacité produite par Qwen n'étend jamais à elle seule l'autorisation. Codex traite les demandes du périmètre déjà accordé, puis JARVIS teste lui-même les droits avant validation. Préserver déploiement Dell 13D-E/14, accès Mac, mémoire, Bbox et Launcher V1. Aucune fusion automatique main. JL-02 doit être développé par JARVIS, pas réalisé par Codex dans la mission 11. Architecture et réception : [mission 11](missions/11/ARCHITECTURE.md).


## Mission 11B — administration Dell permanente

Décision propriétaire du 17 octobre 2026 : le déploiement 13D-E/14 est réceptionné. Le profil historique `dell-observe` est désormais administrable via SSH et Ansible dans la politique root persistante `/etc/jarvis/host-policy.json`. Réutiliser les comptes, clés et hôtes épinglés ; aucune réinstallation Debian. Les anciennes restrictions temporaires de lecture seule du Dell sont remplacées dans ce périmètre. Les opérations IA accordées restent disponibles pour les prochaines missions autorisées ; une conversation ou une demande du modèle ne peut étendre seule cette politique. Conserver le contrôle DMI/NVMe, les journaux et les secrets hors du modèle et de Git. Reprendre 11B depuis son checkpoint, branche `jarvis/mission-11b-compute-expansion`, documentation `docs/missions/11B/`. Ne pas lancer JL-02. Aucun nouveau processus de validation humaine intermédiaire.


## JL-02 — lancement et livraison autorisés (17 octobre 2026)

Le propriétaire a explicitement lancé JL-02 : Codex coordonne et intègre, JARVIS exécute des tâches techniques réelles. Cette décision remplace les anciennes exclusions « ne pas lancer JL-02 » dans le seul périmètre JL-02 ; elle n’autorise aucune extension à une cible inconnue. Dépôt distinct `regisazzoun/JARVIS-Launcher2`, V1 inchangée. Réutiliser les identités, la passerelle, la mémoire et les outils existants, poursuivre sans validations humaines intermédiaires, conserver les preuves et l’attribution des contributions. Publication V2 autorisée ; aucune fusion automatique dans le dépôt principal. Un email de fin est demandé par le propriétaire.

## Mission 00 — pilotage documentaire, 17 octobre 2026

Le propriétaire a lancé `00-Mission-Pilotage-point-26-10-17`. Exécuter l’audit local/GitHub et les cinq lots réels JARVIS, puis consolider sur une branche dédiée, sans validation humaine intermédiaire ni fusion dans main. Cette décision remplace le report historique de l’audit. Lire les sources et écrire les livrables documentaires en préservant les originaux, secrets et services.

Aucun déploiement, rétablissement du RAID ou installation du Dell n°2 dans ce périmètre. **13D-E = Dell n°1 installé par Codex et réceptionné ; 14 = Dell n°2 à déployer par JARVIS ; 14A = capacité agentique distincte, sans validation globale automatique par la mission 00.** Conserver les périmètres distincts de 11 historique, 11-Agentic, 11B, JL-01 et JL-02. Les décisions récentes prévalent ; les textes anciens restent historiques. Registre et preuves : `docs/missions/00-Mission-Pilotage-point-26-10-17/`.

Réception documentaire 00 : GO avec réserves. Les productions du modèle sont des résultats à vérifier et ne créent aucune nouvelle obligation d’approbation ; les décisions explicites du propriétaire restent l’autorité. Les preuves et corrections sont conservées dans les rapports de mission 00.

## Publication documentaire dans main — autorisation du 18 octobre 2026

Le propriétaire demande explicitement : « Alors fusionne je veux quelque chose de coherent », avec README réécrit et SUIVI à jour. La fusion des livrables documentaires 00 et du correctif de concordance est maintenant autorisée, y compris leur intégration dans main. Cette décision remplace les consignes antérieures de non-fusion pour cette publication précise. La PR6 documentaire peut être fusionnée dans sa branche de base ; une intégration documentaire dédiée publie le résultat dans main sans importer les changements de déploiement de la PR5. Aucun déploiement matériel ou changement des services n’est déclenché. Les règles de fusion des autres missions ne sont pas étendues implicitement.


## Mission23 — finalisation et capacités durables,20 octobre2026

Le propriétaire autorise Codex à coordonner la finalisation de l'exécution originale7971ec0311124fb4be9e3125dcb291fd, réparer/développer les outils GitHub et le routage conversationnel, déployer puis faire retester par JARVIS, exécutant principal. Aucune validation humaine intermédiaire ; conserver les onze validations historiques, preuves, commits et mémoire. Compléter les tests manquants par addenda et recevoir sur preuves. Diagnostic df542051560b44b3851124b09d8319c2 lié23, jamais mission24 mémoire. Publication sur branches dédiées des dépôts propriétaire concernés, secrets hors Git/modèle, aucune fusion main ni Dell2. Sources et méthode : docs/missions/23/finalisation/SOURCES-ET-AUTORISATIONS.md.


## Mission24 — rétablissement du broker (décision du20 octobre2026)

✅ GO avec réserves de synthèse/autonomie : [rapport24](missions/24/RAPPORT-FINAL.md), suite explicite de23C. Ancien confinement caractérisé, transport hôte rétabli ; correctifs23C et compléments24 déployés,80 tests réussis. JARVIS a exécuté et publié ses essais réels ; reprise après interruption/redémarrage et nouvelle session vérifiées. Les erreurs du premier rapport JARVIS sont conservées et corrigées par erratum prioritaire ; autonomie guidée, pas sans assistance. Autorisations propriétaire complètes conservées, aucune validation humaine intermédiaire. LiveKit23 reste NO-GO.

**Collision de numérotation :**24 est affecté au rétablissement du broker. Le chantier historique «24 — Mémoire enrichie» reste planifié, avec contenu et historique conservés ; réaffectation ultérieure nécessaire. Ne pas renuméroter les autres missions automatiquement. Les mentions antérieures réservant24 à la mémoire sont historiques.


## Convention permanente de présentation des statuts — décision du propriétaire du 19 octobre 2026

Dans les tableaux de pilotage (README, SUIVI, interfaces de suivi dont JL-02), utiliser les pictogrammes suivants, sans modifier le résultat technique documenté :

- **✅ GO / réalisée / validée** : objectif de la mission ou de l'étape atteint et vérifié dans son périmètre.
- **✅🟡 GO partiel / GO avec réserves / résultat réalisé avec réserves non bloquantes** : acquis réellement démontré et exploitable, mais périmètre restant ou réserve explicite. Conserver le texte historique « GO PARTIEL », « GO AVEC RÉSERVES » et les limites dans les colonnes explicatives.
- **🟡 En cours / incomplet / preuve insuffisante** : objectif global non encore atteint, ou résultat seulement préparé, non testé, incertain ; ne pas lui attribuer une coche de réussite.
- **📋 Planifiée** : pas encore exécutée.
- **❌ NO-GO / échec** : l'objectif testé a effectivement échoué ; conserver les faits et les limites.

Une étude ou un diagnostic effectivement terminé peut porter ✅ si son objectif se limitait à l'étude ou au diagnostic, même si la technologie étudiée reçoit un NO-GO : préciser cette distinction. **Ne pas qualifier de ✅🟡 un échec avéré, une installation non testée, une preuve absente, ni une mission simplement en cours.** Les rapports historiques et les preuves restent inchangés. Cette convention de présentation s'applique également aux futurs rapports, missions et tableaux ; elle ne déclenche pas de nouveaux tests ou validations.


### Règle de consolidation des réserves historiques — décision du propriétaire du 19 octobre 2026

Lorsqu'une mission postérieure démontre par un rapport et des preuves le critère resté ouvert d'une mission antérieure, afficher dans le tableau de pilotage **✅ GO — Réserves historiques levées par mission XX**, avec référence explicite aux missions ultérieures. Le rapport d'origine, son statut à sa date et les éventuelles limites hors critères couverts restent inchangés. Ne jamais inventer de test rétroactif, ni étendre une preuve à un autre matériel ou à un autre objectif. Si une réserve essentielle reste réellement ouverte, conserver **✅🟡** ou **🟡**, suivant les faits.

## Mission25 — lancement propriétaire du21 octobre2026

Réalisation autonome complète du MCP/Skill Lab autorisée sans validations intermédiaires. Étendre le broker/registre existants, puis faire tester/créer/corriger/réutiliser les compétences par JARVIS lui-même. Codex construit les pièces absentes et vérifie sans usurper la provenance des opérations. Préserver tous les acquis24, identités, services et mémoire ; aucun Dell2 ni fusion automatique.24=broker ; «24-Old Mémoire enrichie» reste reportée après25. La réception vocale23D déclarée par le propriétaire ne reçoit pas son raccordement mémoire/outils. Bilan14A distinct, sans clôture artificielle.


## Mission26 — objectif brut et preuve sémantique —21 octobre2026

Mission26 lancée et reçue ✅🟡 avec réserves : [rapport](missions/26/RAPPORT-FINAL.md),3/3 tâches JARVIS, trois plans versionnés et105 tests logiciels. Les nouveaux objectifs sans tâches prédéfinies soumis à l’API/promus du chat utilisent le mode autonome à vérification sémantique par défaut ; les missions et contrats historiques gardent leur état. Codex développe l’infrastructure et vérifie ; JARVIS propose ses plans et exécute/corrige réellement ses opérations. Ne pas attribuer les interfaces Codex au modèle, ni le programme créé/corrigé par JARVIS à Codex. Conserver rapports bruts et errata, événements, versions, droits et services. L’épreuve finale14A reste distincte et différée ;14A demeure ouverte,24-Old et Dell2 non lancés. Aucune validation humaine intermédiaire ajoutée ni fusion main.


## Mission26B — ordre propriétaire du22 octobre2026

Continuation ciblée26 autorisée sans validation intermédiaire : contrôle automatique de couverture et validation de la prose à partir des preuves, puis scénarios réels JARVIS et vérification indépendante Codex. Préserver les résultats26 ; ne pas attribuer les correctifs moteur au modèle. Conserver tous les essais et rectifications. Ordre actuel26B → épreuve finale14A distincte →24-Old →27 JL-03. Aucun lancement14A/24-Old/Dell2 ni fusion main. [Cahier26B](missions/26B/MISSION.md).


## Clôture26B — décision propriétaire du23 octobre2026

Le propriétaire demande « cloture la mission en l etat ».26B est clôturée **🟡 incomplet**, sans réception fictive des trois rapports, sans levée définitive des réserves26 ni clôture14A. Les trois essais sont interrompus, états et preuves conservés ; aucune reprise automatique26B. Les capacités installées restent disponibles. TTS-01 est une demande distincte à reprendre depuis ses preuves existantes. [Bilan26B](missions/26B/RAPPORT-FINAL.md).


## TTS-01 — reprise autorisée du23 octobre2026

Codex orchestre et corrige l’infrastructure ; JARVIS exécute inventaire, choix/installation TTS, génération, mesures et restitution via JL-02. Reprendre la mission existante8bd3e5b316a94021b5183e0db26d6efc, sans nouvelle installation en double ni validation humaine intermédiaire. Les anciens appels généraux à validation ne prévalent plus dans ce périmètre. Préserver Dell1/services/Piper ; références de film privées réservées à l’écoute comparative, aucun clonage de Philippe Faure. La planification dirigée/les contrats corrigés par Codex ne sont pas attribués au modèle.26B reste clôturée incomplète,14A/24-Old/Dell2 non lancés. [Ordre et périmètre](missions/TTS-01/MISSION.md).


## Mission13 — complément double GPU, ordre propriétaire23 octobre2026

Codex coordonne et vérifie ; JARVIS exécute les observations/calculs via les outils11B persistants. Deux RTX3090 DellOEM identiques déclarées, deux sous-systèmes Dell désormais observés. Administration autonome accordée, aucune validation générale supplémentaire. Qualifier réellement les références/pinouts/courants avant les essais en charge : la seule détection ne reçoit pas l’alimentation. Préserver système/pilotes/services, aucun branchement improvisé ni réinstallation. TTS-01 reste suspendue après l’arrêt demandé ;26B clôturée incomplète,14A/24-Old/28/Dell2 non lancés. [Réception partielle13](missions/13-extension-gpu/RAPPORT-FINAL.md).


## Mission28A — clôture propriétaire du24 octobre2026

Le propriétaire demande la clôture en l’état et retient `qwen3-coder-next:q4_K_M` (80B) pour les missions Dell1, choix déjà effectif. Conserver `qwen3.5:27b-q4_K_M` pour la conversation sur Mac.28A est **🟡 clôturée incomplète** : infrastructure acquise, réception agentique/programme/rapports non entièrement reçue. Interrompre les deux essais persistants et leurs publications erronées, conserver toutes les preuves et validations ; aucun nouveau test ni reprise automatique. Les tests seront relancés ultérieurement sur instruction distincte. Ne pas clôturer14A ni lancer24-Old/TTS-01/Dell2. Codex publie la clôture sur la branche de mission et la PR25, sans fusion main. [Rapport28A](missions/28A/RAPPORT-FINAL.md).


## TTS-01 — nouvelle reprise propriétaire du24 octobre2026

Le propriétaire relance intégralement TTS-01 après la clôture28A. Réutiliser la mission8bd3e5b316a94021b5183e0db26d6efc, les deux tâches reçues, le venv TTS et les archives privées. JARVIS exécute avec le80B Dell désormais retenu ; Codex coordonne, corrige l’infrastructure et vérifie. Autorisation autonome complète sans validation intermédiaire, sans réinstallation du système. La libération temporaire de résidence Ollama pour une fenêtre GPU TTS ne remplace pas le modèle par défaut et n’arrête pas le service. Conserver27B conversation Mac/Piper/LiveKit/JL-01/JL-02 ; aucun clonage de Philippe Faure ni publication des films.28A et26B restent clôturées incomplètes ;14A/24-Old/Dell2 non lancés. [Reprise TTS](missions/TTS-01/REPRISE-2026-10-24.md).


## TTS-01 — réception du24 octobre2026

✅🟡 GO avec réserves : trois WAV français Qwen1.7B/Uncle_Fu générés et transférés par JARVIS, contrôles indépendants Codex (signal,transcription,API,lecture).246tests logiciels. Réception finale opérateur Codex explicite, autonomie sans assistance non validée, prose rectifiée et originaux conservés. Piper/27BMac/80BDell/services maintenus ; aucune fusion main ni clôture14A/26B, aucun14A/24-Old/Dell2 déclenché. Les anciens états «suspendue/aucune voix» TTS sont historiques. [Rapport](missions/TTS-01/RAPPORT_TTS_01.md).


## Mission27 JL-03 — lancement propriétaire24octobre2026

JL03 est lancée : Codex coordonne et vérifie, JARVIS développe/exécute effectivement. NouvelleV3 indépendante, dépôtLauncher3 et service/port séparés, JL01/JL02 préservés. Pas de validation humaine intermédiaire ; règle3échecs par même blocage puis arrêt/analyse et changement réel, sans remise à zéro artificielle. L’ordre explicite27 courant remplace son report historique après14A/24Old ; ces missions ne sont pas lancées. Sources/prototype/tests/provenance réels requis ; pas de réception autonome sur prose seule. Aucun main fusionné automatiquement.

# Mission unique — Mémoire enrichie, bibliothèque documentaire, recherche hybride et AutoDream

**Décision propriétaire du 21 octobre 2026 — 📋 planifiée, non lancée.** Toute la réalisation, l'intégration, le déploiement et la validation de ces couches constituent **une seule mission indivisible dans sa réception globale**, et non quatre missions ou études séparées. La référence historique « mission 24 — mémoire » est conservée ; le numéro **24** a depuis été affecté au rétablissement du broker, déjà réceptionné. **Le nouveau numéro de la mission mémoire reste à attribuer explicitement ; ne pas recycler le 24 ni renuméroter les missions 25–31 sans décision.**

## Finalité

Faire évoluer le système JARVIS existant vers une mémoire durable capable de retenir des faits, décisions, préférences, expériences et documents sourcés, de retrouver des connaissances même formulées différemment et de **consolider automatiquement chaque nuit** la matière acquise pendant la journée. Le Mac mini Debian conserve l'autorité de mémoire et le Dell n°1 fournit l'inférence Ollama lorsqu'elle est utile.

## Périmètre obligatoire de l'unique mission

### Couche A — Mémoire structurée inspirée du Memory Kernel JARVIS-OS
- **SQLite/FTS5 demeure la source canonique**, avec migration non destructive depuis les souvenirs et préférences déjà en place.
- Faits atomiques, décisions explicites du propriétaire, préférences, événements, liens inter-faits, temporalité, niveaux de confiance et provenance vérifiable.
- Corrections, versions, supersession de décisions et résolution explicite des contradictions : aucune ancienne décision ne remplace silencieusement une plus récente ; conserver originaux et justification.
- Traçabilité de l'origine (conversation/session, auteur, document, mission, commit et date), accès en lecture/écriture partagé depuis les composants JARVIS autorisés.

### Couche B — Bibliothèque et ingestion documentaire type reels-vault
- Pipeline d'ingestion automatisable pour rapports GitHub, procédures, Markdown, PDF et autres formats réellement utiles ; étudier les formats et connecteurs disponibles sans revendiquer un import non exécuté.
- Extraction, découpage, métadonnées, liens aux originaux, empreintes, mise à jour différentielle, dédoublonnage et reprise sur incident.
- Documents indexés mais **distincts des souvenirs personnels** : une phrase dans un rapport ne devient pas une décision canonique sans preuve suffisante.
- Préserver la structure et les originaux GitHub/Drive ; n'enregistrer aucun secret dans les artefacts publics.

### Couche C — Recherche hybride FTS5 + sémantique/RAG
- Ajouter une recherche de sens fondée sur embeddings locaux ; évaluer les moyens techniques pertinents (vecteurs indexés dans SQLite ou magasin auxiliaire, par exemple Qdrant/Chroma/FAISS) sur le corpus réel, sans imposer une dépendance disproportionnée.
- Faire coopérer recherche lexicale, filtres de métadonnées, recherche vectorielle et classement des résultats ; produire la provenance consultable de chaque réponse.
- Favoriser un index sémantique reconstructible depuis les données canoniques, plutôt qu'une seconde base de vérité.
- Tester mots exacts, paraphrases, dates, négations, décisions remplacées, documents proches mais distincts, et absence de preuve.

### Couche D — AutoDream nocturne, automatique et persistant
- Créer un service de consolidation nocturne **automatisé par un timer systemd sur le Mac mini**, avec journal de runs, état, reprise idempotente et réglage de l'horaire dans la configuration (horaire à déterminer au déploiement, sans prétendre qu'il est déjà fixé).
- Chaque nuit : analyser les nouveaux échanges texte/voix réellement conservés et les missions/événements reçus ; extraire faits durables et décisions, consolider doublons, relier erreurs aux résolutions vérifiées, détecter contradictions et lacunes documentaires, actualiser les index.
- **Apprentissage opérationnel** : conserver les solutions réellement testées et les échecs, sans transformer une hypothèse ou une synthèse erronée en vérité.
- **Anticipation** : préparer les dépendances, missions en attente et suggestions d'amélioration, sans déclencher de nouvelles missions ni actions sur le matériel par simple inférence.
- Préserver les décisions et autorisations explicites récentes du propriétaire. Respecter les règles de mémoire existantes et le contrôle sur les modifications sensibles ; pas de nouvelles obligations générales d'approbation pour les actions déjà autorisées.
- Fournir un **brief du matin** à consulter depuis les interfaces JARVIS existantes puis JL-03 : faits consolidés, documents indexés, décisions modifiées, contradictions ouvertes, recommandations et preuves associées. Le brief distingue strictement observation, inférence et action exécutée.
- Permettre un déclenchement manuel de diagnostic et un rejeu ciblé **sans doubler les écritures** ; ne pas dupliquer ou relancer aveuglément une nuit déjà achevée.

### Raccordement aux interfaces et agents
- Unifier les accès des conversations texte, des tâches agentiques et de la chaîne vocale LiveKit **vers le même service de mémoire canonique** ; la voix 23D reçue jusqu'ici ne démontrait pas cette persistance.
- Vérifier réellement qu'un élément mémorisé en session vocale est retrouvé dans une autre session vocale et depuis l'interface texte, et inversement.
- Conserver l'interruption LiveKit validée en 23D et l'accès aux outils du broker reçus en mission 24 ; ne pas reconstruire ces composants.

## Exécution et responsabilités

Codex orchestre, développe les capacités manquantes du broker et vérifie indépendamment ; **JARVIS réalise autant que possible l'ingestion, les tests, les contrôles de sa mémoire, les consolidations et les publications de preuves**. Toute capacité créée pour débloquer JARVIS doit lui être confiée pour un retest réel. Exécution sans validation humaine intermédiaire après le lancement de la mission, dans son périmètre autorisé.

Réutiliser les acquis 13C/13F/14A, 23D et 24 ; sauvegardes, migrations idempotentes, conservation des souvenirs, préférences, checkpoints, décisions et journaux. Ne pas exécuter de campagne de réinstallation ou de modification matérielle pour cette mission.

## Réception de la mission unique

1. Migration ou extension de la mémoire existante **sans perte** et restauration vérifiée.
2. Ingestion réelle d'un corpus représentatif provenant des rapports de mission et de documents disponibles, avec métadonnées, dédoublonnage, mises à jour et liens aux originaux.
3. Recherche lexicale et sémantique comparées sur des questions identiques ; provenance et traitement des contradictions vérifiés.
4. Rappel persistant d'une information nouvelle après fermeture puis ouverture d'une autre session, entre voix LiveKit et texte JARVIS, sans régression du barge-in.
5. **Cycle AutoDream réel de bout en bout**, déclenché pour essai puis planifié pour la nuit, avec consolidation traçable, exécution au timer, suivi et reprise idempotente ; aucune mission supplémentaire créée à tort.
6. **Brief du matin réel** produit et consultable, avec preuves et distinction entre suggestion et exécution.
7. Contrôles de non-régression des outils, services, mémoire, GitHub, accès et checkpoints ; preuves attribuées correctement à JARVIS ou Codex.
8. Publication de code, procédures, résultats attendu/réel et rapport global sur une branche dédiée, sans fusion automatique dans main.

**Verdict :** ✅ seulement si l'ensemble des couches intégrées fonctionne dans les essais réels ; ✅🟡 uniquement si les réserves ne bloquent pas l'objectif global ; 🟡 si une couche n'est que préparée, non déployée ou non testée. Les tests simulés, la simple génération de rapports ou le succès des embeddings isolés ne valent pas réception du système complet.

## Références et décisions

- Sources de conception : `Grominet95/jarvis-OS` (Memory Kernel / AutoDream), `sosoj92/reels-vault` (ingestion) ; étudier versions/licences effectives avant réutilisation de code.
- Priorité récente du propriétaire : toutes les couches ci-dessus **dans une seule mission**.
- Le « 24 mémoire » dans le cycle du 19 octobre est un libellé historique : la mission24 effective désigne le broker. Conserver le chantier mémoire jusqu'à attribution d'un nouvel identifiant, sans renuméroter les autres missions.

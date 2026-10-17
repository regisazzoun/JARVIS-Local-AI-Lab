# Bilan agentique JARVIS — mission 00

**Réception : GO AVEC RÉSERVES pour l’exécution documentaire guidée.** Le modèle a réellement utilisé ses outils ; l’autonomie générale sans coordination n’est pas reçue. Le [rapport final](RAPPORT-FINAL.md) et le [registre](REGISTRE-MISSIONS.md) restent la consolidation Codex.

## Les cinq tâches réellement confiées

| Tâche | Opérations JARVIS observées | Résultat et réception Codex |
| --- | --- | --- |
| JARVIS-00-01 | Découverte/lecture par programmes Python via host_exec ; écriture et réparation de son extracteur, puis exécution sur le manifeste élargi | 671 chemins uniques ; 637 du relevé initial couverts, 34 supplémentaires. 671 empreintes concordantes au contrôle. Classement sémantique non exhaustif. |
| JARVIS-00-02 | Lectures ciblées via outils puis rédaction de quinze lots de fiches ; premiers prototypes Python également conservés | Production réelle ; réception avec corrections explicites d’exécutants, fonctions et dépendances. Les originaux erronés ne deviennent pas le registre canonique. |
| JARVIS-00-03 | Lecture de rapports et de cellules exactes des suivis ancien/nouveau ; matrice initiale, révision et complément de sept cas | Évolution des états réellement comparée. Confusion JL-02/Dell n°2 corrigée après diagnostic Codex. Le document n’atteste aucun nouveau déploiement. |
| JARVIS-00-04 | Extraction de citations puis analyse de trois lots de rapports historiques, voix/agent et réceptions récentes | Première grille générique rejetée ; reprise par lectures source. Les tests historiques sont rapportés, jamais présentés comme relancés par JARVIS dans 00. Les détails non lus restent réservés. |
| JARVIS-00-05 | Lecture de ses propres matrices et analyses, puis rédaction de la synthèse finale avec notes de réception Codex explicitement attribuées | Synthèse réelle distincte du rapport Codex. Les premières sorties simulées/incomplètes et la réponse vide sans écriture sont rejetées. La dernière synthèse est reçue dans les limites de ses extraits et de son guidage. |

Les fichiers originaux expurgés sont dans [jarvis/](jarvis/). Voir surtout [inventaire](jarvis/INVENTAIRE-LOCAL-JARVIS.json), [fiches assemblées](jarvis/FICHES-MISSIONS-JARVIS.md), [concordance](jarvis/CONCORDANCE-JARVIS.md), [preuves](jarvis/PREUVES-JARVIS.md) et [synthèse](jarvis/SYNTHESE-AUTONOME-JARVIS.md). Les [corrections sémantiques](CORRECTIONS-RESULTATS-JARVIS.md) sont une contribution Codex, sans réécriture silencieuse des originaux.

## Mécanisme réel et traçabilité

Les premiers envois ont utilisé l’API conversationnelle et le planificateur durable existants. Devant les boucles de lectures et réponses vides, Codex a développé [un client de mission](../../../agentic/mission00/README.md) réutilisant les classes installées Core, Memory et Registry, le véritable transport Ollama et le broker propriétaire. Aucune réponse modèle ni invocation d’outil n’a été simulée. Les écritures ont eu lieu dans `/var/lib/jarvis/projects/mission00` sur Debian réel, par les mécanismes hôte existants.

Le client guidé expose d’abord les lecteurs, puis l’écriture du seul fichier attribué sur une génération suivante. Les sélecteurs renvoient des données réellement lues, sans verdict automatique. Le contrôleur s’arrête après écriture effective ; il ne fabrique pas une clôture conversationnelle. Codex relit et reçoit séparément. Ce client n’est pas un nouveau service ni un nouveau moteur d’exécution ; ses conversations rejoignent la mémoire canonique. Ses tâches CLI ne sont pas prétendument toutes des missions durables visibles dans le Launcher.

[PREUVES-AGENTIQUES.json](PREUVES-AGENTIQUES.json) conserve **53 essais/lots**, **276 appels d’outils observés** et **38 retours d’échec**. Ce compteur comprend les essais infructueux et les tâches mises en file puis interrompues ; il ne représente pas autant de succès. Une erreur sémantique peut aussi suivre un outil techniquement réussi. Chaque entrée conserve instruction envoyée, mécanisme, modèle, heures de début/dernière activité, outils, arguments expurgés, erreurs et références de preuve. Les contenus écrits sont référencés par empreinte/longueur ; les fichiers produits et leurs empreintes publiées sont séparés. Les horloges sont réelles, avec UTC ou décalage explicite.

Modèles effectivement essayés : `llama3.1:8b`, `ministral-3:14b-instruct-2512-q4_K_M`, `qwen3.5:27b-q4_K_M`. Les productions retenues sont celles de Qwen. Les essais Ministral ont échoué au transport/prédiction ; Llama a produit des exemples ou placeholders non reçus. Cela ne révoque pas leurs validations d’inférence antérieures dans d’autres scénarios.

## Répartition des contributions

**JARVIS** : choix et appel effectif d’outils, programmes d’inventaire puis réparation, lectures, interprétations et rédaction des lots, matrices, grille reprise et synthèse. Le titre « autonome » du fichier de synthèse est historique ; sa production actuelle est guidée.

**Codex** : lecture des directives, inventaire GitHub, archives et compléments locaux, manifeste et droits temporaires de lecture, raccordement du client, sélecteurs, découpage des tâches, diagnostics, assemblages mécaniques, corrections documentaires, corroboration privée expurgée, registre, README/SUIVI/ROADMAP, récupération de 129 documents/preuves sur JARVIS et publication. Les assemblages et notes fournies au modèle sont identifiés comme tels dans le manifeste des artefacts.

## Erreurs conservées et limites

La première passe d’inventaire ne contenait que 63 fichiers. Une variable non initialisée a ensuite limité un résultat à 141 entrées ; JARVIS l’a corrigée avant les passages 218 puis 671. Les générateurs de fiches ont rencontré des clés incohérentes, un état de section nul et des corrections invalides. Des lectures répétées, un format JSON d’appel incorrect, des réponses vides et une clôture non aboutie ont été enregistrés. Une date 2025 inventée dans un brouillon a été rejetée ; les appels réels horodatés restent la référence.

Les fiches attribuant à JARVIS des opérations Codex historiques, les dépendances humaines inventées et les causalités RAID affirmées sont corrigées dans la consolidation. La référence 04S, signalée dans les fiches puis vérifiée par Codex dans 04T/04U, a été ajoutée À confirmer avec ses sources manquantes ; aucun trou de numérotation n’est comblé arbitrairement.

Les lectures machine intégrales ne signifient pas analyse de chaque ligne par le modèle. Les lectures interprétatives sont bornées et identifiées. Les journaux privés du Dell/11B ont été contrôlés par Codex, pas transmis au modèle. Les anciens états running restent datés ; le [checkpoint 11B](CHECKPOINT-11B-OBSERVE.json) observé est incomplet après cinq tentatives.

La politique du broker conserve ses protections et droits permanents 11B. Les lectures documentaires ajoutées pour cette mission sont retirées après la fin des tâches, avec contrôle distinct. Aucun compte ni clé n’a été recréé ; aucun service n’a été redémarré ; aucun disque, RAID ou BIOS modifié. Le [contrôle final](CONTROLES-DOCUMENTAIRES.json) précise les vérifications réellement exécutées.

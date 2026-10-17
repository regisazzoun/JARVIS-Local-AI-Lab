# Index et méthode de lecture des sources

**Provenance :** Codex produit cet index et la consolidation ; les résultats originaux de JARVIS sont conservés distinctement dans `jarvis/` avec leur réception et leurs erreurs.

## Inventaires exhaustifs

- [GitHub](INVENTAIRE-GITHUB.json) et [CSV](INVENTAIRE-GITHUB.csv) : 963 entrées dépôt/branche/document, commit, empreinte, URL, dates disponibles et correspondance locale. Cliché avant la publication 00 : trois dépôts, quinze branches et six PR préexistantes.
- [Relevé local initial Codex](INVENTAIRE-LOCAL-COMPLEMENT-CODEX.json) : 637 fichiers Markdown, racines et limites d’accès ; environnements, runtime, .git et secrets exclus.
- [Inventaire original JARVIS](jarvis/INVENTAIRE-LOCAL-JARVIS.json) : 671 chemins et empreintes ; [réception](RECEPTION-INVENTAIRE.json). [Consolidation par document](INVENTAIRE-LOCAL-CONSOLIDE.json) : fonctions et rattachements ajoutés par Codex, informations insuffisantes marquées À confirmer.
- [Archives](INVENTAIRE-ARCHIVES.json) : 94 archives inspectées en lecture seule, 23 158 membres catalogués ; 323 membres Markdown / 298 contenus uniques, tous déjà retrouvés hors archives. Les binaires et journaux privés ne sont pas repris.
- [Autres formats](AUTRES-FORMATS-CODEX.json) : 31 candidats TXT/JSON examinés structurellement. Les rapports de compétences du projet tiers JarvisVoice sont des sources d’étude, pas des opérations JARVIS. Aucun rapport PDF/DOCX supplémentaire retrouvé par cette découverte de noms.
- [129 documents et preuves récupérés](RAPPORTS-RECUPERES.json) : sources locales réelles, destinations, empreintes des originaux et des copies expurgées. [100 rapports/fiches historiques](../historique/README.md), [JL-01](../JL-01/RAPPORT-JL-01.md) et [JL-02](../JL-02/RAPPORT-JL-02.md).

Les métadonnées contenant des identifiants uniques sont expurgées ; les empreintes décrivent les contenus sources. Une date Git n’est pas une date de test. Un fichier découvert et chargé par un programme ne signifie pas que chaque ligne a été interprétée par le modèle.

## Sources de référence actuelles

| Périmètre | Rapports et branches consultés |
| --- | --- |
| Directives / pilotage | AGENTS.md, charte, README, SUIVI, ROADMAP, chronologie et décisions récentes du propriétaire |
| Historique | Fiches des branches consolidation/réorganisation PR2/3 et rapports originaux 03–13A sur JARVIS ; rapports racine 02 et 02B |
| 13B / 13C / 13D | Fiches, rapports et états successifs avec leurs réserves et sous-missions d’accès |
| 13E | Rapport, architecture, tests et incidents ; branche mission13e-integration-20261014 / PR1 |
| 13F | Débrief, rapport, architecture, tests, incidents et reprise ; branche codex/mission-13f-20261014-a0ed2a / PR4 |
| 13D-E / Dell n°1 | RECEPTION-MISSION14.md, rapport final et reprise ; branche codex/mission-13de-preparation au commit 6dd5f57 / PR5 |
| 11-Agentic / 11B | Rapports, habilitations et raccordement ; branches codex/mission-11-agentic-enablement, jarvis/mission-11b-compute-expansion, puis codex/jl-02-launcher-v2 pour les dernières directives |
| JL-01 / JL-02 | Dépôts distincts JARVIS-Launcher et JARVIS-Launcher2, rapports d’exécution, tests, preuves publiques et bilan agentique |
| 14A / 14 | Critères agentiques, roadmap et décision propriétaire : Dell n°2 réservé à JARVIS |
| 15A / 15B | Cahiers natifs macOS/iOS, cinq incréments chacun ; décisions iOS gratuit et indépendance de 14 |

Les chemins et URL détaillés, y compris les documents publiés uniquement hors main, restent dans les inventaires et les sources de chaque ligne du [registre](REGISTRE-MISSIONS.json). Les textes externes cités par un rapport sont des références historiques ; aucun nouvel audit de leurs produits n’est revendiqué.

## Corroboration privée, sans publication des journaux

Codex a contrôlé les champs utiles de `complete.json`, `progress.json`, `applications-after-reboot.json` et `integration-results.json` du dernier déploiement, ainsi que `before.json`/`after.json` de 11B. [Extraction expurgée](CORROBORATION-PRIVEE-CODEX.json) : dix-huit états Dell validés, treize appels avant et seize après du scénario 11B réussis, références SSH/Ansible conservées. Ces fichiers privés ne sont ni transmis au modèle ni publiés intégralement. Aucune campagne n’est relancée.

Le [checkpoint durable 11B](CHECKPOINT-11B-OBSERVE.json) est observé incomplet après cinq tentatives. Cette observation ne remet pas en cause le raccordement reçu et ne clôture pas Compute Expansion. Les [niveaux de preuve consolidés](NIVEAUX-PREUVE-CONSOLIDES.md) distinguent étude, installation, exécution, test et réception.

## Exécution et contrôles de la mission 00

[Instructions et traces réelles](PREUVES-AGENTIQUES.json), [bilan agentique](BILAN-AGENTIQUE-JARVIS.md), [corrections des sorties modèle](CORRECTIONS-RESULTATS-JARVIS.md), [anomalies documentaires](ANOMALIES-DOCUMENTAIRES.md) et [contrôles finaux](CONTROLES-DOCUMENTAIRES.json). Les sorties incorrectes restent des traces, sans devenir des directives.

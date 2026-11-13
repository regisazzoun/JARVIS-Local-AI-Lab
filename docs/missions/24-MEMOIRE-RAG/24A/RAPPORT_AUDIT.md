# Mission JARVIS 24A — Audit en lecture seule

**Date : 13 novembre 2026, heure de Paris. Statut : 🟡 COMMENCÉE / EXÉCUTÉE PARTIELLEMENT — réception 24A non acquise.**
**24B : NON LANCÉE, en attente de validation explicite. Aucun GO de production.**

## Autorité et référence
Demande explicite du propriétaire dans ce chat : lancer 24A et publier rapport/preuves sur branche/PR.
Plan PR [#49](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/49), branche docs/mission-24-rag-plan-20261113, commit figé caa6f5e1c9a126bec953de3d418378192f7318af ; plan blob dd59e163f5d0d45058a01d98a67c3f8901a24287.
Directives consultées : AGENTS.md, docs/CHARTE_DIRECTIVES_JARVIS.md, SUIVI.md, ROADMAP.md, plan 24 et utilisation/architecture 13F historiques. Autorisations préservées : lectures des sources et services par accès existants, rédaction/publication documentaire. Restrictions actuelles : aucune modification production, aucun secret publié, aucune activation 24B, aucune fusion.
SUIVI indique encore 24 planifiée : état documentaire antérieur au déclenchement présent, pas preuve d'exécution.
L'inspection locale utilise uniquement les anciens espaces Codex sélectionnés et les métadonnées SSH ; aucune clé privée ni base n'est copiée.

## Résultat et limites essentielles
L'arbre GitHub figé a été inventorié (328 entrées, 253 fichiers, truncated=false) ; sélection des directives réellement lue, pas les 253 contenus.
Drive a fourni le document S407, l'export Télémaintenance et le cadrage RAG. Leurs résumés expurgés et liens sont en [preuves](preuves/EXTRAITS_EXPURGES.md). La [matrice](MATRICE_SOURCES.csv) distingue accès réels, droits inconnus et états rapportés.
La clé SSH disponible est refusée sur le Mac mini (Tailscale et LAN) et Dell1 direct ; agent SSH sans identité chargée. Les hôtes ont été vérifiés contre known_hosts existant, sans modifier les empreintes ni tenter de mot de passe. Pas de contournement, de nouvelle identité ou d'hôte inconnu ajouté.
Un GET vers la racine du service documenté historiquement sur le Mac mini échoue côté transport (URLError, aucun statut HTTP). Cela ne prouve ni arrêt du service local, ni refus applicatif.
Conséquence : base SQLite réelle, tables/index, connecteurs installés, sauvegardes, API authentifiée et services Dell/Raspberry non inventoriés en live. **Aucune restauration, aucun test FTS5 et aucune réponse JARVIS obtenus.** Le schéma v3 et runtime/memory.sqlite sont des références 13F historiques, pas des constatations actuelles.

## État des critères
| Critère | Statut | Preuve / limite |
|---|---|---|
| Lecture plan et référentiels | vérifié sur sélection | commit et blob figés |
| Inventaire GitHub | exécuté, arbre vérifié | 253 fichiers, contenu partiel |
| Inventaire Drive | exécuté partiellement | 3 requêtes bornées, 3 documents lus |
| Matrice sources/propriétaires/ACL | exécutée partiellement | propriétaires réels non déterminés pour Drive |
| Mémoire réelle/API/services | échec d'accès SSH ; inventaire non exécuté | sorties expurgées OBSERVATIONS.json |
| Baseline documentaire S407 | exécutée | BASELINE_S407.md et mesures par appel |
| Baseline moteur JARVIS | non exécutée | accès authentifié indisponible |
| Sauvegarde/restauration sur copie | non exécutée | aucune base disponible ; ne pas créer une fixture pour prétendre valider la production |
| ACL lecture positive | vérifiée sur S407 | fetch réussi, rôles owner/writer agrégés |
| ACL négative/révocation/isolation RAG | non exécutées | aucune identité secondaire ou copie dédiée disponible |
| Expurgation livrables | revue par liste blanche | aucun export brut, base, identifiant matériel ou secret |
| 24B | prévue seulement | attente de validation propriétaire |

## Découvertes vérifiées et anomalies
1. **A01 — accès réel bloqué.** Le réseau atteint un serveur SSH mais l'authentification échoue (code 255). Cela ne démontre ni perte globale des accès existants ni révocation de la clé côté serveur. Reprendre avec un accès existant confirmé par le propriétaire.
2. **A02 — FusionPBX dispose d'une source documentaire.** L'export du 6 novembre contient un constat utilisateur du 5 novembre : services FreeSWITCH/Nginx/PostgreSQL actifs et accès via Dell1. Le document S407 seul ne prouvait pas l'IPBX ; l'absence totale de documentation FusionPBX n'est donc pas retenue. Configuration actuelle et état live : non vérifiés.
3. **A03 — secrets à exclure à la source.** L'export rapporte un dépôt de mots de passe dans un tableau partagé. Ses métadonnées montrent 1 rôle owner et 4 writer individuels ; le contenu n'a pas été ouvert. Risque de source sensible identifié, pas une fuite publique démontrée ni une remise en cause des décisions de partage du propriétaire. Exclure le fichier entier de l'ingestion pilote tant qu'une vue expurgée indépendante n'est pas disponible.
4. **A04 — chemin/source institutionnelle non établis.** Le parent réel du document est Mon Drive / SEP CIEL / Archi-Reseau / 00-Documentation. Le libellé « Téléphonie » demandé ne correspond pas à son parent. Le caractère institutionnel Éducation/lycée n'est pas prouvé par les métadonnées disponibles.
5. **A05 — fraîcheur et doublons.** Le document récent déclare les 24 configurations historiques anciennes. Plusieurs guides téléphones homonymes et de même taille apparaissent en recherche : candidats doublons, non certifiés sans hash. Une date 1979 apparaît dans des métadonnées de supports anciens : date technique non fiable comme preuve de fraîcheur métier. La recherche n'est pas un inventaire complet.
6. **A06 — droits excessifs disponibles pour une simple lecture.** Les rôles writer observés ne sont pas des jetons limités à la lecture. 24A n'a utilisé que des lectures ; les ACL applicatives effectives pour JARVIS et l'isolation des projets restent à tester.
7. **A07 — continuité non démontrée.** Les anciens livrables Codex locaux sont accessibles ; aucun mécanisme de dépôt canonique automatique de toutes les conversations Work/ChatGPT/Codex n'a été prouvé.

## Baseline et scénario salle 407
Voir [réponse de référence et protocole](BASELINE_S407.md) et [mesures](preuves/BASELINE.json).
Deux sources de scénario effectivement lues et citées, plus une source d'orientation. Réseau bancs 1–2 documenté, dix téléphones banc 1 repérés, SIP/appels restant à recetter ; bancs 3–6 restant à déployer. IPBX documenté historiquement par une autre source.
Mesures du connecteur Codex uniquement : elles ne sont pas une mesure du RAG JARVIS, ne permettent pas d'attribuer une hallucination à ce moteur et ne valident pas l'essai vocal JM-01.
Les citations ont été résolues par lecture authentifiée dans cette session ; aucun accès public/anonyme garanti.

## Lecture seule et conservation des preuves
Actions distantes : GitHub GET/lecture connecteur, Drive recherche/fetch/métadonnées, tentatives SSH strictes avec commande de consultation (non exécutée car authentification refusée), GET HTTP racine sans corps conservé.
Aucune migration, ingestion, réindexation, édition ACL, redémarrage, changement de compte, installation ou écriture de données de production. Les journaux d'accès des services peuvent enregistrer les lectures/tentatives.
Écritures limitées aux livrables locaux et à la branche documentaire demandée. Aucune fusion.
Les preuves publiées sont des observations structurées expurgées, pas des journaux bruts complets. Leurs hashes assurent l'intégrité du paquet publié, pas l'authenticité cryptographique des sources ni une sauvegarde de la production.
Le contrôle de secrets du paquet est une revue de contenu généré par liste blanche complétée par un balayage de motifs ; pas une garantie exhaustive de détection de secrets dans les sources non lues.

## Backlog vérifiable pour achever 24A
| Priorité | Écart | Action autorisée à reprendre | Critère de clôture |
|---|---|---|---|
| P0 | A01 accès | utiliser un accès SSH existant valide, conserver empreintes | identité/cible confirmées, consultation réussie |
| P0 | base réelle inconnue | inventorier chemin canonique, mode/owner, schéma/index/version et volumes sans exporter le contenu sensible | preuve expurgée issue de la base réelle |
| P0 | copie/restauration absente | snapshot cohérent vers espace privé d'audit uniquement, source ouverte mode=ro, restauration dans une deuxième copie privée | integrity_check, schéma/comptages comparés, aucun chemin production en destination |
| P0 | baseline JARVIS absente | sur copie/corpus figé, question S407, journal requêtes/outils/documents/réponse et durée bout en bout | trace expurgée rejouable, pas de mémorisation de test en production |
| P0 | ACL incomplètes | identités de test autorisées/copie, accès positif et négatif, isolation, révocation sur copie | refus effectif sans fuite, citation inaccessible gérée |
| P1 | services non observés | inventaire lecture seule Mac/Dell/Raspberry via alias existants | santé actuelle, API et connecteurs avec preuves datées |
| P1 | sources sensibles/anciennes | exclusion du tableau d'accès et des identifiants, sélection des références fraîches, hash des copies autorisées | manifeste pilote expurgé et dédoublonné |
| P1 | sources dispersées | confirmer propriétaires/Drive institutionnel, originaux, exports Work/Codex et politique de rétention | chemins et droits explicitement établis |

## Décision de sortie
**🟡 24A partiellement exécutée, preuves documentaires publiables ; critères de sortie non satisfaits.** Les échecs d'accès et tests non exécutés restent ouverts. Reprise 24A requise avant réception. **24B non démarrée et subordonnée à validation explicite.**

# Mission JARVIS 24A — Audit en lecture seule

**13 novembre 2026 — reprise vérifiée jusqu'à 21 h 40 (Paris).**
**Statut : 🟡 audit réellement exécuté, réception 24A avec critères encore ouverts. 24B NON LANCÉE.**
Rapport initial corrigé après récupération des accès existants ; les premiers refus restent conservés comme observations historiques.

## Autorité et références
Demande du propriétaire : audit des sources/services réels, preuves expurgées et publication sur branche/PR, aucune modification de production ni lancement 24B.
Plan [PR #49](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/49), branche docs/mission-24-rag-plan-20261113, commit caa6f5e1c9a126bec953de3d418378192f7318af, blob du plan dd59e163f5d0d45058a01d98a67c3f8901a24287.
Directives consultées : AGENTS.md, CHARTE_DIRECTIVES_JARVIS.md, SUIVI.md, ROADMAP.md, plan 24, architecture/utilisation 13F ; puis code réellement déployé, pont de continuité et discussion « Tellemaintenance LCC » indiquée par le propriétaire.
AUTORISÉ : lectures, accès existants, copies privées d'audit, tests sur copies et publication documentaire expurgée.
INTERDIT : migration/ingestion/réindexation de production, modification des comptes/ACL/services, secret publié, fusion ou 24B sans validation.
La discussion historique est utilisée comme source d'accès et de contexte, pas comme autorisation de reprendre ses opérations anciennes.

## Résultat essentiel
- **Mac mini : accès SSH rétabli avec la clé existante, sans modification.** Elle était chiffrée : sa phrase existante, retrouvée dans la discussion, permet la connexion. Les refus BatchMode ne prouvaient pas une expiration ni une révocation.
- **Dell1 : accès par mot de passe existant réussi**, puis alias existants depuis Mac mini confirmés. **Dell2 : alias existant réussi**, services IA/VNC/SSH actifs. **Raspberry FusionPBX : port SSH joignable depuis Dell1**, session authentifiée et services PBX non revalidés.
- Mémoire historique 13F active sur **/opt/jarvis/conversation/runtime/memory.sqlite**, schéma v3, FTS5. La copie sous ~/JARVIS/conversation est ancienne et n'est pas la base du service.
- **Open WebUI natif v0.12.0 est aussi actif**, avec SQLite webui.db, Chroma et un pont de continuité. La mémoire historique ne décrit donc pas, seule, le parcours courant.
- Deux snapshots cohérents obtenus par SQLite backup avec source **mode=ro**, destination en mémoire puis flux SSH privé vers ce poste. Restaurations locales vérifiées ; aucune base ou sauvegarde brute publiée.
- Baselines réelles : FTS5 sur copie et recherche mémoire native authentifiée sur service actif. La synthèse finale complète dans le client JARVIS/JM-01 reste non rejouée.

## Matrice et inventaire
Voir [MATRICE_SOURCES.csv](MATRICE_SOURCES.csv), [MAC_LIVE.json](preuves/MAC_LIVE.json), [REPRISE_DELL1.json](preuves/REPRISE_DELL1.json), [CONNECTEURS_SAUVEGARDES.json](preuves/CONNECTEURS_SAUVEGARDES.json).
GitHub : arbre figé complet, 328 entrées/253 fichiers, non tronqué ; directives sélectionnées lues, pas les 253 contenus.
Drive : 3 requêtes ciblées bornées, 3 documents de contexte/scénario lus, métadonnées et ACL choisies. Le tableau d'accès a ensuite été consulté **uniquement pour l'authentification**, sur instruction explicite du propriétaire ; ses valeurs restent hors corpus et hors preuves.
Les propriétaires Drive individuels ne sont pas identifiés par les métadonnées normalisées ; aucun rôle nominal inventé.

### Mémoire historique réelle
Snapshot : 6 320 128 octets ; 102 documents, 20 projets, 419 messages, 5 souvenirs, 4 préférences, 13 819 entrées tool_audit.
FTS5 documents/messages/souvenirs présents. Schéma versions 1/2/3. Intégrité ok, aucune violation de clé étrangère.
102 documents sans projet global ; dernier created documentaire : 31 octobre 2026. Aucun contenu exactement dupliqué ; 3 lignes supplémentaires partagent source/projet avec une autre version (pas des doublons de contenu établis).
Les 102 champs source n'ont pas de lien Google/GitHub reconnu par le comptage simple : cela ne prouve pas l'absence de liens dans le contenu.
Droits : base/auth/credentials/traces en 0600, répertoire runtime/backups en 0700 ; test Unix sous utilisateur non privilégié : lecture de la base refusée.
33 sauvegardes memory-*.sqlite en 0600 ; dernière au 13 novembre 00:00 Paris. Intégrité de cette sauvegarde historique vérifiée, schéma v3/102 documents. Restauration testée sur le snapshot courant, pas sur chacune des 33 sauvegardes.
Voir [SQLITE_AUDIT.json](preuves/SQLITE_AUDIT.json) pour schéma/index/comptages et hashes des sources réellement lues.

### Mémoire native et continuité
Snapshot webui.db : 8 499 200 octets, intégrité ok ; 46 mémoires, 50 notes, 1 base de connaissances, 6 fichiers, 2 liaisons knowledge_file, 3 utilisateurs, 3 access_grant.
Chroma existant observé, chroma.sqlite3 de 2 400 256 octets. Aucun nouveau modèle ni index déployé, aucune ingestion ou réindexation ; la requête de test utilise la fonction d'embedding déjà installée.
Pont actif : lecture des documents/préférences historiques et de 9 JSON de synthèses sélectionnés, écriture habituelle du pont vers notes/mémoires natives. **24A n'a pas exécuté ce pont** ; timer et code seulement inspectés.
20 chemins d'archives héritées et 9 chemins de synthèses retrouvés dans les mémoires natives. Ce mécanisme concret remplace l'hypothèse initiale d'absence de pont, mais ne démontre pas une récupération universelle des conversations.
Aucun lien vers les deux documents récents S407/télémaintenance de référence retrouvé dans les 46 contenus mémoire ; les notes, fichiers et conversations n'ont pas fait l'objet d'une recherche exhaustive.
Voir [NATIVE_SQLITE_AUDIT.json](preuves/NATIVE_SQLITE_AUDIT.json).

## Baseline recherche/RAG salle 407
[BASELINE_S407.md](BASELINE_S407.md) distingue trois mesures, sans mélanger leurs latences.

1. **Connecteur documentaire Codex** : S407 du 12 novembre et Télémaintenance du 6 novembre réellement lus ; synthèse de référence sourcée. Source RAG du 12 novembre lue pour le cadrage.
2. **Moteur historique, code déployé sur copie réelle** : sans projet, 0 document pour S407/salle 407/FusionPBX/SIP. Sur l'ensemble des projets, « salle 407 » donne 5 correspondances FTS via OR, dont 4 retournées par la limite ; S407/FusionPBX/SIP : 0. Ce n'est pas une preuve de 5 documents pertinents : « salle OR 407 » est une recherche large.
3. **Mémoire native live authentifiée** : S407 → 3 résultats (7,50 ms), salle 407 → 0 (6,69 ms), FusionPBX → 0 (6,38 ms), SIP → 1 (6,45 ms). Une requête vectorielle existante sur la question complète donne 4 éléments en 426,30 ms ; 2 mentionnent S407/salle 407, aucun FusionPBX. Une seule mesure vectorielle, pas un percentile ni une comparaison de gain.
Les contenus natifs retournés ont été reçus par le script en mémoire, puis seuls comptes, identifiants hachés et métriques ont été conservés. Pas de réponse finale LLM, de citations générées ou d'hallucinations attribuables au client évaluées.
Voir [BASELINE_NATIVE_LIVE.json](preuves/BASELINE_NATIVE_LIVE.json) et [ACL_RECHERCHE.json](preuves/ACL_RECHERCHE.json).

## Tests réellement exécutés
| Test | Résultat | Limite |
|---|---|---|
| Clé SSH Mac mini avec déverrouillage existant | vérifié, accès réussi | aucun changement de clé/compte |
| Dell1 et Dell2 | accès authentifié, services IA/VNC actifs | pas de benchmark ni reboot |
| Raspberry | TCP SSH joignable depuis Dell1 | pas de session/service PBX live validé |
| Snapshot cohérent 13F + restauration locale | intégrité/schema/comptages concordants | base privée, aucune restauration production |
| Snapshot natif + restauration locale | intégrité/comptages concordants | vecteurs Chroma non restaurés : pas une restauration RAG complète |
| SQLite mode=ro | écriture refusée sur snapshot source local | tentative d'écriture jamais dirigée vers production |
| Unix utilisateur non privilégié | base historique illisible | ne couvre pas tous les groupes/ACL système |
| API historique sans session | search/memories/export → 401 | health/session lisibles volontairement |
| Host/Origin invalides | 403 sur API historique | pas de balayage offensif |
| API native | liste authentifiée 200/46 mémoires ; sans jeton 401 | identité secondaire/révocation native non testées |
| Filtre projet historique sur copie | global + bon projet visibles ; autre projet absent | filtre de classement, pas ACL par utilisateur |
| Auth historique sur fixture locale | mauvais secret refusé, bon login accepté, logout invalide le jeton | pas de login/révocation production |
| Lecture Drive S407 et ACL | contenu lu, 1 owner/4 writer individuels | pas d'identité secondaire ni révocation réelle Drive |
| Motifs sensibles dans contenus | 0 clé privée/jeton/Bearer détecté ; 2 documents historiques avec libellé de credential | candidats à revue, ni preuve d'absence de secrets ni secrets confirmés |
| Expurgation publication | liste blanche + scan du paquet | pas de garantie sur sources privées non auditées |

## Anomalies et backlog vérifié
| ID | Priorité / état | Fait et suite |
|---|---|---|
| A01 | résolu | refus initial dû à clé verrouillée ; accès existant réutilisé. Ne pas remplacer la clé. |
| A02 | P1 / documenté | FusionPBX est documenté historiquement dans Télémaintenance ; sa configuration actuelle reste non vérifiée. |
| A03 | P0 avant ingestion | tableau d'accès sensible : exclure intégralement du corpus ; consultation ponctuelle de coffre distincte de l'indexation. 2 contenus historiques portent un marqueur de credential, valeurs non publiées, revue privée à terminer. |
| A04 | P1 | document S407 sous Mon Drive/SEP CIEL/Archi-Reseau/00-Documentation, pas sous Téléphonie ; identité institutionnelle du Drive non établie. |
| A05 | P1 | références Cisco de 24 configurations explicitement anciennes ; guides homonymes candidats doublons non certifiés. Versions documentaires source/projet à gérer. |
| A06 | P0 avant corpus multiutilisateur | historique sans champ ACL par document ; filtre project contrôlé par l'appelant. Natif scoped user_id, access_grant présent ; propagation ACL Drive et révocation multiidentité non démontrées. |
| A07 | P1 | pont de continuité réel, mais seulement archives et synthèses sélectionnées ; pas de collecte universelle des conversations. |
| A08 | P0 de cadrage | écart entre plan 24 actuel et runtime : Open WebUI natif/Chroma/pont/anciens répertoires mission24 déjà présents. Clarifier l'autorité logique et le parcours à recevoir avant 24B, sans recréer une base concurrente. |
| A09 | P1 recherche | document_search coupe aux 10 premiers termes : la question complète perd salle/407/SIP/FusionPBX dans ce moteur historique. OR, LIMIT 4 puis injection 2 sans ORDER BY de pertinence explicitée. Observation de code, pas défaut automatiquement attribuable au natif. |
| A10 | P1 corpus | aucun résultat natif FusionPBX malgré sa source Drive accessible à Codex ; aucun lien des deux sources récentes dans les 46 mémoires. Vérifier la couverture réelle du connecteur/notes/fichiers avant de conclure à une absence globale. |
| A11 | P1 réception | scénario écrit complet dans le client courant non rejoué ; qualité, citations, latence bout en bout et erreurs de synthèse restent à mesurer sur copie avec outils strictement limités à la lecture. |
| A12 | P1 exploitation | traces historiques ~454 Mo, base missions ~3,19 Go observée ; rétention à inventorier séparément. Aucune suppression/rotation imposée par 24A. |

Les services Google education/personal sont installés et configured=true via leur pont existant. Cela ne prouve pas une lecture Drive réussie depuis JARVIS : les lectures Drive de cet audit utilisent le connecteur Codex. Ne pas confondre leurs identités, scopes et résultats.
Aucun GO n'est déduit des seuls fichiers présents, timers actifs ou récits historiques.

## Conservation, non-modification et publication
Écritures de 24A : espace local privé d'audit, copies locales de test, livrables expurgés et branche documentaire.
Sur production : lectures SSH/SQL/HTTP, inspection de code et métadonnées ; les POST natifs utilisés sont **search/query de lecture** après inspection des handlers, aucun endpoint de mutation appelé. Aucun login production généré ; un jeton existant a été utilisé en mémoire.
Aucune migration, ingestion, réindexation, édition ACL, redémarrage, changement de compte, installation distante ou restauration production. Les journaux d'accès habituels et les tâches préexistantes peuvent évoluer pendant l'audit ; absence de changement de hash production non revendiquée.
Preuves : observations structurées, schémas et métriques autorisés, pas exports bruts. Copies SQLite avec données privées et aides d'authentification hors outputs et hors GitHub.
Le manifeste SHA-256 couvre le paquet publié, pas une attestation cryptographique des sources.
Voir [PROCEDURE_REPRODUCTION.md](PROCEDURE_REPRODUCTION.md) pour rejouer les mesures et limites.

## Verdict 24A et porte 24B
**Audit réel largement exécuté ; réception 24A encore incomplète** : synthèse client complète, propagation ACL/révocation multiidentité, restauration cohérente du RAG natif incluant vecteurs et couverture live PBX/Cisco restent ouverts.
Les résultats positifs SQLite/restauration/recherche/contrôle d'accès sont vérifiés dans les périmètres ci-dessus ; les anomalies ont un backlog exploitable.
**24B non lancée. Validation explicite du propriétaire indispensable avant toute ingestion ou évolution de schéma/index. Aucune fusion automatique.**


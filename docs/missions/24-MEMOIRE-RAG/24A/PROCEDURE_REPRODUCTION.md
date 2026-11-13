# Reproduction de 24A — accès et copies privées

## Préconditions
Réutiliser les alias/hôtes déjà épinglés et l'accès propriétaire existant. Ne pas remplacer de clé ni désactiver StrictHostKeyChecking.
Une clé privée SSH ordinaire n'a pas d'expiration intrinsèque. Ici, elle était chiffrée : la phrase existante a été utilisée sans stockage dans le trousseau ni changement de clé. Une session/certificat peut, elle, expirer ; aucune expiration n'a été diagnostiquée.
Les secrets d'authentification et les snapshots restent dans un dossier privé mode 0700, fichiers 0600. Aucun de ces fichiers ne rejoint GitHub.
Lire AGENTS/charte/plan, les chemins effectifs du service et le code live avant d'exécuter un contrôle. Ne pas relancer les timers ou les ponts de synchronisation.

## Sources et versions
- Plan figé : commit caa6f5e1c9a126bec953de3d418378192f7318af.
- Mémoire historique effective : /opt/jarvis/conversation/runtime/memory.sqlite, confirmée par WorkingDirectory et commande de service.
- Natif : conteneur jarvis-open-webui, image v0.12.0 ; volume jarvis-open-webui-data/webui.db, plus Chroma existant.
- Hash de memory.py live : 66acf6954f164acb4b989011029a85a063a481aa07ce52a519b3516fdfc35cc2. Les autres hashes live sont dans SQLITE_AUDIT.json.
- Dépendances des tests SQLite : Python standard sqlite3, import du seul module memory.py copié, jamais lancement de server.py/Core/worker ni import du pont à effets de bord.

## Snapshot cohérent sans écriture distante
Sur la source, ouvrir SQLite avec URI mode=ro ; utiliser l'API backup vers :memory:, puis serialize pour envoyer le snapshot via le flux SSH existant vers le dossier privé local.
Ne pas faire une simple copie du fichier pendant une transaction/WAL. Ne pas utiliser une destination de restauration sous /opt, le volume Docker ou le runtime distant.
Pour webui.db, la source réelle est dans le volume Docker. L'accès administrateur existant a servi uniquement à sa lecture. La base sérialisée peut conserver le drapeau WAL : lire le snapshot privé figé avec mode=ro&immutable=1. **Ne jamais utiliser immutable=1 sur une base de production en évolution.**

Extrait de la lecture source utilisée :
~~~python
source = sqlite3.connect("file:" + chemin_source + "?mode=ro", uri=True)
snapshot = sqlite3.connect(":memory:")
source.backup(snapshot)
flux_prive.write(snapshot.serialize())
source.close()
snapshot.close()
~~~

## Inventaire et restauration sur copie
Sur les snapshots locaux :
1. PRAGMA integrity_check et PRAGMA foreign_key_check (historique).
2. Inventorier sqlite_master (type/name/tbl_name/sql), PRAGMA table_info et SELECT COUNT(*) par table. Ne pas exporter SELECT * de contenu.
3. Lire schema_version pour l'historique, et compter documents/projets/sources/versions/doublons par hash en mémoire. Ne publier que les agrégats.
4. Restaurer l'historique avec Memory.restore vers **un fichier local neuf**, puis comparer schéma/comptages/intégrité.
5. Restaurer le natif avec SQLite backup vers un autre fichier local privé et comparer intégrité/comptages.
6. Les vecteurs n'ont pas été copiés/restaurés : ne pas annoncer une restauration applicative complète du RAG natif.
7. Une tentative CREATE TABLE sur le snapshot local ouvert mode=ro doit échouer. Ne pas tenter cette écriture contre la base réelle.

## Baseline historique
Utiliser le memory.py live copié avec la copie restaurée. Appels document_search et search pour S407, salle 407, FusionPBX, FreePBX, SIP et la question intégrale de BASELINE_S407.md.
5 répétitions, chronomètre monotone, publier min/médiane/max et cardinalités seulement.
Exécuter aussi le comptage FTS direct avant filtre projet et la recherche sur chacun des projets ; ne pas publier leurs noms privés ni le contenu des résultats.
Le code tokenise en OR, coupe à 10 termes documentaires et limite à 4 documents ; retrieve injecte au plus 2 documents. Vérifier le code et ses hashes avant toute comparaison future.

## API native actuelle en lecture
Avec un jeton **existant**, lu en mémoire sur son hôte et jamais affiché :
- GET /api/v1/memories/ : positif authentifié et négatif sans jeton.
- POST /api/v1/memories/search avec query, limit=20, pour S407 / salle 407 / FusionPBX / SIP.
- POST /api/v1/memories/query avec content=question complète, k=4.
Ces deux POST sont des recherches, vérifiés dans les handlers déployés. Ne pas appeler add/update/delete/reindex/reset, ne pas générer un jeton, ne pas lancer une conversation ou une mission.
Chronométrer requête/réponse, publier statut, cardinalité, hashes d'ID et mentions pertinentes ; exclure les contenus et identifiants utilisateurs.
La mesure vectorielle utilise le modèle existant et ne démontre aucun gain comparatif. Une seule itération a été effectuée.

## Contrôles ACL bornés
- API historique : GET /api/search, /api/memories et /api/export sans session → 401 ; Host/Origin invalides sur health → 403.
- Unix : test de lecture sous utilisateur non privilégié sur base 0600 → refus.
- Copier la base historique dans une fixture distincte ; y ajouter 3 documents synthétiques (global/projet A/projet B), puis vérifier l'absence de B en contexte A et réciproquement. Ne jamais ajouter ces fixtures dans un index réel.
- Auth historique : importer auth.py copié ; credentials synthétiques générés localement, stockage/session DB de fixture ; tester login valide, mauvais secret, absence/invalidité cookie et logout. Aucun compte réel modifié.
- Les tests multiidentité natif/Drive et révocation Drive ne sont pas exécutés. Ne pas les remplacer par la seule inspection de code ou par un filtre projet.

## Services et documents
systemctl is-active/show sur les services explicitement listés dans les preuves ; jamais restart/enable.
Raspberry : test TCP SSH depuis Dell1, pas de revalidation complète PBX.
Drive : recherches ciblées Salle 407/FusionPBX/Téléphonie, lectures des 3 Google Docs indiqués, parents et ACL choisies. Les limites 30/30/40 empêchent de déclarer l'inventaire exhaustif.
Le tableau d'accès a servi uniquement comme fichier privé d'authentification demandé par le propriétaire, pas comme document RAG.
Discussion Tellemaintenance LCC : lecture ciblée pour retrouver le mécanisme d'accès existant, sans reprise de ses anciennes actions.
Les traces privées volumineuses ne sont pas exportées ; scanner des motifs en agrégats ne garantit pas l'absence de secrets.

## Publication
Conserver prévu/exécuté/vérifié/non exécuté séparés. Générer un manifeste SHA-256 de tous les livrables sauf le manifeste lui-même, contrôler tous les JSON/liens relatifs et les motifs sensibles/IP/MAC, puis publier uniquement ce paquet expurgé sur la branche documentaire.
Aucune fusion, aucune 24B sans validation.


## Complément : client complet et comptes de copie
1. Copier l’image et le code effectivement déployés, SQLite natif, Chroma et son cache de modèle d’embedding. Ouvrir les sources SQLite en mode=ro et sauvegarder vers destinations d’audit privées. Ne pas mettre les bases actives en immutable.
2. Pseudonymiser les comptes copiés, retirer les tokens/API keys/OAuth réels et générer des credentials de recette. Conserver le rôle administrateur de la source pour la baseline propriétaire ; utiliser deux comptes standards distincts pour l’isolation. Ne jamais modifier les comptes réels.
3. Lancer uniquement la copie, réseau none et racine en lecture seule, sur ses volumes privés. Relayer l’inférence vers le moteur existant et les seules lectures Éducation nécessaires via une liste d’opérations explicitement contrôlée. Les credentials du connecteur sont copiés dans l’espace d’audit pour éviter ses écritures de cache/rafraîchissement sur le profil original.
4. Préserver le modèle, son prompt et ses paramètres ; désactiver les chemins d’exécution/mutation externes dans la copie. Admettre les sources pertinentes effectivement découvertes et exclure le coffre sensible. Un refus dû à une liste de sources de test trop étroite doit être distingué d’un échec provider.
5. Dans le vrai frontend copié, saisir la question figée dans un nouveau chat. Conserver en privé la réponse et la trace complète ; vérifier done=true et la réponse affichée. Publier uniquement la réponse expurgée, les appels/métriques et le jugement des affirmations. Ne pas réutiliser les textes de credentials comme exemples publics.
6. Créer seulement des canaris synthétiques dans notes, mémoires, fichiers et knowledge de la copie. Tester propriétaires B/C, IDs directs, listes/recherche, vecteurs, lecture partagée sans écriture, révocation avec le même jeton, contenu de fichier après révocation et anonymes. Tester aussi la révocation d’une session fictive et la persistance de la session de l’autre acteur.
7. Vérifier le modèle proposé à l’utilisateur standard. Si son appel échoue alors qu’il est listé, enregistrer un échec fonctionnel ; un éventuel grant temporaire de contrôle n’est permis que sur copie, doit être qualifié et retiré.
8. Comparer la requête vectorielle live de lecture et la copie avant les canaris : même identité logique, mêmes quatre IDs hachés dans ce scénario. Ce test ne rend pas la capture atomique multi-stores.
9. Arrêter la seule instance de recette et son relais après collecte, retirer les credentials temporaires de connexion/Google copiés, conserver les copies d’audit en privé et confirmer que le client de production est toujours actif. Aucune ingestion 24B.

Les paramètres, résultats, limites et hash du code sont dans TESTS_CLIENT_ET_ACL.md et les preuves JSON de clôture. La réponse expurgée conserve ses erreurs pour permettre la revue ; elle ne doit pas être utilisée comme une nouvelle vérité documentaire du lycée.

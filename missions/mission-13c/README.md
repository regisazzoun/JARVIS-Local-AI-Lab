# Mission 13C

- Identifiant : 13C.
- Date ou période : Date de contenu non établie ; métadonnées disponibles dans MANIFESTE.json.
- Objectif initial : Rapport 13C — GO PARTIEL
- Matériel mentionné : Non documenté dans les rapports retenus.
- Logiciels mentionnés : Open WebUI / SQLite / FTS5
- État final documentaire : **PARTIEL**. Mémoire structurée et persistance testées ; validation intégrée différée.

## Actions et résultats confirmés

Mémoire structurée et persistance testées ; validation intégrée différée.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Mémoire structurée et persistance testées ; validation intégrée différée.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [13C.md](../../archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/reports/13C.md)

## Références et dépendances

Aucune référence explicite extraite.. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [13C.md](../../archives/recuperation-2026-10-14/membres/dc0c53fd9aac/conversation/reports/13C.md)

Version 1 transactionnelle : schema_version, conversations(id, projet, date), messages(id, conversation FK, rôle, texte, modèle, date), memories(id, type, projet, conversation, texte, statut, dates), audit(opération, identifiant, date), messages_fts et memories_fts sous FTS5. Les insertions de messages se font par échange atomique ; contenu et index sont modifiés dans la même transaction. Connexions SQLite limitées aux opérations, fermeture explicite, FK activées, timeout 10 s. Schéma plus récent refusé. Prochaine version devra être ajoutée à MIGRATIONS, sauvegarde préalable, sans migration destructive.

## Fonctionnement et validation
Dépôt indépendant de l’interface et du moteur. Propositions permanentes et de projet en attente, approbation exigeant le booléen explicite true. Rejet sans injection. Édition validée explicitement, suppression avec retrait de FTS, filtrage projet et souvenirs globaux. Temporaire limité à la conversation, sans promotion automatique. Historique conservé indépendamment, rétention 30 jours configurable, purge au lancement ; option de session en RAM sans écriture des échanges. Le fonctionnement continu ne purge pas quotidiennement : relancer manuellement l’application ou prévoir ultérieurement un mécanisme interne, sans service permanent.

Exports JSON, SQLite Online Backup, restauration vers destination nouvelle avec contrôle d’intégrité ; restauration sur données existantes refusée. Audit minimal sans texte. Aucune donnée personnelle utilisée pour les tests. La base runtime créée au démarrage échoué est vide (hors schéma), exclue du partage.

## Preuves
Neuf tests unitaires/intégration backend passent. Migration initiale et réouverture idempotente vérifiées ; aucune migration d’une version antérieure à v1 n’existe. Sauvegarde et restauration testées réellement. Nouveau processus Python : souvenir fictif validé retrouvé depuis SQLite. Les opérations API sont testées directement, sans transport HTTP.


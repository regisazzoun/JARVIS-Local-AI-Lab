# Observations documentaires expurgées — 13 novembre 2026

Ces résumés sont des observations de lecture, pas des exports bruts. Les documents sources restent privés. Les liens sont des références soumises à leurs ACL.

## S407 — document réellement lu
Source : https://docs.google.com/document/d/1acU_Eldah1TP1ogSj2zdLsPuQmQCDAVamp6h80i5wyk/edit
Révision remontée par Drive : 2026-11-12T13:08:50.063Z.
- Le document rapporte une relecture SSH des centraux, des deux têtes et des deux routeurs pédagogiques au 12 novembre.
- Trunks LACP Po1 actifs aux bancs 1 et 2 ; bancs 3 à 6 à inventorier et déployer.
- Dix téléphones repérés au banc 1 par recoupement MAC/ARP/CDP. Adresses et identifiants matériels supprimés de cette preuve.
- Recette SIP et appels restant à réaliser ; test applicatif sur un véritable client derrière le banc 2 restant.
- Ports clients du routeur pédagogique du banc 2 encore dans le VLAN de maquette ; usage à décider.
- Export historique de 24 configurations explicitement ancien ; certaines références conservent l'ancien Po1 routé.
- Droits élèves et exposition du réseau d'administration à cadrer avant ouverture.

## TELEMAINTENANCE — export réellement lu
Source : https://docs.google.com/document/d/1F-U3jtXIOs-vcvpyb0IgkO7mLi2QcCbDPIRrmevIQTU/edit
Métadonnées : modification 2026-11-06T10:53:10.266Z.
- Message utilisateur du 5 novembre : trajet Mac → Mac mini JARVIS → Dell1 → Raspberry FusionPBX testé.
- Le message rapporte FreeSWITCH, Nginx et PostgreSQL actifs. Ceci documente un état historique, pas un contrôle de service exécuté par 24A.
- Trajet complet via Dell2 restant à tester à cette date.
- L'export signale ensuite des mots de passe renseignés dans un tableau partagé sur décision du propriétaire. Initialement seules ses ACL avaient été lues. Lors de la reprise, le propriétaire a demandé sa consultation : les rubriques utiles ont servi à l'authentification privée, sans aucune valeur publiée ou indexée dans le corpus.
- Cette source infirme l'idée d'une absence totale de documentation FusionPBX, mais ne fournit pas sa configuration actuelle ni la recette des téléphones S407.

## ORIENTATION_RAG — document réellement lu
Source : https://docs.google.com/document/d/1hdE_3LRgspkM4Zz1VRrUBl8fIIdHjwS8hXzmFMN13oY/edit
Modification 2026-11-12T17:05:51.654Z.
- Orientation : réutiliser la mémoire canonique SQLite/FTS5 sur Mac mini.
- Sources à inventorier, aucun nouveau déploiement confirmé.
- Continuité universelle des conversations ChatGPT/Work/Codex non établie.

## Chemin Drive observé
Métadonnées de parents : Mon Drive → SEP CIEL → Archi-Reseau → 00-Documentation → S407.
Le chemin demandé « SEP / Archi-Réseau / Téléphonie » n'est donc pas le chemin canonique observé de ce document.
L'identité « Drive Éducation du lycée Christophe Colomb » n'est pas attestée par ces seuls noms ou par un drive_id : non vérifiée.

## Périmètre des recherches
Requêtes Salle 407, FusionPBX et Téléphonie, résultats limités à 30/30/40 : inventaire ciblé, pas exhaustif. Des supports Trixbox historiques et des guides téléphones homonymes existent. Les guides de même nom/taille sont des candidats doublons, pas des doublons certifiés par hash.


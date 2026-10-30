# Contrôles et reprises — 30 octobre 2026

## Tests logiciels

**221 tests PASS** dans la suite ciblée existante enrichie. Résultat intégral : [TESTS-LOGICIELS.txt](TESTS-LOGICIELS.txt). Aucun total additionné entre suites qui se recouvrent ; les fixtures et transports simulés sont des tests logiciels, pas une démonstration d’autonomie.

Contrôles ajoutés : réexécution des quatre anciens récits faux, correspondance unité/reçu/code/date, négations et citations historiques, comptage des unités distinct des appels, code non nul conservé comme observation, existence démontrée par Loaded, portée de santé applicative, segmentation exacte des tableaux, sources limitées au lot, réécriture sans ancien texte empoisonné, refus de prose non vérifiée avant écriture, conservation du reçu enfant, interruption pendant revue, feedback durable et déduplication sans perte des critères.

Le contrôle d’un faux PASS exige le même SHA du rapport et le même critère avant réouverture. Les tests couvrent aussi la forme native qui stocke `verification_events` plutôt qu’un objet `verification`, ainsi que l’idempotence de la rectification.

## Essais opérationnels et incidents conservés

| Preuve | Résultat réellement observé |
| --- | --- |
| 92045,92052–92054 | Code d’interface installé et précontrôlé, reprise après vraie réparation. Les six échecs antérieurs restent enregistrés. Le précontrôle ne lance pas le modèle. |
| 92088,92111,92117–92155 | Premier nouveau rapport écrit et relu par JARVIS ; lots de revue terminés sans dépassement ; FAIL final pour historique/références insuffisants. |
| 92214,92235,92273 | Deuxième rapport et relecture réels ; **faux PASS** du reviewer sur une absence de networkd contredite par Loaded. |
| 92319,92330 | Nouveau contrôle installé : relecture broker puis FAIL déterministe ; PASS original et ancien résultat SUCCESS conservés, échec compté. |
| 92352,92361,92370,92372 | Trois textes refusés avant exécution car3852,3279,4201 caractères dépassaient3200. Arrêt et correction du schéma, pas quatrième répétition inchangée. |
| 92374 | Limite d’interface portée à8000caractères ; fenêtre modèle et compteur fonctionnel inchangés. |
| 92406–92553 | Rapport long effectivement écrit ; revue atomique entière exécutée sous budget ; second faux PASS global. Des affirmations de nombres, date et santé restaient incorrectes. |
| 92561,92562,92569 | Relecture réelle et rejet déterministe des champs faux ; erratum et escalade du troisième échec de ce segment. Nouvelle stratégie seulement après réparation vérifiée du code. Totaux9 conservés. |
| 92693,92696 | Rapport suivant refusé automatiquement, notamment faute de référence originale complète ; total10, frontière9. Le reviewer a également formulé une cause de manque de source trop large : une source omise du lot n’est pas absente du journal. Les verdicts du reviewer ne sont pas traités comme des observations techniques. |
| 92719 | Précontrôle du compositeur installé : choix de16références, tableau assemblé depuis les reçus, aucune inférence dans ce précontrôle. |
| 92740,92742,92828,92829 | JARVIS sélectionne réellement le compositeur et produit une explication encore fautive. La revue termine, mais l’interruption demandée avant publication empêche l’écriture tardive. Aucun faux succès de publication. |
| 92831 | Contrat d’explication renforcé, références et nombres fournis par le moteur ; refus récents réintroduits dans le contexte propre. |
| 92848–92856 | Paquet obligatoire refusé à27887/27648octets ; arrêt après trois incidents comparables. Déduplication réelle ; reprise du paquet archivé à26170octets, objectif/contrat/cartes sources/compteurs fonctionnels identiques. Le dernier incident d’infrastructure est correctement passé de15à16 ; il n’est pas effacé. |

| 92932,92975,92995,92998 | Trois explications refusées avant écriture, dont des recomptages en lettres ; arrêt et escalade. Les deux premiers défauts de champs de schéma sont aussi conservés. |
| 93000 | Repli FACTS_ONLY explicitement décidé par Codex, après vrai changement du contrat : explication vide, tableau complet assemblé depuis les reçus et certification exacte par le moteur. Pas de quatrième tentative de prose libre. Les totaux fonctionnels10/frontière9 restent inchangés. |

Les originaux des écritures JARVIS restent dans `JARVIS-RAPPORT-*.md`, avec index des invocations et SHA. Les compositions non écrites restent dans les événements `proof_bound_report_prepared`. Les textes comportant des erreurs ne deviennent jamais rétrospectivement des rapports reçus.

## Périmètre de réception

La capacité de la revue se juge sur des appels natifs complets, pas seulement sur les nombres du précontrôle. La justesse d’un rapport se juge séparément. Les faux PASS rencontrés ci-dessus empêchent toute affirmation de fiabilité universelle du reviewer.

Le parcours final utilise des faits rendus exactement par le moteur et une explication JARVIS contrôlée avant publication. La réception finale et le SHA retenu sont décrits dans le rapport de réception, avec une vérification indépendante du fichier réellement écrit.

M26-P4 et la sonde originale restent interrompues ; aucune nouvelle réception14A,26B ou autonomie de développement distribué n’est déduite de ces essais de restitution.


La reprise d’une rectification de faux PASS est également testée avec interruption simulée entre l’événement persistant et son incrément de compteur : la reprise complète l’incrément une seule fois. Ce test logiciel ne crée aucun échec opérationnel fictif ; les totaux réels restent inchangés.

Réception native finale : préparation93021, écriture93036, PASS par relecture93060, tâche93087, bilan factuel93177/93178 et état completed93179. La compatibilité des anciens événements sans champ observations a été réparée93158 après trois échecs du renderer ; aucune source manquante n’a été inventée. Contrôles indépendants93156 et93180.

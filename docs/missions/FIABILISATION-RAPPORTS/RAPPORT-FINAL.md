# Fiabilisation des rapports et du budget de revue — 30 octobre 2026

**✅🟡 GO avec réserves pour les protections livrées. Rapport factuel reçu ; rédaction libre autonome NON REÇUE.**

Le découpage et la sélection des preuves permettent désormais de terminer les revues de la sonde sous le budget. La publication factuelle est sécurisée par un adaptateur réellement utilisé par JARVIS : il sélectionne les reçus, le moteur assemble les faits exacts et le broker écrit le rapport. La relecture indépendante et la clôture native ont réussi.

La rédaction libre du modèle reste un défaut mesuré : elle inverse encore des faits, compte mal et peut expliquer incorrectement les erreurs historiques. Après trois explications refusées avant écriture, Codex a activé un repli explicite sans commentaire libre. Cette réception ne prétend pas avoir corrigé les capacités intrinsèques du80B ni validé une autocorrection éditoriale autonome.

## Résultats reçus

| Point | Réception et preuve |
| --- | --- |
| Revue de gros rapports | **GO capacité ciblée** :54lots natifs achevés. Entrées natives admises au maximum27532/27648octets ; fenêtre32768tokens inchangée. Les avis de ces lots ont aussi comporté des faux PASS ; leur capacité ne prouve pas leur justesse. [Mesures](MESURES-BUDGET.json). |
| Contrôle des faits fermés | **GO ciblé** : codes, existence, références, heures, appels/unités et portée fonctionnelle comparés aux reçus. Relectures réelles92319 et92561 rejettent des textes faussement acceptés par le reviewer. Les PASS originaux restent historiques avec errata. |
| Publication d’un relevé fidèle | **GO mode factuel** : sélection native93019, préparation93021, contrôle93022, écriture enfant `de1917629b3d4707a4853975a00be606`, nouvelle lecture et PASS93060, tâche validée93087. [Relevé reçu](JARVIS-RAPPORT-5.md). |
| Contrôle indépendant | **GO93156** : lecture locale du fichier et analyse SQL indépendante des sorties brutes, sans appeler le renderer. Chaque ligne unité/sortie/code/date/UUID est comparée ; les lignes status correspondent aux originaux. [Preuve](VERIFICATION-INDEPENDANTE.json). |
| Bilan global | **GO mode factuel** : publication native93177/93178, mission `completed`93179 ; contrôle indépendant93180. La prose globale du modèle est archivée sans être ajoutée au document publié. [Réception](RECEPTION-PUBLICATION.json). |
| Rédaction libre et qualité générale du reviewer | **NON REÇUES**. Les originaux faux, refus et faux PASS sont conservés. Le repli évite de les publier comme des faits ; il ne les transforme pas en rédaction correcte de JARVIS. |

Le relevé décrit **12unités distinctes :9sorties active et3inactive**, issues de **20appels is-active** :16codes0,2codes3 et2codes4. Un code non nul observé n’est pas une commande non exécutée. `mdmonitor` est introuvable au status ; `systemd-networkd` est chargé mais inactif. Les sorties systemd ne prouvent pas la santé applicative.

SHA256 du relevé reçu : `884fb38539b0c86b87d9890b76bcac14300bb1cb4ca63a77b1acf15b42f9a777`.

## Réalisation et attribution

Codex a développé les contrôles, le découpage par affirmations et lignes de tableau, le contexte de réécriture, le compositeur lié aux preuves, le repli et les corrections de compatibilité du bilan global. Il a installé des ajouts ciblés en préservant les évolutions historiques du runtime, et réalisé les contrôles indépendants.

JARVIS/Qwen80B sur Dell1 a choisi ses appels, écrit les quatre nouveaux brouillons libres non reçus, sélectionné les16références et déclenché le compositeur puis la vérification et la clôture. Les lectures et écritures du broker ont lieu sur le Mac mini. Le tableau final est produit par **JARVIS-engine, code Codex** : aucune attribution de sa rédaction au modèle. Dell2 n’a pas été sollicité dans cette reprise de restitution ; aucune autonomie distribuée nouvelle n’est revendiquée.

L’événement93036 portait à tort `model_authored_explanation=true` malgré l’explication vide : erratum93069 conservé, booléen de l’interface corrigé. Les anciens faux PASS92273 et92553 sont rectifiés sans effacement des originaux. Les vérifications directes92319/92561 sont des interventions Codex ; elles ne deviennent pas des autocorrections de JARVIS.

## Incidents corrigés et conservation des limites

Les plafonds de prose trop courts ont produit des brouillons incomplets puis des refus avant écriture. Les anciens prompts de rédaction et des retours de schéma perdus rendaient le nouvel adaptateur contradictoire ; ils ont été corrigés. Le paquet de27887octets a été refusé, puis dédupliqué sans perdre objectif, contrat, cartes sources ou compteurs fonctionnels. La finalisation réutilise sa vue compacte existante.

Le renderer global rencontrait un ancien événement sémantique sans champ `observations`. Trois échecs natifs ont provoqué l’escalade ; la compatibilité a été corrigée puis retestée sur le journal réel. Le champ absent reste explicitement non renseigné, sans reçu inventé. Aucun relevé de service reçu n’a été recommencé.

**221tests logiciels PASS**, distincts des essais natifs et des contrôles indépendants. Historique final :10échecs fonctionnels conservés, frontière de réparation9 ;17incidents de capacité conservés et reconnus jusqu’au17e après correction. Les trois refus comparables de chaque stratégie restent archivés. Aucun quatrième essai de prose libre après son escalade.

## Installation, publication et périmètre

- [Architecture](ARCHITECTURE.md), [tests et reprises](TESTS-ET-REPRISES.md), [installation et rollback](INSTALLATION-REPRISE.md).
- [Preuves natives sélectionnées](PREUVES-JARVIS.json), [index des textes originaux](INDEX-RAPPORTS.json), [faits des reçus](FAITS-OBSERVES.json).
- [Manifeste installé](MANIFESTE-INSTALLATION.json), [patch runtime conservant les ajouts historiques](PATCH-RUNTIME.diff), [tests logiciels](TESTS-LOGICIELS.txt).

Les services conversation, broker, JL03, workers, guard, WebUI/tools, Apache et Ollama étaient actifs au contrôle ; WebUI privé HTTP200 avec vérification TLS0. Aucun test de microphone Apple ajouté. Aucun modèle, système, routage Ollama ou base canonique remplacé.

**M26-P4 reste interrompue et MANUAL-HOLD conservé.** La sonde originale27fc… reste interrompue. Aucune clôture14A/26B/P4 ni lancement24-Old. La branche de livraison est `codex/fiabilisation-rapports-preuves`, issue de `aaf72cc`/PR33 ; aucune fusion dans main.

# Observation des services — preuves et explication

Faits assemblés par JARVIS-engine depuis les reçus originaux. Infrastructure et contrôles développés par Codex ; lectures choisies et déclenchées par JARVIS via le broker. Les explications libres, lorsqu’elles sont retenues, sont rédigées par Qwen sur Dell1.

## Comptages exacts des lectures is-active

Unités distinctes observées : 1. Sorties par unité : {"active": 1}.
Appels is-active enregistrés : 1. Appels à retour non nul : 0. Unités à dernier retour non nul : 0.

| Catégorie | Compte |
| --- | --- |
| Appels is-active rc=0 | 1 |

## Sorties originales par unité

| Service | Sortie is-active | Code | Heure du reçu | Invocation |
| --- | --- | --- | --- | --- |
| jarvis-conversation.service | active | 0 | 2026-10-30T18:57:05.895085+01:00 | deed803b57cd4b639db758c6fc54d43f |

## Lectures status distinctes

- jarvis-conversation.service — Aucune propriété d’état extraite. — reçu 013a3eb281bb4e25a98cebdf0d3b6bfd.
- jarvis-conversation.service — Loaded: loaded (/etc/systemd/system/jarvis-conversation.service; enabled; preset: enabled) ; Active: active (running) since Fri 2026-10-30 18:12:21 CET; 44min ago — reçu 6339983b35cf496c81a5209923eb091e.

## Historique et limites

Historique des revues et compteurs : consultable dans le journal canonique. Les statuts FAIL et INSUFFICIENT ne sont pas effacés par ce rapport ; les anciens faux PASS rectifiés restent historiques. Le présent relevé ne prétend pas figer le nombre de vérifications qui auront lieu après sa rédaction.
Ces lectures systemd ne constituent pas un test fonctionnel des applications. Aucun changement de service n’est réalisé par ce rapport ; une écriture du rapport est distincte d’une modification de service.
Les états et dates ci-dessus décrivent les instants des reçus, sans nouvelle observation implicite ni idempotence applicative revendiquée.

## Explication complémentaire

Mode factuel après escalade : aucune explication libre du modèle publiée. Les brouillons antérieurs restent archivés ; les faits et limites ci-dessus sont assemblés par JARVIS-engine.

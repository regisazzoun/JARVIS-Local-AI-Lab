# Observation des services — preuves et explication

Faits assemblés par JARVIS-engine depuis les reçus originaux. Infrastructure et contrôles développés par Codex ; lectures choisies et déclenchées par JARVIS via le broker. Les explications libres, lorsqu’elles sont retenues, sont rédigées par Qwen sur Dell1.

## Comptages exacts des lectures is-active

Unités distinctes observées : 2. Sorties par unité : {"active": 2}.
Appels is-active enregistrés : 2. Appels à retour non nul : 0. Unités à dernier retour non nul : 0.

| Catégorie | Compte |
| --- | --- |
| Appels is-active rc=0 | 2 |

## Sorties originales par unité

| Service | Sortie is-active | Code | Heure du reçu | Invocation |
| --- | --- | --- | --- | --- |
| jarvis-conversation.service | active | 0 | 2026-10-31T21:43:17.845587+01:00 | 7ca000a2cd4b41e2bf40f76650718602 |
| jarvis-webui-tools.service | active | 0 | 2026-10-31T21:45:07.629422+01:00 | b2f08f313b9347d2b427cd67b74ccb28 |

## Lectures status distinctes

- jarvis-conversation.service — Loaded: loaded (/etc/systemd/system/jarvis-conversation.service; enabled; preset: enabled) ; Active: active (running) since Sat 2026-10-31 21:31:13 CET; 11min ago — reçu ae58843b16e4465baff95732f9836117.
- jarvis-webui-tools.service — Loaded: loaded (/etc/systemd/system/jarvis-webui-tools.service; enabled; preset: enabled) ; Active: active (running) since Sat 2026-10-31 21:40:14 CET; 4min 4s ago — reçu f2f4569a2f934e1f833dadad05cf8875.
- jarvis-webui-tools.service — Aucune propriété d’état extraite. — reçu 99e11f1094ba43228f4a6e906834ad57.

## Historique et limites

Historique des revues et compteurs : consultable dans le journal canonique. Les statuts FAIL et INSUFFICIENT ne sont pas effacés par ce rapport ; les anciens faux PASS rectifiés restent historiques. Le présent relevé ne prétend pas figer le nombre de vérifications qui auront lieu après sa rédaction.
Ces lectures systemd ne constituent pas un test fonctionnel des applications. Aucun changement de service n’est réalisé par ce rapport ; une écriture du rapport est distincte d’une modification de service.
Les états et dates ci-dessus décrivent les instants des reçus, sans nouvelle observation implicite ni idempotence applicative revendiquée.

## Explication complémentaire

Mode factuel après escalade : aucune explication libre du modèle publiée. Les brouillons antérieurs restent archivés ; les faits et limites ci-dessus sont assemblés par JARVIS-engine.

# Observation des services — preuves et explication

Faits assemblés par JARVIS-engine depuis les reçus originaux. Infrastructure et contrôles développés par Codex ; lectures choisies et déclenchées par JARVIS via le broker. Les explications libres, lorsqu’elles sont retenues, sont rédigées par Qwen sur Dell1.

## Comptages exacts des lectures is-active

Unités distinctes observées : 12. Sorties par unité : {"active": 9, "inactive": 3}.
Appels is-active enregistrés : 20. Appels à retour non nul : 4. Unités à dernier retour non nul : 3.

| Catégorie | Compte |
| --- | --- |
| Appels is-active rc=0 | 16 |
| Appels is-active rc=3 | 2 |
| Appels is-active rc=4 | 2 |

## Sorties originales par unité

| Service | Sortie is-active | Code | Heure du reçu | Invocation |
| --- | --- | --- | --- | --- |
| jarvis-agent-proof.service | active | 0 | 2026-10-30T09:51:52.071702+01:00 | 0b9ef9b10a61454aac61dce2b44acf96 |
| jarvis-conversation.service | active | 0 | 2026-10-30T09:53:03.217555+01:00 | 233eb89cb7d44aafbba6e201b2a1a572 |
| jarvis-ollama.service | active | 0 | 2026-10-30T09:54:40.199812+01:00 | eb77a552ebc5433cae5f2b6ec819d247 |
| jarvis-open-webui.service | active | 0 | 2026-10-30T09:54:15.365541+01:00 | ae48ef2a5d06441a82c6b55db7b7be63 |
| NetworkManager.service | active | 0 | 2026-10-30T10:30:47.242422+01:00 | 3529c3f730264bb7b899ce4a3da51ff4 |
| jarvis-mission-worker.service | active | 0 | 2026-10-30T10:31:50.479031+01:00 | f4541922b0cf4a9ea51fd8e4a479c111 |
| jarvis-mission-worker@2.service | active | 0 | 2026-10-30T10:32:22.312630+01:00 | bd9773c72f6d44ccaea0caef50930355 |
| jarvis-dell-desktop-gateway.service | active | 0 | 2026-10-30T10:40:31.031594+01:00 | 07b01b3c12984c62adbe9b4689054eed |
| mdmonitor.service | inactive | 4 | 2026-10-30T10:42:14.079049+01:00 | 9c4a3a106ab348e78741b919f5f1e032 |
| nvidia-persistenced.service | inactive | 3 | 2026-10-30T10:56:41.323218+01:00 | 512eacb2d79740c5b5015fef37e73e4d |
| ssh.service | active | 0 | 2026-10-30T10:57:41.323078+01:00 | 48094bec627d494a9673afd28437154d |
| systemd-networkd.service | inactive | 3 | 2026-10-30T11:00:59.767825+01:00 | fa5ade3000cd4f9298e6683ea1dea0c4 |

## Lectures status distinctes

- jarvis-agent-proof.service — Loaded: loaded (/etc/systemd/system/jarvis-agent-proof.service; disabled; preset: enabled) ; Active: active (exited) since Sat 2026-10-17 14:05:54 CEST; 1 week 5 days ago — reçu 18bc4c1d9a254560a4357edd3d2f8421.
- NetworkManager.service — Loaded: loaded (/usr/lib/systemd/system/NetworkManager.service; enabled; preset: enabled) ; Active: active (running) since Mon 2026-10-12 22:00:25 CEST; 2 weeks 3 days ago — reçu 17c3a906e27b48e7b69dbecc905c800f.
- mdmonitor.service — Unit mdmonitor.service could not be found. — reçu 2ddb1d7902924073b1f27340925e1c90.
- systemd-networkd.service — Loaded: loaded (/usr/lib/systemd/system/systemd-networkd.service; disabled; preset: enabled) ; Active: inactive (dead) — reçu 72425eb7c6554ed99c69840f667f1abb.

## Historique et limites

Historique des revues et compteurs : consultable dans le journal canonique. Les statuts FAIL et INSUFFICIENT ne sont pas effacés par ce rapport ; les anciens faux PASS rectifiés restent historiques. Le présent relevé ne prétend pas figer le nombre de vérifications qui auront lieu après sa rédaction.
Ces lectures systemd ne constituent pas un test fonctionnel des applications. Aucun changement de service n’est réalisé par ce rapport ; une écriture du rapport est distincte d’une modification de service.
Les états et dates ci-dessus décrivent les instants des reçus, sans nouvelle observation implicite ni idempotence applicative revendiquée.

## Explication complémentaire

Mode factuel après escalade : aucune explication libre du modèle publiée. Les brouillons antérieurs restent archivés ; les faits et limites ci-dessus sont assemblés par JARVIS-engine.

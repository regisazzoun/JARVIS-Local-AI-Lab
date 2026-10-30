# Relevé factuel indépendant — Codex

Ce document est une restitution déterministe de Codex depuis les reçus des opérations exécutées par JARVIS. Il ne remplace pas le verdict négatif sur sa prose libre. Il rapporte chaque observation à sa date ; il ne garantit pas l’état actuel ni une réponse applicative.

Politique :12noms autorisés. `is-active` :12noms observés,9sorties `active`,3sorties `inactive` ; codes0×9,3×2,4×1.

| Nom interrogé | Heure du reçu | Sortie brute | Code | Invocation |
|---|---|---|---:|---|
| NetworkManager.service | 2026-10-30T10:30:47+01:00 | active | 0 | 3529c3f730264bb7b899ce4a3da51ff4 |
| jarvis-agent-proof.service | 2026-10-30T09:51:52+01:00 | active | 0 | 0b9ef9b10a61454aac61dce2b44acf96 |
| jarvis-conversation.service | 2026-10-30T09:53:03+01:00 | active | 0 | 233eb89cb7d44aafbba6e201b2a1a572 |
| jarvis-dell-desktop-gateway.service | 2026-10-30T10:40:31+01:00 | active | 0 | 07b01b3c12984c62adbe9b4689054eed |
| jarvis-mission-worker.service | 2026-10-30T10:31:50+01:00 | active | 0 | f4541922b0cf4a9ea51fd8e4a479c111 |
| jarvis-mission-worker@2.service | 2026-10-30T10:32:22+01:00 | active | 0 | bd9773c72f6d44ccaea0caef50930355 |
| jarvis-ollama.service | 2026-10-30T09:54:40+01:00 | active | 0 | eb77a552ebc5433cae5f2b6ec819d247 |
| jarvis-open-webui.service | 2026-10-30T09:54:15+01:00 | active | 0 | ae48ef2a5d06441a82c6b55db7b7be63 |
| mdmonitor.service | 2026-10-30T10:42:14+01:00 | inactive | 4 | 9c4a3a106ab348e78741b919f5f1e032 |
| nvidia-persistenced.service | 2026-10-30T10:56:41+01:00 | inactive | 3 | 512eacb2d79740c5b5015fef37e73e4d |
| ssh.service | 2026-10-30T10:57:41+01:00 | active | 0 | 48094bec627d494a9673afd28437154d |
| systemd-networkd.service | 2026-10-30T11:00:59+01:00 | inactive | 3 | fa5ade3000cd4f9298e6683ea1dea0c4 |

Le `status` distinct de mdmonitor.service a répondu « Unit mdmonitor.service could not be found. » (invocation2ddb1d7902924073b1f27340925e1c90, code4). Le `status` de systemd-networkd.service indiquait Loaded: loaded et inactive(dead) : il ne s’agit pas d’une unité absente déduite du code3. La présence de nvidia-persistenced n’est pas démontrée par son seul is-active.

Le [manuel systemctl](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html#Exit%20status) distingue les codes3 et4 et signale les limites du mapping. Conserver les sorties originales et utiliser une observation indépendante pour expliquer une cause.

Aucun is-enabled ni contrôle de réponse applicative n’est reçu ici. Les FAIL éditoriaux précédents et les revues INSUFFICIENT restent dans PREUVES-JARVIS.json. Codex a changé les interfaces ; JARVIS a choisi et exécuté les observations. Son dernier rapport libre est NON VALIDÉ ; le problème est ESCALATED après6échecs historiques, dont3après la frontière de réparation vérifiée. Aucun compteur supprimé.

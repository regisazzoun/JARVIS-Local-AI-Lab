# Observation des services JARVIS — 2026-10-30

## Résumé

12 unités interrogées via `systemctl is-active` (20 appels au total). 9 retournent `active`, 3 `inactive`, 2 unités absentes du système (`mdmonitor.service`, `systemd-networkd.service`). Aucune modification réalisée.

Historique FAIL connu : **11** (voir `report_history`).

## Services JARVIS principaux (tous actifs)

- `jarvis-agent-proof.service` — `active (exited)`, désactivé (`is-enabled: disabled`) — [reçu 0b9ef9b10a61454aac61dce2b44acf96]
- `jarvis-conversation.service` — `active` — [reçu 233eb89cb7d44aafbba6e201b2a1a572]
- `jarvis-ollama.service` — `active` — [reçu eb77a552ebc5433cae5f2b6ec819d247]
- `jarvis-open-webui.service` — `active` — [reçu ae48ef2a5d06441a82c6b55db7b7be63]
- `jarvis-mission-worker.service` — `active` — [reçu f4541922b0cf4a9ea51fd8e4a479c111]
- `jarvis-mission-worker@2.service` — `active` — [reçu bd9773c72f6d44ccaea0caef50930355]
- `jarvis-dell-desktop-gateway.service` — `active` — [reçu 07b01b3c12984c62adbe9b4689054eed]

## Services système observés

- `NetworkManager.service` — `active (running)`, activé — [reçu 3529c3f730264bb7b899ce4a3da51ff4 + 17c3a906e27b48e7b69dbecc905c800f]
- `ssh.service` — `active` — [reçu 48094bec627d494a9673afd28437154d]

## Services non actifs / absents

- `mdmonitor.service` — code 4 (`no such unit`) — [reçu 2ddb1d7902924073b1f27340925e1c90]
- `nvidia-persistenced.service` — `inactive` (code 3) — [reçu 512eacb2d79740c5b5015fef37e73e4d]
- `systemd-networkd.service` — `inactive (dead)`, désactivé — [reçu fa5ade3000cd4f9298e6683ea1dea0c4 + 72425eb7c6554ed99c69840f667f1abb]

## Limites

- Aucune commande `is-enabled` exécutée pour les unités JARVIS principales (seul `jarvis-agent-proof.service` possède un reçu `is-enabled` implicite via `status`).
- Deux é
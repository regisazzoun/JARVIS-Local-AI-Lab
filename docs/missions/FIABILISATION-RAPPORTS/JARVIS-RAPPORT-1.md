# Observation des services JARVIS — 2026-10-30 (non destructive)

## Résumé
- **Unités observées** : 12 (d’après `is-active`)
- **Statut actif** : 9 services
- **Statut inactif ou non trouvé** : 3 unités
- **Appels `is-active`** : 20 (d’après les reçus)
- **Retours `is-active` ≠ 0** : 3 (codes 3 ou 4)

## État détaillé par unité (d’après les reçus `is-active` et `status`)

| Service | `is-active` | `is-enabled` (si disponible) | Notes |
|---------|-------------|------------------------------|-------|
| `jarvis-agent-proof.service` | `active` | `disabled` | Status : exited, activé depuis 2026-10-17 |
| `jarvis-conversation.service` | `active` | — | — |
| `jarvis-ollama.service` | `active` | — | — |
| `jarvis-open-webui.service` | `active` | — | — |
| `NetworkManager.service` | `active` | `enabled` | Status : running, depuis 2026-10-12 |
| `jarvis-mission-worker.service` | `active` | — | — |
| `jarvis-mission-worker@2.service` | `active` | — | — |
| `jarvis-dell-desktop-gateway.service` | `active` | — | — |
| `ssh.service` | `active` | — | — |
| **`mdmonitor.service`** | **`inactive`** | — | **Unité non trouvée** (status: code 4, stderr explicit) |
| **`nvidia-persistenced.service`** | **`inactive`** | — | **Code 3 → unité inactive, non absente** (status non lu, mais `is-active`=inactive) |
| **`systemd-networkd.service`** | **`inactive`** | `disabled` | **Status : loaded + inactive(dead)**. **Code 3 ≠ unité absente** ; le status le confirme. |

## Remarques critiques
- Le code de retour `3` (`is-active`) signifie « unité non active », **pas absente** ; l’interprétation « masquée ou absente » est incorrecte.
- Le code `4` (`is-active`) est réservé aux unités inconnues (status `could not be found`). C’est le cas de `mdmonitor.service`. Ce n’est pas le cas de `nvidia-pers…`
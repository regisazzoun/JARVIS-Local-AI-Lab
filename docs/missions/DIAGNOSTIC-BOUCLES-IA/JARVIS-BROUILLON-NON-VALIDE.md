> **Original JARVIS NON VALIDÉ, conservé comme preuve.** Il contient une inversion erronée des codes3/4 et des diagnostics incorrects. Voir CONTROLE-RAPPORT-FINAL.json ; ne pas utiliser ces explications comme état de référence.

# État observé des services JARVIS — 2026-10-30T09:51:52+01:00 à 11:00:59+01:00

> **Mise en garde** : les résultats ci-dessous proviennent d’appels `systemctl is-active` exécutés entre 09:51:52 et 11:00:59 UTC+01:00. Ils ne garantissent ni la persistance après redémarrage, ni l’intégrité du code chargé. L’absence d’erreur (`returncode=0`) implique que l’unité est chargée, mais pas qu’elle fonctionne correctement. Le code `returncode=3` signifie que l’unité n’est pas présente (non installée ou masquée), et `returncode=4` qu’elle est inactive (inclut `inactive`, `failed`, `activating`, `deactivating`). C’est une lecture de l’état *visible*, non une garantie de bon fonctionnement.

## Services actifs (`observed_text = active`, `returncode = 0`)

| Service | Heure d’observation (UTC+01:00) | Invocation | Référence de réception |
|---------|----------------------------------|------------|-----------------------|
| `jarvis-agent-proof.service` | 2026-10-30T09:51:52+01:00 | `0b9ef9b10a61454aac61dce2b44acf96` | `observed_service_reads.jarvis-agent-proof.service.is-active` |
| `jarvis-dell-desktop-gateway.service` | 2026-10-30T10:40:31+01:00 | `07b01b3c12984c62adbe9b4689054eed` | `observed_service_reads.jarvis-dell-desktop-gateway.service.is-active` |
| `jarvis-conversation.service` | 2026-10-30T09:53:03+01:00 | `233eb89cb7d44aafbba6e201b2a1a572` | `observed_service_reads.jarvis-conversation.service.is-active` |
| `jarvis-open-webui.service` | 2026-10-30T09:54:15+01:00 | `ae48ef2a5d06441a82c6b55db7b7be63` | `observed_service_reads.jarvis-open-webui.service.is-active` |
| `jarvis-ollama.service` | 2026-10-30T09:54:40+01:00 | `eb77a552ebc5433cae5f2b6ec819d247` | `observed_service_reads.jarvis-ollama.service.is-active` |
| `NetworkManager.service` | 2026-10-30T10:30:47+01:00 | `3529c3f730264bb7b899ce4a3da51ff4` | `observed_service_reads.NetworkManager.service.is-active` |
| `jarvis-mission-worker.service` | 2026-10-30T10:31:50+01:00 | `f4541922b0cf4a9ea51fd8e4a479c111` | `observed_service_reads.jarvis-mission-worker.service.is-active` |
| `jarvis-mission-worker@2.service` | 2026-10-30T10:32:22+01:00 | `bd9773c72f6d44ccaea0caef50930355` | `observed_service_reads.jarvis-mission-worker@2.service.is-active` |
| `ssh.service` | 2026-10-30T10:57:41+01:00 | `48094bec627d494a9673afd28437154d` | `observed_service_reads.ssh.service.is-active` |

**Total actifs observés** : 9.

## Services non actifs (`returncode ≠ 0`)

### Inactifs (`observed_text = inactive`, `returncode = 4`)

| Service | Heure d’observation (UTC+01:00) | Invocation | Référence de réception |
|---------|----------------------------------|------------|-----------------------|
| `mdmonitor.service` | 2026-10-30T10:42:14+01:00 | `9c4a3a106ab348e78741b919f5f1e032` | `observed_service_reads.mdmonitor.service.is-active` |

### Absents/masqués (`returncode = 3`) — unité non trouvée

| Service | Heure d’observation (UTC+01:00) | Invocation | Référence de réception |
|---------|----------------------------------|------------|-----------------------|
| `nvidia-persistenced.service` | 2026-10-30T10:56:41+01:00 | `512eacb2d79740c5b5015fef37e73e4d` | `observed_service_reads.nvidia-persistenced.service.is-active` |
| `systemd-networkd.service` | 2026-10-30T11:00:59+01:00 | `fa5ade3000cd4f9298e6683ea1dea0c4` | `observed_service_reads.systemd-networkd.service.is-active` |

**Total non actifs observés** : 3 (`mdmonitor`, `nvidia-persistenced`, `systemd-networkd`).

## Résumé comptage par la politique et les lectures

- **Unités autorisées par la politique (`observed_host_policy.services`)** : 12 (`NetworkManager`, `jarvis-agent-proof`, `jarvis-conversation`, `jarvis-dell-desktop-gateway`, `jarvis-mission-worker`, `jarvis-mission-worker@2`, `jarvis-ollama`, `jarvis-open-webui`, `mdmonitor`, `nvidia-persistenced`, `ssh`, `systemd-networkd`).
- **Lectures `is-active` réalisées** : 12 (toutes les unités listées dans la politique ont reçu un appel `is-active` dans cette session).
- **Résultats obtenus** : 9 × `active` (`returncode=0`), 1 × `inactive` (`returncode=4`), 2 × absent/masqué (`returncode=3`).
- **Services interrogés** : 12. **Aucun manquant** dans cette session d’observation.

## Références utilisées

- `observed_host_policy`: invocation `a52057b73ef5464ebd6d932798cdc0cc` (autorisations uniquement)  
- `observed_service_reads`: 12 lectures `is-active`, dont 9 avec `returncode=0`/`active`, 1 avec `returncode=4`/`inactive`, 2 avec `returncode=3`/absent  

**Couverture de l’observation** : 12/12 interrogées → 9 actives, 3 non actives. **Résultat global** : `SUCCESS` (complétude atteinte), `PARTIAL` (non tous actifs, mais observés).  
Aucune modification des services n’a été effectuée. Seul ce fichier de rapport a été réécrit.

**Génération du rapport** : 2026-10-30T11:08:00+01:00 par JARVIS. Correction issue de l’échec de validation interne (`review_feedback.status=FAIL`, `event:91269`).
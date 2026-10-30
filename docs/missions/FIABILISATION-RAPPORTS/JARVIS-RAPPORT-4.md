# État des services JARVIS — Observation non destructive

**Date des observations** : 2026-10-30T09:49:33+02:00 à 2026-10-30T11:02:03+02:00 (sources : [18bc4c1d](#), [fa5ade30](#), [72425eb7](#))  
**Portée** : Seuls les services listés dans `host_policy` ont été interrogés. Aucune modification effectuée.  
**Total des appels `is-active`** : 20 (code 0 à 4).  
**Unités distinctes observées** : 12.  
**Retours non actifs (`is-active != 0`)** : 3 unités (voir ci-dessous).  
**Retours d’unité inconnue (`systemctl exit code 4`)** : 2.  

## Services actifs (`is-active == active`, code 0)

| Service | Retour `is-active` | État `is-enabled` (si disponible) | Référence reçu |
|---------|-------------------|----------------------------------|----------------|
| `jarvis-agent-proof.service` | active (exited) | disabled (preset: enabled) | [18bc4c1d](#) |
| `jarvis-agent-proof.service` | active | — | [0b9ef9b1](#) |
| `jarvis-conversation.service` | active | — | [233eb89cb7](#) |
| `jarvis-ollama.service` | active | — | [eb77a552eb](#) |
| `jarvis-open-webui.service` | active | — | [ae48ef2a5d](#) |
| `NetworkManager.service` | active (running) | enabled (preset: enabled) | [3529c3f730](#), [17c3a906e2](#) |
| `jarvis-mission-worker.service` | active | — | [f4541922b0](#) |
| `jarvis-mission-worker@2.service` | active | — | [bd9773c72f](#) |
| `jarvis-dell-desktop-gateway.service` | active | — | [07b01b3c12](#) |
| `ssh.service` | active | — | [48094bec62](#) |

→ **9** services actifs sur **9** appels `is-active` retournant 0.

## Services inactifs ou absents (`is-active != 0`)

| Service | `is-active` | Code retour | Commentaire | Référence |
|---------|-------------|-------------|-------------|----------|
| `mdmonitor.service` | inactive | 4 | Unité non trouvée (« Unit mdmonitor.service could not be found. ») | [9c4a3a106a](#), [2ddb1d7902](#) |
| `nvidia-persistenced.service` | inactive | 3 | Inactive (unité existante, mais non active) | [512eacb2d7](#) |
| `systemd-networkd.service` | inactive (dead) | 3 | Charge mais inactive (disabled, preset: enabled) | [fa5ade3000](#), [72425eb7c6](#) |

→ **3** retours `is-active` non nuls, **1** unité inconnue (code 4), **2** unités existantes mais inactives.

## Limites de cette observation

- **Absence de test fonctionnel** : seuls les états de l’unité systemd sont observés (non démonstration d’un service HTTP ou autre fonctionnalité).  
- **Heure d’observation** : chaque reçu porte son horodatage ISO 8601 original ; aucune synthèse temporelle n’est faite ici.  
- **États `is-enabled` incomplets** : tous les services n’ont pas été interrogés avec `is-enabled`, et les pré-réglages (`preset:`) ne remplacent pas un statut réel.  
- **Retours unités manquantes** : le code 4 indique que l’unité n’existe pas ; il ne faut pas la confondre avec une unité inactive.  
- **Bilan historique FAIL** : 13 revues échouées pour des erreurs de typographie ou d’interprétation des codes (référence : `report_history.FAIL_reviews`).

## Références des reçus exploités

- Receipts `is-active` ayant retourné `active` (code 0) : [0b9ef9b1](#), [233eb89cb7](#), [eb77a552eb](#), [ae48ef2a5d](#), [3529c3f730](#), [f4541922b0](#), [bd9773c72f](#), [07b01b3c12](#), [48094bec62](#).  
- Receipts `is-active` non actifs (code ≠ 0) : [9c4a3a106a](#) (`mdmonitor`), [512eacb2d7](#) (`nvidia-persistenced`), [fa5ade3000](#) (`systemd-networkd`).  
- Receipts `status` (contexte complet) : [18bc4c1d](#), [17c3a906e2](#), [2ddb1d7902](#), [72425eb7c6](#).  

> **Note** : Ce rapport est une observation non destructive et est rédigé d’après les seules données d’origine. Aucune modification n’a été opérée sur le système.

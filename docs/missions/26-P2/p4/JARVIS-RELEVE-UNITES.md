# Rapport préparatoire — Unités systemd JARVIS worker

**Date du rapport** : 2026-10-28T21:00:00+01:00  
**Source** : Lecture directe brute (sans interpolation) des fichiers `/etc/systemd/system/jarvis-mission-worker.service` et `/etc/systemd/system/jarvis-mission-worker@.service`  
**Objectif** : Extraire `ExecStart`, `WorkingDirectory`, `EnvironmentFile`, `User`, dépendances (`After`, `Wants`), pour préparer une intégration progressive du worker candidat (ref 65474). Aucun déploiement ni changement applicatif.

---

## 1. Fichier `jarvis-mission-worker.service` (unité principale)

### 1.1. Champs réellement présents

| Champ | Valeur observée |
|-------|-----------------|
| `Description` | `JARVIS existing durable engine — background worker` |
| `After` | `network-online.target jarvis-host-bridge.service` |
| `Wants` | `network-online.target` |
| `Type` | `simple` |
| `User` | `adminjarvis` |
| `Group` | `adminjarvis` |
| `WorkingDirectory` | `/opt/jarvis/conversation` |
| `Slice` | `jarvis-background.slice` |
| `Environment` | `JARVIS_WORKLOAD_CLASS=mission` |
| `ExecStart` | `/opt/jarvis/conversation/.venv/bin/python -m jarvis.worker --config /opt/jarvis/conversation/config/13e.json --slot 1` |
| `Restart` | `on-failure` |
| `RestartSec` | `5` |
| `TimeoutStopSec` | `700` *(non réclamé mais présent)* |
| `WantedBy` | `multi-user.target` |

### 1.2. Champs requis mais **absents**

| Champ | Présence | Remarque |
|-------|----------|----------|
| `EnvironmentFile` | ❌ Absent | Aucun fichier d’environnement externe déclaré |
| `ExecStartPre` / `ExecStartPost` | ❌ Absents | Aucun script de préparation/post-traitement déclaré |
| `TimeoutStartSec` | ❌ Absent | Non spécifié |
| `ProtectSystem` / `ProtectHome` | ❌ Absents | Aucune isolation additionnelle déclarée |

---

## 2. Fichier `jarvis-mission-worker@.service` (template instanciable)

### 2.1. Champs réellement présents

| Champ | Valeur observée |
|-------|-----------------|
| `Description` | `JARVIS canonical durable mission worker slot %i` |
| `After` | `jarvis-conversation.service jarvis-host-bridge.service` |
| `Wants` | `jarvis-conversation.service` |
| `User` | `adminjarvis` |
| `Group` | `adminjarvis` |
| `WorkingDirectory` | `/opt/jarvis/conversation` |
| `Slice` | `jarvis-background.slice` |
| `Environment` | `PYTHONPATH=/opt/jarvis/conversation`<br>`JARVIS_WORKLOAD_CLASS=mission` |
| `ExecStart` | `/opt/jarvis/conversation/.venv/bin/python -m jarvis.worker --config /opt/jarvis/conversation/config/13e.json --slot %i` |
| `Restart` | `on-failure` |
| `RestartSec` | `3` |
| `TimeoutStopSec` | `700` *(non réclamé mais présent)* |
| `WantedBy` | `multi-user.target` |

### 2.2. Champs requis mais **absents**

| Champ | Présence | Remarque |
|-------|----------|----------|
| `EnvironmentFile` | ❌ Absent | Aucun fichier d’environnement externe déclaré |
| `ExecStartPre` / `ExecStartPost` | ❌ Absents | — |
| `TimeoutStartSec` | ❌ Absent | — |
| `ProtectSystem` / `ProtectHome` | ❌ Absents | — |

---

## 3. Analyse comparative et observations clés

| Critère | `jarvis-mission-worker.service` | `jarvis-mission-worker@.service` |
|---------|----------------------------------|-----------------------------------|
| **Slots** | `--slot 1` codé en dur | `--slot %i` paramétrable |
| **Dépendances réseau** | `network-online.target` requis | Aucune dépendance réseau déclarée |
| **PYTHONPATH** | Non déclaré | `PYTHONPATH=/opt/jarvis/conversation` |
| **RestartSec** | `5` | `3` |
| **Wants** | `network-online.target` | `jarvis-conversation.service` |

### Points d’attention

- **Absence de `EnvironmentFile`** dans les deux unités. Les variables sont déclarées directement dans le fichier unité.
- **Absence de `ProtectSystem`/`ProtectHome`** : le worker s’exécute sans isolation additionnelle. Ce choix est cohérent avec la configuration actuelle mais limite la sécurité en cas de compromission du worker.
- **`ExecStart` partage la même configuration `--config /opt/jarvis/conversation/config/13e.json`**. Cela suppose que le fichier `13e.json` contient les paramètres spécifiques à chaque slot ou que le worker gère le multi-slot via `--slot`.
- **Temps d’arrêt (`TimeoutStopSec=700`)** court pour un worker de mission longue ; l’unité template impose `3s` entre tentatives, le principal impose `5s`.

---

## 4. Limites des preuves observées

> Les deux lectures brutes (`cat`, sans interpolation) ont succédé (refs 68869, 68871). Elles **ne prouvent pas** que :
> - Le code Python `/opt/jarvis/conversation/.venv/bin/python -m jarvis.worker` est actuellement chargé en mémoire ;
> - Le service est actuellement opérationnel (seul `host_service is-active` ou `status` le prouverait à l’instant T) ;
> - La configuration `13e.json` est valide ou correspond à celle du candidat worker reçu (ref 65474).

La fraîcheur du rapport de démarrage et l’état réel du code chargé exigent une vérification distincte (ex. `systemctl show`, `journalctl`, inspection du processus réel).

> **Événements conservés explicitement** : `event:69316` pour le FAIL initial (semantic mismatch sur preuves manquantes), `event:69342` pour le retrait des trois reproces de preuves absentes.

---

Historique conservé : `event:69664` (FAIL).

**Fin du relevé de fichiers.**

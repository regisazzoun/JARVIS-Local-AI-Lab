# Diagramme JARVIS — vue couches physiques, applicatives et fonctionnelles

**État documentaire au 25/10/2026**, source du rendu vectoriel V2. Les flèches continues représentent les liens réellement utilisés dans le périmètre de leur mission ; les pointillés un usage prévu ou non démontré. `✅🟡` signifie acquis avec réserves.

```mermaid
flowchart LR
    C["✅🟡 CLIENTS<br/>MacBook / iPhone<br/>JL01 / JL02 / JL03"]
    subgraph M["MAT-01 ✅🟡 MAC MINI — COORDINATEUR"]
    direction TB
    M0["✅ Debian · systemd · RTX3090 eGPU"]
    M1["✅🟡 Conversation API / Ollama / Qwen3.5 27B"]
    M2["✅🟡 Mission Engine26 / SQLite FTS5 / Broker"]
    M3["✅🟡 Whisper / Piper / LiveKit / JL03"]
    M4["✅🟡 Routeur 28A / workers / watchdog"]
    M0 --- M1 --- M2 --- M3 --- M4
    end
    subgraph D1["MAT-02 ✅ DELL 1 — INFÉRENCE + EXÉCUTION"]
    direction TB
    D10["✅ Debian13 · RAID1 · 2 ESP · 2 RTX3090"]
    D11["✅ CUDA · Ollama 11435 (28A)"]
    D12["✅🟡 Qwen3-Coder-Next 80B Q4 · ctx24576"]
    D13["✅🟡 host_remote/project_exec · worker"]
    D10 --- D11 --- D12 --- D13
    end
    subgraph D2["MAT-03 ✅🟡 DELL 2 — EXÉCUTION"]
    direction TB
    D20["🟡 OS/CPU/RAM/2GPU à réconcilier"]
    D21["✅🟡 Node.js · Bubblewrap · project_exec"]
    D22["📋 Ollama / modèle IA non démontrés"]
    D23["🟡 CPU+2GPU vers JL03 : D17"]
    D20 --- D21 --- D22 --- D23
    end
    G["✅🟡 GitHub<br/>missions / preuves / branches"]
    C <-->|"API / SSH / Tailscale"| M1
    M4 <-->|"LIA-02 API Ollama / SSH / Ansible"| D12
    M2 <-->|"LIA-03 project_exec / checkpoints"| D21
    M4 -.->|"LIA-06 admission inférence prévue"| D22
    D13 -.->|"LIA-04 inter-Dell directe non prouvée"| D21
    M2 <-->|"commits / documents"| G
    D23 -.->|"métriques non réceptionnées"| M3
```

**Attention :** deux Dell comme exécutants ne veut pas dire équilibrage d'inférence. Le diagramme distingue les deux canaux. Le propriétaire confirme le Dell2 déployé ; les fonctions exactes et l'activation GPU IA restent à documenter séparément.

Voir [inventaires et sources](PRIORITES-ET-PROGRESSION.md), [diagnostic des boucles](ANALYSE-BLOCAGES-ET-BOUCLE-CONTROLE.md).

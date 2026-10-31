# Architecture observée et frontières

Trait continu : liaison testée, aujourd’hui ou historiquement selon Fxx. Pointillé : configuration ou réception incomplète. Croix : liaison absente. Les suffixes Fxx renvoient à interconnexions.csv ; un diagramme n’ajoute aucune réception.

```mermaid
flowchart TB
  U[Utilisateur distant] -->|HTTPS tailnet F01 historique| TS[Tailscale Serve :443]
  subgraph MAC[Mac mini Debian]
    TS -->|HTTP loopback8088 F02| AP[Apache]
    AP -->|HTTP3000 F03| WEB[Open WebUI]
    WEB -.->|conversation HTTP11434 F04| OM[Ollama Mac / Qwen 27B]
    WEB -->|API8092 F05 historique| REG[Registry JARVIS]
    QC[Qwen Code sur Mac] -->|OpenAI HTTP8091 F06| GUARD[Guard / admission]
    QC -->|MCP stdio F10| REG
    JL[JL03 :8766] -->|HTTP/SSE8765 F20 historique| CONV[Conversation]
    CONV -->|HTTP11434 F08 historique| OM
    ME[Mission Engine / deux workers] -->|F19 SQLite| MEM[Mémoire / missions canoniques]
    ME --> REG
    REG -->|F14| SK[Skill Lab]
    REG -->|Unix socket F11| BROKER[Broker / politique root]
    JL -.->|F21| TEL[Télémétrie / health / watchdog]
  end
  subgraph D1[Dell 1 / 256 GiB RAM]
    OD[Ollama :11434 / :11435]
    Q80[Qwen 80B chargé sur 11435]
    G10[RTX3090 24 GiB]
    G11[RTX3090 24 GiB]
    EX1[Exécuteur SSH / candidats / TTS]
    OD --> Q80
    Q80 --> G10
    Q80 --> G11
  end
  subgraph D2[Dell 2 / 128 GiB RAM]
    EX2[Exécuteur SSH / candidats]
    G20[RTX3090 24 GiB]
    G21[RTX3080 10 GiB]
    NONE[Pas de serveur Ollama observé]
  end
  GUARD -->|HTTP11435 F07| OD
  ME -->|HTTP11435 F09 historique| OD
  BROKER -->|SSH22 F12| EX1
  BROKER -->|SSH22 F13| EX2
  ME --x|F22 absent| NONE
  TEL -.->|mesures F21| G10
  TEL -.->|mesures F21| G11
  TEL -.->|mesures F21| G20
  TEL -.->|mesures F21| G21
  OM --> GM[RTX3090 eGPU Mac 24 GiB]
  REG -->|F15 MCP/OAuth profil personal| GP[Connecteur Google personnel]
  REG -->|F16 MCP/OAuth profil education| GE[Connecteur Google Éducation]
  QC -.->|F17 parcours Éducation non reçu| GE
  GP --> GA[API Google HTTPS443]
  GE --> GA
  REG -->|gh HTTPS443 F18 historique| GH[GitHub]
  TEL -.->|F23 envisagé| P7[Incident GPU vers diagnostic agentique P7]
```

Les cinq GPU sont représentés une seule fois. Le Dell 2 exécute des commandes mais n’est pas un serveur d’inférence. Le relais OAuth externe du connecteur Google échange/renouvelle les jetons : la connexion n’est pas intégralement hors ligne. La voie LiveKit est une chaîne vocale prototype reçue historiquement avec ses réserves ; elle ne crée pas une seconde mémoire canonique. Les liens MacBook/iPhone n’ont pas été retestés physiquement dans ce bilan.

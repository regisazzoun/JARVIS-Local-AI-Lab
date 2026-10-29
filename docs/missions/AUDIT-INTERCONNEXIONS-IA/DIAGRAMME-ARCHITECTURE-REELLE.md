# Graphe observé

**Trait épais `==>` :validé**, avec preuve actuelle ou réception historique datée. **Trait fin `-->` :configuré, non reçu boutenbout.** **Pointillé `-.->` :absent ou envisagé.** Les référencesFxx renvoient à la matrice ;elles précisent protocole, port et portée de la preuve.

```mermaid
flowchart TB
  U[MacBook / iPhone] -->|F02 HTTPS443, clients physiques non testés| TS[Tailscale Serve Mac]
  A[Chromium audit / curl Dell1] ==>|F01 HTTPS443, certificat valide| TS
  subgraph Mac[Mac mini Debian — contrôle central]
    TS ==>|F03 HTTP loopback8088| AP[Apache2]
    AP ==>|F04 HTTP / WS / SSE3000| W[Open WebUI]
    W ==>|F24 SQLite volumeDocker| WH[Historique WebUI]
    W ==>|F07 outil HTTP8092, reçu historique| AD[Adaptateur outils/audio]
    AD ==>|F08 subprocess local| QC[Qwen Code]
    QC ==>|F09 OpenAI HTTP8091| G[Garde de contexte]
    QC ==>|F25 fichiersJSONL| QS[Sessions Qwen]
    JL[JL03 port8766] ==>|F14 HTTP8765| J[JARVIS conversation]
    V23[Prototype vocal23D port8783]
    J ==>|F16 SQLite / FTS5| M[Mémoire canonique]
    J ==> ME[Mission Engine / workers Mac]
    ME ==>|F16 SQLite| MS[Missions / plans / reçus]
    ME ==>|F19 socketUnix, historique26| B[Broker SSH / Ansible]
    AD ==>|F11 HTTP8765 lecture| J
    AD -->|F12 POST8765, non exercé| ME
    AD ==>|F13 STT/TTS historiques| VO[Whisper / Piper]
    J ==>|F17 HTTP11434, limité reçu| OM[Ollama Mac]
    W ==>|F05 HTTP11434, choix aléatoire si doublon| OM
    OM ==>|F26 CUDA| GM[GPU1 : RTX3090 24GiB]
  end
  subgraph D1[Dell1]
    O1[Ollama principal11434]
    O2[Ollama missions11435]
    DS[Catalogue partagé entre les deux instances]
    O1 ==> DS
    O2 ==> DS
    E1[Exécuteur SSH / projets]
    O2 ==>|F26 CUDA| G11[GPU2 : RTX3090 24GiB]
    O2 ==>|F26 CUDA| G12[GPU3 : RTX3090 24GiB]
  end
  subgraph D2[Dell2]
    E2[Exécuteur SSH / projets]
    O3[Ollama absent des contrôles]
    G21[GPU4 : RTX3090 24GiB]
    G22[GPU5 : RTX3080 10GiB]
    O3 -.->|F27 inférence non disponible| G21
    O3 -.->|F27 inférence non disponible| G22
  end
  W ==>|F06 HTTP11435| O2
  G ==>|F10 API native11435, Qwen80B| O2
  ME ==>|F18 HTTP11435, reçu26| O2
  B ==>|F20 SSH22, reçu26 / observationCodex| E1
  B ==>|F20 SSH22, reçu26 / observationCodex| E2
  QC -.->|F21 aucun worker intégré| ME
  QC -.->|F22 pas de délégation configurée| E2
  ME -.->|F23 nœud désactivé, URLnull| O3
```

Les liens catalogue/Ollama sont des dépendances de stockage constatées, pas des copies de modèles entreAPI. Le graphe n'attribue ni80B niOllama àDell2. Les workersMac orchestrent des commandes surlesDell ;ils ne sont pas déplacés artificiellement surlesGPU.

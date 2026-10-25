# Architecture agentique JARVIS — Diagramme validé par le propriétaire

**Validation graphique et fonctionnelle : 25 octobre 2026.**
**Statut : conception approuvée pour documentation, non assimilée à un déploiement.**

Cette représentation est le dernier diagramme explicitement accepté par le propriétaire. Respecter sa disposition : **couche bleue supérieure : mission complète, décomposition et distribution** ; **couche verte inférieure : résolution agentique de chaque micro-tâche**. Le contrôle de clôture globale se trouve dans la couche bleue.

```mermaid
flowchart TB
    U["MISSION GLOBALE<br/>Instruction du propriétaire"]

    subgraph BLEU["🔵 COUCHE SUPÉRIEURE — PILOTAGE GLOBAL"]
        direction TB
        A["Réception et analyse de la mission"]
        B["JARVIS décompose et hiérarchise<br/>les micro-tâches"]
        C["Organisation des dépendances<br/>et des priorités"]
        D[("Stockage persistant SQLite<br/>Micro-tâches, contextes et états")]
        E["Sélection et distribution<br/>d'une micro-tâche"]
        Q{"Mission globale<br/>entièrement résolue ?"}
        R["✅ MISSION TERMINÉE<br/>Synthèse et validation globale"]

        A --> B --> C --> D
        D --> E
        Q -->|"Non"| E
        Q -->|"Oui"| R
    end

    subgraph VERT["🟢 COUCHE INFÉRIEURE — RÉSOLUTION AGENTIQUE"]
        direction TB
        F["JARVIS : analyse et stratégie"]
        G["Exécution par les workers<br/>Dell 1 / Dell 2"]
        H["Observation et vérification"]
        I{"Micro-tâche résolue ?"}
        J["Capitalisation de la méthode"]
        K["Compétence réutilisable"]
        L["Diagnostic causal"]
        M{"Cause identifiée ?"}
        N["Nouvelle hypothèse et stratégie"]
        O["Recherche documentaire et outils"]
        P["Codex : assistance sur blocage persistant"]

        F --> G --> H --> I
        I -->|"Oui"| J --> K
        I -->|"Non"| L --> M
        M -->|"Oui"| N
        M -->|"Non"| O --> N
        N --> F
        L -.->|"3 répétitions sans progrès"| P
        P -.-> N
    end

    U --> A
    E -->|"Micro-tâche + contexte limité"| F
    K -->|"Résultat + preuves + apprentissage"| D
    D --> Q

    style BLEU fill:#e2edff,stroke:#3678cb,stroke-width:3px,color:#173d70
    style VERT fill:#e1f4e7,stroke:#369058,stroke-width:3px,color:#174f30
    style R fill:#bfeccc,stroke:#21844a,stroke-width:2px,color:#15502c
```

## Principes actés

- La couche supérieure reçoit la mission, produit et stocke un plan hiérarchisé, transmet une **micro-tâche et son contexte limité** à la couche verte.
- La couche verte exécute, vérifie et résout localement ; la protection contre les répétitions est appliquée à la **micro-tâche**, sans arrêter la mission globale.
- Après résolution, résultats, preuves et apprentissages remontent dans le stockage canonique.
- La couche supérieure décide si la **mission globale est entièrement résolue** : si non, elle distribue la suite ; si oui, elle synthétise et clôture après validation globale.
- Codex n'est sollicité que pour l'assistance sur un blocage persistant, sans se substituer systématiquement à la capacité agentique de JARVIS.
- Ce diagramme représente la **cible validée de conception**, et non une affirmation d'installation ou de réussite technique.

**Sources normatives relues :** `AGENTS.md`, `docs/CHARTE_DIRECTIVES_JARVIS.md`, `docs/architecture/P0-P3-2026-10-25/PRIORITES-ET-PROGRESSION.md`. Les missions existantes et leurs états documentés restent inchangés.

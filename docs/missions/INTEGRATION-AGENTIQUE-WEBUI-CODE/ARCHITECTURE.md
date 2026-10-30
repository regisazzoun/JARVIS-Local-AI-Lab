# Architecture installée

Le connecteur étend le registre JARVIS existant. Il utilise `runtime/memory.sqlite` pour les reçus clients, `runtime/missions.sqlite` pour les missions et le Skill Lab existant. Aucun second ordonnanceur ou stockage canonique de mémoire n’est créé. L’historique Open WebUI préexistant reste son historique d’interface ; sa mémoire intégrée est désactivée dans les profils livrés.

```mermaid
flowchart LR
  U[Propriétaire sur le tailnet] -->|HTTPS existant| T[Tailscale Serve]
  T -->|HTTP loopback 8088| A[Apache2]
  A -->|HTTP et WebSocket existants| W[Open WebUI]
  W -->|Conversation réelle| M[Ollama Mac mini / Qwen27B]
  W -->|Outils natifs asynchrones| C[Adaptateur local 8092]
  C --> R[Registre canonique JARVIS]
  R --> S[SQLite canonique / missions / Skill Lab]
  R --> B[Broker existant]
  B -->|SSH projets confinés| D1[Dell1 exécuteur]
  B -->|SSH projets confinés| D2[Dell2 exécuteur]
  R -->|qwen_code_run| Q[Qwen Code spécialiste]
  Q -->|stdio MCP, six outils de découverte/appel| R
  Q -->|OpenAI compatible 8091| G[Garde et ComputeQueue existants]
  W -->|Profil développement / API native| G
  G -->|Ollama 11435| L[Qwen80B Dell1]
  R -.->|OAuth local non raccordé| GG[Google Workspace]
```

Les flèches pleines décrivent les parcours utilisés dans la campagne ; Google reste une dépendance d’authentification, sans réception distante. Dell2 est un exécuteur de commandes et tests : aucune inférence Ollama n’y est annoncée.

## Contrats

- `client_capabilities.py` : découverte paginée, schémas du registre actif, appel sous les autorisations existantes, reçus et consultation/création des missions canoniques.
- `client_mcp.py` : transport stdio compact pour Qwen Code. Le serveur MCP historique reste intact.
- `qwen_specialist.py` : délégation au spécialiste existant et lecture de son état. L’appel n’est pas une validation du code. Un conflit de concurrence signifie `NOT_EXECUTED` et demande l’observation du travail précédent.
- `google_workspace.py` : comptes OAuth distincts et opérations Workspace structurées. Le statut sans jeton est `AUTH_REQUIRED`. Aucun envoi Gmail n’est exposé dans cette livraison.
- Outils Open WebUI : les appels réseau sont exécutés par `asyncio.to_thread`, pour conserver la disponibilité de son serveur pendant une tâche longue.

Chaque appel conserve l’acteur déclencheur, les arguments, le résultat original et sa référence d’audit. Une projection courte est envoyée au modèle ; l’original reste lisible par pagination. Un identifiant réutilisé avec d’autres arguments est refusé. Si une réservation existe sans résultat, la réponse est `UNKNOWN` et ne redéclenche pas l’opération.

Les appels clients isolés ne sont pas présentés comme des missions autonomes reçues. Les missions durables restent sous le moteur existant et ses mécanismes P2/P3/P4. M26-P4 reste en pause.

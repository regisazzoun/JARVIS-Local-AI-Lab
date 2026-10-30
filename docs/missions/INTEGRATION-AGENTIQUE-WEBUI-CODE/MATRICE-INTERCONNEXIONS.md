# Interconnexions avant / après

| Flux | Avant | Après / preuve |
|---|---|---|
| Navigateur → Tailscale → Apache → WebUI | Déjà reçu | Conservé, conversations Chromium HTTPS réelles |
| WebUI → Qwen27B Mac | Conversation existante | Nouveau profil par défaut, outils natifs exécutés |
| WebUI → Qwen80B Dell1 | Profil développement existant | Outils de registre commun ; délégation spécialiste réelle |
| WebUI → outils hôte / recherche | Adaptateur limité missions/Code | Ressources et recherche réellement affichées |
| WebUI → GitHub / Skill Lab | Raccordement incomplet | `github-publish`, branche d’essai, vérification des blobs et lecture indépendante |
| WebUI → missions | API canonique existante | Liste réelle ; façade de création avec contrôle du reçu, pas de seconde file |
| Code → registre JARVIS | Isolé des capacités communes | MCP stdio et reçus canoniques, appels réels |
| Code → Dell2 | Non exposé dans le lanceur initial | Transferts et unittest réellement exécutés, limites de finalisation documentées |
| Code → Goal Runtime | Outils explicitement exclus | Lecture/actualisation autorisées ; clôture observée et cas longs réservés |
| WebUI → résultats Code après déconnexion | Reçu privé peu découvrable | `qwen_code_status` et lien `client_audit_id` vers `jarvis_receipt` |
| WebUI/Code → Google | Aucun OAuth local trouvé | Connecteur chargé, assistant OAuth prêt, authentification propriétaire en attente |
| Dell2 → modèle d’inférence | Non démontré | Inchangé ; aucune installation ni inférence inventée |
| JARVIS → mémoire canonique | SQLite/FTS5 existant | Conservé ; mémoire intégrée WebUI désactivée dans ces profils |

Les dernières réceptions et réserves de chaque parcours figurent dans les tests et le rapport. Une flèche configurée, un HTTP200 ou un outil découvert ne constitue pas à lui seul une réception fonctionnelle.

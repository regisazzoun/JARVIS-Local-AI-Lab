# Google Workspace — raccordement préparé, réception distante en attente

Le connecteur est installé et chargé par le registre canonique. Il est accessible depuis les mêmes façades WebUI/MCP. JARVIS a réellement appelé son état : `AUTH_REQUIRED`, reçu70.

Les fonctions implémentées couvrent Drive, Docs, Sheets, Calendar et Gmail, avec profils personal/education séparés. Les écritures de calendrier n’invitent personne ; Gmail permet lecture/recherche et brouillon, sans fonction d’envoi dans ce connecteur. Les tests logiciels vérifient les contrats et la gestion des jetons ; ils ne prouvent pas un accès Google distant.

Aucun jeton OAuth local réutilisable n’a été trouvé. Le raccordement requiert la connexion interactive au compte du propriétaire. Suivre [GOOGLE-RACCORDEMENT.md](GOOGLE-RACCORDEMENT.md), puis faire une recherche/lecture réelle et une écriture de test relue pour chaque service autorisé. Les profils Éducation peuvent nécessiter une politique administrateur réellement constatée ; ne pas présumer son refus.

Verdict : 🟡 préparation livrée, connexion et réception de bout en bout en attente. Les outils Google de Codex ne sont pas transférés comme identifiants de JARVIS.

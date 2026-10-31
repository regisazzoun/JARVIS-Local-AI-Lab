# Google MCP / OAuth existant — livraison de préparation

**31octobre2026 — 🟡 EN ATTENTE D’AUTHENTIFICATION.** Installation et interconnexions reçues avec réserves ; réception des comptes et des API Google non réalisée. La mission n’est pas déclarée terminée.

## Solution retenue

Le serveur open source [gemini-cli-extensions/workspace](https://github.com/gemini-cli-extensions/workspace), Apache2.0, fournit son clientOAuth et son relais. Il fonctionne directement par MCP/Node sur le Mac mini sans installer GeminiCLI ni modifier Ollama. **Aucun projet Google Cloud personnel, client_secret.json, abonnement ou service payant n’a été créé/configuré.** Le parcours de PR35 reste historique ; le [nouveau guide](AUTHENTIFICATION.md) le remplace pour cette extension.

Les alternatives ont été vérifiées, en distinguantOAuth fourni, BYOC applicatif, automatisation d’un projet et simple session navigateur. [Comparatif](COMPARATIF-CONNECTEURS.md), [sources](SOURCES.json). Le relais du fournisseur reste nécessaire pour l’échange et le renouvellement : les jetons sont stockés chiffrés sur le Mac, et le refresh token est transmis au relais lors du renouvellement. Cette dépendance est explicite.

## Réalisation installée

Profils personal et education isolés, permissions700/600, registre et mémoire existants conservés. Le MCP historique compte neufoutils, dont les huitanciens ; le transport client PR35 reste à sixinterfaces. Un outil google_mcp découvre/appelle30méthodes amont. Deux opérations Sheets additionnelles de création/écriture réutilisent son AuthManager et le scopeDrive déjà demandé ; elles sont attribuées àCodex, pas au serveur amont. Elles restent non réceptionnées sur Google. [Catalogue](CATALOGUE-GOOGLE.json), [extensionSheets](EXTENSIONS-SHEETS.md).

Le modèle27B dans WebUI et le80B dans QwenCode ont réellement appelé les statuts des deuxprofils et l’outil local de date. Le moteur JARVIS a également produit septappels natifs de statut. Ces résultats prouvent le raccordement au modèle, pas l’accès aux fichiers ou messages Google. L’interface de prélogin Google reconnaît l’application fournie ; aucun compte n’a été authentifié.

**20tests logiciels ciblésPASS**, contratSDK stdio et appels réels des troisclients observés. Les services contrôlés sont actifs. Les93tests/cinqcontrôles acquisPR35 n’ont pas été rejoués. [Tests et incidents](TESTS.md), [preuves](PREUVES.json), [installation/retour arrière](INSTALLATION.md).

## Réserves précises

- Les deuxcomptes restentAUTH_REQUIRED : recherche/lecture/création/relectureDocs,Sheets,Calendar,Gmail et persistance de l’authentification sont en attente. L’interaction navigateur du propriétaire a été demandée avec les seules commandes nécessaires ; aucun projetCloud demandé.
- Les politiquesÉducation ne sont pas présumées permissives ou bloquantes. Un éventuel refus doit être observé et documenté séparément du compte personnel.
- Le plan initial de la sonde native était incorrect. Codex a fourni le plan2 de préflight ; les appels ont eu lieu, puis les lectures ont bouclé et la sonde a été interrompue. Rapport et autonomie de cette sonde NONREÇUS ; pas de modification générale du moteur26 pour masquer ce résultat.
- Une instruction de réponseWebUI confondait Terminal et navigateur. L’original est conservé et rectifié dans le guide et les champs structurés de configuration. La prose libre n’est pas déclarée globalement fiable.
- Aucun envoi Gmail n’est activé. Le code amont prévoit l’envoi, mais son ouverture nécessite la demande utilisateur explicite correspondante. Aucun message externe n’a été envoyé pendant les tests.

## Attribution et suite

Google/projet amont : serveur, clientOAuth, relais et stockage chiffré. Codex : inventaire/recherche, sélection, isolation des profils, adaptations du registre, callback sécurisé, deuxfonctionsSheets additionnelles, installation, tests et contrôles indépendants. JARVIS/WebUI et QwenCode : appels et restitutions réellement journalisés. JARVIS natif : appels de statut observés, plan initial imparfait, rapport non reçu. Propriétaire : authentification des comptes encore nécessaire.

Code1abd51d, branche codex/google-mcp-oauth-existant à la suite dePR35 ; aucune fusionmain. M26P4 et MANUAL-HOLD conservés, modèles et distributionDell inchangés. Prochaine étape : suivre [AUTHENTIFICATION.md](AUTHENTIFICATION.md), puis recevoir les opérations Google réelles. Les composants et preuves déjà livrés restent utilisables pendant cette attente.

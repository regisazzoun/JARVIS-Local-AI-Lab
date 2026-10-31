# Google MCP / OAuth existant — état de réception

**31octobre2026 — ✅🟡 compte personnel reçu avec réserves ; 🟡 compte Éducation bloqué avantOAuth.** La mission globale n’est pas entièrement réceptionnée.

## Résultats actuels

Le compte personnel a été autorisé par le propriétaire. Drive, Docs, Sheets, Calendar et Gmail ont répondu réellement. Un document et un classeur de réception ont été créés, puis relus avec comparaison du contenu attendu. Un document existant et les métadonnées d’un messageGmail ont aussi été lus ; deuxévénementsCalendar ont été retournés. Les fichiers et données personnels restent dans les journaux privés, pas dansGitHub.

Open WebUI27B et QwenCode80B ont réellement lu le document de réception et restitué son marqueur. La connexion a persisté après recharge des services. Un test contrôlé d’échéance locale a déclenché le renouvellementOAuth, puis une nouvelle lectureDrive a réussi. [Réception personnelle](RECEPTION-PERSONAL.md) · [preuves expurgées](RECEPTION-PERSONAL.json).

Le compteÉducation n’a pas fourni de jeton. Le propriétaire rapporte un message d’accès au service refusé demandant la console d’administration. Une politique de service/app est probable ; l’écran/service exact n’est pas encore identifié. Aucune politique n’est modifiée ou contournée. [Diagnostic Éducation](BLOCAGE-EDUCATION.md).

## Installation et attribution

Le serveur open source Workspace Apache2 fournit son clientOAuth et son relais : **aucun projetGoogleCloud personnel ni abonnement n’a été créé/configuré**. Deuxprofils chiffrés et distincts sont hébergés sur le Mac. Le relaisOAuth externe reste nécessaire à l’échange et au renouvellement des jetons. [Choix/architecture](CHOIX-ET-ARCHITECTURE.md), [comparatif](COMPARATIF-CONNECTEURS.md), [connexion](AUTHENTIFICATION.md).

Trenteméthodes amont et deuxméthodesSheets additionnelles sont exposées par les registres/MCP existants. Les deuxextensionsSheets sont deCodex et réutilisent l’AuthManager amont ; leurs créations/écritures ont maintenant été testées surGoogle. Les huitoutils MCP historiques sont conservés, neuvenincluantGoogle ; les sixinterfaces de transportPR35 sont inchangées. Aucun nouveau moteur ou mémoire canonique.

Codex a sélectionné/intégré le connecteur, développé le callback et les extensions, exécuté les testsAPI et contrôles indépendants. JARVIS/WebUI et QwenCode ont exécuté les lecturesmodèles observées. Dans le moteur natif, septstatuts préauth ont été lus après un plan2 fourni explicitement parCodex ; la sonde a répété les lectures puis a été interrompue. Son rapport/autonomie restent NONREÇUS, sans effacer le plan initial incorrect ni les brouillons.

## Validation et réserves

**21tests logiciels ciblésPASS** après les derniers ajustements, sans rejeu93tests/cinqcontrôlesPR35. Le dossier PREUVES.json reste l’instantané AVANTauthentification, conservé comme historique ; RECEPTION-PERSONAL.json porte les preuves actuelles expurgées. Aucun token, identifiant privé de document, contenu de message ou document personnel n’y est publié.

Restent : authentification et réceptionÉducation après diagnostic administratif précis ; Gmailenvoi non activé et corpscomplet/brouillon non reçus ; toutes les autres opérations avancées et une missionGoogle autonome complète non reçues. Un succèsGoogle est distingué d’une validation indépendante de l’artefact. Les sorties et erreurs originales sont conservées.

Code de raccordement1abd51d, lien court8f97bfd, ajustements de restitution/confinement5b98c9a. [PR37](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/37), branche codex/google-mcp-oauth-existant surPR35, sans fusionmain. M26P4/MANUAL-HOLD, modèles et distributionDell restent inchangés.

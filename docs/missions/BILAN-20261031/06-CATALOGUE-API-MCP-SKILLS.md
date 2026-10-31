# Catalogue des composants et niveaux de disponibilité

Le [CSV](composants-enfichables.csv) contient144 lignes :87 outils natifs,4 skills actifs,32 fonctions Google,15 familles amont et6 interfaces MCP clientes. Ces catégories sont de niveaux différents ;144 ne signifie pas144 applications indépendantes.

Le registre actif contient87 définitions et expose65 schémas dans le contexte interrogé. La façade cliente autorise35 noms ; Qwen Code peut en masquer un pour éviter la récursion. Les9 outils du serveur MCP historique sont distincts des6 interfaces de transport clientes.

Les quatre skills actifs sont `config-repair` v6, créé par JARVIS, et `debian-diagnostic`, `dell-roundtrip`, `github-publish` v1, initialisés par Codex. Le Skill Lab conserve9 versions et 15 runs au relevé. Leur catalogue est lu réellement ; aucune nouvelle exécution de skill n’est prétendue dans cet audit.

Google expose30 méthodes amont sous licence Apache-2.0 et2 extensions Sheets développées par Codex. Le callback et le stockage isolent les profils personnel/Éducation. Le personnel a reçu cinq API et des lectures depuis WebUI/Qwen Code lors de la mission Google. Pour Éducation, seules les lectures Drive, Calendar et Gmail sont reçues à ce stade, avec les reçus 164/166/168. Les écritures Docs/Sheets et les parcours clients Éducation ne sont pas encore réceptionnés. Le relais OAuth du projet amont reste externe ; les API Google ne sont pas du code développé par Codex.

GitHub réutilise `gh`, le broker et le skill de publication. Les réceptions antérieures sont conservées, pas rejouées. Les outils de recherche web/fetch sont enregistrés ; leur seule présence ne reçoit pas une nouvelle recherche depuis WebUI.

Goal de Qwen Code et missions JARVIS sont deux contrats distincts. Les connecteurs de cette interface OpenAI ne sont pas des composants installés sur le Mac et leurs jetons ne sont pas transférés à JARVIS.

Chaque ligne précise identifiant, origine, source, licence, localisation, version, adaptation, consommateurs et preuve. « Chargé » ne signifie pas « exécuté ». Le statut d’une fonction non testée n’est jamais extrapolé à partir d’une autre fonction du même connecteur.

[Schémas natifs](preuves/catalogue-outils.json) · [contrats Google](preuves/catalogue-google.json) · [état local](preuves/local.json).

Le catalogue complémentaire [api-routes.csv](api-routes.csv) contient26 chemins REST trouvés dans les sources installées. Ce sont des déclarations, pas26 parcours testés. Les [72 fiches applicatives par machine](applications-detail.csv) distinguent présence, configuration, démarrage et limites d’usage.


**Séparation Google :** les profils disposent de répertoires et jetons chiffrés distincts. L’interface actuelle reste toutefois un outil commun `google_mcp(profile=personal|education)`, pas deux conteneurs ou deux outils dotés de droits distincts. L’isolation complète demandée au niveau des interfaces reste à préparer ; elle n’est pas déclarée reçue par la séparation du stockage. Aucun changement d’architecture n’est fait pendant ce bilan.

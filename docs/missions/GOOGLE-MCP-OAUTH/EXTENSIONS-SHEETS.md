# Écritures Sheets : complément minimal préparé

Le catalogue amont expose seulement sheets.getText/getRange/getMetadata ; son groupe sheets.write ne contient aucun outil dans le commit reçu. Ce manque est distingué d’un refus OAuth effectivement observé : les comptes ne sont pas encore authentifiés.

Deux opérations locales additionnelles, sheets.create et sheets.writeRange, utilisent l’AuthManager, les scopes et le stockage du connecteur retenu. Elles ne sont pas présentées comme deux méthodes MCP amont. Elles sont encapsulées par le même outil google_mcp du registre/MCP JARVIS ; aucun deuxième orchestrateur ou base n’est créé.

Les [méthodes de création](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/create) et [mise à jour de cellules](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/update) acceptent officiellement le scope Drive complet, déjà demandé par l’application amont. Aucun scope additionnel non publié ni projetCloud propriétaire n’est ajouté. La passerelle fixe les deux endpoints et les payloads, valide l’identifiant et la plage, et écrit les valeurs en RAW.

Les contrats et protections sont testés en logiciel ; **aucune création ou écriture Sheets distante n’est reçue**. Après authentification, créer un classeur d’essai, écrire une valeur puis la relire via sheets.getRange. Un refus API403, une politique de domaine ou un scope refusé devra être enregistré ; le fait que le scope soit documenté ne prouve pas qu’un compte l’a accordé.

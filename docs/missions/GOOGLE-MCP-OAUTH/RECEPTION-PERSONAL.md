# Compte personnel — réception Google réelle

L’autorisation fournie par le propriétaire a été retrouvée dans le profil personal. Une première rechercheDrive réelle a retourné troisfichiers, reçu132. Les originaux sont privés ; les preuves publiées n’exposent ni identifiants de documents ni messages personnels.

| Fonction | Réalisation et contrôle | Preuve canonique |
|---|---|---|
| Drive | Recherche de documentsGoogle réels, puis lecture d’un document existant sélectionné dans les résultats | 134 /146 |
| Docs | Création d’un document de réception et relecture du mêmeID ; exporttitre+contenu exactement conforme au texte de test | 136 /144 |
| Sheets | Création d’un classeur, écritureRAW d’une ligne, relecture du mêmeID/plage ; marqueur et valeur affichée42 exacts | 142 /148 /150 |
| Calendar | Lecture du calendrierprimary, deuxévénements retournés | 138 |
| Gmail | Recherche puis lecturemetadata du même message ; pas de corps complet reçu ni d’envoi | 140 /152 |
| Open WebUI | Modèle27B lit réellement le document de test et affiche le marqueur attendu | 154, capture et historique privés |
| Qwen Code | Modèle80B lit le même document viaMCP ; résultat final conforme, septtours | Voir RECEPTION-PERSONAL.json |
| Persistance | Services rechargés avant la lectureWebUIGoogle ; authentification retrouvée sans nouvelle connexion navigateur | Horodatages service/audit comparés |
| RenouvellementOAuth | Seule l’échéance locale a été avancée pour tester l’AuthManager existant ; nouveauGoogleDriveappel réussi et nouvelle échéance future | 162 |

Le renouvellement a utilisé le mécanisme amont et son relais, sans afficher de token. Une sauvegarde chiffrée privée permettait le retour arrière ; elle n’a pas été restaurée, le renouvellement ayant réussi. Ni révocation ni nouvelle autorisation utilisateur n’a été effectuée.

L’export docs.getText inclut son en-tête Document Title ; la comparaison porte sur cet export complet. Sheets.getRange retourne des valeurs formatées :42est lu comme chaîne, sans prétendre avoir vérifié le type interne en UNFORMATTED_VALUE.

Les premiers reçusGoogle conservaient remote_access_verified=false par conception initiale avantauthentification. Le correctif5b98c9a distingue maintenant réponseGoogle réussie, calcul localtime et validation indépendante du résultat. Les anciens reçus restent inchangés et leurs contenus sont contrôlés séparément. Les pièces jointes de brouillon restent confinées au dossier de téléchargement du profil ; aucune pièce jointe privée arbitraire ni envoi n’est autorisé.

**Verdict personnel : GO avec réserves.** Les cinqAPI ont été utilisées, Docs/Sheets créés et relus, et les deuxclients ont lu une donnéeGoogle réelle. Gmailenvoi/corpscomplet/brouillon, toutes les opérations de modification et la mission autonome complète n’ont pas été reçus dans ces essais. Le compteÉducation reste séparément bloqué avantOAuth.

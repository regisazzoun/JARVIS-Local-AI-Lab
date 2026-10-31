# Compte Éducation — refus signalé pendant la connexion

Le propriétaire rapporte : « Désolé, vous n’avez pas accès à ce service. Pour l’activer, veuillez vous connecter à votre console d’administration. » Aucun jeton Éducation n’a été enregistré ; le statut local reste AUTH_REQUIRED. Le compte personnel est indépendant et fonctionne.

Ce message est compatible avec un service désactivé ou une politique d’accès du domaine. Il ne suffit pas à déterminer quel service est désactivé ni à conclure que le clientOAuth est mal configuré. Le nom du site affiché et l’éventuel codeGoogle ont été demandés, sans URL complète susceptible de contenir des paramètresOAuth. Ce refus a été observé par le propriétaire, pas reproduit dans une session Éducation par Codex.

Google indique que les restrictions de service et d’applications d’un compteÉducation relèvent de l’administrateur : [aide comptesÉducation](https://support.google.com/edu/classroom/answer/11081157?hl=fr), [erreurs Sign in with Google](https://support.google.com/accounts/answer/16668185?hl=fr). Une restriction de service et un refus admin_policy_enforced ne sont pas confondus sans code/page précis.

Aucune politique de l’établissement n’est modifiée ou contournée. Aucun projetGoogleCloud personnel n’est requis pour diagnostiquer ou demander l’activation du service approprié. La suite consiste à identifier l’écran exact, puis à faire traiter le réglage ciblé par l’administrateur habilité. Les essais du compte personnel continuent séparément.


## Précisions fournies par le propriétaire

Page : access.workspace.google.com/ServiceNotAllowed, paramètre application=995920231026, source=scrip. Le propriétaire indique être administrateur du WorkspaceÉducation. Aucun tokenÉducation obtenu à ce stade.

La correspondance officielle de cet identifiant de service n’a pas été établie. Ne pas le présenter comme l’identifiantOAuth du connecteur ni en déduire une obligationGemini/GoogleOne payante. Le clientOAuth réellement installé est338689075775-o75k922vn5fdl18qergr96rp8g63e4d7.apps.googleusercontent.com, intitulé Gemini CLI Workspace Extension.

Prochain diagnostic depuis le compteadmin : Sécurité → Contrôle des accès et des données → ContrôlesAPI → Gérer l’accès des applications ; retrouver le client exact et observer son état pour le compte/unité concernés. La [documentationGoogle](https://knowledge.workspace.google.com/admin/apps/control-which-apps-access-google-workspace-data) distingue le contrôleOAuth des services désactivés. Aucun changement généralisé de politique n’est prescrit sur la seule base du numéro995920231026.

# Authentifier les deux profils sans projet Google Cloud personnel

Le connecteur retenu fournit son client OAuth applicatif. **Ne crée pas de projet Google Cloud et ne télécharge pas de client_secret.json.** L’ancien guide PR35 décrivait le connecteur précédent ; la présente décision propriétaire et ce guide s’appliquent à cette extension.

Depuis le **Terminal du MacBook connecté à Tailscale**, exécuter pour le compte personnel :

```bash
ssh -t -L 8769:127.0.0.1:8769 adminjarvis@jarvis-macmini.tail805e83.ts.net '/home/adminjarvis/.local/bin/google-mcp-connect --profile personal'
```

Laisser le Terminal ouvert, copier l’URL Google affichée dans le navigateur, sélectionner le compte personnel puis accorder les permissions souhaitées. Google affiche « Gemini CLI Workspace Extension ». Le retour sur127.0.0.1:8769 rejoint le Mac mini par le transfert SSH et enregistre les jetons chiffrés dans le profil personal. La page confirme le raccordement. La commande se termine ; le transfert n’est plus nécessaire pour l’utilisation quotidienne.

Répéter ensuite pour le compte Éducation :

```bash
ssh -t -L 8769:127.0.0.1:8769 adminjarvis@jarvis-macmini.tail805e83.ts.net '/home/adminjarvis/.local/bin/google-mcp-connect --profile education'
```

Choisir explicitement l’autre compte dans le sélecteur Google. Ne jamais coller de jeton, mot de passe ou JSON de credentials dans le chat. Ce parcours ne demande aucun copier/coller de jeton.

Une autorisation Google incomplète ou une politique administrateur peut refuser certaines permissions. Conserver le message d’erreur sans paramètre sensible ; le profil personnel reste indépendant. Une simple page de connexion affichée n’est pas une authentification réussie.

Le logiciel et les appels MCP s’exécutent sur le Mac mini. Le client OAuth et l’échange/renouvellement des jetons utilisent le relais fourni par le projet, `google-workspace-extension.geminicli.com` : le refresh token lui est transmis lors du renouvellement. Ce n’est pas un OAuth entièrement autonome hors fournisseur. Aucun abonnement ni projet/facturation Cloud personnel n’est configuré.

Après connexion, demander dans Open WebUI : « Avec google_mcp, consulte le statut du profil personal, puis découvre drive.search et cherche mes documents. » Les recherches/lectures puis création et relecture d’un document d’essai restent nécessaires pour réceptionner réellement les accès. Répéter avec education. Le serveur amont est limité à la lecture Sheets ; deux méthodes additionnelles JARVIS de création/écriture sont préparées mais restent à recevoir après authentification ; l’envoi Gmail n’est pas activé par cette mission.

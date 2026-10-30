# Raccorder Google à la fin de la mission

Le propriétaire a demandé un rappel et un accompagnement en fin de mission. Le connecteur et son assistant OAuth sont installés ; **aucun compte Google local n’est encore authentifié**. Les connexions Google éventuellement disponibles à Codex ne sont pas des identifiants transférables à JARVIS.

## Préparation dans Google Cloud

1. Ouvrir la [console Google Cloud](https://console.cloud.google.com/), choisir ou créer le projet JARVIS.
2. Activer les API Google Drive, Docs, Sheets, Calendar et Gmail dans ce projet.
3. Configurer l’écran de consentement OAuth. Pour une application externe en mode test, ajouter le compte à connecter parmi les utilisateurs test.
4. Créer un **client OAuth “Application de bureau”**, puis télécharger son JSON. Il ne s’agit pas d’une clé de compte de service. Ne pas transmettre ce JSON dans le chat ou dans GitHub.

Voir les [instructions officielles de création des identifiants](https://developers.google.com/workspace/guides/create-credentials#desktop-app).

## Connexion initiale depuis le MacBook

Les commandes suivantes sont à exécuter dans Terminal sur le MacBook connecté au tailnet. Nommer le fichier téléchargé `client-google-jarvis.json` dans Téléchargements pour reprendre cet exemple.

```bash
ssh adminjarvis@jarvis-macmini.tail805e83.ts.net 'install -d -m 700 /home/adminjarvis/.config/jarvis/google'
scp ~/Downloads/client-google-jarvis.json adminjarvis@jarvis-macmini.tail805e83.ts.net:.config/jarvis/google/client-personal.json
ssh adminjarvis@jarvis-macmini.tail805e83.ts.net 'chmod 600 /home/adminjarvis/.config/jarvis/google/client-personal.json'
ssh -t -L 8769:127.0.0.1:8769 adminjarvis@jarvis-macmini.tail805e83.ts.net '/home/adminjarvis/.local/bin/google-connect --profile personal --client-file /home/adminjarvis/.config/jarvis/google/client-personal.json'
```

Laisser cette dernière fenêtre ouverte. Ouvrir dans Safari l’URL Google affichée, sélectionner le compte voulu et accorder les accès. Le retour vers127.0.0.1:8769 passe par le transfert SSH temporaire ; la page confirme le raccordement. Ce transfert sert uniquement à cette connexion initiale. L’usage quotidien reste dans Open WebUI, sans tunnel manuel.

Les jetons sont stockés sous `~/.config/jarvis/google/personal/token.json`, permissions600, dans un dossier700. L’assistant utilise la bibliothèque OAuth officielle ; il n’affiche pas les jetons.

## Vérification dans Open WebUI

Ouvrir le profil **JARVIS — Conversation et outils**, puis demander :

> Consulte le statut Google du profil personal, recherche mes documents Google Docs dans Drive, puis lis le document que je t’indiquerai. Ne modifie rien.

La réception Google exige ensuite une recherche réelle, une lecture et, dans un espace d’essai autorisé, une création suivie d’une relecture. Le seul statut `configured` ne prouve pas l’accès distant.

Pour le compte Éducation, répéter l’autorisation avec `--profile education` afin de conserver deux identités séparées. Un refus affiché par l’administration du domaine doit être documenté ; il ne doit pas être contourné ni masquer les autres fonctions reçues.

## Fonctions préparées

Drive : recherche, métadonnées, création de dossier et renommage. Docs : lecture, création, ajout et remplacement de texte. Sheets : lecture, écriture de cellules et création. Calendar : lecture, création et modification sans invitations. Gmail : recherche, lecture et brouillons. **Aucun envoi Gmail dans cette mission.** Ces fonctions restent non réceptionnées à distance avant authentification et essais réels.

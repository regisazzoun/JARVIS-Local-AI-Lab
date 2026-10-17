> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/MISSION-13E-UTILISATION.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 13E — utilisation immédiate

## Mac mini ou macOS
Sur le serveur, ouvrir **http://localhost:8765**. Depuis macOS, utiliser l’accès SSH existant :
```bash
ssh -N -L 8765:[ADRESSE PRIVÉE EXPURGÉE]:8765 COMPTE@ADRESSE_PRIVEE_DU_SERVEUR
```
Ouvrir la même URL localhost dans le navigateur du Mac. Les accès SSH doivent déjà fonctionner : le rejet éventuel de clé relève de 13D, pas d’un défaut de la chaîne vocale.

Sur un terminal privé du serveur, consulter les identifiants :
```bash
cat /opt/jarvis/conversation/runtime/credentials.txt
```
Ne pas copier ce contenu dans un rapport, une issue ou une capture. Se connecter, autoriser le microphone dans le navigateur et dans les réglages de confidentialité macOS. Choisir microphone et haut-parleur côté client.

Cliquer « Démarrer / arrêter le microphone », parler, puis cliquer à nouveau. Ou maintenir Push-to-Talk et relâcher. Par défaut, la transcription déclenche la réponse ; décocher « Envoyer après transcription » pour corriger avant envoi. Le modèle réfléchit, le texte apparaît et Piper Tom parle. « Arrêter l’audio » interrompt la lecture ; si lecture automatique bloquée, cliquer ▶ dans le lecteur natif. « Lire la dernière réponse » prépare une nouvelle lecture. Les enregistrements ne sont pas conservés par le backend.

Choisir un moteur sans créer une nouvelle identité. « Nouvelle conversation » démarre un échange séparé ; « Reprendre une conversation » récupère l’historique. Décocher la conservation démarre une nouvelle session en RAM, sans effacer les anciennes données. Dans Mémoire, consulter les propositions, approuver/refuser explicitement, corriger, supprimer ou marquer obsolète ; les souvenirs de projet sont filtrés par projet. Aucun silence ou absence de réponse n’approuve une proposition.

## iPhone
La disposition mobile est testée sous Chromium, pas Safari/iOS physique. Une adresse LAN en HTTP ne suffit pas pour le microphone. L’accès iPhone HTTPS privé n’est **pas activé** dans 13E : la configuration préparée doit être mise en service lors d’une mission d’accès distincte, sans exposition publique. Aucune URL distante fonctionnelle n’est revendiquée.

Après activation validée : ouvrir l’URL HTTPS privée avec certificat reconnu, se connecter, autoriser le micro Safari, garder la page au premier plan, utiliser le bouton démarrer/arrêter, et ▶ natif si nécessaire. Tester Wi-Fi puis réseau mobile/VPN ; la suspension en arrière-plan peut interrompre capture et lecture. Ajouter à l’écran d’accueil seulement après ces contrôles.

## Dépannage
- Micro absent : origine localhost/HTTPS, permissions navigateur et système, périphérique sélectionné.
- Silence ou transcription fausse : parler distinctement, rapprocher micro, corriger le texte avant envoi.
- Audio bloqué : ▶ dans le lecteur, volume et périphérique de sortie ; aucune écoute physique validée automatiquement.
- HTTP 401 : se reconnecter, notamment après redémarrage.
- HTTP 409 : une opération JARVIS est déjà en cours, attendre avant réessai.
- Délai modèle : premier chargement plus lent, choix manuel de Llama si besoin ; aucun modèle n’est téléchargé automatiquement.

Contrôles :
```bash
systemctl status jarvis-conversation.service --no-pager
journalctl -u jarvis-conversation.service -n 40 --no-pager
/opt/jarvis/conversation/scripts/diagnostic
```

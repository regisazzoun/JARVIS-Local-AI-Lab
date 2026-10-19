# Bureau Dell — accès LAN et Tailscale reçus le19 octobre2026

Rédigé par Codex lors de la vérification indépendante du18 octobre2026. Les appels de configuration et de test ont été exécutés par JARVIS. Le serveur TigerVNC et la session Plasma sont des services distincts, sur le bureau virtuel :21, avec clavier français vérifié. Le port5921 écoute uniquement sur le loopback du Dell.

Depuis un poste disposant de l’identité SSH autorisée, ouvrir un tunnel vers le Dell (remplacer le paramètre par sa destination LAN connue) :

```sh
ssh -N -L 15921:127.0.0.1:5921 adminjarvis@<DELL_LAN>
```

Le client VNC se connecte ensuite à `127.0.0.1:15921` avec l’authentification VNC existante conservée privée. Une connexion directe à l’adresse LAN du Dell sur5921 n’est pas la procédure configurée. Aucun port Bbox n’est redirigé.

Le Dell possède désormais son client Tailscale enrôlé et en ligne (`Running`). Le propriétaire confirme l’usage KDE/VNC depuis son Mac. JARVIS a séparément testé les tunnels LAN et Tailscale avec authentification RFB et réception effective d’image ; voir les [preuves](RECEPTION-MISSION21.md).

Pour le trajet direct sur le tailnet, utiliser le nom/adresse Tailscale réel du Dell, vérifié dans son client Tailscale :

```sh
ssh -N -L 15921:127.0.0.1:5921 adminjarvis@jarvis-dell
```

`jarvis-dell` nécessite la résolution MagicDNS du poste ; à défaut utiliser son adresse tailnet connue. Fermer le tunnel précédent avant de réutiliser le même port local, ou choisir un autre port libre. Se connecter ensuite en VNC à `127.0.0.1:15921` avec le secret existant, conservé privé. Le profil interne du broker `dell-observe` n’est pas un nom DNS.

Historique conservé : le18oct, le client était installé mais `NeedsLogin`, et seule la voie LAN était reçue. Le test par passerelle Mac ne suffisait pas à valider le trajet direct. Le19oct, Codex a corrigé la lecture du secret par le client de test ; le mot de passe du serveur et les accès utilisateur fonctionnels ont été préservés.

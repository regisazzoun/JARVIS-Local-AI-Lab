# Bureau Dell — procédure vérifiée et réserve Tailscale

Rédigé par Codex lors de la vérification indépendante du18 octobre2026. Les appels de configuration et de test ont été exécutés par JARVIS. Le serveur TigerVNC et la session Plasma sont des services distincts, sur le bureau virtuel :21, avec clavier français vérifié. Le port5921 écoute uniquement sur le loopback du Dell.

Depuis un poste disposant de l’identité SSH autorisée, ouvrir un tunnel vers le Dell (remplacer le paramètre par sa destination LAN connue) :

```sh
ssh -N -L 15921:127.0.0.1:5921 adminjarvis@<DELL_LAN>
```

Le client VNC se connecte ensuite à `127.0.0.1:15921` avec l’authentification VNC existante conservée privée. Une connexion directe à l’adresse LAN du Dell sur5921 n’est pas la procédure configurée. Aucun port Bbox n’est redirigé.

JARVIS a installé le client Tailscale et activé son service. L’état observé est `NeedsLogin`, sans adresse du tailnet : aucun test VNC direct par Tailscale ne peut être déclaré reçu. L’enrôlement nécessite une identité de compte authentifiée ou une clé d’enrôlement valide, absente des emplacements privés vérifiés. Aucun état Tailscale du Mac n’est copié sur Dell. Les instructions officielles sont [installation Linux](https://tailscale.com/docs/install/linux) et [enrôlement par clé](https://tailscale.com/docs/features/access-control/auth-keys).

Après enrôlement, reprendre la même mission persistante et tester le même tunnel en utilisant la destination Tailscale du Dell. Le contrôle doit authentifier RFB et recevoir une image du bureau, pas seulement ouvrir un port. Le test LAN antérieur utilise un client réel sans écran depuis le Mac ; il ne démontre pas l’utilisation d’un MacBook physique.

Une passerelle Mac vers le bureau existe aussi. Son fonctionnement ne remplace ni l’installation d’un client propre au Dell ni la réception de l’accès direct au tailnet. Les formulations divergentes éventuelles du rapport brut du modèle sont des réserves sémantiques, pas une configuration alternative.

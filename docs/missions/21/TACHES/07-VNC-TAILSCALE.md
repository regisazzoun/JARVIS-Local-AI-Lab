# 21.07 — Bureau KDE distant, LAN et Tailscale
**Cible :** Dell n°1, Debian 13 + KDE Plasma/SDDM.
**Action :**
1. Inspecter les sessions X11/Wayland et serveurs VNC existants, les interfaces LAN, le pare-feu et Tailscale.
2. Choisir une solution compatible : **TigerVNC** pour une session KDE virtuelle indépendante, ou **x11vnc** si partage d'une vraie session X11 déjà ouverte est voulu/possible.
3. Installer, configurer un utilisateur/session et le service systemd ; conserver authentification VNC distincte, secrets privés.
4. Donner un accès graphique depuis le LAN local et depuis les appareils du tailnet Tailscale, via liaison privée et/ou tunnel chiffré approprié. Pas de publication Internet, pas de redirection Bbox.
5. Vérifier le service, l'authentification, la session KDE et, avec un client disponible, les connexions LAN et Tailscale. Si test client impossible, déclarer exactement la réserve ; un port ouvert n'est pas une preuve de bureau utilisable.
6. Vérifier l'absence de régression SSH, Ollama et JARVIS. Fournir les paramètres **non secrets** de connexion et la procédure de réutilisation sur Dell n°2, sans l'installer maintenant.
**Résultat :** `RAPPORTS/07-VNC-LOCAL-TAILSCALE.md`.
**Réception :** installation et tests réellement exécutés, limites précisément signalées. Puis rapport final et publication.

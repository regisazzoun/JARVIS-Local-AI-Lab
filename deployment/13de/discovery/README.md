# Découverte depuis le shell Debian Installer chargé en RAM

Préparé sans activation réseau. Initrd réellement servi lors de PXE-01 inspecté : usr/bin/wget GNU 1.25.0 accepte --post-file ; BusyBox 1.37.0 contient nc, sh, ip, mktemp, cat, readlink, wc, grep et sed. Le binaire BusyBox extrait a servi à vérifier la syntaxe du collecteur. Aucun initrd modifié ni nouveau boot requis. Présence effective sur le Dell revérifiée par command -v à l'exécution.

collect.sh lit uniquement /proc et /sys. Il refuse un DMI autre que Dell 5820 et refuse /tmp si son système de fichiers n'est pas identifié RAM. Rapport et accusé stockés uniquement dans un répertoire temporaire RAM du Dell. Pas de lecture brute des NVMe, assemblage RAID, montage, partitionnement, installation, benchmark ou écriture sysfs. Les composants non exposés restent absents : notamment DIMM détaillées/SMART/superblocs RAID ne sont pas déduits du silence de sysfs.

Le script rendu et le jeton sont dans deployment/13de/private/discovery-shell, ignoré par Git. Rapport attendu : dell-hardware.txt. Jeton aléatoire de 96 bits dans une URL de capacité ; chaque GET/POST exige ce jeton et l'IP Dell 192.168.1.74. HTTP transporte le jeton et le rapport en clair sur le LAN. Aucun annuaire ni fichier arbitraire n'est exposé. POST borné à 1 Mio, écriture exclusive 0600 ; affichage du texte reçu avec neutralisation des caractères de contrôle. Aucun contenu reçu n'est exécuté sur JARVIS.

Restriction réseau proposée : table nft temporaire jarvis_discovery, uniquement TCP 8090 sur enp4s0 ; rejet des MAC différentes de b0:7b:25:1c:a5:79 et des sources IPv4 différentes de 192.168.1.74. Serveur lié uniquement à 192.168.1.99. Le filtrage MAC sur ce LAN direct n'est pas une protection contre usurpation. Aucun changement aux règles existantes SSH/Tailscale, au DHCP, aux services JARVIS ou aux unités systemd.

## Après autorisation explicite seulement

Depuis deployment/13de/private/discovery-shell :

    sudo -n python3 -u serve-session.py

Le superviseur vérifie les empreintes et l'IP locale, applique la seule table temporaire, puis lance receive.py sans privilèges en adminjarvis. Il supprime la table après réception, timeout (20 minutes) ou signal TERM/INT. Aucun démarrage si la table existe déjà. Le rapport est automatiquement imprimé sur stdout dans la session Codex ; l'agent attend sa réception avec l'outil de session. Aucun serveur n'est activé par cette documentation.

Après indication RECEIVER_READY, saisir sur le Dell la ligne unique de COMMAND.txt. Elle vérifie wget, télécharge le collecteur avec le jeton puis l'exécute. Le collecteur vérifie --post-file et utilise wget pour POST ; nc est le repli automatique d'envoi. Si wget est réellement absent, FALLBACK-COMMAND.txt prépare le téléchargement par nc, également présent dans l'initrd inspecté. Si l'envoi n'est pas confirmé, le rapport reste en RAM et son chemin est affiché ; aucun reboot nécessaire.

Arrêt manuel : SIGTERM au PID DISCOVERY_SUPERVISOR affiché par le lancement. Vérifier ensuite absence d'écoute 8090 et de table jarvis_discovery. Ne jamais supprimer une autre table.

## Validation sans service réseau

Test_receive exerce les vrais handlers avec un serveur simulé, sans ouverture de socket : mauvaise IP, mauvais jeton, GET authentifié, taille excessive, rapport tronqué, réception complète, permissions 0600, affichage automatique. Refus du collecteur sur le Mac mini confirmé avant écriture temporaire ou envoi. Syntaxe nft vérifiée avec --check, aucune application. Transport réel du Dell en attente de l'autorisation et de la commande console.

Mission arrêtée à la demande explicite de l'utilisateur avant autorisation d'activation. Aucun récepteur activé, aucun rapport matériel Dell reçu. Scripts conservés comme préparation uniquement.


Reprise suivante : la découverte est désormais embarquée automatiquement par bootstrap/build-discovery.py ; voir docs/missions/13D-E/BOOTSTRAP-AUTOMATISE.md. La commande manuelle historique reste un repli, pas l'étape physique proposée. Le récepteur supporte un CIDR d'origine avec filtrage MAC externe et produit un manifeste non approuvé quand configuré. Aucun ancien arrêt de mission ne vaut autorisation de réactivation.

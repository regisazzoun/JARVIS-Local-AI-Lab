# Diagnostic des sockets — observations Codex

## Point de refus démontré

Le processus Python de diagnostic et son parent bash descendent de `codex`, PID1 de la vue courante, PPid0. UID/EUID/GID1000. Les groupes extérieurs non mappés apparaissent65534 ; le groupe1000 est présent. `NoNewPrivs=1`, `Seccomp=2`, un filtre, `CapEff=0`. Les mappings utilisateur/groupe contiennent `1000 0 1` : la vue utilise un espace utilisateur distinct. La racine et /run sont montés en lecture seule. Le cgroup visible correspond à une session utilisateur systemd.

Espaces observés : réseau4026533078, montage4026533075, utilisateur4026533133, PID4026533077, identiques pour codex/bash/python. `/proc/net/unix` ne montre aucun listener dans cet espace réseau. Cela ne démontre pas l'absence de serveur dans l'espace hôte.

- `socket(AF_UNIX, SOCK_STREAM)` réussit.
- `connect('/run/jarvis-host/bridge.sock')` échoue avec `PermissionError`, errno1, `Operation not permitted`.
- `socket(AF_INET, SOCK_STREAM)` et AF_INET6 échouent dès la création avec errno1.
- Le socket exact existe, type socket, mode0660, UID apparent65534, GID1000. Son répertoire existe en0755. La session possède le groupe1000 : aucune justification pour chmod/chown arbitraire.
- systemctl échoue au raccordement local au bus, également EPERM. Aucun état de service reçu.
- `/proc/self/attr/current` indique `unconfined` ; cela n'annule pas seccomp ni les espaces de noms.

Le confinement est démontré ; l'attribution de chaque refus à une règle seccomp précise reste non démontrée car le filtre n'est pas lisible ici. Bubblewrap est installé ; son emploi comme lanceur de cette session n'est pas prouvé : le parent hôte n'est pas visible. Ne pas confondre ce confinement Codex avec celui de host_exec JARVIS.

## Distinctions

| Hypothèse | Observation |
| --- | --- |
| Socket absent | Réfuté pour le chemin exact ; deux chemins supposés initiaux absents étaient incorrects |
| Création Unix interdite | Réfuté dans cette session |
| Création TCP interdite | Démontré IPv4/IPv6 |
| Connexion Unix interdite | Démontré EPERM avant échange |
| Permissions classiques inadéquates | Non démontré ; groupe1000 cohérent |
| ECONNREFUSED / serveur absent | Non observé ; processus hôte non accessible |
| Refus d'authentification ou politique broker | Aucune réponse broker, donc non établi |
| Politique historique mission11 responsable | Non établi ; libellé sans sélection d'habilitations dans le code |

La politique privée renvoie EACCES13 à l'ouverture ; ce refus de fichier est distinct d'EPERM1 sur transport. Aucun contenu privé publié. Les sources sous /usr/local et /opt sont lisibles, mais les destinations de déploiement ne sont pas inscriptibles.

Aucune session hôte autorisée disponible via les outils courants n'a fourni de comparaison effective. Les appels EPERM ne sont pas réessayés en boucle.

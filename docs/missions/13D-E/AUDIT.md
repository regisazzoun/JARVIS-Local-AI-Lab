# Audit non destructif — 15 octobre 2026

Rapport produit avant toute installation. Aucune installation système effectuée.

| Domaine | Observation | Conclusion |
| --- | --- | --- |
| OS | Debian 13.7 trixie, x86_64 ; noyau 6.18.54-1-t2-trixie | Compatible avec outillage utilisateur amd64 ; noyau conservé |
| CPU/RAM | i7-8700B, 6 cœurs/12 threads, VMX/VT-x ; 31 Gio RAM, 28 Gio disponibles | VM envisageable avec plafond 2 vCPU/4 Gio |
| Stockage | NVMe hôte 465,9 Gio ; racine LVM, 352 Gio libres | Aucun disque physique utilisable par le laboratoire |
| Virtualisation | /dev/kvm absent dans cette session ; QEMU, libvirt, OVMF absents | KVM non prouvé ; TCG sans changement noyau à envisager après fourniture des outils |
| Réseau | Interfaces Ethernet, Wi-Fi, tailscale0 visibles via sysfs | netlink et /proc/net/route restreints : adresses, routage, DHCP/DNS actifs non vérifiables |
| SSH/Tailscale | openssh-server 10.0p1, tailscale 1.104.1 installés | État des services inaccessible ; aucun changement des configurations ou clés |
| Clé de déploiement | Aucune clé publique accessible dans le périmètre de cette session | Ne rien générer ; fournir ultérieurement une clé publique existante dont JARVIS possède le signataire |
| Ansible | Exécutable absent ; pip absent | Préparation possible ; exécution et idempotence réelle non attestées |
| PXE | dnsmasq-base 2.91 installé ; iPXE/TFTP/OVMF absents | Aucun DHCP démarré ; préférer DHCP/TFTP internes à QEMU |
| Docker | docker.io 26.1.5 installé ; socket refusée | Conteneurs et disponibilité WebUI non vérifiables |
| JARVIS/Ollama | Sources et environnement Python sous /opt/jarvis/conversation ; rapports 13F présents | systemd, processus hôte et sockets inaccessibles ; aucune preuve de santé courante |
| Agent 13F | Registre outils, Bubblewrap et politique consultés en lecture seule | /work 128 Mio, 25 s, réseau interdit, Dell désactivé : incompatible avec VM longue sans contrôleur distinct |
| GitHub | Lecture connecteur opérationnelle ; gh local non authentifié ; .git racine vide et protégée | Publication via connecteur et branche dédiée ; ne pas initialiser le dépôt racine |

Limite : la session dispose d'une vue restreinte des processus et sockets. Une absence dans cette vue ne prouve pas l'arrêt d'un service hôte. Aucun SSH Dell tenté. AGENTS.md absent de la racine GitHub (404) et des répertoires d'instructions locaux consultés.

Diagnostic complémentaire requis hors sandbox : état systemd, écoute DHCP/DNS, routes, accès KVM et santé HTTP JARVIS/Ollama/WebUI. Toute installation système reste soumise à validation ciblée ; elle n'est pas nécessaire à la génération des présents livrables.

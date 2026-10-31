# Inventaire logiciel par machine

| Machine | Paquets APT installés | Environnements Python trouvés | Unités chargées observées | États |
|---|---|---|---|---|
| mac | 3070 | 4 | 183 | {'active': 79, 'inactive': 104} |
| dell1 | 1233 | 1 | 126 | {'active': 45, 'inactive': 81} |
| dell2 | 446 | 0 | 107 | {'active': 36, 'inactive': 71} |

[Applications utiles](applications-dell.csv), [catalogue APT/Python/npm/npm](logiciels.csv), [services chargés](services.csv), [Node projet](preuves/node-projects.json).

Mac : services conversation, broker, deux workers, JL03, WebUI, tools8092, guard8091, Apache, Ollama, LiveKit, watchdog et sauvegarde mémoire. Open WebUI 0.12.0 dans un seul conteneur Docker sain, volume persistant existant. Qwen Code0.26.4 est une dépendance de projet avec son propre Node ; l’absence de npmglobal ne décrit pas son installation. Python 3.13.5 système, deuxvenvs actifs conversation/voix et deux environnements historiques trouvés.

Dell 1 : deux processus Ollama depuis/opt/ollama/bin, pas dans PATH ; il serait faux de conclure «absent» depuis `ollama --version`. Venv TTS spécialisé, bureau Plasma/VNC, supervision et profilGPU. Dell 2 : Debian minimal446 paquets relevés avant filtrage, SSH/Python/Node CUDA, console de progression. Pas de conteneur, contrôleur Ansible, Git/npm/Qwen Code trouvés dans les périmètres examinés. Leur absence n’est pas un échec d’installation 14B : ses rôles n’exigeaient pas tous ces outils.

Aucun service en échec au relevé des trois hôtes. Inactive peut désigner un oneshot terminé, jamais automatiquement une panne. Tous les services chargés sont dans services.csv ; les fichiers d’unités installés et timers complets restent dans les originaux privés avec empreintes.

Couverture : dpkg exhaustif pour son catalogue installé ; distributions Python des venvstrouvés jusqu’à profondeur 6 sous/opt,JARVIS,.local ; projets Node jusqu’à profondeur 4 complétés par Qwen runtime. Cela ne garantit pas la découverte de tout binaire manuel sur tout disque. La présence d’un paquet n’atteste ni son import ni son usage parJARVIS. Les versions inconnues sont conservées comme telles.


Ressources Mac observées : slice de fond plafonné à900%CPU, soit9 des12 threads logiques (75%), MemoryMax8GiB ; slice interactif CPUWeight1000 et MemoryLow20GiB. Ces paramètres sont lus dans systemd, pas une nouvelle réception de la dynamique75/25 ni une partition de la VRAM. Les bascules sous interaction restent les essais historiques28A. [Configuration lue](preuves/configurations.json).

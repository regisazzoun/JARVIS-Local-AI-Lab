# Mission continue 13D-E / 14 — nouvelle tentative, 17 octobre 2026

La mission complète a été relancée par le propriétaire : installation Debian neuve, conservation prioritaire du RAID/GPT/ESP, comptes jarvis-bootstrap et adminjarvis avec le même mot de passe utilisateur privé, maintien SSH par mot de passe et clé, clavier français, puis Ansible/NVIDIA/CUDA/Ollama/modèles/intégration/réception. Les anciennes clôtures, reports IA et révocations automatiques ne régissent plus cette tentative. Aucun résultat physique nouveau n'est déclaré réussi à ce stade.

## Chaîne préparée et exécutants

`deployment/13de/reinstall/` contient le constructeur d'overlay du netboot existant, le démarrage SSH en RAM, l'installation de la racine sur miroir préexistant, le contrôleur PXE/SSH, le suivi, le playbook serveur IA, les tests d'intégration avec restauration des paramètres précédents en cas d'échec et la publication des seuls résultats expurgés. Les scripts de poursuite attendent la preuve d'accès indépendant par mot de passe/clé/sudo avant la phase IA. Les comptes de secours ne sont pas révoqués automatiquement.

La reconstruction de l'overlay est nécessaire pour ajouter la supervision SSH, le clavier français effectif et la réutilisation du RAID, que l'ancienne recette partman recréait. Le noyau Debian authentifié existant est conservé. Le démarrage supervisé ne retourne jamais au partitionneur et n'écrit aucun disque ; le contrôleur vérifie ensuite l'identité avant de lancer le script d'installation. Celui-ci exige un miroir RAID1 sain, deux membres exacts et deux ESP FAT/GPT ; il n'appelle ni mdadm --create, ni wipefs, ni un outil de repartitionnement. Le formatage ext4 vise uniquement le volume RAID racine contrôlé.

Une clé hôte de supervision et une clé hôte du système cible sont préparées dans le stockage privé et épinglées localement. Le SSH en mémoire utilise le port 2222 et une clé, limité à JARVIS. Le système installé utilise adminjarvis et jarvis-bootstrap, avec mot de passe utilisateur et clé publique. Le rapport de premier boot n'est plus l'unique voie de reprise.

## Vérifications préparatoires réellement effectuées

- Signature Release Debian, empreintes du noyau/initrd et des udebs ajoutés vérifiées ; secrets et identifiants restent privés.
- Test ciblé sans disque : chargement NVMe/RAID1/ext4, debootstrap disponible, sshd démarré. Carte française chargée et relue : keycode16=a, keycode17=z.
- Test ciblé en RAM sur réseau QEMU utilisateur avec redirection localhost : authentification SSH indépendante par clé, vérification stricte de la clé hôte et `uid=0` obtenus. Aucun disque ni installation complète VM.
- Syntaxe Python/shell et playbook Ansible vérifiée. Ces vérifications ne remplacent pas la réception physique à venir.
- ProxyDHCP/TFTP et HTTP actifs dans le périmètre Dell, ressources de boot HTTP vérifiées. Bbox demeure serveur DHCP d'allocation. Mail envoyé au propriétaire pour F12 → UEFI IPv4.

## IA et intégration à valider sur le Dell

Réutilisation de l'Ollama 0.40.3 et des modèles présents sur le Mac, sans modifier les sources : qwen3.5:27b-q4_K_M, ministral-3:14b-instruct-2512-q4_K_M et llama3.1:8b. Une seule RTX 3090 utilisable est exigée, l'UUID effectif est fixé dans CUDA_VISIBLE_DEVICES. Pilote et toolkit proviennent des paquets Debian compatibles ; nvidia-smi, VRAM Ollama et inférences réelles doivent valider l'accélération. Un échec de chargement du pilote reste un échec, jamais un succès supposé.

Whisper Small/Piper Tom, outils et mémoire SQLite restent sur le Mac mini. L'intégration change uniquement le backend d'inférence de la passerelle existante et d'Open WebUI, avec sauvegarde de configuration, sauvegarde SQLite en ligne et restauration des paramètres précédents si les tests échouent. Les tests doivent inclure authentification, réponse modèle, souvenir fictif temporaire dans la mémoire canonique, appel réel d'un outil autorisé, chaîne vocale sur WAV synthétique et requête Open WebUI. Aucune extension silencieuse des droits agentiques.

## Supervision et reprise

Vue locale : `python3 deployment/13de/reinstall/progress.py deployment/13de/private/reinstall-02/progress.json` (répéter avec watch si souhaité). Barres globale/par tâche, états, durée et dernière activité ; aucune coche sans validation réelle. Les phases sans mesure continue restent explicitement indéterminées. Le relais affiche cette vue sur tty1 de l'installateur et la conserve dans `/run/jarvis/progress.txt`, lisible depuis les consoles et SSH. Logs détaillés et transferts modèles restent privés.

Sur échec, consulter les fichiers privés controller.log, installer-tail.log, ai-phase.log et les marqueurs d'erreur. Ne pas relancer aveuglément le script de formatage : le marqueur RAM empêche un second lancement pendant la même session. Après reboot, l'existence de preuves privées doit guider la reprise ; ne pas repartir en PXE destructif pour un simple échec d'intégration.

La réception finale reste à établir : démarrage physique, stockage préservé, authentifications, Ansible idempotent, pilote/CUDA/inférence, intégration et redémarrage final. La publication automatique résume les seules étapes réellement validées, sur la branche existante, sans fusion.

Sources techniques : [preseed Debian trixie](https://www.debian.org/releases/trixie/amd64/apbs04.en.html), [pilotes NVIDIA pour Debian](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/debian.html), [installation Linux Ollama](https://docs.ollama.com/linux). Versions effectivement observées et preuves locales priment sur une supposition de compatibilité.

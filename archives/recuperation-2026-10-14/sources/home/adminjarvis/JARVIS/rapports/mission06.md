# JARVIS — Mission 06 : Open WebUI et utilisation quotidienne

12 octobre 2026 — **GO : Open WebUI fonctionne avec authentification, Llama 3.1 8B et inférence sur la Quadro.**

## Accès et utilisation

Ouvrir **http://192.168.1.99:3000** depuis un navigateur du LAN. Compte administrateur : **admin@jarvis.local**. Mot de passe initial dans [identifiants-admin.txt](../open-webui/identifiants-admin.txt), fichier mode 0600, répertoire parent 0700 ; changer ce mot de passe dans les paramètres du compte. Choisir `llama3.1:8b` et démarrer une conversation. Trois conversations « Mission 06 — Test … » sont conservées dans l’interface.

Installation/documentation : [open-webui](../open-webui/) et [README.md](../open-webui/README.md). Les secrets ne sont pas reproduits dans ce rapport ou les sorties des commandes.

## État initial et installation

Ollama 0.40.3 répondait, modèle et Quadro reconnus ; NVIDIA 595.91.07, noyau T2 6.18.54-1-t2-trixie. Docker/Compose absents. Simulation APT puis installation : **9 paquets nouveaux, zéro suppression et zéro modification de version des paquets existants** : docker.io/docker-cli 26.1.5+dfsg1-9+deb13u1, docker-compose 2.26.1-4, containerd 1.7.24~ds1-6+deb13u1, runc 1.1.15+ds1-2+b4, iptables 1.8.11-2, libip4tc2/libip6tc2 1.8.11-2, tini 0.19.0-3+b8. Le nom Debian est docker-compose, pas docker-compose-v2 ; aucune modification des dépôts ou apt update nécessaire.

Docker et containerd activés par les paquets. `/etc/docker/daemon.json` créé avant installation : iptables=false, ip6tables=false, bridge=none, ip-forward=false. Les règles nftables avant/après sont identiques. L’installation iptables crée ses alternatives ; Docker n’ajoute pas ici de pont/NAT/règles de filtrage. Ce réglage est adapté à cette installation en réseau hôte ; les futures applications Docker nécessitant un bridge demanderaient une revue de configuration.

Image officielle **ghcr.io/open-webui/open-webui:v0.12.0**, version publiée le 10 octobre 2026, fixée également au digest **sha256:1565038903151ced924b5a3226f73f40f16963df4b910441f6391f10144afdaa**. Compose dans JARVIS/open-webui/compose.yaml. Conteneur jarvis-open-webui, volume nommé **jarvis-open-webui-data** monté sur /app/backend/data, politique restart unless-stopped. Aucun conteneur GPU ni NVIDIA Container Toolkit nécessaire : Open WebUI appelle Ollama sur l’hôte. [Installation officielle Open WebUI](https://docs.openwebui.com/getting-started/quick-start/), [release v0.12.0](https://github.com/open-webui/open-webui/releases/tag/v0.12.0).

## Réseau et authentification

Réseau Docker host ; Open WebUI écoute exclusivement **192.168.1.99:3000**. Ollama reste sur **127.0.0.1:11434**, accessible au conteneur via cette même boucle locale. Aucun port IPv6, aucune publication Docker et aucune redirection Internet créés. CORS limité aux origines de cette installation. La clé WEBUI_SECRET_KEY aléatoire stable est dans .env, mode 0600. WEBUI_AUTH=true ; inscriptions désactivées après création du premier administrateur, effectuée avant exposition LAN. API OpenAI externe désactivée, mode hors ligne/collecte télémétrique désactivée dans la configuration. [Configuration Open WebUI](https://docs.openwebui.com/reference/env-configuration/).

Tests : HTML de la page HTTP 200 (11 601 octets), health HTTP 200, connexion administrateur réussie, modèles visibles dont llama3.1:8b. Accès /api/models sans jeton : 401. Nouvelle inscription : 403. L’authentification ne chiffre pas HTTP : installation destinée à un LAN de confiance. Aucune vérification du routeur/NAT ou d’un client externe n’a été possible ; une redirection 3000 depuis Internet doit rester absente. Les tests HTTP utilisent l’adresse LAN depuis le Mac, pas un navigateur distant ni une session visuelle automatisée.

## Démarrage reproductible et GPU temporairement absent

Ollama manuel de 05D arrêté proprement puis remplacé par **jarvis-ollama.service**, exécuté comme adminjarvis avec mêmes binaires/modèles, contexte 4096, une requête parallèle et UUID Quadro fixé. API locale ; Restart=on-failure. **jarvis-open-webui.service** lance Compose après Docker et Ollama, sans télécharger une nouvelle image. Les deux unités sont enabled et actives ; configuration vérifiée avec systemd-analyze verify. Aucun reboot effectué : l’activation est vérifiée, le futur démarrage complet ne l’est pas.

Test logiciel d’absence d’accélérateur : seconde instance Ollama temporaire sur 127.0.0.1:11435, CUDA_VISIBLE_DEVICES=-1 ; démarre et liste le modèle, puis arrêtée. Aucun retrait physique ou test d’inférence CPU. Il n’existe pas de dépendance systemd à un périphérique NVIDIA : l’absence du GPU ne bloque pas le démarrage applicatif. La redécouverte GPU après un prochain branchement n’est pas garantie par ce test ; si nécessaire, après fin des requêtes, redémarrer seulement jarvis-ollama et vérifier nvidia-smi.

Le contournement matériel reste **démarrage Debian sans Core, puis branchement après affichage Intel**. Cette mission ne valide pas le démarrage Core connecté. L’adresse LAN fixe actuelle est nécessaire ; si elle change, adapter WEBUI_HOST/CORS avant relance. Un conteneur dont cette adresse est momentanément absente réessaie via sa politique de redémarrage.

## Tests d’inférence via Open WebUI

Trois appels **authentifiés à /api/chat/completions d’Open WebUI**, et non directement à Ollama. Les réponses ont été enregistrées comme conversations dans la base. Requêtes : définition courte de JARVIS, multiplication 17×23 avec vérification, fonction Python de crible d’Ératosthène/complexité. Le calcul donne **391**. Le dernier test atteint la limite de 256 tokens et coupe l’explication ; cela valide la génération de code, pas une réponse complète ou l’exécution du code généré. Les options de test limitaient contexte/tokens ; aucun outil d’exécution de code activé.

| Test | Durée murale | Chargement Ollama | Tokens générés | Tokens/s de génération |
|---|---:|---:|---:|---:|
| 1 | 5.68 s | 4.937 s | 47 | 71.18 |
| 2 | 1.93 s | 0.002 s | 133 | 70.53 |
| 3 | 3.72 s | 0.002 s | 256 | 70.10 |

Accélération attestée par les logs Ollama (CUDA/Quadro, **33/33 couches sur GPU**), le processus llama-server dans nvidia-smi, un pic de **5172 MiB de mémoire GPU** et **99 % d’utilisation GPU**. La VRAM occupée et l’activité sont échantillonnées pendant les requêtes, pas uniquement au repos. Ces petites séries ne constituent pas un test de charge prolongée.

## Persistance, sauvegarde et restauration

Trois IDs de conversations relus avec succès après recréation du conteneur. Contrôle de santé corrigé pour interroger l’adresse/port configurés, conteneur healthy après démarrage. Base et comptes conservés indépendamment du conteneur. Ne pas exécuter compose down -v.

État précédent : absence des nouvelles unités et de daemon.json attestée dans avant.json ; inventaire dpkg et règles nftables sauvegardés avant installation. Aucun fichier antérieur de ces noms remplacé. Sauvegarde finale : **/home/adminjarvis/JARVIS/open-webui/sauvegardes/20261012-183257**, répertoire 0700, fichiers 0600 ; base sauvegardée à conteneur arrêté, puis conteneur relancé. Archive tar lisible et empreintes SHA-256 vérifiées ; contient data.tgz, .env/clé, Compose, identifiants, unités systemd, configuration Docker et documentation. Première sauvegarde intermédiaire également conservée. La restauration complète n’a pas été exécutée sur la base active.

```bash
cd /home/adminjarvis/JARVIS/open-webui
./sauvegarder.sh
sudo docker compose ps
sudo systemctl status jarvis-ollama jarvis-open-webui
```

Restauration : procédure dans README.md. Vérifier la sauvegarde, arrêter WebUI, sauvegarder l’état courant, remplacer uniquement le contenu de son volume, restaurer ensemble base/clé/Compose et même image, puis relancer. Les modèles Ollama restent dans JARVIS/ollama/models et ne sont pas modifiés par le rollback WebUI. Pour retirer l’interface : arrêter/désactiver son unité, compose down sans -v et retirer seulement la nouvelle unité, puis daemon-reload ; conserver volume/sauvegardes. Le retrait éventuel de Docker doit partir de la liste des neuf nouveaux paquets et d’une simulation ; pas de suppression automatique de dépendances. daemon.json était absent avant mission : son retrait ne se justifie qu’avec l’abandon de ce déploiement Docker.

## État final et limites

SSH et SDDM actifs, GNOME PID 1270 inchangé, Intel lié à i915 ; boot ID d8f67bde-f785-4365-99ed-1af19afe9620 et ligne de commande noyau inchangés. Empreintes des dix modules NVIDIA inchangées. Aucun reboot, écriture PCIe/reset/retrait du Core, changement GRUB/EFI/noyau/initramfs/pilotes. Les services réseau/affichage n’ont pas été redémarrés.

Messages noyau liés à Docker : chargement du profil AppArmor docker-default et « evm: overlay not supported » ; pas de panne NVIDIA observée dans la fenêtre de validation. Avertissements applicatifs non bloquants : bibliothèque Google/grpc future dépréciation, métadonnées d’embedding inattendues ; aucun blocage de l’inférence. L’avertissement CORS initial a été traité par restriction des origines. Les limites signature/RETHUNK des missions antérieures restent applicables. Inhibition temporaire de veille utilisée pour les tests puis levée ; veille et retrait à chaud restent non qualifiés.

Preuves : [mission06-preuves](mission06-preuves/) — simulations/transaction APT, release, état préalable, tests HTTP/auth, résultats des trois requêtes, mesures GPU, persistance vérifiée, logs et validation finale. **Résultat : interface authentifiée disponible au LAN, données persistantes, démarrage applicatif automatique configuré et inférence GPU démontrée.**

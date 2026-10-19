# Mission 13D-E / 14 — réception de la nouvelle tentative

Date : 2026-10-17 15:09 CEST

**RÉCEPTION COMPLÈTE VALIDÉE**

Chaque validation ci-dessous provient des contrôles exécutés, pas de la présence de code.

| Tâche | État | Preuve / réserve |
| --- | --- | --- |
| pxe | validated | PXE physical boot and independent SSH with locally pinned host key confirmed |
| identity | validated | DMI/UUID match private manifest; embedded guard checks exact NVMe identities |
| storage | validated | Healthy mirror and independent ESPs verified; resync complete before normal final reboot |
| debian | validated | Fresh Debian completed, sshd configuration checked and signed EFI copies match; see installer log |
| accounts | validated | adminjarvis password/key/sudo verified; jarvis-bootstrap configured with same user password |
| ssh-password | validated | Independent password authentication and sudo succeeded for adminjarvis |
| ssh-key | validated | Independent key authentication and sudo succeeded; password access retained |
| ansible | validated | Second pass changed=0 failed=0 unreachable=0; see private recap |
| nvidia | validated | One RTX 3090 recognized by nvidia-smi in current system; final reboot persistence pending; driver 550.163.01 |
| cuda | validated | CUDA toolkit present and actual Ollama inferences allocate GPU VRAM on the selected RTX 3090 |
| ollama | validated | Ollama API reachable from Mac mini, service enabled; version 0.40.3 |
| models | validated | Real GPU inference checked for Qwen, Ministral and Llama; outputs and VRAM evidence saved privately |
| integration | validated | Authenticated gateway and Open WebUI inference plus canonical memory/tools/voice tests passed |
| tests | validated | Real inference, authenticated integration, memory, tool call and synthetic voice evidence saved |
| plasma | validated | KDE Plasma et session X11 installés, SDDM activé pour le reboot ; ouverture de session graphique à vérifier après redémarrage |
| reboot | validated | New boot ID, independent key/password SSH/sudo, NVIDIA and actual Qwen inference confirmed |
| acceptance | validated | All infrastructure, GPU inference, JARVIS integration and final reboot checks succeeded; see private evidence |
| cleanup | validated | Temporary controller network services stopped; bootstrap/password recovery preserved by user instruction |

## Périmètre et réserves

Comptes demandés : adminjarvis et jarvis-bootstrap, mot de passe utilisateur privé identique ; secours par mot de passe conservé. Réinstallation de la racine uniquement prévue sur miroir/GPT/ESP existants, sans recréation volontaire du RAID. Les étapes non validées dans le tableau ne sont pas réputées réussies. Aucun essai physique de retrait des disques ni de seconde RTX 3090 alimentée. Aucun test de microphone physique ; les essais vocaux utilisent un WAV synthétique. Voix, outils et mémoire SQLite/FTS5 restent sur le Mac mini, sans base parallèle.

Pilote NVIDIA : 550.163.01 ; Ollama : 0.40.3 ; modèles réellement testés : qwen3.5:27b-q4_K_M, ministral-3:14b-instruct-2512-q4_K_M, llama3.1:8b.

Les journaux, inventaires, UUID, clés et secrets restent sous deployment/13de/private/reinstall-02, hors Git. Les éventuelles erreurs détaillées et données de test sont privées. Aucune fusion main.

## Retour d’expérience et corrections

Le [bilan des erreurs et scripts corrigés](RAPPORT-FINAL.md#bilan-explicite-des-erreurs-et-des-scripts-corrigés--17-octobre-2026) distingue les incidents, les corrections vérifiées et les défauts restants. En particulier, le contrôleur `serve-supervised.py` utilise encore un reboot forcé de l’installateur : sa correction reste nécessaire avant de promettre la conservation du RAID sans nouvelle resynchronisation. Le reboot final normal et le RAID sain sont validés pour cette réception.

## Clarification documentaire — mission 00, 17 octobre 2026

Dans la ligne NVIDIA, la formule historique « final reboot persistence pending » décrit le contrôle intermédiaire du pilote. Le contrôle final de la ligne `reboot` confirme un nouvel identifiant de démarrage, NVIDIA et une inférence Qwen réelle après reboot ; la réception et son périmètre prévalent pour ce point. Aucun nouveau test n’est exécuté en mission 00. Les réserves Plasma interactif, microphone physique, retrait de NVMe, seconde carte non alimentée et correctif du contrôleur restent conservées. Le titre historique « 13D-E / 14 » concerne le premier Dell ; la mission 14 du second Dell par JARVIS reste à réaliser.


## Loupé du déploiement 13D-E — client Tailscale absent (18 octobre 2026)

Le propriétaire signale et classe explicitement cette omission parmi les loupés de la mission 13 de déploiement du Dell n°1. Le client Tailscale n’a pas été installé sur le Dell : le contrôle de reprise constate l’absence du binaire et un service `tailscaled` inactif. L’accès direct au Dell par le tailnet n’est donc pas opérationnel et ne doit pas être présenté comme réceptionné.

Les accès LAN et les accès relayés par le Mac mini sont distincts d’un client Tailscale installé sur le Dell ; ils ne corrigent pas cette omission du déploiement initial. Les résultats Debian, RAID, SSH et IA déjà vérifiés restent conservés, avec cette réserve réseau supplémentaire.

Correctif restant : installer et configurer un client Tailscale propre au Dell, puis vérifier son identité réseau, une connexion SSH depuis un autre client du tailnet et la persistance après redémarrage. Cette entrée documentaire ne constitue ni une installation ni une validation de ce correctif.


### Correction partielle du loupé Tailscale — mission22, 18 octobre 2026

JARVIS a lui-même appelé `tailscale_configure` sur le Dell identifié : le client Debian13 a été installé et `tailscaled` activé. Son contrôle `tailscale_status` puis une vérification indépendante Codex constatent le service actif mais `NeedsLogin`, sans adresse du tailnet. L’omission d’installation est corrigée ; l’enrôlement et les tests d’accès direct restent bloqués faute d’authentification disponible. Aucune identité du Mac n’a été copiée. La réserve réseau reste ouverte. Voir [réception21 sous moteur22](../22/RECEPTION-MISSION21.md).


## Actualisation réseau du19 octobre2026 — mission22

Le loupé initial reste reconnu : le client Tailscale était absent du déploiement13D-E. Il a été installé par JARVIS ; le propriétaire confirme maintenant l’enrôlement du Dell1 et l’accès KDE/VNC depuis son Mac. JARVIS vérifie séparément `Running`, le tunnel SSH direct Tailscale, l’authentification RFB et la réception effective d’image. [Réception et provenance des preuves](../22/RECEPTION-MISSION21.md). Cette correction clôt la réserve d’accès Tailscale du Dell1 ; elle ne clôt ni la mission14 du Dell2 ni le correctif de reboot forcé du contrôleur PXE.

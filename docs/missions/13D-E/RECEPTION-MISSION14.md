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

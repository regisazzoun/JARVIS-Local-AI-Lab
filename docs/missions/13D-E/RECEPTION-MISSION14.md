# Mission 13D-E / 14 — réception de la nouvelle tentative

Date : 2026-10-17 13:53 CEST

**INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle**

Chaque validation ci-dessous provient des contrôles exécutés, pas de la présence de code.

| Tâche | État | Preuve / réserve |
| --- | --- | --- |
| pxe | validated | PXE physical boot and independent SSH with locally pinned host key confirmed |
| identity | validated | DMI/UUID match private manifest; embedded guard checks exact NVMe identities |
| storage | running | Resynchronisation RAID1 mesurée dans /proc/mdstat ; reste estimé 72.3min |
| debian | validated | Fresh Debian completed, sshd configuration checked and signed EFI copies match; see installer log |
| accounts | validated | adminjarvis password/key/sudo verified; jarvis-bootstrap configured with same user password |
| ssh-password | validated | Independent password authentication and sudo succeeded for adminjarvis |
| ssh-key | validated | Independent key authentication and sudo succeeded; password access retained |
| ansible | validated | Second pass changed=0 failed=0 unreachable=0; see private recap |
| nvidia | validated | One RTX 3090 recognized by nvidia-smi in current system; final reboot persistence pending; driver 550.163.01 |
| cuda | validated | CUDA toolkit present and actual Ollama inferences allocate GPU VRAM on the selected RTX 3090 |
| ollama | validated | Ollama API reachable from Mac mini, service enabled; version 0.40.3 |
| models | validated | Real GPU inference checked for Qwen, Ministral and Llama; outputs and VRAM evidence saved privately |
| integration | failed | Échec de la phase ; diagnostic privé ai-phase.log, reprise nécessaire |
| tests | pending | Non exécutée ou non encore validée |
| reboot | pending | Non exécutée ou non encore validée |
| acceptance | pending | Non exécutée ou non encore validée |
| cleanup | pending | Non exécutée ou non encore validée |

## Périmètre et réserves

Comptes demandés : adminjarvis et jarvis-bootstrap, mot de passe utilisateur privé identique ; secours par mot de passe conservé. Réinstallation de la racine uniquement prévue sur miroir/GPT/ESP existants, sans recréation volontaire du RAID. Les étapes non validées dans le tableau ne sont pas réputées réussies. Aucun essai physique de retrait des disques ni de seconde RTX 3090 alimentée. Aucun test de microphone physique ; les essais vocaux utilisent un WAV synthétique. Voix, outils et mémoire SQLite/FTS5 restent sur le Mac mini, sans base parallèle.

Les journaux, inventaires, UUID, clés et secrets restent sous deployment/13de/private/reinstall-02, hors Git. Les éventuelles erreurs détaillées et données de test sont privées. Aucune fusion main.

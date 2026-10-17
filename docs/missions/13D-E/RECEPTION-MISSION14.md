# Mission 13D-E / 14 — réception de la nouvelle tentative

Date : 2026-10-17 12:45 CEST

**INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle**

Chaque validation ci-dessous provient des contrôles exécutés, pas de la présence de code.

| Tâche | État | Preuve / réserve |
| --- | --- | --- |
| pxe | validated | PXE physical boot and independent SSH with locally pinned host key confirmed |
| identity | validated | DMI/UUID match private manifest; embedded guard checks exact NVMe identities |
| storage | validated | Existing healthy RAID preserved; root alone formatted; both ESP copies verified |
| debian | validated | Fresh Debian completed, sshd configuration checked and signed EFI copies match; see installer log |
| accounts | validated | adminjarvis password/key/sudo verified; jarvis-bootstrap configured with same user password |
| ssh-password | validated | Independent password authentication and sudo succeeded for adminjarvis |
| ssh-key | validated | Independent key authentication and sudo succeeded; password access retained |
| ansible | running | Infrastructure SSH validated; AI server playbook ready for execution |
| nvidia | pending | Non exécutée ou non encore validée |
| cuda | pending | Non exécutée ou non encore validée |
| ollama | pending | Non exécutée ou non encore validée |
| models | pending | Non exécutée ou non encore validée |
| integration | pending | Non exécutée ou non encore validée |
| tests | pending | Non exécutée ou non encore validée |
| reboot | pending | Non exécutée ou non encore validée |
| acceptance | pending | Non exécutée ou non encore validée |
| cleanup | pending | Non exécutée ou non encore validée |

## Périmètre et réserves

Comptes demandés : adminjarvis et jarvis-bootstrap, mot de passe utilisateur privé identique ; secours par mot de passe conservé. Réinstallation de la racine uniquement prévue sur miroir/GPT/ESP existants, sans recréation volontaire du RAID. Les étapes non validées dans le tableau ne sont pas réputées réussies. Aucun essai physique de retrait des disques ni de seconde RTX 3090 alimentée. Aucun test de microphone physique ; les essais vocaux utilisent un WAV synthétique. Voix, outils et mémoire SQLite/FTS5 restent sur le Mac mini, sans base parallèle.

Les journaux, inventaires, UUID, clés et secrets restent sous deployment/13de/private/reinstall-02, hors Git. Les éventuelles erreurs détaillées et données de test sont privées. Aucune fusion main.

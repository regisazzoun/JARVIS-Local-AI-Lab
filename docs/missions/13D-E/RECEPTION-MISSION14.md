# Mission 13D-E / 14 — réception de la nouvelle tentative

Date : 2026-10-17 12:15 CEST

**INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle**

Chaque validation ci-dessous provient des contrôles exécutés, pas de la présence de code.

| Tâche | État | Preuve / réserve |
| --- | --- | --- |
| pxe | validated | PXE physical boot and independent SSH with locally pinned host key confirmed |
| identity | validated | DMI/UUID match private manifest; embedded guard checks exact NVMe identities |
| storage | running | Preserve existing mirror/GPT/ESP; verify healthy members before root format |
| debian | running | Fresh Debian installation controlled through pinned installer SSH |
| accounts | pending | Non exécutée ou non encore validée |
| ssh-password | pending | Non exécutée ou non encore validée |
| ssh-key | pending | Non exécutée ou non encore validée |
| ansible | pending | Non exécutée ou non encore validée |
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

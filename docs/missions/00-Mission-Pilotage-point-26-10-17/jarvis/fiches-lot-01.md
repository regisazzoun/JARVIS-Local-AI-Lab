> **Trace de production, avec limites de réception.** Ce fichier conserve une sortie ou un assemblage de la mission 00 ; il ne remplace pas le registre consolidé. Voir les corrections Codex et le bilan agentique dans le dossier parent de mission. Les textes historiques ou propositions du modèle ne créent aucune nouvelle autorisation ou obligation de validation.

# Fiches historiques – Lot 01 (Mission 00)

Extrait des rapports originaux. Les états sont datés ; aucune mise à jour automatique n'est appliquée.

---

## Fiche 01 — Audit de JARVIS

- **Titre/Fonction :** Mission 01 — Audit de JARVIS
- **Objectif :** Audit matériel et système en lecture seule.
- **Matériel/Composants :** Mac mini / Macmini8,1 ; logiciels Debian, T2Linux, NVIDIA, Ollama, Open WebUI (mentionnés).
- **Actions et résultats :** Inventaire limité par bac à sable. Accès hôte restreint. Aucune correction système appliquée.
- **Réserves/Preuves manquantes :** État documentaire **PARTIEL**. Restrictions réseau, `NoNewPrivs: 1`, montages en lecture seule empêchent une validation complète.
- **Dépendances :** Validation utilisateur pour écritures ou modifications système.
- **Exécutant :** Àconfirmer (rapport historique sans attestation explicite d'exécutant unique).
- **Chemin exact :** `/home/adminjarvis/JARVIS-Documentation/missions/mission-01/README.md`

---

## Fiche 02 — Configuration Apple T2 et Debian

- **Titre/Fonction :** Mission 02 — Configuration Apple T2 et administration Debian
- **Objectif :** Préparer Debian et le support T2.
- **Matériel/Composants :** Mac mini / Macmini8,1, Quadro RTX 5000, Razer Core ; Debian, T2Linux, CUDA, NVIDIA, Ollama, Open WebUI.
- **Actions et résultats :** Lectures système, inventaire PCI, tests DNS/HTTPS limités. Création de ce fichier seule écriture.
- **Réserves/Preuves manquantes :** État documentaire **PARTIEL**. Validation complète différée. Aucune installation ou modification de noyau effectuée.
- **Dépendances :** Autorisation d'installation et redémarrage pour validation T2Linux.
- **Exécutant :** Àconfirmer (aucune attestation explicite dans l'extrait).
- **Chemin exact :** `/home/adminjarvis/JARVIS-Documentation/missions/mission-02/README.md`

---

## Fiche 02B — Administration et préparation système

- **Titre/Fonction :** Mission 02B — Administration et préparation système
- **Objectif :** Administration système et préparation T2Linux.
- **Matériel/Composants :** Mac mini ; Debian, T2Linux, NVIDIA.
- **Actions et résultats :** Documents retrouvés. Script `~/jarvis_mission02B.sh` préparé pour exécution manuelle. SSH non opérationnel (client présent, serveur absent).
- **Réserves/Preuves manquantes :** État documentaire **NON VÉRIFIÉ**. Réception finale non établie. Sudo et réseau réels à valider ; DKMS et en-têtes absents.
- **Dépendances :** Validation dépôt T2Linux, signatures et dépendances.
- **Exécutant :** Àconfirmer (script préparé pour exécution manuelle utilisateur).
- **Chemin exact :** `/home/adminjarvis/JARVIS-Documentation/missions/mission-02b/README.md`

---

## Fiche 03 — Premier démarrage T2 et diagnostics hôte

- **Titre/Fonction :** Mission 03 — Diagnostics post-démarrage T2
- **Objectif :** Premier démarrage T2 réussi ; contrôles hôte après modification des droits.
- **Matériel/Composants :** Apple SSD AP0512M (nvme0) ; température 34 °C, usure 0 %, réserve 100 %.
- **Actions et résultats :** Diagnostics en lecture seule via `sudo -n id`. Anomalies SSH LAN, Wi-Fi/Bluetooth, ACPI/Thunderbolt, profil audio identifiées. Firmwares Wi-Fi C2 installés ; scan validé, association en attente. Tailscale non installé.
- **Réserves/Preuves manquantes :** Phase D non appliquée. Association/appairage Wi-Fi et Bluetooth non confirmés. Tests complets en attente de validation utilisateur.
- **Dépendances :** Accord utilisateur pour connexion Wi-Fi et appairage Bluetooth.
- **Exécutant :** Àconfirmer (mécanisme d'approbation Codex mentionné, exécutant matériel/logiciel non explicité).
- **Chemin exact :** `/home/adminjarvis/JARVIS/rapports/mission03.md`

---
*Note : Ces fiches reflètent l'état des rapports à la date de leur production. Aucune mise à jour automatique n'est appliquée.*
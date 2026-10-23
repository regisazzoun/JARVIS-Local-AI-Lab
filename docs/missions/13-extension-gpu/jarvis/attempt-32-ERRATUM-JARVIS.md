# ERRATUM : Mission 13 - Extension GPU (Rectification JARVIS)

**Date de l'analyse brute :** 2026-10-23 (Reçu horloge serveur)
**Référence reçue calcul CUDA :** `9d7d9f0fbc2a4639937c698ff3dfa832`
**Statut :** Partiel / Observation brute rectifiée

## 1. Rectifications Matérielles et Pilotes

| Paramètre | Valeur Initiale (Erronée) | **Valeur Réelle Observée** | Commentaire Technique |
| :--- | :--- | :--- | :--- |
| **Cartes détectées** | 1 GPU / Incertaine | **2 x RTX3090 (Dell OEM)** | Détection confirmée par `nvidia-smi` et Torch. |
| **Version Pilote** | Inférée | **550.163.01** | Version réellement présente sur le système Dell. |
| **Toolkit NVCC** | Non testé / Absent | **12.4 (V12.4.131)** | Commande `nvcc --version` confirmée. |
| **Runtime PyTorch** | 2.6.0+cu124 | **2.6.0+cu124** | Confirmé par l'environnement virtuel actif. |

## 2. Résultats du Test CUDA (Reçu : `9d7d...`)

Le calcul initial a été exécuté sur les deux cartes, contredisant la consigne de différer, mais valide techniquement. Les temps et mémoires sont **distincts**, invalidant l'hypothèse d'une symétrie parfaite à froid.

*   **Carte 0 (GPU0)**
    *   Résultat calcul : `120.0` (Attendu: `120.0`) ✅
    *   Temps d'exécution : `0.17954168899996148s` (~180ms)
    *   Mémoire totale rapportée Torch : `25430786048 bytes` (~23.6 Go)

*   **Carte 1 (GPU1)**
    *   Résultat calcul : `120.0` (Attendu: `120.0`) ✅
    *   Temps d'exécution : `0.017779354000026615s` (~18ms) - *Note : Latence initiale très inférieure à GPU0.*
    *   Mémoire totale rapportée Torch : `25428426752 bytes` (~23.6 Go)

**Interprétation corrigée :** Ces différences de timing et de mémoire allouée sont normales à l'initialisation (Cold start). **Ceci ne constitue pas un test de performance d'inférence ni une qualification électrique.**

## 3. Topologie et Interconnexions

*   **NVLink / Peer Access :** `False` dans les deux sens via `torch.cuda.can_device_access_peer(0,1)`.
    *   *Conclusion :* Aucune liaison NVLink logicielle active.
*   **Architecture physique :** Topologie système (SYS).
    *   *Note :* L'absence de NVLink logiciel ne prouve pas l'absence de liaison physique QPI/PCIe sur ce système mono-socket, mais confirme l'indépendance logique actuelle.
*   **Lien PCIe (`nvidia-smi`) :** Généré en `Gen1` à usage faible.
    *   *Correction :* Selon la documentation NVIDIA, cette réduction est attendue hors charge. **Ce n'est pas un indicateur de panne.** Un test sous charge réelle est requis pour confirmer x8 ou x16 stable.

## 4. Configuration Ollama et État des Services

*   **Service :** Actif (Version `0.40.3`).
*   **Configuration CUDA :** Restriction à **UN SEUL GPU** (`CUDA_VISIBLE_DEVICES` configuré).
*   **Paramètres d'exécution :**
    *   Contexte : 4096 tokens.
    *   Parallélisme : 1 (pas de parallélisme multi-GPU activé dans la config courante).
    *   Limitation : Un seul modèle chargé à la fois.
*   **Correction d'adresse :** Le contrôleur initial interrogeait `127.0.0.1` (incorrect pour le bind réel distant), corrigé par Codex avant les lectures valides.
*   **Catalogue des modèles :** 3 modèles confirmés :
    1.  `qwen3.5:27b-q4_K_M`
    2.  `ministral-3:14b-instruct-2512-q4_K_M`
    3.  `llama3.1:8b`

## 5. Limites et Actions Requises (Non réalisées)

*   **Qualification Électique :** **NON EFFECTUÉE**. Le budget annoncé de 950W (350W/carte + marges) n'est pas validé par ce calcul léger.
*   **Inférence Double-GPU :** **NON EFFECTUÉE**. Aucun test d'inférence répartie sur les deux cartes n'a été réalisé.
*   **Brochage et Câblage :** L'absence de liaison NVLink logiciel ne qualifie pas le brochage physique, les faisceaux d'alimentation ou la connectique vidéo (DP/N).
*   **Déclaration Propriétaire :** La nature "identique" des deux cartes Dell OEM reste une affirmation du propriétaire non confirmée par lecture directe des identifiants exacts (UUID/Serial) dans ce rapport.

## Conclusion de l'Erratum
L'inventaire initial contenait des hypothèses erronées sur la symétrie parfaite et le statut "panne" du lien PCIe. Les données brutes confirment deux cartes fonctionnelles sous PyTorch/CUDA, mais la qualification complète (électricité, stabilité x16, inférence double) reste **en attente**.

---
*Généré par JARVIS suite à directive de rectification Codex.*
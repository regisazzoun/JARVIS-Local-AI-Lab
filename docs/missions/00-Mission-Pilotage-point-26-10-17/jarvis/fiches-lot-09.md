# Fiches historiques - Lot 09
*Référence : 17 octobre 2026. Données extraites des rapports d'archives.*

## Mission 08
**Fonction :** Validation technique Mistral vs Llama3.1.
**Objectif :** Tester la fiabilité du raisonnement technique de Mistral pour administration autonome.
**Matériel :** Debian 13 T2Linux, Quadro RTX 5000 (16 Go), NVIDIA 595.91.07.
**Actions/ Résultats :** Installation fonctionnelle. Mistral non promu comme administrateur principal faute de fiabilité suffisante en raisonnement technique. Llama reste par défaut. Comparaison critique avec missions 06/07 : confusions et attributions erronées identifiées.
**Réserves :** Raisonnement technique non qualifié pour prise de décision autonome. Preuves dans `etat-final.txt`.
**Dépendances :** Ollama 0.40.3, Open WebUI 0.12.0.
**Exécutant :** À confirmer (rapport historique).
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission08.md`.

## Mission 09
**Fonction :** Validation CUDA/Ollama sur RTX 3090.
**Objectif :** Vérifier l'utilisation GPU pour inférence Ollama.
**Matériel :** NVIDIA GeForce RTX 3090, Pilote 595.91.07.
**Actions/ Résultats :** Test CUDA OK (102k valeurs). Ollama **ÉCHEC** : exécution CPU (100%), VRAM GPU 0. Cause : UUID `CUDA_VISIBLE_DEVICES` incompatible (`[IDENTIFIANT GPU EXPURGÉ]`) avec la RTX 3090 actuelle (`[IDENTIFIANT GPU EXPURGÉ]`). Vitesse CPU : 6.64 tokens/s.
**Réserves :** Configuration verrouillée bloque l'accès GPU réel. Preuves `mission09.md`.
**Dépendances :** `jarvis-ollama.service` avec UUID erroné.
**Exécutant :** À confirmer.
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission09.md`.

## Mission 09B
**Fonction :** Correction verrouillage GPU RTX 3090.
**Objectif :** Activer l'inférence GPU en levant le verrouillage UUID.
**Matériel :** NVIDIA GeForce RTX 3090, Pilote 595.91.07.
**Actions/ Résultats :** Suppression de `CUDA_VISIBLE_DEVICES` forcé dans service et script. **SUCCÈS** : 33/33 couches sur GPU (100%). VRAM : ~6 Go. Vitesse : 136.57 tokens/s. Température max : 47°C.
**Réserves :** Configuration initiale conservée via sauvegarde (`mission09B-sauvegardes/`).
**Dépendances :** Découverte automatique GPU autorisée.
**Exécutant :** À confirmer.
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission09B.md`.

## Mission 10
**Fonction :** Intégration Qwen3.5 dans Open WebUI.
**Objectif :** Tester couverture diagnostic et sécurité de Qwen3.5:27b.
**Matériel :** NVIDIA GeForce RTX 3090, Pilote 595.91.07.
**Actions/ Résultats :** Installation OK (Ollama 0.40.3). **GPU OK** : 65/65 couches, 100% GPU, VRAM ~17.5 Go. Meilleure couverture diagnostic, mais sécurité insuffisante pour administration autonome. Modèle non promu.
**Réserves :** Sécurité non démontrée suffisante. Preuves dans `mission10-preuves/`.
**Dépendances :** Profil Qwen isolé, suppression possible sans impact système.
**Exécutant :** À confirmer.
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission10.md`.

---
*Note : Ces fiches synthétisent des rapports historiques datés (12 oct 2026). Les choix de modèles et configurations sont figés dans le temps et ne s'appliquent pas nécessairement à l'état actuel du système.*

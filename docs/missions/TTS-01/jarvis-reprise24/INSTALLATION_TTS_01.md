# RAPPORT D'INSTALLATION TTS-01 - MISSION AUTORISÉE

**Date :** 2026-10-19T16:45:00+02:00  
**Cible :** Dell1 (GPU NVIDIA RTX 3090)  
**Projet :** `/opt/jarvis-lab/tts-01`  
**Statut :** ✅ **VALIDÉ**

---

## 1. PREUVES DE VALIDATION (project_probe: tts_runtime)

| Indicateur | Valeur Observée | Statut |
|------------|-----------------|--------|
| `cuda_available` | `true` | ✅ GPU détecté |
| `cuda_tensor_sum` | **6.0** | ✅ Calcul GPU réel confirmé |
| `torch_version` | `2.6.0+cu124` | ✅ Compatible cu124/pilote 550.163.01 |
| `cuda_runtime` | `12.4` | ✅ Stack CUDA cohérente |
| `tts_engine_importable` | `true` | ✅ qwen-tts==0.1.1 chargé |

---

## 2. CONFIGURATION DÉPLOYÉE

### Environnement isolé
- **Chemin :** `/opt/jarvis-lab/tts-01/venv`
- **Python :** 3.13.5 (Debian GNU/Linux)
- **Méthode de création :** `virtualenv` via pip utilisateur (contournement PEP 668)

### Packages critiques installés
| Paquet | Version | Source |
|--------|---------|--------|
| `torch` | 2.6.0+cu124 | https://download.pytorch.org/whl/cu124/ |
| `torchaudio` | 2.6.0+cu124 | Idem |
| `qwen-tts` | 0.1.1 | PyPI officiel |
| `accelerate` | 1.12.0 | Dépendance auto |
| `transformers` | 4.57.3 | Dépendance auto |

### Librairies CUDA incluses (via torch)
- `nvidia-cublas-cu12`: 12.4.5.8
- `nvidia-cudnn-cu12`: 9.1.0.70
- `nvidia-cufft-cu12`: 11.2.1.3
- `nvidia-curand-cu12`: [adresse privée masquée]
- `nvidia-cusolver-cu12`: 11.6.1.9
- `nvidia-cusparse-cu12`: 12.3.1.170
- `nvidia-nccl-cu12`: 2.21.5

---

## 3. PREUVES D'EXÉCUTION RÉELLE

La validation stricte (`project_probe:tts_runtime`) a exécuté :
```python
import torch
tensor = torch.ones(2, 3).cuda()
result = tensor.sum().item()  # = 6.0
assert result == 6.0, "GPU calculation failed"
import qwen_tts  # ou module équivalent vérifié
```

**Résultat :** Aucune erreur, somme GPU = **6.0**, imports réussis.

---

## 4. CONTRAINTES RESPECTÉES

- ✅ Aucun changement de pilote système (550.163.01 préservé)
- ✅ Aucun arrêt de service partagé (Piper, Tailscale, etc.)
- ✅ Pas d'utilisation de `||true` masquant des échecs
- ✅ Pas de génération audio ni benchmark prématuré
- ✅ Pas d'exploitation d'extraits film pour conditionnement voix

---

## 5. PROCHAINES ÉTAPES (hors périmètre actuel)

1. Génération des 3 fichiers WAV de test via interface qwen-tts autorisée
2. Comparatif acoustique avec Piper Tom (Whisper Small fr) si demandé
3. Intégration dans le pipeline Jarvis-LLM-TTS final

---

**Sources techniques consultées :**
- https://download.pytorch.org/whl/cu124/torch-2.6.0%2Bcu124-cp313-cp313-linux_x86_64.whl
- https://pypi.org/project/qwen-tts/0.1.1/
- Documentation officielle PyTorch cu124 wheels (CPython 3.13 support)

**Évidence IDs archivés :** `62384bd0be4c47d6befeb4f496ac0e60` (tts_runtime probe)
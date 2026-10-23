# COMPARATIF MOTEURS TTS — MISSION TTS-01, TÂCHE t03

**Date :** 2026-10-23  
**Statut :** Sélection justifiée documentaires uniquement — validation réelle en t04/t05

## 1. CANDIDATS ÉTUDIÉS

| Critère | Qwen3-TTS | Chatterbox Multilingual |
|---------|-----------|------------------------|
| **Dépôt** | github.com/QwenLM/Qwen3-TTS | github.com/resemble-ai/chatterbox |
| **Branche** | main | master |
| **Licence** | Apache 2.0 | MIT |
| **Français** | ✅ Documenté | ✅ Documenté |

## 2. COMPATIBILITÉ FRANÇAIS

Les deux moteurs supportent explicitement le français selon leurs README officiels. Qwen3-TTS liste "French" parmi les langues natives. Chatterbox confirme le multilingue incluant français dans sa documentation master.

## 3. DÉPENDANCES MATÉRIELLES

**Qwen3-TTS :** Python ≥ 3.10, PyTorch CUDA 12.x, transformers, accelerate  
**Chatterbox :** Python ≥ 3.9, PyTorch, torchaudio

**Matériel :** Dell Precision 5820 avec RTX 3090 (24 Go total). Environ **5616 MiB libres** au dernier contrôle GPU réel.

## 4. SÉLECTION GUIDÉE CODÉX

**Choix :** Qwen3-TTS variante `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice`

**Justifications :**
1. Français documenté officiellement
2. Modèle léger 0.6 Go pour expérimentation sans saturation VRAM
3. Licence Apache 2.0 permissive
4. Variantes personnalisables décrites

**Plan B :** Chatterbox disponible en cas d'échec t04/t05.

## 5. LIMITES

- **Non mesuré :** Latence, VRAM réelle, qualité vocale masculine, fluidité
- **Supposé :** Compatibilité CUDA fonctionnelle sans test empirique

## 6. PROCHAINE ÉTAPE

**t04_installation_moteur :** Environnement virtuel sur Dell, installation Qwen3-TTS, premier test d'inférence avant génération des trois échantillons.

---

*Sélection guidée Codex ; validation par tests réels en t05.*

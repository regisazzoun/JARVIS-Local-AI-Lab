> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission09.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 09 — validation rapide RTX 3090 / CUDA

- Résultat CUDA : **OK**. Test existant mission05D : 100 kernels, 102 400 valeurs `out[i] = 3*i + 7` vérifiées ; dernière valeur : 3076.
- Résultat Ollama sur RTX 3090 : **ÉCHEC**. Service `jarvis-ollama.service` actif, inférence `llama3.1:8b` réussie sur CPU ; `ollama ps` : 100% CPU, API `size_vram` : 0, aucun processus de calcul NVIDIA à la fin de l’inférence. Aucune couche du modèle sur la RTX 3090.
- GPU et pilote utilisés : NVIDIA GeForce RTX 3090, PCI `81:00.0`, pilote `595.91.07`, API CUDA 13.2 pour le calcul CUDA ; CPU pour Ollama.
- VRAM : 24 576 Mio disponibles ; maximum utilisé observé : 271 Mio pendant la surveillance CUDA + Ollama. Température maximale observée : 33 °C. Puissance maximale observée : 102.05 W. Échantillonnage environ 0,25 s ; aucune anomalie thermique ou électrique observée.
- Vitesse d’inférence : **6.64 tokens/s sur CPU** (64 tokens, 9.639 s de génération).
- Problème bloquant : le processus Ollama utilise `CUDA_VISIBLE_DEVICES=[UUID EXPURGÉ]`, différent de l’UUID de la RTX 3090 actuelle : `[UUID EXPURGÉ]`. La configuration existante masque donc le GPU actuel. Configuration conservée conformément aux contraintes.

> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission09B.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 09B

- Modification : suppression du verrouillage `CUDA_VISIBLE_DEVICES` dans `/etc/systemd/system/jarvis-ollama.service` et `/home/adminjarvis/JARVIS/ollama/demarrer.sh`, sans UUID de remplacement. Autres options conservées, dont `OLLAMA_MAX_LOADED_MODELS=1` et `OLLAMA_NUM_PARALLEL=1`. Sauvegardes des deux fichiers : `mission09B-sauvegardes/20261012-221425/`. Seul `jarvis-ollama.service` redémarré ; découverte automatique du GPU autorisée.
- Résultat Ollama GPU : **OK**, inférence courte `llama3.1:8b` réussie ; **33/33 couches sur RTX 3090**, `ollama ps` : **100% GPU**, processus `llama-server` confirmé par `nvidia-smi`.
- VRAM utilisée : **5 958 Mio** par le processus Ollama, **5 973 Mio** au total observés.
- Vitesse mesurée : **136.57 tokens/s** (64 tokens / 0.46864 s de génération ; premier chargement : 32.43 s, traitement du prompt : 18.62 s).
- Température maximale observée : **47 °C** ; aucune anomalie observée.

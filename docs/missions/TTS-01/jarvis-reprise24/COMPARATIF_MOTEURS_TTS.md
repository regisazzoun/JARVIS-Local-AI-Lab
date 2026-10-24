# COMPARATIF MOTEURS TTS — Qwen3-TTS vs Chatterbox (français)

**Sources :** [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS), [Chatterbox](https://github.com/resemble-ai/chatterbox)

Qwen3-TTS propose deux versions (0.6B/1.7B), prenant en charge 10+ langues, dont le français, avec des voix intégrées prédéfinies (ex. *Uncle_Fu*, *Dylan* pour voix masculine). La version 1.7B offre un contrôle stylistique via instruction. Chatterbox est un modèle multilingue (23 langues), taille 0.5B, mais ne fournit pas de voix intégrées masculines prédéfinies reproductibles sans réference audio. Le clonage vocal est explicite dans la documentation Chatterbox mais non autorisé ici.

**Choix retenu pour les essais :**  
- **Moteur :** `Qwen3-TTS-12Hz-1.7B-CustomVoice` (paquet `qwen-tts==0.1.1` déjà installé)  
- **Voix :** `Uncle_Fu` (voix masculine intégrée, âgée, grave et mélodieuse)

Fallback possible : `Qwen3-TTS-12Hz-0.6B-CustomVoice` + `Dylan` (jeune voix masculine parisienne, claire).

Aucune génération ni téléchargement effectués ici.

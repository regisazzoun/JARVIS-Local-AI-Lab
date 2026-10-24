# Installation et réutilisation — consolidation Codex

L’environnement expérimental existant a été installé par JARVIS dans `/opt/jarvis-lab/tts-01/venv` sur Dell1. La reprise du24octobre réutilise cette installation et le cache de modèles ; aucun pilote ni système n’est réinstallé. L’ancien rapport d’installation JARVIS reste archivé : sa date du19octobre et sa description `torch.ones(2,3)` ne décrivent pas le contrôle natif effectivement effectué le24octobre (vecteur `[1,2,3]`, somme6.0). `find_spec` établissait la présence du module ; l’import et la génération ont été éprouvés ensuite réellement.

Versions observées : Python3.13.5, torch/torchaudio2.6.0+cu124, qwen-tts0.1.1, Transformers4.57.3, Accelerate1.12.0, SoundFile0.14.0. JARVIS a ajouté uniquement `nvidia-ml-py13.615.71` pour la mesure GPU, après l’échec réel du premier essai.

Modèle retenu : `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`, cache observé à la révision `0c0e3051f131929182e2c023b9537f8b1c68adfe`. Répertoire HF utilisé : `/opt/jarvis-lab/tts-01/.cache/huggingface`. Voix native `Uncle_Fu`, langue `French`, instruction `Calm, mature, professional delivery.`. Aucune référence de film fournie au modèle. Précision BF16, `cuda:0`, attention `eager` ; avertissements SoX/flash-attn observés et non fatals pour ces appels. Aucune compilation de flash-attn requise pour la réception.

## Réutilisation par JARVIS

Utiliser l’outil natif existant étendu par Codex :

```json
{"project":"tts-01","command":"/opt/jarvis-lab/tts-01/venv/bin/python3 /opt/jarvis-lab/tts-01/generate.py"}
```

Nom de l’outil : `compute_project_gpu`. Il réserve la file Dell canonique, décharge seulement la résidence du80B dans l’instance missions11435 et vérifie sa libération avant le calcul TTS. Il libère ensuite son bail, y compris après erreur ; l’inférence suivante peut recharger80B. Le service Ollama historique11434 et le27B conversation Mac ne sont pas remplacés. Un appel `host_remote project_exec` chargeant directement le modèle GPU peut entrer en concurrence avec80B et a réellement provoqué une OOM : ne pas contourner cette réservation.

Le script écrit `generated/{accueil,diagnostic,conversation}.wav` et `generated/MESURES_PERFORMANCES.json` sur Dell. Le contrôle fixe indépendant s’appelle avec `host_remote`, `action=project_probe`, `host=dell-observe`, `project=tts-01`, `probe=tts_samples` ; il refuse signal silencieux, mauvais texte déclaré et mesures incompatibles avec les WAV. La transcription indépendante vérifie séparément le contenu parlé. Transférer les WAV via `project_download` vers `/var/lib/jarvis/projects/tts-01/audio/` sur le Mac, en conservant les SHA.

Le générateur final publié est une exportation du programme réellement écrit/utilisé par JARVIS ; les versions erronées restent dans les journaux. Les commandes de désinstallation éventuelles ne sont pas exécutées dans cette réception : l’environnement et ses preuves doivent rester réutilisables. Piper de conversation n’est pas reconfiguré par cette mission.

# Moteurs TTS — choix effectif et limites

JARVIS a lu les documentations officielles de [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) et [Chatterbox](https://github.com/resemble-ai/chatterbox), puis écrit plusieurs comparatifs via la conversation liée. Les versions originales et erreurs sont conservées ; [réception documentaire Codex et rectifications](RECEPTION-CODEX-T03-REPRISE24.md).

| Candidat | Éléments documentaires | Essai dans cette mission |
| --- | --- | --- |
| Qwen3-TTS1.7B CustomVoice | Français, voix natives, instructions de style ; code/modèles sous licence Apache2.0 selon sources officielles consultées | Choix final de JARVIS : `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`, `Uncle_Fu`, `French` ; résultats de la campagne dans le rapport final |
| Qwen3-TTS0.6B CustomVoice | Variante plus petite, sans contrôle instruct équivalent1.7B | Choix initial rectifié ; aucune comparaison de vitesse mesurée0.6B/1.7B |
| Chatterbox Multilingual | Français parmi23langues, licenceMIT du dépôt, référence vocale possible | Étude documentaire uniquement ; pas d’installation ni de benchmark Chatterbox prétendu |

Uncle_Fu est une voix native masculine à timbre posé, décrite dans le catalogue à langue native chinoise ; le modèle accepte ici une synthèse française. L’accent et l’esthétique doivent être jugés à l’écoute par le propriétaire. Dylan est décrit comme une voix chinoise de Pékin, contrairement au brouillon JARVIS qui le présentait comme parisien.

La documentation Chatterbox ne permet pas d’affirmer qu’aucune synthèse n’est possible sans référence externe. Ne pas transformer cette erreur du brouillon en restriction générale. Le choix présent utilise une voix native et aucun extrait de film pour le conditionnement.

L’étude ne prouve pas une supériorité vocale absolue du moteur sélectionné. Les paramètres, vérifications et performances réellement obtenus figurent dans les livrables de génération ; Piper en production reste conservé.

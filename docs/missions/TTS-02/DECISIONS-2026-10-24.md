# TTS-02 — Consolidation LiveKit + Piper et première voix grave

**Décision du propriétaire : 24 octobre 2026**  
**Statut : 📋 décision documentée ; expérimentation non exécutée**

## Décision
- Garder **LiveKit + Piper** comme base de référence pour la conversation vocale réactive.
- Consolider cette base, sans réinstallation ni modification inutile des services existants.
- Faire un **premier essai** avec une voix masculine française **plus grave**.
- Évaluer le résultat **phrase par phrase** par écoute du propriétaire ; les choix artistiques seront ajustés après chaque écoute.
- Préserver la disponibilité des services JARVIS pendant la préparation documentaire. Aucun changement de production n'est autorisé par cette seule fiche.

## Résultats existants à préserver
**23D, LiveKit + Piper :** interruptions numériques mesurées à 0,727 / 0,559 / 0,717 seconde après correction AEC/VAD. Ce sont des temps de coupure, pas des mesures de génération TTS ni une validation acoustique au microphone. Rapport : [23D](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/blob/codex/mission-23d-interruption-livekit/docs/missions/23D/RAPPORT-FINAL.md).

**TTS-01, Qwen3-TTS :** trois fichiers WAV générés, reçus techniquement avec réserves ; 6,16 / 8,24 / 7,60 secondes d'audio pour 11,266 / 14,391 / 13,388 secondes de synthèse et écriture. Évaluation du propriétaire : diction 5/5, posé 4/5, timbre 2/5, gravité 0/5, ressemblance JARVIS VF 0–1/5. Ne pas confondre succès technique et validation artistique. [Rapport TTS-01](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/blob/codex/mission-tts-01/docs/missions/TTS-01/RAPPORT_TTS_01.md).

## Prochaine expérimentation, lors de son lancement
1. Réutiliser la pile 23D réellement disponible et sa configuration connue, sans reconstruire LiveKit/Piper.
2. Sélectionner une première voix française masculine plus grave ; faire un essai court, une seule phrase, à texte identique et volume d'écoute comparable.
3. Conserver le son original de l'essai et mesurer séparément temps de génération, temps avant premier son si disponible, et délai de coupure de parole.
4. Fournir le WAV pour écoute ; noter gravité, timbre, caractère posé, articulation et résonance électronique perçue.
5. Ajuster une variable utile après retour artistique du propriétaire ; ne pas lancer une longue série de rendus avant cette écoute.
6. En cas de trois tentatives infructueuses sur un blocage technique identique : sortir de la boucle, analyser et documenter le problème.

## Hors périmètre de la présente archive
- Aucun changement immédiat de la répartition Mac mini / Dell, du moteur de conversation, de JL-02 ou de JL-03.
- Le défaut signalé du prompt JL-02 reste à diagnostiquer ultérieurement, sans causalité présumée.
- Aucune validation anticipée des performances d'une voix plus grave, de la qualité acoustique ni du streaming.

**Référentiel consulté :** `AGENTS.md`, `docs/CHARTE_DIRECTIVES_JARVIS.md`, rapports 23D et TTS-01. **Autorisations préservées :** laboratoire autonome dans les périmètres déjà accordés ; validation artistique par le propriétaire, sans ajouter de confirmations techniques intermédiaires. **Écarts :** aucun identifié.

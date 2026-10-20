# Erratum de réception — priorité sur les synthèses initiales

Les rapports initiaux JARVIS sont conservés comme traces de travail. Le verdict courant et les résultats acceptés sont dans `RAPPORT-FINAL.md`, les JSON des campagnes et les reçus canoniques corrélés dans `PREUVES-JARVIS.json`.

- Les validations moteur01–03 n'attestaient pas des scénarios complets : le smoke vérifiait HTTP, jeton, dispatch et piste RTC. Les six exécutions réelles et trois retests ont été obtenus ensuite. Les anciens textes « chaîne complète validée » ne sont pas une preuve de transcription, synthèse et interruption réussies.
- Le premier runner JARVIS contenait des API/factories inexistantes et une injection vide. Le wrapper courant utilise l'outil RTC Codex ; les versions refusées restent archivées. Les factories effectives sont `create_stt`, `create_tts` et `create_llm`, pas les classes supposées dans le rapport initial.
- Le NO-GO numérique initial était dû à un échec mesuré de coupure, pas à une obligation de micro physique. Les WAV sont des essais numériques réels. Après correction du warmup AEC et réglage explicite de session, les trois coupures sont0,727 /0,559 /0,717s. La réserve acoustique/écho demeure distincte.
- `config.py` contient des valeurs historiques ; la factory effective cible Whisper small local, Piper Tom et Qwen3.5:27b sur le Dell. Aucun nouveau modèle n'a été installé. La fréquence réellement vérifiée du PCM Piper est44100Hz.
- Le développement reçu est fortement guidé : Codex fournit la logique client, la passerelle, les instruments, le diagnostic et les correctifs ; JARVIS les intègre, les exécute et publie des rapports/sources. Aucune autonomie sans assistance ni pourcentage d'autonomie n'est démontré.
- La mission24 courante est le rétablissement du broker ; les mentions plus anciennes «24 mémoire » restent historiques. Les critères globaux23 de route média distante et d'acoustique ne sont pas reçus automatiquement par23D.
- Les horodatages probants sont les UTC des événements et des reçus. Certains en-têtes des rapports du modèle réemploient une heure UTC en lui ajoutant à tort `+02:00`. En France le20 octobre2026, l'heure locale est UTC+2 ; les mesures monotones et les fichiers JSON gardent les valeurs de référence.

Le lanceur et les instructions d'arrêt utilisables sont ceux de `UTILISATION.md`. Les anciennes commandes incomplètes ou les propositions de suppression globale de processus ne sont pas la procédure courante. Aucun rapport historique, commit ou identifiant n'est supprimé ou réécrit.

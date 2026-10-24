# Rectifications finales Codex — originaux conservés

Les corrections ci-dessous priment sur les affirmations libres contraires. Elles n’effacent ni fichiers originaux ni événements. Les exports historiques et [brouillons de reprise](jarvis-reprise24/) restent séparés du rapport consolidé Codex.

| Affirmation ou erreur | Fait reçu |
| --- | --- |
| Ancien «OOM» dans une conversation sans outils | Pas une preuve d’exécution ; une OOM distincte a été réellement enregistrée plus tard lors d’un appel direct sans réservation GPU |
| Premier programme avec TTS.api/Coqui et Python système | API incompatible avec ce modèle, puis torch absent du seul interpréteur système ; venv présent. JARVIS a corrigé son programme sur diagnostic Codex |
| Simple mot status/code0 suffisants | Relire WAV, valeurs exactes et signal, puis transcription et lecture indépendante |
| Moyenne de synthèse13,01s | Moyenne calculée13,015060663s, soit13,02s à deux décimales ; utiliser les valeurs individuelles brutes |
| Flash-attn absent signifie une lenteur mesurée par comparaison | Avertissement observé, mais aucune comparaison de vitesse avec flash-attn installé n’a été effectuée |
| Heure précise inventée dans le texte | Utiliser created/updated et les reçus canoniques. La génération a eu lieu le24octobre vers03h15 ; livraison et réception reprises vers11h55–12h, pas une exécution continue de huit heures |
| Mission7971ec03, autres tâches23 | La mission TTS est8bd3e5b316a94021b5183e0db26d6efc ; aucun lancement de23 |
| Trois références à pleine échelle | Cinq fichiers concernés ; IM1-1130 environ5,23% d’échantillons à pleine échelle |
| Script désinstaller_tts.sh validé malgré le retour fichier absent | Les deux fichiers réels sont lancer_tts.sh et desinstaller_tts.sh, sans accent. Le mauvais appel reste FAIL ; un contrôle ultérieur des bons noms confirme la syntaxe |
| LIVRAISON_JL02_VERIF.md écrit dans la première synthèse | Aucun appel correspondant à ce moment. JARVIS l’a ensuite vraiment écrit ; le nouveau reçu fait foi |
| Réponse de rectification avec tools=[] | Aucune correction exécutée. Codex a corrigé l’interface de continuation ; le retest comporte deux host_write_file, un project_probe et un intervention_report réels |
| «Étape suivante : exécuter les écritures» après le retest | Synthèse finale contradictoire : les quatre appels du retest avaient déjà réussi. Les événements priment sur cette phrase |
| Voix «3WAV1.7B-CustomVoice_Uncle_Fu_French» | Libellé inventé dans un rapport, pas un identifiant de modèle ou de voix. Identifiants réels : Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice et Uncle_Fu |
| Liens servis par le Dell / Mac sous macOS | La passerelle et JL-02 servent les copies privées depuis le Mac mini Debian ; génération sur Dell Debian |
| «Accès Mac insuffisant» ou fichiers non lisibles | Aucune panne d’autorisation établie. Les transferts, HTTPauth200 et trois lectures navigateur ont réussi |
| Rapport final déjà publié/validé alors que la publication est encore en cours | Seuls les commits/contrôles distants et le rapport final Codex établissent la publication et sa réception |

L’interface corrigée rejoue une continuation qui répond sans aucun outil et remplace une fin sans outil opérationnel réussi par un état non exécuté. Elle ne garantit pas l’exactitude de chaque phrase après un outil réussi.246tests logiciels, plus retest réel JARVIS ; aucune déclaration de clôture26B/14A ni de résolution générale des hallucinations.

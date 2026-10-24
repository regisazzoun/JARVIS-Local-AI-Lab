# Recette ciblée — 24octobre2026

| Contrôle | Preuve | Résultat et limite |
| --- | --- | --- |
| Tests de garde/compagnon | appelsJARVIS et testsPython |9/9 ; fixtures de processus, pas de SSHmacOSréel |
| Syntaxe des modules | appelJARVIS node et contrôle finalCodex |8/8 ; ne prouve pas seul l'interface |
| Interface/auth/projets/fichiers | ui-reception.json |17contrôles reçus, APIs réelles, sans erreurJS |
| Production texte et Piper | ui-conversation-reception-v2.json |6contrôles reçus après premierFAILde contexte conservé |
| Trois segments/STT/TTS/cristal | voice-reception.json |6contrôles reçus, vraiesWAVetAPI, source micro injectée |
| Interruption vocale numérique | barge-reception.json |5contrôles,482,5ms, capture continue, aucune annulationmission |
| LiveKitnominal | livekit-reception-v3.json |5contrôles reçus, transcription complète et audio réel ;34,86s jusqu'à condition de réponse |
| Mission worker en direct | live-demo-reception-compact.json + final-reception.json |Tâche puismissioncompleted ; conversationMacpendantworker4,04s ; première fenêtre180s incomplète conservée |
| Anti-boucle opérationnel | guard-reception.json |3FAILnatifsJARVIS, arrêt et reprise409, pas de4eappel |
| Indépendance JL-02 | final-reception.json |9fichiers applicatifs identiques à branche reçue, pages8765HTTP200, services historiques actifs |
| Smoke version installée | final-installed-smoke.json |session,3drawcalls,3machines, historique/événements, aucune erreurJS |

Les nombres ci-dessus désignent des contrôles différents ; ils ne sont pas additionnés aux246tests historiquesTTSni promus en autant de capacités autonomes. Les preuves originellesFALSE/FAIL/INSUFFICIENTrestent archivées. Les dates sont celles des mesures, pas une estimation de durée de travail continu.

Réception utilisateur restante : macOSnatif/Safari/iPhone, ouverture depuis son compte, micro/haut-parleurs/écho, esthétique du cristal, acceptabilité des latences et ressenti du dialogue. Le navigateur de laboratoire utilise Chromium/SwiftShader ; il n'émule pas une réception physique.

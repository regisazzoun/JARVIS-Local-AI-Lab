# D01 — répétition des commandes vocales

Défaut signalé : « Répétition des commandes vocales ». Le détail utilisateur reste à préciser : commande à répéter pour être prise en compte, duplication d'une émission, ou les deux. Diagnostic d'abord ; ne pas présenter une hypothèse comme un résultat.

Attendu : une émission vocale complète produit une prise en compte visible unique, sans répétition imposée ni duplication. Deux commandes volontairement identiques restent deux commandes. Ne pas masquer le défaut par filtrage textuel arbitraire.

Sources utiles uniquement : source/site/voice.js, source/site/app.js (sendPrompt, toggleMic), source/site/api.js ; source/site/livekit.js si le défaut concerne ce mode. Pas de lecture complète du projet. Production reste /var/lib/jarvis/projects/jl03 ; modifications et preuves dans ce dossier D01/source isolé, pas dans D02 ou la production avant contrôleCodex.

JARVIS dirige : ACK et sous-tâches de taille raisonnable, affectationsDell1/Dell2 choisies par toi, lancement des vrais exécutants, supervision et rapport. Première réception : écrire CHECKPOINT.json avec ack=true, problème/hypothèses, sous-tâches/affectations, état/prochaines actions et blocages ; réponse courte.

Capacité réellement observée parCodex : host_remote Dell1=dell-observe dispose d'autres projets, mais pas de projetJL03 ; Dell2=dell2 a SSH/Ansible de réception, pas de project_exec autorisé. Ne pas appeler trois fois une action absente ni prétendre lancer ces workers. Demander la capacité de projet ciblée àCodex avec capability_request puis continuer ce qui est indépendant. Aucun modèle nouveau ni changement de routage demandé.

Validation : reproduction ciblée avant/après, trace capture→STT→envoi→réponse ; une prise en compte par émission, répétition volontaire préservée ; arrêt/reprise micro et interruption TTS sans duplication ni perte ; au moins une chaîne numérique avec audio réel si disponible, tests simulés étiquetés. Réception microphone physique propriétaire distincte.

Trois échecs comparables par blocage : arrêt, dossier, escalade ; compteurs conservés dans le journal canonique même après nouveau contexte. Journaux longs dans logs/, checkpoint compact avant renouvellement ; ne recharge pas toute la conversation. Rapport final compact : Identifiant, Statut, Exécuteurs réels, Actions, Tests/preuves, Blocages/compteurs, Références, Prochaine action. Un résumé n'est pas une preuve.

Directives consultéesCodex : AGENTS/charte/dernierJL03, dernière autorisation propriétaire deux tâches en contextes distincts ; préserverJL01/JL02 et services/mémoire ; aucune fusionmain. Lis uniquement ce paquet et les extraits utiles àD01.

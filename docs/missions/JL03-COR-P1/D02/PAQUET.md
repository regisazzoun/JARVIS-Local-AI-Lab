# D02 — transcription Whisper incohérente

Défaut signalé : transcription Whisper incohérente dansJL03. Identifier le chemin réellement touché et ses entrées ; distinguer capture/format/canaux, segmentation et réponseSTT. Ne pas imputer d'avance le défaut au modèle.

Attendu : transcription française fidèle à l'audio, sans phrases inventées sur silence ni fragments incohérents ; conservation des émissions distinctes et restitution exploitable. Ne pas corriger arbitrairement le sens des commandes ni substituer silencieusement un modèle.

Sources utiles uniquement : source/site/voice.js et source/site/api.js, puis contrat du serviceSTT réellement appelé. Ne lis pas tout l'historiqueD01 ni le dépôt. Dossier actuel D02/source isolé ; pas d'édition deD01 ou de la production. Si dépendance avec captureD01, enregistrer le besoin de référence/patch au lieu d'en recopier le contexte ou d'intégrer concurremment.

JARVIS dirige : ACK, diagnostic, sous-tâches raisonnables, affectationsDell1/Dell2 choisies par toi, lancement des vrais exécutants, supervision et rapport. Première réception : écrire CHECKPOINT.json avec ack=true, problème/hypothèses, sous-tâches/affectations, état/prochaines actions et blocages ; réponse courte.

Capacité réellement observée parCodex : Dell1=dell-observe n'a pas de projetJL03 autorisé ; Dell2=dell2 a réceptionSSH/Ansible, pas de projetexécutable. Demander la capacité de projet àCodex via capability_request ; ne pas multiplier les appels refusés. Les deuxDell exécutent les tâches sans installation de nouveau modèle ni modification du routage.

Validation : corpus français de test autorisé avec texte attendu, silence et entrées invalides ; vraies lectures audio/STT et comparaison avant/après, provenance/paramètres conservés ; tests workers réellement exécutés, pas de réponse simulée présentée commeWhisper. Les échantillonsPiper du laboratoire peuvent servir ; ne pas utiliser ni publier des extraits de film. Tests navigateur et acoustique physique restent distincts.

Trois échecs comparables par blocage : arrêt/diagnostic/escalade ; compteur dans journal canonique, jamais remis à zéro par session. Journaux longs dans logs/, checkpoint compact avant renouvellement. Rapport synthétique : Identifiant, Statut, Exécuteurs réels, Actions, Tests/preuves, Blocages/compteurs, Références, Prochaine action. Codex valide avant intégration.

Directives consultéesCodex : AGENTS/charte/dernierJL03, autorisation récente deux tâches en contextes distincts ; préserverJL01/JL02/services/mémoire ; aucune fusionmain. ContexteD02seul, sans rechargeD01.

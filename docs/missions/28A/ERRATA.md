# Errata prioritaires sur les sorties originales

Les fichiers JARVIS-*-BRUT.md conservent les réponses conversationnelles réelles. Les faits suivants prévalent sur leur prose.

- Le tag `qwen3:32b-q4_K_M` existe au registre officiel. Sa non-présence dans /api/tags local signifiait seulement qu’il n’était pas installé. Le27B déjà présent ne constituait pas son remplacement accepté. Le téléchargement32B effectif est une opération ultérieure via l’interface réparée ; voir les reçus dans PREUVES-JARVIS.json.
- La première tentative GET /api/pull a reçu405 ; l’impression d’un texte HTTP200/done par le script initial ne la rend pas réussie. Le modèle a ensuite utilisé POST et téléchargé réellement le70B. Le nouveau contrat confronte la fin du flux à la présence du tag exact.
- Les températures48–51°C relevées après la campagne ne sont pas les maxima sous charge. La preuve indépendante de l’essai court donne un maximumGPU66°C et une pointe cumulée699,37W. Le retour250W/carte est observé ; aucune mesure à la prise ni tenue prolongée700W n’est établie.
- La correction du contrat et le programme de gestion des modèles sont développés/installés par Codex. Les appels effectifs du nouvel outil et de la campagne GPU sont effectués par JARVIS. La planification coordonnée n’est pas une preuve de planification autonome.
- La réussite de217tests logiciels ne signifie pas que217opérations agentiques ont été reçues. Le70B reste provisoire ; le gain qualitatif par rapport au27B n’est pas encore réceptionné.

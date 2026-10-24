# Répartition Mac mini75/25

Le Mac dispose de12threads logiques. Le plafond de fond est `CPUQuota=900%`, soit9CPU de référence, et non900% de la machine. Le noyau expose `cpu.max=900000 100000`. La capacité restante peut servir à l’interaction ; la réserve ne signifie pas une utilisation permanente de25%.

Le slice interactif reçoit CPUWeight1000 et MemoryLow20G ; le slice parent porte aussi MemoryLow20G. Le fond reçoit CPUWeight25, MemoryHigh4G et MemoryMax8G. Ollama et la conversation sont dans le slice interactif. Le worker et les commandes hôte de mission sont affectés au slice de fond ; les poids sont relatifs et ne constituent pas seuls une garantie de latence.

Le watchdog réduit temporairement le plafond de fond à300% pendant une interaction ou une pression détectée, puis le rétablit à900%. Les traces de réception ont effectivement montré les deux valeurs. Un essai fini de douze processus de charge a consommé environ75,3% agrégés sur8s, compatible avec les frontières de période d’un quota75% ; la valeur du noyau reste l’autorité sur le plafond.

Les modèles de mission sont placés sur le Dell par défaut. Aucun modèle léger ne remplace le27B local. L’admission vérifie les ressources ; le GPU n’est pas découpé matériellement en fractions75/25. Les résultats CPU et les latences observées restent des mesures ciblées, pas une promesse universelle de temps de réponse.

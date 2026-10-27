# Intervention P4 — copies, chemins et contrat d'exécution

P4 reste **EN COURS — NON VALIDÉ**. InterventionCodex après la question du propriétaire sur la poursuite improductive de l'audit. Aucun essai P2/P3 rejoué, aucune validation humaine ajoutée, aucun modèle/routage modifié.

## Causes vérifiées

- Les Dell contiennent des exports de sources sans Git ni .git. C'est un état attendu, pas un dépôt à réparer ou à réinstaller.
- Le fichier existe surlesdeuxDell sous engine/jarvis/core.py ; le chemin engine/core.py était faux. L'analyse du modèle concluant à un export absent était incorrecte et reste conservée.
- Le corps de authority_work exigeait executor et command pour inspect/test/correct, mais son schéma ne les rendait pas obligatoires. Le modèle pouvait donc produire une intention valide au regard du schéma, inexécutable par le corps.

## Corrections et vérifications

PréflightCodex57077 : les cinq fichiers de référence existent et leurs SHA correspondent à l'observation source sur chacun des deuxDell, via Python3/hashlib. Aucun Git installé ni copie convertie artificiellement en clone. Les trois incidents de délégation restent dans delegation_failures ; delegation_resolved_through=3 enregistre leur résolution après un changement réel de méthode. Aucun compteur brut remis à zéro.

Commit926ab42 : conditions JSON Schema pour les paramètres d'exécution, commande non vide, phase optionnelle d'exécution concrète.70tests logiciels ciblés PASS, dont trois nouveaux tests du contrat réellement exposé par le Registry ; distincts de l'autonomie. Déploiement57096 sur le coordinateur et les deux exports, contrôle du schéma installé57099, rechargement des seuls workers. Sauvegarde privée disponible ; conversation/Launcher/Ollama préservés.

JARVIS a ensuite exécuté ses programmes : premier échec57121 conservé, puis artefacts produits surDell2(57177) etDell1(57205). Contrôle indépendantCodex57490 : les SHA relevés dans les deux artefacts pour core.py et tools.py correspondent à la source observée. Deux fichiers relevés, pas cinq ni un dépôt complet. L'audit global n'est donc pas reçu.

Le mode authority_execution_only était temporaire pour exiger une vraie commande. Après ces preuves, il a été désactivé et les outils de réception/compte rendu ont été rendus, sans redémarrage des services ni effacement des compteurs. Les lecteurs répétitifs restent masqués pour cette stratégie.

## Limites et suite

La comparaison des fichiers surdisque ne prouve pas le code chargé. Un instantané de services conservait aussi des PID historiques après mise à jour des SHA : une observation datée nouvelle a été fournie sous un nom distinct, les données anciennes restant historiques. Il ne faut pas lire ces PID comme une attestation permanente du processus actif.

JARVIS poursuit son audit et ses comptes rendus, avec supervision périodique existante. Aucune réception P4, du déploiement ou du rollback n'est annoncée par cette intervention. Preuves : DEBLOCAGE-GIT-ET-CHEMINS.json, CORRECTION-CONTRAT-EXECUTION.json et PREUVES-REPRISE-CONTRAT.json.

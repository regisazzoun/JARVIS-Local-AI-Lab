# Écarts et rationalisation

Trois recouvrements fonctionnels sont établis, sans suppression autorisée :

1. **Deux interfaces Google** : ancien google_workspace et nouveau google_mcp. Vérifier les anciens jetons et consommateurs avant dépréciation ; ne pas confondre deux profils de comptes nécessaires avec un doublon.
2. **Historique WebUI et mémoire JARVIS** : WebUI conserve son chat ; la mémoire canonique JARVIS n’est utilisée que lorsque le parcours passe par ses API. Un chat Ollama brut ne devient pas une mission ou un souvenir canonique. Clarifier les profils avant tout changement de stockage.
3. **Collecte et surveillance réparties** : telemetry_launcher, health, supervision Dell, watchdog et garde Qwen remplissent des rôles partiellement voisins. Ils ne sont pas tous identiques : santé de service, charge, disponibilité d’inférence et progression de mission sont des contrats différents. Mutualiser les métriques avant de fusionner des décisions.

Deux instances Ollama Dell 1 sont un choix de séparation de services, pas deux copies physiques du catalogue : même racine de modèles. Trois modèles historiques existent sur Mac et Dell 1 ; suppression non recommandée avant analyse de l’usage et du secours. Les modèles 32B/70B non chargés aujourd’hui ont une histoire de comparaison reçue.

Risque majeur : six modules installés différents de la branche documentaire. Les mises à jour par remplacement de fichier complet pourraient perdre des corrections actives. Produire un manifeste source/configuration/installation, puis comparer les versions avant toute transformation.

Le premier essai Qwen Code de cet audit s’arrête sur contexte estimé 12946 au-dessus d’une limite 9768, malgré une fenêtre 32768 annoncée dans le lanceur. Ce sont deux couches distinctes : budget client et fenêtre serveur. Ne pas annoncer une saturation de VRAM ; aucun OOM n’est prouvé. Le second essai court réussit les appels mais invente des disques et transforme des valeurs MiB en Ko. La prose ne doit pas alimenter les inventaires sans contrôle.

Aucun nouvel orchestrateur, aucune suppression de poids, aucun déploiement P7 ou remplacement d’interface dans ce bilan. Les services sans panne observée ne sont pas redémarrés pour vérifier leur présence.


[Comparatif des standards et contrats](COMPARATIF-STANDARDS.md).

La limite 9768 observée peut être un budget utile après réservation des outils et de la réponse ; elle ne prouve pas que la fenêtre serveur32768 a été réduite. La cause exacte de la compaction refusée reste à isoler. Le besoin démontré est de borner ce parcours réel, pas de relever aveuglément la VRAM ou les limites.

# Intégration future Dell2

Le Dell2 reste désactivé et non installé. `operations/mission28a/dell2-profile.json` décrit un profil logique avec100% de capacité exploitable destinée aux missions, sans adresse ni capacité matérielle inventée. CPU, RAM, GPU et modèle sont inconnus jusqu’à observation.

L’intégration ultérieure réutilisera l’installation/enrôlement autorisés dans la mission distincte du Dell2, les contrôles d’identité, clés épinglées, SSH/Ansible, puis une instance d’inférence et une sonde de ressources. Après découverte réelle, renseigner son profil protégé, son URL privée, le catalogue effectivement installé et les réserves mesurées, puis activer le nœud dans les routes canoniques. Ne pas recopier l’identité Tailscale/SSH du Dell1.

Le routeur accepte déjà un second nœud configuré. Il sélectionne un nœud éligible selon la charge de file pour les missions. Le test logiciel offline→ready utilise un catalogue de fixture explicitement simulé : il montre le raccordement du code, pas l’existence du serveur. Le test offline confirme l’absence de toute requête réseau vers le Dell2 désactivé.

La mémoire et les missions restent canoniques sur le Mac. En cas d’indisponibilité, les checkpoints ne sont pas recréés ailleurs ; le prochain appel éligible choisit un nœud disponible. Une mutation dont le résultat est inconnu exige une nouvelle observation avant reprise. L’activation future de plusieurs workers durables est une extension d’ordonnancement à mesurer ; aucune exécution parallèle réelle sur Dell2 n’est reçue par28A.

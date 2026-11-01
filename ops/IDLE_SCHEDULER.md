# Mission de fond — ordonnanceur expérimental

**État : code préparé, non déployé, non actif.** Ticket de cadrage : #46.

## Contrôles
L'ordonnanceur n'exécute rien par défaut. Il faut simultanément `enabled: true` dans un fichier de configuration local et l'option `--execute`. Il accepte des commandes structurées `argv` sans shell. Il attend la disponibilité CPU et mémoire puis exécute une unité courte. Il interrompt l'unité si la charge remonte ou au bout du délai ; l'application appelée DOIT prendre en charge les checkpoints et l'arrêt SIGTERM. Un fichier JSON conserve les étapes réussies et le nombre d'échecs (plafond 3). **Attention :** ceci n'est pas une préemption transactionnelle d'une mission arbitraire.

## Essai inoffensif, sur un hôte Linux de test
```sh
python3 ops/idle_scheduler.py --config ops/idle_scheduler.example.json
```

Pour un véritable essai il faut d'abord copier le JSON dans une configuration locale, choisir un chemin d'état accessible en écriture et activer explicitement `enabled`, puis ajouter `--execute`. Ne pas l'installer comme service en production avant revue.

## Conditions avant déploiement
- Vérifier l'architecture existante des workers JARVIS, ne pas lancer deux ordonnanceurs.
- Ajouter mesure GPU/VRAM NVIDIA, charge des modèles Ollama et sessions actives, état Dell 1/Dell 2 et modèle de quotas.
- Verrouillage monoinstance, journaux, reprise robuste après crash, protection contre tâches malveillantes, identités système restreintes.
- Vérifier interruption/récupération, sécurité des chemins et de l'environnement, tests de non-régression.
- Ne jamais stocker de secrets ni autoriser des opérations de production sans validation.

**Il n'y a pas d'activation autonome de JM-01 sur les serveurs à ce stade.**

## Réutilisation obligatoire de la supervision JARVIS existante
Le projet possède déjà des mesures CPU/RAM/GPU multi-hôtes (affichées dans le Launcher et/ou via les outils JARVIS). **Avant tout déploiement**, identifier leur point d'accès exact, leur fraîcheur et les droits d'accès, et faire de cette source le pilote principal de l'ordonnanceur. Les sondes locales `/proc` et `nvidia-smi` de ce prototype sont des garde-fous temporaires, **pas un second système de supervision à mettre en production**. Si une mesure hôte manque ou est périmée, aucun lancement de tâche de fond sur cet hôte. Conserver en priorité les missions interactives et la charge de modèles Qwen.

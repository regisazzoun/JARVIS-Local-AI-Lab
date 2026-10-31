# Architecture cible proposée, non déployée

Conserver le Mac comme point de coordination : Mission Engine, mémoire SQLite/FTS5, registre de contrats, broker et preuves. Conserver Dell 1 comme nœud d’inférence 80B et exécuteur isolé ; Dell 2 comme exécuteur CPU/GPU tant qu’aucune inférence n’y est explicitement déployée et réceptionnée. Décrire ces rôles dans un inventaire Ansible versionné plutôt que copier toutes les applications partout.

**Interfaces** : Open WebUI assure la conversation standard. JL03 conserve les fonctions spécifiques demandées : orbe et console chronologique des preuves. Les deux appellent les mêmes API canoniques lorsqu’une mission ou un souvenir JARVIS est requis. Les historiques d’interface sont distingués de la mémoire canonique, sans migration implicite.

**Programmation** : réutiliser Qwen Code pour édition, terminal, tests et sessions. Le Mission Engine lui délègue une tâche bornée et conserve état, acteurs, code testé et reçus. Ne pas reconstruire un second agent de programmation ni un Goal parallèle. Le modèle 80B reste servi par Ollama Dell 1 ; le lieu de l’inférence ne désigne pas le lieu d’exécution des commandes.

**Outils** : registre unique, export MCP et API générés depuis les mêmes schémas, pagination et retour compact, données détaillées en artefacts persistants. Profils Google personnel/Éducation distincts et jetons séparés. Garder le connecteur amont reçu ; aucune offre plafonnée ou abonnement intermédiaire retenu.

**Supervision P7** : métriques standardisées via collecteur éprouvé (Ansible facts, nvidia-smi ou exporter compatible), complétées d’un adaptateur vers les incidents existants. systemd garde les redémarrages de processus ; le moteur vérifie la reprise fonctionnelle d’une charge réellement attendue. Ni VRAM vide ni 0%GPU ne suffisent à déclencher une correction.

**Frameworks** : LangGraph fournit des checkpointers/stores, Temporal une exécution durable et des retries. Ils pourraient réduire du code générique mais ne remplacent pas directement le ledger de preuves, la politique propriétaire, l’identité des hôtes et la réception sémantique. Une migration globale ajouterait infrastructure et risque sans gain mesuré ici. Préférer des composants ciblés et un essai de contrat avant remplacement.

Tout changement ultérieur exige une version épinglée, licence vérifiée, sauvegarde, comparaison avant/après et critères propres. Il ne faut pas attribuer les fonctions de la documentation actuelle à Qwen Code0.26.4 sans contrôle. Cette architecture est une recommandation, pas un déploiement reçu.

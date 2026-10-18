# Ressources — mission 22

Inventaire réel Codex : Mac mini,12 threads, environ32 Gio RAM ; Dell n°1, environ256 Gio RAM, une RTX3090 opérationnelle. L'API Ollama confirme le modèle Qwen27B entièrement chargé en VRAM avec contexte16384. Observation GPU réelle pendant l'essai :100% d'utilisation, environ17,5 Gio utilisés ; le second GPU n'est pas sollicité.

[Mesures brutes non sensibles](MESURES-CONTEXTE.json) : deux inférences courtes, contextes8192 et16384. Ce n'est pas un benchmark de qualité ni une moyenne. Le coût observé à16384 inclut environ15,9s de chargement du modèle ; les durées de génération seules sont proches. Aucune amélioration sémantique n'est déduite de ces deux réponses.

Le contexte durable16384 réserve de la place aux schémas d'outils, objectifs et preuves ; la voix peut conserver son contexte existant. La consommation doit être comparée à la réussite de missions, pas au seul débit. Le déploiement supprime MemoryMax=2G et TasksMax=128 du service conversation conformément à la demande propriétaire. Aucun quota CPU n'existait. Les frontières d'accès aux secrets et les contrôles d'identité ne sont pas des plafonds d'économie et sont conservés.

Références primaires : [Ollama FAQ](https://docs.ollama.com/faq), [paramètres Modelfile](https://docs.ollama.com/modelfile). num_ctx est explicite ; keep_alive maintient le modèle chargé. Le nombre de générations d'un cycle sert au partage du worker : il ne limite pas la durée de vie d'une mission durable.

# Ressources — mission 22

Inventaire réel Codex : Mac mini,12 threads, environ32 Gio RAM et une RTX3090 réellement détectée ; Dell n°1, environ256 Gio RAM, une RTX3090 opérationnelle. L'API Ollama confirme le modèle Qwen27B entièrement chargé en VRAM avec contexte16384. Observation GPU réelle pendant l'essai :100% d'utilisation, environ17,5 Gio utilisés ; le second GPU n'est pas sollicité.

[Mesures brutes non sensibles](MESURES-CONTEXTE.json) : deux inférences courtes, contextes8192 et16384. Ce n'est pas un benchmark de qualité ni une moyenne. Le coût observé à16384 inclut environ15,9s de chargement du modèle ; les durées de génération seules sont proches. Aucune amélioration sémantique n'est déduite de ces deux réponses.

Le contexte durable16384 réserve de la place aux schémas d'outils, objectifs et preuves ; la voix peut conserver son contexte existant. La consommation doit être comparée à la réussite de missions, pas au seul débit. Le déploiement supprime MemoryMax=2G et TasksMax=128 du service conversation conformément à la demande propriétaire. Aucun quota CPU n'existait. Les frontières d'accès aux secrets et les contrôles d'identité ne sont pas des plafonds d'économie et sont conservés.

Références primaires : [Ollama FAQ](https://docs.ollama.com/faq), [paramètres Modelfile](https://docs.ollama.com/modelfile). num_ctx est explicite ; keep_alive maintient le modèle chargé. Le nombre de générations d'un cycle sert au partage du worker : il ne limite pas la durée de vie d'une mission durable.


## Deux GPU sur deux machines, sans solliciter le second GPU du Dell

Le catalogue réel contient les trois mêmes modèles sur Mac mini et Dell1. Le routage interactif utilise le Mac ; les missions utilisent le Dell. La seconde carte non alimentée du Dell reste exclue. Les verrous sont séparés pour éviter qu'une mission longue bloque la voix.

[Test réel de concurrence](CONCURRENCE-VOIX-CONVERSATION.json) : synthèse Piper WAV en2,12s pendant une mission ; conversation Qwen sur le Mac en39,14s dont33,70s de chargement à froid. Le worker Dell restait actif. Cela ne vaut pas test de microphone physique. Le coût à froid doit être distingué de la génération chaude.

[Essai réflexion et repli](ROUTAGE-REFLEXION.json) : véritable nœud primaire indisponible sur un port de test, puis réponse réelle sur Mac. Sur la même petite question shell, think=false a produit une proposition en1,03s ; think=true en245,56s avec9115 tokens évalués. Les deux propositions sont plausibles ; ce test de génération n'exécute pas les commandes et ne réceptionne pas l'autonomie. Aucune limite de durée n'a été introduite pour interrompre cette réflexion. Le réglage existant think=false reste celui de production, faute d'amélioration démontrée sur cet essai. Le réglage est désormais configurable pour de futurs essais.


## Réglage de finalisation

Le contexte durable passe de16384 à32768 après observation de lectures volumineuses compactées à chaque tour. Le reçu complet reste dans le journal, les vues du modèle sont bornées et explicitement signalées comme extraits ; ce réglage vise la conservation du contexte utile, sans économiser les ressources disponibles. Il ne garantit pas à lui seul une meilleure autonomie. Le dernier échantillon et les limites réelles figurent dans [RESSOURCES-FINALES.json](RESSOURCES-FINALES.json). Aucun quota CPU/RAM/tâches du service ; `durable_num_predict=-1`. Les délais réseau et quanta servent à la reprise, sans durée maximale de mission.


La [télémétrie finale de JL-02](TELEMETRIE-JL02-FINALE.json) voit réellement Mac mini et Dell1 disponibles, Ollama actif sur les deux. Après passage en attente externe, les GPU sont à0% d’activité au prélèvement ; le Dell conserve le modèle chargé en VRAM. Cela distingue absence de travail actif et indisponibilité. Dell2 reste indiqué indisponible, sans déploiement.

# Centre de documentation JARVIS

Ce répertoire propose une **navigation thématique** sans déplacement ni suppression des documents historiques. Le statut des missions est documentaire et reflète les preuves retrouvées, pas l'état instantané des machines.

## Accès rapides

| Besoin | Document |
| --- | --- |
| Comprendre l'architecture et les plateformes | [Architecture et plateformes](01-architecture/README.md) |
| Suivre les expériences Mac mini, eGPU et CUDA | [Matériel et calcul GPU](02-plateformes-gpu/README.md) |
| Retrouver Ollama, WebUI, voix et mémoire | [Services IA et interfaces](03-services-ia/README.md) |
| Consulter toutes les missions et leurs preuves | [Missions Codex](07-missions-codex/README.md) |
| Voir les résultats vérifiés et leurs limites | [État technique](../indexes/ETAT_TECHNIQUE.md) |
| Voir les décisions prises | [Décisions](../indexes/DECISIONS.md) |
| Retrouver les archives collectées | [Archives](../archives/README.md) |
| Suivre les travaux ouverts | [Priorités et réserves](04-suivi/README.md) |
| Consulter la chronologie consolidée | [Chronologie](../indexes/CHRONOLOGIE.md) |
| Consulter le rapport de récupération | [Rapport final](../indexes/RAPPORT_FINAL.md) |

## Principes

1. Conserver les originaux et leurs empreintes SHA-256, avec provenance dans [le manifeste](../indexes/MANIFESTE.json).
2. Classer les sujets par **liens documentaires**, sans réécrire les archives ni déplacer les rapports existants.
3. Distinguer les statuts **prévu / installé / testé / validé**, sans transformer un essai historique en validation actuelle.
4. Ne jamais publier de secrets, bases de données privées ou journaux non nettoyés.
5. Laisser les opérations serveur, Docker, SSH, GPU et mission 13F hors du périmètre documentaire.

Les [documents historiques](chronologie.md) et [la méthode expérimentale](methodologie.md) demeurent inchangés.

# État technique réellement démontré

État historique issu des preuves, sans nouvel essai du serveur le 14 octobre. La présence d’un service ou d’un fichier ne prouve pas sa validation actuelle.

| Catégorie | Éléments et limites | Source |
|---|---|---|
| Fonctionnel et validé dans les essais | CUDA mathématique et inférence Quadro ; Llama RTX 3090 après correctif ; Qwen 65/65 couches GPU | [05D](../missions/mission-05d/README.md), [09B](../missions/mission-09b/README.md), [10](../missions/mission-10/README.md) |
| Installé mais non validé à cette étape | DKMS avant chargement ; aucune stabilité prolongée établie | [05B](../missions/mission-05b/README.md) |
| Partiellement opérationnel | Voix/mémoire avec Ollama réel et Chromium ; source micro artificielle, clients physiques et HTTPS distant non validés | [13E](../missions/mission-13e/README.md) |
| En expérimentation | Autonomie 13F : fichiers et tests intermédiaires, aucun rapport final ; sûreté du raisonnement limitée | [13F](../missions/mission-13f/README.md), [10](../missions/mission-10/README.md) |
| Planifié, non démontré | Clients 13D, Dell 14, mission 15 reportée ; aucune réalisation présumée | ROADMAP existante, [13D](../missions/mission-13d/README.md) |

L’échec historique 09 est conservé même après 09B. Les validations 13E ne sont pas rétroactivement attribuées à 13BC. Aucun test de production, compilation, déploiement ou redémarrage exécuté pendant cette mission.

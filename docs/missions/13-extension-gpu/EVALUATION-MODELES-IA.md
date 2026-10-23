# Modèles IA — réévaluation préparatoire, sans nouveau benchmark

Deux3090 sont visibles au pilote et à PyTorch. Cela fournit deux budgets par carte, pas un seul espace48Go. L’accès pair est faux et le service Ollama reste limité à une carte ; aucune amélioration de débit ou de fiabilité agentique n’est déduite de l’ajout physique.

## Catalogue réellement présent

| Modèle | Taille locale du fichier catalogue | Usage à comparer | Mesure nouvelle |
| --- | --- | --- | --- |
| qwen3.5:27b-q4_K_M |17478556591octets,16,28GiB | Conserver comme référence agentique ; poids/contexte/buffers doivent tenir sur la carte affectée | Aucune nouvelle latence/débit reçue |
| ministral-3:14b-instruct-2512-q4_K_M |9082537546octets,8,46GiB | Candidat plus léger pour réponse interactive | Non comparé ici |
| llama3.1:8b |4920753328octets,4,58GiB | Référence légère | Non comparé ici |

Ce sont des tailles de catalogue, pas la VRAM totale d’exécution. Les empreintes exactes et métadonnées de quantification sont dans INVENTAIRE-OBSERVE.json. Les anciennes inférences13D-E restent acquises dans leur périmètre ; elles ne deviennent pas des benchmarks double-GPU.

## Candidats supplémentaires documentés, non téléchargés

- [Qwen3 32B Q4_K_M](https://ollama.com/library/qwen3:32b-q4_K_M) : catalogue fournisseur20GB. Candidat de comparaison, sans présumer un meilleur raisonnement que le27B actuel ou sa tenue à long contexte sur24GiB.
- [Llama3.3 70B Q4_K_M](https://ollama.com/library/llama3.3:70b-instruct-q4_K_M) : catalogue43GB, donc candidat à répartition, avec peu de marge après poids pour KV/buffers. Ne pas garantir qu’il tient avec le contexte souhaité et les autres services. Licence et compatibilité exacte du runtime à vérifier lors du téléchargement.
- Quantifications plus élevées : augmenter la précision augmente généralement le stockage des poids, mais l’effet sur qualité et débit doit être mesuré ; aucun gain chiffré n’est annoncé. Pour70milliards de paramètres, le seul stockage théorique4bits représente35milliards d’octets avant surcoûts ; ce calcul ne remplace pas le fichier réel43GB du catalogue.

## Configuration cohérente à ce stade

Conserver le modèle et le service actuels tant que l’électricité n’est pas qualifiée. Après qualification, essayer d’abord une répartition de charges indépendantes : LLM principal sur une carte, modèle auxiliaire ou futur TTS sur l’autre. Cela correspond à un placement expérimental local ; aucun TTS n’est relancé ici et aucun routeur mission28 n’est installé.

Comparer ensuite un modèle réparti avec une instance d’essai explicitement autorisée à voir les deux GPU. Mesurer le premier contenu, débit, charge/mémoire par carte, CPU/RAM, erreurs, contexte effectif et température. Le schéma de mesure est préparé dans `operations/mission13-dual/benchmark.py`, non exécuté. La [FAQ Ollama](https://docs.ollama.com/faq) décrit le placement mono si le modèle tient, réparti sinon ; cela reste à vérifier sur la version locale. Deux requêtes simultanées, deux modèles résidents et le partage de couches sont trois essais différents.

Les251,42GiB exposés à Linux permettent d’envisager un offload, sans le rendre interactif par principe ;256Go est la capacité historique déclarée. Aucun besoin RAM/KV réel pour un nouveau70B n’est mesuré.

## Critères avant changement du modèle principal

Même prompt, contexte, quantification et limites de génération comparables ; une phase de chargement identifiée, puis un essai chaud. Vérifier des appels d’outils réellement exécutés, couverture d’objectif, corrections et fidélité des rapports. Les erreurs observées pendant cette reprise rappellent qu’un modèle plus gros et davantage de VRAM ne garantissent pas une autonomie plus fiable. Le choix définitif reste ouvert jusqu’aux mesures.

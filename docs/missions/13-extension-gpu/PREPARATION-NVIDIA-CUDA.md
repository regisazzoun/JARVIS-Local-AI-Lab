# Préparation logicielle

## État réellement observé

Le pilote550.163.01 initialise déjà les deux GA102. `nvcc`12.4.131 est disponible ; le venv expérimental TTS existant fournit PyTorch2.6.0+cu124/runtime12.4. JARVIS y a exécuté le petit calcul sur chaque carte :120.0 obtenu,120.0 attendu. Aucune installation de pilote, paquet, BIOS ou nouveau service n’est nécessaire pour ces résultats. Le venv est réutilisé en lecture ; TTS reste suspendue.

Les scripts [inventory.py](../../../operations/mission13-dual/inventory.py) et [cuda_check.py](../../../operations/mission13-dual/cuda_check.py) sont développés par Codex et exécutés par JARVIS via deux commandes fixes du broker existant. Pas de nouvelle base, clé SSH ou shell root donné au modèle. Le garde d’identité11B s’applique avant chaque appel.

L’inventaire a été corrigé par Codex : réduction de la sortie PCI tronquant le premier JSON, lecture du bind Ollama réel au lieu d’imposer loopback, résumé limité à la vue modèle et masquage de l’UUID GPU. Les traces initiales restent conservées. Le refus loopback initial ne démontrait pas une panne du service.

## Ollama et affectation

Ollama0.40.3 est actif, mais son service définit `CUDA_VISIBLE_DEVICES` sur un seul UUID. Configuration observée : contexte4096, parallélisme1, un modèle chargé au maximum. La seconde carte est disponible pour des processus qui la voient, pas automatiquement pour ce service. La [documentation officielle GPU](https://docs.ollama.com/gpu) décrit la sélection par UUID, préférable à un index susceptible de changer ; ne publier que des espaces réservés.

Après qualification électrique, comparer trois modes, sans modifier le service principal à l’aveugle :

| Mode | Configuration à appliquer seulement lors de l’essai | Limite de la préparation |
| --- | --- | --- |
| Référence actuelle | Garder le service/UUID existant | Déjà configuré ; pas de nouveau débit mesuré ici |
| Modèle réparti | Service d’essai borné aux deux UUID et port local distinct ; même dépôt de modèles accessible sous les droits existants | À créer/tester après qualification ; pas de deuxième service permanent installé |
| Modèles séparés | Une instance d’essai par UUID, ports distincts et catalogue existant | Capacité de placement préparée, pas un routeur mission28 ni un test de concurrence acquis |

Exemple de **paramètres**, pas fichier installé : `CUDA_VISIBLE_DEVICES=GPU_UUID_A,GPU_UUID_B`, `OLLAMA_HOST=127.0.0.1:11435`, `OLLAMA_NUM_PARALLEL=1`. Utiliser l’exécutable et le dépôt de modèles relevés localement ; ne pas lancer une instance root ni exposer un port public. Vérifier que la version installée accepte chaque option avant son usage.

La [FAQ officielle](https://docs.ollama.com/faq) décrit un placement sur un GPU si le modèle y tient, une répartition sinon. Cette documentation courante ne remplace pas un essai sur0.40.3. Une distribution de couches n’est pas une mémoire monolithique ni une multiplication garantie du débit.

## Bus et accès inter-GPU

PCIe maximal Gen3 observé, largeurs courantes x16/x8 au faible usage. La [documentation NVIDIA](https://docs.nvidia.com/deploy/nvidia-smi/index.html) explique que génération et largeur courantes peuvent baisser hors charge ; Gen1 au repos n’est pas une panne démontrée. Topologie SYS et accès pair CUDA faux dans les deux sens. Ne pas promettre NVLink ou transferts directs : vérifier sous charge qualifiée, puis mesurer les transferts et les coûts CPU/PCIe. Aucun réglage BIOS/ACS/IOMMU n’est changé sur cette seule observation.

## Outils de réception préparés

- `cuda_check.py --expect 2` : petits calculs réels et observation de l’accès pair ; un seul GPU donne un statut insuffisant, pas une réception double.
- `benchmark.py` : appel réel streaming `/api/chat`, temps de premier contenu, métriques serveur, débit calculé et échantillons mémoire/charge/température/puissance/PCIe par GPU. Refuse un nombre de GPU inattendu ou l’écrasement d’un résultat. N’effectue ni téléchargement ni modification de service.
- Exécution future : Python disponible, `benchmark.py --model MODELE_EXISTANT --url URL_LOCALE_SERVICE --output NOUVEAU_RESULTAT.json --expected-gpus 2 --context 4096`.

Ces outils sont compilés et leur interface vérifiée. **Le benchmark n’a pas été exécuté dans cette reprise**, faute de qualification électrique. Après qualification, JARVIS doit le lancer et Codex comparer ses fichiers, les événements et les observations NVIDIA. Un exemple de commande n’est pas un test reçu.

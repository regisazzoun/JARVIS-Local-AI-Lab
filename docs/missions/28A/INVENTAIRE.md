# Inventaire utile28A

| Élément | Mac mini | Dell1 |
|---|---|---|
|CPU|Corei7-8700B,6cœurs/12threads|Corei9-10980XE,18cœurs/36threads|
|RAM|32Gio physiques|256Go annoncés,~251,42Gio exposés|
|GPU|RTX3090 externe24Gio|Deux RTX3090 DellOEM,24Gio chacune|
|Système|Debian existant conservé|Debian13.7, noyau6.12.113|
|NVIDIA/CUDA|GPU local exploité par Ollama|Pilote550.163.01, nvcc12.4.131|
|Inférence|Ollama local11434,27B conservé|Instance historique11434 conservée, instance mission11435 utilisant les deux GPU|

Le Dell expose deux liensPCIe Gen3, largeursx16/x8 ; une génération basse au repos est un état d’économie, pas une panne démontrée. La topologieCUDA peer access était fausse dans les deux directions, sans lien NVLink observé. Deux24Gio ne sont pas automatiquement un espace unique48Gio ; le découpage des couches et l’offload dépendent du moteur et des mesures.

Les clés, identifiants matériels uniques, adresses privées et politique root restent hors publication. Aucun pilote, système, partition, RAID ni service vocal n’a été réinstallé pour28A. Le Dell2 n’est pas compté dans les ressources disponibles.

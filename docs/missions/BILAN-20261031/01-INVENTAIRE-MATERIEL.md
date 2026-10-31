# Matériels réellement observés

| Machine | Modèle | CPU | RAM physique GiB | GPU | BIOS |
|---|---|---|---|---|---|
| mac | Macmini8,1 | Intel(R) Core(TM) i7-8700B CPU @ 3.20GHz | 32 | NVIDIA GeForce RTX 3090 | 2020.80.5.0.1 (iBridge: 21.16.3049.0.0,0) |
| dell1 | Precision 5820 Tower X-Series | Intel(R) Core(TM) i9-10980XE CPU @ 3.00GHz | 256 | NVIDIA GeForce RTX 3090; NVIDIA GeForce RTX 3090 | 2.8.0 |
| dell2 | Precision 5820 Tower X-Series | Intel(R) Core(TM) i9-10980XE CPU @ 3.00GHz | 128 | NVIDIA GeForce RTX 3090; NVIDIA GeForce RTX 3080 | 2.24.0 |

Le laboratoire observé comprend trois hôtes x86_64 Debian 13.7 : Macmini8,1, deux Precision 5820 X-Series. Cinq GPU : quatre 3090 et une 3080. Les identités uniques sont remplacées par des empreintes stables ; les bus PCI restent des adresses locales non uniques.

Le Mac possède 32 GiB DIMM, un SSD Apple 500277792768 octets, LVM/ext4 et swap. Les Dell ont chacun deux NVMe 2048408248320 octets, Kioxia et Samsung, miroir RAID1 sain[UU], racine ext4. La santé SMART détaillée et un retrait physique d’un disque ne sont pas testés. Lecteurs SD de taille 0 identifiés : pas assimilés à des disques utilisables.

RAM Dell 1 : huit modules 32 GiB, fabricants mixtes Samsung/Hynix, débit configuré 2934 MT/s. Dell 2 : quatre modules 32 GiB Micron 2934 MT/s, quatre emplacements vides. Mac : deux 16 GiB 2667 MT/s. La RAM utilisable par Linux est inférieure aux valeurs DIMM ; voir JSON.

RTX3090 Mac reconnue sur PCI 81:00.0 et pilote 595.91.07 ; boîtier eGPU documenté historiquement, périphériques PCI/USB observés dans l’inventaire brut, sans nouvelle qualification du boîtier. Dell pilote 550.163.01, nvcc 12.4.131. La version CUDA affichée par nvidia-smi est une capacité du pilote, pas la preuve d’un toolkit identique. Le Mac ne fournit pas nvcc dans le PATH examiné.

Instantané : Mac modèle 27B résident (~17889 MiB utilisés,0% au relevé), Dell 1 même PID llama-server sur deux GPU (~23127/23090 MiB,26/34%), Dell 2 aucun processus compute GPU observé (1 MiB par carte). Ce repos n’est pas une panne. Puissances limites 250 W/carte sur Dell 1 ; pas d’essai 700 W rejoué. Puissance 3080 N/A, aucune valeur inventée.

Ethernet actif 1 Gb/s full duplex sur chaque hôte. Interfaces USB/Wi-Fi/PCI inventoriées dans les preuves privées ; périphériques non qualifiés signalés sans marque/modèle inventés. Pas de manipulation de matériel. [CSV](materiels.csv) · [preuves](preuves/).

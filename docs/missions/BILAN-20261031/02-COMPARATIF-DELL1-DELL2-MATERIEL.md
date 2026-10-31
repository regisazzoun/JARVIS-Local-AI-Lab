# Comparatif matériel Dell 1/Dell 2

| Caractéristique | Dell 1 | Dell 2 | Écart |
|---|---|---|---|
| CPU | Intel(R) Core(TM) i9-10980XE CPU @ 3.00GHz | Intel(R) Core(TM) i9-10980XE CPU @ 3.00GHz | identique observé |
| Cœurs/threads | 18/36 | 18/36 | identique observé |
| RAM DIMM | 256 GiB ; 8 modules | 128 GiB ; 4 modules | différent ; voir conséquence ci-dessous |
| GPU | NVIDIA GeForce RTX 3090 24 GiB + NVIDIA GeForce RTX 3090 24 GiB | NVIDIA GeForce RTX 3090 24 GiB + NVIDIA GeForce RTX 3080 10 GiB | différent ; voir conséquence ci-dessous |
| VRAM cumulée physique | 48.0 GiB | 34.0 GiB | différent ; voir conséquence ci-dessous |
| Stockage | KXG70PNV2T04 NVMe KIOXIA 2048GB 2048408248320 octets + PM9A1 NVMe Samsung 2048GB 2048408248320 octets | KXG70PNV2T04 NVMe KIOXIA 2048GB 2048408248320 octets + PM9A1 NVMe Samsung 2048GB 2048408248320 octets | identique observé |
| RAID | RAID1 mdadm [2/2] [UU] | RAID1 mdadm [2/2] [UU] | identique observé |
| BIOS | 2.8.0 | 2.24.0 | différent ; voir conséquence ci-dessous |
| Debian/noyau | Debian 13.7 / 6.12.113+deb13-amd64 | Debian 13.7 / 6.12.113+deb13-amd64 | identique observé |
| Pilote NVIDIA | 550.163.01 | 550.163.01 | identique observé |
| CUDA toolkit | 12.4.131 | 12.4.131 | identique observé |
| Ethernet actif | 1000 Mb/s full | 1000 Mb/s full | identique observé |
| Tailscale | Running | binaire absent dans PATH ; paquet non trouvé | différent ; voir conséquence ci-dessous |

Sources : [Dell 1](preuves/dell1.json), [Dell 2](preuves/dell2.json). Relevés actuels, pas capacités prévues.

Conséquences : Dell 2 possède moitié moins de RAM physique (128 contre 256 GiB) et une carte 3080 10 GiB, contre 24 GiB par 3090. Un processus assigné à 3080 doit tenir dans sa mémoire ou utiliser une stratégie explicite d’offload ; la somme 34 GiB ne constitue pas une mémoire monolithique. Dell 1 total 48 GiB physique ; même réserve. Un modèle 80B à 51,74 Go de poids ne devient pas compatible Dell 2 sans étude de quantification/contexte/offload. Aucune nouvelle installation ou inférence Dell 2 n’est faite.

Les liens actifs observés sont 1 Gb/s. Un objectif 10 Gb/s ou une interface présente ne prouve pas une négociation 10 Gb/s. Aucun débit réseau ni benchmark n’a été lancé. BIOS différents : Dell 1 en 2.8.0 et Dell 2 en 2.24.0. Cette différence est à examiner avant une harmonisation ; aucun flash n’est autorisé par cet audit. L’alimentation électrique et les câbles ne sont pas requalifiés par cet inventaire.

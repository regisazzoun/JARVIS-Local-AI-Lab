# Inventaire Dell n°1 — réception indépendante

Date de la dernière observation JARVIS : 2026-10-23T12:22:44.653957+02:00. Reçu 9c6280638c2b4452b31fe788f6d35ee3, invocation 2cf2af9e955a4eba8a9a578d3cb647bc. Voir [données](INVENTAIRE-OBSERVE.json) et [corrélation root](CORRELATION-BROKER.json).

| Élément | Résultat réel |
| --- | --- |
| Châssis | Precision 5820 Tower X-Series |
| Carte mère | 0X75JG, révisionA01 ; ne désigne pas la PDB |
| BIOS | 2.8.0, date constructeur01/15/2021 ; inchangé |
| CPU | Intel(R) Core(TM) i9-10980XE CPU @ 3.00GHz, 36threads |
| Mémoire exposée Linux | 263631320KiB, soit251.42GiB ; capacité historique256Go, pas une nouvelle mesure des étiquettes DIMM |
| OS / noyau | Debian13.7 /6.12.113+deb13-amd64 |
| Pilote / toolkit | NVIDIA550.163.01 ; nvcc12.4.131 |
| Calcul CUDA | Deux appareils via PyTorch2.6.0+cu124/runtime12.4, somme120.0 sur chacun |
| Ollama | 0.40.3, actif, limité à un UUID GPU |
| Services Dell observés | SSH, jarvis-ollama, nvidia-persistenced et tailscaled actifs |
| PSU / PDB / faisceaux | PSU950W déclaré, aucune capacité SMBIOS exploitable ; DP/N et brochages à relever physiquement |

## GPU

| Index | VRAM NVIDIA | VRAM occupée | Température | Puissance ponctuelle | Limite annoncée | PCIe courant / maximal |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 24576 MiB | 11 MiB | 31°C | 13.99 W | 350.00 W | Gen1/Gen3, x16/x16 |
| 1 | 24576 MiB | 52 MiB | 36°C | 29.13 W | 350.00 W | Gen1/Gen3, x8/x16 |

Le contrôle PCI indépendant identifie deux GA10210de:2204, sous-système Dell1028:3880 et pilote nvidia sur les deux. Cela conforte l’indication OEM Dell du propriétaire, sans identifier leur DP/N précis ni leurs faisceaux. Topologie SYS ; accès pair CUDA indisponible dans les deux sens. Les versions nvidia-smi et Torch de mémoire totale ne doivent pas être confondues ; les octets Torch exacts sont conservés dans CUDA-JARVIS.json.

Ces relevés sont ponctuels pendant l’intervention. La charge CPU est échantillonnée sur0,25s ; aucune campagne de repos certifié, température mémoire GDDR6X, intensité de ligne PDB ou consommation secteur n’est reçue. Gen1 à faible usage n’établit pas une panne ; le x8 de la seconde carte reste à qualifier sous charge et avec le slot réel.

## Écarts nouveaux par rapport à13D-E et TTS-01

- Une seule3090 était reçue dans les preuves antérieures ; deux sont désormais détectées et chacune exécute le petit calcul CUDA. Le montage physique a été réalisé hors de cette session Codex ; sa date et son câblage exact ne sont pas inférés.
- Pilote550.163.01, Debian13.7, CPU et noyau concordent avec l’état récent ; aucune réinstallation.
- La seconde carte n’est pas visible par le service Ollama actuellement épinglé à un seul UUID.
- Aucun Xid, fallen-off ou AER n’est présent dans l’extrait ciblé du journal de démarrage consulté ; ce contrôle limité ne démontre pas l’absence de toute anomalie historique.
- Les réserves de câblage et de charge double ne sont pas levées par le seul boot.

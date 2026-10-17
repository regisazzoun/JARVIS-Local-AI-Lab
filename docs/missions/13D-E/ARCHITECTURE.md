# Architecture et limites

Séparation : fichiers publics de préparation → worker VM utilisateur dédié → QEMU TCG (KVM seulement après diagnostic) → deux disques qcow2 nommés et réseau SLIRP `restrict=on`. Aucun bridge, TAP, DHCP hôte, port transféré ou périphérique physique. DHCP/TFTP QEMU internes au seul invité. Pas de libvirt global nécessaire. Limite : SLIRP restreint bloque aussi le miroir Debian ; une source de paquets hors ligne ou un proxy documentaire/miroir explicitement limité reste à préparer et tester avant installation complète. Ne pas retirer `restrict=on` pour contourner ce blocage.

Le contrôleur livré sait préparer les commandes, créer deux fichiers qcow2 (24 Gio virtuels chacun), lancer une VM bornée à 30 minutes, collecter ses sorties série et supprimer un workspace marqué. Un verrou exclusif empêche une suppression concurrente par cet outil. Le modèle ne reçoit pas d'argument shell ni de chemin de disque. Un workspace ne doit pas être accessible en écriture à un autre utilisateur. Les actifs sont contrôlés par SHA-256 local ; cette vérification garantit la stabilité, pas la provenance. Vérifier la signature Debian et les signatures/provenances OVMF/iPXE avant de calculer les empreintes.

Le worker reste **non activé**, faute de QEMU/firmware et de canal de paquets isolé validé. Pas de socket/API nouvelle exposée. La modification de la passerelle 13F est différée ; ne pas monter ses secrets ou bases dans la VM.

## Dépendances proposées, non installées

`qemu-system-x86`, `qemu-utils`, `ovmf`, `ipxe`, `cpio`, `gzip`, `ansible-core` ; uniquement après diagnostic de provenance/impact et validation humaine si installation système. Alternative : extraire ces paquets et leurs bibliothèques dans un répertoire utilisateur dédié, sans scripts de maintenance ni services, puis vérifier les versions. Cette alternative n'a pas été exécutée ici. TCG évite toute modification du noyau, mais sera plus lent. Ne pas supposer KVM disponible sur la base du seul flag VMX.

## RAID et matériel Dell : décision différée

Comparer VROC/VMD (exposition contrôleur/namespace, firmware, licence et support RAID NVMe effectifs, module vmd, importation metadata) à mdadm Linux RAID1. Les informations CPU/châssis seules ne prouvent pas la compatibilité VROC. Recueillir ultérieurement `lspci -nnk`, `lsblk -o NAME,MODEL,SERIAL,SIZE,TYPE`, `nvme list`, firmware et topologie FlexBay, sans écriture. Aucune commande Dell exécutée dans cette mission.

Variantes préparatoires :

| Variante | Plan | Condition bloquante |
| --- | --- | --- |
| VM initiale | GPT/ESP et racine automatique sur vda ; vdb réservé | Test de base avant RAID ; ne valide pas la redondance |
| Dell VROC/VMD | Installer sur le volume logique RAID1 reconnu, deux ESP selon exposition firmware | Contrôleur réellement compatible, provenance métadonnées et boot dégradé à démontrer |
| Dell mdadm | GPT sur chaque NVMe, ESP indépendante sur chacun, racine RAID1 mdadm, swap en fichier | Identifier deux SSD par numéro de série et autoriser explicitement l'effacement ; synchronisation des ESP et deux entrées UEFI à vérifier |

Les variantes Dell sont des plans, **pas des recettes exécutables approuvées**. Aucun `wipefs`, `mdadm --create` ou partitionnement physique livré au worker. Une recette RAID1 UEFI préseed non testée ne doit pas être déclarée opérationnelle. La VM livrée ne teste pour l'instant qu'un disque système, malgré la présence de deux disques virtuels.

Sources : [Debian preseed trixie](https://www.debian.org/releases/trixie/amd64/apbs04.en.html), [QEMU invocation / SLIRP](https://www.qemu.org/docs/master/system/invocation.html). Roadmap distante et SUIVI consultés via connecteur GitHub ; les validations 13F restent historiques.

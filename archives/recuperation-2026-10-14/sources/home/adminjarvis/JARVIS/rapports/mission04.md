# JARVIS — Mission 04 : préparation du premier GPU NVIDIA

Date : 11 octobre 2026, diagnostic initial à 18:38–18:40 CEST. Statut : étape 1 réalisée ; attente du signal utilisateur avant connexion du premier Razer Core. Aucun boîtier externe ou GPU NVIDIA détecté, aucune installation ni modification système exécutée.

## Périmètre

Diagnostic en lecture seule et recherches documentaires uniquement. Rapport et preuves créés dans le répertoire utilisateur. Réseau/SSH, noyaux, GRUB et EFI inchangés. Aucune autorisation Thunderbolt accordée, aucun paquet téléchargé/installé, aucun dépôt ajouté, aucun reboot. Les validations Wi-Fi/Bluetooth précédentes figurent dans mission03.md ; l’utilisateur confirme leur disponibilité.

## Thunderbolt, Bolt et PCIe

- Deux contrôleurs Intel JHL7540 Thunderbolt 3 NHI Titan Ridge : 07:00.0 et 7d:00.0, PCI 8086:15eb rev06, pilote thunderbolt actif. Ponts Titan Ridge 8086:15ea et contrôleurs USB 8086:15ec liés à pcieport/xhci_hcd ; ponts amont DSL6540 8086:1578.
- bolt 0.9.8, service actif (unité static ; ce n’est pas une absence d’activation). auth-mode=enabled ; force-power non supporté. Deux domaines domain0/domain1, sécurité user, bootacl 0/0. boltctl list vide ; sysfs ne contient que hôtes 0-0/1-0 et domaines, aucun boîtier externe.
- Noyau : avertissement sur chaque NHI « device links to tunneled native ports are missing! ». Aucun message AER:, PCIe Bus Error, DPC: ou faute DMAR trouvé lors de la recherche ciblée du boot. Ne pas déclarer la liaison eGPU validée avant connexion.
- Intel UHD630 i915 est le seul contrôleur graphique présent. Quadro RTX 5000 16 Go = matériel annoncé par l’utilisateur, non encore détecté ni vérifié.

## IOMMU

Noyau actif 6.18.54-1-t2-trixie. /proc/cmdline confirme intel_iommu=on iommu=pt pm_async=off. Journal : DMAR IOMMU enabled, remapping IRQ x2apic et invalidation en file activés ; domaine par défaut Passthrough. Les ponts/contrôleurs Thunderbolt partagent le groupe IOMMU2 avec les ponts hôtes concernés. Les deux attributs domain*/iommu_dma_protection valent 0 : l’activation globale IOMMU ne constitue donc pas une preuve de protection DMA Thunderbolt active. Sécurité user conservée ; aucune modification IOMMU, groupe ou autorisation.

## En-têtes, compilation et DKMS

build -> /usr/src/linux-headers-6.18.54-1-t2-trixie, Makefile, Module.symvers et include/generated/autoconf.h présents ; include/config/kernel.release = 6.18.54-1-t2-trixie. Paquet en-têtes 6.18.54-1 installé. DKMS 3.2.2-1~deb13u1 installé, dkms status vide : aucun module externe actuellement construit. GCC14.2.0-19 identique au compilateur du noyau. Environnement de compilation disponible, aucune compilation NVIDIA tentée. Images/initramfs Debian 6.12.107 et 6.12.111 conservés dans /boot.

## Pilotes candidats et limites de compatibilité

APT local : nvidia-driver, nvidia-kernel-dkms et nvidia-cuda-toolkit sans candidat. Sources trixie/security/updates limitées à main et non-free-firmware ; contrib/non-free absents, aucun dépôt NVIDIA ou backports configuré. Aucun pilote NVIDIA installé (entrées dpkg un = paquet non installé, pas une installation incomplète démontrée).

Sources primaires consultées :

- Debian stable/trixie nvidia-kernel-dkms 550.163.01-2 : https://packages.debian.org/trixie/nvidia-kernel-dkms
- Debian trixie-backports nvidia-driver 550.163.01-4~bpo13+1 : https://packages.debian.org/trixie-backports/nvidia-driver . Il reste en branche550 ; ne pas supposer que backports fournit une branche580 plus récente.
- NVIDIA580.119.02 répertorie Quadro RTX5000 dans les produits pris en charge : https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/supportedchips.html
- Modules ouverts NVIDIA pris en charge sur Turing et ultérieurs : https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/kernel_open.html
- Guide de paquets Debian NVIDIA : https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/debian.html
- CUDA fournit une cible Debian13 amd64, mais la matrice Debian consultée valide le noyau6.12, pas ce noyau T2 personnalisé : https://docs.nvidia.com/cuda/cuda-installation-guide-linux/

Conclusion de sélection initiale : branche580 candidate documentée pour le matériel Quadro RTX5000 ; version exacte et paquet DKMS à choisir après identification PCI effective, inspection des paquets/dépendances et de leur support d’API6.18. Les variantes propriétaires et ouvertes restent à comparer pour cet eGPU Turing. La branche550 Debian ne sera pas retenue automatiquement sur la seule base de sa présence dans stable/backports. Aucune source consultée ne certifie le couple exact 6.18.54-1-t2-trixie/eGPU ; compatibilité à établir par build DKMS puis chargement/test. Ne pas confondre support de la carte et compatibilité du noyau hôte. CUDA/toolkit et Container Toolkit ne sont pas installés ; pas de choix de version CUDA définitif à cette étape.

## Suite, après signal utilisateur

1. Demander le branchement et l’alimentation du premier Razer Core uniquement, avec câble Thunderbolt3 adapté, puis attendre la confirmation de connexion. Aucun second boîtier.
2. Comparer boltctl list/domains, sysfs et PCI à l’inventaire initial ; identifier UUID, fabricant/modèle et état d’autorisation. Si une autorisation est requise, présenter le périphérique exact et la différence entre autorisation de session et inscription permanente ; demander explicitement l’accord avant toute inscription permanente. Aucune commande authorize/enroll n’est exécutée actuellement.
3. Vérifier la Quadro dans PCIe, IDs/subsystem, ponts/BAR/ressources et erreurs nouvelles ; ne pas installer de pilote si GPU absent. Si le GPU reste masqué faute d’autorisation, traiter cette étape avant la sélection finale.
4. Une fois GPU reconnu, préparer le choix pilote/CUDA, dépôts et clés avec provenance, simulation APT sans suppression et examen des scripts mainteneurs (DKMS/initramfs/blacklist/display). Prévoir la conservation des deux secours et un retour arrière ciblé. Présenter le plan complet avant installation. Toute modification de GRUB/EFI ou reboot nécessite un accord spécifique.

État réseau final : enp4s0 UP 192.168.1.99/24, NetworkManager/ssh/ssh.socket actifs. Aucun réglage réseau/SSH modifié. Preuves initiales : mission04-initial-20261011/pci.log, bolt.log, noyau.log, bolt-domaines.log, bolt-peripheriques.log et dkms.log.

# JARVIS — Mission 05B-P : préparation sécurisée NVIDIA

12 octobre 2026 — Macmini8,1, Debian 13. Rapport de préparation, après lecture de mission05A.md. **Aucune installation, sauvegarde opérationnelle, compilation DKMS, activation de dépôt système, modification de service/initramfs/GRUB/EFI, chargement NVIDIA, redémarrage ou connexion du Core.** Les fichiers créés et les téléchargements d’inspection sont uniquement dans le répertoire utilisateur.

## 1. Point de décision avant toute installation

**GO technique conditionnel pour une installation contrôlée Core absent, après votre autorisation explicite.** Le candidat reste **595.91.07-1, branche R595, modules ouverts DKMS et composants de calcul**. Ce GO ne valide ni le fonctionnement réel du module, ni CUDA, ni le hotplug, ni le passage en production. Le branchement et les essais GPU restent une phase autorisée séparément.

| Décision à approuver | Résultat préparé |
|---|---|
| Version | **595.91.07-1** ; 595.104.02 production plus récent en amont mais absent du dépôt Debian 13 authentifié consulté |
| Amorçage du dépôt | **cuda-keyring=1.1-1**, clé spécifique Debian 13, source NVIDIA Debian 13 x86_64 |
| Branche | **nvidia-driver-pinning-595=595-1**, plus isolation APT proposée empêchant le dépôt de remplacer DKMS/libxnvctrl0 |
| Cibles principales | **nvidia-driver-cuda=595.91.07-1**, **nvidia-kernel-open-dkms=595.91.07-1**, **libelf-dev=0.192-4** |
| Transaction complète | **29 paquets nouveaux ; 0 mise à jour, 0 suppression, 0 paquet laissé à mettre à jour avec la politique finale** |
| Paquets existants remplacés | **Aucun dans la simulation finale** ; aucune collision de fichier existant non répertoire identifiée |
| Initramfs | Régénération du plus récent, donc **6.18.54-1-t2-trixie**, par trigger initramfs-tools ; sauvegarde à réaliser avant, non faite ici |
| DKMS | Configuration locale **autoinstall_all_kernels=yes** : construction attendue pour **6.12.111+deb13-amd64 et 6.18.54-1-t2-trixie**, installation/depmod/signature éventuelle |
| Services | Création du compte/groupe nvidia-persistenced, activation et tentative de démarrage prévues par le paquet ; **démarrage à différer par masque runtime ciblé**, puis désactivation du seul nouveau service |
| Autres effets | Blacklists nouveau/nova-core, options NVIDIA, règle udev avec runtime PM au bind, bibliothèque CUDA et cache ldconfig, utilitaire nvidia-modprobe setuid root |
| Risques résiduels | Compilation non testée, hooks initramfs, panne GSP/DMA/Thunderbolt au futur hotplug, effets de puissance, révision amont plus récente, transaction réelle pouvant différer si l’état change |
| Retour arrière | Purge des seuls 29 ajouts confirmés, retrait DKMS sur les deux noyaux, nettoyage du service/compte/pins/dépôt, traitement des clés DKMS créées et restauration conditionnelle de l’initrd sauvegardé |

**Ne rien installer sur la base de ce tableau seul : l’autorisation humaine demeure obligatoire.** Aucun changement de branche vers R610/R615 n’a été retenu.

## 2. État réel et absence du Core

Boot ID **d8f67bde-f785-4365-99ed-1af19afe9620**, noyau actif **6.18.54-1-t2-trixie**. La cmdline conserve nouveau blacklisté, intel_iommu=on, iommu=pt, pm_async=off et les réserves PCIe NP32/PREF512. Aucune modification proposée de ces paramètres.

- Intel **0000:00:02.0, 8086:3e9b**, lié à **i915**, module chargé.
- Session locale **GNOME, Wayland, Active=yes, State=active** ; processus gnome-shell et gnome-session présents.
- **SDDM, ssh.service et ssh.socket actifs**, unités enabled ; session SSH effective pendant l’investigation.
- Aucun GPU **10de:1eb0** ni aucune autre fonction NVIDIA dans l’inventaire PCIe. Les contrôleurs Thunderbolt internes restent présents ; sysfs Thunderbolt ne montre que les domaines et routeurs hôtes **0-0 / 1-0**, aucun périphérique externe. **Core absent de l’inventaire : condition de poursuite satisfaite.** Cela atteste l’inventaire, pas une observation physique du câble.
- Headers **linux-headers-6.18.54-1-t2-trixie 6.18.54-1**, lien build correct, kernel.release exact. Makefile, Module.symvers, autoconf.h, utsrelease.h et scripts/sign-file présents. Le header **include/soc/tegra/bpmp-abi.h** est présent aussi.
- GCC/G++ **14.2.0-19**, identiques au compilateur déclaré du noyau ; make **4.4.1-2**, build-essential **12.12**, DKMS Debian **3.2.2-1~deb13u1**. État DKMS vide.
- **SecureBoot disabled**, lockdown **none**, MODULE_SIG_FORCE désactivé ; MODULE_SIG, MODVERSIONS, ZONE_DEVICE et HMM_MIRROR activés. Aucune opération MOK/EFI nécessaire dans cet état observé.
- Espace libre au relevé : environ **397 Gio sur /** et **604 Mio sur /boot**. Cette marge autorise la préparation ; elle ne dispense pas d’un contrôle avant la transaction réelle et d’une surveillance de la taille du nouvel initrd.

Preuves : `etat.txt`, `headers-et-services.txt`, `boot-hashes.txt`. Les empreintes de GRUB, noyau et initrd concordent avec les références antérieures : grub.cfg **9bc2c064…**, vmlinuz **a41e1a76…**, initrd **4c7fe763…** ; valeurs complètes dans la preuve.

## 3. Versions et sécurité recontrôlées

Le dépôt officiel **Debian 13/x86_64**, signé, fournit toujours :

| Branche | Révisions de nvidia-driver-cuda / nvidia-kernel-open-dkms observées |
|---|---|
| R590 | 590.44.01-1, 590.48.01-1 |
| **R595** | 595.45.04-1, 595.58.03-1, 595.71.05-1, **595.91.07-1** |
| R610 | 610.43.02-1, 610.57.04-1 |
| R615 | 615.71.09-1, 615.71.09-2 |

**595.104.02** est une révision production publiée le **22 septembre 2026**, dans la même branche R595. Ses notes mentionnent un correctif d’allocation de tables de pages GPU supérieures à 2 Gio et un correctif Vulkan/Wayland sur les métadonnées HDR. Le premier peut concerner le calcul ; le second n’est pas un motif de déplacer GNOME sur NVIDIA. Son absence de l’index signé Debian 13 empêche de proposer `apt install …=595.104.02` comme commande disponible. Ne pas la substituer avec un .run, des bibliothèques d’une autre branche ou un dépôt Debian 12. [Notes officielles 595.104.02](https://www.nvidia.com/en-us/drivers/details/279807/), [branche production annoncée](https://forums.developer.nvidia.com/t/current-graphics-driver-releases/28500).

**Sécurité :** le bulletin officiel **30 septembre 2026, ID 5861**, indique pour **NVIDIA RTX PRO/RTX/Quadro, Linux, R595** les versions **antérieures à 595.91.07** comme affectées et **595.91.07** comme version mise à jour. Le candidat satisfait donc le seuil de correction de ce bulletin, contrairement aux premières révisions R595 du dépôt. Le bulletin de mai 2026 fixait auparavant le seuil R595 à 595.71.05. Cette vérification corrige la limite documentaire laissée en 05A ; elle n’est pas une garantie d’absence de toute vulnérabilité ou de toute publication future. Aucun bulletin GPU plus récent applicable n’a été identifié lors du contrôle. [Bulletin NVIDIA septembre 2026](https://nvidia.custhelp.com/app/answers/detail/a_id/5861/~/security-bulletin:-nvidia-gpu-display-driver---september-2026), [bulletin mai 2026](https://nvidia.custhelp.com/app/answers/detail/a_id/5821/).

**Recommandation maintenue : 595.91.07-1 pour un premier essai contrôlé**, à recontrôler le jour de l’installation. Si 595.104.02 ou une autre révision R595 entre dans ce dépôt, recommencer la simulation et l’audit des paquets ; aucune adoption automatique. L’installation n’est pas une démonstration de compatibilité opérationnelle.

## 4. Authenticité du dépôt, keyring et politiques APT

`cuda-keyring_1.1-1_all.deb` a été téléchargé puis **décompressé pour inspection**, sans dpkg -i. Contenu pertinent :

- `/usr/share/keyrings/cuda-archive-keyring.gpg` ; clé **RSA 4096**, identifiant **97A5D4CB8793F200**.
- Empreinte complète : **02182E60104FCDC26EAE1B8597A5D4CB8793F200**.
- `/etc/apt/sources.list.d/cuda-debian13-x86_64.list`, déclaré conffile, avec **signed-by=/usr/share/keyrings/cuda-archive-keyring.gpg** et URL Debian 13.
- Postinst : recherche une ancienne clé 7FA2AF80 et affiche, si elle existe, une instruction de retrait. **Il ne l’exécute pas et ne lance pas apt update.** Pas de postrm spécifique trouvé ; fichiers/conffile supprimables par purge dpkg.

La clé **8793F200** est bien celle publiée par NVIDIA pour Debian 13 ; ne pas reprendre par habitude la clé **3BF863CC** des anciens dépôts Debian 12/Ubuntu. [Gestion officielle des clés](https://github.com/NVIDIA/cuda-repo-management).

**Vérifications faites hors système :** APT isolé accepte InRelease sans option d’affaiblissement. `gpgv` retourne **0**, GOODSIG/VALIDSIG pour l’empreinte ci-dessus ; signature du **9 octobre 2026**. Le SHA-256 du fichier Packages correspond à l’InRelease signé, et les **29 .deb** de la transaction correspondent aux SHA-256 des index authentifiés. Le keyring lui-même concorde aussi avec le hash Packages. Le bootstrap de confiance repose sur HTTPS officiel et la clé officielle, pas sur une certification indépendante hors réseau. Aucune clé importée dans le système, aucun trusted=yes, allow-insecure, contournement sqv ou apt-key employé.

**Pin de branche inspecté :** nvidia-driver-pinning-595 **595-1** installe `/etc/apt/preferences.d/nvidia-driver-pin`, priorité **1000**, familles sources NVIDIA version 595*, y compris modules, outils et métapaquets. Ce pin n’a aucun script de maintenance ; il autorise les futures microversions 595.

**Risque de dépôt identifié et traité dans la proposition :** avant isolation supplémentaire, le dépôt NVIDIA rendait candidats **DKMS 3.4.3-1** et **libxnvctrl0 595.91.07-1**, alors que la machine utilise DKMS Debian 3.2.2 et libxnvctrl0 535.171.04-1+b2. Ils ne faisaient pas partie de l’installation demandée, mais pouvaient être proposés lors d’une mise à jour globale.

Le fichier **00-jarvis-nvidia-isolation**, à créer seulement après accord, prévoit :

```text
Package: dkms libxnvctrl0
Pin: origin developer.download.nvidia.com
Pin-Priority: -1

Package: *
Pin: origin developer.download.nvidia.com
Pin-Priority: 100
```

**Ordre important, vérifié avec APT :** ce fichier doit être lu **avant** nvidia-driver-pin dans preferences.d. Aucune règle de branche préalable dans `/etc/apt/preferences` ; ce fichier est absent actuellement. Une première disposition de test où la règle de branche était lue d’abord n’empêchait pas la promotion libxnvctrl0 ; elle a été corrigée dans l’environnement utilisateur. La politique finale maintient les candidats DKMS/libxnvctrl0 à leurs versions locales tout en sélectionnant NVIDIA 595.91.07-1.

**Dépôt supplémentaire envisagé : uniquement NVIDIA Debian 13.** La résolution finale a été refaite **sans contrib** : aucune dépendance de cette transaction n’en a besoin. Le conseil générique du guide NVIDIA d’activer contrib n’est donc pas appliqué sans nécessité. Aucun backports, sid, non-free Debian ou dépôt d’une autre distribution à ajouter. Les sources Debian main/non-free-firmware actuelles restent la référence.

## 5. Simulation APT complète réalisée hors système

Une configuration APT privée a été créée sous **mission05B-P-preuves/apt-isole/**. Elle utilise :

- sources, préférences, listes, caches et logs **dans ce répertoire utilisateur** ;
- lecture de `/var/lib/dpkg/status` et des états APT existants pour résoudre avec les paquets réellement installés ;
- main/non-free-firmware des trois suites déjà utilisées et le dépôt NVIDIA ;
- les keyrings Debian et NVIDIA explicitement référencés ;
- aucun chargement des snippets APT système et **aucun hook PackageKit/AppStream/dpkg** de la machine ;
- exécution utilisateur, sans sudo, architecture amd64, recommandations désactivées.

Les `apt-get update --error-on=any` effectués ici concernent **exclusivement ces index privés**. **Aucun index /var/lib/apt/lists ni source /etc/apt n’a été modifié.** L’opération est un téléchargement d’inspection hors système permis par la mission, pas une activation du dépôt. La comparaison de **53 fichiers système lisibles** (état dpkg/APT, index et configuration APT) a donné **zéro modification** ; contrôles finaux à nouveau consignés, également sans différence. La syntaxe du texte de sauvegarde a été vérifiée avec **bash -n, retour 0**, sans l’exécuter.

La commande de résolution, en mode `-s -V --no-install-recommends`, comprend le keyring local, le pin de branche, libelf-dev et les deux cibles NVIDIA avec versions imposées. **Simulation finale : retour 0, 0 upgraded, 29 newly installed, 0 to remove, 0 not upgraded.** Aucun code de paquet, build, trigger ni service exécuté par la simulation. APT rappelle que le verrouillage est désactivé en simulation : recontrôler l’état au moment réel.

### Liste exacte de la transaction

| Paquet nouveau | Version exacte | Origine |
|---|---|---|
| cuda-keyring | `1.1-1` | NVIDIA Debian 13 |
| firmware-nvidia-gsp | `595.91.07-1` | NVIDIA Debian 13 |
| libcuda1 | `595.91.07-1` | NVIDIA Debian 13 |
| libcudadebugger1 | `595.91.07-1` | NVIDIA Debian 13 |
| libelf-dev | `0.192-4` | Debian trixie/main |
| libnvcuvid1 | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-cfg1 | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-encode1 | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-fbc1 | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-gpucomp | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-ml1 | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-nvvm4 | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-nvvm704 | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-opticalflow1 | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-pkcs11-openssl3 | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-present | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-ptxjitcompiler1 | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-sandboxutils | `595.91.07-1` | NVIDIA Debian 13 |
| libnvidia-tileiras | `595.91.07-1` | NVIDIA Debian 13 |
| libnvoptix1 | `595.91.07-1` | NVIDIA Debian 13 |
| libzstd-dev | `1.5.7+dfsg-1` | Debian trixie/main |
| nvidia-driver-cuda | `595.91.07-1` | NVIDIA Debian 13 |
| nvidia-driver-pinning-595 | `595-1` | NVIDIA Debian 13 |
| nvidia-kernel-open-dkms | `595.91.07-1` | NVIDIA Debian 13 |
| nvidia-kernel-support | `595.91.07-1` | NVIDIA Debian 13 |
| nvidia-modprobe | `595.91.07-1` | NVIDIA Debian 13 |
| nvidia-opencl-icd | `595.91.07-1` | NVIDIA Debian 13 |
| nvidia-persistenced | `595.91.07-1` | NVIDIA Debian 13 |
| zlib1g-dev | `1:1.3.dfsg+really1.3.1-1+b1` | Debian trixie/main |

Les **26 ajouts NVIDIA** comprennent keyring et pin ; les **3 ajouts Debian** sont libelf-dev, libzstd-dev et zlib1g-dev. Dépendances majeures : DKMS ouvert nécessite **DKMS ≥3.1.8**, g++ et **firmware-nvidia-gsp=595.91.07-1** ; le DKMS existant satisfait cette contrainte. Les bibliothèques NVIDIA et le firmware sont verrouillés par dépendances exactes. `nvidia-driver-cuda` fournit nvidia-smi ; pas de nvidia-driver graphique complet, libGL/EGL/Vulkan NVIDIA ou xserver-xorg-video-nvidia dans la transaction. La recommandation libcuda1:i386 est **non installée**, aucun ajout multiarch.

Aucun paquet nouveau ne requiert de mise à jour d’une bibliothèque déjà installée dans cette résolution. L’analyse des listes de fichiers des 29 .deb n’a trouvé **aucun fichier existant non répertoire à écraser**. Ce contrôle complète la résolution APT ; il ne prouve pas qu’aucun script ne modifiera un fichier généré comme initrd ou ld.so.cache.

**Composants protégés :** aucun linux-image, linux-headers, paquet Mesa/libdrm/Intel, GNOME, SDDM, OpenSSH, firmware Apple/T2 ou module t2bce remplacé/supprimé. i915 est un module du noyau conservé. Aucun restart SDDM/SSH ni écriture GRUB/EFI dans les scripts des paquets examinés. Les hooks de maintenance génériques de la machine ont également été lus : apt-listchanges, debconf et notification PackageKit ; pas de needrestart installé identifié. Ils justifient de surveiller la transaction réelle, sans lancer de mise à jour globale.

## 6. Audit des scripts et effets persistants

Les **29 archives** ont été téléchargées (~255 Mo), leurs scripts et fichiers de configuration inspectés sans exécution. Les **26 fichiers scripts/triggers** trouvés sont regroupés dans `scripts-maintenance-complets.txt` ; données et listes par paquet dans `controles/`.

| Paquet / mécanisme | Installation réelle attendue | Retrait / limite |
|---|---|---|
| cuda-keyring | Installe keyring et source signée ; affiche éventuellement un avertissement ancienne clé | Purge retire fichiers/conffile ; aucun retrait automatique d’une autre clé |
| nvidia-driver-pinning-595 | Installe le pin source/version 595 à priorité 1000 | Purge du fichier ; conserver le pin d’isolation jusqu’au retrait du driver |
| nvidia-kernel-open-dkms | Postinst appelle `/usr/lib/dkms/common.postinst` : add, build, install, depmod, signature éventuelle | Prerm appelle `dkms remove -m nvidia -v 595.91.07 --all` ; ne pas supprimer d’autres modules |
| nvidia-kernel-support | Installe nvidia.conf et 60-nvidia.rules ; postinst configure appelle update-initramfs -u | Postrm **purge** appelle aussi update-initramfs -u ; conffile et règle retirés |
| Bibliothèques NVIDIA | Installent CUDA/NVML et autres bibliothèques ; triggers **activate-noawait ldconfig** | Le retrait provoque aussi des traitements du cache de bibliothèques ; pas de remplacement Mesa dans cette sélection |
| firmware-nvidia-gsp | Installe `/lib/firmware/nvidia/595.91.07/gsp_tu10x.bin` et gsp_ga10x.bin | Pas de script de maintenance propre identifié |
| nvidia-persistenced | Crée compte/groupe système ; deb-systemd-helper unmask/enable ; daemon-reload ; tentative start (ou restart en upgrade) | Prerm stop ; postrm remove daemon-reload ; purge nettoie les états helper. **Compte/groupe non supprimés par ces scripts** |
| nvidia-driver-cuda | Outils de calcul ; preset activant la persistance | Retrait du preset ; nettoyage effectif du service par son paquet |
| nvidia-modprobe | Installe le helper **setuid root, mode 4755** | Retrait du binaire par purge ; ses appels peuvent charger le module/créer les nœuds |
| 3 bibliothèques de développement Debian | Ajout fichiers de développement | Aucun script de maintenance propre trouvé dans ces .deb |

### Modprobe / udev / puissance

`/etc/modprobe.d/nvidia.conf` ajoute blacklist nouveau et **nova-core**, ainsi que **NVreg_TemporaryFilePath=/var/tmp, NVreg_EnableS0ixPowerManagement=1, NVreg_PreserveVideoMemoryAllocations=1**. Ce sont des réglages NVIDIA, pas i915. Ils n’ont pas été appliqués en 05B-P.

`60-nvidia.rules` appelle nvidia-modprobe sur événement add/bind du périphérique nvidia ; lors du bind d’un GPU 10de VGA/3D, elle écrit **power/control=auto**, puis **on** à l’unbind. **Le futur hotplug comportera donc une politique runtime PM du paquet**, même sans réglage manuel. Ne pas la masquer dans le protocole et ne pas affirmer que les réglages de puissance demeurent tous inchangés. Aucun réglage PM correctif ajouté ici.

### DKMS : deux noyaux, signature et absence de chargement automatique direct

Le fichier local **/etc/dkms/framework.conf.d/autoinstall_all_kernels.conf** contient `autoinstall_all_kernels="yes"`. Les deux répertoires build utilisables correspondent à **6.12.111+deb13-amd64** et **6.18.54-1-t2-trixie** ; la construction automatique couvrira donc les deux, même Core absent. Le noyau 6.12.107 n’a pas de lien build et n’est pas une cible DKMS disponible dans ce relevé.

Les flags **modprobe_on_install** et **post_transaction** ne sont pas activés dans la configuration locale. La branche DKMS qui ferait un modprobe de tous les modalias/restart systemd-modules-load n’est donc pas attendue. **Cela ne suffit pas à garantir zéro chargement NVIDIA : la persistance et le helper peuvent le déclencher séparément.** La proposition différera explicitement le démarrage du service.

DKMS peut créer **/var/lib/dkms/mok.key et mok.pub** et signer les modules avec scripts/sign-file. Le répertoire DKMS est vide avant la transaction ; il faut journaliser les fichiers créés. Signature locale n’implique pas enrôlement MOK : **aucun mokutil --import ni changement NVRAM/EFI** proposé.

### Initramfs et GRUB

L’outil local **update-initramfs 0.148.4** diffère des anciennes versions utilisant des stamps : son choix est fondé sur les versions disposant d’un initrd. `update_initramfs=yes`, `backup_initramfs=no`. La version la plus élevée est **6.18.54-1-t2-trixie**.

Dans un maintscript dpkg, `update-initramfs -u` active normalement un **trigger différé** ; le postinst initramfs-tools le traite ensuite réellement. La génération peut donc avoir lieu **après** la construction DKMS et incorporer les nouveaux fichiers selon les hooks/règles MODULES=most. Il faut inspecter le résultat, pas supposer que l’initrd ne contiendra aucun NVIDIA. **Pas de sauvegarde durable automatique à attendre**, d’où la sauvegarde manuelle proposée.

`update-initramfs` peut appeler /etc/initramfs/post-update.d ; **ce répertoire est absent sur cette machine**. Les hooks update-grub existent dans /etc/kernel/postinst.d, mais aucun paquet noyau n’est installé/modifié par cette transaction. Aucun appel GRUB/EFI attendu par le chemin inspecté ; contrôler leurs empreintes après. L’absence d’un hook actuel n’est pas une permission de lancer un hook nouveau.

## 7. Compatibilité Quadro / GSP / API noyau

La Quadro RTX 5000 **Turing, PCI 1EB0, CC 7.5**, est explicitement listée dans les sources NVIDIA 595.91.07. Le module ouvert NVIDIA est distinct de nouveau ; firmware GSP et bibliothèques de même version sont indispensables. Le paquet firmware fournit effectivement **gsp_tu10x.bin** pour Turing. Ne pas désactiver GSP avec le module ouvert. [Sources et matériel NVIDIA 595](https://github.com/NVIDIA/open-gpu-kernel-modules/blob/595.91.07/README.md), [GSP 595](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/gsp.html).

Le paquet DKMS exact inspecté contient :

- conftest détectant le second argument de **get_dev_pagemap**, retiré dans Linux 6.18 ;
- wrapper dans **kernel-open/common/inc/nv-linux.h** appelant l’API à un ou deux arguments selon le résultat ;
- Kbuild basé sur **ccflags-y** ;
- les cinq modules nvidia, nvidia-modeset, nvidia-drm, nvidia-peermem, nvidia-uvm ;
- headers du noyau actuel avec ZONE_DEVICE/HMM actifs, dépendances de développement cohérentes et GCC exact.

Ces constats sont des preuves statiques d’adaptation à 6.18, **pas une compilation ni une validation du binaire T2**. Aucun patch local supplémentaire, aucune copie de module d’un autre noyau ou contournement de contrôle GCC proposé. Pas de préférence générale pour le propriétaire sur ce Turing : NVIDIA recommande l’ouvert pour les GPU compatibles ; garder le propriétaire uniquement comme nouvel essai de repli motivé et séparément autorisé. [Manuel des variantes 595](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/kernel_open.html).

## 8. Sauvegarde préparée, non exécutée

Le fichier **mission05B-P-preuves/sauvegarde-proposee.sh** est un texte de procédure **non exécuté**. Il créerait, après accord, un dossier daté en mode 0700 et couvrirait : versions/états dpkg, paquets manuels/holds, état des services, compte/groupe NVIDIA initial, état DKMS, configurations APT/modprobe/modules-load/DKMS/systemd/initramfs/kernel/X11, états deb-systemd-helper, **tous les initrd existants** et leurs empreintes avec GRUB/noyaux.

Il conserve une copie dpkg-status pour diagnostic/comparaison : **ne pas la restaurer à la place d’une vraie désinstallation**. Les archives peuvent contenir des clés DKMS privées si elles existent au moment réel ; permissions restrictives et aucun affichage de leur contenu. La sauvegarde n’est pas présente aujourd’hui : **à exécuter et vérifier avant la première modification**.

La transaction simulée n’actualise aucun paquet existant : aucun .deb ancien n’est requis pour un downgrade dans ce plan. Si la simulation réelle propose une mise à jour, arrêter et préparer sa récupération avant accord. Ne pas élargir silencieusement le rollback.

## 9. Commandes proposées pour l’installation autorisée

**Les commandes de cette section n’ont pas été exécutées.** Elles sont ordonnées et destinées à une session SSH avec Core toujours absent. Les 29 archives inspectées sont disponibles dans `mission05B-P-preuves/debs/`, leurs SHA-256 vérifiés. Ne pas utiliser la configuration APT d’inspection pour installer réellement.

### A. Vérifier puis sauvegarder

Reprendre les contrôles noyau/Core/i915/SDDM/SSH/Secure Boot, puis exécuter seulement après autorisation :

```bash
bash /home/adminjarvis/JARVIS/rapports/mission05B-P-preuves/sauvegarde-proposee.sh
```

Vérifier les copies, archives et empreintes, et conserver le chemin daté retourné. Ne pas poursuivre avec une sauvegarde incomplète.

### B. Installer la clé et les politiques de sélection

Créer le **seul** nouveau pin d’isolation depuis le texte revu, puis installer keyring et pin de branche inspectés :

```bash
sudo install -m 0644 /home/adminjarvis/JARVIS/rapports/mission05B-P-preuves/pinning-isolation-propose.txt /etc/apt/preferences.d/00-jarvis-nvidia-isolation
sudo dpkg -i /home/adminjarvis/JARVIS/rapports/mission05B-P-preuves/debs/cuda-keyring_1.1-1_all.deb /home/adminjarvis/JARVIS/rapports/mission05B-P-preuves/debs/nvidia-driver-pinning-595_595-1_all.deb
sudo apt-get update
apt-cache policy dkms libxnvctrl0 nvidia-driver-cuda nvidia-kernel-open-dkms
```

Cette future activation est persistante et demande l’accord ; elle n’a pas eu lieu en 05B-P. Exiger signatures sans erreur, candidats DKMS/libxnvctrl0 inchangés et branch R595. Aucun ajout contrib proposé. Aucun apt upgrade/dist-upgrade.

### C. Simuler une dernière fois et différer la persistance

Le fichier **installation-paquets-exacts.txt** contient les **27 autres ajouts avec =version**, tous listés au §5 ; keyring/pin sont déjà traités à l’étape B.

```bash
xargs -r -a /home/adminjarvis/JARVIS/rapports/mission05B-P-preuves/installation-paquets-exacts.txt apt-get -s -V --no-install-recommends --no-remove install
```

Attendre maintenant **27 nouveaux paquets, aucun autre changement**. Arrêter en cas d’écart, erreur ou de version disparue. APT --no-remove empêche les suppressions ; **il n’empêche pas à lui seul toutes les mises à jour**, d’où la revue du plan.

Avant installation des composants :

```bash
sudo systemctl mask --runtime nvidia-persistenced.service
```

C’est une modification runtime du **seul service nouveau**, proposée pour éviter sa tentative de démarrage pendant l’installation. L’audit du deb-systemd-helper installé montre que son unmask manipule ses masques dans **/etc**, pas ce masque **/run**. Le postinst peut cependant créer ses liens d’activation sous-jacents : ils seront retirés à l’étape E. Si le masque échoue ou si un service/masque préexiste désormais, arrêter et revoir sa préservation, sans écraser un état antérieur.

### D. Installer — construction automatique déjà incluse

```bash
sudo env CC=/usr/bin/gcc-14 CXX=/usr/bin/g++-14 xargs -r -a /home/adminjarvis/JARVIS/rapports/mission05B-P-preuves/installation-paquets-exacts.txt apt-get --no-install-recommends --no-remove install
```

Enregistrer la sortie complète depuis SSH. **Cette commande déclenche déjà les builds DKMS et les scripts** : il ne faut pas la présenter comme un simple déploiement de fichiers qui attendrait une autorisation de compiler ensuite. Le masque de persistance n’interdit pas toute action imaginable d’un futur paquet ; ici les scripts exacts et DKMS local ont été inspectés.

### E. Contrôler et terminer la phase Core absent

```bash
/usr/sbin/dkms status
/usr/sbin/modinfo -k 6.18.54-1-t2-trixie -F version nvidia
/usr/sbin/modinfo -k 6.18.54-1-t2-trixie -F vermagic nvidia
/usr/sbin/modinfo -k 6.18.54-1-t2-trixie -F license nvidia
/usr/sbin/modinfo -k 6.18.54-1-t2-trixie -F signer nvidia
/usr/sbin/modinfo -k 6.18.54-1-t2-trixie nvidia_uvm
systemctl status nvidia-persistenced --no-pager
lsmod
lspci -Dnnk -s 0000:00:02.0
systemctl is-active sddm ssh ssh.socket
loginctl list-sessions
sudo sha256sum /boot/grub/grub.cfg /boot/vmlinuz-6.18.54-1-t2-trixie /boot/initrd.img-6.18.54-1-t2-trixie
```

Exiger **nvidia/595.91.07 installed** pour le noyau T2 exact et contrôler aussi la cible 6.12.111 ; version **595.91.07**, vermagic contenant **6.18.54-1-t2-trixie**, licence **Dual MIT/GPL**, modules installés dans updates/dkms et firmware présent. Aucun module NVIDIA chargé attendu dans cette phase ; si lsmod en montre un, documenter et arrêter sans retrait forcé. **Ne pas appeler nvidia-smi ou nvidia-modprobe comme test sans Core : ils peuvent déclencher un chargement.**

Lire le make.log réel sous `/var/lib/dkms/nvidia/595.91.07/` et le journal de la transaction. Inspecter le nouvel initrd avec `/usr/bin/lsinitramfs /boot/initrd.img-6.18.54-1-t2-trixie`, sans le modifier. Comparer conservation i915, stockage/LVM/T2 et ajout des fichiers NVIDIA ; le seul hash différent ne qualifie pas le contenu. GRUB et noyau doivent conserver leurs empreintes ; boot ID et cmdline doivent rester ceux de la phase initiale.

Si un build manque, diagnostiquer **avant toute répétition**. Commandes DKMS explicites préparées, non à ajouter automatiquement après un succès :

```bash
sudo env CC=/usr/bin/gcc-14 CXX=/usr/bin/g++-14 /usr/sbin/dkms build -m nvidia -v 595.91.07 -k 6.18.54-1-t2-trixie
sudo env CC=/usr/bin/gcc-14 CXX=/usr/bin/g++-14 /usr/sbin/dkms install -m nvidia -v 595.91.07 -k 6.18.54-1-t2-trixie
```

Après contrôles réussis, garder la persistance désactivée au boot et enlever uniquement le masque runtime créé pour cette transaction :

```bash
sudo systemctl disable --now nvidia-persistenced.service
sudo systemctl unmask --runtime nvidia-persistenced.service
systemctl is-enabled nvidia-persistenced.service
systemctl is-active nvidia-persistenced.service
```

Attendus **disabled / inactive** (codes non nuls usuels pour inactive). Pas d’activation automatique du daemon au démarrage sans Core. Aucune modification SDDM/SSH/Intel. Le démarrage éventuel du daemon après hotplug sera une décision de la phase suivante. Pas de redémarrage inclus dans cette procédure ; si nécessaire, arrêter et demander un accord séparé.

## 10. Hotplug et validation CUDA — protocole séparé NON EXÉCUTÉ

**NO-GO pour le hotplug à ce stade documentaire : il attend installation validée puis autorisation distincte.**

Préconditions : Core absent, boot ID stable, bureau Intel fonctionnel, deux accès SSH, journal capturé sur le poste distant, aucune charge GPU. Ne pas lancer Ollama avant l’inventaire GPU validé.

Après connexion physique autorisée, lire lspci par **10de:1eb0**, conserver son BDF réel (pas 81:00.0 supposé), contrôler les erreurs noyau et la conservation d’i915. Les règles udev peuvent charger nvidia et modifier son power/control au bind ; ce fait appartient au test autorisé, pas à la phase actuelle.

```bash
lspci -Dnnk -d 10de:1eb0
lsmod
nvidia-smi -L
nvidia-smi --query-gpu=name,uuid,pci.bus_id,driver_version,memory.total --format=csv
nvidia-smi -q
sudo journalctl -k -b --no-pager
lspci -Dnnk -s 0000:00:02.0
```

Attendre Quadro RTX 5000, pilote **595.91.07**, firmware GSP cohérent et VRAM nominale 16 Go. Si UVM/nœuds manquent, actions **supplémentaires du protocole autorisé** : `sudo /usr/sbin/modprobe nvidia_uvm` ou `sudo nvidia-modprobe -u` ; aucune exécution ici. Le test Driver API Python sans Toolkit préparé en **mission05A §9** reste applicable : cuInit, comptage, nom et CC **7.5**. Il ne valide pas un kernel de calcul.

Valider ensuite une charge CUDA courte via un outil revu ou l’inférence Ollama d’une mission séparée. Pas d’installation du Toolkit complet pour cela. nvidia-smi à vide ne garantit pas une charge stable. Arrêt du protocole sur Xid, AER fatal, timeout GSP, DMAR nouveau, GPU fallen off the bus, perte SSH ou régression HDMI ; aucun reset/rescan/écriture PCI ou correction PM improvisée. **Aucun retrait à chaud pendant utilisation** ; NVIDIA ne garantit pas la stabilité du hot-unplug. [Documentation eGPU](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/egpu.html).

Intel reste le GPU d’affichage : pas de nvidia-xconfig, PrimaryGPU NVIDIA, offload GNOME ou modification i915. Vérifier les clients GPU et le compositeur, pas seulement la présence d’i915. Ollama sera installé manuellement/versionné après validation, sans script susceptible d’installer cuda-drivers ou de changer les dépôts.

## 11. Retour arrière précis, également NON EXÉCUTÉ

Le manifeste **retrait-paquets-exacts.txt** contient les **29 ajouts attendus**, un paquet par ligne. Il doit être confronté au journal et à la sauvegarde avant exécution : retirer seulement ce qui a réellement été ajouté, aucun paquet devenu préexistant ou installé indépendamment entre-temps. Pas de wildcard nvidia*, pas d’autoremove général, pas de restauration brute du statut dpkg.

1. **Core absent pour le rollback de la phase d’installation.** Si Core connecté après essai ultérieur, arrêter les clients et établir une récupération autorisée ; aucune déconnexion/reboot implicite.
2. Si créé, laisser/remettre le masque runtime du seul service nvidia-persistenced et arrêter seulement ce service nouveau. Aucun restart du bureau/réseau.
3. Lire les états dpkg/DKMS puis simuler la purge des seuls ajouts confirmés :

```bash
sudo xargs -r -a /home/adminjarvis/JARVIS/rapports/mission05B-P-preuves/retrait-paquets-exacts.txt apt-get -s purge
```

La simulation de retrait devra être faite sur **l’état réellement installé**, pas sur la machine actuelle où ces paquets sont absents. Exiger aucune suppression GNOME/SDDM/SSH/Mesa/noyau/T2. Une installation DKMS partiellement échouée peut laisser des paquets unpacked/half-configured : **ne pas lancer apt --fix-broken install ou dpkg --configure -a aveuglément**, qui peuvent relancer les builds. Préférer une purge ciblée revue.

4. Après approbation du retrait exact :

```bash
sudo xargs -r -a /home/adminjarvis/JARVIS/rapports/mission05B-P-preuves/retrait-paquets-exacts.txt apt-get purge
/usr/sbin/dkms status
```

Le prerm DKMS retire nvidia/595.91.07 **sur les deux noyaux** et traite depmod. Si une entrée orpheline reste, commande préparée seulement après diagnostic : `sudo /usr/sbin/dkms remove -m nvidia -v 595.91.07 --all`. Ne pas enlever le DKMS Debian préexistant ni ses autres modules.

5. Contrôler le retrait de nvidia.conf, 60-nvidia.rules, firmware 595, bibliothèques et presets ; les scripts de purge peuvent déclencher **ldconfig et update-initramfs**. Le postrm du support traite initramfs **à purge**, pas simplement remove. Pas de suppression de la blacklist nouveau de la cmdline : elle existait avant.
6. Retirer **uniquement /etc/apt/preferences.d/00-jarvis-nvidia-isolation**, fichier explicitement créé par la procédure, après retrait des paquets. La purge pin/keyring retire leurs fichiers, dont la source NVIDIA/keyring ; vérifier les résidus. Aucun fichier contrib créé à supprimer. `apt-get update` système pour retrait des anciens index serait une opération future autorisée, pas nécessaire à cette mission.
7. Les scripts de nvidia-persistenced ne suppriment pas le compte/groupe. Si leur absence initiale est confirmée par la sauvegarde, après purge et contrôle qu’ils ne servent plus : **deluser --system nvidia-persistenced**, puis **delgroup --system nvidia-persistenced** seulement si le groupe subsiste. Pas de --remove-home général ; le service a son répertoire runtime. Retirer le masque runtime créé : `sudo systemctl unmask --runtime nvidia-persistenced.service`.
8. Les clés DKMS/signatures et logs peuvent subsister dans /var/lib/dkms. Les comparer à la sauvegarde ; **conserver les clés si une autre utilisation est apparue**, sinon retirer seulement les artefacts créés et confirmés non partagés. Aucun enrôlement MOK n’ayant été proposé, aucun changement NVRAM à annuler.
9. Le nouvel initrd doit rester complet pour LVM/T2/i915. Si besoin d’un retour **binaire** à la référence stable, et seulement si aucun autre changement de noyau/firmware/initramfs n’est intervenu, restaurer la copie **initrd.img-6.18.54-1-t2-trixie** du dossier daté sur le chemin /boot correspondant, avec permissions préservées, puis comparer son SHA-256 à **4c7fe763f3f05300e03c270aa24d2c5b90a55cbd26547898a3c1ca3f44507cc0**. Ne pas restaurer globalement /boot ni exécuter update-grub. Les autres initrd sauvegardés couvrent un effet inattendu éventuel, sans restauration automatique.
10. Vérifier dpkg sain, aucune entrée DKMS NVIDIA, inventaire Intel inchangé, SDDM/SSH/GNOME fonctionnels, GRUB/noyau inchangés. La purge n’enlève pas automatiquement un module déjà chargé : ne pas forcer rmmod si occupé. Une remise à zéro runtime peut nécessiter un reboot **séparément autorisé**.

Les sauvegardes doivent exister avant que ce rollback soit utilisable. Aucun retour arrière n’est nécessaire actuellement : rien n’a été installé/modifié.

## 12. Preuves, limites et recommandation finale

Dossier **/home/adminjarvis/JARVIS/rapports/mission05B-P-preuves/** : état local, empreintes, index signé, clé, signature gpgv, configuration isolée, simulations initiale/finale, politique finale, transaction JSON/TSV, 29 .deb contrôlés, scripts/configurations, adaptation API, collisions, sauvegarde proposée non exécutée, manifestes installation/retrait et SHA256SUMS.

**Limites restantes :** aucune compilation, aucun module NVIDIA chargé, aucune exécution GSP/CUDA/Thunderbolt avec pilote. La simulation ne teste pas les scripts et ne garantit pas l’état futur ; l’audit statique leur donne une portée explicite mais ne remplace pas le suivi de l’installation. 595.104.02 contient des correctifs supplémentaires absents du candidat APT : version à réévaluer si sa disponibilité change. L’initrd régénéré doit être vérifié avant tout redémarrage futur. Le masquage Intel Core présent au démarrage reste hors scope.

**Recommandation finale : GO conditionnel pour la seule installation Core absent, avec sauvegarde préalable vérifiée, politiques APT exactes, démarrage de persistance différé et contrôles DKMS/bureau. Aucune action d’installation ne sera engagée sans votre autorisation explicite. NO-GO pour le branchement et la validation opérationnelle GPU avant réussite de cette phase puis accord séparé.**

> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission05A.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 05A : sélection du pilote NVIDIA pour le serveur IA

Date : 12 octobre 2026, Europe/Paris. Macmini8,1, Debian 13, noyau `6.18.54-1-t2-trixie`. Mission documentaire : lectures locales, consultation des sources officielles et téléchargement de métadonnées/paquets **pour inspection dans le répertoire de preuves seulement**. Aucun paquet installé, aucun script de maintenance exécuté, aucun module chargé, aucun dépôt système modifié, aucune compilation, aucun changement initramfs/GRUB/EFI, aucun redémarrage ou branchement.

## 1. Décision proposée

**Candidat recommandé : NVIDIA 595.91.07-1 du dépôt NVIDIA Debian 13, modules ouverts via `nvidia-kernel-open-dkms`, composants de calcul via `nvidia-driver-cuda`.** Recommandation conditionnelle : compilation DKMS réussie pour le noyau exact, cohérence des bibliothèques/firmware/modules, puis validation CUDA et hotplug. **La compatibilité opérationnelle avec 6.18.54 T2Linux n’est pas encore démontrée.**

La Quadro RTX 5000 Turing `10de:1eb0`, compute capability **7.5**, est explicitement prise en charge. Les sources 595 comprennent des adaptations aux API de Linux 6.18. Le choix du module ouvert suit la recommandation NVIDIA pour les GPU compatibles ; un module propriétaire n’est pas intrinsèquement préférable pour ce Turing. Les deux variantes utilisent les mêmes composants NVIDIA en espace utilisateur et ne peuvent pas être installées ensemble. Sources : [GPU et sources 595.91.07](https://github.com/NVIDIA/open-gpu-kernel-modules/blob/595.91.07/README.md), [comparaison des modules](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/kernel_open.html).

La branche 595 est une branche production. La publication graphique amont annonce déjà **595.104.02**, alors que le dépôt Debian 13 consulté fournit encore **595.91.07-1**. Ne pas confondre dernière version amont et dernière version APT disponible. Recontrôler les correctifs de sécurité et la disponibilité avant toute installation ; si une révision production plus récente entre dans le dépôt, la réévaluer plutôt que maintenir aveuglément cette version. La branche 615 est une branche de nouvelles fonctionnalités, sans besoin identifié pour JARVIS. [Annonce NVIDIA des branches](https://forums.developer.nvidia.com/t/current-graphics-driver-releases/28500).

Conserver le contournement retenu : **démarrage sans Core, affichage Intel initialisé, puis branchement à chaud autorisé séparément**. Aucun pilote ne corrige ici le masquage Intel au démarrage Core présent.

## 2. État local réellement vérifié

| Élément | Résultat local |
|---|---|
| Noyau / compilateur de construction | 6.18.54-1-t2-trixie ; GCC Debian 14.2.0-19 |
| Headers exacts | `linux-headers-6.18.54-1-t2-trixie` **6.18.54-1 installé** |
| Lien build | `/lib/modules/6.18.54-1-t2-trixie/build` → `/usr/src/linux-headers-6.18.54-1-t2-trixie` |
| Arbre de développement | Makefile, Module.symvers, include/config/kernel.release, include/generated/autoconf.h et utsrelease.h présents ; release exact concordant |
| GCC / G++ | gcc-14 et g++-14 **14.2.0-19** ; métapaquets 4:14.2.0-1 |
| DKMS | **3.2.2-1~deb13u1 installé** ; `/usr/sbin/dkms status` ne retourne aucune entrée |
| make / build-essential | **4.4.1-2 / 12.12 installés** |
| libelf-dev | Non installé ; candidat local 0.192-4 ; à inclure comme dépendance de développement préventive dans la future transaction |
| Secure Boot / lockdown | `mokutil --sb-state` : **SecureBoot disabled** ; lockdown `[none] integrity confidentiality` |
| Signature noyau | CONFIG_MODULE_SIG=y, CONFIG_MODULE_SIG_ALL=y, **MODULE_SIG_FORCE désactivé**, MODVERSIONS=y |
| Pilotes courants | i915 présent ; pas de module NVIDIA ni nouveau observé ; GPU NVIDIA absent du relevé PCI actuel |
| Dépôts APT actuels | trixie, trixie-security, trixie-updates : `main non-free-firmware` ; aucun dépôt NVIDIA/backports ; pas de contrib/non-free |
| Candidats NVIDIA locaux | nvidia-driver et nvidia-kernel-dkms : **aucun candidat** |

Le noyau utilise la configuration `/boot/config-6.18.54-1-t2-trixie` ; absence de `.config` à la racine des headers ne suffit pas à déclarer ceux-ci incomplets : les fichiers générés existent. La présence de Module.symvers est importante avec MODVERSIONS. Les headers Debian génériques 6.12.111 déjà installés **ne remplacent pas** les headers T2 exacts.

Les headers T2 ne sont visibles dans APT qu’à priorité 100, depuis `/var/lib/dpkg/status` : ils sont installés, mais aucun dépôt actuellement configuré ne permet de les retélécharger. Préserver cet arbre ; une prochaine mise à jour T2 devra fournir ses propres headers exacts. Le projet T2 publie des noyaux adaptés, sans garantie documentaire identifiée pour cette combinaison eGPU/NVIDIA/noyau précise. [T2Linux, construction du noyau](https://wiki.t2linux.org/guides/kernel/).

Le premier appel `dkms` sans chemin échouait parce que /usr/sbin n’est pas dans le PATH de cette session ; ce n’était pas une absence du paquet. L’appel absolu a réussi. Aucune restriction sudo ne bloque les constatations nécessaires de cette mission.

## 3. Versions étudiées et provenance

Métadonnées récupérées directement par HTTPS, sans `apt update`. Copies intégrales et sélections dans `mission05A-preuves`. Les téléchargements documentaires ne constituent pas une vérification APT des signatures InRelease/Release ; celle-ci devra être faite par APT lors de la future activation autorisée.

| Origine | Version exacte observée | Appréciation pour JARVIS |
|---|---|---|
| Debian trixie non-free | **550.163.01-2** | GPU et CUDA pris en charge ; version ancienne, adaptations noyau insuffisamment récentes pour retenir 6.18 T2 sans preuve ; écartée du premier essai |
| Debian trixie-backports non-free | **550.163.01-4~bpo13+1** | Correctifs supplémentaires aux interfaces noyau ; alternative documentaire, pas compilation T2 prouvée ; branche ancienne avec problèmes de sécurité signalés |
| NVIDIA Debian 13, R590 | **590.44.01-1, 590.48.01-1** | Compatibilité 6.18 rapportée, mais versions anciennes ; pas le choix initial |
| NVIDIA Debian 13, R595 | **595.45.04-1, 595.58.03-1, 595.71.05-1, 595.91.07-1** | **595.91.07-1 retenu comme candidat APT production** |
| NVIDIA Debian 13, R610 | **610.43.02-1, 610.57.04-1** | Disponibles ; aucune nécessité établie d’adopter cette branche |
| NVIDIA Debian 13, R615 | **615.71.09-1 et 615.71.09-2** | Révision APT la plus récente du relevé ; nouvelles fonctionnalités, non retenue initialement |
| NVIDIA amont, R580 | **580.178.04** notamment | Disponible en archives amont ; **aucun paquet R580 dans l’index Debian 13 consulté** ; ne pas importer le dépôt Debian 12 |
| NVIDIA amont graphique | **595.104.02, 615.78.08** repérés | Publications amont plus récentes, absentes de l’index Debian 13 étudié ; pas une instruction d’utiliser .run ou GitHub en installation |

Les versions du dépôt NVIDIA sont disponibles pour les paquets nvidia-driver, nvidia-driver-cuda, modules DKMS ouverts/propriétaires et métapaquets associés. Les noms Debian et NVIDIA diffèrent : **Debian `nvidia-open-kernel-dkms`**, mais **NVIDIA `nvidia-kernel-open-dkms`**. Éviter les commandes mêlant ces deux conventions et leurs bibliothèques.

Sources : [paquet Debian stable](https://packages.debian.org/trixie/nvidia-driver), [DKMS backports](https://packages.debian.org/trixie-backports/nvidia-kernel-dkms), [index NVIDIA Debian 13](https://developer.download.nvidia.com/compute/cuda/repos/debian13/x86_64/Packages.gz), [publications modules NVIDIA](https://github.com/NVIDIA/open-gpu-kernel-modules/releases).

L’absence de candidat sur la machine résulte des composants/dépôts non activés, pas de l’inexistence des paquets. Aucun paquet sid/forky/Ubuntu, aucun mélange de dépôts Debian 12, aucun installateur .run recommandé.

## 4. Compatibilité noyau : ce qui est établi et ce qui manque

Une mention « Linux 4.15 ou supérieur » dans le README NVIDIA n’est pas une garantie pour toutes les révisions futures ou tous les patches T2. La validation doit être attachée au triplet **source du pilote / headers exacts / compilateur**.

**Constats statiques 595.91.07 :**

- `kernel-open/conftest.sh` détecte la présence du second argument de `get_dev_pagemap`, supprimé pour Linux 6.18 (commit dd57f5feb19a).
- Kbuild utilise `ccflags-y`, ce qui évite de dépendre uniquement d’EXTRA_CFLAGS pour les noyaux récents.
- Le paquet ouvert inspecté fournit DKMS `PACKAGE_NAME=nvidia`, `PACKAGE_VERSION=595.91.07`, AUTOINSTALL=yes et les cinq modules : nvidia, nvidia-modeset, nvidia-drm, nvidia-peermem, nvidia-uvm. Les modules peuvent être construits sans GPU connecté.

Ces éléments constituent une **compatibilité attendue et motivée**, pas un résultat de compilation. [Conftest officiel 595](https://github.com/NVIDIA/open-gpu-kernel-modules/blob/595.91.07/kernel-open/conftest.sh), [Kbuild officiel 595](https://github.com/NVIDIA/open-gpu-kernel-modules/blob/595.91.07/kernel-open/Kbuild).

**Debian 550 :** archive des patches backports inspectée. La révision -2 comporte des backports ccflags-y/page_pgmap/autres interfaces ; -3 corrige une interface IOMMU pour le module ouvert avec 6.16 ; -4 corrige drm_fb_create pour 6.17. Il serait inexact de traiter le paquet Debian comme un 550 amont non patché, ou d’affirmer ici que tous les 550 échouent sur 6.18. Inversement, les correctifs publiés jusqu’à 6.17 ne prouvent pas la compilation T2 6.18.54. Un [rapport Debian d’échec à la transition 6.19](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1130058) concerne un autre noyau et ne démontre pas un échec 6.18.

Le [suivi de sécurité Debian](https://security-tracker.debian.org/tracker/source-package/nvidia-graphics-drivers) signale des vulnérabilités non corrigées dans la branche distribuée ; ne pas retenir cette ancienne branche pour un nouveau serveur par simple familiarité.

**Incompatibilités connues pertinentes :** changement get_dev_pagemap de 6.18 documenté dans [PR NVIDIA #951](https://github.com/NVIDIA/open-gpu-kernel-modules/pull/951) ; erreurs de compilation rapportées avec anciennes branches ; incohérences module/bibliothèques provoquant des erreurs NVML ; firmware GSP absent ou d’une autre version empêchant l’initialisation. Aucun correctif T2 spécifique à NVIDIA 595 requis n’a été identifié dans les sources consultées ; cela ne l’exclut pas.

La validation réelle future exige `dkms status` **installed pour 6.18.54-1-t2-trixie**, un make.log sans erreur, vermagic exact, puis initialisation du GPU et calcul. Une simple réussite pour le noyau Debian 6.12 également installé n’est pas suffisante.

## 5. Variante ouverte ou propriétaire, CUDA et dépendances

**Ouvert DKMS en premier**, propriétaire DKMS 595.91.07 comme variante de repli à réévaluer seulement si une panne GSP/init clairement documentée le justifie. Le module ouvert NVIDIA est distinct de nouveau et utilise toujours des bibliothèques utilisateur et un firmware NVIDIA. Les deux variantes bénéficient de CUDA sur Turing. Le propriétaire peut permettre un essai distinct sans GSP ; ne pas appliquer `NVreg_EnableGpuFirmware=0` au module ouvert, qui en dépend.

Limites déclarées pour l’ouvert 595 : initialisation plus lente, certaines transitions de puissance plus lentes ; RTD3 annoncé pour Ampere et ultérieur dans le manuel de cette version. Cela invite à tester ce Turing externe en régime stable, sans ajouter de réglages d’économie d’énergie ou de cycles suspend/resume au premier essai. [Manuel ouvert 595](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/kernel_open.html), [firmware GSP 595](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/gsp.html).

| Nécessité | Traitement envisagé |
|---|---|
| Compilation | Headers T2 exacts, GCC/G++ 14, make, DKMS ; outils de build déjà présents ; libelf-dev à ajouter |
| DKMS ouvert | Dépend de DKMS ≥3.1.8, g++, firmware-nvidia-gsp **595.91.07-1** |
| Calcul NVIDIA | nvidia-driver-cuda **595.91.07-1** : bibliothèques driver/CUDA/NVML et utilitaires via ses dépendances |
| Création des nœuds / persistance | nvidia-modprobe et nvidia-persistenced correspondants tirés par les dépendances |
| Affichage NVIDIA | Métapaquet nvidia-driver/GL/EGL/Vulkan/Xorg complet non choisi pour cette première installation |
| Modules utiles à Ollama | nvidia et nvidia_uvm ; modeset/drm/peermem peuvent être construits sans être requis pour l’inférence CUDA |
| CUDA Toolkit complet / nvcc | **Pas nécessaire pour Ollama précompilé** ; seulement pour développement/compilation CUDA spécifique |
| Container Toolkit NVIDIA | Pas nécessaire pour Ollama natif ni pour Open WebUI utilisant son API ; seulement si un conteneur doit lui-même accéder au GPU |

Le paquet de calcul inspecté fournit `nvidia-smi` (Provides et fichiers) ; ne pas ajouter aveuglément un paquet nvidia-utils d’une autre distribution. La chaîne inspectée est `nvidia-driver-cuda` → `nvidia-opencl-icd` → `libcuda1=595.91.07-1` ; ce dernier fournit `libcuda.so.1`. Contrôler sa résolution après installation via `ldconfig -p` (lecture du cache).

Ollama distribue ses moteurs GPU précompilés. Sa documentation actuelle indique pilote NVIDIA ≥550, CC ≥5.0, et cite la Quadro RTX 5000 à 7.5 ; 595 satisfait ce minimum. **La ligne CUDA Version de nvidia-smi exprime la capacité du pilote, pas la présence de nvcc/Toolkit.** Le pilote seul et les bibliothèques embarquées peuvent donc suffire. [Matériel Ollama](https://docs.ollama.com/gpu), [bibliothèques embarquées](https://docs.ollama.com/troubleshooting).

## 6. Intel principal et risques Thunderbolt

Installer les **composants de calcul seuls**, conserver l’écran sur le HDMI Intel, ne pas générer xorg.conf avec nvidia-xconfig, ne pas définir NVIDIA comme PrimaryGPU et ne pas ajouter d’offload NVIDIA aux variables de GNOME. Ne pas changer i915, GRUB ou les réserves PCIe. GNOME doit continuer à utiliser Intel, ce qui sera vérifié après hotplug ; l’installation dédiée au calcul réduit les interactions graphiques sans constituer une garantie absolue de choix du compositeur.

La présence éventuelle de nvidia_drm ne prouve pas que GNOME a changé de GPU. Vérifier les connecteurs, les pilotes de /dev/dri, les journaux du compositeur et les processus NVIDIA. Si GNOME apparaît dans les clients GPU ou si HDMI régresse, arrêter le test et analyser avant toute modification graphique. Aucun réglage persistant modeset/blacklist DRM ajouté par cette mission.

NVIDIA documente les eGPU Thunderbolt et déconseille de supposer stable un retrait à chaud en cours d’utilisation ; la restriction par défaut des écrans eGPU concerne **Xorg**, pas une garantie pour GNOME Wayland. [Documentation NVIDIA eGPU](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/egpu.html).

Risques du premier branchement avec pilote : udev sonde automatiquement une nouvelle fonction PCI, le module/firmware initialise le GPU et active ses accès DMA ; une panne peut bloquer le périphérique ou la machine malgré des BAR auparavant valides. IOMMU=on/pt n’est pas une preuve de stabilité ou d’isolation complète. Autorisation Thunderbolt, alimentation, liaison et ressources restent à contrôler sans rescan. Les BDF peuvent changer ; découvrir le GPU par **10de:1eb0**, puis utiliser son UUID.

Un [rapport utilisateur NVIDIA sur CUDA/eGPU Blackwell et Thunderbolt 4](https://forums.developer.nvidia.com/t/rtx-5060-ti-egpu-aorus-ai-box-cuda-hard-lock-on-linux-via-thunderbolt-4/365386) décrit nvidia-smi fonctionnel à vide mais blocage sous calcul. Il ne concerne ni Turing ni ce Mac : c’est un motif de validation en charge, pas une incompatibilité démontrée pour JARVIS. Ne pas transformer un succès nvidia-smi en validation Ollama.

Installer hors présence du Core est faisable : DKMS n’a pas besoin du matériel. `nvidia-smi` sans GPU peut échouer et le service de persistance peut ne pas démarrer ; ce n’est pas, en soi, un échec de compilation. Après connexion, udev peut charger nvidia ; UVM/nœuds de périphériques peuvent demander une initialisation complémentaire autorisée. Ne pas promettre qu’Ollama lancé avant le hotplug réévaluera immédiatement sa liste GPU : le démarrer après validation du GPU.

## 7. Secure Boot et effets des paquets inspectés

À l’instant du relevé, Secure Boot désactivé, lockdown inactif, signature forcée désactivée : **aucun enrôlement MOK nécessaire dans ce contexte constaté**. DKMS peut signer ses modules localement ; vérifier le champ signer plutôt que confondre signature présente et clé de confiance exigée. Si Secure Boot/lockdown change, interrompre la procédure et traiter la signature dans une mission dédiée ; aucun mokutil --import, changement de politique Apple, EFI ou NVRAM proposé ici.

Les paquets inspectés ont des effets persistants qui doivent être couverts par l’autorisation future :

- `nvidia-kernel-support` installe `/etc/modprobe.d/nvidia.conf`, blacklistant nouveau et nova-core, avec des paramètres NVIDIA de gestion mémoire/puissance. Son postinst et postrm exécutent **update-initramfs -u**.
- `nvidia-driver-cuda` fournit un preset activant **nvidia-persistenced.service**.
- DKMS installe des modules dans /lib/modules, exécute depmod et participe aux hooks des noyaux. Il construit également les modules graphiques ; « calcul seul » désigne les composants utilisateur retenus, pas un DKMS amputé.

Ce sont des résultats de lecture des .deb, sans exécution. Une installation ne peut donc pas être présentée comme « aucun changement initramfs ». Les restrictions actuelles interdisent ces effets et sont entièrement respectées.

## 8. Procédure envisagée — TOUTES les commandes ci-dessous sont NON EXÉCUTÉES

Procéder en deux missions autorisées séparément : **installation et validation statique Core absent**, puis **hotplug et calcul**. Les commandes sont une procédure à revoir avec le solveur APT après activation autorisée, pas un script à coller intégralement.

### A. Sauvegarde et état avant transaction

Depuis SSH, Core déjà absent, aucun redémarrage nécessaire pour cette étape :

```bash
mkdir -p /home/adminjarvis/JARVIS/rapports/mission05-installation-avant
dpkg-query -W -f='${binary:Package}\t${db:Status-Status}\t${Version}\n' > /home/adminjarvis/JARVIS/rapports/mission05-installation-avant/paquets.tsv
apt-mark showmanual > /home/adminjarvis/JARVIS/rapports/mission05-installation-avant/manuels.txt
apt-mark showhold > /home/adminjarvis/JARVIS/rapports/mission05-installation-avant/holds.txt
sudo tar -C / -czf /home/adminjarvis/JARVIS/rapports/mission05-installation-avant/configuration.tgz etc/apt etc/modprobe.d etc/modules-load.d etc/X11 etc/systemd/system
sudo cp --preserve=all /boot/initrd.img-6.18.54-1-t2-trixie /home/adminjarvis/JARVIS/rapports/mission05-installation-avant/initrd.img-6.18.54-1-t2-trixie
sudo sha256sum /boot/grub/grub.cfg /boot/vmlinuz-6.18.54-1-t2-trixie /boot/initrd.img-6.18.54-1-t2-trixie
/usr/sbin/dkms status
mokutil --sb-state
```

Vérifier espace libre sur /, /boot et /var/tmp avant transaction. Sauvegarder également les versions antérieures des paquets qui seraient **mis à jour**, avec leurs .deb récupérables : une liste seule ne garantit pas leur restauration.

### B. Dépôt NVIDIA Debian 13 et choix de branche

La procédure NVIDIA demande contrib. Pour ce chemin, le firmware/driver viennent du dépôt NVIDIA : activer non-free Debian n’est pas nécessairement requis. Ajouter seulement un fichier dédié, sans réécrire les sources existantes :

```bash
printf '%s\n' 'deb https://deb.debian.org/debian trixie contrib' | sudo tee /etc/apt/sources.list.d/jarvis-nvidia-prerequis.list
curl --fail --location --output /home/adminjarvis/JARVIS/rapports/mission05-installation-avant/cuda-keyring_1.1-1_all.deb https://developer.download.nvidia.com/compute/cuda/repos/debian13/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i /home/adminjarvis/JARVIS/rapports/mission05-installation-avant/cuda-keyring_1.1-1_all.deb
sudo apt-get update
apt-cache policy nvidia-driver-pinning-595 nvidia-driver-cuda nvidia-kernel-open-dkms
sudo apt-get -s install nvidia-driver-pinning-595=595-1
```

Revoir le paquet de clé et ses fichiers/empreintes à cette date. Ne pas accepter une erreur de signature APT. Après revue de la simulation et autorisation couvrant ce verrouillage :

```bash
sudo apt-get install nvidia-driver-pinning-595=595-1
apt-cache policy nvidia-driver-cuda nvidia-kernel-open-dkms firmware-nvidia-gsp
sudo apt-get -s --no-install-recommends install libelf-dev nvidia-driver-cuda=595.91.07-1 nvidia-kernel-open-dkms=595.91.07-1
```

Arrêter si 595.91.07-1 a disparu, si une révision production plus récente mérite réévaluation, si APT retire des composants GNOME/Mesa/Intel/T2, remplace le noyau ou mélange les variantes/branches. Examiner toutes les dépendances, installations, mises à jour, suppressions et effets des services. Pas de `dist-upgrade` global. Le pin de branche inspecté impose une priorité 1000 aux familles NVIDIA 595 ; il ne fige pas chaque microversion pour toujours. [Méthode Debian NVIDIA](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/debian.html), [verrouillage de version](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/version-locking.html).

### C. Installation autorisée, matériel toujours absent

Seulement après validation du plan exact :

```bash
sudo env CC=/usr/bin/gcc-14 CXX=/usr/bin/g++-14 apt-get --no-install-recommends install libelf-dev nvidia-driver-cuda=595.91.07-1 nvidia-kernel-open-dkms=595.91.07-1
/usr/sbin/dkms status
/usr/sbin/modinfo -k 6.18.54-1-t2-trixie nvidia
/usr/sbin/modinfo -k 6.18.54-1-t2-trixie nvidia_uvm
systemctl status nvidia-persistenced --no-pager
```

Exiger une construction/installation DKMS du **noyau exact**, pas seulement 6.12. Si non construite automatiquement et uniquement après diagnostic du journal : commande prévue `sudo env CC=/usr/bin/gcc-14 CXX=/usr/bin/g++-14 /usr/sbin/dkms install -m nvidia -v 595.91.07 -k 6.18.54-1-t2-trixie`. Cela compile/installe : non exécuté en 05A et pas une commande de lecture.

Inspecter `/var/lib/dkms/nvidia/595.91.07/` pour le make.log réel (DKMS peut organiser les logs par noyau/architecture), version, vermagic, licence `Dual MIT/GPL`, signer et firmware. Les modules peuvent être présents sur disque sans être chargés. Ne pas provoquer leur chargement hors du test prévu. L’installateur peut activer des services : vérifier ces effets sans promettre que tout reste inactif.

La documentation générale NVIDIA prescrit un redémarrage. Ici une première validation sans redémarrage est **techniquement envisageable** car aucun NVIDIA/nouveau n’est chargé et le GPU est absent ; ce n’est pas une garantie de tout script de paquet. Si un effet exige un reboot ou si le bureau régresse, arrêter et demander une mission explicitement autorisée, sans redémarrage automatique.

### D. Hotplug — autorisation distincte obligatoire

Avant connexion, relever boot ID, affichage Intel et kernel journal ; suivre le journal depuis un poste SSH indépendant. Après connexion humaine autorisée et sans rescan :

```bash
lspci -Dnnk -d 10de:1eb0
lspci -Dnnk -s 0000:00:02.0
lsmod
nvidia-smi -L
nvidia-smi --query-gpu=name,uuid,pci.bus_id,driver_version,memory.total --format=csv
nvidia-smi -q
ls -l /dev/nvidia* /dev/dri/by-path
sudo journalctl -k -b --no-pager
```

Attendre Quadro RTX 5000, mémoire nominale 16 Go (valeur reportée légèrement différente possible), driver 595.91.07, firmware cohérent et i915 toujours présent. Si UVM/nœuds manquent, commandes complémentaires **à autoriser dans ce test**, pas à déclencher automatiquement par ce rapport :

```bash
sudo /usr/sbin/modprobe nvidia_uvm
sudo nvidia-modprobe -u
```

Les alias udev peuvent charger nvidia au hotplug ; nvidia-smi/nvidia-modprobe ne sont pas des sondes totalement passives quand on veut interdire tout chargement : **aucune de ces commandes NVIDIA n’a été exécutée pendant 05A**.

Arrêter sur Xid, AER fatal, fault DMAR nouveau, timeout GSP, GPU fallen off the bus, perte SSH ou régression HDMI. Ne pas réinitialiser le GPU, écrire PCI, rescanner, retirer le Core ou recharger des modules en guise de correction improvisée.

## 9. Tests CUDA puis Ollama — proposés uniquement

### Driver API sans Toolkit

Après hotplug validé, test Python standard (aucun pip ni nvcc) :

```bash
python3 - <<'PY'
import ctypes
cuda = ctypes.CDLL('libcuda.so.1')
def check(result):
    if result != 0:
        raise RuntimeError(f'CUDA Driver API error {result}')
check(cuda.cuInit(0))
count = ctypes.c_int()
check(cuda.cuDeviceGetCount(ctypes.byref(count)))
print('CUDA devices:', count.value)
if count.value < 1:
    raise RuntimeError('Aucun GPU CUDA')
device = ctypes.c_int()
check(cuda.cuDeviceGet(ctypes.byref(device), 0))
name = ctypes.create_string_buffer(256)
check(cuda.cuDeviceGetName(name, 256, device))
major, minor = ctypes.c_int(), ctypes.c_int()
check(cuda.cuDeviceComputeCapability(ctypes.byref(major), ctypes.byref(minor), device))
print(name.value.decode(), 'compute capability', major.value, minor.value)
PY
```

Ce test valide chargement libcuda, initialisation et inventaire, **pas l’exécution d’un kernel de calcul**. Le vrai test en charge sera une inférence Ollama et la surveillance conjointe des erreurs et de l’utilisation GPU.

### Installation Ollama séparée

Ne pas utiliser `curl ... | sh`. Le script officiel inspecté peut ajouter le dépôt CUDA/keyring, exécuter apt update et installer cuda-drivers, installer des headers, appeler DKMS/modprobe, créer modules-load.d et démarrer un service. Il détecte les GPU/outils présents ; le Core absent peut éviter certaines branches, mais cela n’est pas une méthode fiable de contrôle. [Script officiel inspecté](https://github.com/ollama/ollama/blob/main/scripts/install.sh).

Préférer une **archive Ollama versionnée**, téléchargée dans le répertoire utilisateur, contrôlée (version/empreinte et contenu), extraite d’abord dans un staging utilisateur, puis copiée seulement après revue. La documentation actuelle utilise une archive **tar.zst** amd64, pas nécessairement l’ancien tar.gz. Les URLs `download/…` sont mobiles : résoudre et figer la release lors de la mission Ollama. Aucune version Ollama ni URL versionnée finale inventée ici. Installer le binaire et ses bibliothèques NVIDIA embarquées, sans installer le Toolkit complet ni exécuter le script de pilotes. [Installation manuelle officielle](https://docs.ollama.com/linux).

Commencer par un serveur au premier plan, **après** apparition du GPU, sur loopback :

```bash
CUDA_VISIBLE_DEVICES=GPU-UUID_RELEVE OLLAMA_VULKAN=0 OLLAMA_DEBUG=1 OLLAMA_HOST=[ADRESSE PRIVÉE EXPURGÉE]:11434 ollama serve
```

Remplacer GPU-UUID_RELEVE par l’UUID de `nvidia-smi -L` ; aucune variable globale GNOME modifiée. Désactiver le backend Vulkan pour ce test garde le diagnostic centré sur CUDA et évite de sélectionner l’iGPU pour l’IA. Dans une autre session, après autorisation du téléchargement de modèle, par exemple :

```bash
ollama pull qwen2.5:7b
ollama run qwen2.5:7b 'Réponds en français : combien font 17 multiplié par 19 ?'
ollama ps
nvidia-smi
```

Le modèle est un exemple raisonnable pour 16 Go à quantification adaptée, pas une garantie que tout contexte tient en VRAM. Vérifier la quantification/taille réelle du tag au téléchargement. Attendus : réponse correcte (323), moteur CUDA dans les logs, offload GPU et VRAM allouée, `ollama ps` indiquant le traitement GPU (idéalement 100% pour ce petit test), utilisation NVIDIA pendant génération, bureau Intel et SSH stables. Des CPU actifs restent normaux ; le seul temps de réponse ou la seule présence du GPU dans nvidia-smi ne suffisent pas.

Si service futur : vérifier accès /dev/nvidia* pour **son utilisateur réel**, groupes et éventuelles restrictions systemd ; tester sous ce compte plutôt que masquer un problème en lançant root. Le serveur initialement CPU avant hotplug doit être relancé proprement dans une mission autorisée si sa détection reste ancienne ; aucune boucle de rechargement UVM proposée automatiquement.

## 10. Retour arrière envisagé

Le retour cible est l’état initial **sans pilote NVIDIA**, noyau T2 et i915 conservés. Toute désinstallation exécute aussi des hooks et exige une autorisation. Ne jamais supprimer globalement `nvidia*`, utiliser autoremove sans revue ou toucher aux paquets Mesa/T2.

1. Arrêter seulement les clients GPU/Ollama/services NVIDIA ajoutés, après autorisation. Si le GPU est connecté, **ne pas le retirer à chaud sous charge**. Une récupération nécessitant arrêt physique ou redémarrage sera autorisée séparément.
2. Produire le manifeste des paquets **nouvellement installés** depuis la sauvegarde et revoir les paquets mis à jour. Exemple prévu :

```bash
python3 - <<'PY'
import pathlib, subprocess
base = pathlib.Path('/home/adminjarvis/JARVIS/rapports/mission05-installation-avant')
before = {l.split('\t')[0] for l in (base / 'paquets.tsv').read_text().splitlines() if '\tinstalled\t' in l}
current = subprocess.check_output(['dpkg-query', '-W', '-f=${binary:Package}\t${db:Status-Status}\n'], text=True)
new = sorted(l.split('\t')[0] for l in current.splitlines() if l.endswith('\tinstalled') and l.split('\t')[0] not in before)
(base / 'paquets-ajoutes.txt').write_text('\n'.join(new) + '\n')
print('\n'.join(new))
PY
```

La différence peut inclure des installations indépendantes : sélectionner seulement les paquets de la transaction NVIDIA dans **paquets-retour-arriere-revus.txt**, une entrée par ligne, avant toute purge. Inclure dépendances de calcul/firmware nouvellement ajoutées, DKMS ouvert, pinning, keyring et libelf-dev uniquement si ajoutés par cette transaction. Préserver DKMS/GCC/headers/build-essential préexistants.

```bash
sudo xargs -r -a /home/adminjarvis/JARVIS/rapports/mission05-installation-avant/paquets-retour-arriere-revus.txt apt-get -s purge
sudo xargs -r -a /home/adminjarvis/JARVIS/rapports/mission05-installation-avant/paquets-retour-arriere-revus.txt apt-get purge
/usr/sbin/dkms status
```

Revoir la simulation avant la seconde commande. La suppression du paquet DKMS doit retirer nvidia/595.91.07 via son prerm ; seulement si une entrée orpheline subsiste et après diagnostic : `sudo /usr/sbin/dkms remove -m nvidia -v 595.91.07 --all`. Ne pas supprimer d’autres modules DKMS.

3. Enlever seulement le fichier contrib ajouté par cette mission future et les éventuels fichiers de dépôt/pin/keyring résiduels identifiés par `dpkg -L cuda-keyring` et la sauvegarde. Exemple pour le fichier dédié, s’il a effectivement été créé : `sudo rm /etc/apt/sources.list.d/jarvis-nvidia-prerequis.list`. Ne pas restaurer aveuglément tout /etc/apt par-dessus des changements indépendants.
4. Le postrm NVIDIA régénère l’initramfs. Examiner le résultat ; si nécessaire et autorisé, `sudo update-initramfs -u -k 6.18.54-1-t2-trixie`. La copie de l’initrd d’origine reste une récupération de dernier recours **uniquement si le noyau et les autres modifications initramfs n’ont pas changé**, après revue. Ne pas écraser automatiquement un initrd contenant d’autres correctifs.
5. Restaurer les versions de paquets préexistants modifiées par la transaction à partir des .deb sauvegardés et d’une simulation APT spécifique. Aucun downgrade global. Vérifier i915, GNOME, SSH, boot ID et paramètres conservés. Des modules chargés peuvent rester en mémoire après purge : ne pas forcer leur retrait si occupés ; une remise à zéro peut exiger un redémarrage séparément autorisé.

Le rollback paquet est réversible et documentable ; le retour runtime n’est pas garanti sans arrêt des clients ou reboot. La variante propriétaire serait un **nouvel essai**, après retrait complet de l’ouvert et simulation `nvidia-driver-cuda=595.91.07-1 nvidia-kernel-dkms=595.91.07-1`, pas une installation simultanée.

## 11. Suite recommandée et limites

Ordre proposé : accord pour dépôt/paquets/effets initramfs et persistance → installation Core absent et contrôle DKMS exact → accord hotplug → nvidia-smi + Driver API + charge courte → installation Ollama manuelle et versionnée → inférence stable → service utilisateur dédié → Open WebUI.

Pour Open WebUI, privilégier une interface cliente du serveur Ollama déjà validé, liée au départ à loopback et accessible par tunnel SSH. Elle n’a pas besoin de pilote NVIDIA, de Toolkit CUDA ou d’accès GPU lorsqu’elle utilise l’API Ollama. Si un déploiement conteneur est retenu, figer les versions et résoudre séparément le chemin vers l’Ollama hôte ; ne pas ajouter Docker/NVIDIA Container Toolkit à la première validation du pilote.

**Limites :** GPU non connecté pendant la mission ; aucune compilation, aucun chargement, aucun calcul ; aucune preuve de compatibilité intégrale NVIDIA 595 / T2Linux 6.18.54 / Thunderbolt 3 sur Macmini8,1. L’état exhaustif des avis de sécurité NVIDIA pour 595.91.07 n’a pas été certifié par cette recherche ; la recommandation ne vaut pas garantie d’absence de vulnérabilité et la révision production plus récente devra être comparée avant installation. Aucun solveur APT après activation du dépôt n’a été exécuté ; la liste de dépendances et les effets examinés sont documentaires. La stabilité du hotplug sans pilote de 04P ne valide pas l’initialisation GSP/DMA avec pilote. Le problème de démarrage Core présent reste reporté.

Les preuves locales et sources téléchargées sont dans `/home/adminjarvis/JARVIS/rapports/mission05A-preuves/`, avec SHA256SUMS. Les quatre .deb inspectés concordent avec les SHA-256 de l’index NVIDIA téléchargé ; cela n’équivaut pas à une validation cryptographique de l’index par APT. Aucun script de paquet téléchargé n’a été exécuté.

**Mission 05A documentaire terminée. Attente de l’autorisation explicite avant installation, activation de dépôt, compilation/chargement, modification de service/initramfs ou branchement du Core.**

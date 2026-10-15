# JARVIS — Mission 05B-A : audit des avertissements NVIDIA objtool

Date : 12 octobre 2026. Audit exclusivement en lecture ; seule création persistante : ce rapport. Aucune compilation, modification des modules, action sur les services, connexion du Core, commande nvidia-smi, test CUDA ou chargement NVIDIA.

## Décision

**GO sous conditions pour proposer un premier branchement à chaud surveillé en Mission 05C, après autorisation distincte.** Aucun motif de blocage opérationnel concret n’est établi par les diagnostics examinés. Cette décision autorise une étape de qualification limitée, pas une mise en production ni une affirmation de sécurité complète. La compatibilité démontrée reste celle de la construction ; la compatibilité d’exécution reste à tester.

Les retours non conformes à RETHUNK correspondent à une lacune réelle de durcissement du code NVIDIA indépendant du noyau. Ils ne sont pas qualifiés d’inoffensifs. Leur nombre ne représente pas autant de défauts indépendants. Les protections IBRS annoncées par ce processeur réduisent la pertinence de certaines attaques de prédiction des retours, sans démontrer une couverture complète du pilote ou remplacer un audit de sécurité.

Le NO-GO immédiat de 05B était une suspension de décision en attente d’analyse. Cet audit permet de proposer un essai conditionnel, avec risque résiduel de blocage de la machine accepté explicitement par l’autorisation de 05C.

## 1. État et preuves

Noyau actif confirmé : `6.18.54-1-t2-trixie`. Boot ID : `d8f67bde-f785-4365-99ed-1af19afe9620`. `lspci -d 10de:` ne retourne aucune entrée. `lsmod` confirme i915 et aucun module nvidia/nouveau. SDDM et SSH actifs ; gnome-shell PID 1270 et session graphique 5 présents. nvidia-persistenced désactivé/inactif. Ces observations ne testent pas le pilote NVIDIA.

Référence : [mission05B.md](mission05B.md). Preuves déjà conservées dans [mission05B-preuves](mission05B-preuves/) :

- `dkms-make-0.txt` : journal Debian 6.12.111, 15 839 lignes ; SHA-256 `c144bb9527ab68dc9d750f1759384265c3c3a75c48eb4e2211512b8d8b0b3683`.
- `dkms-make-1.txt` : journal T2 6.18.54, 15 844 lignes ; SHA-256 `73115e79d744504c436910a14aac1feaf6fe74b60045e8acce82ca6abfe579cc`.
- `installation-complete.log`, `modules-verification.json`, `validation-complete.json`, `mitigations-lecture.txt`, `initramfs-comparaison.json` : éléments de 05B, distingués des contrôles actuels.

Les deux journaux ont été parcourus intégralement par analyse textuelle, toutes les lignes contenant `warning:` classifiées, puis comparées en multiensembles après retrait du préfixe situé avant `warning:`. **Différence : zéro dans les deux sens**, y compris symboles et offsets. Les lignes normales et les métadonnées des journaux diffèrent ; leurs SHA ne doivent pas être identiques. Les deux fins de journal attestent `exit code: 0`, durées 1 min 36 / 1 min 35. Aucun diagnostic d’erreur de compilation retrouvé. T2 omet la génération BTF faute de vmlinux ; Debian affiche la génération BTF. Ce manque d’information BTF n’équivaut pas à une erreur de liaison ou à un défaut de chargement.

## 2. Classification exhaustive

| Diagnostic par construction | Debian 6.12.111 | T2 6.18.54 | Origine observée | Portée |
|---|---:|---:|---|---|
| naked return, objet nvidia.o | 11 098 | 11 098 | Partie OS-agnostic du module principal | Durcissement des retours incomplet |
| naked return, objet nvidia-modeset.o | 2 684 | 2 684 | Partie OS-agnostic du modesetting | Même problème |
| data relocation to !ENDBR | 265 | 265 | nvidia-modeset.o, exclusivement .eh_frame | Vérification IBT à contextualiser |
| expansion-to-defined | 7 | 7 | kernel-open/nvidia/nv-imp.c | Portabilité du préprocesseur |
| missing-prototypes | 6 | 6 | kernel-open/nvidia/nv-vm.c | Cohérence des déclarations C |
| **Total warning** | **14 060** | **14 060** | | |

Aucune autre famille dans ces 28 120 lignes d’avertissement : pas de stack-state mismatch, unreachable instruction ou relocation overflow signalés. Cela ne démontre pas l’absence de tout défaut de contrôle de flot : seules les anomalies effectivement diagnostiquées sont classées. Les avertissements de relocalisation sont les 265 !ENDBR, pas une erreur du linker.

Les 13 782 diagnostics naked concernent 13 578 noms de symboles distincts par journal. Plusieurs offsets/instances peuvent porter le même nom, notamment les fonctions générées NVOC ; des exemplaires dans différents objets ne constituent pas automatiquement la même fonction physique. La cause commune est une politique de génération de retours, pas 13 782 régressions indépendantes.

## 3. Objets, fonctions et compilation locale

Le Makefile installé `/usr/src/nvidia-595.91.07/Makefile`, lignes 13–54, construit `src/nvidia/<OUTPUTDIR>/nv-kernel.o` et `src/nvidia-modeset/<OUTPUTDIR>/nv-modeset-kernel.o`, puis les relie par des symlinks nommés `nv-kernel.o_binary` et `nv-modeset-kernel.o_binary` avant Kbuild. Les journaux montrent réellement `make -C src/nvidia`, `make -C src/nvidia-modeset`, des étapes CC/CXX/LD et les symlinks. **Le suffixe _binary ne prouve donc pas une compilation préalable chez NVIDIA. Ici, les parties OS-agnostic sont compilées localement à partir des sources ouvertes.** Il existe aussi des données embarquées, shaders et firmware ; les avertissements portent sur le code x86 hôte des objets liés, pas sur une analyse des instructions du processeur GSP.

Exemples traçables :

- `resIsPartialUnmapSupported_d69453`, `__nvoc_ctor_AccessCounterBuffer`, `__nvoc_objCreate_BinaryApi` : wrappers/constructeurs NVOC et gestion de ressources, sources `src/nvidia/generated/`.
- `kgspGetBinArchiveGspRmBoot_TU102` et variantes : fonctions hôtes de sélection d’archives GSP ; leur avertissement n’atteste pas un défaut du firmware GSP lui-même.
- `nvstatusToString` : `src/common/shared/nvstatus/nvstatus.c:69`, lié notamment au modesetting.
- `DeviceInMigMode` : `src/common/src/nv_smg.c` ; helpers HDMI/EDID/DSC, fonctions Evo/KMS, code DisplayPort C++ et décompression LZMA sont également cités par les diagnostics .eh_frame. Bibliothèques communes NVIDIA, code de rendu/push et helpers d’affichage se retrouvent dans l’objet agrégé modeset.

Les Makefiles OS-agnostic utilisent notamment `-mindirect-branch=thunk-extern`, `-mindirect-branch-register` et conditionnellement `-fcf-protection=branch`, mais **ne contiennent pas `-mfunction-return=thunk-extern`**. Retpoline pour appels indirects et thunk pour retours sont des mécanismes différents. Le code Linux compilé via Kbuild bénéficie de ses propres options. Les 13 avertissements C proviennent de cette couche Linux : nv-imp.c lignes 133, 171, 230, 305, 364 ; nv-vm.c lignes 601, 709, 739, 793, 873, 899, fonctions `nv_mem_pool_alloc_pages`, `nv_mem_pool_destroy`, `nv_mem_pool_init`, `nv_mem_pool_free_pages`, `nv_init_page_pools`, `nv_destroy_page_pools`.

L’objet agrégé seul ne fournit pas une attribution exhaustive à chaque unité source. Les journaux constituent la liste complète des fonctions/offsets diagnostiqués ; les exemples ci-dessus et les Makefiles établissent l’origine commune sans prétendre disposer des objets intermédiaires nettoyés par DKMS.

## 4. Signification RETHUNK et !ENDBR

Linux objtool v6.18 signale naked return pour une instruction de retour non annotée sûre lorsque la vérification rethunk est active. Un `ret` ordinaire reste valide sur le plan architectural ; il contourne toutefois le mécanisme de thunk attendu pour durcir les retours. C’est un problème technique réel de couverture de mitigation, sans preuve dans cet audit d’exploitation ni de crash causé par ce retour. [Source Linux check.c](https://raw.githubusercontent.com/torvalds/linux/v6.18/tools/objtool/check.c).

Vérification ELF : dans les deux `nvidia-modeset.ko.xz` installés, `nvstatusToString+0x48` et `+0x57` contiennent bien `c3` / `ret`. Les avertissements ne sont donc pas seulement historiques ou effacés par la signature finale. Les sections `.return_sites` et la référence non définie `__x86_return_thunk` sont néanmoins présentes dans nvidia et modeset : certaines parties sont instrumentées, ce qui ne rend pas tous les retours conformes.

Les 265 !ENDBR se trouvent tous dans `.eh_frame`, données de description de déroulement de pile qui réfèrent aux fonctions, et non dans 265 appels indirects exécutés démontrés. Linux objtool vérifie les destinations des références de données et signale celles qui n’aboutissent pas à ENDBR et ne sont pas annotées exemptées. Cette famille peut donc refléter des références de métadonnées à des fonctions locales sans point d’entrée indirect ; elle ne suffit pas à prouver un piège IBT futur. Inversement, elle ne permet pas de certifier que toute cible indirecte réelle est correcte. Une exception de protection de flot au chargement serait un blocage. [Vérification des relocalisations dans Linux](https://raw.githubusercontent.com/torvalds/linux/v6.18/tools/objtool/check.c).

## 5. Configurations et protections

Les deux `/boot/config-*` ont `CONFIG_X86_KERNEL_IBT=y`, `CONFIG_MITIGATION_RETHUNK=y`, `CONFIG_MITIGATION_RETPOLINE=y`, `CONFIG_OBJTOOL=y`, `CONFIG_UNWINDER_ORC=y`. Les options de mitigation UNRET_ENTRY, CALL_DEPTH_TRACKING, IBPB_ENTRY, IBRS_ENTRY, SRSO, SLS, GDS, RFDS, SPECTRE_BHI, MDS, TAA, MMIO_STALE_DATA, L1TF, RETBLEED, SPECTRE_V1/V2, SRBDS, SSB, ITS, TSA et VMSCAPE sont également activées dans les deux configurations examinées. Une option compilée ne prouve pas qu’un mécanisme particulier est actif sur ce CPU.

T2 : `CONFIG_OBJTOOL_WERROR` explicitement non activé. Debian 6.12 ne porte pas cette ligne dans son config ; il ne faut pas inventer sa valeur. Les deux builds acceptent effectivement ces warnings. Signature SHA-256 activée, MODULE_SIG_FORCE non activé ; T2 a MODULE_SIG_ALL=y. Selon 05B, Secure Boot désactivé et lockdown none. Aucune mesure de mitigation n’a été modifiée.

Lectures actuelles : retbleed = `Mitigation: IBRS` ; spectre_v2 = `Mitigation: IBRS; IBPB: conditional; STIBP: conditional; RSB filling; PBRSB-eIBRS: Not affected; BHI: Not affected`. Ces états concernent le noyau actif et ne certifient pas les deux builds ni l’ensemble du code NVIDIA.

## 6. Explications officielles et retours d’expérience

Dans [NVIDIA #1077](https://github.com/NVIDIA/open-gpu-kernel-modules/issues/1077), le collaborateur aritger reconnaît le 30 mars 2026 l’absence du flag de retour dans la partie OS-agnostic ; il décrit la différence warning/erreur selon OBJTOOL_WERROR. Il ne fournit pas une certification d’innocuité opérationnelle. L’issue reste ouverte lors de la consultation. Un commentaire utilisateur du 10 octobre rapporte une modification de flag dans 615.71.09 et une alerte de thunk non patché sur Linux 6.18.55. Versions différentes : aucune extrapolation de correction à 595.91.07, aucune proposition de changement de branche ou de suppression des protections.

Dans [NVIDIA #1095](https://github.com/NVIDIA/open-gpu-kernel-modules/issues/1095), des utilisateurs rapportent un BUG jump_label en suspension lorsque les instructions attendues NOP restent JMP après omission du traitement objtool. L’issue 595.58.03/Ubuntu 7.0 est fermée en juillet en référence à un correctif d’empaquetage Canonical ; cela ne garantit pas sa présence dans les paquets NVIDIA Debian13. Le texte initial comporte aussi une analyse générée par IA : ses généralisations ne sont pas reprises comme faits. Désactiver WERROR n’équivaut pas à supprimer l’exécution d’objtool.

**Contrôle local ciblé de #1095 :** les cinq sites associés à `freezer_active + 2` dans le `__jump_table` de nvidia-modeset sont tous NOP dans les deux modules. Debian : offsets .text 0x9a0, 0xaa3, 0x1d15, 0x1dd3, 0x1f55, bytes `66 90`. T2 : 0x7d0 (`0f 1f 44 00 00`), 0xaa3, 0x1cf4, 0x1db3, 0x1f35 (`66 90`). Les deux autres entrées T2 concernent validate_usercopy_range, également NOP aux offsets 0x144e et 0x14bf. Cela écarte le défaut précis de ces sites sur disque, sans certifier tous les branchements statiques de tous les modules ni la suspension.

Les signalements [#1378, NVIDIA 595.91.07 et suspension Wayland](https://github.com/NVIDIA/open-gpu-kernel-modules/issues/1378) et [595.91.07, défaut DMA sur RTX 3070 Ti](https://forums.developer.nvidia.com/t/595-91-07-kernel-null-deref-gpf-in-dmaallocmapping-gm107-path-rtx-3070-ti/384575) concernent d’autres GPU/configurations et sont des retours utilisateurs, pas une causalité objtool démontrée. Aucun retour primaire consulté ne valide exactement Quadro RTX 5000 + Macmini8,1/T2 + 6.18.54 + eGPU Thunderbolt + 595.91.07. L’absence de correspondance n’est pas une preuve d’incompatibilité.

## 7. GSP et Thunderbolt : risques distincts

Les modules ouverts prennent en charge Turing et nécessitent GSP. nvidia annonce `nvidia/595.91.07/gsp_tu10x.bin`, présent (30 073 728 octets), ainsi que gsp_ga10x.bin (72 873 968 octets). Version cohérente ne signifie pas initialisation réussie : échange RPC, allocation DMA, reset et disponibilité du GPU doivent être observés. Ne pas proposer la désactivation GSP comme contournement pour cette variante ouverte. [Modules ouverts NVIDIA](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/kernel_open.html), [firmware GSP](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/gsp.html).

Le tunnel Thunderbolt, les BAR, l’IOMMU, l’alimentation et la gestion runtime PM ajoutent des chemins non exercés par une compilation. Les BAR correctement attribuées en 04P ne prouvent pas leur état lors du prochain branchement. NVIDIA documente les eGPU et avertit du risque d’instabilité lors d’un retrait à chaud ; les règles X11 de cette documentation ne certifient pas le comportement GNOME Wayland. [Documentation eGPU](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/egpu.html).

L’autochargement via modalias/udev est possible dès le branchement. Le paquet calcul ne garantit pas que modeset/DRM resteront absents : les cinq modules sont installés, et l’ouverture d’un périphérique peut déclencher des chargements supplémentaires. Intel doit rester maître de l’affichage et cela doit être vérifié, sans improviser de blacklist ni de configuration graphique pendant l’essai. Le problème connu de masquage Intel au démarrage Core connecté demeure hors de cet audit.

## 8. Niveau de preuve et critères de blocage

| Classe | Constat | Décision |
|---|---|---|
| Connus, sans effet opérationnel démontré ici | Portabilité defined, six prototypes, absence BTF T2 | Pas de blocage isolé |
| Nécessitent qualification | Retours RETHUNK réellement ordinaires ; références !ENDBR .eh_frame ; initialisation GSP et DMA/Thunderbolt | Essai surveillé seulement, durcissement incomplet reconnu |
| Défaut concret recherché, non retrouvé aux sites contrôlés | Sites freezer_active restant JMP, défaut #1095 | Pas de blocage établi par ce contrôle ciblé |
| Bloquants si observés ultérieurement | BUG/Oops/panic, exception IBT, unknown symbol/invalid module format, échec signature exigée, GSP/RPC timeout persistant, AER fatal, faute IOMMU, Xid, perte i915/SSH, module différent des empreintes auditées | Arrêt des essais et décision humaine, sans correction automatique |

DKMS installed, vermagic et version corrects attestent la construction/l’installation. Les métadonnées de signature ne vérifient pas cryptographiquement chaque signature ni son acceptation par le chargeur. Une signature signe aussi un binaire avec lacunes de mitigation ; elle n’en certifie pas le comportement. `retpoline: Y` n’est pas un certificat de conformité RETHUNK/IBT. La décision GO conditionnel est un jugement d’ingénierie limité à la qualification, fondé sur l’origine identique des avertissements, l’explication mainteneur et les contrôles ELF, et non une compatibilité opérationnelle déjà démontrée.

## 9. Conditions précises de la future Mission 05C — aucune exécutée

1. Autorisation explicite distincte pour brancher le Core et accepter que le probe puisse se produire automatiquement ; présence d’un opérateur local, SSH indépendant du GPU et sauvegardes 05B disponibles. Si une indisponibilité même temporaire est inacceptable, **NO-GO pour l’essai**.
2. Avant branchement : même noyau T2, mêmes versions/empreintes auditées, état i915/SDDM/GNOME/SSH sain ; Core absent ; persistance désactivée ; aucun Ollama/CUDA ni tâche GPU. Toute divergence impose une revue préalable.
3. Préparer une capture horodatée du journal noyau et de l’inventaire PCIe, relever boot ID et état Intel avant l’action. Ce rapport ne lance pas la capture ni le branchement.
4. Prévoir une fenêtre empêchant toute mise en veille/hibernation et tout retrait du Core durant l’essai. Si la veille automatique ne peut être exclue dans l’état courant, la préparation d’une inhibition temporaire devra être explicitement comprise dans 05C ; aucune modification de service ici.
5. Premier palier : branchement unique, observation du probe et de GSP au repos, sans boucle de chargement/déchargement forcé et sans CUDA. Puis, seulement si les journaux et Intel restent sains, une validation nvidia-smi limitée selon l’autorisation 05C. Ni le branchement ni nvidia-smi ne sont autorisés par 05B-A.
6. Contrôler PCI/BAR/driver, modules réellement chargés, version et état GPU, absence des signatures de blocage ci-dessus, maintien de SSH et de l’affichage HDMI Intel. Stabilisation d’au moins dix minutes au repos proposée ; ce délai ne prouve pas la stabilité sous charge.
7. Au premier défaut : interrompre l’escalade des tests ; conserver les traces si accessible ; aucune déconnexion à chaud, reset, rescan, modification de mitigation ou retour arrière automatique. Une éventuelle récupération nécessite une décision distincte adaptée à l’état.
8. Après succès au repos : CUDA progressif dans une étape séparément autorisée avant Ollama. Aucun service IA exposé ni code GPU non fiable avant qualification ; pas de garantie complète de sécurité du pilote. La veille et le retrait à chaud restent non qualifiés et hors du GO proposé.

## 10. Limites et méthode reproductible

Tous les modules ont été lus depuis `/lib/modules/<noyau>/updates/dkms/*.ko.xz`. Décompression en mémoire avec Python/lzma, descripteur memfd, lecture par readelf/nm/objdump et analyse ELF64 little-endian via struct. Aucune copie décompressée sur disque, aucun appel à objtool sur les binaires (cet outil peut les modifier), aucun accès à la mémoire d’un module chargé.

La comparaison warnings utilise les multiensembles de suffixes commençant à `warning:` : elle conserve message, symbole et offset mais retire le chemin de compilation. La présence de sections ELF n’est pas une validation exhaustive de leurs entrées. Seuls les sept sites jump_table de modeset T2 / cinq Debian et les retours représentatifs cités ont été examinés au niveau instructions. Aucun test d’exécution, signature cryptographique complète ou audit exhaustif des cibles indirectes. La liste intégrale des diagnostics reste dans les deux make.log référencés, les objets intermédiaires ne sont pas disponibles pour une remontée source exhaustive.

## 11. Relevé actuel des modules et sections

Les tailles ci-dessous sont en octets dans l’ELF décompressé ; `.return_sites` utilise des entrées de quatre octets, qui ne recensent pas les retours ordinaires non instrumentés. Empreintes calculées sur les fichiers .ko.xz installés. Les contrôles ne chargent rien.

| Noyau | Module | return_sites | orc_unwind | ibt_endbr_seal | jump_table |
|---|---|---:|---:|---:|---:|
| 6.12.111+deb13-amd64 | nvidia-drm.ko.xz | 748 | 10824 | 192 | 48 |
| 6.12.111+deb13-amd64 | nvidia-modeset.ko.xz | 280 | 230850 | 240 | 80 |
| 6.12.111+deb13-amd64 | nvidia-peermem.ko.xz | 8 | 24 | 0 | 0 |
| 6.12.111+deb13-amd64 | nvidia-uvm.ko.xz | 8412 | 116892 | 3668 | 1616 |
| 6.12.111+deb13-amd64 | nvidia.ko.xz | 4320 | 717570 | 21428 | 208 |
| 6.18.54-1-t2-trixie | nvidia-drm.ko.xz | 752 | 10806 | 192 | 64 |
| 6.18.54-1-t2-trixie | nvidia-modeset.ko.xz | 280 | 230844 | 240 | 112 |
| 6.18.54-1-t2-trixie | nvidia-peermem.ko.xz | 8 | 24 | 0 | 0 |
| 6.18.54-1-t2-trixie | nvidia-uvm.ko.xz | 8444 | 116868 | 3668 | 1632 |
| 6.18.54-1-t2-trixie | nvidia.ko.xz | 4216 | 714792 | 21428 | 448 |

- `6.12.111+deb13-amd64/nvidia-drm.ko.xz` : SHA-256 `6961038156d75d74770d42d3968cbefabcbef7459732f8a1af2cf96d2cc4d88b` ; version `595.91.07` ; vermagic `6.12.111+deb13-amd64 SMP preempt mod_unload modversions` ; signer `DKMS module signing key` ; hash signature `sha256` ; licence `Dual MIT/GPL`.
- `6.12.111+deb13-amd64/nvidia-modeset.ko.xz` : SHA-256 `7e61d9267be468d6e48ddccb88f3138b49018c240dfa3cfef4127f0130f7ae95` ; version `595.91.07` ; vermagic `6.12.111+deb13-amd64 SMP preempt mod_unload modversions` ; signer `DKMS module signing key` ; hash signature `sha256` ; licence `Dual MIT/GPL`.
- `6.12.111+deb13-amd64/nvidia-peermem.ko.xz` : SHA-256 `d97eb461e2fadd8137aef22a6f66dd3ea84510acaf69ab7bf293896f9cda2061` ; version `595.91.07` ; vermagic `6.12.111+deb13-amd64 SMP preempt mod_unload modversions` ; signer `DKMS module signing key` ; hash signature `sha256` ; licence `Dual BSD/GPL`.
- `6.12.111+deb13-amd64/nvidia-uvm.ko.xz` : SHA-256 `a3d73c6bba26f1817fdf2d59416619eb95c55f6b0592d3b7515dc910f0692e20` ; version `595.91.07` ; vermagic `6.12.111+deb13-amd64 SMP preempt mod_unload modversions` ; signer `DKMS module signing key` ; hash signature `sha256` ; licence `Dual MIT/GPL`.
- `6.12.111+deb13-amd64/nvidia.ko.xz` : SHA-256 `e61e72d37ea68e32cfea700306cffd1b29b801f60fa5d109975dee8f8fb878f8` ; version `595.91.07` ; vermagic `6.12.111+deb13-amd64 SMP preempt mod_unload modversions` ; signer `DKMS module signing key` ; hash signature `sha256` ; licence `Dual MIT/GPL`.
- `6.18.54-1-t2-trixie/nvidia-drm.ko.xz` : SHA-256 `ee0dc46492998eb34353116d31bbc4b2c4fd9119cd138b15306a81ed96af4b26` ; version `595.91.07` ; vermagic `6.18.54-1-t2-trixie SMP preempt mod_unload modversions` ; signer `DKMS module signing key` ; hash signature `sha256` ; licence `Dual MIT/GPL`.
- `6.18.54-1-t2-trixie/nvidia-modeset.ko.xz` : SHA-256 `de8ab8b72fabdb3c2849e69c9b3f8682eb6d9fe48a41242eacc09d0d164a38cb` ; version `595.91.07` ; vermagic `6.18.54-1-t2-trixie SMP preempt mod_unload modversions` ; signer `DKMS module signing key` ; hash signature `sha256` ; licence `Dual MIT/GPL`.
- `6.18.54-1-t2-trixie/nvidia-peermem.ko.xz` : SHA-256 `2a84d2a80d53a46fbc2158561c6cf2bbe141a0776f8990f6cceeefbd080e5389` ; version `595.91.07` ; vermagic `6.18.54-1-t2-trixie SMP preempt mod_unload modversions` ; signer `DKMS module signing key` ; hash signature `sha256` ; licence `Dual BSD/GPL`.
- `6.18.54-1-t2-trixie/nvidia-uvm.ko.xz` : SHA-256 `15812b7f78bcfa6d4a91acb4b72f6af4e776618ebea0e7274f24aa82f544e70a` ; version `595.91.07` ; vermagic `6.18.54-1-t2-trixie SMP preempt mod_unload modversions` ; signer `DKMS module signing key` ; hash signature `sha256` ; licence `Dual MIT/GPL`.
- `6.18.54-1-t2-trixie/nvidia.ko.xz` : SHA-256 `91bf2ad5041a118f9e6a6333e49ed022dd836b760b521cd1f2e5b5717985d662` ; version `595.91.07` ; vermagic `6.18.54-1-t2-trixie SMP preempt mod_unload modversions` ; signer `DKMS module signing key` ; hash signature `sha256` ; licence `Dual MIT/GPL`.

**Recommandation finale : GO sous les conditions de la section 9, exclusivement pour un premier essai surveillé à autoriser en 05C. Aucun GO production, CUDA ou branchement n’est exécuté par cet audit.**

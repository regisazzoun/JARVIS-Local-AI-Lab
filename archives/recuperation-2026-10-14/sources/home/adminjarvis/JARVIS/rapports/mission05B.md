# JARVIS — Mission 05B : installation contrôlée NVIDIA

12 octobre 2026, Europe/Paris. Installation autorisée par l’utilisateur, exécutée dans le périmètre de mission05B-P.md. **Core absent pendant toute la mission ; aucun redémarrage/arrêt, aucune connexion/déconnexion, aucun chargement volontaire NVIDIA, aucun nvidia-smi/CUDA/Ollama, aucun rescan/écriture PCI/DEVEN, aucune modification GRUB/EFI/NVRAM ou du rôle Intel.**

## 1. Résultat et recommandation

**Installation terminée avec succès : NVIDIA 595.91.07-1, modules ouverts DKMS, composants de calcul.** APT retourne **0** ; dpkg cohérent ; **29 ajouts exacts au total, aucun paquet préexistant modifié ou supprimé**. DKMS est **installed** pour **6.12.111+deb13-amd64** et **6.18.54-1-t2-trixie**. Les cinq modules de chaque noyau sont présents, de version et vermagic corrects. Firmware GSP cohérent.

**JARVIS reste démarré et accessible en SSH, avec Intel i915 et GNOME Wayland actifs.** Le processus gnome-shell conserve son PID **1270**. SDDM et SSH sont actifs. `nvidia-persistenced` est **disabled / inactive, MainPID=0**, masque runtime retiré. Aucun module NVIDIA ni nouveau chargé, Core toujours absent de l’inventaire.

**Recommandation : NO-GO immédiat pour connecter le Razer Core.** Les contrôles structurels d’installation réussissent, mais les builds émettent **14 060 lignes warning par noyau**, dont **13 782 diagnostics objtool sur des retours « naked » dans un build MITIGATION_RETHUNK**. Ces avertissements ne sont pas des erreurs de compilation, mais leur portée sur le binaire exact et ses mitigations n’est pas qualifiée. Je recommande un audit en lecture seule avant d’autoriser le chargement/hotplug en Mission 05C. Ce choix de prudence ne démontre ni un crash futur ni une vulnérabilité exploitable sur JARVIS.

Aucun correctif, rebuild de réparation, changement de branche, désactivation de mitigation ou rollback automatique appliqué. **Attente d’une décision et d’une autorisation distincte pour toute suite.**

## 2. État initial et sauvegarde

Boot ID avant/après : **d8f67bde-f785-4365-99ed-1af19afe9620** ; noyau **6.18.54-1-t2-trixie** et cmdline inchangés. Avant modification :

- aucun périphérique NVIDIA dans lspci ; Core absent de l’inventaire ;
- Intel **0000:00:02.0, 8086:3e9b**, pilote i915 ; GNOME Wayland session 5 active, gnome-shell présent ;
- SDDM, ssh.service et ssh.socket actifs ; session SSH de travail opérationnelle ;
- headers T2 exacts, GCC 14.2.0-19, DKMS Debian 3.2.2-1~deb13u1 ; aucun module DKMS enregistré ;
- Secure Boot désactivé, lockdown none ;
- environ **397 Gio libres sur /** et **604 Mio sur /boot**, contrôles d’espace réussis ;
- audit dpkg initial vide.

La procédure **sauvegarde-proposee.sh** préparée en 05B-P a été **exécutée avant modification**. Dossier réel :

```text
/home/adminjarvis/JARVIS/rapports/mission05B-sauvegarde-20261012-171120
```

Sauvegarde validée : **configurations.tgz lisible**, inventaire tar archivé dans les preuves, présence des arbres APT/modprobe/DKMS/systemd/initramfs/kernel/X11 et état DKMS ; paquets, manuels/holds et états de services enregistrés ; copie du statut dpkg ; **trois initramfs** copiés et leurs SHA-256 comparés avec les originaux, tous concordants. Compte/groupe nvidia-persistenced absents initialement. Le dossier est en mode 0700 ; aucune clé privée DKMS existante à copier à ce stade.

Empreintes de référence complètes dans **boot-sha256.txt** du dossier de sauvegarde :

| Fichier | SHA-256 initial |
|---|---|
| /boot/grub/grub.cfg | `9bc2c064607d7daa3438da38e9f7808e71060aa6430c32af3decb3adbf5d7726` |
| /boot/vmlinuz-6.18.54-1-t2-trixie | `a41e1a7680c5d76761a744d4265b7901bbd7494e90340fda1eb59eec73d72d1b` |
| /boot/initrd.img-6.18.54-1-t2-trixie | `4c7fe763f3f05300e03c270aa24d2c5b90a55cbd26547898a3c1ca3f44507cc0` |

Preuves : preflight.json, sauvegarde-execution.txt, sauvegarde-validation.json, sauvegarde-archive-inventaire.txt, sauvegarde-empreintes.txt.

## 3. Préparation APT et paquets réellement installés

Les 29 archives précédemment inspectées ont été revérifiées par SHA-256 avant utilisation. Seuls les fichiers d’amorçage approuvés ont été installés :

1. **/etc/apt/preferences.d/00-jarvis-nvidia-isolation**, copie du texte validé ;
2. **cuda-keyring 1.1-1**, depuis l’archive Debian 13 inspectée ;
3. **nvidia-driver-pinning-595 595-1**, depuis l’archive inspectée ;
4. `apt-get update --error-on=any`, succès sans incohérence de signature.

Le dépôt ajouté est exclusivement **https://developer.download.nvidia.com/compute/cuda/repos/debian13/x86_64/**, avec signed-by vers la clé fournie par cuda-keyring. Aucun contrib/non-free/backports/sid/Ubuntu ajouté. L’isolation laisse les candidats **DKMS 3.2.2-1~deb13u1** et **libxnvctrl0 535.171.04-1+b2** inchangés et sélectionne R595.

La simulation **réelle** avec les index système actualisés et les versions imposées retourne : **0 upgraded, 27 newly installed, 0 to remove, 0 not upgraded**. Une seconde simulation avec les chemins des .deb locaux donne exactement les mêmes 27 ajouts. Les versions des paquets préexistants ont été comparées avec la sauvegarde avant de poursuivre : aucun changement ; seuls keyring et pin étaient ajoutés.

Le masque runtime de **nvidia-persistenced.service** a ensuite été créé et sa cible /dev/null vérifiée. L’installation a reçu les **27 archives locales approuvées**, avec **CC=/usr/bin/gcc-14 et CXX=/usr/bin/g++-14**, apt-get --yes --no-install-recommends --no-remove. APT a néanmoins choisi de récupérer les mêmes versions depuis les dépôts (~255 Mo), du fait de sa résolution/priorité ; aucun changement de version ni ajout de paquet hors manifeste. La sortie complète conserve ces récupérations. Les arguments exacts sont enregistrés dans **installation-resultat.json**.

Début transaction : **2026-10-12T17:15:56.717137+02:00**. Fin : **2026-10-12T17:20:56.728641+02:00**. Code retour : **0**.

### Liste exacte : 29 ajouts, zéro remplacement

| Paquet installé | Version |
|---|---|
| cuda-keyring | `1.1-1` |
| firmware-nvidia-gsp | `595.91.07-1` |
| libcuda1:amd64 | `595.91.07-1` |
| libcudadebugger1:amd64 | `595.91.07-1` |
| libelf-dev:amd64 | `0.192-4` |
| libnvcuvid1:amd64 | `595.91.07-1` |
| libnvidia-cfg1:amd64 | `595.91.07-1` |
| libnvidia-encode1:amd64 | `595.91.07-1` |
| libnvidia-fbc1:amd64 | `595.91.07-1` |
| libnvidia-gpucomp:amd64 | `595.91.07-1` |
| libnvidia-ml1:amd64 | `595.91.07-1` |
| libnvidia-nvvm4:amd64 | `595.91.07-1` |
| libnvidia-nvvm704:amd64 | `595.91.07-1` |
| libnvidia-opticalflow1:amd64 | `595.91.07-1` |
| libnvidia-pkcs11-openssl3:amd64 | `595.91.07-1` |
| libnvidia-present:amd64 | `595.91.07-1` |
| libnvidia-ptxjitcompiler1:amd64 | `595.91.07-1` |
| libnvidia-sandboxutils:amd64 | `595.91.07-1` |
| libnvidia-tileiras:amd64 | `595.91.07-1` |
| libnvoptix1:amd64 | `595.91.07-1` |
| libzstd-dev:amd64 | `1.5.7+dfsg-1` |
| nvidia-driver-cuda | `595.91.07-1` |
| nvidia-driver-pinning-595 | `595-1` |
| nvidia-kernel-open-dkms | `595.91.07-1` |
| nvidia-kernel-support | `595.91.07-1` |
| nvidia-modprobe | `595.91.07-1` |
| nvidia-opencl-icd:amd64 | `595.91.07-1` |
| nvidia-persistenced | `595.91.07-1` |
| zlib1g-dev:amd64 | `1:1.3.dfsg+really1.3.1-1+b1` |


Les 26 ajouts NVIDIA comprennent keyring/pin, modules, firmware et bibliothèques de calcul ; les 3 ajouts Debian sont libelf-dev, libzstd-dev et zlib1g-dev. Aucun CUDA Toolkit complet, pilote graphique NVIDIA complet, composant i386 ou Ollama installé. **Paquets préexistants changés : aucun**, selon paquets-difference.json. Les noyaux, headers, Mesa, GNOME, SDDM, SSH et paquets T2 conservent leurs versions/états initiaux.

## 4. DKMS : résultats par noyau

La configuration locale **autoinstall_all_kernels=yes** a bien entraîné les deux builds attendus, sans commande de réparation additionnelle. Commande du maintscript enregistrée dans chaque make.log : make -j12, KERNEL_UNAME propre à la cible ; GCC/G++ 14 fournis via l’environnement. Les flags IGNORE_PREEMPT_RT_PRESENCE/IGNORE_XEN_PRESENCE proviennent du paquet inspecté et n’ont pas été ajoutés comme correction locale.

| Noyau | Début enregistré dans make.log | Résultat build | Durée build | État DKMS |
|---|---|---|---|---|
| 6.12.111+deb13-amd64 | 17:17:04 CEST | **exit code 0** | **1 min 36 s** | **installed** |
| 6.18.54-1-t2-trixie | 17:18:51 CEST | **exit code 0** | **1 min 35 s** | **installed** |

Modules construits, signés puis installés dans **/lib/modules/<noyau>/updates/dkms/** ; depmod terminé pour chaque cible. `dkms status` :

```text
nvidia/595.91.07, 6.12.111+deb13-amd64, x86_64: installed
nvidia/595.91.07, 6.18.54-1-t2-trixie, x86_64: installed
```

| Noyau | Module | Version | Vermagic |
|---|---|---|---|
| 6.12.111+deb13-amd64 | nvidia | 595.91.07 | `6.12.111+deb13-amd64 SMP preempt mod_unload modversions` |
| 6.12.111+deb13-amd64 | nvidia_modeset | 595.91.07 | `6.12.111+deb13-amd64 SMP preempt mod_unload modversions` |
| 6.12.111+deb13-amd64 | nvidia_drm | 595.91.07 | `6.12.111+deb13-amd64 SMP preempt mod_unload modversions` |
| 6.12.111+deb13-amd64 | nvidia_uvm | 595.91.07 | `6.12.111+deb13-amd64 SMP preempt mod_unload modversions` |
| 6.12.111+deb13-amd64 | nvidia_peermem | 595.91.07 | `6.12.111+deb13-amd64 SMP preempt mod_unload modversions` |
| 6.18.54-1-t2-trixie | nvidia | 595.91.07 | `6.18.54-1-t2-trixie SMP preempt mod_unload modversions` |
| 6.18.54-1-t2-trixie | nvidia_modeset | 595.91.07 | `6.18.54-1-t2-trixie SMP preempt mod_unload modversions` |
| 6.18.54-1-t2-trixie | nvidia_drm | 595.91.07 | `6.18.54-1-t2-trixie SMP preempt mod_unload modversions` |
| 6.18.54-1-t2-trixie | nvidia_uvm | 595.91.07 | `6.18.54-1-t2-trixie SMP preempt mod_unload modversions` |
| 6.18.54-1-t2-trixie | nvidia_peermem | 595.91.07 | `6.18.54-1-t2-trixie SMP preempt mod_unload modversions` |


Le module principal de chaque noyau annonce **Dual MIT/GPL**, signer **DKMS module signing key**. Le DKMS a créé **/var/lib/dkms/mok.key (0600)** et **mok.pub (0644)** et signé les modules. Aucun enrôlement MOK/import NVRAM n’a été exécuté ; Secure Boot reste disabled. Les métadonnées sont archivées, **pas le contenu de la clé privée**.

Journaux complets originaux :

- `/var/lib/dkms/nvidia/595.91.07/6.12.111+deb13-amd64/x86_64/log/make.log` ; copie **dkms-make-0.txt** ;
- `/var/lib/dkms/nvidia/595.91.07/6.18.54-1-t2-trixie/x86_64/log/make.log` ; copie **dkms-make-1.txt**.

**Aucune ligne d’erreur de compilation détectée**, make exit 0 pour les deux ; avertissements détaillés au §8. La cible T2 signale aussi **BTF generation skipped due to unavailability of vmlinux** : modules produits et installés, mais métadonnées BTF non générées pour cette cible. Aucun vmlinux ou outil installé pour changer cela.

Firmware : **/lib/firmware/nvidia/595.91.07/gsp_tu10x.bin** et **gsp_ga10x.bin** présents ; `dpkg --verify firmware-nvidia-gsp` sans différence ; déclarations firmware de modinfo nvidia concordantes. Les SHA-256 et tailles sont dans firmware-verification.json. **Aucune initialisation matérielle GSP testée.**

## 5. Initramfs régénéré

Le trigger différé initramfs-tools s’est exécuté normalement après les builds, et a régénéré **/boot/initrd.img-6.18.54-1-t2-trixie**. Nouveau fichier : **91 033 069 octets**. SHA-256 final :

```text
cd674a39e2872c93477ab6bd2ee06ac52a587059e88877feba8d68dbd964d82e
```

`lsinitramfs` réussit avant/après. Inventaire : **1 933 entrées avant**, **1 934 après**, **aucune entrée supprimée**, seul chemin ajouté **etc/modprobe.d/nvidia.conf**. La comparaison est dans initramfs-comparaison.json ; les contenus de fichiers générés, notamment dépendances de modules, peuvent changer sans modifier la liste des chemins.

Composants indispensables retrouvés : **init**, scripts/local, **usr/sbin/lvm**, **usr/sbin/dmsetup**, configuration/règles udev LVM, modules **dm-mod, nvme, ext4 et i915** du noyau exact. Les composants Apple/HID préexistants sont conservés. Le stockage ANS2 Apple T2 utilise le NVMe du noyau T2 conservé ; aucune substitution de pilote stockage.

**Précision T2 :** les modules t2bce_core/dma/vhci/audio ne figuraient déjà pas dans l’initrd fonctionnel sauvegardé et ne figurent pas dans le nouveau. Il ne s’agit pas d’une suppression par l’installation. Ils restent **présents sur le système et chargés dans le boot actuel**, comme avant ; t2-verification.json atteste leur conservation. Aucun ajout manuel initramfs n’a été fait pour transformer cette situation initiale.

Les modules graphiques NVIDIA DKMS ne sont pas incorporés au nouvel initrd selon l’inventaire ; les chemins forcedeth/typec_nvidia retrouvés sont des modules noyau préexistants, **pas le pilote GPU NVIDIA nouvellement installé**. Seule la configuration blacklist/options NVIDIA a été ajoutée à l’archive.

GRUB et vmlinuz ont **exactement leurs SHA-256 initiaux**. Aucun autre initrd ne devait être régénéré ; les trois copies initiales restent disponibles. Cette validation contrôle lisibilité, inventaire et présence des composants de boot ; **elle ne remplace pas un essai de redémarrage**, interdit ici.

## 6. Intel, GNOME et SSH après installation

Les contrôles structurels automatisés regroupés dans **validation-complete.json** donnent **34 critères réussis, zéro critère échoué**. Contrôles complémentaires T2 et clôture :

- même boot ID, même noyau et cmdline ;
- Intel 00:02.0 toujours lié à i915 ; i915 chargé ;
- modules t2bce_core/dma/vhci/audio toujours chargés ;
- GNOME Wayland session 5 active ; gnome-shell même PID 1270, sans redémarrage ;
- SDDM, SSH et socket SSH actifs ; accès SSH utilisé jusqu’à la clôture ;
- interrogation **en lecture seule** de Mutter GetCurrentState réussie : moniteur **LG TV**, connecteur logique **DP-3**, mode courant **1920×1080 à 60 Hz** ; affichage Intel conservé dans le contexte HDMI du Mac ;
- aucun périphérique NVIDIA dans PCIe ; aucun module NVIDIA/nouveau chargé ;
- journal noyau depuis le début de la transaction : **aucune nouvelle entrée conservée**, aucune trace d’un chargement GPU inattendu ;
- état dpkg final cohérent ; environ **395 Gio libres sur /** et **604 Mio sur /boot**.

Il s’agit de contrôles logiciels du bureau/moniteur, sans observation visuelle externe supplémentaire. **Aucune commande nvidia-smi, CUDA, Ollama, modprobe NVIDIA ou insmod exécutée.** Modinfo ne fait que lire les modules sur disque.

## 7. Modifications persistantes réellement réalisées

| Élément | État obtenu |
|---|---|
| Dépôt/keyring | Source NVIDIA Debian 13, keyring signé prévu, index APT système actualisés |
| Politiques APT | 00-jarvis-nvidia-isolation + nvidia-driver-pin, branche R595 ; DKMS/libxnvctrl0 non promus |
| Paquets | Les 29 ajouts du §3, aucun autre |
| Sources/modules DKMS | /usr/src/nvidia-595.91.07, état/logs sous /var/lib/dkms ; 5 modules signés sur chacun des 2 noyaux, métadonnées depmod actualisées |
| Signature locale | mok.key/mok.pub créés ; aucun enrôlement EFI/MOK |
| Firmware/bibliothèques | GSP 595.91.07, CUDA Driver API/NVML et dépendances ; cache ldconfig actualisé |
| Modprobe | nvidia.conf : blacklist nouveau/nova-core, TemporaryFilePath=/var/tmp, EnableS0ixPowerManagement=1, PreserveVideoMemoryAllocations=1 |
| Udev | 60-nvidia.rules du paquet, avec helper et runtime PM au futur bind GPU ; aucun bind GPU NVIDIA durant la mission |
| Utilitaire | nvidia-modprobe installé setuid root par le paquet, non exécuté par l’agent |
| Persistance | Compte/groupe système nvidia-persistenced créés ; unité/preset présents, **service disabled/inactive** |
| Initramfs | Initrd T2 régénéré, sauvegarde initiale intacte |

Protection runtime : masque appliqué avant installation, puis **systemctl disable --now nvidia-persistenced.service** et **unmask --runtime** exécutés conformément au plan. Le masque est retiré ; **aucun PID de persistance**, état final disabled/inactive. Aucun autre service arrêté/redémarré par nos commandes.

Aucune modification de GRUB, EFI/NVRAM, ACPI, cmdline, PCIe/DEVEN, i915 ou de la configuration GNOME/SDDM/SSH. Les éventuels traitements de cache/documents et notifications des hooks APT sont des effets ordinaires de la transaction approuvée ; journaux complets conservés.

## 8. Anomalies et portée des preuves

### A. Avertissements objtool : à qualifier avant chargement

Chaque make.log contient **14 060 lignes warning** ; **13 782** correspondent à :

```text
objtool: 'naked' return found in MITIGATION_RETHUNK build
```

D’autres diagnostics incluent des relocalisations vers des cibles **!ENDBR**, des prototypes manquants et quelques avertissements de portabilité du préprocesseur. Les adresses/symboles varient ; les nombres sont des **lignes de diagnostic**, pas un décompte de 14 060 défauts indépendants. Le noyau T2 et le noyau Debian ont CONFIG_X86_KERNEL_IBT et CONFIG_MITIGATION_RETHUNK activés.

Un collaborateur NVIDIA reconnaît dans [l’issue officielle #1077](https://github.com/NVIDIA/open-gpu-kernel-modules/issues/1077) un problème de compilation de la partie indépendante de l’OS avec les flags de return thunk ; la sévérité warning/error dépend de la configuration objtool. Le signalement concerne une autre version/un autre noyau : **il ne certifie pas l’innocuité des modules exacts de JARVIS**. Aucun contournement proposé dans ce fil n’a été appliqué ici ; aucun patch, rebuild, changement de kernel flags ou désactivation d’IBT/mitigation.

La réussite DKMS et la signature attestent la construction/installation, **pas la validation complète du contrôle de flot ni l’exécution sans défaut**. L’installation est conservée sans chargement, et je recommande d’examiner les diagnostics avant la prochaine expérience.

### B. Message du preset de persistance

Le maintscript affiche **Failed to preset unit … is masked**, puis un message deb-systemd-helper « systemctl preset failed » et indique ne pas démarrer le service. Ces messages sont provoqués par la protection runtime prévue ; **APT et le paquet terminent avec succès**, service jamais actif observé. La commande disable sous masque affiche également qu’il ignore cette unité masquée ; après unmask, l’état effectif a bien été contrôlé **disabled/inactive**. Aucune correction hors procédure n’a été nécessaire.

### C. BTF et taint

La cible T2 manque d’un vmlinux disponible pour générer BTF ; modules .ko.xz créés/signés malgré ce message. Aucun outil supplémentaire installé.

Le taint noyau relevé après installation vaut **1024** ; aucune mesure initiale de ce champ n’a été faite. **Ne pas l’attribuer à NVIDIA** : aucun module NVIDIA chargé et aucune nouvelle entrée noyau depuis le début de la transaction. Son origine/antériorité ne sont pas établies dans cette mission.

### Limites

Aucun test de boot du nouvel initrd, aucun chargement matériel, aucune mesure de fonctionnement GSP/VRAM/CUDA, aucun essai Thunderbolt avec pilote. La compatibilité de construction avec le noyau T2 est maintenant attestée ; **la compatibilité opérationnelle reste non démontrée**. Aucun test structurel n’a échoué ; les avertissements constituent un point de revue supplémentaire, pas une justification pour modifier automatiquement le système.

## 9. Retour arrière adapté à l’état réel — NON EXÉCUTÉ

Les **29 paquets réellement ajoutés**, noms exacts avec architecture quand pertinente, figurent dans **mission05B-preuves/rollback-paquets-reels.txt**. Aucune restauration de version d’un paquet préexistant n’est nécessaire pour cette transaction, puisque leurs versions/états n’ont pas changé.

**Tout rollback demande votre décision et une autorisation distincte.** Core doit rester absent ; vérifier qu’aucun client/module NVIDIA n’a été activé entre-temps. Ne pas déclencher automatiquement apt --fix-broken install, dkms rebuild, rmmod, reboot ou autoremove.

Procédure préparée pour cet état :

1. Relire la sauvegarde **/home/adminjarvis/JARVIS/rapports/mission05B-sauvegarde-20261012-171120**, le manifeste réel et les versions installées ; contrôler qu’aucun des ajouts ne sert désormais à une autre installation.
2. Le service est déjà disabled/inactive. Conserver cet état ; si le contexte a changé, arrêter le rollback pour revue avant toute action sur des clients GPU.
3. Simuler la purge ciblée puis l’exécuter seulement après revue/accord :

```bash
sudo xargs -r -a /home/adminjarvis/JARVIS/rapports/mission05B-preuves/rollback-paquets-reels.txt apt-get -s purge
sudo xargs -r -a /home/adminjarvis/JARVIS/rapports/mission05B-preuves/rollback-paquets-reels.txt apt-get purge
```

La simulation doit ne retirer que les ajouts confirmés ; aucun noyau, header, DKMS Debian préexistant, Mesa, GNOME, SDDM, SSH ou T2. Pas de wildcard nvidia*.

4. Le prerm du DKMS retirera **nvidia/595.91.07 sur les deux noyaux** ; vérifier dkms status et les répertoires updates/dkms. En cas d’orphelin, commande disponible **seulement après diagnostic/accord** : `sudo /usr/sbin/dkms remove -m nvidia -v 595.91.07 --all`. Ne pas toucher aux autres modules.
5. Les scripts de purge traitent service/états helper, retirent firmware/config/udev et déclenchent **update-initramfs -u et ldconfig**. Aucun update-grub nécessaire. La blacklist nouveau de la cmdline préexistait et doit rester inchangée.
6. Purge keyring/pin retire source NVIDIA et nvidia-driver-pin. Retirer **uniquement** le fichier manuel **/etc/apt/preferences.d/00-jarvis-nvidia-isolation** créé par cette mission, après retrait NVIDIA ; vérifier les résidus. Une actualisation APT éventuelle pour nettoyer l’ancien index sera autorisée dans le rollback. Aucune source contrib à supprimer.
7. Compte/groupe nvidia-persistenced absents dans la sauvegarde, désormais créés : les scripts de purge ne les retirent pas. Après retrait du service et vérification qu’ils ne servent plus, supprimer le compte système puis le groupe restant, sans --remove-home global. Les fichiers runtime/logs associés sont à inventorier, pas à effacer globalement.
8. **mok.key/mok.pub** ont été créés dans cette transaction alors que /var/lib/dkms était vide. Après retrait NVIDIA, vérifier qu’aucun autre module DKMS/signature ne les utilise ; seulement dans ce cas, retirer ces deux fichiers exacts et les artefacts NVIDIA résiduels. Aucun MOK enrôlé à retirer de NVRAM.
9. Vérifier le contenu du nouvel initrd généré par la purge. Pour retrouver exactement la référence antérieure, si aucun changement ultérieur d’initramfs/noyau/firmware n’est intervenu, restauration préparée :

```bash
sudo cp --preserve=all /home/adminjarvis/JARVIS/rapports/mission05B-sauvegarde-20261012-171120/initrd.img-6.18.54-1-t2-trixie /boot/initrd.img-6.18.54-1-t2-trixie
sudo sha256sum /boot/initrd.img-6.18.54-1-t2-trixie /boot/vmlinuz-6.18.54-1-t2-trixie /boot/grub/grub.cfg
```

Exiger le SHA-256 initrd initial **4c7fe763…** complet au §2. Pas de restauration globale /etc ou /boot, pas d’écrasement du statut dpkg. Les deux autres initrd sauvegardés restent des références ; ne pas les restaurer automatiquement.
10. Contrôler dpkg, DKMS, absence NVIDIA, i915/GNOME/SDDM/SSH et empreintes. Comme aucun NVIDIA n’a été chargé ici, aucun retrait de module ou reboot n’est actuellement requis pour cette désinstallation proposée. Si un chargement a lieu dans une mission ultérieure, adapter ce point avant de purger.

**Rollback non exécuté. Installation conservée, système stable, en attente de décision.**

## 10. Preuves et clôture

Dossier : **/home/adminjarvis/JARVIS/rapports/mission05B-preuves/**. Les fichiers essentiels sont installation-complete.log, installation-resultat.json, paquets-difference.json, dkms-final.txt, modules-verification.json, les deux make.log copiés, dkms-logs-analyse.json, avertissements-dkms-synthese.txt, firmware-verification.json, initramfs-comparaison.json, boot-hashes-final.txt, persistance-configuration-finale.json, gnome-affichage-etat.txt et cloture-etat.txt. SHA256SUMS couvre les preuves ; la clé privée DKMS n’est pas incluse.

**Mission 05B réalisée : installation et contrôles sur disque réussis, affichage Intel et SSH préservés. NO-GO immédiat pour brancher le Core tant que la portée des avertissements objtool n’a pas été qualifiée et qu’une autorisation distincte de Mission 05C n’a pas été donnée.**

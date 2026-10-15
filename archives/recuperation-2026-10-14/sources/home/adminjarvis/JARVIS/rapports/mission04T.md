# JARVIS — Mission 04T : préparation du diagnostic pré-Linux de DEVEN

Date : 12 octobre 2026. Machine : Mac mini 2018 / Macmini8,1, Debian 13 T2Linux, noyau `6.18.54-1-t2-trixie`.

**Statut : préparation uniquement. Aucune expérimentation autorisée ou effectuée. Attente explicite d’une autorisation avant tout redémarrage, changement de branchement ou commande pré-Linux.**

## Décision recommandée

La première méthode à autoriser est une lecture à l’invite du **GRUB existant**, avant de choisir l’entrée Linux, avec `setpci -s 00:00.0 54.L`, répétée et photographiée. Elle ne nécessite ni installation, ni modification GRUB, ni écriture de configuration PCI, ni sauvegarde sur l’EFI. Les modules nécessaires sont présents sur disque ; leur chargement par le GRUB effectivement démarré reste à vérifier lors d’un essai autorisé.

Cette mesure répond à « DEVEN est-il déjà masqué avant Linux ? ». Elle ne suffit pas à répondre à « Apple ou GRUB a-t-il effectué le masquage ? », car le firmware et une partie de GRUB ont déjà fonctionné à l’apparition du menu. Une UEFI Shell démarrée directement constituerait une seconde expérience, avec un chemin de démarrage différent et une compatibilité Mac T2 non démontrée ici.

## 1. État de référence et périmètre de cette préparation

Résultats 04S fournis par l’utilisateur, sans nouvelle lecture matérielle :

| Essai 04S | Core avant démarrage | DEVEN sous Linux | Intel / i915 / graphique |
|---|---|---|---|
| A1 | absent | `0000003f` | présents et fonctionnels |
| B1 | présent | `0000000f` | Intel absent, aucun DRM, aucun greeter |
| A2 | absent | `0000003f` | rétablis |

Même noyau et mêmes paramètres dans les trois essais. La reproductibilité est établie ; l’acteur et le moment de la modification ne le sont pas.

Pour cette mission, seules la documentation publique et des données statiques locales ont été consultées : rapport 04R et preuves déjà archivées, base des paquets, fichiers GRUB, présence des modules. **Aucun `setpci`, `lspci`, relevé PCI/sysfs matériel, redémarrage, montage EFI, installation, chargement de pilote ou changement matériel n’a été exécuté.** La seule écriture de travail est ce rapport. Aucun fichier de démarrage n’a été modifié. Le rapport 04S n’a pas été retrouvé dans les fichiers recherchés ; ses résultats ci-dessus proviennent du contexte utilisateur.

## 2. Possibilités réelles du GRUB installé

Constats statiques :

- Paquets `grub-common`, `grub2-common`, `grub-efi-amd64` et `grub-efi-amd64-bin` : `2.12-9+deb13u2`, installés. Des variantes signée et non signée sont également installées ; cela ne prouve pas laquelle est exécutée.
- `/boot/grub/x86_64-efi/setpci.mod` : présent, 8 144 octets. Même taille dans `/usr/lib/grub/x86_64-efi/setpci.mod` ; l’identité binaire n’a pas été vérifiée.
- `/boot/grub/x86_64-efi/lspci.mod` : présent, 7 136 octets.
- `/boot/grub/grub.cfg` contient l’entrée `jarvis-t2-egpu-np32-pref512`, avec le noyau et l’initrd T2 attendus. Aucune commande `setpci` ni `chainloader` n’apparaît dans ce fichier. Il peut charger un `custom.cfg` ; `/boot/grub/custom.cfg` est absent, mais un autre `config_directory` utilisé au démarrage n’est pas exclu.
- Le préambule charge l’environnement, la vidéo et le thème avant le menu. Il contient des `save_env` conditionnels pour `next_entry` et `prev_saved_entry`. Donc le diagnostic proposé n’ajoute aucune écriture, mais on ne peut pas certifier que **tout le démarrage GRUB existant** est sans écriture.
- Le choix par défaut configuré est le noyau Debian `6.12.111+deb13-amd64`, **pas** l’entrée NP32/PREF512. Il faudra sélectionner manuellement cette dernière, sans changer le défaut.

Le [code GRUB 2.12 de setpci](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/commands/setpci.c) distingue lecture et écriture : sans affectation dans l’argument du registre, il lit ; `.L` demande 32 bits. `-s` utilise bus:device.function, sans domaine. `-d` permet de filtrer l’identité ; `-v` place la lecture dans une variable en mémoire. Une commande inconnue, un module refusé ou une absence de résultat ne valent jamais zéro. La commande est soumise au verrouillage de sécurité éventuel.

Le [backend PCI x86 de GRUB 2.12](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/include/grub/i386/pci.h) adresse les ports CF8/CFC : la lecture écrit le sélecteur d’adresse CF8, puis lit les données CFC. **Ce n’est pas une écriture dans un registre de configuration du périphérique, notamment pas dans DEVEN.** Cette méthode convient au domaine 0 et à l’offset standard 54h ; elle ne constitue pas une méthode générique de lecture des segments PCI multiples. Aucun accès direct improvisé par `outb`, `outl` ou mémoire physique n’est proposé.

`lspci` dans GRUB permet un inventaire, mais ne remplace pas la lecture ciblée de DEVEN. Un nom comme `pcidump`, une syntaxe Linux transposée ou une lecture mémoire à une adresse supposée ne sont pas retenus sans validation. La version du paquet et la présence du module ne prouvent ni le chemin EFI réellement emprunté ni le `$prefix` effectif.

## 3. Signification de DEVEN pour 8086:3ec4

L’identification archivée 04R donne `8086:3ec4`, pont hôte 8e/9e génération. La référence appropriée est le [datasheet Intel Coffee Lake / Coffee Lake Refresh, volume 2, 337345-003, §3.14, pages imprimées 56–58](https://www.intel.com/content/dam/www/public/us/en/documents/datasheets/8th-gen-core-family-datasheet-vol-2.pdf#page=57), registre 32 bits à B0:D0:F0 + 54h. Ne pas utiliser les copies de DEVEN décrites pour les périphériques 2 ou 4.

| Bit | Nom | Valeur 0 | Valeur 1 |
|---|---|---|---|
| 4, masque `0x10` | D2EN | périphérique 2 du bus 0 désactivé et masqué | activé et visible |
| 5, masque `0x20` | D3EN | périphérique 3 du bus 0 désactivé et masqué | activé et visible |

Ces champs sont RW_L, verrouillables par Intel TXT ; une capacité désactivée peut maintenir le bit à zéro. D2 correspond ici au GPU Intel. **D3EN n’est pas un second bit d’activation du GPU Intel** : ne pas lui attribuer une fonction graphique ou une fonction Thunderbolt sans preuve propre à la plateforme.

Calcul sur les observations : `0x3f XOR 0x0f = 0x30`. Les bits 4 **et** 5 changent, de 1 à 0 avec Core. Le masquage Intel est expliqué par D2EN ; la causalité de D3EN reste indéterminée. Les valeurs 04S ne révèlent ni l’auteur des écritures ni l’état des verrous. Aucun essai d’écriture ou de déverrouillage n’est prévu.

## 4. UEFI : outils envisageables et contraintes T2

Une UEFI Shell EDK II/TianoCore **X64**, contenant les commandes PCI, est techniquement candidate. Il faut vérifier le binaire exact, sa provenance, son empreinte, ses commandes intégrées et ses scripts automatiques. Ni présence d’un shell Apple intégré ni fonctionnement d’un binaire Shell particulier sur ce Mac n’ont été démontrés. L’existence de l’UEFI sur cette machine n’est pas une certification de compatibilité Shell.

Le [code EDK II de pci](https://raw.githubusercontent.com/tianocore/edk2/master/ShellPkg/Library/UefiShellDebug1CommandsLib/Pci.c) lit la configuration par `EFI_PCI_ROOT_BRIDGE_IO_PROTOCOL`. Un dump de B0:D0:F0 contient l’offset 54h ; il est plus large que nécessaire et peut aussi lire la configuration étendue suivant la fonction. `mm` permet une lecture ciblée, mais possède aussi un mode d’écriture et un mode interactif : seules l’absence de valeur à écrire et l’option `-n` sont acceptables. Voir [l’aide EDK II](https://raw.githubusercontent.com/tianocore/edk2/master/ShellPkg/Library/UefiShellDebug1CommandsLib/UefiShellDebug1CommandsLib.uni) et [l’implémentation de mm](https://raw.githubusercontent.com/tianocore/edk2/master/ShellPkg/Library/UefiShellDebug1CommandsLib/Mm.c).

Commandes candidates **non exécutées**, à vérifier avec l’aide du binaire retenu avant une mission Shell séparément autorisée :

```text
help pci
help mm
pci 00 00 00 -s 0000
mm 000000000000 -PCI -w 4 -n
mm 000000000054 -PCI -w 4 -n
mm 000000000054 -PCI -w 4 -n
```

Pour `mm -PCI`, l’adresse est segment/bus/device/function/registre : `0000/00/00/00/54`. La lecture à zéro doit donner `3ec48086`. Dans le dump PCI, les quatre octets à 54h seront `3f 00 00 00` ou `0f 00 00 00`, à interpréter en little-endian. Aucune valeur supplémentaire après l’adresse ; ne jamais ouvrir le mode interactif pour cette mission.

Les [protocoles PCI UEFI](https://uefi.org/specs/UEFI/2.10/14_Protocols_PCI_Bus_Support.html) constituent une autre possibilité : une petite application EFI auditée ne lisant que VID/DID et DEVEN, avec sortie console. Elle demanderait compilation, validation et chargement d’un nouveau binaire ; aucun n’a été créé ou installé ici.

Contraintes du chemin Apple :

- T2Linux documente un démarrage EFI, sans mode BIOS sur T2 ; consulter [le guide rEFInd T2Linux](https://wiki.t2linux.org/guides/refind/). Aucun GRUB BIOS ou outil DOS n’est pertinent.
- Les politiques Apple Secure Boot et démarrage externe peuvent interdire un outil EFI non Apple. [Apple décrit ces contrôles](https://support.apple.com/en-au/102522) ; le [guide T2Linux](https://wiki.t2linux.org/guides/preinstall/) explique les exigences pour Linux. Le démarrage Debian actuel ne prouve pas que le démarrage externe est permis. **Ne changer aucune politique** pour cette préparation ; si un futur essai exige un changement, arrêter et demander une autorisation distincte.
- Une Shell lancée depuis GRUB reste **après GRUB**. Une Shell lancée directement via Startup Manager permet une observation sans GRUB, mais change l’entrée EFI, les supports et éventuellement les connexions de pilotes firmware. Elle ne photographie pas le passé du démarrage Debian.
- Le chemin exact peut inclure un autre chargeur ou une image EFI avec configuration intégrée. Aucun inventaire de l’ESP ni de NVRAM n’a été effectué ici. Le [guide Windows T2Linux](https://wiki.t2linux.org/guides/windows/) montre que plusieurs dispositions EFI existent : ne pas supposer que `boot.efi`, shim ou rEFInd sont présents dans le chemin Linux local.
- L’affichage et le clavier disponibles avant Linux dépendent des services firmware. La présence d’un framebuffer EFI ne prouve pas que l’iGPU reste visible en PCI. Aucun port série pré-Linux utilisable n’est établi sur ce Mac mini.

## 5. Conservation des preuves et comparaison des risques

| Méthode | Risque / retour arrière | Fiabilité et limites |
|---|---|---|
| GRUB actuel, lecture ciblée, photographie externe | le plus faible ; aucun ajout persistant ; Échap retourne au menu | conserve le chemin existant ; mesure après initialisation GRUB ; dépend d’un écran et clavier utilisables |
| GRUB, variable `-v` en RAM | faible, disparaît au démarrage suivant | pratique pour l’affichage, pas une archive ; aucune raison de la persister |
| Shell X64 sur support externe, sélection ponctuelle Apple | supérieur ; nouveau support et nouveau chemin ; retrait après arrêt autorisé | observation sans GRUB possible ; compatibilité, politique externe et scripts à valider ; ne prouve pas l’état du chemin Debian |
| Shell chaînée depuis GRUB | supérieur ; ajoute un programme ; pas de persistance nécessaire en principe | reste après GRUB, donc gain causal limité |
| Application EFI minimale auditée | supérieur en préparation ; nouveau binaire à qualifier | accès précis et contrôlable ; même limite de chemin et moment que son point de lancement |
| Modification de grub.cfg, sauvegarde grubenv, NVRAM, installation rEFInd/Shell interne | hors périmètre | inutile pour la première mesure ; risque persistant évitable |
| Lecture Linux / initramfs | simple pour le relevé post-boot | déjà après lancement du noyau ; ne répond pas seule au besoin pré-Linux |

**Capture recommandée : appareil photo ou vidéo externe**, horodatée sur l’appareil de capture, avec identifiant d’essai, état Core, commandes et réponses visibles. Conserver les originaux ; transcrire séparément ; calculer les empreintes sur le poste distant. Cette méthode n’écrit sur aucun volume du Mac et reste indépendante d’une panne graphique après Linux. Si aucun texte nouveau n’est visible, l’essai est « capture impossible », pas « DEVEN=0 ».

GRUB n’offre pas une redirection de fichiers POSIX générale à supposer utilisable ; ne pas essayer `echo ... > ...` pour enregistrer la mesure. `save_env` écrit un bloc d’environnement et ne doit pas servir de journal. Aucun `grub-editenv`, `grub-reboot`, `grub-set-default`, `update-grub`, `grub-install`, `efibootmgr` en écriture, `bless`, `bcfg` ou `setvar` n’est prévu.

La redirection Shell peut écrire un journal sur FAT, mais `fs0:` peut désigner l’ESP interne. Aucun chemin de sauvegarde Shell n’est recommandé tant qu’un support externe dédié n’a pas été identifié sans ambiguïté ; la photographie évite ce risque. Ajouter une clé seulement pour B ajouterait une variable : une future série Shell doit garder le même support présent dans tous ses essais.

Pour conserver le relevé Linux sans écrire de fichiers de preuves sur Debian, préférer la capture de la sortie SSH **sur le poste distant**. Linux et ses services écrivent néanmoins leurs journaux habituels : il ne s’agit pas d’un démarrage globalement sans écriture disque.

## 6. Protocole GRUB proposé — commandes non exécutées

### Conditions avant toute autorisation d’essai

Maintenir écran et câble HDMI sur le Mac, même port Thunderbolt, même réseau indépendant du Core, même clavier, alimentation, firmware, GRUB, noyau et initrd. Ne modifier ni NVIDIA, ni i915, ni Thunderbolt, ni les ressources PCIe. Conserver NP32/PREF512 et tous les paramètres de 04S.

Prévoir un opérateur local capable de lire GRUB et de sélectionner l’entrée correcte. **SSH n’existe pas dans GRUB ou une Shell standard et sera interrompu pendant l’arrêt/redémarrage.** Le maintien signifie retrouver le service et la connectivité après Linux, sans changement réseau ; une continuité SSH absolue est incompatible avec ce diagnostic. Vérifier avant chaque essai autorisé que l’accès distant fonctionne et n’emprunte pas le Core.

Ne pas mélanger démarrage chaud, arrêt normal puis mise sous tension, coupure secteur ou reset SMC. Choisir la même procédure normale pour toute la série. Si une présence Core différente exige un arrêt, utiliser cette même procédure pour A et B, sans coupure secteur ajoutée. Aucun changement de connexion pendant un essai. Documenter délai après mise sous tension et durée à l’invite ; les délais eux-mêmes peuvent influencer un événement firmware.

### Série séparée des essais historiques 04S

| Essai 04T | Variable unique | Mesures |
|---|---|---|
| T-A1 | Core absent avant démarrage | GRUB deux lectures puis Linux |
| T-B1 | Core présent avant démarrage | mêmes commandes, mêmes délais, même entrée |
| T-A2 | Core absent avant démarrage | retour à la référence |
| T-B2 facultatif | Core présent | réplication seulement après bilan A/B/A |

Les changements physiques sont à effectuer uniquement après autorisation, machine arrêtée suivant la procédure choisie. Leur réalisation n’est pas autorisée par ce document.

### À l’invite du GRUB existant

Interrompre le décompte du menu ; presser `c`. Photographier version affichée et contexte. Exécuter seulement après autorisation :

```text
echo $grub_platform
echo $grub_cpu
echo $prefix
help setpci
```

Si `setpci` n’est pas connu, charger uniquement le module déjà installé :

```text
insmod setpci
help setpci
```

`insmod` ici charge un module **GRUB en RAM**, pas un pilote Linux et pas un outil installé sur l’EFI. Si le chargement échoue, noter l’erreur et arrêter la mesure ; ne réparer ni installer quoi que ce soit. Si la plateforme n’est pas EFI x86-64, interrompre ce protocole.

Lire l’identité, puis DEVEN deux fois avec le même ordre et le même intervalle dans tous les essais :

```text
setpci -s 00:00.0 0.L
setpci -s 00:00.0 -d 8086:3ec4 54.L
setpci -s 00:00.0 -d 8086:3ec4 54.L
```

Identité attendue `3ec48086`, puis `3f` ou `f` si les états 04S se retrouvent avant Linux. GRUB peut omettre les zéros initiaux et traduire le texte de sortie. Toute autre valeur doit être conservée entière. Aucun caractère d’affectation dans l’argument `54.L`. Photographier l’invite, la BDF, l’offset et les deux réponses. Un résultat vide, `ffffffff`, une erreur ou une identité différente invalident la mesure ; ne pas conclure à un masquage.

Un inventaire complémentaire peut être ajouté **à tous les essais**, après la lecture ciblée, si nécessaire :

```text
insmod lspci
lspci
```

Il augmente la durée de mesure et les lectures de configuration ; le relevé DEVEN seul suffit au premier objectif. Ne pas lire le registre d’une fonction Intel absente pour essayer de la réactiver.

### Retour à Linux sans changer GRUB

Presser **Échap**, sélectionner manuellement **« JARVIS — T2 eGPU NP 32M + PREF 512M »**, identifiant `jarvis-t2-egpu-np32-pref512`, puis Entrée. Ne pas utiliser l’entrée Debian par défaut et ne pas réécrire une ligne `linux` à la main. Dans le fichier consulté, cette entrée contient :

```text
linux /vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M 'pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0'
initrd /initrd.img-6.18.54-1-t2-trixie
```

Ces lignes sont une référence à contrôler, **pas des commandes à exécuter dans cette mission**. Le retour au menu conserve le mode vidéo existant ; aucun changement de terminal ou de résolution n’est prescrit. Si l’écran/clavier est inutilisable avec Core, ne pas taper aveuglément et ne pas charger NVIDIA : marquer l’essai non mesurable et préparer une autre méthode séparément.

### Relevé post-Linux par SSH, après autorisation

Commandes exactes à saisir dans une session SSH ; leur sortie sera enregistrée par le client distant. Elles ne sont pas exécutées ici :

```bash
date -Is
cat /proc/sys/kernel/random/boot_id
uname -r
cat /proc/cmdline
sudo -n setpci -s 0000:00:00.0 0.L
sudo -n setpci -s 0000:00:00.0 54.L
sudo -n setpci -s 0000:00:00.0 54.L
lspci -Dnnk
ls -ld /dev/dri /sys/bus/pci/devices/0000:00:02.0
systemctl is-active ssh
systemctl is-active sddm
sudo -n journalctl -b -k --no-pager
```

Si `sudo -n` est refusé ou un outil absent, noter le défaut de collecte sans installer ni changer sudo. L’absence de `/dev/dri` ou de `00:02.0` est un résultat possible, pas une commande de correction. Après connexion, vérifier intégralement la cmdline contre 04S ; une différence rend l’essai impropre à la comparaison contrôlée. Le relevé sous Linux arrive après initialisation du noyau et services ; il ne localise pas à lui seul une écriture au noyau plutôt qu’au firmware tardif.

## 7. Interprétation, vérifiabilité et suite éventuelle

Pour chaque essai conserver : identifiant, date externe, état Core, type de démarrage et délais, photo des commandes/résultats, version et prefix GRUB, entrée choisie, boot ID Linux, cmdline, valeurs intégrales DEVEN, présence Intel/DRM/i915, état SSH et observation HDMI/greeter. Associer les photos au boot ID dans la transcription distante. Deux lectures concordantes établissent une stabilité sur cet intervalle, pas sur tout le démarrage.

| Résultat | Conclusion permise |
|---|---|
| GRUB A=`3f`, B=`0f`, A2=`3f` ; Linux concordant | différence déjà présente avant lancement de Linux ; Linux n’a pas initié ce premier état masqué ; firmware ou chemin pré-Linux restent à départager |
| GRUB=`3f`, Linux=`0f` pour un même essai | transition après la mesure ; peut inclure chargement/finalisation GRUB, callbacks firmware, ExitBootServices, noyau ou événements ultérieurs |
| deux lectures GRUB différentes | état instable, intervalle à étudier ; pas de conclusion causale simple |
| GRUB inaccessible avec Core | manque de mesure ; absence d’affichage ne remplace pas une valeur DEVEN |
| A2 ne retrouve pas A1 | arrêter la série et examiner l’état hérité, les délais ou une variable non maîtrisée |

Pour départager Apple et GRUB, une mission suivante pourrait comparer une application/Shell lancée **directement** par Apple avec le chemin GRUB, dans deux séries séparées A/B/A. Un masquage reproduit sans exécuter GRUB montrerait que GRUB n’est pas nécessaire à ce phénomène sur ce chemin. Il ne prouverait pas l’instant précis de l’écriture dans le chemin Debian. Une preuve plus forte nécessiterait une mesure encadrant le **même** GRUB au cours du même démarrage, voire une instrumentation ; cela ajoute des outils ou des modifications et sort du périmètre présent. De même, une lecture initramfs est trop tardive pour exclure un chemin noyau très précoce.

**Aucune méthode examinée ne permet aujourd’hui d’attribuer définitivement l’écriture à Apple, GRUB ou Linux sans nouvelle expérimentation.** Le premier essai GRUB est le meilleur compromis entre information obtenue, conservation du chemin validé et absence de modification persistante.

## Autorisation attendue

**Mission 04T terminée au stade documentaire. Aucune expérience ne doit commencer sur la base de ce rapport seul.** Attendre une autorisation explicite couvrant la série choisie, les arrêts/démarrages, les changements Core machine arrêtée, les commandes GRUB en RAM et les relevés Linux en lecture seule. Une éventuelle Shell ou application EFI nécessite une autorisation séparée ; aucune installation, modification EFI/GRUB/NVRAM ou écriture PCI n’est incluse dans la recommandation.

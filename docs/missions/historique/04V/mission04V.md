> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission04V.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 04V : préparation de la mesure DEVEN en fin de GRUB

Date : 12 octobre 2026. Machine Macmini8,1, Debian 13 T2Linux. **Préparation uniquement : aucune expérimentation exécutée, aucun redémarrage, aucune modification de configuration ou du matériel. Le seul fichier créé est ce rapport.**

## Faisabilité et méthode retenue

**Oui : le GRUB installé permet de charger le noyau et l’initrd existants, puis de lire DEVEN avant de lancer le noyau. La méthode recommandée est la console interactive, commande par commande.** Après `linux` et `initrd`, elle reste à l’invite aussi longtemps que nécessaire pour photographier G1. Le lancement n’intervient qu’à la saisie volontaire de `boot` suivie d’Entrée. Aucun `sleep` n’est nécessaire pour cette pause.

G0 et G1 sont donc deux lectures dans le même démarrage, encadrant les commandes de chargement. **G1 ne mesure pas la fin des Boot Services ni le dernier instant précédant l’entrée CPU dans Linux** : `boot` exécute encore les hooks, la préparation vidéo et le transfert EFI. Un résultat G1=3f, L=0f laissera ces étapes et Linux précoce à départager.

Il ne faut pas simplement ajouter `sleep --interruptible` après `initrd` dans l’éditeur et supposer qu’Échap annule le démarrage : **une entrée exécutée possède un `boot` implicite à sa fin**. Interrompre la pause peut laisser le script se poursuivre. Cette variante est possible techniquement, mais ne fournit pas le contrôle manuel et la récupération de la console.

## 1. GRUB réellement installé et données statiques vérifiées

- `grub-common`, `grub2-common`, `grub-efi-amd64`, `grub-efi-amd64-bin` : **2.12-9+deb13u2**.
- Manuel local `/usr/share/info/grub.info*.gz` : GRUB **2.12**, édition du 3 mai 2026. Les chapitres console, menu, éditeur, linux, initrd, sleep, echo et boot ont été lus.
- `/boot/grub/grub.cfg` a pu être lu avec `sudo -n cat` ; l’entrée exacte est présente, identifiant `jarvis-t2-egpu-np32-pref512`. Son corps concorde avec `/etc/grub.d/47_jarvis_t2_egpu_np32_pref512`.
- Modules EFI x86-64 `setpci`, `sleep`, `linux`, `normal`, `echo` présents dans `/boot/grub/x86_64-efi/`, et identiques par SHA-256 à ceux de `/usr/lib/grub/x86_64-efi/`.
- `/boot` est un système ext4 séparé sur `/dev/nvme0n1p2`. Le chemin GRUB `/vmlinuz-…` est relatif au volume `/boot` sélectionné par UUID ; il ne faut pas ajouter un préfixe `/boot/` à la commande.
- Le bloc d’environnement consulté avec `grub-editenv ... list` ne contient aucune variable affichée. `/boot/grub/custom.cfg` est absent. Ne pas en créer.
- Lecture NVRAM par `efibootmgr -v`, sans options d’écriture : BootCurrent `0000`, BootOrder `0000,0080`, entrée Debian vers `\EFI\debian\shimx64.efi`. Cela renseigne le chemin déclaré, sans prouver à lui seul chaque image chaînée ou le `$prefix` utilisé.
- Le module linux local contient des symboles de chargement/boot EFI et x86 legacy : ne pas déduire du seul mot `linux` quel sous-chemin Debian sera utilisé. La séparation chargement/exécution est le point nécessaire ici.
- Le boot courant demeure `[UUID EXPURGÉ]`, avec les paramètres NP32/PREF512 de 04U.

Empreintes de référence, obtenues par lectures :

| Fichier | SHA-256 |
|---|---|
| `/boot/grub/grub.cfg` | `9bc2c064607d7daa3438da38e9f7808e71060aa6430c32af3decb3adbf5d7726` |
| `/boot/grub/grubenv` | `f64122858064885ef0733e42c6a3d2d3fd642671f714db0d974b880c0f087430` |
| `/boot/vmlinuz-6.18.54-1-t2-trixie` | `a41e1a7680c5d76761a744d4265b7901bbd7494e90340fda1eb59eec73d72d1b` |
| `/boot/initrd.img-6.18.54-1-t2-trixie` | `4c7fe763f3f05300e03c270aa24d2c5b90a55cbd26547898a3c1ca3f44507cc0` |
| `/boot/efi/EFI/debian/grubx64.efi` | `425ffb5b84e8738084815d9df4a33c0e5f64409c7aadeb3dd3bcf60357551c5a` |

Le noyau fait 10 449 408 octets, l’initrd 91 048 480 octets. Ces constats ne valent pas essai du chargement en RAM. La version affichée, plateforme et préfixe effectifs devront être photographiés lors de l’expérience autorisée ; le succès des lectures GRUB 04U rend `setpci` plausible, mais ne dispense pas du contrôle runtime.

## 2. Console, éditeur et commandes

Le manuel **installé** précise : `c` au menu ouvre la console normale ; `e` ouvre l’éditeur ; Échap depuis l’éditeur abandonne ses modifications et revient au menu. Entrée dans l’éditeur insère une nouvelle ligne ; **Ctrl+x lance l’entrée**, F10 est l’alternative prévue par le code. Depuis l’éditeur, **Ctrl+c ou F2** ouvre une console imbriquée ; Échap revient alors à l’éditeur, puis un deuxième Échap au menu. Au menu, la touche est `c`, sans Ctrl.

Le [code de l’éditeur GRUB 2.12](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/normal/menu_entry.c) confirme ces touches et le boot implicite après exécution. Le [code menu](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/normal/menu.c) complète ce comportement. En console normale, Entrée exécute seulement la commande saisie ; il n’y a pas de boot automatique à la suite d’un `initrd`.

| Commande | Syntaxe retenue / fonction | Contrainte |
|---|---|---|
| `setpci` | `setpci -s 00:00.0 0.L` puis `setpci -s 00:00.0 -d 8086:3ec4 54.L` | `.L` = lecture 32 bits ; syntaxe GRUB, sans domaine. **Aucun `=` dans l’argument registre.** |
| `linux` | Ligne exacte reproduite ci-dessous | Charge l’image et prépare le chargeur ; ne lance pas le noyau. Une nouvelle commande linux oblige à recharger l’initrd. |
| `initrd` | Ligne exacte ci-dessous | Exige un linux chargé avec succès ; charge les données/initramfs sans les exécuter. |
| `echo` | `echo G0`, `echo G1`, `echo $?` | Affiche un libellé ou le code de la commande précédente ; sans `-e`, pas d’échappements nécessaires. |
| `sleep` | Optionnel : `sleep --verbose --interruptible 60` | Pause de 60 secondes ; Échap/F4/Shift interrompent, statut 1. Fin normale : statut 0. En console, revient à l’invite ; dans un script, ne garantit pas son abandon. |
| `boot` | `boot` seul | Lance le chargeur enregistré avec sa cmdline et son initrd ; peut ne pas revenir. Aucune récupération GRUB garantie après le transfert. |

Le [code setpci](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/commands/setpci.c) distingue lecture et écriture via la présence d’une affectation. Sans périphérique correspondant, une sortie vide n’est pas une valeur zéro. Un statut 0 ne suffit donc pas pour valider une mesure. Les valeurs sont affichées en hexadécimal, souvent sans zéros initiaux : `3f` et `f` représentent `0x3f` et `0x0f`. Le module utilise une commande soumise au lockdown : une interdiction doit être enregistrée, sans changer de politique de sécurité.

Sur x86, la lecture PCI peut écrire le sélecteur CF8 avant de lire CFC. Ce n’est pas une écriture de configuration PCI ni une écriture DEVEN. Ne pas employer des commandes d’accès brut improvisées.

Le [code sleep](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/commands/sleep.c) et le manuel local concordent sur l’interruption. `sleep 60` sans option interruptible ignore ces demandes de raccourcissement. La pause humaine à l’invite est plus simple : elle ne limite pas le temps de photographie et ne démarre jamais Linux quand un délai expire.

Le [chargeur EFI](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/loader/efi/linux.c), le [chargeur x86](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/loader/i386/linux.c) et la [commande boot](https://raw.githubusercontent.com/rhboot/grub2/grub-2.12/grub-core/commands/boot.c) séparent enregistrement du chargeur et invocation. Sources amont utilisées pour expliquer le comportement ; le paquet Debian possède des adaptations. Le manuel local et les modules installés ont été contrôlés, mais aucune exécution pré-Linux n’a été faite dans cette mission.

## 3. Corps exact de l’entrée actuelle

Ce bloc est une transcription du fichier actif, **pas un script à exécuter dans Linux ni une nouvelle entrée à installer** :

```text
    load_video
    insmod gzio
    if [ x$grub_platform = xxen ]; then insmod xzio; insmod lzopio; fi
    insmod part_gpt
    insmod ext2
    search --no-floppy --fs-uuid --set=root [UUID EXPURGÉ]
    linux /vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M 'pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0'
    initrd /initrd.img-6.18.54-1-t2-trixie
```

La ligne `linux` doit rester **une seule ligne logique**, même si l’écran la replie visuellement. Les apostrophes ASCII autour de `pci=resource_alignment=…` sont indispensables : elles empêchent les points-virgules d’être interprétés comme des séparateurs GRUB. Ne pas ajouter `linuxefi`, `gfxpayload`, `acpi_osi`, une blacklist i915, un paramètre NVIDIA ou une autre valeur NP/PREF.

## 4. Procédure recommandée, touche par touche — NON EXÉCUTÉE

### A. Préconditions et entrée dans la console

Après autorisation explicite du futur redémarrage, avec opérateur local et appareil photo prêt :

1. Interrompre le décompte du menu par une flèche. Ne pas appuyer sur Entrée : le défaut configuré est le noyau Debian 6.12.111, pas l’entrée cible.
2. Avec les flèches, sélectionner **JARVIS — T2 eGPU NP 32M + PREF 512M**.
3. Appuyer sur **e**. Vérifier visuellement et photographier les lignes linux/initrd contre le §3, sans éditer. Les flèches et Ctrl+a/Ctrl+e permettent de naviguer ; un retour visuel à la ligne n’est pas une coupure de commande.
4. Appuyer sur **Échap** pour revenir au menu. Aucune commande du corps de l’entrée n’a encore été exécutée par cette inspection.
5. Appuyer sur **c** pour obtenir l’invite normale `grub>`. Cette console issue du menu est celle dont Échap permet le retour au menu. Une invite `grub rescue>` ne convient pas : arrêter ce protocole.

Saisir les commandes suivantes **une par une**, Entrée après chacune. Ne jamais coller un bloc contenant `boot` et ne pas saisir plusieurs commandes sur une ligne avec des séparateurs.

```text
echo $grub_platform
echo $grub_cpu
echo $prefix
insmod setpci
help setpci
help linux
help initrd
help boot
```

Attendus : plateforme `efi`, CPU `x86_64`, préfixe cohérent avec le GRUB inspecté, modules/commandes accessibles sans erreur. Si un contrôle échoue, photographier et revenir au menu ; ne pas installer de module ni changer le verrouillage. `insmod` ici concerne GRUB en RAM, pas i915 ni un pilote Linux.

### B. G0 — avant les commandes de préparation et de chargement

```text
echo G0_AVANT_CHARGEMENT
setpci -s 00:00.0 0.L
setpci -s 00:00.0 -d 8086:3ec4 54.L
setpci -s 00:00.0 -d 8086:3ec4 54.L
```

Photographier commandes et réponses. Identité attendue `3ec48086`. Valeur DEVEN attendue selon 04U : `3f`, mais toute autre valeur réelle doit être enregistrée sans correction. Deux lectures contradictoires rendent l’état instable : ne pas poursuivre comme si G0 était unique. Une sortie vide, une erreur, `ffffffff` ou une identité différente invalident la mesure.

**G0 encadre aussi les commandes de préparation de l’entrée**, qui seront exécutées après lui. Les modules chargés pour obtenir la mesure elle-même sont déjà présents avant G0 ; documenter ce point et les délais. C’est comparable au G0 de console 04U, pas une observation avant toute initialisation GRUB.

### C. Charger la même entrée, en console, sans lancer le noyau

Reprendre les commandes du corps, dans leur ordre, sans l’enveloppe `menuentry { … }` :

```text
load_video
insmod gzio
if [ x$grub_platform = xxen ]; then insmod xzio; insmod lzopio; fi
insmod part_gpt
insmod ext2
search --no-floppy --fs-uuid --set=root [UUID EXPURGÉ]
linux /vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=hpmmiosize=32M 'pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0'
```

**Après chaque commande, vérifier l’absence d’erreur. Immédiatement après linux**, saisir :

```text
echo $?
```

Attendu `0`. Une sortie nulle ne remplace pas la lecture de l’erreur éventuelle. Si le chargement est refusé, interrompre le protocole : ne pas saisir boot. Une commande qui ne produit aucun texte peut réussir normalement.

Ensuite, et seulement si linux a réussi :

```text
initrd /initrd.img-6.18.54-1-t2-trixie
echo $?
```

Attendu `0` et aucune erreur. Ne pas retaper linux après initrd ; cela exigerait de recharger l’initrd et changerait le déroulement expérimental. Si une erreur de saisie oblige à recommencer, abandonner cet essai comme mesure contrôlée, puis préparer un nouvel essai après bilan.

### D. G1 — noyau et initrd chargés, lancement toujours en attente

```text
echo G1_APRES_LINUX_INITRD
setpci -s 00:00.0 0.L
setpci -s 00:00.0 -d 8086:3ec4 54.L
setpci -s 00:00.0 -d 8086:3ec4 54.L
```

Photographier. **Ne rien saisir ensuite jusqu’à ce que la photographie soit obtenue** : la console attend indéfiniment. Le noyau et l’initrd restent chargés ; Linux n’est pas lancé par ces lectures.

Noter l’intervalle G0→G1 et G1→boot avec l’appareil externe. Si la pause est longue, effectuer une troisième lecture DEVEN immédiatement avant boot et l’appeler **G1b**, afin de ne pas masquer une évolution pendant la photographie. Cette lecture supplémentaire doit être fixée à l’avance pour tous les essais.

### E. Lancer volontairement

Uniquement si identité, chargements et capture sont valides, et si l’autorisation couvre le lancement : taper **boot**, puis **Entrée**.

```text
boot
```

**Ne pas revenir au menu pour lancer l’entrée à ce stade** : cela rechargerait les fichiers et ne lancerait plus exactement l’état mémoire dont G1 vient d’être photographié. Boot réutilise le chargeur préparé ; aucun paramètre supplémentaire n’est passé par cette commande.

### F. L — après démarrage Linux

Depuis SSH indépendant du Core, avec capture sur le poste distant, relever :

```bash
cat /proc/sys/kernel/random/boot_id
uname -r
cat /proc/cmdline
sudo -n setpci -s 0000:00:00.0 0.L
sudo -n setpci -s 0000:00:00.0 54.L
sudo -n setpci -s 0000:00:00.0 54.L
ls -ld /sys/bus/pci/devices/0000:00:02.0 /dev/dri
sudo -n dmesg --time-format=raw
```

Ces commandes ne sont pas exécutées dans cette préparation. Associer les photographies G0/G1 au nouveau boot ID. Comparer **la cmdline entière**, notamment les trois BDF et les réserves 32M/512M. L’absence Intel/DRM constitue un résultat attendu possible, pas une demande de correction. Aucun i915 forcé, aucun rescan ni NVIDIA installé.

## 5. Éditeur : possibilité technique et alternative

Le chargement et les lectures ont la même syntaxe dans le corps d’une entrée. Dans l’éditeur, il est techniquement possible d’insérer après initrd `echo G1`, `setpci … 54.L` et une pause, puis Ctrl+x. Mais les différences sont décisives : les commandes s’enchaînent, un délai peut expirer, les erreurs ne constituent pas toujours un arrêt de tout le script, et boot est implicite à la fin. **Échap pendant sleep n’a pas la sémantique d’Échap avant Ctrl+x dans l’éditeur.** Ne pas retenir cette variante pour le premier essai.

Si l’opérateur préfère conserver l’entrée visible, ouvrir avec **e**, puis **Ctrl+c** (ou F2) pour la console imbriquée, et exécuter les commandes du §4 ligne par ligne. Après G1, lancer avec `boot` directement depuis cette console. Pour annuler avant boot : Échap revient à l’éditeur, puis Échap au menu. **Ne pas appuyer sur Ctrl+x/F10 après les mesures**, ce qui exécuterait à nouveau le corps de l’entrée.

La console normale recommandée ne modifie même pas la copie éditable de l’entrée. Si l’entrée/console est protégée par mot de passe, si setpci est bloqué ou si les commandes ne sont pas disponibles dans le GRUB effectif, l’expérience n’est pas réalisable avec les prérequis actuels : noter l’échec, ne pas réparer GRUB. Aucun autre outil pré-Linux non persistant déjà validé n’est disponible ici ; une Shell/application EFI changerait le chemin de boot et demanderait une préparation séparée.

## 6. Récupération et risques

| Situation | Action avant tout boot |
|---|---|
| Erreur de frappe dans la ligne en cours | Ctrl+a/Ctrl+e, flèches, Retour arrière ; en console Ctrl+u efface avant le curseur. Ne pas valider une ligne incertaine. |
| Erreur linux/initrd/module/recherche du volume | Photographier, arrêter la séquence ; pas de boot ni de tentative de modification du disque. |
| G0/G1 invalide ou mesure non photographiable | Marquer l’essai invalide ; ne pas conclure à DEVEN=0. |
| Retour demandé depuis console `c` du menu | À l’invite, Échap ; menu normal réapparaît. |
| Retour demandé depuis console ouverte par l’éditeur | À l’invite, Échap vers éditeur, puis Échap vers menu. |
| Retour depuis éditeur avant exécution | Échap abandonne les éditions en mémoire. |
| Sleep optionnel encore actif en console | Échap interrompt ; attendre l’invite, puis Échap pour revenir au menu. Aucun boot n’est automatiquement appelé en console. |
| Boot déjà lancé | Ne pas supposer que les touches GRUB restent utilisables. Observer et attendre le retour SSH ; panne nécessitant un arrêt ne donne aucune autorisation de reset supplémentaire. |

Après un retour au menu, **le retour d’interface n’annule pas nécessairement le chargeur, les modules, le root et les autres états préparés en RAM**. Il ne constitue pas un retour causal au G0 initial. Pour simplement démarrer la référence si l’autorisation le permet, sélectionner manuellement l’entrée NP32/PREF512 d’origine et Entrée : elle recharge linux et initrd. Ne pas choisir l’entrée Debian par défaut, ne pas utiliser un `boot` isolé après une erreur d’initrd. Ce démarrage de récupération n’est pas une expérience G0/G1 valide.

Risques concrets : erreur de transcription de la longue cmdline, clavier Apple et disposition pré-Linux différente (apóstrophes, deux-points et points-virgules à vérifier visuellement), délai influençant un événement firmware, chargement en RAM susceptible d’appeler des services EFI, extinction/perte d’affichage lors du transfert, interruption SSH pendant le redémarrage. Une console GRUB ne propose pas SSH. Le réseau de récupération doit être indépendant du Core.

La pause humaine et les lectures ajoutent du temps au chemin habituel : répéter avec délais comparables avant de conclure à un effet spécifique du chargement. Le protocole n’exécute ni i915 ni initramfs avant boot, mais le chargement fait travailler **GRUB et éventuellement des services firmware** ; G0→G1 ne permet pas à lui seul de distinguer leur auteur.

## 7. Persistance : aucune modification requise

Aucun `update-grub`, `grub-install`, `grub-reboot`, `grub-set-default`, `save_env`, changement grubenv, écriture EFI/NVRAM ou changement BootOrder n’est nécessaire. La procédure utilise seulement les fichiers existants, des modules et un chargeur en RAM, puis le démarrage explicitement choisi.

Nuance : ceci ne certifie pas que **tout le démarrage existant** est sans écritures. Le préambule actuel de grub.cfg contient des `save_env` conditionnels pour next_entry/prev_saved_entry ; le bloc consulté est vide. Le fichier charge aussi `bli`, interface d’information de boot susceptible de publier des variables EFI. Ces comportements existants ne sont pas ajoutés ni modifiés par cette préparation. Ne pas désactiver de composant pour tenter de garantir une absence absolue de toute écriture, ce qui changerait le chemin comparé.

## 8. Critères d’interprétation

| G0 | G1 | L | Conclusion permise |
|---|---|---|---|
| 3f | 0f | 0f | Transition déjà pendant les commandes de préparation/chargement ou leur intervalle temporel ; Linux principal n’est pas lancé au point G1. GRUB/firmware/asynchronisme restent à départager. |
| 3f | 3f | 0f | Transition après G1 : hooks boot, vidéo, EFI/ExitBootServices, stub ou Linux précoce demeurent candidats. |
| 3f | 3f | 3f | Masquage non reproduit dans cet essai ; changement de durée ou état hérité possible. Pas de correction démontrée. |
| 0f | 0f | 0f | État masqué déjà à G0 ; différent de 04U, examiner le chemin et les conditions. |
| quelconque | lectures différentes | quelconque | État instable ; garder toutes les valeurs et horodatages, ne pas retenir un G1 unique. |
| quelconque | invalide | quelconque | Expérience non interprétable pour séparer G0 et G1. |

Lire les valeurs intégrales ; `3f→0f` correspond aux bits 4 et 5. D2EN explique le masquage Intel ; D3EN n’est pas un second bit graphique. Toute autre transition doit être analysée séparément. Une mesure L après SSH n’est pas une mesure DEVEN à 0,167 s ; conserver dmesg pour vérifier le premier scan sans transformer son absence Intel en lecture de registre.

## 9. Prérequis à vérifier avant autorisation

- Opérateur local, clavier fonctionnel dans GRUB, écran directement utilisable, photographie/vidéo externe permettant de lire commandes, réponses et temps.
- Conserver Core connecté au même port, alimentation, écran, noyau/initrd et paramètres PCIe ; aucune variation NP/PREF ni pilote.
- Revoir le corps exact du §3 et les empreintes si les fichiers ont changé entre préparation et essai ; ne pas approuver un protocole basé sur une autre entrée.
- Disposer du chemin de récupération vers l’entrée NP32/PREF512, sans dépendre du GPU NVIDIA ; réseau/SSH indépendant du Core et interruption prévue pendant le boot.
- À l’invite, valider GRUB EFI x86-64, `$prefix`, aide et identité du pont hôte ; arrêter si authentification/lockdown/modules bloquent.
- Fixer la procédure de mise sous tension et les délais, décider à l’avance si G1b est inclus, définir qui saisit boot après photographie.
- L’autorisation doit couvrir explicitement **le redémarrage, les commandes GRUB en RAM, les lectures PCI, le lancement manuel et la collecte Linux**, ainsi que le démarrage de récupération éventuel. Elle ne couvre pas un reset forcé, une installation ou une réparation GRUB/EFI.

**Mission 04V terminée au stade préparatoire. La méthode distingue réellement G0 et G1, avec pause illimitée à l’invite et boot manuel. Attente de votre autorisation explicite avant toute expérimentation.**

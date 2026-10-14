# Mission 04I — Entrée réserve PCIe 512M installée

**Installation explicitement autorisée par « oui install », terminée et vérifiée le 2026-10-11T21:36:23.538987+02:00. Aucun redémarrage ni débranchement exécuté.** Cette section remplace le statut de préparation non installée conservé dans l’étude ci-dessous.

Entrée **JARVIS — T2 eGPU réserve PCIe 512M**, ID `jarvis-t2-egpu-reserve-512m`, installée via `/etc/grub.d/45_jarvis_t2_egpu_reserve_512m` (root:root 0755). GRUB actif (root:root 0600, mode conservé) identique au candidat préparé et à la génération contrôlée ; syntaxe vérifiée. Diff strictement limité au nouveau bloc 45.

Arguments propres à cette entrée : `intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M`, image/initramfs exacts `6.18.54-1-t2-trixie`, root/ro/quiet existants conservés. Debian 6.12.111 demeure le choix par défaut, menu 15 s ; secours Debian 6.12.107/6.12.111 et toutes les entrées T2 précédentes conservés. grubenv inchangé, aucune next_entry.

SHA-256 de `/boot/grub/grub.cfg` : `81be6b6101d1916fb9c62de50444959ee19b8a3dbbf714c8eb9c368f2919054d`. Autres empreintes protégées identiques avant/après : configuration globale/sources JARVIS existantes, grubenv et les trois paires noyau/initramfs. Sauvegarde juste avant installation et contrôles dans `mission04I-preparation/installation-20261011-213406/`.

Génération effectuée vers un fichier de contrôle dans un espace de montage privé avec racine, /boot et /run en lecture seule, copies des sources superposées, thème copié comparant le cache au lieu de le réécrire, verrous LVM et temporaires locaux. Génération retenue code 0, identique octet pour octet au candidat. Première tentative d’isolation non retenue conservée ; ses différences n’ont pas été installées. Aucun fichier thème système modifié.

Relecture après installation : boot ID `565560bb-80ac-424b-8bc3-101e7441b335` inchangé, Quadro encore présente, SSH/service/socket et display-manager actifs. `pci=hpmmioprefsize=512M` **n’est pas encore actif** dans le noyau lancé : son effet reste à tester lors d’un futur démarrage autorisé. La conclusion C de 04H n’est pas corrigée par cette installation seule.

**Installation terminée. Le retrait du Core, le redémarrage sans Core et le branchement surveillé ne sont pas autorisés par l’accord d’installation et n’ont pas été exécutés.** Le plan et les critères de validation avant branchement restent ceux de l’étude ; aucune configuration pilote, i915, VFIO, EFI, réseau, service ou initramfs modifiée.

---

# Historique de préparation — étude de la réservation mémoire PCIe hotplug

11 octobre 2026. **Préparation terminée ; entrée 512M non installée. Attente de l’accord explicite pour l’installation. Aucun essai matériel exécuté.**

Le test 04H est clos : pci=realloc=on n’a pas attribué BAR 1/3. Une demande de réserve au démarrage mérite un essai contrôlé, mais sa réussite est incertaine : elle doit obtenir de l’espace dans tous les parents, et pas seulement demander 512 Mio au pont hotplug.

## 1. Archivage et référence

Les 27 empreintes du dossier `mission04H-preuves/20261011-211801/` ont été vérifiées sans divergence. Archive contenant ce dossier et le rapport 04H : [mission04H-archive.tar.gz](mission04I-preparation/mission04H-archive.tar.gz), avec empreinte SHA-256 séparée. Les originaux restent conservés. Le suivi incident est actualisé.

Référence 04H : boot `565560bb-80ac-424b-8bc3-101e7441b335`, noyau exact `6.18.54-1-t2-trixie`, Core autorisé, Quadro identifiée par 10de:1eb0 à 81:00.0 ; Nouveau bloqué, i915/Ethernet/SSH et bureau conservés. BAR 0 = 16 Mio à 0x90000000–0x90ffffff, attribué et couvert ; BAR 1 = 256 Mio et BAR 3 = 32 Mio non attribués. Échecs de fenêtre finale 289 puis 288 Mio et messages can't assign/no space/failed to assign. Les vérifications hôte de 04H ont levé les réserves d’accès de 04G.

## 2. Comparaison avant/après activation de realloc

04E : boot cf644abb-f9ae-4308-ba1f-d97be3e7aa39, même noyau et blacklist, sans realloc. 04H : autre boot, avec realloc. Même chaîne : `00:01.2 → 7b:00.0 → 7c:01.0 → 7f:00.0 → 80:01.0 → 81:00.0`. Les adresses ci-dessous sont des résultats archivés ; le prochain GPU devra être identifié dynamiquement.

| Pont | 04E sans realloc : non préchargeable | 04H avec realloc : non préchargeable | 04E : préchargeable | 04H : préchargeable |
|---|---|---|---|---|
| 0000:00:01.2 | `0x8f900000–0x9dafffff` (226 Mio) | `0x8fa00000–0x9dbfffff` (226 Mio) | `0xbf400000–0xcd3fffff` (224 Mio) | `0xbf400000–0xcd3fffff` (224 Mio) |
| 0000:7b:00.0 | `0x8f900000–0x9dafffff` (226 Mio) | `0x8fa00000–0x9dbfffff` (226 Mio) | `0xbf400000–0xcd3fffff` (224 Mio) | `0xbf400000–0xcd3fffff` (224 Mio) |
| 0000:7c:01.0 | `0x8fb00000–0x96afffff` (112 Mio) | `0x8fc00000–0x96bfffff` (112 Mio) | `0xbf400000–0xc63fffff` (112 Mio) | `0xbf400000–0xc63fffff` (112 Mio) |
| 0000:7f:00.0 | `0x90000000–0x961fffff` (98 Mio) | `0x90000000–0x961fffff` (98 Mio) | `0xc0000000–0xc63fffff` (100 Mio) | `0xc0000000–0xc63fffff` (100 Mio) |
| 0000:80:01.0 | `0x90000000–0x910fffff` (17 Mio) | `0x90000000–0x910fffff` (17 Mio) | Absente | Absente |


Les fenêtres NP hôtes sont translatées de +1 Mio, sans gain de taille. Les fenêtres préchargeables sont inchangées. BAR 0 reste identique ; BAR 1/3 échouent dans les deux tests. Cette comparaison entre boots ne permet pas d’attribuer causalement la translation NP à realloc. Les captures restreintes 04G du même boot avant le hotplug montrent aussi les mêmes fenêtres hôtes que 04H après hotplug.

## 3. Contraintes amont et intérêt de 512M

La fenêtre préchargeable racine 00:01.2 et celle de 7b:00.0 sont `0xbf400000–0xcd3fffff`, soit 224 Mio. Elles ne peuvent contenir un BAR de 256 Mio. Avec son alignement naturel de 256 Mio, le premier début possible dans cette plage est 0xc0000000 ; sa fin serait 0xcfffffff, au-delà de 0xcd3fffff. Il ne reste que 212 Mio depuis ce début aligné. La branche 7c:01.0 est limitée à 112 Mio, puis 7f:00.0 à 100 Mio ; le dernier pont n’a aucune fenêtre préchargeable. Le besoin total de 288 Mio est donc une borne inférieure, pas une garantie de placement.

Les fenêtres préchargeables actuellement observées sont annoncées 32 bits par lspci. Le journal expose une aperture hôte basse `0x80000000–0xfeafffff`, et une aperture haute `0x4000000000–0x7fffffffff`. Cette aperture haute n’établit pas que chaque pont de la chaîne puisse y transférer une fenêtre 64 bits. La présence d’un espace hôte ne prouve pas qu’une plage contiguë, compatible, alignée et libre existe ; l’iomem est archivé, pas modifié. Aucun pci=nocrs, forçage EFI ou changement des ponts n’est proposé.

512M = 536 870 912 octets = 0x20000000 : marge supérieure aux 288 Mio des deux BAR, utile seulement si le noyau réserve une fenêtre utilisable avant insertion et si les parents la contiennent. Il s’agit d’espace d’adressage MMIO, pas de 512 Mio de RAM ou de VRAM alloués au GPU. Ce réglage est global aux ponts reconnus hotplug : il ne cible pas exclusivement le Core. Les branches et besoins supplémentaires peuvent exiger plus de 512 Mio dans un ancêtre commun.

## 4. Syntaxe et prise en charge du noyau installé

La documentation Linux 6.18.54 décrit `pci=hpmmioprefsize=nn[KMG]` pour la réserve préchargeable hotplug, avec défaut de 2 Mio. La syntaxe demandée `pci=hpmmioprefsize=512M` est valide ; elle ne change pas la réserve non préchargeable comme le ferait hpmemsize. [Documentation versionnée](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/Documentation/admin-guide/kernel-parameters.txt).

Le parser pci_setup reconnaît hpmmioprefsize= et passe la valeur à memparse avant de la stocker dans pci_hotplug_mmio_pref_size. Deux arguments pci= séparés peuvent être traités successivement : l’entrée conserve pci=realloc=on puis pci=hpmmioprefsize=512M. [Parser Linux 6.18.54](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/pci/pci.c).

**Vérification locale du binaire installé, au-delà de la documentation :** extraction en lecture seule de /boot/vmlinuz-6.18.54-1-t2-trixie avec extract-vmlinux fourni par les headers. Le désassemblage de pci_setup compare le texte situé à 0xffffffff825b32ef (rodata : hpmmioprefsize=), avance de 15 octets, appelle memparse à 0xffffffff81f81550, puis stocke le résultat à 0xffffffff82dbcf50, identifié par System.map comme pci_hotplug_mmio_pref_size. Les fichiers rodata, désassemblage, System.map et empreinte de l’ELF extrait sont conservés ; l’ELF volumineux temporaire a été retiré. Cela confirme la prise en charge syntaxique dans l’image T2 installée, pas une réservation effective de 512 Mio sur le boot actuel qui ne porte pas encore cet argument.

Configuration locale : CONFIG_PCI=y, CONFIG_HOTPLUG_PCI=y, CONFIG_HOTPLUG_PCI_PCIE=y, CONFIG_PCI_REALLOC_ENABLE_AUTO=y. Paquets image/headers 6.18.54-1, source annoncée linux-upstream. Les sources PCI amont 6.18.54 ont été téléchargées et archivées pour l’analyse ; elles ne sont pas présentées comme l’intégralité du source patché T2.

## 5. Limites du mécanisme

Le dimensionnement applique le supplément aux ponts marqués is_hotplug_bridge. La réserve est susceptible d’être traitée comme extension optionnelle dans les passes de réallocation. pbus_size_mem retourne immédiatement lorsqu’une fenêtre est déjà rattachée à une ressource parent. La réservation ne force donc pas systématiquement l’agrandissement de chaque fenêtre firmware. Le chemin d’allocation hotplug répartit l’espace déjà disponible sous le pont. [Dimensionnement et allocation Linux 6.18.54](https://raw.githubusercontent.com/gregkh/linux/v6.18.54/drivers/pci/setup-bus.c).

Observation locale : 7c:01.0 annonce HotPlug+ ; 00:01.2 annonce HotPlug-. Le bit lspci n’est pas une preuve exhaustive du champ interne is_hotplug_bridge (des particularités du noyau peuvent intervenir), mais il rappelle que la demande n’est pas uniformément appliquée à tous les ancêtres. Si les fenêtres 224/112 Mio restent attribuées telles quelles au nouveau boot, la demande 512M sera inutilisable pour le GPU. Aucun paramètre ne crée de nouvel espace physique ou ne contourne les limites des parents.

**Évaluation : essai conditionnellement utile, sans promesse de correction.** Il teste la différence entre une réserve demandée avant insertion et une allocation de BAR après insertion. L’effet effectif doit d’abord être démontré sans Core. Si les parents restent insuffisants, le branchement n’apportera pas de preuve de réussite et le test matériel doit être reporté.

## 6. Entrée GRUB préparée, non installée

Titre : **JARVIS — T2 eGPU réserve PCIe 512M**. ID unique : `jarvis-t2-egpu-reserve-512m`. Source prévue : /etc/grub.d/45_jarvis_t2_egpu_reserve_512m, actuellement uniquement dans le dossier de préparation. Image/initramfs T2 et UUID /boot repris de l’entrée active vérifiée.

```text
intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M
```

root, ro et quiet existants sont conservés. Aucun argument i915/VFIO/EFI ajouté. Fichiers reviewables : [source](mission04I-preparation/45_jarvis_t2_egpu_reserve_512m), [entrée](mission04I-preparation/entree-grub-prevue.cfg), [candidat](mission04I-preparation/grub.cfg-candidat), [diff](mission04I-preparation/grub-diff.patch). Le candidat est la copie de GRUB actif plus ce seul bloc, pas une nouvelle génération installée.

Lanceur shell validé séparément du corps GRUB ; sa sortie correspond exactement à l’entrée prévue. grub-script-check valide l’entrée et le candidat. Aucun grub-mkconfig/update-grub/grub-install effectué. Empreintes avant/après identiques pour GRUB actif, grubenv, configuration/sources JARVIS et les trois paires noyau/initramfs.

Debian 6.12.111 demeure le défaut, menu 15 s, grubenv sans next_entry. Debian 6.12.107 et les entrées normales/recovery, les entrées T2 existantes, diagnostic sans Nouveau et réallocation restent conservés. L’ajout proposé n’exige ni initramfs ni changement global de blacklist.

## 7. Risques et plan avant toute installation

| Risque | Conséquence possible | Prévention / critère d’arrêt |
|---|---|---|
| Réserve globale sur plusieurs ponts | Pression MMIO, fragmentation, nouvelles allocations refusées | Examiner tous les ponts et erreurs au boot sans Core |
| Ancêtres insuffisants ou fenêtres firmware conservées | Réserve ignorée/non allouée ; même échec BAR | Pas d’essai de branchement si aucune plage adéquate n’est démontrée |
| Réallocation de ressources de périphériques internes | Régression Intel, Ethernet ou stockage ; perte SSH | Validation i915, écran, réseau, SSH et NVMe avant insertion ; secours local prêt |
| Hotplug de la chaîne déjà connue en défaut | Nouveaux échecs, avertissements DROM, éventuel blocage | Un seul branchement autorisé et surveillé ; arrêt des manipulations au premier défaut |
| Mauvaise entrée/paramètre ignoré | Test non comparable | Vérifier cmdline, boot ID, message PCI Unknown option et journaux |

**Étape 1 — installation, uniquement après accord explicite.** Relire les empreintes et l’état GRUB ; actualiser la sauvegarde si des changements autorisés sont intervenus. Installer seulement la nouvelle source 45 ; produire un candidat de génération en contrôlant les effets annexes, comparer au diff autorisé, vérifier syntaxe et conservation des secours, puis installer le candidat validé. Ne pas changer le défaut, grubenv ou les sources précédentes. L’installation n’autorise pas à elle seule un reboot ou un débranchement.

**Étape 2 — préparation matérielle et boot, après autorisations distinctes.** Le Core est actuellement branché : ne pas le retirer maintenant. Pour le futur scénario « démarrage sans Core », convenir explicitement du retrait et du redémarrage, avec accès écran/clavier et SSH indépendant prêt. Choisir manuellement l’entrée 512M pour un seul démarrage, sans changement persistant du défaut. Aucun reboot automatique préparé.

**Étape 3 — contrôles au boot sans Core.** Confirmer noyau exact, blacklist et les deux pci=, absence de module nouveau/nvidia ; boot ID nouveau. Contrôler Intel primaire/i915/DP-3, bureau humainement, Ethernet et connexion SSH authentifiée depuis le poste distant. Archiver la collecte complète vers un nouveau dossier avant-branchement. Retrouver la topologie hôte, relever pour tous les ponts les fenêtres NP/PREF, leurs types 32/64 bits, début/fin/taille et ressources sysfs/iomem ; comparer à 04E/04H. Vérifier toute réserve demandée, tout échec d’attribution, ACPI/DMAR/AER/DPC et NVMe/Thunderbolt.

Condition avant insertion : une fenêtre utilisable sur la branche destinée au Core, réellement attribuée et couverte par chaque parent, permettant 256 Mio alignés puis 32 Mio et les besoins annexes. Une réserve de 512 Mio visible seulement en aval ne suffit pas. Si 224/112 Mio persistent, si la réserve est non attribuée ou si une régression apparaît, ne pas brancher. Rapporter le résultat du boot et attendre la décision suivante.

**Étape 4 — unique branchement surveillé, seulement après validation et autorisation de l’essai.** Démarrer depuis le poste SSH les flux journalctl noyau/Bolt/système avec timestamps, enregistrés sur le poste indépendant ; garder une seconde connexion de commande et l’observation GNOME. Même port/câble/boîtier/Quadro que 04H, noter l’heure. Un seul branchement, aucun cycle de répétition. Ne pas autoriser manuellement Bolt ni modifier sa politique ; relever sa décision existante.

**Étape 5 — collecte après branchement du même boot.** Identifier par 10de:1eb0, déduire tous les ponts parents du chemin sysfs, archiver lspci -nnvvk, resource et iomem, comparer les fenêtres avant/après. Vérifier tailles et débuts/fins, absence de flags UNSET et présence noyau ; inclusion de chaque BAR dans les fenêtres compatibles de chaque parent. Un BAR déclaré disabled sans pilote peut être attribué : ne pas confondre décodage et allocation. Contrôler GNOME/i915/Ethernet/SSH, erreurs d’allocation/AER/DPC/IOMMU/stockage/Thunderbolt. Ne charger aucun pilote pour tester CUDA.

Critères : A si BAR 1 et 3 attribués et couverts par tous les parents (BAR 0 aussi valide) ; B si amélioration réelle mais ressources incomplètes ; C si fenêtres insuffisantes et BAR restent absents ; D si données/conditions insuffisantes. Les avertissements et régressions restent signalés même en cas d’allocation réussie. Au premier défaut, cesser toute manipulation : conserver les logs, ne pas débrancher/redémarrer spontanément.

Collecteur préparé : [collecte-lecture-seule.py](mission04I-preparation/collecte-lecture-seule.py), à lancer depuis l’hôte avec sudo python3 et un **nouveau** dossier de sortie avant/après. Il lit seulement le système et écrit l’archive demandée. La collecte est complète et ponctuelle, pas un substitut aux flux distants pendant le branchement. Exemple futur, non exécuté :

```sh
sudo python3 /home/adminjarvis/JARVIS/rapports/mission04I-preparation/collecte-lecture-seule.py /home/adminjarvis/JARVIS/rapports/mission04I-essai/avant-branchement
```

Le même outil vers après-branchement ; vérifier les codes de sortie, le même boot ID et les empreintes. Les fichiers créés sous sudo pourront appartenir à root ; aucun changement de propriétaire système n’est nécessaire à la lecture.

## 8. Retour arrière ciblé, non exécuté

Si seul l’ajout GRUB est installé et aucune autre modification n’est intervenue, revenir sur demande en supprimant uniquement la source 45 et en restaurant le grub.cfg sauvegardé, après comparaison et contrôle syntaxique. Si GRUB a changé entre-temps, retirer seulement le bloc 45 via un candidat contrôlé : ne pas écraser des modifications autorisées plus récentes. Ne pas restaurer grubenv puisque la procédure ne l’altère pas ; conserver toutes les images/initramfs.

Pour quitter un boot problématique, choisir au redémarrage autorisé Debian 6.12.111 (défaut), puis 6.12.107/recovery si nécessaire ; ou l’entrée T2 diagnostic **sans Nouveau** pour comparer sans la réserve. Ne pas choisir l’entrée T2 générale sans blacklist pour un nouvel essai Core. Le retrait de l’entrée ne retire pas le paramètre du noyau déjà lancé : un retour à un autre boot nécessite l’accord de reboot. Tout retrait du Core nécessaire à la récupération doit également être autorisé. Si SSH est perdu, utiliser le secours local convenu ; aucun reset, rescan ou écriture PCIe à distance.

Ce retour conserve Debian, le noyau T2, leurs secours et les configurations Intel/SSH existantes ; il ne garantit pas une disponibilité permanente pendant un démarrage expérimental. Aucun changement i915, VFIO, EFI, réseau, service, pilote ou initramfs n’est requis par le plan.

**Statut final : étude et préparation terminées. Réservation 512M syntaxiquement prise en charge, utilité conditionnelle et non démontrée. Aucun changement GRUB installé. Attente de l’accord explicite d’installation ; débranchement, redémarrage et branchement futur restent des actions distinctes.**

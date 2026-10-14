**Statut actualisé : entrée 512M installée après accord explicite. Aucun retrait du Core, reboot ou essai matériel exécuté. Les étapes 2 et suivantes restent en attente de leurs autorisations.**

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

> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission04M.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 04M : validation de la réallocation PCIe ciblée

**D — Diagnostic incomplet : NON CONCLUANT. Ne pas brancher le Razer Core.**

La reconstruction PREF est réelle : 1024 Mio sur chaque pont amont, 512 Mio sur le port cible. Mais la fenêtre NP du port cible ne mesure que 2 Mio : elle ne peut pas recevoir le BAR0 de 16 Mio documenté en 04L, ni la marge NP de 32 Mio proposée. Le résultat technique accessible correspond à **B — réallocation partielle, ressources insuffisantes** ; la conclusion globale reste D faute de preuves privilégiées actuelles. A n'est pas établi ; C est contredit par l'agrandissement mesuré ; aucune preuve accessible ne suffit à conclure E ni à exclure toute régression.

## Démarrage et périmètre

Noyau `6.18.54-1-t2-trixie`. Ancien boot `[UUID EXPURGÉ]`, nouveau boot `[UUID EXPURGÉ]`. Ligne reçue :

```text
BOOT_IMAGE=/vmlinuz-6.18.54-1-t2-trixie root=/dev/mapper/JARVIS--MacMIini--vg-root ro quiet intel_iommu=on iommu=pt pm_async=off module_blacklist=nouveau pci=realloc=on pci=hpmmioprefsize=512M pci=resource_alignment=0000:00:01.2;0000:7b:00.0;0000:7c:01.0
```

`/sys/bus/pci/resource_alignment` contient exactement `0000:00:01.2;0000:7b:00.0;0000:7c:01.0`. Les identités restent celles attendues. L'image noyau conserve le SHA-256 de 04L : `a41e1a7680c5d76761a744d4265b7901bbd7494e90340fda1eb59eec73d72d1b`.

Contrôles système en lecture seule ; seules les preuves et le rapport utilisateur sont écrits. Aucun branchement, pilote NVIDIA, écriture PCI, GRUB, reboot ou changement i915/VFIO/ACPI/EFI.

## Comparaison historique / démarrage actuel

Adresses inclusives ; Mio = 1048576 octets. Pilote de tous les ponts ci-dessous : `pcieport`.

| Pont (domaine 0000) | NP avant | NP après | PREF avant | PREF après | Type PREF |
|---|---|---|---|---|---|
| 00:01.2 — 8086:1909 | 8fa00000–9dbfffff / 226 Mio | 8fa00000–8fffffff / 6 Mio | bf400000–cd3fffff / 224 Mio | 4000000000–403fffffff / 1024 Mio | 64 bits |
| 7b:00.0 — 8086:1578 | 8fa00000–9dbfffff / 226 Mio | 8fa00000–8fffffff / 6 Mio | bf400000–cd3fffff / 224 Mio | 4000000000–403fffffff / 1024 Mio | 64 bits |
| 7c:01.0 — 8086:15ea | 8fc00000–96bfffff / 112 Mio | 8fb00000–8fcfffff / 2 Mio | bf400000–c63fffff / 112 Mio | 4000000000–401fffffff / 512 Mio | 64 bits |
| 7c:04.0 — 8086:15ea, sœur | 96c00000–9dbfffff / 112 Mio | 8fe00000–8fffffff / 2 Mio | c6400000–cd3fffff / 112 Mio | 4020000000–403fffffff / 512 Mio | 64 bits |
| Intersection PREF cible | — | — | 112 Mio | 512 Mio | placement 256 + 32 possible |

## Ensemble des fenêtres de ponts

Les deux domaines Thunderbolt, les ponts SSD/Ethernet et les branches sœurs sont inclus pour vérifier les compatibilités.

| Pont PCI | Identité | Parent | NP après | PREF après | Type base/limite PREF |
|---|---|---|---|---|---|
| 0000:00:01.0 | 0x8086:0x1901 | pci0000:00 | désactivée | désactivée | [1, 1] |
| 0000:00:01.1 | 0x8086:0x1905 | pci0000:00 | `81800000–8f9fffff` (226 Mio) | `b1400000–bf3fffff` (224 Mio) | [1, 1] |
| 0000:00:01.2 | 0x8086:0x1909 | pci0000:00 | `8fa00000–8fffffff` (6 Mio) | `4000000000–403fffffff` (1024 Mio) | [1, 1] |
| 0000:00:1b.0 | 0x8086:0xa340 | pci0000:00 | désactivée | `b0000000–b12fffff` (19 Mio) | [1, 1] |
| 0000:00:1c.0 | 0x8086:0xa338 | pci0000:00 | `81000000–814fffff` (5 Mio) | désactivée | [1, 1] |
| 0000:00:1c.1 | 0x8086:0xa339 | pci0000:00 | `81600000–816fffff` (1 Mio) | `b1300000–b13fffff` (1 Mio) | [1, 1] |
| 0000:05:00.0 | 0x8086:0x1578 | 0000:00:01.1 | `81800000–8f9fffff` (226 Mio) | `b1400000–bf3fffff` (224 Mio) | [1, 1] |
| 0000:06:00.0 | 0x8086:0x15ea | 0000:05:00.0 | `81900000–819fffff` (1 Mio) | désactivée | [1, 1] |
| 0000:06:01.0 | 0x8086:0x15ea | 0000:05:00.0 | `81a00000–889fffff` (112 Mio) | `b1400000–b83fffff` (112 Mio) | [1, 1] |
| 0000:06:02.0 | 0x8086:0x15ea | 0000:05:00.0 | `81800000–818fffff` (1 Mio) | désactivée | [1, 1] |
| 0000:06:04.0 | 0x8086:0x15ea | 0000:05:00.0 | `88a00000–8f9fffff` (112 Mio) | `b8400000–bf3fffff` (112 Mio) | [1, 1] |
| 0000:7b:00.0 | 0x8086:0x1578 | 0000:00:01.2 | `8fa00000–8fffffff` (6 Mio) | `4000000000–403fffffff` (1024 Mio) | [1, 1] |
| 0000:7c:00.0 | 0x8086:0x15ea | 0000:7b:00.0 | `8fa00000–8fafffff` (1 Mio) | désactivée | [1, 1] |
| 0000:7c:01.0 | 0x8086:0x15ea | 0000:7b:00.0 | `8fb00000–8fcfffff` (2 Mio) | `4000000000–401fffffff` (512 Mio) | [1, 1] |
| 0000:7c:02.0 | 0x8086:0x15ea | 0000:7b:00.0 | `8fd00000–8fdfffff` (1 Mio) | désactivée | [1, 1] |
| 0000:7c:04.0 | 0x8086:0x15ea | 0000:7b:00.0 | `8fe00000–8fffffff` (2 Mio) | `4020000000–403fffffff` (512 Mio) | [1, 1] |

## Registres et sysfs

Ressources sysfs indices 14 = NP et 15 = PREF. Flags ciblés NP `0x200`, PREF `0x102201`. COMMAND.MEM actif sur les trois ponts. Les registres bruts 64 octets sont archivés par pont ; les décodages NP/PREF concordent avec sysfs sur les trois ponts ciblés. Le type PREF base et limite vaut 1, donc 64 bits ; les mots hauts valent 0x40.

| Pont | COMMAND | NP 0x20/0x22 | PREF 0x24/0x26 | Hauts 0x28/0x2c |
|---|---|---|---|---|
| 0000:00:01.0 | 0x407 | 0xfff0 / 0x0 | 0xfff1 / 0x1 | 0x0 / 0x0 |
| 0000:00:01.1 | 0x407 | 0x8180 / 0x8f90 | 0xb141 / 0xbf31 | 0x0 / 0x0 |
| 0000:00:01.2 | 0x407 | 0x8fa0 / 0x8ff0 | 0x1 / 0x3ff1 | 0x40 / 0x40 |
| 0000:00:1b.0 | 0x407 | 0xfff0 / 0x0 | 0xb001 / 0xb121 | 0x0 / 0x0 |
| 0000:00:1c.0 | 0x7 | 0x8100 / 0x8140 | 0xfff1 / 0x1 | 0x0 / 0x0 |
| 0000:00:1c.1 | 0x7 | 0x8160 / 0x8160 | 0xb131 / 0xb131 | 0x0 / 0x0 |
| 0000:05:00.0 | 0x7 | 0x8180 / 0x8f90 | 0xb141 / 0xbf31 | 0x0 / 0x0 |
| 0000:06:00.0 | 0x7 | 0x8190 / 0x8190 | 0xfff1 / 0x1 | 0x0 / 0x0 |
| 0000:06:01.0 | 0x407 | 0x81a0 / 0x8890 | 0xb141 / 0xb831 | 0x0 / 0x0 |
| 0000:06:02.0 | 0x7 | 0x8180 / 0x8180 | 0xfff1 / 0x1 | 0x0 / 0x0 |
| 0000:06:04.0 | 0x407 | 0x88a0 / 0x8f90 | 0xb841 / 0xbf31 | 0x0 / 0x0 |
| 0000:7b:00.0 | 0x7 | 0x8fa0 / 0x8ff0 | 0x1 / 0x3ff1 | 0x40 / 0x40 |
| 0000:7c:00.0 | 0x7 | 0x8fa0 / 0x8fa0 | 0xfff1 / 0x1 | 0x0 / 0x0 |
| 0000:7c:01.0 | 0x407 | 0x8fb0 / 0x8fc0 | 0x1 / 0x1ff1 | 0x40 / 0x40 |
| 0000:7c:02.0 | 0x7 | 0x8fd0 / 0x8fd0 | 0xfff1 / 0x1 | 0x0 / 0x0 |
| 0000:7c:04.0 | 0x407 | 0x8fe0 / 0x8ff0 | 0x2001 / 0x3ff1 | 0x40 / 0x40 |

## Inclusion, descendants et réserve

Toutes les allocations mémoire PCI actives relevées sont incluses dans les fenêtres de leurs ponts parents. L'audit complémentaire compare chaque BAR et chaque fenêtre active à chaque ancêtre et cherche les intersections entre ressources de même niveau : aucun échec d'inclusion ni collision détecté dans ce périmètre. Une ressource préchargeable peut être couverte par une fenêtre NP lorsque nécessaire. Les réservations non PCI/firmware restent invérifiables avec iomem masqué.

Sur 7c:00.0, NP `8fa00000–8fafffff` : NHI 7d:00.0 déplacé vers `8fa00000–8fa3ffff` et `8fa40000–8fa40fff`, pilote thunderbolt conservé. Sur 7c:02.0, NP `8fd00000–8fdfffff` : USB 7e:00.0 déplacé vers `8fd00000–8fd0ffff`, xhci_hcd conservé. Le port cible 7c:01.0 est vide ; sa sœur 7c:04.0 est vide et maintenant haute. Le blocage historique de la sœur basse a donc disparu.

La plage cible `4000000000–401fffffff` est libre de descendants et disjointe des autres allocations PCI relevées : **512 Mio contigus enregistrés**, couverts par les deux parents. Placement simultané naturel possible :

- BAR1 : `4000000000–400fffffff`, 256 Mio, base multiple de 256 Mio.
- BAR3 : `4010000000–4011ffffff`, 32 Mio, base multiple de 32 Mio.
- Solde PREF : 224 Mio.

Ce résultat arithmétique ne démontre pas un routage GPU réel, absent, ni l'inclusion dans l'aperture hôte actuelle : `/proc/iomem` est masqué. L'aperture haute 04L `4000000000–7fffffffff` est une référence historique seulement.

**NP bloquante** : 7c:01.0 ne possède que `8fb00000–8fcfffff`, 2 Mio ; même les parents n'offrent que 6 Mio NP chacun. Le prochain emplacement aligné à 16 Mio pour BAR0 est `90000000–90ffffff`, hors de ces fenêtres. Déporter un BAR NP dans la PREF haute n'est pas une solution valide. La combinaison PREF adéquate + NP suffisante échoue dans l'état actuel ; aucun agrandissement futur lors du hotplug n'est garanti.

HDA BAR4 est déplacé de `4000000000–40000fffff` à `4040000000–40400fffff`. Intel LPSS 00:1e.0 passe de `4000100000–4000100fff` à `4040100000–4040100fff`. Ils n'occupent donc pas la nouvelle PREF. Leurs pilotes sont conservés. Les changements exacts de toutes les ressources sont archivés dans `audit-initial.json`.

## Affichage, stockage et réseau

Nouveau absent de /proc/modules ; aucun périphérique NVIDIA en PCI. Intel 00:02.0 lié à i915, boot_vga=1 ; DP-3 connected/enabled et modes 1920×1080 présents. BAR Intel inchangés. Cela confirme la liaison et la sortie active ; réactivité visuelle du bureau à confirmer par l'utilisateur.

SSD Apple AP0512M 465,9 Gio : nvme0 live, 02:00.0 lié à nvme, BAR inchangés. Partitions : p1 976 Mio vfat /boot/efi ; p2 977 Mio ext4 /boot ; p3 464 Gio LVM2_member. Racine visible sur `/dev/mapper/JARVIS--MacMIini--vg-root`. Les options ro vues par findmnt sont celles du sandbox et ne prouvent pas un remontage hôte dû à une erreur. Les dispositifs dm complets et options hôte doivent être contrôlés au terminal SSH.

SMART actuel indisponible : `/usr/sbin/smartctl -a /dev/nvme0` retourne 2, « No such device » dans le namespace de périphériques restreint. Le collecteur original cherche smartctl dans PATH et n'a pas produit de fichier nvme-sante ; la tentative par chemin absolu est archivée. Ce refus ne prouve pas une panne du SSD. Les résultats SMART historiques de 04L ne sont pas réutilisés comme preuve actuelle. Erreurs d'E/S actuelles invérifiables faute de journal noyau.

Ethernet tg3, enp4s0 up, carrier=1, 1000 Mbit/s, BAR inchangés. Netlink bloqué ; espace réseau restreint ne montre que loopback. Adresse [ADRESSE PRIVÉE EXPURGÉE], route, écoute SSH, services et nouvelle connexion depuis le Mac ne sont pas confirmés par ces preuves. Confirmation humaine sollicitée, à documenter séparément si reçue.

## Journaux et limitations d'accès

`sudo -n id` échoue, y compris après la demande utilisateur de réessayer les droits : NoNewPrivs=1, capacités nulles, configuration sudo vue uid 65534. Aucun contournement tenté. `dmesg` : Operation not permitted. `journalctl -b -k` : No entries avec avertissement d'accès limité ; code 0 ne signifie pas journal complet. Journal système accessible limité à la session utilisateur. systemctl/boltctl : D-Bus bloqué. ss peut retourner 0 avec erreur netlink et sortie vide, qui ne démontre pas l'absence d'écoute.

Les recherches PCIe/AER/DPC/IOMMU/ACPI/Thunderbolt/NVMe/i915 dans les journaux privilégiés du boot actuel restent **non réalisables ici**. Aucun certificat d'absence d'erreurs ne peut être émis. Les tables ACPI sont aussi refusées. L'analyseur 04L retourne ARRET : ses contrôles PREF/placement ciblés réussissent, ses contrôles aperture hôte échouent sur adresses masquées. Ce dernier échec est un manque de preuve, pas une collision démontrée.

## Intégrité et méthode

Collecteur original et analyseur vérifiés contre SHA256SUMS 04L, identiques :

- collecte-hote.py : `75652db548609fc92eac57f2198a991695225c283a205721ac05beaba74b1af9`.
- verifier-reserve.py : `7bef9f20ccb5b8d0313ae31b4dc732cec22621b514d00d32404d36b9ae075316`.

Copies archivées ; analyseur original utilisé hors ligne. Le collecteur original exige root : adaptation locale documentée pour relever les données accessibles (suppression du garde root et du chown, répertoire de sortie 04M). Elle conserve commandes et lectures, avec erreurs et codes ; elle ne prétend pas être une collecte privilégiée. Collecteur original non modifié. Audit complémentaire hors ligne archivé avec son code et ses limites.

## Compléments à exécuter au terminal SSH privilégié

Voir `commandes-terminal-privilegie.txt`, reproduit ci-dessous. Les commandes de diagnostic sont en lecture seule ; le collecteur original écrit uniquement ses preuves dans l'espace utilisateur.

```bash
# Depuis le Mac : nouvelle connexion, puis commandes dans le terminal SSH hôte.
ssh adminjarvis@[ADRESSE PRIVÉE EXPURGÉE]
# Vérifier les outils avant exécution (empreintes attendues Mission 04L).
sha256sum /home/adminjarvis/JARVIS/rapports/mission04L-preparation/collecte-hote.py /home/adminjarvis/JARVIS/rapports/mission04L-preparation/verifier-reserve.py
# collecte-hote.py : 75652db548609fc92eac57f2198a991695225c283a205721ac05beaba74b1af9
# verifier-reserve.py : 7bef9f20ccb5b8d0313ae31b4dc732cec22621b514d00d32404d36b9ae075316
# Collecteur original : lectures hôte, écrit uniquement des preuves utilisateur.
sudo python3 /home/adminjarvis/JARVIS/rapports/mission04L-preparation/collecte-hote.py
# Noter le dossier « Preuves » affiché, puis :
python3 /home/adminjarvis/JARVIS/rapports/mission04L-preparation/verifier-reserve.py /CHEMIN/EXACT/DU/DOSSIER_PREUVES
# Compléments en lecture seule :
uname -r
cat /proc/sys/kernel/random/boot_id /proc/cmdline /sys/bus/pci/resource_alignment
sudo cat /proc/iomem
sudo journalctl -b -k --no-pager -o short-iso-precise
sudo journalctl -b -k --no-pager -o short-iso-precise | rg -i 'pci|aer|dpc|dmar|iommu|acpi|thunderbolt|nvme|i915|I/O error|reset|timeout|no space|failed|error'
sudo journalctl -b -u ssh.service -u ssh.socket -u bolt.service --no-pager -o short-iso-precise
sudo /usr/sbin/smartctl -a /dev/nvme0
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,MODEL
findmnt
ip -details address show enp4s0
ip route
sudo ss -lntp
sudo ss -ntp
systemctl status ssh.service ssh.socket display-manager.service --no-pager
boltctl list
# Attendre cinq minutes en surveillant le bureau ; refaire le collecteur original.
# Confirmer manuellement nouvelle connexion SSH et bureau Intel réactif.
# Aucun setpci, rescan, chargement de module, modification GRUB ou redémarrage.

```

## Décision

**D — NON CONCLUANT**, accès aux preuves essentielles incomplet. **B établi dans le périmètre PCI visible** : la PREF est reconstruite et permet les BAR1/BAR3, mais NP insuffisante pour BAR0 et fonctions supplémentaires. Ne pas brancher le Core ; aucun pilote ou changement système. Attente de l'accord utilisateur pour toute suite ; même une collecte privilégiée favorable ne résoudrait pas à elle seule l'insuffisance NP mesurée.

## Observation initiale / finale

Relevé initial 20261011-222715, final 20261011-223221, durée mesurée 322.6 secondes (au moins cinq minutes). Boot identique. Ressources et pilotes de tous les périphériques PCI inchangés : True. Configurations brutes de ponts inchangées : True.

| État | Initial | Final |
|---|---|---|
| /sys/class/nvme/nvme0/state | live | live |
| /sys/class/net/enp4s0/operstate | up | up |
| /sys/class/net/enp4s0/carrier | 1 | 1 |
| /sys/class/net/enp4s0/speed | 1000 | 1000 |
| /sys/class/drm/card0-DP-3/enabled | enabled | enabled |
| /sys/class/drm/card0-DP-3/status | connected | connected |

Observation stable dans le périmètre accessible ; aucune affirmation d’absence d’erreurs noyau, de santé SMART complète ou de stabilité humaine du bureau. Nouvelle connexion SSH et bureau réactif non confirmés par l’utilisateur au moment de la clôture.

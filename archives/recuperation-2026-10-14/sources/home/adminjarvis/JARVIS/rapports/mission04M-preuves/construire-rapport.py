from pathlib import Path
import json,datetime
base=Path('/home/adminjarvis/JARVIS/rapports/mission04M-preuves'); snaps=sorted(base.glob('hote-*'));a=snaps[0];z=snaps[-1]
s=json.loads((a/'pci-sysfs.json').read_text());audit=json.loads((base/'audit-initial.json').read_text())
def interval(t):
 a,z,f=t
 return f'`{a:x}–{z:x}` ({(z-a+1)/1048576:g} Mio)' if f&0x200 else 'désactivée'
text='''# JARVIS — Mission 04M : validation de la réallocation PCIe ciblée

**D — Diagnostic incomplet : NON CONCLUANT. Ne pas brancher le Razer Core.**

La reconstruction PREF est réelle : 1024 Mio sur chaque pont amont, 512 Mio sur le port cible. Mais la fenêtre NP du port cible ne mesure que 2 Mio : elle ne peut pas recevoir le BAR0 de 16 Mio documenté en 04L, ni la marge NP de 32 Mio proposée. Le résultat technique accessible correspond à **B — réallocation partielle, ressources insuffisantes** ; la conclusion globale reste D faute de preuves privilégiées actuelles. A n'est pas établi ; C est contredit par l'agrandissement mesuré ; aucune preuve accessible ne suffit à conclure E ni à exclure toute régression.

## Démarrage et périmètre

Noyau `6.18.54-1-t2-trixie`. Ancien boot `a5d47772-9fed-4f51-8d99-ffe75be725b1`, nouveau boot `b88dab5b-c58b-49fb-85a1-9fd50b9e9716`. Ligne reçue :

```text
'''+(a/'proc_cmdline.txt').read_text().strip()+'''
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
'''
for b in audit['bridges']:
 text+=f"| {b['bdf']} | {b['id']} | {b['parent']} | {interval(b['NP'])} | {interval(b['PREF'])} | {b['PREF_type']} |\n"
text+='''
## Registres et sysfs

Ressources sysfs indices 14 = NP et 15 = PREF. Flags ciblés NP `0x200`, PREF `0x102201`. COMMAND.MEM actif sur les trois ponts. Les registres bruts 64 octets sont archivés par pont ; les décodages NP/PREF concordent avec sysfs sur les trois ponts ciblés. Le type PREF base et limite vaut 1, donc 64 bits ; les mots hauts valent 0x40.

| Pont | COMMAND | NP 0x20/0x22 | PREF 0x24/0x26 | Hauts 0x28/0x2c |
|---|---|---|---|---|
'''
for b in audit['bridges']:
 r=b['registers'];text+=f"| {b['bdf']} | {r['0x4']} | {r['0x20']} / {r['0x22']} | {r['0x24']} / {r['0x26']} | {r['0x28']} / {r['0x2c']} |\n"
text+='''
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

Ethernet tg3, enp4s0 up, carrier=1, 1000 Mbit/s, BAR inchangés. Netlink bloqué ; espace réseau restreint ne montre que loopback. Adresse 192.168.1.99, route, écoute SSH, services et nouvelle connexion depuis le Mac ne sont pas confirmés par ces preuves. Confirmation humaine sollicitée, à documenter séparément si reçue.

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
'''+(base/'commandes-terminal-privilegie.txt').read_text()+'''
```

## Décision

**D — NON CONCLUANT**, accès aux preuves essentielles incomplet. **B établi dans le périmètre PCI visible** : la PREF est reconstruite et permet les BAR1/BAR3, mais NP insuffisante pour BAR0 et fonctions supplémentaires. Ne pas brancher le Core ; aucun pilote ou changement système. Attente de l'accord utilisateur pour toute suite ; même une collecte privilégiée favorable ne résoudrait pas à elle seule l'insuffisance NP mesurée.
'''
(base.parent/'mission04M.md').write_text(text)
print('Rapport préparé')

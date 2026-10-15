# Mission 04U

- Identifiant : 04U.
- Date ou période : 12 octobre 2026
- Objectif initial : JARVIS — Mission 04U : localiser le masquage Intel entre GRUB et Linux
- Matériel mentionné : Mac mini / Macmini8,1 / Razer Core
- Logiciels mentionnés : Debian / T2Linux / NVIDIA
- État final documentaire : **NON VÉRIFIÉ**. Documents retrouvés ; réception finale non établie dans cette première passe.

## Actions et résultats confirmés

Documents retrouvés ; réception finale non établie dans cette première passe.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Documents retrouvés ; réception finale non établie dans cette première passe.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [mission04U.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04U.md)
- [mission04U-dmesg.txt](../../archives/preuves-controlees/part-060.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/mission04U-dmesg.txt`
- [mission04U-journal-noyau.txt](../../archives/preuves-controlees/part-060.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/mission04U-journal-noyau.txt`

## Références et dépendances

04N-P, 04O-P, 04P-P, 04T, 04U-D, 04U-J. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [mission04U.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04U.md)

Date : 12 octobre 2026. Mac mini 2018, Debian 13 T2Linux, noyau `6.18.54-1-t2-trixie`.

**Conclusion : la transition `DEVEN 0x3f → 0x0f` est établie entre les mesures communiquées dans GRUB et Linux. Son auteur n’est pas identifié. Les candidats prioritaires sont une intervention firmware pendant le transfert EFI, ou une interaction ACPI/firmware déclenchée par Linux. Une écriture directe du noyau reste à vérifier sur les sources exactes du binaire T2 installé.**

**Mise à jour après réception des fichiers : les deux captures complètes de 1 538 lignes ont été analysées. Le dmesg commence à 0.000000. Intel manque dès le scan initial du bus racine, vers 0,167 s, avant la réallocation publiée à 0,262 s et avant la détection NVIDIA à 3,965 s. Aucun résultat du boot 04R n’est attribué au boot 04U. Les journaux ne mesurent toutefois pas DEVEN à cet instant et ne tracent pas son écriture.**

Seules des lectures et la création de ce rapport ont été effectuées. Aucun redémarrage, débranchement, rescan, chargement de pilote, installation, écriture DEVEN ou modification GRUB/EFI/PCIe/ACPI/systemd. Tous les protocoles ci-dessous sont des propositions non exécutées, nécessitant une autorisation distincte.

## 1. Preuves et provenance


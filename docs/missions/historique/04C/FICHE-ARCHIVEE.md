> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS-Documentation/missions/mission-04c/README.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 04C

- Identifiant : 04C.
- Date ou période : Date de contenu non établie ; métadonnées disponibles dans MANIFESTE.json.
- Objectif initial : Mission 04C — Plan exact, non exécuté
- Matériel mentionné : Mac mini
- Logiciels mentionnés : Debian
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

- grubenv (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/boot/grub/grubenv`
- __init__.py (référence locale historique non publiée)
- grub.cfg-apres (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357/grub.cfg-apres`
- initrd.img-6.18.54-1-t2-trixie-contenu.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357/initrd.img-6.18.54-1-t2-trixie-contenu.txt`
- 43_jarvis_t2_egpu_diagnostic (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04C-preparation/43_jarvis_t2_egpu_diagnostic`
- empreintes-apres-installation.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04C-preparation/empreintes-apres-installation.txt`
- empreintes-apres-preparation.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04C-preparation/empreintes-apres-preparation.txt`
- entree-grub-prevue.cfg (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04C-preparation/entree-grub-prevue.cfg`
- installation-diff.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04C-preparation/installation-diff.patch`
- plan-installation-et-essai.md (référence locale historique non publiée)
- validation-installation.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04C-preparation/validation-installation.txt`
- validation-preparation.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04C-preparation/validation-preparation.txt`
- verification-apres-demarrage.sh (référence locale historique non publiée)

## Références et dépendances

04C-P. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### plan-installation-et-essai.md (référence locale historique non publiée)

## Fichiers et modification proposée

Source préparée : `/home/adminjarvis/JARVIS/rapports/mission04C-preparation/43_jarvis_t2_egpu_diagnostic`.
Destination nouvelle : `/etc/grub.d/43_jarvis_t2_egpu_diagnostic`, propriétaire root:root, mode 0755.
Titre : **JARVIS — T2 eGPU diagnostic sans Nouveau**.
ID : `jarvis-t2-egpu-sans-nouveau`.

Le fichier reprend les chemins, UUID du /boot et racine LVM de l’entrée T2 déjà installée. Il ajoute une entrée distincte, sans modifier la précédente. Contenu exact :

```sh

# Mission 03

- Identifiant : 03.
- Date ou période : Date de contenu non établie ; métadonnées disponibles dans MANIFESTE.json.
- Objectif initial : Objectif non explicité dans un rapport autonome retrouvé.
- Matériel mentionné : Non documenté dans les rapports retenus.
- Logiciels mentionnés : Non documenté dans les rapports retenus.
- État final documentaire : **PARTIEL**. Démarrage T2 et scans Wi-Fi/Bluetooth rapportés réussis ; association et appairage restent ouverts.

## Actions et résultats confirmés

Démarrage T2 et scans Wi-Fi/Bluetooth rapportés réussis ; association et appairage restent ouverts.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Démarrage T2 et scans Wi-Fi/Bluetooth rapportés réussis ; association et appairage restent ouverts.

Rapport autonome non retrouvé. Des preuves ou références indirectes peuvent exister dans le manifeste.

## Documents et preuves

- [ssh](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/7e6d714df7cc/etc/default/ssh`
- [sshd_config](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/7e6d714df7cc/etc/ssh/sshd_config`
- [00-jarvis.conf](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/7e6d714df7cc/etc/ssh/sshd_config.d/00-jarvis.conf`
- [NetworkManager-wait-online.service](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/7e6d714df7cc/usr/lib/systemd/system/NetworkManager-wait-online.service`
- [ssh.service](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/7e6d714df7cc/usr/lib/systemd/system/ssh.service`
- [ssh.socket](../../archives/preuves-controlees/part-001.tar.gz) — membre `archives/recuperation-2026-10-14/membres/7e6d714df7cc/usr/lib/systemd/system/ssh.socket`
- [grub.cfg](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/boot/grub/grub.cfg`
- [grubenv](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/boot/grub/grubenv`
- [grub](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/default/grub`
- [00_header](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/00_header`
- [05_debian_theme](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/05_debian_theme`
- [10_linux](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/10_linux`
- [20_linux_xen](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/20_linux_xen`
- [25_bli](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/25_bli`
- [30_os-prober](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/30_os-prober`
- [30_uefi-firmware](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/30_uefi-firmware`
- [35_fwupd](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/35_fwupd`
- [40_custom](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/40_custom`
- [41_custom](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/41_custom`
- [README](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/membres/ad2241b1fe5e/etc/grub.d/README`
- [__init__.py](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/conversation/jarvis/__init__.py)
- [99-jarvis-t2.cfg-avant](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357/99-jarvis-t2.cfg-avant`
- [generation-test.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357/generation-test.log`
- [grub.cfg-apres](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357/grub.cfg-apres`
- [hashes-avant.json](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357/hashes-avant.json`
- [initrd.img-6.12.107+deb13-amd64-contenu.txt](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357/initrd.img-6.12.107+deb13-amd64-contenu.txt`
- [initrd.img-6.12.111+deb13-amd64-contenu.txt](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357/initrd.img-6.12.111+deb13-amd64-contenu.txt`
- [initrd.img-6.18.54-1-t2-trixie-contenu.txt](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-20261011-180357/initrd.img-6.18.54-1-t2-trixie-contenu.txt`
- [42_jarvis_t2](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-proposition/42_jarvis_t2`
- [99-jarvis-t2.cfg](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-proposition/99-jarvis-t2.cfg`
- [entree-t2.cfg](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-proposition/entree-t2.cfg`
- [menu-simulation.cfg](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-grub-proposition/menu-simulation.cfg`
- [SHA256SUMS](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437/SHA256SUMS`
- [ecoutes-apres.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437/ecoutes-apres.log`
- [etat-apres.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437/etat-apres.log`
- [etat-avant.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437/etat-avant.log`
- [journal-apres.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437/journal-apres.log`
- [journal-demarrage.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437/journal-demarrage.log`
- [10-jarvis-socket.conf](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437/ssh.service.d/10-jarvis-socket.conf`
- [10-jarvis-lan.conf](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437/ssh.socket.d/10-jarvis-lan.conf`
- [unites-apres.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437/unites-apres.log`
- [unites-avant.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-ssh-proposition-20261011-182437/unites-avant.log`
- [audio.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-validation-hote-20261011-1819/audio.log`
- [noyau.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-validation-hote-20261011-1819/noyau.log`
- [smart.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-validation-hote-20261011-1819/smart.log`
- [ssh.log](../../archives/preuves-controlees/part-002.tar.gz) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission03-validation-hote-20261011-1819/ssh.log`

## Références et dépendances

Aucune référence explicite extraite.. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports



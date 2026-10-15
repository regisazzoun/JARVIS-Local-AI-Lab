# Phase C2 — plan préparé, non appliqué

Préparation : /home/adminjarvis/JARVIS/rapports/phaseC2-preparation. Destination commune : /usr/lib/firmware/brcm (alias /lib/firmware/brcm). Les quatre fichiers n’existent pas actuellement ; ajout uniquement, root:root, 644.

| Fichier | Octets | SHA256 |
|---|---:|---|
| `brcmfmac4364b2-pcie.apple,lanai.bin` | 1026416 | `837b83cea19be2ff13061f93c1f2b64907b90cc520a393888385def11473ba37` |
| `brcmfmac4364b2-pcie.apple,lanai-HRPN-u.txt` | 12895 | `7d15d2f6346a1e8bbd0de1f4f63c75127baafb13be6901530eadf347bbafe362` |
| `brcmfmac4364b2-pcie.apple,lanai.clm_blob` | 30626 | `088906b75952e0444d913440e0ff08696c9044bcc3fc038bda707e22fe2e3d7c` |
| `brcmfmac4364b2-pcie.apple,lanai.txcap_blob` | 489 | `422ca743214254d2f236f482b7a61d8e67ef48db371442223374bf97ed7acfe4` |

Sources exactes et empreintes : manifest-installation.json. Image Apple Sonoma 14.6.1 / build 23G93 / produit récupération 696-08090 ; origine et URL dans recovery/provenance.json. Télécharger uniquement BaseSystem.dmg (753 Mio) et sa chunklist ; pas d’installateur macOS complet.

Le helper OSX-KVM est figé au commit 4c378a4b5e0b219783683012bec680325eb40719, code lu. Adaptation locale download-reviewed.py : appel recovery via HTTPS, téléchargement oscdn.apple.com via HTTP officiel (certificat HTTPS incompatible), rejet des autres domaines ; pas de désactivation TLS. Tous les blocs SHA256 et la signature RSA de la chunklist ont été validés avant usage ; clé Apple intégrée au helper audité, sans attestation indépendante supplémentaire. SHA256 locaux dans images-sha256.json. firmware.sh figé par empreinte, lu et bash -n validé ; seul son convertisseur Python a été extrait dans rename-reviewed.py et exécuté sans root. Aucun appel de ses branches installation/montage/rechargement.

dmg2img Debian a été téléchargé et extrait localement, sans installation système. SHA256 du .deb identique aux métadonnées APT : 4b1145b01c9a8c719e1ed940cab5def3849dac691d32904859306163e79394b5. Image convertie puis loop créé read-only ; partition HFS+ montée ro,nosuid,nodev,noexec. Montage et loop retirés après extraction. Liens Apple lanai.trx -> ekans.trx et fichiers de variantes X3 résolus exclusivement dans l’image. Archive de renommage contrôlée pour chemins relatifs simples et liens internes sûrs ; seuls les quatre membres retenus sont matérialisés comme fichiers réguliers, pas de lien installé. Les quatre empreintes sont identiques aux sources Apple.

La demande noyau est lanai-HRPN-u-7.5-X3 ; les noms moins spécifiques ci-dessus sont ceux produits par l’algorithme T2Linux : le binaire et les blobs sont communs à lanai, le NVRAM sélectionné reste spécifiquement HRPN-u version module 7.5. Ne pas copier la variante Murata m ou B3 ; ne pas créer de BCM.hcd depuis un fichier PCIe 4377.

## Commandes proposées après accord

Exécuter les commandes de installation-proposee.sh après revue et contrôle de l’état courant. Le script vérifie les hashes, sshd et l’absence des quatre destinations avant copie. Puis :

```bash
sudo -n install -o root -g root -m 644 SOURCE DESTINATION
sudo -n /usr/sbin/modprobe -r brcmfmac
sudo -n /usr/sbin/modprobe brcmfmac
```

La première commande sera répétée pour chacun des quatre chemins exacts du manifeste. Aucun téléchargement/sudo distant dans le script. Ne pas décharger tg3, usbcore, hci_uart ou t2bce, ne pas redémarrer NetworkManager/SSH, ne pas changer les routes. Si un déchargement refuse pour module utilisé, arrêter ; aucun force-unload. Rechargement Wi-Fi seulement : Ethernet utilise tg3, indépendant de brcmfmac. Pas de broadcom-wl, apt install, DKMS, update-initramfs, noyau ou GRUB.

Vérifier stat (root:root 644), hashes installés, pilote PCI, nouveau journal brcmfmac, interface NetworkManager, rfkill et scan Wi-Fi : `nmcli -f IN-USE,SSID,SIGNAL,SECURITY device wifi list --rescan yes`. Ne pas créer de connexion Wi-Fi ni changer la route Ethernet automatiquement ; le test d’association nécessitera le SSID/choix réseau de l’utilisateur. Vérifier ip/route, HTTPS et écoute SSH après le rechargement, puis comparer les empreintes /boot avec boot-sha256-avant.txt.

## Bluetooth

Contrôleur UART serial0-0, ACPI BCM2E7C:APPLE-UART-BLTH, hci_uart_bcm ; puce BCM4364B0 Maui Olympic GEN (MFG), chip id 123. Bluetooth déjà listé par BlueZ, Powered=yes, Discovering=no, aucun périphérique enregistré. Erreurs -16 baudrate, absence reset et brcm/BCM.hcd restent à qualifier par un test matériel. L’image ne contient aucun fichier BCM4364 dans usr/share/firmware/bluetooth, et aucune ressource HEX/HCD correspondante n’a été trouvée dans usr ou System/Library/Extensions ; elle contient des firmwares Bluetooth PCIe 4377/4378 et suivants, incompatibles avec ce chemin UART. Le convertisseur upstream ignore les anciens UART. Aucun fichier Bluetooth n’est donc proposé à l’installation dans ce lot, aucune promesse de réparation par ce firmware Wi-Fi.

Après accord pour les tests : `bluetoothctl show`, `bluetoothctl --timeout 15 scan on`, puis `bluetoothctl scan off`, et journal Bluetooth récent. Aucun appairage, changement de sécurité, désactivation de bonding ou reload hci_uart proposé. Un périphérique en mode découverte est nécessaire pour établir la réception radio ; un scan vide ne prouve pas une panne. Ne pas reconstruire de pilote/noyau pour contourner le problème. Si le test échoue, poursuivre un diagnostic séparé UART avec source matérielle exacte avant proposition supplémentaire.

## Sauvegarde et retour arrière

firmware-brcm-avant.tgz sauvegarde tous les firmwares brcm existants ; empreinte dans images-sha256.json. Inventaire de destinations inexistantes dans le manifeste. Pour annuler ce lot : supprimer uniquement les quatre fichiers ajoutés (vérifier leurs empreintes auparavant) puis recharger uniquement brcmfmac si sûr. Ne pas écraser tout le répertoire par l’archive, ce qui pourrait effacer une modification ultérieure. Prévoir de réactualiser la sauvegarde si les firmwares système changent avant accord.

Aucun reboot prévu. Un reboot et toute autre correction nécessitent un accord distinct. NVIDIA hors périmètre.

Sources : https://wiki.t2linux.org/guides/wifi-bluetooth/ ; https://raw.githubusercontent.com/kholia/OSX-KVM/4c378a4b5e0b219783683012bec680325eb40719/fetch-macOS-v2.py ; scripts et manifestes conservés localement.

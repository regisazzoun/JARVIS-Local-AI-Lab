# Laboratoire : préparation reproductible et recette future

**Statut : code préparé ; aucun démarrage VM ou essai PXE réel réalisé.**

1. Fournir les exécutables utilisateur validés (voir architecture), vérifier leurs versions et la possibilité de lancer QEMU TCG sans privilège. Ne pas activer dnsmasq/libvirt sur l'hôte.
2. Fournir sous `deployment/13de/lab/assets` le firmware `OVMF_CODE.fd`, `debian/linux` et `debian/initrd.gz` issus du netboot **trixie amd64**. Vérifier les signatures et sommes Debian officielles avant extraction ; ne pas accepter un checksum obtenu du même téléchargement non authentifié comme preuve suffisante.
3. Construire `ipxe.efi` UEFI avec script embarqué qui fait `dhcp` puis `chain tftp://10.0.2.2/boot.ipxe`. Un binaire iPXE générique sans ce script peut boucler sur le bootfile DHCP ; ne pas le considérer prêt. Copier le `pxe/boot.ipxe` livré vers les actifs. Secure Boot invité n'est pas validé ; firmware OVMF sans Secure Boot uniquement pour cette première recette.
4. Ajouter les trois fichiers privés de bootstrap à l'initrd gzip/cpio (`preseed.cfg`, `install-ssh.sh`, `authorized_key`), conserver l'original et vérifier l'archive. Le preseed est un **template laboratoire**, avec garde QEMU/UEFI et disque vda, non validé par l'installateur. Les retours d'erreur des hooks doivent être vérifiés en VM avant toute recette considérée sûre.
5. Produire `SHA256.json` : objet JSON associant chaque nom relatif obligatoire à son SHA-256, après vérification de provenance. Ne pas versionner les actifs ou initrd contenant la clé publique.
6. Résoudre le miroir de paquets sans donner accès au réseau réel : CD/DVD Debian authentifié et configuration d-i adaptée ou serveur de miroir dans une seconde VM isolée. La présente version ne livre pas ce serveur ni la configuration CD ; une installation complète est donc bloquée volontairement.
7. Utiliser `python3 lab/controller.py create vm-test1`, puis `plan vm-test1`, `run vm-test1`, `logs vm-test1`, `destroy vm-test1`. `create` échoue avant création si qemu-img manque. Échec partiel : garder le marqueur pour diagnostic puis supprimer par le contrôleur. Limiter à une VM à la fois ; quota disque externe recommandé avant service multiutilisateur.

Le réseau SLIRP permet DHCP/TFTP internes sans écoute production. Le menu demande kernel/initrd via TFTP ; HTTP n'est pas implémenté dans cette première version isolée. Pour HTTP, préparer ultérieurement un serveur dans une VM de services sur un segment socket QEMU privé, sans bridge hôte, et valider les ACL. Aucun serveur HTTP/TFTP/DHCP système n'est créé ici.

## Réception 14A à produire par le modèle local

- Trace modèle → outil → worker → résultat, identifiant VM et empreintes des actifs.
- Console UEFI/iPXE et requêtes TFTP réelles ; Debian 13 installé, sortie disque puis second démarrage (le worker actuel reste en boot réseau et `-no-reboot` : phase de boot disque à ajouter).
- SSH authentifié avec empreinte, `sudo -n true`, Ansible convergence et seconde exécution sans changement.
- RAID1 VM et démarrage dégradé ultérieurs si une recette RAID est ajoutée.
- Injection d'une panne réversible sur une fixture neuve ; diagnostic, recherche documentaire, correction et nouvel essai choisis par JARVIS, pas un scénario résolu par Codex.
- Journaux installateur `/var/log/installer`, erreurs, versions, temps, contrôle de non-régression hôte par outils en lecture seule.

La capture série seule n'est pas une extraction de tous les journaux installateur. Le code conserve `installation_verified: false` même si QEMU sort avec 0. Les ressources créées par un autre outil ou hors du workspace ne sont jamais supprimées.

# 13D-E — bootstrap en deux phases, 16 octobre 2026

## État et prochaine étape physique

Le PXE UEFI physique est acquis : snponly.efi → iPXE → noyau/initrd → Debian Installer. Il n'est ni reconçu ni simulé à nouveau. Le premier essai Legacy avait échoué ; le second UEFI a atteint Debian. Aucun disque Dell n'a été écrit par cette session.

La nouvelle session préparée est **découverte automatique seulement** : preseed embarqué, chargement des pilotes réseau PCI et NVMe, DHCP par netcfg, lecture /proc et /sys, envoi authentifié vers JARVIS et blocage indéfini avant retour à l'installateur. Aucun copier-coller de résultats ni de clé sur le Dell. La réception imprime le rapport dans Codex et produit un manifeste non approuvé. Si le réseau, les pilotes ou la validation échouent, le démarrage reste bloqué sans passer au partitionnement. Le comportement early_command/netcfg doit encore être éprouvé sur le Dell ; le PXE de transport, lui, est déjà validé.

Actifs privés prêts : `deployment/13de/private/bootstrap-discovery-02/`. Aucun service n'est actif. Après **autorisation réseau n°1** seulement :

```sh
sudo -n python3 deployment/13de/bootstrap/serve-discovery.py deployment/13de/private/bootstrap-discovery-02
```

ProxyDHCP/TFTP/HTTP existants réutilisés. Interface/IP JARVIS et MAC Dell réelles conservées dans la configuration privée de session. Le récepteur 8090 accepte le sous-réseau local et le filtre nft impose la MAC Dell : l'IP Dell peut changer au DHCP sans inventer d'adresse. Bbox conserve l'allocation. Fichiers HTTP limités à linux/initrd.gz/discovery.ipxe. Fin au rapport, erreur d'un service ou après 15 minutes ; retrait de la seule table temporaire jarvis_bootstrap. Aucun systemd/service existant modifié.

Ensuite seulement demander F12 → UEFI IPv4 au propriétaire. Le serveur recevra `hardware-report.txt`, son empreinte et son IP source, puis `manifest.unapproved.json` si l'identité passe les contrôles. Toute différence de produit DMI est conservée dans le rapport et exige revue ; le guard d'installation historique reste strict `Precision 5820 Tower`. Le profil strict existant n’est pas élargi avant lecture du DMI réel ; un autre libellé bloque le manifeste sans perdre le rapport brut.

## Phase A — installation candidate, non autorisée

`preseed-bootstrap.candidate.cfg` réutilise la recette existante : GPT, ESP indépendante d'environ 1 Gio sur chaque disque, deuxième partition de chaque disque membre du RAID1 ext4 racine, pas de RAID VROC ni de swap partitionné. Les noms de disques sont dérivés du manifeste, et non choisis par approximation commerciale.

`build-install.py` conserve le guard avant partman et au late_command. Sans approbation, aucun approved-erase.sha256 ni confirmation automatique ni autorisation de reboot n'est inclus. Les artefacts installables restent impossibles tant que ces éléments ne sont pas établis :

1. Identité réelle : UUID, deux chemins NVMe, modèles, séries distinctes et capacités exactes ; aucun disque physique supplémentaire.
2. Qualification ciblée de la recette partman RAID/ESP. Elle n'a pas été effectuée ici. Les contrôles après installation ne remplacent pas cette qualification préalable.
3. **Autorisation n°2** explicite portant sur ces deux séries et l'effacement complet, avec décision de reboot séparément consignée dans ce même accord.
4. Revue de l'exposition LAN et des opérations EFI de l'installation (GRUB et entrée secondaire NVRAM). Aucun réglage BIOS/VMD/VROC n'est changé.

Le JSON d'approbation privé doit contenir : installation_authorized=true, serials exactes, manifest_sha256 du JSON brut, recipe_sha256 du template, base_initrd_sha256 de l'initrd Debian vérifié, payload_sha256 pour guard-physical.sh et les quatre scripts install-bootstrap.sh/finalize-efi.sh/sync-esp.sh/verify-storage.py, raid_efi_qualified=true, lan_exposure_reviewed=true, expires_at futur en secondes Unix ; reboot_authorized doit être explicitement true pour poursuivre au reboot. Ces preuves ne sont jamais créées à partir d'une supposition. Le builder ne signe pas l'approbation : elle matérialise la décision humaine enregistrée dans la session.

Un secret unique de déploiement a été généré localement dans `private/bootstrap-secret-01/`, permissions 0700/0600. Le clair n'est ni affiché, ni inclus dans un URL, un argument de processus, le preseed ou l'initrd. Seul le hash SHA-512 crypt est embarqué dans le futur candidat d'installation. `prepare-secret.py` ne modifie aucun compte ni aucune clé du Mac mini.

Le système cible prévoit openssh-server, sudo, Python, mdadm, utilitaires NVMe/SMART/PCI/DMI, efibootmgr, rsync et wget. Root par SSH interdit. PasswordAuthentication est désactivé globalement, avec exception seulement pour jarvis-bootstrap depuis l’IPv4 JARVIS validée ; AllowUsers limite aussi jarvisadmin à JARVIS. Sudo bootstrap temporairement complet. Aucune clé/configuration SSH du Mac modifiée.

Un contrôle à 24 h émet une alerte si la reprise n'est pas terminée. **Il ne verrouille jamais le compte avant la preuve positive d'accès permanent.** Après abandon, supprimer les secrets locaux et révoquer explicitement la cible si elle existe ; ne pas réutiliser le secret dans un nouveau déploiement. Un nouveau cycle exige un nouveau secret. Après preuve d'accès par clé et révocation vérifiée, le contrôleur supprime automatiquement le clair et le hash locaux. Les anciens initrd installables contenant hash/capacité doivent alors être retirés du service et supprimés des actifs locaux selon leur chemin enregistré ; la suppression n'est pas une garantie d'effacement physique sur SSD.

`finalize-efi.sh` refuse un miroir incorrect/dégradé et attend au plus 2 h la fin de sa synchronisation initiale. Il exige les deux ESP FAT/GPT distinctes, vérifie l'ESP montée, copie les mêmes binaires Debian signés sur ESP2 et crée EFI/BOOT sur les deux. Aucune commande de formatage dans la finalisation. Le hook sync-esp.sh maintient ensuite la copie lors des mises à jour APT. Qualification de la recette, amorçage réel depuis chacun des NVMe, démarrage dégradé et reconstruction restent des réserves : aucune résilience n'est revendiquée comme testée.

## Phase B — prise de contrôle explicite

Au premier boot installé, un service cible lit DMI/stockage et la **clé hôte publique** SSH générée sur le Dell, puis les envoie au récepteur privé. Il retente après échec, marque le succès et supprime sa copie locale du collecteur contenant la capacité. Aucune clé hôte privée ne sort du Dell.

`import-install-report.py` compare l'identité au manifeste approuvé, associe la clé hôte à l'IP effectivement observée et prépare les réglages de takeover avec administration_authorized=false. Il n'approuve pas l'administration.

**Limite de confiance :** le PXE/TFTP/HTTP existant ne chiffre ni n'authentifie cryptographiquement l'initrd sur un LAN hostile. Une capacité incluse dans cet initrd peut y être observée ; MAC et jeton ne sont pas une attestation matérielle. La réception de la clé hôte permet son épinglage pour les connexions suivantes, mais n'apporte pas une preuve indépendante contre un attaquant du LAN qui aurait lu cette capacité. Cette phase exige un LAN maîtrisé et une fenêtre courte explicitement approuvés ; sinon l'installation reste bloquée jusqu'à mise en place d'un transport de confiance. Le clair du mot de passe et la clé privée hôte ne transitent pas en HTTP. Le hash SHA-512 du mot de passe aléatoire fort reste exposé dans le futur initrd et justifie son retrait après usage.

Aucune clé publique de déploiement autorisée n'a été trouvée parmi les fichiers .pub accessibles ni dans un agent SSH lors de cette préparation. Avant la phase B, sélectionner une identité existante autorisée ou autoriser une identité dédiée conservée sous private, sans changer les clés/configurations existantes de JARVIS. Aucun transfert manuel de clé n'est requis sur le Dell.

Après **autorisation administrative n°3** seulement, `takeover.py` :

- Épingle la clé hôte du rapport revu dans un known_hosts privé, refuse son changement et vérifie UUID/DMI par SSH.
- Utilise SSH_ASKPASS pour lire le secret local ; aucun sshpass ni mot de passe dans argv.
- Installe la clé publique autorisée dans jarvisadmin sans effacer ses clés existantes.
- Ouvre une connexion indépendante publickey-only, ControlMaster=no, vérifie DMI et sudo.
- Enregistre la preuve sur le Dell, puis seulement verrouille/expire le bootstrap, retire sudo et l'exception password, recharge SSH cible.
- Reteste une nouvelle connexion par clé et vérifie la révocation avant suppression des secrets locaux.

Une interruption avant preuve laisse le bootstrap disponible ; une interruption après preuve/revocation se reprend par clé. Aucun StrictHostKeyChecking=no, ssh-keyscan considéré comme preuve ou acceptation silencieuse d'une nouvelle clé hôte.

`configure.py` exige l'autorisation n°3 et une recette stockage privée liée au hash du manifeste (storage_acceptance_complete=true, dual_esp_boot_qualified=true). Il enchaîne takeover puis deux passes Ansible ; la seconde doit être sans changement, échec ou hôte inaccessible. L'inventaire généré reste bloqué tant que la réception stockage n'est pas explicitement vraie. Les rôles existants sont protégés par la preuve de takeover et un contrôle RAID en lecture seule.

NVIDIA/CUDA/Ollama restent différés/exclus. Leur déploiement futur ne demande aucune réinstallation Debian. Aucun essai ou configuration de la seconde RTX 3090 non alimentée n'a été réalisé. Le rôle JARVIS ne devient pas une intégration cluster opérationnelle du fait de ces scripts.

## Validation effectuée et limites

22 tests unittest passent : 16 historiques et 6 nouveaux cas agrégés couvrant manifeste, approbations, échec avant clé et transition réussie simulée. Le test du récepteur couvre IP/jeton/tailles/intégrité du rapport, stockage 0600 et affichage, sans ouvrir de socket. Deux playbooks passent syntax-check. Politique SSH cible évaluée avec sshd -T dans un fichier isolé et une clé hôte éphémère : password seulement pour bootstrap depuis JARVIS, root interdit. Aucun daemon SSH lancé ni configuration hôte touchée.

Les archives générées ont été inspectées : découverte = trois fichiers attendus, aucun preseed RAID/hash de mot de passe/autorisation ; installation synthétique = hash seulement, aucun clair, aucune autorisation d'effacement/confirmation/reboot. Le candidat synthétique est supprimé. Scripts shell acceptés par sh et collecteur/wrapper par le BusyBox extrait de l'initrd. dnsmasq --test et nft --check passent, aucun service LAN activé. Aucun test VM, partitionnement, installation, SSH réel Dell ou Ansible appliqué lors de cette préparation. Les tests du takeover simulent le transport : ils prouvent l'ordre des décisions, pas une connexion réelle.

Référence Debian utilisée : [preseed trixie, comptes et partitionnement](https://www.debian.org/releases/trixie/amd64/apbs04.en.html). Elle ne qualifie pas à elle seule notre recette.

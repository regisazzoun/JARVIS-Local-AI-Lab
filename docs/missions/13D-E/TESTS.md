# Tests et preuves — 15 octobre 2026

Exécutés dans la session de préparation :

- `python3 -m unittest discover -s deployment/13de/tests -v` : 6 tests réussis. Refus de chemins arbitraires, symlink workspace, symlink imbriqué, destruction sans propriété ; destruction limitée au workspace marqué ; refus des actifs absents. Ce sont des tests du contrôleur sur dossiers temporaires, pas des VM ni une démonstration agentique.
- `sh -n deployment/13de/debian/install-ssh.sh` : syntaxe shell acceptée. Aucun `in-target` exécuté.
- Comparaison SHA-256 avant/après : `sshd_config` et politique laboratoire 13F identiques. Hashes gardés hors publication.
- Relecture de SUIVI : aucune ligne de mission historique supprimée, sections et colonnes conservées ; une ligne 13D-E actualisée et entrée de journal ajoutée.

Non exécutés : syntax-check Ansible et convergence réelle, VM/TCG/KVM, firmware UEFI, requêtes PXE/TFTP/HTTP réelles, installation Debian, injection clé en invité, premier boot disque, SSH invité, RAID1/démarrage dégradé, NVIDIA/CUDA/Ollama cible, modèle local et reprise longue.

Les fichiers protégés et services n'ont reçu aucune commande d'écriture. Les seules écritures sont les livrables sous mission13de, des dossiers de tests temporaires et la publication sur branche dédiée. Pas d'élévation, d'installation, de reboot, de DHCP hôte ou de contact Dell.

## Reprise physique — résultats exécutés le 15 octobre 2026

| Contrôle | Résultat | Limite |
| --- | --- | --- |
| Outillage et services | Versions auditées ; réseau et sockets lisibles | Pas de scan des clients LAN |
| KVM | Ouverture `/dev/kvm` : EACCES | Aucune permission modifiée ; TCG disponible |
| Tests Python | 16 tests réussis : 6 historiques + 10 sélection physique | Cas synthétiques, pas de lecture des SSD Dell |
| Ansible | `site.yml` et `dell.yml` syntax-check réussis sous 2.19.11 | Aucun rôle appliqué à l'hôte ni au Dell |
| Refus Ansible physique | `dell.yml --check` avec inventaire livré : scope refusé, changed=0, aucune connexion cible | Échec intentionnel ; pas une preuve d'idempotence |
| Garde shell physique | Exécution sur hôte : STOP vendor, code 1 | Aucun chemin d'écriture dans la garde |
| Sources Debian | Release.gpg vérifié par gpgv ; SHA256SUMS lié au Release, payloads liés au manifeste | Assets privés non publiés ; current doit être repinné à chaque nouvelle acquisition |
| QEMU ciblé | TCG, 1 vCPU, 768 Mio, sans disque et `-nic none` ; noyau puis interface Debian Installer démarrés | Arrêt volontaire à 20 s, code timeout 124 ; avertissement low-memory attendu ; aucun test UEFI/PXE ou installation complète |
| ProxyDHCP | Template rendu avec IP/MAC de documentation, `/usr/sbin/dnsmasq --test` : syntax check OK | Aucun socket DHCP/TFTP ouvert ; coexistence Bbox à tester après accord |
| HTTP | Serveur éphémère loopback, linux et initrd.gz récupérés ; SHA256 identiques, serveur fermé | Aucun service HTTP LAN démarré |
| Initrd candidat | Construction avec manifeste/clé publique synthétiques ; seconde archive cpio décompressée et inspectée | Contient cinq fichiers attendus et aucune autorisation d'effacement ; pas une installation qualifiée |
| Scripts | Compilation Python et syntaxe shell réussies ; diff sans erreur d'espacement | Recette partman candidate non exécutée |

Empreintes acquises, sans identifiants de matériel privé :

```text
linux       2b2358b37674d2505350528875bb17afae2a36522a9e8a9417eaca65a7da0e08
initrd.gz   57303d157cffce3fa402301667fbc9b2280aa7372082b081e777375ae49da5f2
snponly.efi 9a624b4e05ebc25718a7658356628a352532bd278e7a50465a36ab94a7c4e580
ipxe.iso    4f158a0f2d41e9564d7a9b57fcbb60fbddd95b152a5e60a4e27044d0dc194404
```

Les logs bruts, manifeste synthétique, paramètres réseau et téléchargements sont conservés localement sous `deployment/13de/private/`, ignoré par Git. Le code de vérification permet de reproduire les contrôles ; les tests sur matériel, le double démarrage NVMe et les deux passes Ansible seront consignés seulement après exécution autorisée.


## Bootstrap A/B — 16 octobre 2026

- 22 tests unittest réussis (16 historiques + 6 nouveaux tests agrégés) : extraction du manifeste, refus séries/chemins dupliqués et disque inattendu, absence d'autorisation administrative, hash/expiration d'approbation, absence de révocation si clé indépendante échoue, parcours de succès simulé et suppression du secret seulement après preuve.
- Test récepteur sans socket : IP/jeton incorrects, GET authentifié, POST excessif/tronqué, enregistrement 0600, affichage du rapport. Aucun service réseau lancé pour ce test.
- sshd -T sur configuration isolée et clé hôte éphémère : mot de passe pour bootstrap depuis JARVIS seulement ; refus root, autre source et jarvisadmin par mot de passe. Aucun daemon/configuration hôte modifié.
- site.yml et dell.yml passent syntax-check avec inventaires explicites ; aucun playbook appliqué.
- Archive initrd découverte inspectée : exactement trois fichiers ajoutés, aucun hash de mot de passe/recette partitionnement/autorisation. Deux scripts validés par le BusyBox extrait de l'initrd réellement utilisé.
- Construction d'un candidat d'installation synthétique : hash SHA-512 embarqué, aucun clair, aucun approved-erase/approved-reboot ni confirmations. Artefact temporaire supprimé.
- dnsmasq --test et nft --check passent ; aucune activation LAN, aucun test VM et aucune écriture Dell.

Limites : early_command/netcfg automatique encore à éprouver physiquement ; les tests de takeover simulent SSH. Recette RAID/ESP, double boot, accès SSH réel, convergence/idempotence Ansible et GPU/IA restent à réceptionner. Voir BOOTSTRAP-AUTOMATISE.md.


### Correctif découverte automatique — 16 octobre, après premier essai

Téléchargement physique confirmé, rapport absent, écran curseur seul. Pilotes NVMe absents du netboot initial : correction par trois modules Debian authentifiés, DHCP BusyBox et affichage tty1/nomodeset. Test TCG ciblé sans disque ni réseau : nvme-auth, nvme-core et nvme se chargent avec succès, marqueur JARVIS_NVME_DRIVER_OK. Aucun benchmark ni écriture disque ; pas de validation RAID/EFI ou de campagne PXE/VM. Tests 22 + récepteur et syntaxes restent réussis. Reprise physique requise avec l'image corrigée.


## Découverte automatique physique reçue — 16 octobre 2026, 19:24

Le Dell affiche « rapport envoyé, attente de revue humaine ». Rapport complet reçu et empreinte vérifiée ; réception et inventaire brut conservés uniquement sous private, permissions 0600. Services ProxyDHCP/TFTP/HTTP/récepteur automatiquement arrêtés et filtre temporaire retiré ; SSH/Tailscale/NetworkManager restent actifs. Aucune installation/écriture NVMe.

Données mesurées : Precision 5820 Tower X-Series, Core i9-10980XE, 36 processeurs logiques, MemTotal 263631232 kB ; deux NVMe KIOXIA KXG70PNV2T04 et Samsung PM9A1, chacun 2048408248320 octets. Les deux disques ont déjà des partitions. Un seul contrôleur graphique NVIDIA est exposé par le rapport PCI ; aucune opération sur la seconde carte et aucune validation CUDA. /proc/mdstat absent : absence de RAID non démontrée.

**NO-GO installation maintenu.** Le manifeste d'installation a été refusé : périphérique supplémentaire /dev/sda, SD/MMC CRW, taille nulle, et produit DMI « Precision 5820 Tower X-Series » différent du profil strict historique « Precision 5820 Tower ». Les séries et UUID sont conservés dans l'inventaire privé ; aucun identifiant matériel unique publié. Ne pas ignorer globalement les disques supplémentaires : identifier/qualifier le lecteur sans média avant révision précise de la politique. Autre écart à revoir : BIOS DMI 2.8.0 daté du 15 janvier 2021, alors que 2.24.0 avait été annoncé ; aucune modification firmware autorisée ou effectuée.

Découverte automatique réalisée et reçue ; qualification RAID/deux ESP, approbation d'effacement portant sur les séries réelles, identité SSH permanente et autorisation administrative restent à obtenir.

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

# Tests et preuves — 15 octobre 2026

Exécutés dans la session de préparation :

- `python3 -m unittest discover -s deployment/13de/tests -v` : 6 tests réussis. Refus de chemins arbitraires, symlink workspace, symlink imbriqué, destruction sans propriété ; destruction limitée au workspace marqué ; refus des actifs absents. Ce sont des tests du contrôleur sur dossiers temporaires, pas des VM ni une démonstration agentique.
- `sh -n deployment/13de/debian/install-ssh.sh` : syntaxe shell acceptée. Aucun `in-target` exécuté.
- Comparaison SHA-256 avant/après : `sshd_config` et politique laboratoire 13F identiques. Hashes gardés hors publication.
- Relecture de SUIVI : aucune ligne de mission historique supprimée, sections et colonnes conservées ; une ligne 13D-E actualisée et entrée de journal ajoutée.

Non exécutés : syntax-check Ansible et convergence réelle, VM/TCG/KVM, firmware UEFI, requêtes PXE/TFTP/HTTP réelles, installation Debian, injection clé en invité, premier boot disque, SSH invité, RAID1/démarrage dégradé, NVIDIA/CUDA/Ollama cible, modèle local et reprise longue.

Les fichiers protégés et services n'ont reçu aucune commande d'écriture. Les seules écritures sont les livrables sous mission13de, des dossiers de tests temporaires et la publication sur branche dédiée. Pas d'élévation, d'installation, de reboot, de DHCP hôte ou de contact Dell.

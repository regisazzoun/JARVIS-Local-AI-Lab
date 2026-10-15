# Reprise 13D-E — GO AVEC RÉSERVES pour la préparation physique

La préparation progresse vers le Dell sans imposer un laboratoire virtuel complet. Aucun Dell installé et aucune autorisation de lancement physique déduite de ce verdict. Le NO-GO historique reste conservé ci-dessous avec son contexte.

Livré et contrôlé : audit hôte accessible, sources Debian authentifiées, templates ProxyDHCP limité au MAC Dell/TFTP/HTTP, iPXE de découverte, manifeste matériel et garde pré-partitionnement, builder d'initrd sans autorisation d'effacement, preseed RAID candidat, playbook physique verrouillé, procédures réseau/RAID/SSH/reprise/intégration. 16 tests passent, deux playbooks passent le syntax-check, HTTP loopback et démarrage Debian Installer TCG ciblé réalisés. Aucun service LAN PXE activé, accès hôte conservés.

**Réserves empêchant le lancement immédiat de l'installation :**

- Plan réseau exact, interface d'écoute, MAC Dell et effets LAN à approuver humainement avant activation.
- Identités Dell/CPU/GPU/contrôleur/SSD et mode VROC inconnus ; manifeste réel à valider avant toute écriture.
- Recette partman RAID candidate non qualifiée, double ESP et démarrage depuis chacun des NVMe à tester ; aucun effacement autorisé.
- Clé publique de déploiement réelle à sélectionner et vérifier ; premiers SSH et idempotence Ansible non testés faute de Debian cible.
- Rôles NVIDIA/CUDA/Ollama encore différés ; worker et intégration JARVIS non réceptionnés. Ces étapes ne doivent pas être présentées comme opérationnelles.
- Accès utilisateur KVM refusé, sans impact sur la préparation physique ; TCG testé.

La prochaine étape est une séance de découverte et la qualification ciblée du stockage, suivies des autorisations distinctes réseau et installation. Les commandes et conditions exactes sont dans [la procédure physique](DEPLOIEMENT-PHYSIQUE.md), les preuves dans [les tests](TESTS.md). Ce GO AVEC RÉSERVES porte sur l'avancement préparatoire ; il ne vaut pas GO de mise en service ni clôture des réserves de recette.

**ROADMAP ↔ SUIVI synchronisés, format SUIVI conservé.** Publication sur `codex/mission-13de-preparation`, sans fusion dans main.

---

## Rapport historique de la première exécution (conservé)

# Réception 13D-E — NO-GO pour réception complète

La préparation documentaire et une première base de code sont livrées. Les critères de réception ne sont pas tous atteints : aucun essai PXE/UEFI réel, aucune installation VM et aucune exécution Ansible ne sont possibles dans les capacités actuellement exposées à cette session. La mission n'est donc **pas déclarée achevée techniquement**. NO-GO pour lancer 14A avec cette chaîne, et pour tout déploiement Dell. Ce verdict n'annule pas le GO historique des accès 13D ou les preuves 13F.

| Domaine | Preuve acquise | Réserve / verdict |
| --- | --- | --- |
| Infrastructure JARVIS | Aucun changement système, modèle, base, disque physique ou service | Santé courante inaccessible ; absence de dégradation non certifiable |
| SSH | sshd_config identique avant/après ; aucun accès ni clé modifié | Procédure et script invités seulement ; aucune connexion Dell attendue |
| Tailscale | Aucun fichier/commande de configuration modifié | Service non inspectable dans cette session |
| Ansible | Inventaires lab/Dell, playbook et neuf rôles distincts | Absent ; syntax-check et idempotence non testés ; trois rôles IA explicitement différés |
| PXE/Debian | Script iPXE, template preseed, injection SSH préparés | Pas d'essai réel ; HTTP/mirror isolé et recette RAID1 exécutables non livrés |
| Laboratoire | Contrôleur TCG préparé ; six tests de garde-fous passent | QEMU/OVMF absents ; KVM non accessible ; boucle complète non fonctionnelle |
| Agent JARVIS | Contrat d'outils bornés et recette 14A documentés | Aucun raccordement à 13F ni service de tâches durable ; aucune autonomie simulée |
| Dell | Aucune intervention | Contrôleur, SSD, RAID et firmware toujours à identifier avant décision destructive |
| Documentation | Audit, architecture, SSH, laboratoire, agent, tests, incidents ; roadmap/suivi synchronisés | Publication sur branche dédiée, sans fusion automatique |

## Suite nécessaire

1. Rendre disponibles les outils utilisateur et firmware authentifiés dans un environnement permettant QEMU TCG ; un diagnostic/une validation ciblée reste requis avant toute installation système à risque.
2. Fournir une source de paquets hors ligne isolée, un transport SSH invité et un profil de second boot disque ; compléter HTTP si retenu.
3. Sélectionner une clé publique existante dont JARVIS contrôle le signataire ; produire l'initrd privé et vérifier le compte SSH.
4. Exécuter installation VM, Ansible deux fois, collecte complète des journaux ; développer et éprouver le RAID1 en VM.
5. Raccorder le worker à une copie de la passerelle avec superviseur durable et quotas, puis faire réaliser la recette 14A par le modèle local.

Les essais VM jetables restent autorisés sans confirmation par essai. Les obstacles actuels sont l'absence d'outils et les capacités de la session, pas une demande d'approbation des essais virtuels. Aucun service sensible n'a été modifié pour les contourner.

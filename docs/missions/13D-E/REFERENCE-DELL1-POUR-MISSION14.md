# Dell Precision n°1 — Référence d'installation validée (mission 13)

**Date de consolidation :** 17 octobre 2026  
**Plateforme :** Dell Precision 5820 Tower X-Series, Debian 13  
**Sources prioritaires :** [réception matérielle et fonctionnelle](RECEPTION-MISSION14.md), [rapport final / incidents](RAPPORT-FINAL.md), [tests et chronologie](TESTS.md), [directives d'installation](PROMPT-INSTALLATION-AUTONOME.md).  
**État documentaire :** réception complète validée dans les rapports 13D-E/14 du 17 octobre ; les preuves brutes et secrets restent privés sur le contrôleur. Cette note ne vaut pas un nouveau test de la machine.

## 1. Objectif et règle de réutilisation

Cette installation fournit la **base technique acquise du Dell 1** pour les missions futures, dont la mission 14 et l'extension agentique 11B. Ne pas refaire la découverte PXE, la qualification RAID/ESP, l'installation Debian, les authentifications ou les tests GPU acquis, sauf changement réel ou incident démontré. Conserver le caractère historique des anciennes sections « NO-GO » et « INCOMPLET » ; le dernier verdict daté fait foi.

## 2. Matériel identifié

| Élément | Résultat documenté |
| --- | --- |
| Machine | Dell Precision 5820 Tower X-Series ; processeur Intel Core i9-10980XE, 36 threads |
| RAM | 263631232 kB de MemTotal lors de la découverte physique (configuration propriétaire : 256 Go) |
| Disques | Deux NVMe d'environ 2,048 To : KIOXIA KXG70PNV2T04 et Samsung PM9A1 ; identités exactes/UUID/séries dans le manifeste privé |
| RAID système | RAID1 Linux mdadm, miroir vérifié sain [UU] après synchronisation ; conservation GPT/partitions et deux ESP indépendantes |
| Carte graphique vérifiée | RTX 3090 avec 24 576 MiB de VRAM détectée ; pilote 550.163.01 |
| Firmware | BIOS DMI 2.8.0 relevé lors de la découverte ; aucune modification de firmware revendiquée |

Ne jamais sélectionner un disque par /dev/nvme* ou par taille seule ; reprendre l'identification du manifeste privé pour toute action sur les disques. Aucun test réel d'extraction de disque n'a été effectué.

## 3. Déploiement réellement réceptionné

1. **Démarrage réseau :** chaîne PXE physique UEFI IPv4 validée : snponly.efi → iPXE → noyau/initrd → installateur Debian. La Bbox reste serveur DHCP ; services temporaires du contrôleur arrêtés après réception.
2. **Stockage :** réinstallation de Debian avec conservation prioritaire des structures RAID/GPT/ESP existantes. Miroir mdadm [UU], synchronisation terminée ; deux ESP indépendantes et copies EFI vérifiées.
3. **Système :** Debian installé ; redémarrage final démontré par changement de boot ID et nouvelles connexions indépendantes.
4. **Comptes et accès :** `adminjarvis` par mot de passe **et** clé SSH, avec sudo vérifié indépendamment ; `jarvis-bootstrap` conservé suivant la directive propriétaire. Secours par mot de passe conservé. Clavier français AZERTY exigé et corrigé lors de la reprise.
5. **Ansible :** deux passes réalisées ; seconde passe `changed=0 failed=0 unreachable=0`.
6. **NVIDIA / CUDA / Ollama :** `nvidia-smi` sur RTX 3090 ; allocation GPU réelle observée lors d'inférences. Ollama **0.40.3**, API accessible depuis le Mac mini et service activé.
7. **Modèles testés :** `qwen3.5:27b-q4_K_M`, `ministral-3:14b-instruct-2512-q4_K_M`, `llama3.1:8b`. Ces noms sont ceux de la réception, pas une promesse de modèles disponibles en permanence.
8. **Intégration :** passerelle authentifiée, Open WebUI, mémoire canonique SQLite/FTS5, outil agentique et voix testés ; la voix a utilisé un WAV synthétique, pas de microphone réel.
9. **Graphique :** KDE Plasma/X11 installé ; SDDM activé ; ouverture de session interactive graphique **non vérifiée**.
10. **Nettoyage :** services réseau temporaires du contrôleur arrêtés ; accès de secours conservés par décision propriétaire.

## 4. Architecture réutilisable

- **Mac mini Debian :** pilotage conversationnel, voix Whisper/Piper, mémoire SQLite/FTS5, outils agentiques, GitHub, orchestration.
- **Dell 1 :** moteur distant de calcul GPU, Ollama et modèles ; API accessible par le Mac mini.
- **SSH/Ansible :** `adminjarvis`, accès et élévation testés en mission d'installation. Attention : l'agent conversationnel dispose séparément d'une **politique de broker** ; le profil `dell-observe` de la mission 11 n'autorisait que la lecture, même lorsque les comptes SSH existaient. L'extension 11B doit adapter et tester les habilitations distantes persistantes, sans recréer les comptes ni le serveur.

## 5. Problèmes rencontrés et corrections capitalisées

| Incident | Solution ou état acquis |
| --- | --- |
| Initrd de découverte initial sans pilotes NVMe | Modules Debian NVMe ajoutés et découverte physique relancée avec succès |
| Écart DMI X-Series et lecteur SD vide | Politique d'identification affinée sans désactiver les contrôles des disques |
| Échec de bootstrap/retour premier boot et clavier QWERTY | Reprise supervisée, configuration SSH/comptes et clavier français corrigées |
| Transfert des modèles bloqué par permissions `/var/lib/ollama` | Transfert corrigé au moyen de `sudo rsync` sur la cible |
| Erreur d'authentification passerelle | Corrigée ; intégration JARVIS finalement testée |
| Resynchronisation intégrale après reboot forcé de l'installateur | Miroir finalement sain et reboot normal validé ; **reste un défaut du contrôleur de réinstallation** |

**Défaut technique connu à ne pas recopier :** `serve-supervised.py` comporte encore `sync; reboot -f` pour le passage installateur → Debian. Le rapport signale que ce redémarrage forcé a probablement contribué à la resynchronisation ; sa cause exclusive n'est pas démontrée. Corriger ce chemin avant de promettre qu'une prochaine installation conservera un RAID synchronisé sans nouvelle resynchronisation. `finish-ai.py` a été corrigé pour attendre la fin du RAID et utiliser un redémarrage normal.

## 6. Prérequis pratiques pour la mission 14

- Consulter **en premier** `AGENTS.md`, `docs/CHARTE_DIRECTIVES_JARVIS.md`, le dernier `SUIVI.md` et la réception datée `RECEPTION-MISSION14.md` ; distinguer décisions récentes et consignes historiques.
- Reprendre les rôles Ansible, templates, superviseur PXE, contrats SSH et procédures de diagnostic **en conservant leur historique et sans copier les identités matérielles du Dell 1 vers une autre cible**.
- Pour une machine distincte, établir son inventaire matériel et son autorisation propre avant les opérations destructives. Ne jamais extrapoler les deux NVMe ou leur manifeste.
- Réutiliser les sources privées uniquement sur les machines qui y ont droit ; ne pas les committer.
- Rejouer seulement les contrôles nécessaires sur la cible de mission 14 : identité, stockage, boot, accès SSH et sudo, convergence Ansible, pilotes/GPU, inférence Ollama, intégration JARVIS.
- Distinguer les droits SSH réels de la **politique agentique** `/etc/jarvis/host-policy.json`. Une permission de lecture seule de l'agent n'invalide pas la recette SSH ; elle nécessite un raccordement distinct dans une mission qui l'autorise.
- Conserver le DHCP Bbox, les services du Mac mini, ses comptes, Tailscale et la mémoire canonique.

## 7. Réserves finales

- Aucun test physique de retrait NVMe ni de fonctionnement dégradé réel.
- Session graphique KDE interactive non démontrée.
- Microphone/haut-parleurs physiques non testés.
- Défaut de reboot forcé du **script de déploiement**, malgré reboot final Dell validé.
- Les permissions distantes du broker agentique et les tests de mission 11B sont un chantier distinct de l'installation 13D-E.

## 8. Traçabilité et verdict

**Installation Dell 1 : RÉCEPTION COMPLÈTE VALIDÉE (17 octobre 2026), avec réserves documentées.** Ce résultat provient du rapport de réception, non d'un nouvel accès au Dell pendant cette consolidation.

Les détails sensibles (clés, secrets, numéros de série, UUID et preuves brutes) restent sous `deployment/13de/private/reinstall-02` et ne doivent pas être publiés.

**Directives consultées :** `AGENTS.md`, `docs/CHARTE_DIRECTIVES_JARVIS.md`, réception `RECEPTION-MISSION14.md`, `RAPPORT-FINAL.md`, `TESTS.md`. **Autorisations préservées :** autonomie dans les périmètres autorisés, absence de validation intermédiaire inventée, préservation des ressources et comptes existants. **Écart signalé :** anciennes restrictions et statuts historiques ne remplacent pas la réception finale.
